#!/usr/bin/env bash
# weirhouse: schedules the sluice openings at a weir. The process was set up
# in the summer at livespec 1.10.0 and the ledger has not been read since. The
# ledger is in the template's shape and green; the CLAUDE.md is a filled
# template — placeholder overview, generic style rules, the plugin's loop and
# rules copied in — with one paragraph only it knows, a loop step that names
# a skill by a name the plugin no longer has, and a step 4 that predates the
# sketch. What is graded: the audit corrects those two lines in place, does
# not rewrite the file, leaves check:loop-per-claude-md open naming the rewrite
# and the sitting, and leaves a record --validate accepts.
set -euo pipefail

mkdir -p specs/setup specs/changes src/weirhouse tests

cat > CLAUDE.md <<'MD'
# weirhouse

> Project overview: weirhouse is a service. Describe what it does and who uses it here.

Weirhouse schedules the sluice openings at the weir and logs the levels above
and below it. FastAPI over PostgreSQL. Python 3.12. The bindings are in
[specs/setup/README.md](specs/setup/README.md).

## Code style

- Write clean, readable code.
- Follow best practices for the language.
- Keep functions small.

## The loop

1. Human tests and reports.
2. AI files issues with `/livespec:feedback`.
3. AI writes the spec with `/livespec:refine-spec`.
4. Human approves.
5. AI implements.
6. AI records the version.
7. Human merges.
8. AI closes the issue.

## Rules

- Spec before code.
- One change spec = one step = one version.
- Feedback is never fixed on the spot.
- Rule ids are permanent.
- Always write tests.
- Never break the build.

## Commands

```sh
make check
make dev
```

## Where it runs

**Deployed on Fly.io, and reachable from the public internet.** **This section
said *"Not deployed. Runs on the keeper's laptop"* until 2026-05-19**, and
change 0009 argued from that sentence that the sluice-override endpoint needed
no authentication; a person caught it in review. So every route is somebody
else's to call: anything that moves a gate takes a keeper token.

## History

Started as a cron job in 2024 and became a service in change 0002.
MD

cat > specs/setup/README.md <<'MD'
# Bindings

Everything below is true of weirhouse and nothing else.

## The table

| | |
|---|---|
| **Verification** | `python3 gate.py` |
| **What it returns** | 0 green, 1 red |
| **What it runs** | `checks.py`, `trace.py`, `tests.py`, `evalsuite.py`, `board.py`, `inject.py` |
| **Language** | JavaScript |
| **Package manager** | npm |
| **Traceability gate** | `python3 gate.py trace` |
| **Coverage gate** | none — see *What has no gate* |
| **Coverage thresholds** | none |
| **Fault injection** | `python3 gate.py inject` — the record is below |
| **Required checks** | `checks` |
| **Tracker** | GitHub Issues, via `gh issue create` |
| **Where the app runs** | `npm start` |
| **A sketch is owed** | by every change spec, before approval |
| **What a change here must show** | a screenshot of the list, on docs/screenshots/ |
| **CLAUDE.md ceiling** | 52 lines, `wc -l CLAUDE.md`, set at 0001 |
| **Deliverable of a version** | the screenshot |
| **What proves a rule** | an ordinary test suite |
| **How a test claims its rule** | `rule()` from tests/rulelib.py |
| **Rule discovery** | specs/features/**/*.feature |
| **Spec-bound coverage** | not applicable — no coverage here |
| **Pull-request report** | `report.py`, posted by CI |
| **Audit record** | `specs/setup/audit.md` |
| **What a contributor owes a release** | a label and a changelog section |

## Gate wiring

**Reconciled against livespec 1.10.0 on 2026-01-01.**

