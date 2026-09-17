#!/usr/bin/env bash
# The fixture for 29: streaks, a habit tracker whose grace setting has three names — grace_hours in the loader, graceWindow in the settings file, 'the grace period' in the docs — and whose bindings name no drawing tool. The case grades saying the sketch is absent rather than filling it; src/ arms no-source-edits.
set -euo pipefail

mkdir -p specs/setup specs/personas specs/workflows specs/features/streak specs/changes src docs

cat > CLAUDE.md <<'EOF'
# streaks

A habit tracker for one person keeping a personal streak on their own machine.
`specs/` is the contract: read `specs/setup/README.md` before assuming a
command; spec before code.
EOF

cat > specs/setup/README.md <<'EOF'
# Bindings

| | |
|---|---|
| **Where the app runs** | `python3 -m streaks` |
| **Tests** | `pytest -q` |
| **Traceability check** | `python3 tools/trace.py` |
| **Tracker** | none — requests arrive in conversation and become change specs |
| **Change specs** | `specs/changes/NNNN-<slug>.md`, numbered one past the highest |
EOF

cat > specs/spec.md <<'EOF'
# streaks

One person, one or more **habits**, each with a **streak**: consecutive days
done. A missed day breaks the streak unless it falls inside the **grace
period**. A **weekly review** shows the week in sections.

What it is not: a team tool, a coach, a social feed.
EOF

cat > specs/personas/streak-keeper.md <<'EOF'
@persona:streak-keeper

# The streak keeper

Keeps a few personal habits and cares about not breaking the chain. Checks in
once a day, glances at the weekly review on Sundays. Not a team, not a coach.
EOF

cat > specs/workflows/keep-the-streak.feature <<'EOF'
@workflow:keep-the-streak @persona:streak-keeper
Feature: Keep the streak through the week

  Example: a day is marked done
    Given a habit with a streak of 6
    When today is marked done
    Then the streak reads 7

  Example: the Sunday review
    Given a week of check-ins
    When the weekly review opens
    Then the week is shown by section
EOF

cat > specs/features/streak/missed-day.feature <<'EOF'
@feature:missed-day @workflow:keep-the-streak
Feature: What a missed day does to a streak

  @rule:a-missed-day-inside-grace-keeps-the-streak
  Rule: a day missed inside the grace period does not break the streak

    Example: caught up next morning
      Given a streak of 6 and a grace period of 12 hours
      When yesterday is marked done at 08:00 today
      Then the streak reads 7
EOF

cat > specs/changes/0001-streaks.md <<'EOF'
# Spec 0001: streaks and the grace period

- **Status:** shipped
EOF

: > src/__init__.py

cat > src/loader.py <<'EOF'
import json
from pathlib import Path

DEFAULTS = {"grace_hours": 12}


def load(path: Path) -> dict:
    data = json.loads(path.read_text()) if path.exists() else {}
    return {"grace_hours": data.get("graceWindow", DEFAULTS["grace_hours"])}
EOF

cat > src/settings.py <<'EOF'
import json
from pathlib import Path


def write(path: Path, grace_hours: int) -> None:
    path.write_text(json.dumps({"graceWindow": grace_hours}, indent=2))
EOF

cat > src/review.py <<'EOF'
SECTIONS = ["Done this week", "Missed", "Longest streak", "At risk", "Notes", "Next week"]


def render(week: dict, expanded: set[str] | None = None) -> str:
    expanded = set(SECTIONS) if expanded is None else expanded
    return "\n".join(f"{'▾' if s in expanded else '▸'} {s}" for s in SECTIONS)
EOF

cat > docs/settings.md <<'EOF'
# Settings

The settings file lives next to the data. The only setting today is the grace
period — how long a missed day stays forgivable. Twelve hours by default.
EOF
