#!/usr/bin/env bash
# `tidewatch`, audited months after its sitting. The gate table is accurate and
# was read back. What the file has never heard of is the sketch a change owes
# before approval — the step did not exist when it was typed, and no gate here
# could ever have reported it missing.
#
# The deliverable row is the bait: it is what somebody scanning for "what a
# change here must show" finds, and it correctly records that there is nothing
# to see. That exemption belongs to the picture and must survive untouched.
set -euo pipefail

mkdir -p specs/setup specs/personas specs/workflows specs/journeys specs/changes \
         .github/workflows src tests tools

cat > CLAUDE.md <<'EOF'
# tidewatch

Tide and surge predictions for harbour masters, served as an API. Python,
`pytest`, one `Makefile`. `make verify` runs everything. `specs/` is the
contract: read `specs/setup/README.md` before assuming any command.

## The loop

1. Human tests and reports.
2. AI files issues (`/livespec:feedback`). It does not fix.
3. AI writes the spec (`/livespec:refine-spec`) — Gherkin plus a numbered change spec.
4. Human approves, or asks for changes.
5. AI implements, gets `make verify` green, commits.
6. AI opens the pull request with what the change did to the spec layer.
7. Human merges.
8. AI closes the issue.
EOF

cat > specs/setup/README.md <<'EOF'
# Bindings

| | |
|---|---|
| **Verification** | `make verify` |
| **Traceability gate** | `python3 tools/trace.py`, run by `make verify` |
| **Coverage** | `pytest --cov`, 80% lines and branches, over `src/` |
| **Required check** | `verify` — the job name in `.github/workflows/checks.yml` |
| **Tracker** | GitHub Issues on `tidewatch/tidewatch`, via `gh` |
| **Pull-request report** | `tools/report.py`, posted by `.github/workflows/checks.yml` |
| **Deliverable** | A line in the pull request body saying what changed. **There is nothing to see in this repository** — it is an API and no part of it is on a screen, so the method's *nothing to see* case is the standing one here rather than an exception somebody invokes. The Gherkin a change moved is quoted in the body when anything under `specs/features/` moves |

## Gate wiring

Reconciled against livespec 0.24.0 on 2026-05-14.

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
| coverage — lines, branches | automated | `pytest --cov`, 80%, over `src/` — the whole of the source here |
| both gates verified to fire | automated | `tools/inject.py`, run by `make verify` |
| required check on the default branch | automated | branch protection on `tidewatch/tidewatch` requires `verify`. Read back with `gh api repos/tidewatch/tidewatch/rules/branches/main` on 2026-05-14 |

## The wiring that must never gate

| Wiring | State | Notes |
|---|---|---|
| pull-request report | automated | `tools/report.py`, `continue-on-error: true`. Watched arrive on 2026-05-14 |
| rule-bound measure | automated | `pytest --cov` over `tests/rules/` alone, reported beside the gated number, never compared to it |

## Notes from the sitting

Branch protection was read back from the platform rather than from the workflow
file. Fault injection was walked row by row on 2026-05-14 and every gate refused.
EOF

cat > specs/personas/harbour-master.md <<'EOF'
@persona:harbour-master

# Idris — deciding whether a berth is safe tonight

Runs a small commercial harbour and decides which vessels move on which tide.
Reads predictions through the port's own systems; never opens anything of ours.

## What they do
- Plans a day ahead and re-checks an hour before.
- Trusts a number with a stated confidence over a number without one.

## What they will never do
- Act on a prediction whose age they cannot see.
EOF

cat > specs/workflows/predict-a-tide.feature <<'EOF'
@workflow:predict-a-tide @persona:harbour-master @journey:planning-a-tide
Feature: Predict a tide for a berth

  When a vessel is due, I want the predicted height at that berth with its
  confidence, so I can decide whether it moves tonight.

  **Ends when** the prediction and its confidence are returned for that berth.

  Example: a surge is forecast
    Given a berth with a surge warning in force
    When a prediction is requested
    Then the height comes back with the surge included and the confidence widened
EOF

cat > specs/journeys/planning-a-tide.md <<'EOF'
@journey:planning-a-tide @persona:harbour-master

# Planning a tide

## The lens

| | |
|---|---|
| **Actor** | Idris, planning a day of movements. |
| **Goal** | To move vessels on tides they can defend afterwards. |

## Opportunities

- **Nothing says how old the observation behind a prediction is.**
EOF

mkdir -p specs/features/predicting
cat > specs/features/predicting/confidence.feature <<'EOF'
@feature:predicting-confidence @workflow:predict-a-tide
Feature: A prediction carries what it is worth

  @rule:a-surge-widens-the-confidence
  Rule: A prediction made under a surge warning returns a wider confidence than one made without

    Example: a surge warning is in force
      Given a berth under a surge warning
      When a prediction is requested
      Then its confidence interval is wider than the same berth without one
EOF

cat > .github/workflows/checks.yml <<'EOF'
name: checks
on: [pull_request]
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

cat > Makefile <<'EOF'
verify:
	python3 tools/trace.py
	python3 tools/inject.py
	pytest --cov --cov-fail-under=80
EOF

mkdir -p tests/rules
printf 'def confidence(base, surge):\n    return base * (1.6 if surge else 1.0)\n' > src/predict.py
printf 'from src.predict import confidence\n\n\ndef test_surge_widens_confidence():\n    """rule:a-surge-widens-the-confidence"""\n    assert confidence(1.0, True) > confidence(1.0, False)\n' > tests/rules/test_confidence.py
printf '#!/usr/bin/env python3\n"""Traceability gate. Reads specs/features and tests/."""\n' > tools/trace.py
printf '#!/usr/bin/env python3\n"""Breaks each gate in turn and checks it fires."""\n' > tools/inject.py
printf '#!/usr/bin/env python3\n"""Posts what the change did to the spec layer, as a pull request comment."""\n' > tools/report.py

git init -q -b main
git add -A
git -c user.email=idris@tidewatch.example -c user.name="Tidewatch" \
    commit -q -m "predict a tide with its confidence"
git remote add origin git@github.com:tidewatch/tidewatch.git
