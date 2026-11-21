#!/usr/bin/env python3
"""Verification — the one command that means everything passes.

    repository checks      what only this repo knows about itself (checks.py)
    traceability           gate 1: rules <-> eval cases, features -> workflows
    unit tests             the code under tools/ and the gates, each test naming its rule
    eval suite             gate 2: every skill held, every case able to fail
    gate fault injection   every gate broken on purpose, to prove they fire

CI, the pre-push hook and a person all run this same command. A longer list in
CI than a person can run locally is how a required check turns into something
nobody can reproduce.

It does not run the eval cases, and it does not ask for their measurements to
be fresh: a run costs money, and it happens when the maintainer chooses —
evals/runner/tiers.py and run.py. board.py reports what is stale; nothing here
waits on it. See specs/changes/0087.

Exit 0 green, 1 something is broken.

Run: python3 .github/scripts/verify.py
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent

# Output is not swallowed: the traceability matrix and the map are worth reading
# on a green run, and a gate whose output nobody ever sees is one nobody checks.
GATES = [
    ("repository checks", "checks.py"),
    ("traceability", "trace.py"),
    ("unit tests", "tests.py"),
    ("eval suite", "evalsuite.py"),
    ("gate fault injection", "inject.py"),
]


def main() -> int:
    failed: list[str] = []
    for name, script in GATES:
        # flush: the children write straight to the terminal, so an unflushed
        # header lands after the output it is meant to introduce.
        print(f"\n── {name} " + "─" * (56 - len(name)), flush=True)
        if subprocess.run([sys.executable, str(SCRIPTS / script)]).returncode != 0:
            failed.append(name)

    print()
    if failed:
        print(f"✘ verification failed: {', '.join(failed)}", file=sys.stderr)
        return 1
    print(f"✔ verification green — {len(GATES)} gates, all fired against injected faults")
    return 0


if __name__ == "__main__":
    sys.exit(main())
