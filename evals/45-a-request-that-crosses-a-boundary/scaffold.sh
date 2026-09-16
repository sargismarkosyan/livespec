#!/usr/bin/env bash
# tideboard: a wall board showing one harbour's latest tide readings, pulled
# from a gauge service over the network. A young but real specs/ tree, with a
# boundaries table naming the gauge service as boundary:network, so the with-arm
# has a boundary to place the request against. src/ is present so the
# no-source-edits grader is armed.
set -euo pipefail

mkdir -p specs/personas specs/workflows specs/features/board specs/changes specs/setup src

cat > CLAUDE.md <<'EOF'
# tideboard

A wall board showing one harbour's latest tide readings, pulled from the gauge
service. `specs/` is the contract: read `specs/setup/README.md` before assuming
a command, and spec before code — a change starts in `specs/changes/`, never in
`src/`.
EOF

cat > specs/setup/README.md <<'EOF'
# Bindings

| | |
|---|---|
| **Where the app runs** | `npm run dev`, then the board on the wall screen |
| **Traceability check** | `npm run trace` |
| **Tracker** | none — requests arrive in conversation and become change specs |
| **Change specs** | `specs/changes/NNNN-<slug>.md`, numbered one past the highest |

## The boundaries

One row per thing the board talks to that is not its own code.

| id | boundary | state | since | evidence |
|---|---|---|---|---|
| `boundary:network` | the gauge service | real | 0001 | `fetch` against the harbour gauge API; a recorded set of replies stands in for the behaviour tests. Leaves uncovered: the service slow rather than down |
| `boundary:clock` | the clock | mocked | 0001 | a fixed clock in the tests; cover: none |
EOF

cat > specs/spec.md <<'EOF'
# tideboard

One harbour's tide readings, on a wall screen. A **reading** is a height and a
time from the gauge service. The **board** shows the latest reading and the
next high water. Nothing is stored; the board holds what it last fetched.
EOF

cat > specs/personas/harbourmaster.md <<'EOF'
@persona:harbourmaster

# The harbourmaster — watches the board on the wall

Watches the board across the room while working. Never touches it for minutes
at a time. Needs to trust that what is on it is current, or to be told when it
is not — a stale reading shown as current is worse than a blank.
EOF

cat > specs/workflows/watch-the-board.feature <<'EOF'
@workflow:watch-the-board @persona:harbourmaster
Feature: Watch the board through the day

  Example: the reading updates
    Given the board on the wall
    When a new reading arrives from the gauge service
    Then the board shows it and the time it was taken
EOF

cat > specs/README.md <<'EOF'
# The spec layer

- personas/ — who it is for
- workflows/ — the bounded attempts
- features/ — the enforced rules
- changes/ — one numbered change spec per version
- setup/ — the bindings
EOF

cat > src/board.js <<'EOF'
// The board. Renders the latest reading; a fetch of the gauge service is wired
// elsewhere. Pure rendering here.
export function render(reading) {
  if (!reading) return "No reading yet";
  return `${reading.height_m} m at ${reading.at}`;
}
EOF

cat > package.json <<'EOF'
{
  "name": "tideboard",
  "private": true,
  "scripts": {
    "dev": "vite",
    "trace": "node tools/trace.mjs"
  }
}
EOF
