#!/usr/bin/env python3
"""What a change costs each workflow walk: the base against the branch. Standard library only.

    python3 walkcost.py --samples walks.jsonl --policy walk-cost.json \
        [--base-policy base-walk-cost.json] [--body pr-body.md] [--out report.md] [--gate]

Copied into a consuming repository by livespec's setup, which writes the
version it copied on the first line. The walks are the repository's own; this
only reads what they wrote, one JSON object a line:

    {"workflow": "checkout", "layer": "front end", "measure": "requests", "side": "base", "value": 42}

`side` is `base` or `branch`; `layer`, optional, is where the walk was measured:
the front end with the service's answers replayed, the back end with no
browser, or end to end. Both sides are walked on one runner, in one job,
in turns, so whatever slows the runner slows both. The policy file:

    {"rounds": 5,
     "measures": {"load-ms": {"kind": "time", "noise": 3, "allowance": 10},
                  "requests": {"kind": "count", "allowance": 0}},
     "budgets": {"checkout": {"requests": 42}}}

noise and allowance are percentages. A count compares the medians of the two
sides; a time takes the median of the pairwise log ratios and its 95% interval
from the Mann-Whitney rank statistic. Nothing is random: the same samples give
the same report. A walk past its allowance is answered by naming its workflow
under `## Performance` in the pull request's body, passed as --body. Exit 0;
1 when --gate is given and a count is over its budget or, with --body, a walk
past its allowance goes unanswered; 2 when the policy is refused. See livespec's method/gates.md, What a change
costs a workflow.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path

Z95 = 1.959964
ORDER = ["over budget", "past its allowance", "within its allowance", "inconclusive", "better", "no change"]


class Refused(Exception):
    pass


def load_policy(path: str) -> dict:
    try:
        policy = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise Refused(f"{path}: cannot be read as JSON ({exc})")
    measures = policy.get("measures")
    if not isinstance(measures, dict) or not measures:
        raise Refused(f"{path}: names no measures")
    for name, spec in measures.items():
        kind = spec.get("kind")
        if kind not in ("time", "count"):
            raise Refused(f"{path}: measure {name} is {kind!r}; a measure is a time or a count")
        if kind == "time" and ("noise" not in spec or "allowance" not in spec):
            raise Refused(f"{path}: the time {name} needs its noise and its allowance, decided before anything runs")
        if "budget" in spec:
            raise Refused(f"{path}: {name} carries a budget of its own; budgets are set per walk, under budgets")
    for workflow, budgets in (policy.get("budgets") or {}).items():
        for name in budgets:
            if name not in measures:
                raise Refused(f"{path}: the {workflow} walk has a budget on {name}, which the policy does not measure")
            if measures[name]["kind"] == "time":
                raise Refused(f"{path}: the {workflow} walk has a budget on {name}, a time; a time cannot carry a budget, "
                              "because a shared runner's noise would decide it. Report it, and budget a count that stands in for it")
    return policy


def load_samples(path: str) -> dict:
    found: dict = {}
    for number, line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
            key = (str(row["workflow"]), str(row.get("layer") or ""), str(row["measure"]))
            side = row["side"]
            value = float(row["value"])
        except (ValueError, KeyError, TypeError) as exc:
            raise Refused(f"{path}:{number}: not a sample ({exc})")
        if side not in ("base", "branch"):
            raise Refused(f"{path}:{number}: side is {side!r}, not base or branch")
        found.setdefault(key, {"base": [], "branch": []})[side].append(value)
    return found


def median(values: list) -> float:
    ordered = sorted(values)
    middle = len(ordered) // 2
    return ordered[middle] if len(ordered) % 2 else (ordered[middle - 1] + ordered[middle]) / 2


def number(value: float) -> str:
    return str(int(value)) if value == int(value) else f"{value:.1f}"


def pct(value: float) -> str:
    return "+∞%" if math.isinf(value) else f"{value:+.1f}%"


def judge_count(base: list, branch: list, spec: dict, budget) -> dict:
    b, h = median(base), median(branch)
    row = {"base": number(b), "branch": number(h)}
    if min(base) != max(base) or min(branch) != max(branch):
        return {**row, "verdict": "inconclusive", "change": "—",
                "why": "it varies between rounds of one side, so it is not a count and carries no verdict"}
    change = (h - b) / b * 100 if b else (0.0 if h == b else math.inf)
    row["change"] = f"{h - b:+g} ({pct(change)})" if h != b else "—"
    if budget is not None and h > budget:
        return {**row, "verdict": "over budget", "why": f"{number(h)} against a budget of {number(budget)}"}
    if h == b:
        return {**row, "verdict": "no change", "why": ""}
    if h < b:
        return {**row, "verdict": "better", "why": ""}
    allowance = float(spec.get("allowance", 0))
    verdict = "within its allowance" if change <= allowance else "past its allowance"
    return {**row, "verdict": verdict, "why": f"allowance {allowance:g}%"}


def judge_time(base: list, branch: list, spec: dict) -> dict:
    row = {"base": number(median(base)), "branch": number(median(branch)), "change": "—"}
    if min(base + branch) <= 0:
        return {**row, "verdict": "inconclusive", "why": "a time of zero or less cannot be compared as a ratio"}
    diffs = sorted(math.log(h) - math.log(b) for b in base for h in branch)
    m, n = len(base), len(branch)
    k = math.floor(m * n / 2 - Z95 * math.sqrt(m * n * (m + n + 1) / 12))
    if k < 0:
        return {**row, "verdict": "inconclusive",
                "why": f"too few rounds to bound the change: {m} on the base, {n} on the branch"}
    est, lo, hi = (100 * math.expm1(x) for x in (median(diffs), diffs[k], diffs[m * n - 1 - k]))
    noise, allowance = float(spec["noise"]), float(spec["allowance"])
    shown = f"{pct(est)} ({pct(lo)} … {pct(hi)})"
    if hi <= noise:
        verdict = "better" if hi < -noise else "no change"
        return {**row, "verdict": verdict, "change": shown if verdict == "better" else "—", "why": ""}
    if lo > noise:
        verdict = "within its allowance" if est <= allowance else "past its allowance"
        return {**row, "verdict": verdict, "change": shown, "why": f"allowance {allowance:g}%"}
    return {**row, "verdict": "inconclusive", "change": shown,
            "why": f"the interval reaches both sides of the {noise:g}% noise; more rounds would decide it"}


def compare(samples: dict, policy: dict) -> list:
    rows = []
    for (workflow, layer, measure), sides in sorted(samples.items()):
        spec = policy["measures"].get(measure)
        row = {"workflow": workflow, "walk": f"{workflow} · {layer}" if layer else workflow, "measure": measure}
        if spec is None:
            rows.append({**row, "verdict": "inconclusive", "base": "—", "branch": "—", "change": "—",
                         "why": "the policy names no such measure"})
            continue
        missing = [side for side in ("base", "branch") if not sides[side]]
        if missing:
            rows.append({**row, "verdict": "inconclusive", "base": "—", "branch": "—", "change": "—",
                         "why": f"the {missing[0]} has no samples"})
            continue
        if spec["kind"] == "count":
            budget = (policy.get("budgets") or {}).get(workflow, {}).get(measure)
            rows.append({**row, **judge_count(sides["base"], sides["branch"], spec, budget)})
        else:
            rows.append({**row, **judge_time(sides["base"], sides["branch"], spec)})
    return sorted(rows, key=lambda r: (ORDER.index(r["verdict"]), r["walk"], r["measure"]))


def flatten(policy: dict) -> dict:
    flat = {"rounds": policy.get("rounds")}
    for name, spec in policy.get("measures", {}).items():
        for key in ("noise", "allowance"):
            flat[f"{name} {key}"] = spec.get(key)
    for workflow, budgets in (policy.get("budgets") or {}).items():
        for name, value in budgets.items():
            flat[f"the {workflow} walk's {name} budget"] = value
    return flat


def moved(base: dict, branch: dict) -> list:
    old, new = flatten(base), flatten(branch)
    lines = []
    for key in sorted(set(old) | set(new)):
        a, b = old.get(key), new.get(key)
        if a == b:
            continue
        if a is None:
            lines.append(f"{key}: set to {b}")
        elif b is None:
            lines.append(f"{key}: removed, was {a}")
        else:
            lines.append(f"{key}: moved from {a} to {b}")
    return lines


def answers(body: str) -> list:
    """The lines of the body's ## Performance section."""
    match = re.search(r"^##\s+Performance\s*$(.*?)(?=^##\s|\Z)", body, re.M | re.S)
    lines = match.group(1).splitlines() if match else []
    return [line.strip().lstrip("-* ").strip() for line in lines if line.strip()]


