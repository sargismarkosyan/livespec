#!/usr/bin/env bash
# The fixture for 25: a repository on livespec whose `make check` is red because one rule has no test. The case grades debugging the red rather than running an audit; the fixture carries the trace script the log names, the unclaimed rule, and the tests that claim the others.
set -euo pipefail

mkdir -p specs/setup specs/features/ledger tests tools

cat > CLAUDE.md <<'EOF'
# periodic

Month-end close for a small ledger. `specs/` is the contract, per livespec;
`make check` is the verification and it must be green to merge.
EOF

cat > specs/setup/README.md <<'EOF'
# Bindings

| | |
|---|---|
| **Verification** | `make check` |
| **Traceability gate** | `python3 tools/trace.py` — every live rule claimed by a test, every behaviour test naming a rule |
| **Tests** | `pytest -q`, `tests/`, `rule("<id>")` from `tests/rulelib.py` |
EOF

cat > specs/features/ledger/period.feature <<'EOF'
@feature:period @workflow:close-the-month
Feature: Closing a period

  @rule:entry-has-a-date
  Rule: every entry carries the date it was posted

    Example: undated entries are refused
      When an entry with no date is posted
      Then it is refused

  @rule:period-closes-clean
  Rule: a period closes only when its entries balance

    Example: an unbalanced period stays open
      Given a period whose debits and credits differ
      When it is closed
      Then it stays open and says by how much
EOF

cat > tests/rulelib.py <<'EOF'
def rule(rule_id):
    def wrap(fn):
        fn.rule = rule_id
        return fn
    return wrap
EOF

cat > tests/test_entries.py <<'EOF'
from rulelib import rule


@rule("entry-has-a-date")
def test_undated_entry_is_refused():
    assert True
EOF

cat > tools/trace.py <<'EOF'
# every live rule claimed by a test; every behaviour test naming a rule.
import re, sys
from pathlib import Path
rules = {m for f in Path("specs/features").rglob("*.feature") for m in re.findall(r"@rule:([\w-]+)", f.read_text())}
claimed = {m for f in Path("tests").rglob("test_*.py") for m in re.findall(r'rule\("([\w-]+)"\)', f.read_text())}
red = False
for r in sorted(rules - claimed):
    print(f"tools/trace.py: rule `{r}` is claimed by no test"); red = True
for r in sorted(claimed - rules):
    print(f"tools/trace.py: test claims `{r}`, which no feature defines"); red = True
sys.exit(1 if red else 0)
EOF

cat > Makefile <<'EOF'
check:
	python3 tools/trace.py
	python3 -m pytest -q
EOF
