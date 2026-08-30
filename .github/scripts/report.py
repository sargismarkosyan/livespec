#!/usr/bin/env python3
"""The pull-request report. Describes a green run; decides nothing.

`gates.md` declares this **not a gate**: it runs after both gates have passed,
it cannot fail a build, and it recomputes nothing. That last one is the reason
this file is thirty lines of formatting rather than a second traversal of
`specs/` — the numbers come from `trace.py --json`, which is the only thing here
that parses the spec layer. A report that re-derived them would be a second copy
of the gate's logic, correct on the day it was written and drifting after.

What it reports is **what moved**, not what exists. "12 live rules" tells a
reviewer nothing about the change in front of them; "+1" is the whole point.

    python3 .github/scripts/report.py <branch.json> [base.json] [branch-board.json] [base-board.json]

The first two files are `trace.py --json` output — the branch's, and the base
ref's. Without the second it prints the totals and says the comparison was
unavailable, which is honest and still worth reading. The last two are
`board.py --json` — the eval board's counts; missing, the board section is
skipped rather than guessed.

Nothing here may exit non-zero for any reason. See `always-green` in
specs/spec.md: a report that can fail a build is a gate nobody declared.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

FOOTER = (
    "<sub>Posted by `.github/scripts/report.py`. Reporting only — it cannot fail "
    "a build, and it recomputes nothing: every number here comes from "
    "`trace.py --json` and `board.py --json`.</sub>"
)

# (heading, [(label, path-into-the-json)]). The order is the order somebody
# reads it in: who it is for, then what they attempt, then what is promised.
SECTIONS = [
    ("Spec health", [
        ("Personas", ("personas", "live")),
        ("Journeys", ("journeys",)),
        ("Workflows", ("workflows", "total")),
        ("Feature files", ("features",)),
        ("Live rules", ("rules", "live")),
        ("Planned rules", ("rules", "planned")),
    ]),
    ("The eval suite", [
        ("Cases", ("cases", "total")),
        ("Cases claiming a rule or workflow", ("cases", "claiming")),
        ("Should-not-fire cases", ("cases", "negative")),
    ]),
]


def dig(data: dict | None, path: tuple[str, ...]) -> int | None:
    for key in path:
        if not isinstance(data, dict) or key not in data:
            return None
        data = data[key]
    return data if isinstance(data, int) else None


def delta(base: int | None, head: int | None) -> str:
    if base is None or head is None or base == head:
        return "–"
    return f"{head - base:+d}"


def table(rows: list[tuple[str, tuple[str, ...]]], base: dict | None, head: dict) -> list[str]:
    out = ["| | `main` | this branch | |", "| --- | ---: | ---: | :--- |"]
    for label, path in rows:
        here = dig(head, path)
        there = dig(base, path)
        out.append(f"| {label} | {'?' if there is None else there} | "
                   f"{'?' if here is None else here} | {delta(there, here)} |")
    return out


BOARD_ROWS = [
    ("Measured, still fresh", ("measured",)),
    ("Stale — inputs changed since", ("stale",)),
    ("Below the floor — a pilot, not a measurement", ("below",)),
    ("Never measured", ("never",)),
]


def board_section(head: dict | None, base: dict | None) -> list[str]:
    # The eval board's counts. A measurement is rarely re-run on a pull
    # request, so the mean is dated rather than dressed up as current.
    if not isinstance(head, dict):
        return []
    lines = ["## The eval board", ""] + table(BOARD_ROWS, base, head) + [""]
    mean = head.get("mean_delta")
    if isinstance(mean, (int, float)):
        dated = f" (as of {head['as_of']})" if head.get("as_of") else ""
        was = base.get("mean_delta") if isinstance(base, dict) else None
        versus = f", was {was:+.2f} on `main`" if isinstance(was, (int, float)) else ""
        lines += [f"Mean Δ over the fresh measurements: **{mean:+.2f}**{dated}{versus}.", ""]
    else:
        lines += ["No fresh measurement to average yet.", ""]
    return lines


def build(head: dict, base: dict | None, board_head: dict | None = None, board_base: dict | None = None) -> str:
    lines: list[str] = []
    for heading, rows in SECTIONS:
        lines += [f"## {heading}", ""] + table(rows, base, head) + [""]
    lines += board_section(board_head, board_base)

    planned = dig(head, ("rules", "planned")) or 0
    if planned:
        lines += [f"**{planned} rule(s) still tagged `@planned`** — specced and not built yet.", ""]
    else:
        lines += ["Nothing is left tagged `@planned` — every written rule is built "
                  "and claimed by a case.", ""]

    if base is None:
        lines += ["The `main` column could not be read, so the change column is "
                  "blank rather than guessed.", ""]
    lines.append(FOOTER)
    return "\n".join(lines)


def main() -> int:
    try:
        head = json.loads(Path(sys.argv[1]).read_text())
    except Exception as error:  # noqa: BLE001 — see the module docstring
        print(f"<!-- report: no numbers for this branch ({error}) -->")
        return 0
    optional = []
    for index in (2, 3, 4):
        try:
            optional.append(json.loads(Path(sys.argv[index]).read_text()))
        except Exception:  # noqa: BLE001 — a missing input is a blank column, not a failure
            optional.append(None)
    base, board_head, board_base = optional
    try:
        print(build(head, base, board_head, board_base))
    except Exception as error:  # noqa: BLE001
        print(f"<!-- report: could not be built ({error}) -->")
    return 0


if __name__ == "__main__":
    sys.exit(main())
