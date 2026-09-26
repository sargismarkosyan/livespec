#!/usr/bin/env python3
"""Run the eval suite: both arms, judged, summarised as delta.

The native runner for this case format — `claude plugin eval` — is gated behind
early access and has never started on this account, so the suite runs here
instead: this script reads `evals/<NN-case>/`, drives each case through
`claude -p` with the plugin loaded and without (provider.py), grades what came
out (asserts.py), and reports the difference. The case folders stay
authoritative and stay in the native format; if enablement ever arrives, both
runners read the same folders.

The flags are the suite's contract, unchanged from the native invocation:
`--ablation with-without` is the only mode there is, `--judge-model` names the
judge (never smaller than the model under test), `--model` names the model both
arms run on — it defaults to `caselib.SESSION_MODEL`, the bindings' one
decision, and every row records what actually ran — and `--allow-tools` is an
operator grant — a gated tool a case asks for but the grant omits is stripped,
exactly as the native CLI behaves, and stripped tools are warned about because
a grader that could never fail proves nothing.

    python3 evals/runner/run.py --ablation with-without --judge-model sonnet \
        --model claude-sonnet-5 --allow-tools Write Edit --scaffold [--case NAME] [--runs N]

`--scaffold` runs each case's `scaffold_script` — author-supplied bash, as you
— in the session's fresh workspace before either arm starts. Off by default,
exactly as the native CLI treats it: only use it on case files you authored. A
scaffolded case run without the flag is warned about, because what it measures
then is an empty workspace where the fixture should be.

A run is a directory (0059). Every session's result and every verdict is
written under `sessions/<case>/<arm>-<run>/` the moment it exists, and
`results.json` is assembled from those files. The first session or verdict
that meets the account's limit stops the run from starting more; the summary
says what is owed and when the limit resets, and

    python3 evals/runner/run.py --resume evals/results/<stamp>

runs exactly that — a session that never finished, a verdict the judge never
returned — and makes each case's row from the whole. A run the machine killed
resumes the same way.

Costs real money per session and never runs in CI. Exit 0 is a completed
measurement, whatever the scores; 3 is a run the limit stopped, resumable;
only a harness failure exits 1. No number from here is trusted before a
read-every-verdict calibration — evals/README.md.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import threading
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".github" / "scripts"))
from caselib import (  # noqa: E402
    MIN_RUNS, SESSION_MODEL, cases, frontmatter, harness_fingerprint, measurement_inputs, replaces, why_stale,
)

# --- the cost gate ------------------------------------------------------------
#
# This runner spends the maintainer's money and the account's session budget:
# six real sessions plus judge calls per case, and three runs in one sitting
# have exhausted the account outright more than once (429, mid-measurement,
# sessions lost). Nothing may start it on its own initiative: not CI, not a
# stale board entry, not the `--changed` heal the board gate prints.
#
# So the default is refusal. The flag below is the maintainer's signature on
# one specific run, and an agent adding it without having been told to, in
# this conversation, for this run, has forged it. What a run would cost is not
# a figure typed here — the one that was read $1.80 a case for a suite that
# cost $4.46 — but an estimate from the board's last costs of the cases
# selected, printed with the refusal, naming the model those costs were made on.
APPROVAL_FLAG = "--i-approve-the-cost"

# What a run that the limit stopped exits with: not 0, which is a completed
# measurement, and not 1, which is a broken harness. The directory is whole
# and `--resume` takes it up (0059).
LIMIT_EXIT = 3

ARMS = ("with", "without")


def estimate(suite: list[dict], board: dict, share: dict[str, float] | None = None) -> tuple[float, set[str], int, bool]:
    """What a run of these cases would cost, from the board's last costs of them.

    An unmeasured case counts at the mean of the measured ones. `share` scales
    a case's cost by the fraction of its jobs still owed, which is what a
    resumed run is priced on. Returns the total, the models those costs were
    made on — so the first Sonnet refusal says plainly that it is quoting Opus
    prices — how many cases were guessed at the mean, and whether the board
    held any cost to estimate from at all.
    """
    entries = board.get("cases", {}) if isinstance(board, dict) else {}
    priced = {name: float(entry["cost"]) for name, entry in entries.items()
              if isinstance(entry, dict) and isinstance(entry.get("cost"), (int, float))}
    mean_cost = sum(priced.values()) / len(priced) if priced else None
    total, models, guessed = 0.0, set(), 0
    for case in suite:
        fraction = (share or {}).get(case["name"], 1.0)
        if case["name"] in priced:
            total += priced[case["name"]] * fraction
            models.add(str(entries[case["name"]].get("model") or "an unknown model"))
        elif mean_cost is not None:
            total += mean_cost * fraction
            guessed += 1
    return total, models, guessed, mean_cost is not None


def refusal(suite: list[dict], board: dict, runs: int | None, model: str, share: dict[str, float] | None = None) -> str:
    total, models, guessed, priced = estimate(suite, board, share)
    if priced:
        if runs and not share:
            total = total * runs / MIN_RUNS
        made_on = ", ".join(sorted(models)) if models else "the board's mean"
        guess = f" ({guessed} of them never measured, counted at the board's mean)" if guessed else ""
        what = (f"the part of {len(suite)} case(s) still owed" if share
                else f"{len(suite)} case(s) at runs: {runs or MIN_RUNS}")
        line = (f"  ≈ ${total:.2f} for {what}, from the board's "
                f"last costs of these cases — made on {made_on}; this run would be on {model}{guess}.")
    else:
        line = "  The board holds no cost yet to estimate this run from."
    return f"""✘ this run spends real money, and nobody approved it.

