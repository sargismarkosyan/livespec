#!/usr/bin/env python3
"""The board of latest measurements — reported, never gated.

`evals/board.json` records what the last runs measured, and beside each number
a hash of what it was a measurement *of*. It holds two kinds of row:

**The tiers** — `route`, `first`, `review` — one call each, written by
`evals/runner/tiers.py`. **The canary pool** — `cases`, the sittings `run.py`
drives.

A row whose inputs no longer match is **stale**: shown as stale, and left out
of every count and mean, because a number that no longer describes the files
is never presented as though it did. A row that does not exist yet, or rests
on fewer runs than the floor, is shown and not counted.

**Nothing here is owed.** A run costs money and happens when the maintainer
chooses, so this exits 0 whatever it finds — see specs/changes/0087. Neither
freshness nor the score is gated: method/graded-cases.md.

Run: python3 .github/scripts/board.py [root] [--json]

`--json` prints the counts for the pull-request report.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from caselib import (  # noqa: E402
    HARNESS_FILES, MIN_RUNS, SESSION_MODEL, TIER_HARNESS_FILES, TIERS, cases, is_measurement, tier_keys,
    tier_why_stale, why_stale,
)

AS_JSON = "--json" in sys.argv
args = [a for a in sys.argv[1:] if a != "--json"]
ROOT = Path(args[0]).resolve() if args else Path(__file__).resolve().parents[2]

# Quoted without the approval flag on purpose: a stale row is a reason to ask
# the maintainer for a run, never a licence to start one, and a command that
# spends money should not be copy-pasteable out of a gate's output.
HEAL = ("python3 evals/runner/tiers.py --changed --scaffold\n"
        "      (spends real money, a call at a time — the maintainer adds --i-approve-the-cost, nobody else)")

TIER_WORDS = {
    "route": "which skill fires",
    "first": "the first move",
    "review": "the rules the skill body still tells",
}

failures: list[str] = []
warnings: list[str] = []
notes: list[str] = []

board_path = ROOT / "evals" / "board.json"
try:
    board = json.loads(board_path.read_text())
except (OSError, json.JSONDecodeError):
    board = {}

suite = cases(ROOT)

# --- the tiers: freshness is the gate ---------------------------------------
tier_counts: dict[str, dict[str, int]] = {}
first_deltas: list[float] = []
tier_as_of = ""
for tier in TIERS:
    rows = board.get(tier) if isinstance(board.get(tier), dict) else {}
    expected = tier_keys(tier, suite, ROOT)
    counts = {"measured": 0, "stale": 0, "never": 0, "below": 0}
    never: list[str] = []
    below: list[str] = []
    for key in expected:
        entry = rows.get(key)
        reasons = tier_why_stale(tier, key, entry, suite, ROOT)
        if reasons == ["never measured"]:
            counts["never"] += 1
            never.append(key)
            continue
        if reasons:
            counts["stale"] += 1
            said = []
            if "inputs" in reasons:
                said.append({"route": "a skill's description or the case has changed since",
                             "first": "the case, a rule it claims or a skill it holds has changed since",
                             "review": "the skill or a rule it upholds has changed since"}[tier])
            if "graders" in reasons:
                said.append("a rubric has changed since")
            if "model" in reasons:
                said.append(f"it was measured on {entry.get('model') or 'an unknown model'}; "
                            f"the suite measures on {SESSION_MODEL}")
            if "harness" in reasons:
                said.append(f"it was measured by a tier harness that has since changed ({', '.join(TIER_HARNESS_FILES)})")
            failures.append(
                f"{tier} {key} ({TIER_WORDS[tier]}): measured at {entry.get('sha', '?')} ({entry.get('at', '?')}), but "
                + "; ".join(said)
                + f". The number no longer describes these files. Re-measure exactly what changed:\n      {HEAL}"
            )
            continue
        # A pilot's row is fresh and still not a measurement (#75): kept,
        # shown, left out of the count and the mean. A review is one reading
        # and carries no runs.
        if tier != "review" and not is_measurement(entry):
            counts["below"] += 1
            below.append(f"{key} ({entry.get('runs', '?')})")
            continue
        counts["measured"] += 1
        tier_as_of = max(tier_as_of, str(entry.get("at", "")))
        if tier == "first" and isinstance(entry.get("delta"), (int, float)):
            first_deltas.append(float(entry["delta"]))
    for key in sorted(set(rows) - set(expected)):
        warnings.append(f"evals/board.json: {tier} row for {key!r}, which the {tier} tier no longer measures; remove the row")
    if never:
        listed = ", ".join(never[:5]) + ("…" if len(never) > 5 else "")
        warnings.append(f"{len(never)} {tier} row(s) never measured ({listed}) — the tier fills as runs happen; "
                        f"the bootstrap's to-do list, not a failure")
    if below:
        listed = ", ".join(below[:5]) + ("…" if len(below) > 5 else "")
        warnings.append(f"{len(below)} {tier} row(s) below the floor of {MIN_RUNS} runs ({listed}) — pilots, kept "
                        f"and shown but not counted as measurements and not in the mean")
    tier_counts[tier] = counts

# --- the canary pool: shown, never gated ------------------------------------
entries = board.get("cases") if isinstance(board.get("cases"), dict) else {}
canary = {"measured": 0, "stale": 0, "below": 0, "never": 0}
canary_deltas: list[float] = []
canary_as_of = ""
stale_names: list[str] = []
below_names: list[str] = []
for case in suite:
    entry = entries.get(case["name"])
    if entry is None:
        canary["never"] += 1
        continue
    # Staleness is asked first, and of every row: a number that no longer
    # describes these files is not shown as though it did, however many runs
    # produced it. It is not a failure either — the tiers carry freshness now.
    if why_stale(entry, case, ROOT):
        canary["stale"] += 1
        stale_names.append(case["name"])
        continue
    if not is_measurement(entry):
        canary["below"] += 1
        below_names.append(case["name"])
        continue
    canary["measured"] += 1
    if isinstance(entry.get("delta"), (int, float)):
        canary_deltas.append(float(entry["delta"]))
    canary_as_of = max(canary_as_of, str(entry.get("at", "")))

for name in sorted(set(entries) - {c["name"] for c in suite}):
    warnings.append(f"evals/board.json: canary row for {name!r}, which is not a case any more; remove the row")
if stale_names:
    listed = ", ".join(stale_names[:5]) + ("…" if len(stale_names) > 5 else "")
    warnings.append(
        f"canary pool: {len(stale_names)} sitting(s) stale ({listed}) — shown as stale, not counted, not "
        f"averaged, and not owed: a sitting is run again when the model moves or the maintainer chooses "
        f"(evals/runner/run.py; {', '.join(HARNESS_FILES)} and the bindings' model stale it too)"
    )
if below_names:
    listed = ", ".join(f"{n} ({entries[n].get('runs', '?')})" for n in below_names[:5]) + ("…" if len(below_names) > 5 else "")
    warnings.append(
        f"canary pool: {len(below_names)} row(s) below the floor of {MIN_RUNS} runs ({listed}) — pilots, "
        f"kept and shown but not counted as measurements and not in the mean"
    )
if canary["never"]:
    notes.append(f"canary pool: {canary['never']} case(s) never sat — nothing is owed; a sitting is the maintainer's choice")


def mean(values: list[float]) -> float | None:
    return round(sum(values) / len(values), 2) if values else None


if AS_JSON:
    # A hand-over for the report, never a gate: exits 0 whatever it found, so
    # a stale board can still be *reported* — which is when the row matters.
    print(json.dumps({
        "measured": sum(c["measured"] for c in tier_counts.values()),
        "stale": sum(c["stale"] for c in tier_counts.values()),
        "never": sum(c["never"] for c in tier_counts.values()),
        "mean_delta": mean(first_deltas), "as_of": tier_as_of or None,
        "tiers": tier_counts,
        "canary": dict(canary, mean_delta=mean(canary_deltas), as_of=canary_as_of or None),
    }))
    sys.exit(0)

for warning in warnings:
    print(f"  ⚠ {warning}")
for note in notes:
    print(f"  · {note}")

parts = [f"{t} {c['measured']} fresh, {c['stale']} stale, {c['never']} never"
         + (f", {c['below']} below the floor" if c["below"] else "") for t, c in tier_counts.items()]
summary = "; ".join(parts)
if mean(first_deltas) is not None:
    summary += f"; mean first-move Δ {mean(first_deltas):+.2f} (as of {tier_as_of})"
summary += (f". Canary: {canary['measured']} fresh, {canary['stale']} stale, {canary['below']} below the floor"
            + (f", mean Δ {mean(canary_deltas):+.2f} over the fresh (as of {canary_as_of})" if canary_deltas else ""))

if failures:
    print(f"\n{len(failures)} stale tier row(s) — reported, not owed:\n")
    for problem in failures:
        print(f"  ⚠ {problem}")
print(f"✔ board: {summary}")
