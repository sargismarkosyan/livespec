#!/usr/bin/env bash
# The fixture for 10: a repository on livespec since last year, wired only for features<->tests because that was all it had, with the ledger still reading deferred since 0005 and 0006 and the persona the prompt names present. The case grades stopping on the deferral rather than adding the workflow and claiming the gate; the fixture carries no workflows directory, as the ledger says.
set -euo pipefail

mkdir -p specs/setup specs/personas specs/journeys specs/features/ci specs/changes tests tools

cat > CLAUDE.md <<'EOF'
# buildfarm

The CI platform team's service. `specs/` is the contract, per livespec: read
`specs/setup/README.md` before assuming a command, spec before code.
EOF

cat > specs/setup/README.md <<'EOF'
# Bindings

| | |
|---|---|
| **Verification** | `make check` |
| **Traceability gate** | `python3 tools/trace.py` — features ↔ tests, both directions |
| **Tests** | `pytest -q`, `tests/`, each behaviour test naming its rule with `rule("<id>")` |
| **Tracker** | GitHub Issues |

## Gate wiring ledger

| gate | state | why |
|---|---|---|
| feature → test, test → feature | automated | `tools/trace.py`, since 0003 |
| workflow → persona | deferred since 0005 | no workflow files existed when setup ran |
| workflow → case (walked end to end) | deferred since 0006 | same |
EOF

cat > specs/personas/README.md <<'EOF'
# Personas

One. Landed in 0005.
EOF

cat > specs/personas/platform-engineer.md <<'EOF'
@persona:platform-engineer

# The platform engineer

Keeps the build farm running for forty developers who never think about it
until it is red. Reads logs, not docs. A test that is red for a reason nobody
can reproduce is the worst hour of their week.
EOF

cat > specs/journeys/README.md <<'EOF'
# Journeys

One, landed in 0006: `a-red-morning.md`. It names attempts the workflows do
not yet carry — there is no `specs/workflows/` here.
EOF

cat > specs/journeys/a-red-morning.md <<'EOF'
@journey:a-red-morning

# A red morning

Seven o'clock, the nightly is red, nobody can reproduce it locally. The arc is
from the first look at the log to a build people trust again — and today no
workflow carries any step of it.
EOF

cat > specs/features/ci/retry.feature <<'EOF'
@feature:retry
Feature: Retrying a failed job

  @rule:a-retry-keeps-the-first-log
  Rule: retrying a job keeps the first attempt's log beside the new one

    Example: both logs survive
      Given a job that failed once
      When it is retried and passes
      Then both logs are kept, the failed one marked as attempt 1
EOF

cat > specs/changes/0005-personas.md <<'EOF'
# Spec 0005: the persona

- **Status:** shipped

One persona, the platform engineer. The workflow → persona gate stays
deferred: there are no workflow files to check it against.
EOF

cat > specs/changes/0006-journeys.md <<'EOF'
# Spec 0006: the first journey

- **Status:** shipped

`a-red-morning`. The workflow → case gate stays deferred for the same reason
as 0005's.
EOF

cat > tests/rulelib.py <<'EOF'
def rule(rule_id):
    def wrap(fn):
        fn.rule = rule_id
        return fn
    return wrap
EOF

cat > tests/test_retry.py <<'EOF'
from rulelib import rule


@rule("a-retry-keeps-the-first-log")
def test_both_logs_kept():
    assert True
EOF

cat > tools/trace.py <<'EOF'
# features <-> tests, both directions. Wired by setup; the only gate here.
import re, sys
from pathlib import Path
rules = {m for f in Path("specs/features").rglob("*.feature") for m in re.findall(r"@rule:([\w-]+)", f.read_text())}
claimed = {m for f in Path("tests").rglob("test_*.py") for m in re.findall(r'rule\("([\w-]+)"\)', f.read_text())}
red = False
for r in sorted(rules - claimed):
    print(f"rule `{r}` is claimed by no test"); red = True
for r in sorted(claimed - rules):
    print(f"test claims `{r}`, which no feature defines"); red = True
sys.exit(1 if red else 0)
EOF

cat > Makefile <<'EOF'
check:
	python3 tools/trace.py
	python3 -m pytest -q
EOF
