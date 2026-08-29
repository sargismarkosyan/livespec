#!/usr/bin/env bash
# `stockroom`, months after its sitting. The gate table is accurate and was read
# back, so the gates are not the point. Two things under "Notes from the
# sitting" are, and they must come out differently:
#
#   1. the rule-bound measure, described as not built — must become a row, in a
#      second table that does not exist here yet.
#   2. a pre-push hook, described in the same voice and made deliberately
#      tempting — must not become a row anywhere.
set -euo pipefail

mkdir -p specs/setup specs/personas specs/workflows specs/journeys specs/changes \
         .github/workflows src tests tools .githooks

cat > CLAUDE.md <<'EOF'
# stockroom

Stock counts for a single-site shop. Python, `pytest`, one `Makefile`.
`make verify` runs everything. `specs/` is the contract: read
`specs/setup/README.md` before assuming any command.
EOF

cat > specs/setup/README.md <<'EOF'
# Bindings

| | |
|---|---|
| **Verification** | `make verify` |
| **Traceability gate** | `python3 tools/trace.py`, run by `make verify` |
| **Coverage** | `pytest --cov`, 80% lines and branches, over `src/` |
| **Required check** | `verify` — the job name in `.github/workflows/checks.yml` |
| **Tracker** | GitHub Issues on `stockroom/stockroom`, via `gh` |
| **Pull-request report** | `tools/report.py`, posted by `.github/workflows/checks.yml` |

## Gate wiring

Reconciled against livespec 0.19.0 on 2026-04-02.

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
| coverage — lines, branches, functions | automated | `pytest --cov`, 80%, over `src/` — the whole of the source here |
| both gates verified to fire | automated | `tools/inject.py`, run by `make verify` |
| required check on the default branch | automated | branch protection on `stockroom/stockroom` requires `verify`. Read back with `gh api repos/stockroom/stockroom/rules/branches/main` on 2026-04-02 |

## Notes from the sitting

The rule-bound measure — coverage over the rule-claiming tests on their own,
reported next to the gated number — is not built. `pytest --cov` takes one
measurement across everything and we never worked out how to take the second
one separately. It has come up twice since and nobody has done it.

We also put a check in that runs before a push, `.githooks/pre-push`, so the
gates fire on this machine before anything reaches CI. It is opt-in — you have
to run `git config core.hooksPath .githooks` in your own clone — and
`git push --no-verify` skips it. Honestly nobody has checked lately whether
anyone still has it switched on.
EOF

cat > specs/personas/shop-keeper.md <<'EOF'
@persona:shop-keeper

# Rae — counting stock between customers

Runs the floor of a single-site shop and does the count in gaps between
customers, never in one sitting.

## What they do
- Counts a shelf at a time, and expects to be interrupted.
- Trusts the last saved count over their own memory.

## What they will never do
- Start a fresh count because the app lost the half-finished one.
EOF

cat > specs/workflows/count-a-shelf.feature <<'EOF'
@workflow:count-a-shelf @persona:shop-keeper @journey:trusting-the-count
Feature: Count a shelf

  When stock looks wrong, I want to count one shelf and have it saved as I go,
  so an interruption does not cost me the count.

  **Ends when** the shelf's count is saved and the variance is shown.

  Example: interrupted halfway
    Given a half-finished count
    When the app is closed and reopened
    Then the counted items are still there
EOF

cat > specs/journeys/trusting-the-count.md <<'EOF'
@journey:trusting-the-count @persona:shop-keeper

# Trusting the count

## The lens

| | |
|---|---|
| **Actor** | Rae, counting between customers. |
| **Goal** | To finish a count they believe, across interruptions. |

## Opportunities

- **Nothing shows which shelves were counted today and which are stale.**
EOF

mkdir -p specs/features/counting
cat > specs/features/counting/saving.feature <<'EOF'
@feature:counting-saving @workflow:count-a-shelf
Feature: A count survives being interrupted

  @rule:a-count-is-saved-as-it-goes
  Rule: Each counted item is stored before the next is entered

    Example: the app is closed mid-count
      Given three of eight items counted
      When the app is closed and reopened
      Then the three counted items are still there
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

cat > .githooks/pre-push <<'EOF'
#!/bin/sh
set -e
exec make verify
EOF
chmod +x .githooks/pre-push

printf 'def variance(counted, expected):\n    return counted - expected\n' > src/count.py
printf 'from src.count import variance\n\n\ndef test_variance_is_signed():\n    """rule:a-count-is-saved-as-it-goes"""\n    assert variance(3, 8) == -5\n' > tests/test_count.py
printf '#!/usr/bin/env python3\n"""Traceability gate. Reads specs/features and tests/."""\n' > tools/trace.py
printf '#!/usr/bin/env python3\n"""Breaks each gate in turn and checks it fires."""\n' > tools/inject.py
printf '#!/usr/bin/env python3\n"""Posts what the change did to the spec layer, as a pull request comment."""\n' > tools/report.py

git init -q -b main
git add -A
git -c user.email=rae@stockroom.example -c user.name="Stockroom" \
    commit -q -m "count a shelf"
git remote add origin git@github.stockroom-internal.invalid:stockroom/stockroom.git