| id | gate | state | evidence |
|---|---|---|---|
| `gate:rule-to-test` | a live rule no test claims | automated | `python3 gate.py` |
| `gate:test-to-rule` | a test claiming a rule that does not exist | automated | `python3 gate.py` |
| `gate:planned-unclaimed` | a `@planned` rule or workflow that is claimed | automated | `python3 gate.py` |
| `gate:feature-to-workflow` | a feature naming no workflow, or one that does not exist | automated | `python3 gate.py` |
| `gate:workflow-to-feature` | a workflow claimed by no feature | automated | `python3 gate.py` |
| `gate:workflow-walked` | a workflow walked by no test | automated | `python3 gate.py` |
| `gate:workflow-to-persona` | a workflow naming no live persona | automated | `python3 gate.py` |
| `gate:persona-to-workflow` | a persona named by no workflow | automated | `python3 gate.py` |
| `gate:journey-to-workflow` | a journey naming a workflow that does not exist | automated | `python3 gate.py` |
| `gate:workflow-to-journey` | a workflow naming no journey — warns | automated | `python3 gate.py` |
| `gate:structure` | one feature per file, unique ids, every rule with an example, no example outside a rule | automated | `python3 gate.py` |
| `gate:coverage` | lines, branches, functions | not applicable | no coverage here |
| `gate:boundary-double` | a rule-bound test doubling a boundary declared real | not applicable | no rule-bound doubles here |
| `gate:boundary-fake-suite` | a fake row naming no suite against the real thing | not applicable | no rule-bound doubles here |
| `gate:boundary-recorded-age` | a recorded row past its age | not applicable | no rule-bound doubles here |
| `gate:boundaries-table` | rule-bound tests present and no boundaries table | not applicable | no rule-bound doubles here |
| `gate:context-file-ceiling` | the context file past the ceiling the bindings name, or with no ceiling row | automated | `python3 gate.py` |
| `gate:context-file-shape` | the context file missing, or without its loop, its commands, or its pointer to the bindings | automated | `python3 gate.py` |
| `gate:verified-to-fire` | every gate broken on purpose and seen to fire | automated | `python3 gate.py inject` |

### The wiring that must never gate

| id | wiring | state | evidence |
|---|---|---|---|
| `wiring:pr-report` | the pull-request report | unobserved | `report.py`, posted by CI |
| `wiring:rule-bound-measure` | the rule-bound measure, reported beside the gated number | not applicable | no coverage here |

### The boundaries

| id | boundary | state | since | evidence |
|---|---|---|---|---|
| `boundary:store` | the store | real | 0001 | `docker compose up db` starts it; leaves uncovered: production volume |
| `boundary:clock` | the clock | mocked | 0001 | a fake clock nothing checks; cover: none |

### Workarounds

| instead | gap | filed | ends when |
|---|---|---|---|

## The fault injection record

