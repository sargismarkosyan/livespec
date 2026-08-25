#!/usr/bin/env python3
"""Verification — the one command that means everything passes.

    repository checks      what only this repo knows about itself (checks.py)
    traceability           gate 1: rules <-> eval cases, features -> workflows
    eval suite             gate 2: every skill held, every case able to fail
    gate fault injection   every gate broken on purpose, to prove they fire

CI runs this same command. A longer list in CI than a person can run locally is
how a required check turns into something nobody can reproduce.

It does not run the eval cases themselves: they cost money per session, and
running them is a maintainer step — evals/runner/run.py — never this command's.
specs/setup/README.md says so rather than letting a green run imply otherwise.

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
    ("eval suite", "evalsuite.py"),
    ("gate fault injection", "inject.py"),
]


def main() -> int:
    failed: list[str] = []
    for name, script in GATES:
        # flush: the children write straight to the terminal, so an unflushed
        # header lands after the output it is meant to introduce.
        print(f"\n── {name} " + "─" * (56 - len(name)), flush=True)
        result = subprocess.run([sys.executable, str(SCRIPTS / script)])
        if result.returncode != 0:
            failed.append(name)

    print()
    if failed:
        print(f"✘ verification failed: {', '.join(failed)}", file=sys.stderr)
        return 1
    print(f"✔ verification green — {len(GATES)} gates, all fired against injected faults")
    return 0


if __name__ == "__main__":
    sys.exit(main())
