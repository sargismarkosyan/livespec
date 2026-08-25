#!/usr/bin/env python3
"""Run the eval suite: both arms, judged, summarised as delta.

The native runner for this case format — `claude plugin eval` — is gated behind
early access and has never started on this account, so the suite runs on
promptfoo instead: this script compiles `evals/<NN-case>/` into a promptfoo
config, runs each case through `claude -p` with the plugin loaded and without
(provider.py), grades what came out (asserts.py), and reports the difference.
The case folders stay authoritative and stay in the native format; if
enablement ever arrives, both runners read the same folders.

The flags are the suite's contract, unchanged from the native invocation:
`--ablation with-without` is the only mode there is, `--judge-model` names the
judge (sonnet or larger, never the model under test), and `--allow-tools` is an
operator grant — a gated tool a case asks for but the grant omits is stripped,
exactly as the native CLI behaves, and stripped tools are warned about because
a grader that could never fail proves nothing.

    python3 evals/runner/run.py --ablation with-without --judge-model sonnet \
        --allow-tools Write Edit [--case NAME] [--runs N] [--model M]

Costs real money per session and never runs in CI. Exit 0 is a completed
measurement, whatever the scores; only a harness failure exits 1. No number
from here is trusted before a read-every-verdict calibration — evals/README.md.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".github" / "scripts"))
from caselib import cases, frontmatter, measurement_inputs  # noqa: E402

PROMPTFOO = "promptfoo@0.122.0"  # pinned: a floating runner makes every delta a comparison across two runners

# Mirrors GATED_TOOLS in .github/scripts/evalsuite.py — the operator grant the
# native CLI enforces, enforced here the same way.
GATED = {"Bash", "Write", "Edit", "WebFetch", "WebSearch"}


def compile_config(suite: list[dict], repeat: int, granted: set[str]) -> dict:
    tests = []
    for case in suite:
        prompt_file = next(s for s in case["sources"] if s.name == "prompt.md")
        fields, body = frontmatter(prompt_file)
        allowed = []
        for tool in case["allowed_tools"]:
            if (tool in GATED or tool.startswith("mcp__")) and tool not in granted:
                print(f"  ⚠ {case['name']} asks for {tool}; not granted — running without it")
                continue
            allowed.append(tool)
        asserts = []
        for grader in case["graders"]:
            entry = {
                "type": "python",
                "value": f"file://{ROOT / 'evals' / 'runner' / 'asserts.py'}",
                "config": {"grader": str(grader["path"].relative_to(ROOT))},
            }
            if grader["type"] == "tool_used" and not grader["fields"].get("max", "").strip().isdigit():
                entry["weight"] = 0  # the plugin-fired indicator never touches a score
            elif grader["fields"].get("weight", "").strip().isdigit():
                entry["weight"] = int(grader["fields"]["weight"])
            asserts.append(entry)
        tests.append({
            "description": case["name"],
            "vars": {
                "prompt": body.strip(),
                "case": case["name"],
                "allowed_tools": " ".join(allowed),
                "disallowed_tools": " ".join(sorted(GATED - set(allowed))),
                "max_turns": fields.get("max_turns", "25"),
                "timeout_seconds": fields.get("timeout_seconds", "600"),
            },
            "assert": asserts,
        })
    provider = f"file://{ROOT / 'evals' / 'runner' / 'provider.py'}"
    return {
        "description": "livespec eval suite — both arms",
        "prompts": ["{{prompt}}"],
        "providers": [
            {"id": provider, "label": "with-plugin", "config": {"with_plugin": True}},
            {"id": provider, "label": "without-plugin", "config": {"with_plugin": False}},
        ],
        "tests": tests,
        "evaluateOptions": {"repeat": repeat},
    }


BOARD = ROOT / "evals" / "board.json"


def load_board() -> dict:
    try:
        return json.loads(BOARD.read_text())
    except (OSError, json.JSONDecodeError):
        return {"format": 1, "cases": {}}


def collect(results_path: Path) -> tuple[dict, dict, int]:
    """Per-case scores, costs and fired-counts out of a promptfoo results file."""
    rows = json.load(results_path.open())["results"]["results"]
    stats: dict[str, dict] = defaultdict(lambda: {
        "with": [], "without": [], "cost": 0.0, "fired": [], "errors": 0,
    })
    for row in rows:
        name = (row.get("vars") or {}).get("case") or (row.get("description") or "?")
        arm = ((row.get("provider") or {}).get("label")) or "?"
        response = row.get("response") or {}
        stats[name]["cost"] += float(response.get("cost") or 0)
        grading = row.get("gradingResult") or {}
        if row.get("error") and not grading.get("componentResults"):
            # a genuine harness error — promptfoo also mirrors a failed judge's
            # reason into `error`, and that is a measurement, not an error
            stats[name]["errors"] += 1
            continue
        key = "with" if arm == "with-plugin" else "without"
        stats[name][key].append(float(grading.get("score") or 0))
        for component in grading.get("componentResults") or []:
            reason = component.get("reason") or ""
            if key == "with" and reason.startswith("plugin-fired indicator"):
                stats[name]["fired"].append("indicator: fired" in reason)
    cost = sum(s["cost"] for s in stats.values())
    return stats, {n: s for n, s in stats.items() if s["with"] and s["without"]}, len(rows)


def mean(values: list[float]) -> float:
    return sum(values) / len(values)


def print_summary(stats: dict, sessions: int) -> None:
    print(f"\n  {'case':<34} {'with':>5} {'w/out':>6} {'Δ':>6}   fired")
    total = []
    for name in sorted(n for n in stats if stats[n]["with"] or stats[n]["without"]):
        with_arm = stats[name]["with"] or [0.0]
        without = stats[name]["without"] or [0.0]
        delta = mean(with_arm) - mean(without)
        total.append(delta)
        flame = f"{sum(stats[name]['fired'])}/{len(stats[name]['fired'])}" if stats[name]["fired"] else "—"
        print(f"  {name:<34} {mean(with_arm):>5.2f} {mean(without):>6.2f} {delta:>+6.2f}   {flame}")
    for name in sorted(n for n in stats if stats[n]["errors"]):
        print(f"  ✘ {name}: {stats[name]['errors']} session(s) errored — see the run's sessions/ directory")
    if total:
        cost = sum(s["cost"] for s in stats.values())
        print(f"\n  suite Δ {mean(total):+.2f} over {len(total)} case(s), {sessions} session(s), ${cost:.2f}")
    print("  No number from here is calibrated until every verdict has been read — evals/README.md.")


def record(measured: dict, suite: list[dict]) -> None:
    """Update the board with what this run measured — and only that.

    An entry carries the number, its provenance, and a hash of what it was a
    measurement of; the board gate fails the entry when those inputs move on.
    A case whose sessions all errored is not recorded — a non-measurement is
    not a measurement of zero.
    """
    board = load_board()
    by_name = {case["name"]: case for case in suite}
    try:
        sha = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "--short", "HEAD"],
                             capture_output=True, text=True).stdout.strip() or "unknown"
    except OSError:
        sha = "unknown"
    for name, s in measured.items():
        board["cases"][name] = {
            "delta": round(mean(s["with"]) - mean(s["without"]), 2),
            "with": round(mean(s["with"]), 2),
            "without": round(mean(s["without"]), 2),
            "runs": min(len(s["with"]), len(s["without"])),
            "at": time.strftime("%Y-%m-%d"),
            "sha": sha,
            "cost": round(s["cost"], 2),
            "inputs": measurement_inputs(by_name[name], ROOT),
        }
    board["cases"] = dict(sorted(board["cases"].items()))
    BOARD.write_text(json.dumps(board, indent=1) + "\n")
    print(f"  board updated: {len(measured)} entr{'y' if len(measured) == 1 else 'ies'} — evals/board.json")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--ablation", required=True, choices=["with-without"],
                        help="the only mode: every case runs with the plugin loaded and without")
    parser.add_argument("--judge-model", required=True, help="judge for llm graders; sonnet or larger, never the model under test")
    parser.add_argument("--allow-tools", nargs="*", default=[], help="operator grant for gated tools cases may ask for")
    parser.add_argument("--case", action="append", help="run only this case (repeatable)")
    parser.add_argument("--changed", action="store_true",
                        help="run only the cases the board holds no fresh measurement for — "
                             "a changed rule, case or skill, or no entry at all")
    parser.add_argument("--runs", type=int, help="override every case's runs: (pilots; the floor for a real measurement is 3)")
    parser.add_argument("--model", default="", help="session model for both arms (default: the account's default)")
    parser.add_argument("--max-concurrency", type=int, default=2)
    args = parser.parse_args()

    if not shutil.which("npx"):
        print("✘ npx not found — the runner needs node (a maintainer-machine prerequisite, never CI's)", file=sys.stderr)
        return 1

    if args.changed and args.case:
        print("✘ --changed picks its own cases; drop --case or drop --changed", file=sys.stderr)
        return 1

    suite = cases(ROOT)
    if args.case:
        suite = [c for c in suite if c["name"] in set(args.case)]
        missing = set(args.case) - {c["name"] for c in suite}
        if missing:
            print(f"✘ no such case: {', '.join(sorted(missing))}", file=sys.stderr)
            return 1
    if args.changed:
        entries = load_board().get("cases", {})
        suite = [c for c in suite
                 if entries.get(c["name"], {}).get("inputs") != measurement_inputs(c, ROOT)]
        if not suite:
            print("✔ board is current — nothing has changed since its measurements")
            return 0
        print(f"  --changed: {len(suite)} case(s) without a fresh measurement")
    if not suite:
        print("✘ no cases selected", file=sys.stderr)
        return 1

    repeat = args.runs or max(c["runs"] for c in suite)
    run_dir = ROOT / "evals" / "results" / time.strftime("%Y%m%d-%H%M%S")
    run_dir.mkdir(parents=True)

    config = compile_config(suite, repeat, set(args.allow_tools))
    config_path = run_dir / "promptfooconfig.json"
    config_path.write_text(json.dumps(config, indent=1))

    env = os.environ.copy()
    env.update({
        "LIVESPEC_ROOT": str(ROOT),
        "LIVESPEC_RUN_DIR": str(run_dir),
        "LIVESPEC_JUDGE_MODEL": args.judge_model,
        "LIVESPEC_SESSION_MODEL": args.model,
        "PROMPTFOO_PYTHON": sys.executable,
        "PROMPTFOO_DISABLE_TELEMETRY": "1",
    })
    results_path = run_dir / "results.json"
    print(f"  {len(suite)} case(s) x 2 arms x {repeat} run(s) — sessions in {run_dir}/sessions/")
    subprocess.run(
        ["npx", "-y", PROMPTFOO, "eval", "-c", str(config_path), "-o", str(results_path),
         "--no-cache", "--no-progress-bar", "--max-concurrency", str(args.max_concurrency)],
        cwd=run_dir, env=env,
    )
    if not results_path.exists():
        print("✘ promptfoo produced no results — harness failure, nothing was measured", file=sys.stderr)
        return 1
    stats, measured, sessions = collect(results_path)
    print_summary(stats, sessions)
    record(measured, suite)
    return 0


if __name__ == "__main__":
    sys.exit(main())
