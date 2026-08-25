#!/usr/bin/env python3
"""Fail a pull request that ships or re-promises something silently.

`main` is production: the marketplace sources this plugin at `./`, no install or
update command takes a ref, and `/plugin update` compares the `version` string on
the default branch. So a change to a skill merging with the version untouched
reaches **nobody**, silently, with a green build.

`release.py` moves that version on merge, which means nothing here has to be
typed by hand any more. What still cannot be automated is the part only the
author knows: **how big the change is**, **what to say about it**, and **what the
promise now says**. This gate checks they are present while there is still
somebody to ask.

    if the change      it must carry
    ─────────────────  ──────────────────────────────────────
    ships              exactly one release label
    ships              a `## Changelog` section in the body
    moves the spec     the Gherkin it moved, quoted or pinned

The triggers are separate. A spec moves without anything shipping far more often
than not, and a wording fix in a skill ships without touching a promise.

Same guarantee — nothing merges silently — one step earlier.

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
from releaselib import (  # noqa: E402
    ReleaseInputError,
    extract_entry,
    extract_gherkin,
    moves_spec,
    select_increment,
    ships,
)

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
moving = moves_spec(changed)

if not shipping and not moving:
    print(f"✔ release inputs: nothing that ships or moves the spec changed against {BASE}")
    raise SystemExit(0)

request = pull_request()
if request is None:
    # Local run, or a push build. There is no pull request to read, and inventing
    # a verdict from its absence would make this command mean two different
    # things depending on where it ran.
    print(
        f"• {len(shipping)} file(s) that ship and {len(moving)} that move the spec "
        f"changed against\n"
        f"  {BASE}, but there is no pull-request payload here, so the body was not\n"
        f"  checked. This gate runs on pull requests in CI; see specs/setup/README.md."
    )
    raise SystemExit(0)

body = request.get("body")
labels = [label.get("name", "") for label in request.get("labels", [])]
problems: list[str] = []
increment = entry = gherkin = None

# The two questions are asked separately because they have different triggers. A
# spec usually moves without anything shipping, and a wording fix in a skill
# ships without moving a promise.
if shipping:
    try:
        increment = select_increment(labels)
    except ReleaseInputError as error:
        problems.append(str(error))
    try:
        entry = extract_entry(body)
    except ReleaseInputError as error:
        problems.append(str(error))

if moving:
    try:
        gherkin = extract_gherkin(body)
    except ReleaseInputError as error:
        problems.append(str(error))

if problems:
    print("\n✘ this pull request cannot merge as it stands:\n", file=sys.stderr)
    for label, paths in (("ship", shipping), ("move the spec", moving)):
        if not paths:
            continue
        print(f"  {len(paths)} file(s) that {label}:", file=sys.stderr)
        for path in paths[:6]:
            print(f"    {path}", file=sys.stderr)
        if len(paths) > 6:
            print(f"    … and {len(paths) - 6} more", file=sys.stderr)
        print(file=sys.stderr)
    for problem in problems:
        print(f"  ✘ {problem}\n", file=sys.stderr)
    print(
        "  Merging is releasing here — `main` is what every install updates from,\n"
        "  and a changed promise nobody can read is a promise nobody reviewed.\n"
        "  These are the parts of a change nobody but you can supply.",
        file=sys.stderr,
    )
    raise SystemExit(1)

said: list[str] = []
if shipping:
    first = entry.split("\n", 1)[0]
    preview = first if len(first) <= 60 else first[:57] + "…"
    said.append(
        f"{increment} bump, {len(entry.splitlines())} line(s) of entry ({preview!r}), "
        f"for {len(shipping)} shipping file(s)"
    )
if moving:
    said.append(f"{len(gherkin.splitlines())} line(s) of Gherkin for {len(moving)} spec file(s)")
print(f"✔ release inputs: {'; '.join(said)}")
