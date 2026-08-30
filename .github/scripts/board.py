#!/usr/bin/env python3
"""Gate 5 — the board of latest measurements.

`evals/board.json` records, per case, what the last eval run measured: both
arms, delta, when, at what commit — and a hash of what that number was a
measurement *of* (the case's files, the rules it claims, the skills it holds).
This gate checks the bookkeeping:

- a case whose current inputs no longer match its entry **fails** — a rule, a
  case or a skill changed and nobody re-measured. The healing command runs
  exactly the stale set, never the full suite.
- a case with no entry **warns** — the bootstrap state; the warning list is the
  to-do list for the first pilot.
- a case whose entry came from fewer runs than the floor **warns, and is not
  counted** — a pilot's number is what the board has, never what it knows. It
  stays visible, it stays out of the mean, and it is not read as coverage.

That last one is why the mean here moved on 2026-08-30 without a single session
being run: 23 of 28 entries turned out to be below the floor — 22 single-run
pilots and one that lost a session to a 429 — and the average had been taken
over all of them as though they were measurements (#75).

**The score is never gated.** A delta of zero ships; a stale delta does not.
Gating the number would turn the suite into something to be optimised at; what
is enforced here is only that a number still describes the files it claims to.

Run: python3 .github/scripts/board.py [root] [--json]

`--json` prints the counts for the pull-request report and always exits 0 —
in that mode this is a hand-over of numbers, not a gate. See gates.md on why
the report may never recompute or fail anything.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from caselib import MIN_RUNS, cases, is_measurement, measurement_inputs  # noqa: E402

AS_JSON = "--json" in sys.argv
args = [a for a in sys.argv[1:] if a != "--json"]
ROOT = Path(args[0]).resolve() if args else Path(__file__).resolve().parents[2]

# Quoted without the runner's approval flag on purpose: a stale entry is a
# reason to ask the maintainer for a run, never a licence to start one, and a
# command that spends money should not be copy-pasteable out of a gate's output.
HEAL = ("python3 evals/runner/run.py --changed --ablation with-without "
        "--judge-model sonnet --allow-tools Write Edit --scaffold\n"
        "      (spends real money — the maintainer adds --i-approve-the-cost, nobody else)")

failures: list[str] = []
warnings: list[str] = []

board_path = ROOT / "evals" / "board.json"
try:
    entries = json.loads(board_path.read_text()).get("cases", {})
except (OSError, json.JSONDecodeError):
    entries = {}

suite = cases(ROOT)
measured: list[str] = []
stale: list[str] = []
below: list[str] = []
never: list[str] = []
deltas: list[float] = []
as_of = ""

for case in suite:
    entry = entries.get(case["name"])
    if entry is None:
        never.append(case["name"])
        continue
    # Staleness is asked first, and of every entry rather than only of the ones
    # that cleared the floor: a number that no longer describes these files is a
    # lie however many runs produced it, and demoting a stale row to a warning
    # because it was only a pilot would be a gate getting quieter over time.
    if entry.get("inputs") != measurement_inputs(case, ROOT):
        stale.append(case["name"])
        failures.append(
            f"evals/{case['name']}: measured at {entry.get('sha', '?')} ({entry.get('at', '?')}), but the "
            f"case, a rule it claims or a skill it holds has changed since. The number no longer describes "
            f"these files. Re-measure exactly what changed:\n      {HEAL}"
        )
        continue
    if not is_measurement(entry):
        below.append(case["name"])
        continue
    measured.append(case["name"])
    if isinstance(entry.get("delta"), (int, float)):
        deltas.append(float(entry["delta"]))
    as_of = max(as_of, str(entry.get("at", "")))

for name in sorted(set(entries) - {c["name"] for c in suite}):
    warnings.append(f"evals/board.json: entry for {name!r}, which is not a case any more; remove the row")

if never:
    listed = ", ".join(never[:6]) + ("…" if len(never) > 6 else "")
    warnings.append(
        f"{len(never)} case(s) never measured ({listed}) — the board fills as runs happen; "
        f"the first pilot's to-do list, not a failure"
    )

if below:
    listed = ", ".join(f"{n} ({entries[n].get('runs', '?')})" for n in below[:6]) + ("…" if len(below) > 6 else "")
    warnings.append(
        f"{len(below)} entr{'y' if len(below) == 1 else 'ies'} below the floor of {MIN_RUNS} runs ({listed}) "
        f"— pilots, kept and shown but not counted as measurements and not in the mean. Not a failure: "
        f"the number is the best the board has, and calling it coverage is what would be the lie"
    )

mean = round(sum(deltas) / len(deltas), 2) if deltas else None

if AS_JSON:
    # A hand-over for the report, never a gate: exits 0 whatever it found, so
    # a stale board can still be *reported* — which is when the row matters.
    print(json.dumps({
        "measured": len(measured), "stale": len(stale), "below": len(below),
        "never": len(never), "mean_delta": mean, "as_of": as_of or None,
    }))
    sys.exit(0)

for warning in warnings:
    print(f"  ⚠ {warning}")

summary = (f"{len(measured)} measured, {len(stale)} stale, {len(below)} below the floor, "
           f"{len(never)} never measured")
if mean is not None:
    summary += f"; mean Δ {mean:+.2f} over the fresh measurements (as of {as_of})"

if failures:
    print(f"\n{len(failures)} stale measurement(s):\n", file=sys.stderr)
    for problem in failures:
        print(f"  ✘ {problem}", file=sys.stderr)
    print(f"\n  The score is never gated — only its bookkeeping is. {summary}.", file=sys.stderr)
    sys.exit(1)

print(f"✔ board: {summary}")
