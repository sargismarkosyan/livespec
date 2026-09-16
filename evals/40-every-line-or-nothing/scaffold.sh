#!/usr/bin/env bash
# tidelog: tide predictions for one harbour. Python, no database. The livespec
# process was installed in the spring at 0.28.0 and the ledger has not been read
# since. Every section of it has one thing wrong.
set -euo pipefail

mkdir -p specs/setup specs/personas specs/workflows specs/journeys specs/changes \
         specs/features/tides src/tidelog tests

cat > CLAUDE.md <<'MD'
# tidelog

Tide predictions for one harbour. Python 3.12; `make check` runs everything.
`specs/` is the contract — read `specs/setup/README.md` before assuming a command.

## The loop

1. Report what you found with `/livespec:feedback`.
2. `/livespec:refine-spec` writes the spec; approve it, then build.
MD

cat > specs/personas/harbourmaster.md <<'MD'
@persona:harbourmaster

# Ora — decides when the gate opens
MD
cat > specs/workflows/plan-a-tide.feature <<'MD'
@workflow:plan-a-tide @persona:harbourmaster @journey:a-season
Feature: Plan the day's gate times
MD
cat > specs/journeys/a-season.md <<'MD'
@journey:a-season @persona:harbourmaster

# A season at the harbour
MD
for n in 0001 0002 0003 0004 0005 0006; do
  printf '# Spec %s\n' "$n" > "specs/changes/${n}-change.md"
done
cat > specs/features/tides/predict.feature <<'MD'
@feature:tides-predict @workflow:plan-a-tide
Feature: Predict the tide

  @rule:a-prediction-names-its-source
  Rule: Every prediction says which table it came from

    Example: the ordinary case
      Given a harbour
      When a day is planned
      Then the source is on the plan
MD
echo "def predict(day): return day" > src/tidelog/__init__.py
echo "def test_predict(): pass" > tests/test_predict.py

cat > specs/setup/README.md <<'MD'
# Bindings

Everything here is true of tidelog and nothing else.

## The table

| | |
|---|---|
| **Verification** | `make check` |
| **What it returns** | 0 green, 1 red |
| **What it runs** | `python3 tools/trace.py`, then `pytest -q` |
| **Language** | Python 3.12 |
| **Package manager** | pip |
| **Traceability gate** | `python3 tools/trace.py` |
| **Coverage gate** | none — see *What has no gate* |
| **Coverage thresholds** | none |
| **Fault injection** | `python3 tools/inject.py` |
| **Required checks** | `check` |
| **Tracker** | GitHub Issues, via `gh issue create` |
| **Where the app runs** | `python3 -m tidelog` |
| **What a change here must show** | a screenshot of the plan |
| **A sketch is owed** | by every change spec |
| **Deliverable of a version** | the screenshot |
| **What proves a rule** | an ordinary test suite |
| **How a test claims its rule** | `rule()` from tests/rulelib.py |
| **Rule discovery** | specs/features/**/*.feature |
| **Spec-bound coverage** | not applicable — no coverage here |
| **Pull-request report** | `report.py`, posted by CI |
| **Audit record** | `specs/setup/audit.md` |
| **What a contributor owes a release** | a label and a changelog section |

## Gate wiring

**Reconciled against livespec 0.28.0 on 2026-04-02.**

| id | gate | state | evidence |
|---|---|---|---|
| `gate:rule-to-test` | a live rule no test claims | automated | `python3 tools/trace.py` |
| `gate:test-to-rule` | a test claiming a rule that does not exist | automated | `python3 tools/trace.py` |
| `gate:planned-unclaimed` | a planned rule that is claimed | automated | `python3 tools/trace.py` |
| `gate:feature-to-workflow` | a feature naming no workflow | automated | `python3 tools/trace.py` |
| `gate:workflow-to-feature` | a workflow claimed by no feature | automated | `python3 tools/trace.py` |
| `gate:workflow-walked` | a workflow walked by no test | deferred | since 0002 — no walkthrough yet |
| `gate:workflow-to-persona` | a workflow naming no live persona | automated | `python3 tools/trace.py` |
| `gate:persona-to-workflow` | a persona named by no workflow | not applicable | decided: no personas here, the audience is in the workflow |
| `gate:journey-to-workflow` | a journey naming a workflow that does not exist | automated | `python3 tools/trace.py` |
| `gate:workflow-to-journey` | a workflow naming no journey — warns | automated | `python3 tools/trace.py` |
| `gate:coverage` | lines, branches, functions | not applicable | no coverage here |
| `gate:boundary-double` | a rule-bound test doubling a boundary declared real | mostly | nobody checked |
| `gate:boundary-fake-suite` | a fake row naming no suite | not applicable | no fakes here |
| `gate:boundary-recorded-age` | a recorded row past its age | not applicable | no recordings here |
| `gate:boundaries-table` | rule-bound tests present and no boundaries table | not applicable | the table is below |
| `gate:verified-to-fire` | every gate broken on purpose and seen to fire | automated | `python3 tools/inject.py` |

### The wiring that must never gate

| id | wiring | state | evidence |
|---|---|---|---|
| `wiring:pr-report` | the pull-request report | unobserved | `report.py`, posted by CI |
| `wiring:rule-bound-measure` | the rule-bound measure | not applicable | no coverage here |

### The boundaries

| id | boundary | state | since | evidence |
|---|---|---|---|---|
| `boundary:tide-table` | the tide table service | mocked | 0002 | a fixture file; cover: none |
| `boundary:clock` | the clock | real | 0001 | the system clock; leaves uncovered: nothing |

### Workarounds

| instead | gap | filed | ends when |
|---|---|---|---|

## The fault injection record

| Injected fault | Expected | Result |
|---|---|---|
| live rule with no test | fails | ✔ |

## Branch protection

Read back with `gh api repos/harbour/tidelog/rulesets` on 2026-04-02: a merge is blocked when `check` fails.

## What has no gate, and what that misses

No coverage gate. The rule-bound measure is not built yet; we should add it once the suite settles.

## Notes from the sitting

Nothing runs on one machine that the pipeline does not.
MD
