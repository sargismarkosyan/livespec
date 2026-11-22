#!/usr/bin/env python3
"""The hint: one line saying a livespec upgrade is waiting here, or nothing.

    python3 <plugin root>/tools/behind.py --root <repository> [--host pi|claude]
    python3 <plugin root>/tools/behind.py --fetch-latest   # the newest release, cached a day

Printed for the person — Pi shows it in the footer, which never reaches the
model. First match wins: this session's plugin is older than the ledger; items
are pending; a newer release exists. Silent where there are no bindings, where
LIVESPEC_NO_HINT is set, and on any failure: a hint never stands in the way.
Reads files only; runs git only for --fetch-latest, outside the repository.
See specs/changes/0108.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

PLUGIN = Path(__file__).resolve().parents[1]
CACHE = Path(os.environ.get("XDG_CACHE_HOME") or Path.home() / ".cache") / "livespec" / "latest.json"


def loaded() -> str:
    return json.loads((PLUGIN / ".claude-plugin" / "plugin.json").read_text())["version"]


def latest() -> str | None:
    try:
        data = json.loads(CACHE.read_text())
        return data["latest"] if time.time() - data["at"] < 86400 else None
    except (OSError, ValueError, KeyError):
        return None


def fetch_latest() -> None:
    if os.environ.get("LIVESPEC_NO_HINT") or latest():
        return
    repository = json.loads((PLUGIN / ".claude-plugin" / "plugin.json").read_text())["repository"]
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    out = subprocess.run(["git", "-c", "credential.helper=", "ls-remote", "--tags", repository, "livespec--v*"],
                         cwd=CACHE.parent, capture_output=True, text=True, timeout=3,
                         env={**os.environ, "GIT_TERMINAL_PROMPT": "0"}).stdout
    versions = re.findall(r"refs/tags/livespec--v(\d+\.\d+\.\d+)$", out, re.M)
    if versions:
        newest = max(versions, key=lambda v: tuple(int(p) for p in v.split(".")))
        CACHE.write_text(json.dumps({"latest": newest, "at": time.time()}))


def hint(root: Path, host: str) -> str:
    sys.path.insert(0, str(PLUGIN / "tools"))
    import doctor
    bindings = root / "specs" / "setup" / "README.md"
    if not bindings.is_file():
        return ""
    ctx = doctor.context(root, bindings, git_reads=False)
    here, top = loaded(), doctor.ceiling(ctx)
    command = "/skill:setup" if host == "pi" else "/livespec:setup"
    if top and doctor.later(top, here):
        pinned = doctor.project_pin(root)
        step = ("move the Pi pin, then pi update and restart" if pinned else "pi update, then restart") if host == "pi" else "update the plugin"
        return f"livespec: this session loads {here}; this repository is at {top} — {step}"
    pending = len(doctor.planned(ctx))
    if pending:
        return f"livespec {ctx['stamp'] or '?'} → {here} · {pending} pending · {command} brings it up to date"
    newest = latest()
    if newest and doctor.later(newest, here):
        step = ("move the Pi pin, then pi update" if doctor.project_pin(root) else "pi update") if host == "pi" else "/plugin update livespec"
        return f"livespec {newest} released (loaded {here}) · {step}"
    return ""


def main(argv: list[str]) -> int:
    try:
        if os.environ.get("LIVESPEC_NO_HINT"):
            return 0
        if "--fetch-latest" in argv:
            fetch_latest()
            return 0
        root = Path(argv[argv.index("--root") + 1]) if "--root" in argv else Path.cwd()
        host = argv[argv.index("--host") + 1] if "--host" in argv else "claude"
        line = hint(root.resolve(), host)
        if line:
            print(line)
    except Exception:
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
