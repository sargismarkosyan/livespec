#!/usr/bin/env python3
"""Fail a pull request that ships something without saying how to release it.

`main` is production: the marketplace sources this plugin at `./`, no install or
update command takes a ref, and `/plugin update` compares the `version` string on
the default branch. So a change to a skill merging with the version untouched
reaches **nobody**, silently, with a green build.

`release.py` moves that version on merge, which means nothing here has to be
typed by hand any more. What still cannot be automated is the part only the
author knows: **how big the change is**, and **what to say about it**. This gate
checks that both are present while there is still somebody to ask.

    before            now
    ────────────────  ──────────────────────────────────────
    version unmoved   no release label, or two
    no entry          no `## Changelog` section in the body

Same guarantee — nothing that ships can merge silently — one step earlier.

This is a property of a pull request rather than of a tree, which is why it is
not part of `verify.py`: that command has to mean the same thing on a laptop with
no remote as it does in CI.

Run: python3 .github/scripts/version_gate.py [base-ref]
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from releaselib import ReleaseInputError, extract_entry, select_increment, ships  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
BASE = sys.argv[1] if len(sys.argv) > 1 else "origin/main"


def git(*args: str) -> str:
    result = subprocess.run(["git", *args], capture_output=True, text=True, cwd=ROOT)
    if result.returncode != 0:
        print(f"✘ git {' '.join(args)}: {result.stderr.strip()}", file=sys.stderr)
        sys.exit(1)
    return result.stdout


def pull_request() -> dict | None:
    """The pull request this run is for, from the event payload GitHub writes."""
    path = os.environ.get("GITHUB_EVENT_PATH")
    if not path or not Path(path).exists():
        return None
    payload = json.loads(Path(path).read_text())
    return payload.get("pull_request")


changed = [line for line in git("diff", "--name-only", f"{BASE}...HEAD").splitlines() if line]
shipping = ships(changed)

if not shipping:
    print(f"✔ release inputs: nothing that ships changed against {BASE}")
    raise SystemExit(0)

request = pull_request()
if request is None:
    # Local run, or a push build. There is no pull request to read, and inventing
    # a verdict from its absence would make this command mean two different
    # things depending on where it ran.
    print(
        f"• {len(shipping)} file(s) that ship changed against {BASE}, but there is no\n"
        f"  pull-request payload here, so the release inputs were not checked.\n"
        f"  This gate runs on pull requests in CI; see specs/setup/README.md."
    )
    raise SystemExit(0)

labels = [label.get("name", "") for label in request.get("labels", [])]
problems: list[str] = []

try:
    increment = select_increment(labels)
except ReleaseInputError as error:
    increment = None
    problems.append(str(error))

try:
    entry = extract_entry(request.get("body"))
except ReleaseInputError as error:
    entry = None
    problems.append(str(error))

if problems:
    print(
        f"\n✘ {len(shipping)} file(s) that ship changed, and this pull request "
        f"cannot be released:\n",
        file=sys.stderr,
    )
    for path in shipping[:10]:
        print(f"    {path}", file=sys.stderr)
    if len(shipping) > 10:
        print(f"    … and {len(shipping) - 10} more", file=sys.stderr)
    print(file=sys.stderr)
    for problem in problems:
        print(f"  ✘ {problem}\n", file=sys.stderr)
    print(
        "  Merging is releasing here — `main` is what every install updates from.\n"
        "  These two are the only parts of a release nobody but you can supply.",
        file=sys.stderr,
    )
    raise SystemExit(1)

first = entry.split("\n", 1)[0]
preview = first if len(first) <= 60 else first[:57] + "…"
print(
    f"✔ release inputs: {increment} bump, {len(entry.splitlines())} line(s) of entry "
    f"({preview!r}), for {len(shipping)} shipping file(s)"
)
