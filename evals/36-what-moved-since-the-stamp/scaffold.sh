#!/usr/bin/env bash
# `saltmarsh`, a tide and mooring log for one small harbour. Set up on livespec
# 0.25.0 on 2026-08-30 and correct as of it: every gate row accurate and read
# back, both never-gating rows present, the coverage exclusion in the tool's own
# config. The plugin has moved on since and the record has not — four things
# are owed, none of which announces itself, and two entries in the range ask
# nothing of this repository at all. See case.yaml.
set -euo pipefail

mkdir -p specs/setup specs/personas specs/workflows specs/journeys specs/changes \
         specs/features/moorings .github/workflows docs/feedback docs/screenshots \
         src/importer tests/rules tools

cat > CLAUDE.md <<'EOF'
# saltmarsh

A tide and mooring log for one small harbour. Every **berth** records the boat
on it, the tide it was taken on, and the tide it has to be off by. Python,
`pytest`, one `Makefile`. `make verify` runs everything. `specs/` is the
contract: read `specs/setup/README.md` before assuming any command.

## The loop

1. Human tests and reports.
2. AI files issues (`/livespec:feedback`). It investigates first. It does not fix.
3. AI writes the spec (`/livespec:refine-spec`) — Gherkin plus a numbered change spec.
4. Human approves, or asks for changes.
5. AI implements, gets `make verify` green, commits.
6. AI records the clip (`/livespec:record-clip`) and opens the pull request.
7. Human merges.
8. AI closes the issue.

Setting the process up again anywhere is `/livespec:setup`.

## The rules worth having in front of you

- Spec before code. One change per version.
- **Feedback is never fixed on the spot** — it gets tracked and specced.
- Never touch `src/` from a skill.
- Rule ids are permanent. Renaming one orphans every test pointing at it.
- Every commit green.

## Labels

`from-feedback` marks anything that came out of a human testing session.

## Commands

```sh
make verify
```
EOF

cat > specs/setup/README.md <<'EOF'
# Bindings

Every livespec skill reads this file before it assumes a command. Everything in
it is a fact about **this repository**.

Reconciled against livespec **0.25.0** on **2026-08-30**.

## The table

| | |
|---|---|
| **Verification** | `make verify` |
| **Traceability gate** | `python3 tools/trace.py`, run by `make verify` |
| **Coverage** | `pytest --cov`, `fail_under` in `pyproject.toml`, over `src/` with `src/importer/` excluded there |
| **Required check** | `verify` — the job name in `.github/workflows/checks.yml` |
| **Tracker** | GitHub Issues on `saltmarsh/saltmarsh`, via `gh` |
| **Screenshot home** | `docs/feedback/`, committed and pushed; deleted when the issue closes |
| **Pull-request report** | `tools/report.py`, posted by `.github/workflows/checks.yml` |
| **Deliverable of a version** | A clip in `docs/screenshots/`, recorded from the app on the branch before the pull request is opened, plus the Gherkin a change moved quoted in the body. A line of text is right when there is nothing to see |

## Gate wiring

Reconciled against livespec **0.25.0** on **2026-08-30**.

| Gate | State | Wired by, or why not |
|---|---|---|
| rule → test | automated | `python3 tools/trace.py` — refused spec 0003 for a rule no test claimed |
| test → rule | automated | `python3 tools/trace.py` |
| feature → workflow | automated | `python3 tools/trace.py` |
| workflow → feature | automated | `python3 tools/trace.py` |
| workflow → test | automated | `python3 tools/trace.py` |
| workflow → persona | automated | `python3 tools/trace.py` |
| persona → workflow | automated | `python3 tools/trace.py` |
| journey → workflow | automated | `python3 tools/trace.py` |
| coverage — lines, branches | automated | `pytest --cov`, `fail_under` in `pyproject.toml`, over `src/` with `src/importer/` excluded there. Refused a drop on 2026-08-27. Sitting exactly on the floor as of 2026-08-30 |
| both gates verified to fire | automated | `tools/inject.py`, run by `make verify` |
| required check on the default branch | automated | branch protection on `saltmarsh/saltmarsh` requires `verify`, and a merge is blocked when it fails. Read back with `gh api repos/saltmarsh/saltmarsh/rules/branches/main` on 2026-08-30; nobody may bypass |

**Second reading, 2026-08-31** (`/livespec:doctor`). Every row above re-read
against the tree and the platform; nothing moved. The one open issue, #12, was
filed with `/livespec:feedback` on 2026-08-31 and is waiting on a spec.

## The wiring that must never gate

| Wiring | State | Notes |
|---|---|---|
| pull-request report | automated | `tools/report.py`, `continue-on-error: true`. Watched arrive on 2026-08-30 |
| rule-bound measure | automated | `pytest --cov` over `tests/rules/` alone, reported beside the gated number, never compared to it |

## What coverage does not cover

`src/importer/` reads the harbour's old spreadsheet exports and is excluded in
`pyproject.toml`, where the coverage tool reads it rather than only here. It goes
when the last export has been migrated.
EOF

cat > pyproject.toml <<'EOF'
[tool.coverage.run]
omit = ["src/importer/*"]

[tool.coverage.report]
# 86.20 (2026-07-14) → 88.75 (2026-08-02) → 90.10 (2026-08-19) → 91.35 (2026-08-30)
# each one the figure the report printed that day, rounded down
fail_under = 91.35
EOF

cat > Makefile <<'EOF'
verify:
	python3 tools/trace.py
	python3 tools/inject.py
	pytest --cov
EOF

cat > specs/features/moorings/berth.feature <<'EOF'
@feature:moorings-berth @workflow:take-a-berth
Feature: What a berth records

  @rule:a-berth-records-the-tide-it-must-be-off-by
  Rule: A berth is not taken until the tide it has to be clear by is recorded

    Example: the boat comes alongside on the morning tide
      Given a boat coming alongside on a recorded tide
      When the harbourmaster enters the tide it must be off by
      Then the berth is taken
EOF

cat > specs/workflows/take-a-berth.feature <<'EOF'
@workflow:take-a-berth @persona:harbourmaster @journey:trusting-the-log
Feature: Taking a berth from the boat arriving to the tide it must be clear by
EOF

printf '# harbourmaster\n\nOne harbourmaster, forty berths, two tides a day.\n' > specs/personas/harbourmaster.md
printf '# trusting-the-log\n\nThe first season of writing every berth down.\n' > specs/journeys/trusting-the-log.md

printf 'def clear_by(taken, tides):\n    return taken + tides\n' > src/tide.py
printf 'def read_export(path):\n    raise NotImplementedError\n' > src/importer/legacy.py
printf 'from src.tide import clear_by\n\n\ndef test_clear_by_counts_tides():\n    """rule:a-berth-records-the-tide-it-must-be-off-by"""\n    assert clear_by(3, 2) == 5\n' > tests/rules/test_tide.py

printf '#!/usr/bin/env python3\n"""Traceability gate. Reads specs/features and tests/."""\n' > tools/trace.py
printf '#!/usr/bin/env python3\n"""Breaks each gate in turn and checks it fires."""\n' > tools/inject.py
printf '#!/usr/bin/env python3\n"""Posts what the change did to the spec layer, as a pull request comment."""\n' > tools/report.py
printf 'Screenshots attached to open issues live here.\n' > docs/feedback/.gitkeep
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
git -c user.email=morag@saltmarsh.example -c user.name="Saltmarsh" \
    commit -q -m "record the tide a berth must be clear by"
git remote add origin git@github.com:saltmarsh/saltmarsh.git