def answer(rows: list, lines: list) -> list:
    """Quote the line naming each walk past its allowance; return the walks nothing answers."""
    unanswered = []
    for r in rows:
        if r["verdict"] != "past its allowance":
            continue
        named = re.compile(rf"(?<![\w-]){re.escape(r['workflow'])}(?![\w-])")
        line = next((l for l in lines if named.search(l)), None)
        if line:
            r["why"] += f"; answered: “{line}”"
        else:
            unanswered.append(f"the {r['walk']} walk's {r['measure']} is past its allowance, "
                              f"and the pull request does not name {r['workflow']} under ## Performance")
    return unanswered


def report(rows: list, changes: list, failures: list) -> str:
    out = ["### What this change costs each workflow walk", ""]
    listed = [r for r in rows if r["verdict"] != "no change"]
    quiet = [f"{r['walk']} · {r['measure']}" for r in rows if r["verdict"] == "no change"]
    if listed:
        out += ["| Walk | Measure | Base | Branch | Change | Verdict |", "|---|---|---|---|---|---|"]
        for r in listed:
            verdict = f"**{r['verdict']}**" + (f" — {r['why']}" if r["why"] else "")
            out.append(f"| {r['walk']} | {r['measure']} | {r['base']} | {r['branch']} | {r['change']} | {verdict} |")
        out.append("")
    if quiet:
        out += [f"**No change:** {', '.join(quiet)}.", ""]
    if not rows:
        out += ["No walk wrote a sample.", ""]
    if changes:
        out += ["**The policy moved in this pull request:**", ""] + [f"- {line}" for line in changes] + [""]
    if failures:
        out += ["**The gate fails:** " + "; ".join(failures) + ".", ""]
    return "\n".join(out)


