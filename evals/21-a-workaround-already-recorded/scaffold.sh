#!/usr/bin/env bash
# The fixture for 21: a repository that adopted the process and diverged from it
# once, on purpose, and wrote that down.
#
# `specs/setup/README.md` is real and complete enough to act on — a verification
# command, a tracker row naming a corporate GitLab reached through `glab`, a gate
# wiring ledger, and a **workarounds** table with one row. That row is the point:
# issues here are filed by hand through the web UI because `feedback` once
# assumed GitHub, filed upstream as livespec#10, and the row names what would end
# it. livespec#10 shipped seven versions ago and nothing here knows.
#
# The app is a CLI, deliberately: `record-clip` films a browser, and there is no
# browser to film, which is the second mismatch the prompt reports.
set -euo pipefail

mkdir -p specs/setup src

cat > CLAUDE.md <<'EOF'
# sift

Filters a structured log down to what you are actually looking for. A CLI —
`python3 src/sift.py --help`. `specs/` is the contract: spec before code, and
`specs/setup/README.md` is where anything about *this* repository lives.
EOF

cat > Makefile <<'EOF'
check:
	python3 -m pytest -q

.PHONY: check
EOF

cat > specs/spec.md <<'EOF'
# sift

A **log** is a list of **entries**, each with a `level`, a `service` and a
`message`. A **filter** narrows the log by level or by service, and a **run**
is one invocation of the CLI over one log file.

What it is not: a log shipper, a storage engine, or anything that watches a file
for changes. It reads what you point it at and prints what matched.
EOF

cat > specs/setup/README.md <<'EOF'
# The bindings

Everything here is true of **this repository** and nothing else. Every skill
reads this file before it assumes a command.

## The table

| | |
|---|---|
| **Verification** | `make check` |
| **Language** | Python 3.12 |
| **Tracker** | the group GitLab at `gitlab.internal.example`, project `platform/sift`, via `glab` |
| **Where the app runs** | `python3 src/sift.py <logfile>` — a CLI, no browser |
| **Deliverable of a version** | the merge request description, with a terminal recording linked from it |

## Gate wiring

Reconciled against livespec 0.11.0 on 2026-06-02.

| Gate | State | Wired by, or why not |
|---|---|---|
| rule → test | automated | `make check` |
| test → rule | automated | `make check` |
| feature → workflow | deferred | since 0004 — the workflow layer is one attempt short |
| coverage | not applicable | measured, never gated; the team reads the number |

## Workarounds

What this repository does its own way because the process did not fit, and the
thing whose arrival would let us stop. A row comes out when the workaround does.

| Recorded | What we do here instead | The gap it goes around | Filed | What would end it |
|---|---|---|---|---|
| 2026-06-02 | Issues are opened by hand in the GitLab web UI and the number pasted back; the plugin's filing step is not used | `feedback` assumed GitHub and `gh`, which cannot reach `gitlab.internal.example` | [livespec#10](https://github.com/sargismarkosyan/livespec/issues/10) | that issue shipping — `feedback` reading the tracker out of these bindings instead of assuming one |
EOF

cat > src/sift.py <<'EOF'
"""sift — narrow a structured log down to what you were looking for."""

import argparse
import json
import sys

LEVELS = ("debug", "info", "warn", "error")


def load(path):
    with open(path) as handle:
        return [json.loads(line) for line in handle if line.strip()]


def matching(entries, level=None, service=None):
    for entry in entries:
        if level and entry.get("level") != level:
            continue
        if service and entry.get("service") != service:
            continue
        yield entry


def main(argv=None):
    parser = argparse.ArgumentParser(prog="sift")
    parser.add_argument("logfile")
    parser.add_argument("--level", choices=LEVELS)
    parser.add_argument("--service")
    args = parser.parse_args(argv)

    for entry in matching(load(args.logfile), args.level, args.service):
        print(f"{entry['level']:>5}  {entry['service']:<12} {entry['message']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
EOF

git init -q -b main
git add -A
git -c user.email=teodora@internal.example -c user.name="Teodora Vasile" \
    commit -q -m "sift reads a log and prints what matched"
git remote add origin git@gitlab.internal.example:platform/sift.git