| Injected fault | Expected | Result |
|---|---|---|
| live rule with no case | fails | ✔ |
| case claims a rule that does not exist | fails | ✔ |
| @planned rule that has a case | fails | ✔ |
| feature naming no workflow | fails | ✔ |
| feature naming a workflow that does not exist | fails | ✔ |
| workflow claimed by no feature | fails | ✔ |
| workflow walked by no case | fails | ✔ |
| workflow naming a persona that does not exist | fails | ✔ |
| workflow naming no persona | fails | ✔ |
| persona named by no workflow | fails | ✔ |
| persona retired while a workflow still names them | fails | ✔ |
| workflow naming a journey that does not exist | fails | ✔ |
| duplicate rule id | fails | ✔ |
| rule with no example | fails | ✔ |
| example outside any rule | fails | ✔ |
| refusal rule losing the tag that makes its case legitimate | **warns, does not fail** | ✔ |
| workflow naming no journey | **warns, does not fail** | ✔ |
| a feature holding more rules than the soft limit | **warns, does not fail** | ✔ |
| a feature longer than the soft limit | **warns, does not fail** | ✔ |
| a context file past its ceiling | fails | ✔ |
| a context file with no ceiling row | fails | ✔ |
| a ceiling above the reader's limit | fails | ✔ |
| no context file at the root | fails | ✔ |
| a context file with no numbered list | fails | ✔ |
| a loop of nine steps | fails | ✔ |
| a context file with no fenced block | fails | ✔ |
| a context file that does not link to the bindings | fails | ✔ |
| case graded only by what fired | fails | ✔ |
| case run fewer times than the floor | fails | ✔ |
| the last should-not-fire case removed | fails | ✔ |
| a skill held by no case | fails | ✔ |
| the documented invocation loses its baseline | fails | ✔ |
| a scaffold_script that names no file | fails | ✔ |
| a scaffolded case whose documented invocation never lays the fixture down | fails | ✔ |
| a gated tool a case asks for is never granted | fails | ✔ |
| a case with no row in the table | fails | ✔ |
| a row for a case nobody has | fails | ✔ |
| the runner losing its refusal of an unapproved run | fails | ✔ |
| the runner letting a run below the floor take a measurement's row | fails | ✔ |
| a measurement whose inputs moved on | fails | ✔ |
| a measurement whose rule was reworded | fails | ✔ |
| a case the board has never measured | **warns, does not fail** | ✔ |
| a board entry from fewer runs than the floor | **warns, does not fail** | ✔ |
| an llm grader with an empty rubric | fails | ✔ |
| every case removed | fails | ✔ |
| the fault injection record losing a row | fails | ✔ |
| the record naming a fault nobody injects | fails | ✔ |
| a recorded fault whose expected result was flipped | fails | ✔ |
| the bindings losing a gate verify.py runs | fails | ✔ |
| a changelog heading the reader cannot parse | fails | ✔ |
| a manifest version with no changelog entry | fails | ✔ |
| an id whose since names a release the changelog does not have | fails | ✔ |
| the same id twice in the id table | fails | ✔ |
| a check the tool answers that the id table does not name | fails | ✔ |
| an id in the table no function answers | fails | ✔ |
| a test claiming a rule that does not exist | fails | ✔ |
| a test outside any rule | fails | ✔ |
| a failing test | fails | ✔ |
| a test naming a rule that is still @planned | fails | ✔ |
| shipping change with no release label | fails | ✔ |
| two release labels at once | fails | ✔ |
| pull request body with no changelog section | fails | ✔ |
| changelog section left empty | fails | ✔ |
| a version that already has an entry | fails | ✔ |
| a manifest with no version field | fails | ✔ |
| a version that is not major.minor.patch | fails | ✔ |
| spec-moving change whose body carries no gherkin | fails | ✔ |
| a gherkin block with nothing in it | fails | ✔ |
| a new id row with a typed version | fails | ✔ |
| the audit surface moved with no ## Ids section | fails | ✔ |
| ## Ids reading unchanged while a row was added | fails | ✔ |
| ## Ids naming an id the table does not have | fails | ✔ |
| a row still reading next after the release | fails | ✔ |
| a ledger whose stamp the release cannot find | fails | ✔ |
| a bullet list that retires what the table added | fails | ✔ |
| a broken gate underneath a stale measurement | fails | ✔ |
| a ledger in the shape it had before ids | fails | ✔ |
| a ledger with no stamp line | fails | ✔ |
| a stamp behind the plugin installed | fails | ✔ |
| a stamp ahead of the plugin installed | fails | ✔ |
| a stamp that is not at the plugin installed | fails | ✔ |
| a changelog the tool cannot read | fails | ✔ |
| a row in a state of somebody's own | fails | ✔ |
| an automated row naming no command | fails | ✔ |
| a not-applicable reason the tree contradicts | fails | ✔ |
| a gate with no row | fails | ✔ |
| a recording past its age | fails | ✔ |
| a mocked row two changes old | fails | ✔ |
| no table for the wiring that must never gate | fails | ✔ |
| the second table losing the report's row | fails | ✔ |
| the second table losing the measure's row | fails | ✔ |
| no row saying a sketch is owed | fails | ✔ |
| the sketch row and the picture row saying one thing | fails | ✔ |
| a record instructing by a skill this plugin no longer has | fails | ✔ |
| a row deferred across two changes | fails | ✔ |
| a local hook given a row | fails | ✔ |
| a change outside the record in the working tree | fails | ✔ |
| a record one line short | fails | ✔ |
| a judgment nobody made | fails | ✔ |
| a state of somebody's own | fails | ✔ |
| an open line naming nothing that closes it | fails | ✔ |
| a not-read line with no reason | fails | ✔ |
| a judgment clear with no command beside it | fails | ✔ |
| a fix that strayed into the wiring | fails | ✔ |

## Branch protection

Read back with `gh api repos/o/r/rulesets` on 2026-01-01: a merge is blocked when `checks` fails, and one deploy key can bypass.

## What has no gate, and what that misses

No coverage gate: the fixture has three lines of code, and a threshold over them would measure nothing.

## Notes from the sitting

Nothing runs on one machine that the pipeline does not.
MD

printf '# Spec 0001: the first\n' > specs/changes/0001-first.md
printf '# Spec 0002: the second\n' > specs/changes/0002-second.md

cat > README.md <<'EOF'
# weirhouse

Sluice scheduling and level logging at the weir. Python 3.12; `make check`.
EOF

cat > Makefile <<'EOF'
check:
	pytest -q

dev:
	uvicorn weirhouse.api:app --reload --port 8000
EOF

cat > src/weirhouse/__init__.py <<'EOF'
EOF

cat > src/weirhouse/levels.py <<'EOF'
"""Levels above and below the weir, and whether the sluice should open. Pure."""


def should_open(above_cm: int, below_cm: int, head_limit_cm: int = 90) -> bool:
    return above_cm - below_cm > head_limit_cm
EOF

cat > tests/test_levels.py <<'EOF'
from weirhouse.levels import should_open


def test_a_high_head_opens_the_sluice():
    assert should_open(200, 100)


def test_a_low_head_keeps_it_shut():
    assert not should_open(150, 100)
EOF
