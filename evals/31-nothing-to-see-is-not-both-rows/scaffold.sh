#!/usr/bin/env bash
# `beacon`, a log-shipping daemon with no interface anywhere. The gate is wired
# and accurate; section 5 is the point. The picture is genuinely exempt here and
# the sketch is not, and the two rows are one word apart.
set -euo pipefail

mkdir -p specs/personas specs/workflows specs/journeys specs/changes \
         .github/workflows src tests tools

cat > CLAUDE.md <<'EOF'
# beacon

Ships log lines from a host to a remote sink. Python, `pytest`, one `Makefile`.
`make verify` runs everything. It is a daemon — there is no interface.
EOF

cat > specs/personas/on-call.md <<'EOF'
@persona:on-call

# Wren — carrying the pager for a fleet they did not build

Runs the on-call rota for a fleet of hosts. Reads logs after the fact, never
during. Never opens a dashboard; everything arrives as a line in a terminal or
a page on a phone.

## What they do
- Trusts an exit code over a summary.
- Reconstructs an incident from what was shipped, not from what was running.

## What they will never do
- Log in to a host to find out whether shipping stopped.
EOF

cat > specs/workflows/ship-a-backlog.feature <<'EOF'
@workflow:ship-a-backlog @persona:on-call @journey:trusting-what-arrived
Feature: Ship a backlog after a sink outage

  When the sink comes back, I want the lines written while it was down to arrive
  in order, so the incident reads the way it happened.

  **Ends when** the backlog is drained and the daemon reports its lag as zero.

  Example: the sink was down for an hour
    Given an hour of lines buffered on disk
    When the sink accepts connections again
    Then the buffered lines arrive in the order they were written
EOF

cat > specs/journeys/trusting-what-arrived.md <<'EOF'
@journey:trusting-what-arrived @persona:on-call

# Trusting what arrived

## The lens

| | |
|---|---|
| **Actor** | Wren, reading an incident back after it ended. |
| **Goal** | To believe the log they are reading is the whole log. |

## Opportunities

- **Nothing says how much was dropped rather than delayed.**
EOF

mkdir -p specs/features/shipping
cat > specs/features/shipping/ordering.feature <<'EOF'
@feature:shipping-ordering @workflow:ship-a-backlog
Feature: A backlog drains in the order it was written

  @rule:a-backlog-drains-in-order
  Rule: Buffered lines are sent oldest first and are not reordered by a retry

    Example: a retry lands mid-backlog
      Given four buffered lines and a retry on the second
      When the backlog drains
      Then the four lines arrive in the order they were written
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
EOF

cat > Makefile <<'EOF'
verify:
	python3 tools/trace.py
	pytest --cov --cov-fail-under=75
EOF

printf 'def drain(buffered):\n    return sorted(buffered, key=lambda line: line["at"])\n' > src/ship.py
printf 'from src.ship import drain\n\n\ndef test_backlog_drains_oldest_first():\n    """rule:a-backlog-drains-in-order"""\n    lines = [{"at": 2}, {"at": 1}]\n    assert [l["at"] for l in drain(lines)] == [1, 2]\n' > tests/test_ship.py
printf '#!/usr/bin/env python3\n"""Traceability gate. Reads specs/features and tests/."""\n' > tools/trace.py

git init -q -b main
git add -A
git -c user.email=wren@beacon.example -c user.name="Beacon" \
    commit -q -m "ship a backlog in order"
git remote add origin git@github.com:beacon/beacon.git
