#!/usr/bin/env bash
# The fixture for 12: a small Python service with a year-old CLAUDE.md that says what it does, how to run the tests and the branch naming, a CONTRIBUTING.md whose one line near the bottom says issues live on a self-hosted GitLab, a real test suite and a GitLab CI file. No specs/ and no bindings: setup writes those, and the case grades what it writes.
set -euo pipefail

mkdir -p src/ledger tests

cat > CLAUDE.md <<'EOF'
# ledger-api

<!-- written 2025-09, last touched then -->

Double-entry ledger service behind the finance dashboard. Python 3.12,
FastAPI, Postgres.

## Running the tests locally

    make test        # python -m pytest -q, needs no database
    make test-db     # the integration suite; needs DATABASE_URL

## Branches

Branch names are `feat/<ticket>-<slug>`, `fix/<ticket>-<slug>` or
`chore/<slug>`; the ticket is the GitLab issue number.
EOF

cat > CONTRIBUTING.md <<'EOF'
# Contributing

Open a merge request against `main`. Keep it small. Run `make test` first.

Every change needs a reviewer from the finance-platform group. Squash on merge.

Formatting is `ruff format`; CI fails on anything it would change.

Issues and merge requests live on our self-hosted GitLab at gitlab.internal.example, not on GitHub.
EOF

cat > .gitlab-ci.yml <<'EOF'
stages: [test]
unit:
  stage: test
  image: python:3.12
  script:
    - pip install -e . pytest
    - python -m pytest -q
EOF

cat > pyproject.toml <<'EOF'
[project]
name = "ledger-api"
version = "0.14.0"
requires-python = ">=3.12"
dependencies = ["fastapi"]
EOF

cat > Makefile <<'EOF'
test:
	python -m pytest -q
test-db:
	python -m pytest -q -m db
EOF

: > src/ledger/__init__.py

cat > src/ledger/entries.py <<'EOF'
from dataclasses import dataclass


@dataclass(frozen=True)
class Entry:
    account: str
    debit: int = 0
    credit: int = 0


def balanced(entries: list[Entry]) -> bool:
    return sum(e.debit for e in entries) == sum(e.credit for e in entries)


def post(entries: list[Entry]) -> list[Entry]:
    if not balanced(entries):
        raise ValueError("a posting must balance")
    return list(entries)
EOF

cat > tests/test_entries.py <<'EOF'
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import pytest
from ledger.entries import Entry, balanced, post


def test_balanced_posting_is_kept():
    assert post([Entry("cash", debit=5), Entry("sales", credit=5)])


def test_unbalanced_posting_is_refused():
    with pytest.raises(ValueError):
        post([Entry("cash", debit=5)])


def test_empty_posting_balances():
    assert balanced([])
EOF

# A repository, not a directory: setup's hook question and its branch reading
# need one, and the fourth run's sessions ended on "there's no git repo" (0058).
unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE
git init -q
git -c user.name=ledger -c user.email=ledger@example.invalid add -A
git -c user.name=ledger -c user.email=ledger@example.invalid commit -q -m "ledger-api as it stands"
