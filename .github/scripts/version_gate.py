#!/usr/bin/env python3
"""Fail a pull request that changes what ships without bumping the version.

`version` in plugin.json is the whole distribution mechanism: `/plugin update`
compares that string and keeps the cached copy when it has not moved. So a change
to a skill merging with the version untouched reaches **nobody**, silently, with
a green build. Nothing else in this repository catches that.

This is a property of a pull request rather than of a tree, which is why it is
not part of `verify.py` — that command has to mean the same thing on a laptop
with no remote as it does in CI.

Run: python3 .github/scripts/version_gate.py [base-ref]
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = sys.argv[1] if len(sys.argv) > 1 else "origin/main"

# What a user actually receives. `evals/`, `specs/` and `.github/` ship too, but
# nothing in them changes what an agent does, and demanding a version for a
# typo in a rubric is how a rule gets switched off.
SHIPPING = ("skills/", "method/", "templates/", "tools/", ".claude-plugin/")

MANIFEST = ".claude-plugin/plugin.json"


def git(*args: str) -> str:
    result = subprocess.run(["git", *args], capture_output=True, text=True, cwd=ROOT)
    if result.returncode != 0:
        print(f"✘ git {' '.join(args)}: {result.stderr.strip()}", file=sys.stderr)
        sys.exit(1)
    return result.stdout


changed = [line for line in git("diff", "--name-only", f"{BASE}...HEAD").splitlines() if line]
shipping = [path for path in changed if path.startswith(SHIPPING)]

if not shipping:
    print(f"✔ version gate: nothing that ships changed against {BASE}")
    raise SystemExit(0)

head = json.loads((ROOT / MANIFEST).read_text())["version"]
base = json.loads(git("show", f"{BASE}:{MANIFEST}"))["version"]

if head == base:
    print(
        f"\n✘ {len(shipping)} file(s) that ship changed, but version is still {head}:\n",
        file=sys.stderr,
    )
    for path in shipping[:10]:
        print(f"    {path}", file=sys.stderr)
    if len(shipping) > 10:
        print(f"    … and {len(shipping) - 10} more", file=sys.stderr)
    print(
        f"\n  `/plugin update` compares that string. Merge this and every existing install\n"
        f"  keeps the cached copy — the change reaches nobody, and nothing else says so.\n"
        f"  Bump {MANIFEST} and add the matching CHANGELOG.md entry.",
        file=sys.stderr,
    )
    raise SystemExit(1)

changelog = (ROOT / "CHANGELOG.md").read_text()
if f"## {head}" not in changelog:
    print(
        f"\n✘ version is {head} but CHANGELOG.md has no `## {head}` entry.\n"
        f"  A bump with no entry is the same silence in a different place.",
        file=sys.stderr,
    )
    raise SystemExit(1)

print(f"✔ version gate: {base} → {head}, with a CHANGELOG entry, for {len(shipping)} shipping file(s)")
