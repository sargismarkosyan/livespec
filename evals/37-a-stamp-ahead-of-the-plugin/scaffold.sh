#!/usr/bin/env bash
# `ridgeline`, a trail-conditions log. Its ledger is stamped against livespec
# 9.4.0, which no installed plugin has reached. Everything else is ordinary,
# with one gap left in prose so the audit has something to carry on to.
set -euo pipefail

mkdir -p specs/setup specs/personas specs/workflows specs/journeys specs/changes \
         specs/features/trails .github/workflows docs/screenshots src tests/rules tools

cat > CLAUDE.md <<'EOF'
# ridgeline

A trail-conditions log for one national park. Every **report** records the
trail, the day, and what a ranger found on it. Python, `pytest`, one
`Makefile`. `make verify` runs everything. `specs/` is the contract: read
`specs/setup/README.md` before assuming any command.

## The loop

1. Human walks the trails and reports.
2. AI files issues (`/livespec:todo`). It does not fix.
3. AI writes the spec (`/livespec:refine-spec`) — Gherkin plus a numbered change spec, and draws the sketch.
4. Human approves the spec and the sketch, or asks for changes.
5. AI implements, gets `make verify` green, commits.
6. AI records the clip (`/livespec:record-clip`) and opens the pull request.
7. Human merges.
8. AI closes the issue.

## Commands

```sh
make verify
```
EOF

cat > specs/setup/README.md <<'EOF'
# Bindings

Every livespec skill reads this file before it assumes a command.

Reconciled against livespec **9.4.0** on **2026-08-30**.

## The table

| | |
|---|---|
| **Verification** | `make verify` |
| **Traceability gate** | `python3 tools/trace.py`, run by `make verify` |
| **Coverage** | `pytest --cov`, 100% of what remains, over `src/` with nothing excluded |
| **Required check** | `verify` — the job name in `.github/workflows/checks.yml` |
| **Tracker** | GitHub Issues on `ridgeline/ridgeline`, via `gh` |
| **Pull-request report** | `tools/report.py`, posted by `.github/workflows/checks.yml` |
| **Deliverable of a version** | A clip in `docs/screenshots/`, plus the Gherkin a change moved quoted in the body |
| **Sketch before approval** | Every change spec is handed over with a page showing the before and after. Drawn from the spec, not recorded from the app |

## Gate wiring

Reconciled against livespec **9.4.0** on **2026-08-30**.

| Gate | State | Wired by, or why not |
|---|---|---|
| rule → test | automated | `python3 tools/trace.py` |
| test → rule | automated | `python3 tools/trace.py` |
| feature → workflow | automated | `python3 tools/trace.py` |
| workflow → feature | automated | `python3 tools/trace.py` |
| workflow → test | automated | `python3 tools/trace.py` |
| workflow → persona | automated | `python3 tools/trace.py` |
| persona → workflow | automated | `python3 tools/trace.py` |
| journey → workflow | automated | `python3 tools/trace.py` |
| coverage — lines, branches | automated | `pytest --cov`, 100% of `src/`, nothing excluded |
| both gates verified to fire | automated | `tools/inject.py`, run by `make verify` |
| required check on the default branch | automated | branch protection on `ridgeline/ridgeline` requires `verify`. Read back with `gh api repos/ridgeline/ridgeline/rules/branches/main` on 2026-08-30 |

## The wiring that must never gate

| Wiring | State | Notes |
|---|---|---|
| pull-request report | automated | `tools/report.py`, `continue-on-error: true`. Watched arrive on 2026-08-30 |

The rule-bound measure — the second coverage pass over `tests/rules/` alone,
reported beside the gated number — is not built yet. We should add it once the
report settles down.
EOF

cat > pyproject.toml <<'EOF'
[tool.coverage.report]
fail_under = 100
EOF

cat > Makefile <<'EOF'
verify:
	python3 tools/trace.py
	python3 tools/inject.py
	pytest --cov
EOF

cat > specs/features/trails/report.feature <<'EOF'
@feature:trails-report @workflow:file-a-report
Feature: What a trail report records

  @rule:a-report-names-the-day-it-was-walked
  Rule: A report is not filed until the day the trail was walked is recorded

    Example: the ranger files the day's walk
      Given a trail walked today
      When the ranger enters the day
      Then the report is filed
EOF

cat > specs/workflows/file-a-report.feature <<'EOF'
@workflow:file-a-report @persona:ranger @journey:trusting-the-log
Feature: Filing a trail report from the walk to the day it is recorded against
EOF

printf '# ranger\n\nOne ranger, twelve trails, a walk a week each.\n' > specs/personas/ranger.md
printf '# trusting-the-log\n\nThe first season of writing every walk down.\n' > specs/journeys/trusting-the-log.md
printf 'def walked(day, days):\n    return day in days\n' > src/report.py
printf 'from src.report import walked\n\n\ndef test_walked_day_is_found():\n    """rule:a-report-names-the-day-it-was-walked"""\n    assert walked(3, [1, 3])\n' > tests/rules/test_report.py
printf '#!/usr/bin/env python3\n"""Traceability gate. Reads specs/features and tests/."""\n' > tools/trace.py
printf '#!/usr/bin/env python3\n"""Breaks each gate in turn and checks it fires."""\n' > tools/inject.py
printf '#!/usr/bin/env python3\n"""Posts what the change did to the spec layer, as a pull request comment."""\n' > tools/report.py
printf 'Clips a version ships with live here.\n' > docs/screenshots/.gitkeep

cat > .github/workflows/checks.yml <<'EOF'
name: checks
on: [pull_request, push]
jobs:
  verify:
    name: verify
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: make verify
      - run: python3 tools/report.py
        continue-on-error: true
EOF

git init -q -b main
git add -A
git -c user.email=ash@ridgeline.example -c user.name="Ridgeline" \
    commit -q -m "record the day a trail was walked"
git remote add origin git@github.com:ridgeline/ridgeline.git
