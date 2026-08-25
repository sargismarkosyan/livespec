#!/usr/bin/env python3
"""Perform the release for a merge that has already landed on `main`.

`main` is production. This is the step that used to be typed by hand and, in the
case of the tag, never typed at all: it moves `version` in the plugin manifest
and writes the `CHANGELOG.md` entry, from the label and the body of the pull
request that was just merged.

It only edits files. The workflow verifies the result, commits it, pushes it and
tags it — so a failure here leaves `main` exactly as the merge left it, and the
worst case is a version that is late rather than one that is wrong.

Run: python3 .github/scripts/release.py --pull-request pr.json --sha <merge-sha>
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from releaselib import (  # noqa: E402
    ReleaseInputError,
    bump_manifest,
    extract_entry,
    next_version,
    prepend_entry,
    select_increment,
    ships,
)

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / ".claude-plugin" / "plugin.json"
CHANGELOG = ROOT / "CHANGELOG.md"


def git(*args: str) -> str:
    result = subprocess.run(["git", *args], capture_output=True, text=True, cwd=ROOT)
    if result.returncode != 0:
        raise SystemExit(f"✘ git {' '.join(args)}: {result.stderr.strip()}")
    return result.stdout


def emit(**outputs: str) -> None:
    """Hand the workflow what it needs to commit, tag and announce."""
    path = os.environ.get("GITHUB_OUTPUT")
    if not path:
        return
    with open(path, "a", encoding="utf-8") as handle:
        for key, value in outputs.items():
            if "\n" in value:
                handle.write(f"{key}<<__EOF__\n{value}\n__EOF__\n")
            else:
                handle.write(f"{key}={value}\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pull-request", required=True, help="JSON for the merged pull request")
    parser.add_argument("--sha", required=True, help="the merge commit on main")
    args = parser.parse_args()

    request = json.loads(Path(args.pull_request).read_text())

    changed = [line for line in git("diff", "--name-only", f"{args.sha}^", args.sha).splitlines() if line]
    shipping = ships(changed)
    if not shipping:
        print(f"• nothing that ships changed in {args.sha[:8]} — no release")
        emit(released="false")
        return 0

    labels = [label.get("name", "") for label in request.get("labels", [])]
    try:
        increment = select_increment(labels)
        entry = extract_entry(request.get("body"))
    except ReleaseInputError as error:
        # version_gate.py should have stopped this before the merge. Reaching here
        # means it was merged past the gate, and releasing something nobody named
        # is worse than a red build on main.
        print(f"\n✘ merged pull request #{request.get('number')} cannot be released:\n", file=sys.stderr)
        print(f"  ✘ {error}\n", file=sys.stderr)
        return 1

    current = json.loads(MANIFEST.read_text())["version"]
    version = next_version(current, increment)
    date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    MANIFEST.write_text(bump_manifest(MANIFEST.read_text(), version))
    CHANGELOG.write_text(prepend_entry(CHANGELOG.read_text(), version, date, entry))

    print(f"✔ release {current} → {version} ({increment}) for {len(shipping)} shipping file(s)")
    for path in shipping[:10]:
        print(f"    {path}")
    if len(shipping) > 10:
        print(f"    … and {len(shipping) - 10} more")

    emit(
        released="true",
        version=version,
        tag=f"livespec--v{version}",
        number=str(request.get("number", "")),
        entry=entry,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