{line}
  Sessions plus judge calls, drawn from the maintainer's account and its
  session limit. A stale board entry is not an approval. A --changed heal is
  not an approval. A green plan is not an approval.

  If you are an agent: do not add {APPROVAL_FLAG} on your own
  initiative. Stop here, tell the maintainer which cases are stale and what
  the run will cost, and add the flag only after they have said yes to this
  specific run. Everything else — the commit, the pull request, the body with
  a gap where the numbers go — can be finished without it.

  Approved by the maintainer, just now, for this run?
      {APPROVAL_FLAG}
"""

# Mirrors GATED_TOOLS in .github/scripts/evalsuite.py — the operator grant the
# native CLI enforces, enforced here the same way.
GATED = {"Bash", "Write", "Edit", "WebFetch", "WebSearch"}


def plan_cases(suite: list[dict], granted: set[str], scaffold: bool) -> list[dict]:
    """What each selected case is run with: its variables for the provider and
    its graders with their weights. Written into the run's `run.json`, so a
    resume runs the same run (0059)."""
    planned = []
    for case in suite:
        prompt_file = next(s for s in case["sources"] if s.name == "prompt.md")
        fields, body = frontmatter(prompt_file)
        if case["scaffold"] and not scaffold:
            print(f"  ⚠ {case['name']} declares a scaffold_script; running without it — pass --scaffold to lay the fixture down")
        allowed = []
        for tool in case["allowed_tools"]:
            if (tool in GATED or tool.startswith("mcp__")) and tool not in granted:
                print(f"  ⚠ {case['name']} asks for {tool}; not granted — running without it")
                continue
            allowed.append(tool)
        graders = []
        for grader in case["graders"]:
            entry = {"grader": str(grader["path"].relative_to(ROOT)), "weight": 1}
            if grader["type"] == "tool_used" and not grader["fields"].get("max", "").strip().isdigit():
                entry["weight"] = 0  # the plugin-fired indicator never touches a score
            elif grader["fields"].get("weight", "").strip().isdigit():
                entry["weight"] = int(grader["fields"]["weight"])
            graders.append(entry)
        # The sitting (0058): the person and the shell, when the case brings them.
        shell = list(case.get("shell") or [])
        if shell and "Bash" not in granted:
            print(f"  ⚠ {case['name']} lends a shell ({', '.join(shell)}); Bash not granted — running without it")
            shell = []
        if case.get("person"):
            print(f"  · {case['name']}: a person answers up to {case['replies']} time(s)"
                  + (f"; a shell of {', '.join(shell)}" if shell else ""))
        elif shell:
            print(f"  · {case['name']}: a shell of {', '.join(shell)}")
        planned.append({
            "case": case["name"],
            "negative": bool(case["negative"]),
            "inputs": measurement_inputs(case, ROOT),
            "vars": {
                "prompt": body.strip(),
                "case": case["name"],
                "scaffold": str(case["scaffold"]) if scaffold and case["scaffold"] else "",
                "allowed_tools": " ".join(allowed),
                "disallowed_tools": " ".join(sorted(GATED - set(allowed))),
                "max_turns": fields.get("max_turns", "25"),
                "timeout_seconds": fields.get("timeout_seconds", "600"),
                "person": str(case["person_file"]) if case.get("person") else "",
                "replies": str(case.get("replies") or 0),
                "shell": ",".join(shell),
            },
            "graders": graders,
        })
    return planned


# --- the run directory ---------------------------------------------------------


def jobs(plan: dict) -> list[tuple[str, str, int]]:
    """Every (case, arm, run) the plan asks for, case by case and run by run,
    both arms together — so a run the limit cuts short has finished whole
    cases rather than half of every case."""
    return [(case["case"], arm, run)
            for case in plan["cases"]
            for run in range(1, int(plan["repeat"]) + 1)
            for arm in ARMS]


def job_dir(run_dir: Path, case: str, arm: str, run: int) -> Path:
    return run_dir / "sessions" / case / f"{arm}-{run}"


def _read(path: Path):
    try:
        return json.loads(path.read_text())
    except (OSError, json.JSONDecodeError):
        return None


def _write(path: Path, value) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(value, indent=1) + "\n")
    tmp.replace(path)


def owed(run_dir: Path, plan: dict) -> tuple[list[tuple[str, str, int]], list[tuple[str, str, int]]]:
    """What the directory still lacks: the jobs whose session never finished,
    met the limit or lost the person, and the jobs whose session exists but a
    verdict of it is missing or errored. A session that errored any other way
    is not owed — a resume is for what the limit or the kill took (0059), and
    for the sitting whose person never answered (#159)."""
    sessions_owed, verdicts_owed = [], []
    graders = {case["case"]: case["graders"] for case in plan["cases"]}
    for job in jobs(plan):
        directory = job_dir(run_dir, *job)
        session = _read(directory / "session.json")
        if session is None or session.get("limit") or session.get("person_unreachable"):
            sessions_owed.append(job)
            continue
        if "error" in session:
            continue
        verdicts = _read(directory / "verdicts.json")
        if not isinstance(verdicts, list) or len(verdicts) != len(graders[job[0]]) \
                or any(v is None or v.get("errored") for v in verdicts):
            verdicts_owed.append(job)
    return sessions_owed, verdicts_owed


def _aside(directory: Path) -> None:
    """A session run again keeps its earlier attempt: everything the last one
    left goes under previous/<stamp>/, evidence rather than clutter."""
    left = [p for p in directory.iterdir() if p.name != "previous"] if directory.is_dir() else []
    if not left:
        return
    previous = directory / "previous" / time.strftime("%Y%m%d-%H%M%S")
    previous.mkdir(parents=True, exist_ok=True)
    for path in left:
        shutil.move(str(path), str(previous / path.name))


def perform(job: tuple[str, str, int], plan: dict, run_dir: Path, stop: threading.Event,
            provider, asserts) -> str:
    """One job: the session if it is owed, then every verdict that is owed,
    each written to disk as it lands. Returns "done", "skipped" — the stop was
    set before it started — or "limit", the job that set it."""
    case_name, arm, run = job
    if stop.is_set():
        return "skipped"
    spec = next(c for c in plan["cases"] if c["case"] == case_name)
    directory = job_dir(run_dir, *job)
    session = _read(directory / "session.json")
    if session is None or session.get("limit"):
        _aside(directory)
        directory.mkdir(parents=True, exist_ok=True)
        session = provider.call_api(
            spec["vars"]["prompt"], {"config": {"with_plugin": arm == "with"}},
            {"vars": dict(spec["vars"], session_dir=str(directory))},
        )
        _write(directory / "session.json", session)
    if "error" in session:
        if session.get("limit"):
            stop.set()
            return "limit"
        return "done"
    verdicts = _read(directory / "verdicts.json")
    if not isinstance(verdicts, list) or len(verdicts) != len(spec["graders"]):
        verdicts = [None] * len(spec["graders"])
    for index, grader in enumerate(spec["graders"]):
        if verdicts[index] is not None and not verdicts[index].get("errored"):
            continue
        if stop.is_set():
            break  # what is left is owed; the wall does not move in a minute
        result = asserts.get_assert(session.get("output", ""), {
            "config": {"grader": grader["grader"]},
            "vars": {"case": case_name},
            "providerResponse": {"metadata": session.get("metadata") or {}},
        })
        verdicts[index] = dict(result, assertion={"weight": grader["weight"], "grader": grader["grader"]})
        _write(directory / "verdicts.json", verdicts)
        if result.get("limit"):
            stop.set()
            return "limit"
    return "done"


def drive(run_dir: Path, plan: dict, max_concurrency: int) -> dict:
    """Perform every owed job, at most `max_concurrency` at a time, until they
    are done or the limit stops the run. Returns what happened: how many ran,
    how many were skipped, and the limit's own words if it was met."""
    runner_dir = Path(__file__).resolve().parent
    if str(runner_dir) not in sys.path:
        sys.path.insert(0, str(runner_dir))
    import asserts  # noqa: E402 — read LIVESPEC_ROOT at import, set by the caller
    import provider  # noqa: E402
    sessions_owed, verdicts_owed = owed(run_dir, plan)
    todo = sessions_owed + verdicts_owed
    stop = threading.Event()
    outcome = {"ran": 0, "skipped": 0, "limit": ""}
    with ThreadPoolExecutor(max_workers=max(1, max_concurrency)) as pool:
        futures = [pool.submit(perform, job, plan, run_dir, stop, provider, asserts) for job in todo]
        for job, future in zip(todo, futures):
            state = future.result()
            if state == "skipped":
                outcome["skipped"] += 1
                continue
            outcome["ran"] += 1
            if state == "limit":
                directory = job_dir(run_dir, *job)
                session = _read(directory / "session.json") or {}
                said = session.get("error") if session.get("limit") else ""
                if not said:
                    for verdict in _read(directory / "verdicts.json") or []:
                        if verdict and verdict.get("limit"):
                            said = verdict.get("reason", "")
                outcome["limit"] = outcome["limit"] or said or "the account's limit"
    return outcome


def assemble(run_dir: Path, plan: dict) -> Path:
    """`results.json` from the directory: one row per session that finished
    and was judged whole, in the shape `collect()` reads. A session still
    owed a verdict is not a row yet."""
    rows = []
    for job in jobs(plan):
        case_name, arm, run = job
        directory = job_dir(run_dir, *job)
        session = _read(directory / "session.json")
        if session is None or session.get("limit"):
            continue
        row = {"description": case_name, "vars": {"case": case_name, "run": run},
               "provider": {"label": f"{arm}-plugin"}}
        if "error" in session:
            row["error"] = session["error"]
            rows.append(row)
            continue
        verdicts = _read(directory / "verdicts.json")
        if not isinstance(verdicts, list) or any(v is None for v in verdicts):
            continue
        row["response"] = session
        row["gradingResult"] = {"componentResults": verdicts}
        rows.append(row)
    results_path = run_dir / "results.json"
    _write(results_path, {"results": {"results": rows}})
    return results_path


BOARD = ROOT / "evals" / "board.json"


def load_board() -> dict:
    try:
        return json.loads(BOARD.read_text())
    except (OSError, json.JSONDecodeError):
        return {"format": 1, "cases": {}}


def judge_costs(results_path: Path) -> dict[str, float]:
    """The judge's bill per case, from the ledger asserts.py keeps beside the
    results. Absent for a run made before 0057, in which case the judge cost
    what it cost and nothing recorded it."""
    ledger = results_path.parent / "judge.jsonl"
    costs: dict[str, float] = defaultdict(float)
    if not ledger.exists():
        return costs
    for line in ledger.read_text().splitlines():
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        costs[str(entry.get("case") or "?")] += float(entry.get("cost") or 0)
    return costs


def _have(requirement: str) -> bool:
    """A binary on the path, or `module:<name>` importable by the path's python3 —
    the fixture that runs `pytest --cov` needs pytest-cov, which is no binary."""
    if requirement.startswith("module:"):
        python = shutil.which("python3") or "python3"
        probe = subprocess.run([python, "-c", f"import {requirement.split(':', 1)[1]}"], capture_output=True)
        return probe.returncode == 0
    return shutil.which(requirement) is not None


def missing_requirements(suite: list[dict]) -> list[tuple[str, str]]:
    """(case, requirement) for every `requires:` this machine cannot satisfy.
    Checked before a config is written: a fixture whose test runner is absent
    measures the absence, so the run refuses instead — a maintainer-machine
    prerequisite, never a number (0058)."""
    return [(case["name"], requirement) for case in suite
            for requirement in (case.get("requires") or []) if not _have(requirement)]


def session_score(components: list[dict]) -> tuple[float | None, int]:
    """One session's score from its verdicts, and how many verdicts errored.

    The fraction is over the graders that returned: weightless indicators are
    not in it, and a judge that said nothing three times is not a verdict —
    it is counted here and left out, never read as the agent failing the
    rubric (#131). None means no grader returned at all.
    """
    weighted, weights, errored = 0.0, 0.0, 0
    for component in components:
        reason = str(component.get("reason") or "")
        if reason.startswith("plugin-fired indicator"):
            continue
        if component.get("errored") or reason.startswith("judge error"):
            errored += 1
            continue
        weight = (component.get("assertion") or {}).get("weight", 1)
        weight = float(weight if isinstance(weight, (int, float)) else 1)
        weighted += weight * float(component.get("score") or 0)
        weights += weight
    return (weighted / weights if weights else None), errored


def collect(results_path: Path) -> tuple[dict, dict, int]:
    """Per-case scores, costs, models and fired-counts out of a results file."""
    rows = json.load(results_path.open())["results"]["results"]
    stats: dict[str, dict] = defaultdict(lambda: {
        "with": [], "without": [], "cost": 0.0, "fired": [], "errors": 0, "errored": 0,
        "lost_person": 0, "models": set(),
    })
    for row in rows:
        name = (row.get("vars") or {}).get("case") or (row.get("description") or "?")
        arm = ((row.get("provider") or {}).get("label")) or "?"
        response = row.get("response") or {}
        stats[name]["cost"] += float(response.get("cost") or 0)
        ran_on = (response.get("metadata") or {}).get("model")
        if ran_on:
            stats[name]["models"].add(str(ran_on))
        grading = row.get("gradingResult") or {}
        if row.get("error") and not grading.get("componentResults"):
            # a genuine harness error — a session that never produced a
            # result, not a verdict that failed. The sitting whose person
            # never answered is counted apart, because it is the one kind a
            # resume can put right (#159).
            if "the person could not be reached" in str(row.get("error")):
                stats[name]["lost_person"] += 1
            else:
                stats[name]["errors"] += 1
            continue
        key = "with" if arm == "with-plugin" else "without"
        components = grading.get("componentResults") or []
        for component in components:
            reason = component.get("reason") or ""
            if key == "with" and reason.startswith("plugin-fired indicator"):
                stats[name]["fired"].append("indicator: fired" in reason)
        # The score is ours to take: an errored verdict is not a fail, and a
        # session whose every verdict errored is not a measurement of zero
        # (0058, #131).
        score, errored = session_score(components)
        stats[name]["errored"] += errored
        if score is None:
            stats[name]["errors"] += 1
            continue
        stats[name][key].append(score)
    for name, judged in judge_costs(results_path).items():
        stats[name]["cost"] += judged  # the whole bill: sessions and the judge (0057)
    return stats, {n: s for n, s in stats.items() if s["with"] and s["without"]}, len(rows)


def mean(values: list[float]) -> float:
    return sum(values) / len(values)


def print_summary(stats: dict, sessions: int, negatives: frozenset[str] | set[str] = frozenset()) -> None:
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
    for name in sorted(n for n in stats if stats[n].get("lost_person")):
        print(f"  ⚠ {name}: {stats[name]['lost_person']} sitting(s) lost the person — the judge could not "
              f"answer from the sheet, so the sitting stopped mid-round and was not scored; "
              f"`--resume` runs them again (#159)")
    for name in sorted(n for n in stats if stats[n].get("errored")):
        print(f"  ⚠ {name}: {stats[name]['errored']} verdict(s) errored — the judge returned nothing three "
              f"times; left out of the score, never counted as a failure (#131)")
    # A skill-tagged case whose plugin arm never fired measured nothing about
    # that skill. A line, never a gate: it would have named 08 and 10 on
    # 2026-09-17 and not 12, where setup fired and then stalled (#123).
    for name in sorted(n for n in stats if stats[n]["fired"] and not any(stats[n]["fired"]) and n not in negatives):
        print(f"  ⚠ {name}: the skill under test never fired in the plugin arm — the case may not reach it (#123)")
    if total:
        cost = sum(s["cost"] for s in stats.values())
        print(f"\n  suite Δ {mean(total):+.2f} over {len(total)} case(s), {sessions} session(s), "
              f"${cost:.2f} sessions and judge")
    print("  No number from here is calibrated until every verdict has been read — evals/README.md.")


def print_owed(run_dir: Path, plan: dict, limit: str) -> bool:
    """What the directory still lacks, and the one command that runs it.
    Returns whether anything is owed."""
    sessions_owed, verdicts_owed = owed(run_dir, plan)
    if not sessions_owed and not verdicts_owed:
        return False
    cases_owed = sorted({job[0] for job in sessions_owed + verdicts_owed})
    print(f"\n  ✋ this run is not finished: {len(sessions_owed)} session(s) never ran or met the limit, "
          f"{len(verdicts_owed)} session(s) are owed a verdict — {', '.join(cases_owed)}")
    if limit:
        print(f"     the account's limit: {limit}")
    try:
        shown = run_dir.relative_to(ROOT)
    except ValueError:
        shown = run_dir
    print(f"     what ran is kept; resume with:\n       python3 evals/runner/run.py --resume {shown}")
    print(f"     (spends real money — the maintainer adds {APPROVAL_FLAG}, nobody else)")
    return True


def entry_for(s: dict, case: dict, root: Path, sha: str, judge: str) -> dict:
    """One board row: the number, its provenance, and what it was a measurement
    of — the case's inputs, the model the sessions ran on (the transcripts' word,
    not the flag's), the judge, and the harness that produced it. Pure, so the
    injector can hold it without writing the board (0057)."""
    runs = min(len(s["with"]), len(s["without"]))
    models = sorted(s.get("models") or [])
    return {
        "delta": round(mean(s["with"]) - mean(s["without"]), 2),
        "with": round(mean(s["with"]), 2),
        "without": round(mean(s["without"]), 2),
        "runs": runs,
        "at": time.strftime("%Y-%m-%d"),
        "sha": sha,
        "cost": round(s["cost"], 2),
        "model": "+".join(models) if models else "",
        "judge": judge,
        "harness": harness_fingerprint(root),
        "inputs": measurement_inputs(case, root),
    }


def record(measured: dict, suite: list[dict], judge: str) -> None:
    """Update the board with what this run measured — and only that.

    An entry carries the number, its provenance, and a hash of what it was a
    measurement of; the board gate fails the entry when those inputs move on.
    A case whose sessions all errored is not recorded — a non-measurement is
    not a measurement of zero.

    **A run below the floor may not take a measurement's row.** `--runs 1` is a
    pilot: it exists so the verdicts can be read before a real run is paid for,
    and its number is the noise the floor exists to keep out. Letting it write
    anyway costs twice — the measurement it replaces is gone, and the fresh
    inputs hash it brings turns the red that was asking for a real run green.
    Both happened to `26-two-seconds-before-the-push` (#75). The pilot's numbers
    are still printed above and still in the run directory, which is where a
    pilot's answer lives; what it does not get is the durable row.
    """
    board = load_board()
    by_name = {case["name"]: case for case in suite}
    try:
        sha = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "--short", "HEAD"],
                             capture_output=True, text=True).stdout.strip() or "unknown"
    except OSError:
        sha = "unknown"
    written, held = 0, []
    for name, s in measured.items():
        runs = min(len(s["with"]), len(s["without"]))
        prior = board["cases"].get(name)
        if not replaces(prior, runs):
            held.append((name, runs, prior))
            continue
        board["cases"][name] = entry_for(s, by_name[name], ROOT, sha, judge)
        written += 1
    board["cases"] = dict(sorted(board["cases"].items()))
    BOARD.write_text(json.dumps(board, indent=1) + "\n")
    print(f"  board updated: {written} entr{'y' if written == 1 else 'ies'} — evals/board.json")
    for name, runs, prior in held:
        # .get() rather than indexing: the board is a hand-editable file, and a
        # refusal that crashes on a missing field is a refusal nobody hears.
        delta = prior.get("delta")
        shown = f"Δ {delta:+.2f}, " if isinstance(delta, (int, float)) else ""
        print(f"  ✋ {name}: {runs} run(s) is below the floor of {MIN_RUNS}, and the board already holds "
              f"a {prior['runs']}-run measurement ({shown}{prior.get('at', 'undated')}). Kept. Read this "
              f"pilot's verdicts in the run directory; re-run it at the floor to replace the number.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--ablation", choices=["with-without"],
                        help="the only mode: every case runs with the plugin loaded and without")
    parser.add_argument("--judge-model", help="judge for llm graders; sonnet or larger, never the model under test")
    parser.add_argument("--allow-tools", nargs="*", default=[], help="operator grant for gated tools cases may ask for")
    parser.add_argument("--scaffold", action="store_true",
                        help="run each case's scaffold_script in its fresh workspace before the session — "
                             "author-supplied bash, run as you; off by default, as the native runner treats it")
    parser.add_argument("--case", action="append", help="run only this case (repeatable)")
    parser.add_argument("--changed", action="store_true",
                        help="run only the cases the board holds no fresh measurement for — "
                             "a changed rule, case or skill, or no entry at all")
    parser.add_argument("--runs", type=int, help="override every case's runs: (pilots; the floor for a real measurement is 3)")
    parser.add_argument("--model", default=SESSION_MODEL,
                        help=f"session model for both arms (default: caselib.SESSION_MODEL, {SESSION_MODEL}; "
                             "the row records what actually ran, and the board stales a row made on anything else)")
    parser.add_argument("--max-concurrency", type=int, default=2)
    parser.add_argument("--resume", metavar="RUN_DIR",
                        help="take up a run the limit or the machine stopped: runs only the sessions that never "
                             "finished and the verdicts the judge never returned, from the run's own run.json; "
                             "takes no selection flag beside it, because a resumed run is the same run")
    parser.add_argument(APPROVAL_FLAG, action="store_true", dest="approved",
                        help="the maintainer's approval for this one run. Required — without it this "
                             "refuses. Never add it on an agent's own initiative")
    args = parser.parse_args()

    if args.resume:
        given = [flag for flag, value in (("--ablation", args.ablation), ("--judge-model", args.judge_model),
                                          ("--allow-tools", args.allow_tools), ("--scaffold", args.scaffold),
                                          ("--case", args.case), ("--changed", args.changed), ("--runs", args.runs))
                 if value]
        if given:
            print(f"✘ --resume runs the run its directory describes; drop {', '.join(given)}", file=sys.stderr)
            return 1
        run_dir = Path(args.resume)
        if not run_dir.is_absolute():
            run_dir = (Path.cwd() / run_dir).resolve()
        plan = _read(run_dir / "run.json")
        if not isinstance(plan, dict) or "cases" not in plan:
            print(f"✘ {run_dir} holds no run.json — a run before 0059 is not resumable; start a fresh run", file=sys.stderr)
            return 1
    else:
        if not args.ablation or not args.judge_model:
            print("✘ --ablation with-without and --judge-model are required (or --resume RUN_DIR)", file=sys.stderr)
            return 1
        if args.changed and args.case:
            print("✘ --changed picks its own cases; drop --case or drop --changed", file=sys.stderr)
            return 1
        run_dir = plan = None

    suite = cases(ROOT)
    if plan:
        wanted = {c["case"] for c in plan["cases"]}
        suite = [c for c in suite if c["name"] in wanted]
        missing = wanted - {c["name"] for c in suite}
        if missing:
            print(f"✘ the run names a case the tree no longer has: {', '.join(sorted(missing))}", file=sys.stderr)
            return 1
        moved = [c["name"] for c in suite if measurement_inputs(c, ROOT) != next(
            p["inputs"] for p in plan["cases"] if p["case"] == c["name"])]
        if moved:
            print(f"  ⚠ changed since the run began, so its halves measure two versions: {', '.join(moved)} "
                  f"— a fresh run is one command")
    elif args.case:
        # In the order named, once each: a run the limit will cut short
        # finishes the cases the maintainer put first (0059).
        by_name = {c["name"]: c for c in suite}
        missing = [name for name in args.case if name not in by_name]
        if missing:
            print(f"✘ no such case: {', '.join(sorted(set(missing)))}", file=sys.stderr)
            return 1
        suite = [by_name[name] for name in dict.fromkeys(args.case)]
    elif args.changed:
        entries = load_board().get("cases", {})
        suite = [c for c in suite if why_stale(entries.get(c["name"]), c, ROOT)]
        if not suite:
            print("✔ board is current — nothing has changed since its measurements")
            return 0
        print(f"  --changed: {len(suite)} case(s) without a fresh measurement")
    if not suite:
        print("✘ no cases selected", file=sys.stderr)
        return 1

    # A virtual environment at the root serves the run and its sessions: on a
    # machine that will not take a system package, `python3 -m venv .venv &&
    # .venv/bin/pip install pytest` is the whole prerequisite. Put on the path
    # here so the requirement check below and the sessions see the same thing.
    venv_bin = ROOT / ".venv" / "bin"
    if venv_bin.is_dir() and str(venv_bin) not in os.environ.get("PATH", "").split(os.pathsep):
        os.environ["PATH"] = f"{venv_bin}{os.pathsep}{os.environ.get('PATH', '')}"
        print(f"  · {venv_bin.relative_to(ROOT)} is on the path for this run and its sessions")

    # What the fixtures need this machine to have, before anything is spent or
    # approved: a missing test runner is a refusal, never a measurement (0058).
    lacking = missing_requirements(suite)
    if lacking:
        for name, binary in lacking:
            print(f"✘ {name} requires {binary}, which this machine does not have — nothing was measured", file=sys.stderr)
        print("  a maintainer-machine prerequisite; install it and run again", file=sys.stderr)
        return 1

    if plan:
        model, judge, repeat = plan["model"], plan["judge"], int(plan["repeat"])
        sessions_owed, verdicts_owed = owed(run_dir, plan)
        if not sessions_owed and not verdicts_owed:
            print(f"✔ {run_dir.name} is whole — nothing is owed; its summary is below")
        per_case = defaultdict(int)
        for job in sessions_owed:
            per_case[job[0]] += 1
        share = {name: per_case[name] / (2 * repeat) for name in per_case}
        # a verdict owed costs the judge's price, not a session's: priced at nothing here
        share.update({job[0]: share.get(job[0], 0.0) for job in verdicts_owed})
        priced_suite = [c for c in suite if c["name"] in share]
    else:
        model, judge, repeat = args.model, args.judge_model, args.runs or max(c["runs"] for c in suite)
        share, priced_suite = None, suite

    # The refusal comes after the selection so it can say what this run would
    # cost, and before anything that could spend.
    if not args.approved and (plan is None or priced_suite):
        print(refusal(priced_suite, load_board(), args.runs, model, share), file=sys.stderr)
        return 2

    if plan is None:
        run_dir = ROOT / "evals" / "results" / time.strftime("%Y%m%d-%H%M%S")
        run_dir.mkdir(parents=True)
        plan = {
            "format": 1,
            "started": time.strftime("%Y-%m-%d %H:%M:%S"),
            "model": model, "judge": judge, "repeat": repeat,
            "granted": sorted(args.allow_tools), "scaffold": bool(args.scaffold),
            "cases": plan_cases(suite, set(args.allow_tools), args.scaffold),
        }
        _write(run_dir / "run.json", plan)
    else:
        plan.setdefault("resumed", []).append(time.strftime("%Y-%m-%d %H:%M:%S"))
        _write(run_dir / "run.json", plan)

    if any(c["vars"].get("shell") for c in plan["cases"]):
        if shutil.which("bwrap"):
            os.environ["LIVESPEC_SANDBOX"] = "1"
            print("  · lent shells run inside Claude Code's sandbox with the network closed (bubblewrap found)")
        else:
            print("  ⚠ no bubblewrap on this machine: a lent shell is confined by its allow-list alone, "
                  "and the fixture is a throwaway under /tmp")
    os.environ.update({
        "LIVESPEC_ROOT": str(ROOT),
        "LIVESPEC_RUN_DIR": str(run_dir),
        "LIVESPEC_JUDGE_MODEL": judge,
        "LIVESPEC_SESSION_MODEL": model,
    })
    sessions_owed, verdicts_owed = owed(run_dir, plan)
    print(f"  {len(plan['cases'])} case(s) x 2 arms x {repeat} run(s) on {model}, judged by {judge} "
          f"— {len(sessions_owed)} session(s) to run, {len(verdicts_owed)} to judge; sessions in {run_dir}/sessions/")
    outcome = drive(run_dir, plan, args.max_concurrency)
    results_path = assemble(run_dir, plan)
    stats, measured, sessions = collect(results_path)
    print_summary(stats, sessions, negatives={c['case'] for c in plan['cases'] if c['negative']})
    if outcome["ran"]:
        record(measured, suite, judge)
    else:
        # Nothing ran: a resume of a whole directory is a reading of it, and a
        # reading does not re-stamp the board with today's date and commit.
        print("  nothing ran, so the board is left as it is")
    if print_owed(run_dir, plan, outcome["limit"]):
        return LIMIT_EXIT
    return 0


if __name__ == "__main__":
    sys.exit(main())