def main(argv: list) -> int:
    parser = argparse.ArgumentParser(description="What a change costs each workflow walk, base against branch.")
    parser.add_argument("--samples", required=True)
    parser.add_argument("--policy", required=True, help="the branch's policy file")
    parser.add_argument("--base-policy", help="the base's policy file, to show what moved")
    parser.add_argument("--body", help="the pull request's body, whose ## Performance section answers a walk past its allowance")
    parser.add_argument("--out", help="also write the report here")
    parser.add_argument("--gate", action="store_true", help="exit 1 when a count is over its budget")
    args = parser.parse_args(argv)
    try:
        policy = load_policy(args.policy)
        changes = moved(load_policy(args.base_policy), policy) if args.base_policy else []
        rows = compare(load_samples(args.samples), policy)
    except Refused as exc:
        print(f"walkcost: refused — {exc}", file=sys.stderr)
        return 2
    failures = [f"the {r['walk']} walk's {r['measure']} is {r['why']}" for r in rows if r["verdict"] == "over budget"]
    if args.body:
        failures += answer(rows, answers(Path(args.body).read_text(encoding="utf-8")))
    text = report(rows, changes, failures if args.gate else [])
    print(text)
    if args.out:
        Path(args.out).write_text(text + "\n", encoding="utf-8")
    return 1 if args.gate and failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
