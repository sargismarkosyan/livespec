#!/usr/bin/env bash
# The same repository as 17, months later. The sitting is long over, the
# process is in use, and the ledger it left behind has never been read again.
# Three things in it are wrong in three different ways:
#
#   1. the required-check row asserts branch protection that nothing in this
#      tree can confirm — and the session has no Bash and no network, so it
#      cannot confirm it either. What it does about that is the point.
#   2. the coverage row is true of the Python half and silent about `web/`,
#      which has tests, no coverage, and is not in `make check` at all.
#   3. the rule-bound split and the report are described in prose. Neither is
#      a row, so neither is on any clock, and nothing has asked since.
set -euo pipefail

mkdir -p specs/setup specs/personas specs/workflows specs/journeys specs/changes \
         .github/workflows src tests web/src web/tests tools

cat > CLAUDE.md <<'EOF'
# ledgerline

Invoice reconciliation for a two-person finance team. Python behind, a small
TypeScript front end in `web/`. `make check` runs everything. `specs/` is the
contract: read `specs/setup/README.md` before assuming any command.
EOF

cat > specs/setup/README.md <<'EOF'
# Bindings

| | |
|---|---|
| **Verification** | `make check` |
| **Traceability gate** | `python3 tools/trace.py`, run by `make check` |
| **Coverage** | `pytest --cov`, 85% lines and branches |
| **Required check** | `verify` — the job name in `.github/workflows/checks.yml` |
| **Tracker** | GitHub Issues on `ledgerline/ledgerline`, via `gh` |
| **Pull-request report** | `tools/report.py`, posted by `.github/workflows/checks.yml` |
| **What a pull request carries** | the changed Gherkin, and a screenshot when the UI moved |

## The gate wiring ledger

Reconciled against livespec 0.14.1 on 2026-02-11.

| Gate | State | Wired by |
|---|---|---|
| rule → test | **automated** | `python3 tools/trace.py` |
| test → rule | **automated** | `python3 tools/trace.py` |
| feature → workflow, workflow → persona, journey → workflow | **automated** | `python3 tools/trace.py` |
| coverage — lines, branches, functions | **automated** | `pytest --cov`, thresholds above |
| required check on the default branch | **automated** | branch protection on `ledgerline/ledgerline` requires `verify` |
| both gates verified to fire | **automated** | `tools/inject.py`, run by `make check` |

## Notes from the sitting

The rule-bound coverage split — coverage over the rule-claiming tests on their
own, reported next to the gated number — is not built yet. `pytest --cov` takes
one measurement over everything and we have not worked out how to take the
second one.

The pull-request report is wired. Nobody has actually seen one appear on a pull
request yet, and there was some question at the time about whether the token it
posts with exists on this repository; we did not chase it down.
EOF

cat > specs/personas/ap-clerk.md <<'EOF'
@persona:ap-clerk

# Dani — reconciling invoices nobody else looks at

Runs accounts payable for a two-person team. Reconciles a few dozen invoices a
week against bank lines, and is the only person who would notice a mismatch.

## What they do
- Works from the bank export, never the invoice list.
- Leaves a mismatch open rather than guessing at it.

## What they will never do
- Close a period with an unexplained difference in it.
EOF

cat > specs/workflows/reconcile-a-period.feature <<'EOF'
@workflow:reconcile-a-period @persona:ap-clerk @journey:closing-the-month
Feature: Reconcile a period

  When the bank export for a period arrives, I want every line matched to an
  invoice or explained, so the period can close without an open difference.

  **Ends when** every line in the period is matched or explained.

  Example: a line with no invoice behind it
    Given a bank line that matches no invoice
    When the period is reconciled
    Then the line is listed as unexplained rather than silently dropped
EOF

cat > specs/journeys/closing-the-month.md <<'EOF'
@journey:closing-the-month @persona:ap-clerk

# Closing the month

## The lens

| | |
|---|---|
| **Actor** | Dani, reconciling a period nobody else checks. |
| **Goal** | To close a period knowing nothing was quietly dropped. |

## Opportunities

- **Nothing says which differences were explained and which were ignored.**
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
      - run: make check
      - run: python3 tools/report.py
        continue-on-error: true
EOF

cat > Makefile <<'EOF'
check:
	python3 tools/trace.py
	python3 tools/inject.py
	pytest --cov --cov-fail-under=85
EOF

printf 'def reconcile(lines, invoices):\n    return [l for l in lines if l not in invoices]\n' > src/reconcile.py
printf 'from src.reconcile import reconcile\n\n\ndef test_unmatched_lines_survive():\n    assert reconcile([1], []) == [1]\n' > tests/test_reconcile.py
printf 'export const unmatched = (lines: number[], invoices: number[]) =>\n  lines.filter((l) => !invoices.includes(l));\n' > web/src/unmatched.ts
printf "import { unmatched } from '../src/unmatched';\n\ntest('unmatched lines survive', () => {\n  expect(unmatched([1], [])).toEqual([1]);\n});\n" > web/tests/unmatched.test.ts
printf '{\n  "name": "ledgerline-web",\n  "scripts": { "test": "jest" }\n}\n' > web/package.json
printf '#!/usr/bin/env python3\n"""Traceability gate. Reads specs/features and tests/."""\n' > tools/trace.py
printf '#!/usr/bin/env python3\n"""Breaks each gate in turn and checks it fires."""\n' > tools/inject.py
printf '#!/usr/bin/env python3\n"""Posts what the change did to the spec layer, as a pull request comment."""\n' > tools/report.py

git init -q -b main
git add -A
git -c user.email=ap@ledgerline.example -c user.name="Ledgerline" \
    commit -q -m "reconcile a period"
git remote add origin git@github.ledgerline-internal.invalid:ledgerline/ledgerline.git
