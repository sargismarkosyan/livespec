#!/usr/bin/env bash
# slipway: the boat-lift schedule for one yard. The process is set up; the
# trees command is written and never proven. Its `new` forgets the hook.
set -euo pipefail

mkdir -p slipway tests scripts tools specs/setup specs/changes

cat > README.md <<'README'
# slipway

The boat-lift schedule for one yard. Python 3.12, standard library.
`make hooks` once per checkout, `make check` for the suite.
README

cat > Makefile <<'MAKEFILE'
check:
	python3 -m unittest discover -s tests -q

hooks:
	python3 tools/gen_hooks.py
	git config core.hooksPath .hooks
MAKEFILE

cat > tools/gen_hooks.py <<'PY'
"""Writes .hooks/pre-push, which runs `make check`. The directory is ignored."""
from pathlib import Path

hooks = Path(".hooks")
hooks.mkdir(exist_ok=True)
hook = hooks / "pre-push"
hook.write_text("#!/bin/sh\nexec make check\n")
hook.chmod(0o755)
PY

cat > .env <<'ENVFILE'
SLIPWAY_YARD=north
ENVFILE

cat > .gitignore <<'IGNORE'
.env
.hooks/
.worktrees/
__pycache__/
IGNORE

cat > slipway/__init__.py <<'PY'
PY

cat > slipway/schedule.py <<'PY'
def next_lift(queue: list[str]) -> str | None:
    return queue[0] if queue else None
PY

cat > tests/test_schedule.py <<'PY'
import unittest

from slipway.schedule import next_lift


class NextLift(unittest.TestCase):
    def test_first_in_queue(self):
        self.assertEqual(next_lift(["Kestrel", "Tern"]), "Kestrel")

    def test_empty_yard(self):
        self.assertIsNone(next_lift([]))
PY

cat > scripts/trees.py <<'PY'
"""slipway's trees: `new <name>`, `list`, `clean`. Every tree lives in .worktrees/."""
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(subprocess.run(["git", "rev-parse", "--path-format=absolute", "--git-common-dir"],
                           capture_output=True, text=True, check=True).stdout.strip()).parent
HOME = ROOT / ".worktrees"


def git(*args, cwd=ROOT):
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)


def new(name):
    path = HOME / name
    result = git("worktree", "add", str(path), "-b", name)
    if result.returncode:
        sys.exit(result.stderr)
    shutil.copy(ROOT / ".env", path / ".env")
    print(f"{path} ready")


def trees():
    out = git("worktree", "list", "--porcelain").stdout.split("\n\n")
    return [block.splitlines()[0].split(" ", 1)[1] for block in out if block.strip()][1:]


def list_():
    for path in trees():
        dirty = git("status", "--porcelain", cwd=path).stdout.strip()
        print(f"{Path(path).name}  {'KEEP  uncommitted files' if dirty else 'safe'}")


def clean():
    for path in trees():
        if git("status", "--porcelain", cwd=path).stdout.strip():
            print(f"kept     {Path(path).name}")
            continue
        git("worktree", "remove", path)
        print(f"removed  {Path(path).name}")


if __name__ == "__main__":
    verb = sys.argv[1] if len(sys.argv) > 1 else ""
    {"new": lambda: new(sys.argv[2]), "list": list_, "clean": clean}.get(verb, lambda: sys.exit(__doc__))()
PY

cat > CLAUDE.md <<'CLAUDEMD'
# slipway

The boat-lift schedule for one yard. `specs/` is the contract: read
[specs/setup/README.md](specs/setup/README.md) before assuming any command.

## The loop

1. The yard reports what it found; `todo` files it.
2. `refine-spec` writes the spec; the owner approves it.
3. Implement, `make check` green, open the pull request.

## Commands

```sh
make check                          # verification
python3 scripts/trees.py new <name> # a tree for the next change; list, clean
```
CLAUDEMD

cat > specs/setup/README.md <<'BINDINGS'
# Bindings

Everything here is true of slipway and nothing else.

## The table

| | |
|---|---|
| **Verification** | `make check` |
| **What it returns** | 0 green, 1 red |
| **Before the push** | `.hooks/pre-push`, written by `make hooks`, which also sets `core.hooksPath` to `.hooks` |
| **Language** | Python 3.12, standard library |
| **Tracker** | GitHub Issues, via `gh issue create` |
| **Where the app runs** | nowhere — it is a library |
| **Trees** | `.worktrees/`, ignored; `python3 scripts/trees.py` with `new`, `list` and `clean` — **unproven**: no throwaway tree has been made with it yet |
| **What trees share** | *own*: nothing yet named. *shared*: `.env`, copied by `new` from the first tree's |
| **A sketch is owed** | by every change spec, before approval |
BINDINGS

cat > specs/changes/0001-the-next-lift.md <<'SPEC'
# Spec 0001: the next lift

- **Status:** shipped
SPEC

python3 tools/gen_hooks.py
git init -q -b main
git config core.hooksPath .hooks
git add -A
git -c user.name=owner -c user.email=owner@slipway.example commit -q -m "slipway, with the process"
