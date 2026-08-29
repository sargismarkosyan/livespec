#!/usr/bin/env python3
"""Verification — the one command that means everything passes.

    repository checks      what only this repo knows about itself (checks.py)
    traceability           gate 1: rules <-> eval cases, features -> workflows
    eval suite             gate 2: every skill held, every case able to fail
    measurement board      gate 5: no eval number outlives the files it measured
    gate fault injection   every gate broken on purpose, to prove they fire

CI runs this same command. A longer list in CI than a person can run locally is
how a required check turns into something nobody can reproduce.

It does not run the eval cases themselves: they cost money per session, and
running them is a maintainer step — evals/runner/run.py — never this command's.
specs/setup/README.md says so rather than letting a green run imply otherwise.

Exit 0 green, 1 something is broken, 2 nothing is broken and a measurement run
somebody pays for is owed. The third is a state method/repository.md sanctions
committing and pushing, and the reason it has its own status is that a red
indistinguishable from a defect stops being read. See verdict() below.

Run: python3 .github/scripts/verify.py [--local]

`--local` is the free half, for .githooks/pre-push — every gate whose failure a
person can clear on this machine without spending anything. See COSTS_MONEY
below and method/testing.md on why that is the line. CI runs the full list.
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
    ("measurement board", "board.py"),
    ("gate fault injection", "inject.py"),
]

# The one gate here whose failure costs money to clear rather than time. A stale
# board is healed by an eval run, the run is the maintainer's to approve, and the
# gate is correctly red until they do — which is right for CI and wrong for a
# hook, where it would refuse every push over an unpaid bill until somebody
# turned the hook off. Named here rather than in the hook so there is one list.
COSTS_MONEY = {"measurement board"}

# Two kinds of red, and the exit status is where they are told apart. 1 is a
# defect somebody here can fix. 2 is nothing broken and a run somebody pays for
# owed — which run.py already exits 2 to say, from the other side of the same
# sentence, so a reader learns it once. method/graded-cases.md requires the
# distinction to exist and leaves the mechanism here; without one, a red that
# nobody can act on is investigated twice, found innocent twice, and read never
# again.
BROKEN = 1
OWED = 2

OWED_NOTE = """
  Nothing is broken. A number no longer describes the files it measured, and the
  only cure is a run of the eval suite — about $1.80 a case, billed to the
  maintainer's account and drawn down from its session limit.

  Committing and pushing this is sanctioned: method/repository.md, "Commits".
  Say in the commit which measurements are waiting; say in the pull request what
  a run costs and who can approve one. It does not merge until somebody has.

  If you are an agent: this is not your approval to give."""


def verdict(failed: list[str]) -> tuple[int, str]:
    """Which red this is — the exit status, and the line that says why.

    Pure, and separate from main for the reason releaselib.py is a module: a
    decision this consequential has to be breakable without a fixture. The one
    that matters is the mix — a real defect alongside an unpaid bill is a
    defect, because a gate that reports a break as a bill is a gate that has
    learned to hide one.
    """
    if not failed:
        return 0, ""
    broken = [name for name in failed if name not in COSTS_MONEY]
    if broken:
        line = f"✘ verification failed: {', '.join(failed)}"
        owed = [name for name in failed if name in COSTS_MONEY]
        if owed:
            line += (f"\n  ({', '.join(owed)} is red as well and is not the kind "
                     f"anything here clears — fix the rest first)")
        return BROKEN, line
    return OWED, f"✘ verification is waiting on a measurement run: {', '.join(failed)}{OWED_NOTE}"


def main(argv: list[str]) -> int:
    local = "--local" in argv
    gates = [g for g in GATES if not (local and g[0] in COSTS_MONEY)]

    failed: list[str] = []
    for name, script in gates:
        # flush: the children write straight to the terminal, so an unflushed
        # header lands after the output it is meant to introduce.
        print(f"\n── {name} " + "─" * (56 - len(name)), flush=True)
        result = subprocess.run([sys.executable, str(SCRIPTS / script)])
        if result.returncode != 0:
            failed.append(name)

    print()
    if failed:
        code, line = verdict(failed)
        print(line, file=sys.stderr)
        return code
    if local:
        left = ", ".join(sorted(COSTS_MONEY))
        print(f"✔ local checks green — {len(gates)} of {len(GATES)} gates. "
              f"Left to CI: {left} — its only fix is an eval run somebody pays for")
        return 0
    print(f"✔ verification green — {len(GATES)} gates, all fired against injected faults")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
