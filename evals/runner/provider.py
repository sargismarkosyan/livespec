#!/usr/bin/env python3
"""The session end of the runner: one arm of one case, in a fresh directory.

promptfoo calls `call_api` once per case x arm x repeat. Each call runs the
case's prompt through `claude -p` — with the plugin loaded or without, which is
the whole ablation — in a working directory of its own, keeps the stream
transcript, and hands the final text back as the output the graders judge.
Everything an assert needs beyond that text (the transcript, the tool calls,
the files the session wrote) travels in `metadata`.

When the run passes a `scaffold` var, that script lays the case's fixture down
in the fresh workspace first — both arms alike, because an arm handed a
different repository would make delta a comparison of two different questions.
The `files` a grader sees are then what the session wrote or changed, never
what the scaffold laid down: a fixture with a `src/` tree must arm a
no-source-edits grader, not trip it in both arms.

Not run directly: `run.py` generates the config that names this file.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path


def _snapshot(workspace: Path) -> dict[str, str]:
    """Path → content hash of everything currently in the workspace."""
    return {
        str(p.relative_to(workspace)): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in workspace.rglob("*")
        if p.is_file()
    }


def _read_stream(raw: str) -> tuple[str, list[dict]]:
    """Final result text and every tool_use from a stream-json transcript."""
    result = ""
    tools: list[dict] = []
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") == "result":
            result = event.get("result") or ""
        elif event.get("type") == "assistant":
            for block in (event.get("message") or {}).get("content") or []:
                if isinstance(block, dict) and block.get("type") == "tool_use":
                    tools.append({
                        "name": block.get("name", ""),
                        "input": json.dumps(block.get("input", {}), sort_keys=True),
                    })
    return result, tools


def _cost(raw: str) -> float:
    for line in raw.splitlines():
        if '"total_cost_usd"' in line:
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if event.get("type") == "result":
                return float(event.get("total_cost_usd") or 0)
    return 0.0


def call_api(prompt, options, context):
    config = (options or {}).get("config") or {}
    vars_ = (context or {}).get("vars") or {}
    root = os.environ["LIVESPEC_ROOT"]
    run_dir = Path(os.environ["LIVESPEC_RUN_DIR"])

    with_plugin = bool(config.get("with_plugin"))
    arm = "with" if with_plugin else "without"
    case = str(vars_.get("case") or "case")
    sessions = run_dir / "sessions"
    sessions.mkdir(parents=True, exist_ok=True)
    session_dir = Path(tempfile.mkdtemp(prefix=f"{case}-{arm}-", dir=sessions))
    # The working directory lives in system tmp, never under the repository —
    # a session run inside the repo walks up, loads livespec's own CLAUDE.md,
    # and both arms stop being what they claim to be. Moved under the session
    # directory afterwards so a run leaves everything inspectable in one place.
    workspace = Path(tempfile.mkdtemp(prefix=f"livespec-eval-{case}-{arm}-"))

    laid_down: dict[str, str] = {}
    scaffold = str(vars_.get("scaffold") or "")
    if scaffold:
        build = subprocess.run(["bash", scaffold], cwd=workspace, capture_output=True, text=True, timeout=120)
        if build.returncode != 0:
            (session_dir / "scaffold.log").write_text(build.stdout + build.stderr)
            shutil.move(str(workspace), str(session_dir / "workspace"))
            return {"error": f"scaffold exited {build.returncode} — nothing was measured; log in {session_dir}"}
        laid_down = _snapshot(workspace)

    # Hermetic: no user settings, no MCP servers, and the gated tools the case
    # was not granted are disallowed outright — otherwise a session inherits
    # whatever this machine's global allowlist and MCP config happen to hold,
    # and a grader passes or fails on the operator's dotfiles.
    command = [
        "claude", "-p", "--verbose",
        "--output-format", "stream-json",
        "--no-session-persistence",
        "--setting-sources", "project",
        "--strict-mcp-config",
        "--max-turns", str(vars_.get("max_turns") or 25),
    ]
    disallowed = [t for t in str(vars_.get("disallowed_tools") or "").split() if t]
    if disallowed:
        command += ["--disallowedTools", ",".join(disallowed)]
    if with_plugin:
        command += ["--plugin-dir", root]
    model = os.environ.get("LIVESPEC_SESSION_MODEL", "")
    if model:
        command += ["--model", model]
    allowed = [t for t in str(vars_.get("allowed_tools") or "").split() if t]
    if allowed:
        # one comma-joined argument: --allowedTools is variadic and would
        # otherwise swallow everything after it
        command += ["--allowedTools", ",".join(allowed)]

    timeout = int(vars_.get("timeout_seconds") or 600)
    try:
        proc = subprocess.run(command, input=prompt, cwd=workspace, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired as err:
        (session_dir / "transcript.jsonl").write_text(str(err.stdout or ""))
        shutil.move(str(workspace), str(session_dir / "workspace"))
        return {"error": f"session timed out after {timeout}s — transcript in {session_dir}"}

    (session_dir / "transcript.jsonl").write_text(proc.stdout)
    if proc.returncode != 0:
        tail = proc.stderr.strip().splitlines()[-3:]
        shutil.move(str(workspace), str(session_dir / "workspace"))
        return {"error": f"claude exited {proc.returncode}: {' / '.join(tail) or 'no stderr'} — {session_dir}"}

    result, tools = _read_stream(proc.stdout)
    (session_dir / "tools.json").write_text(json.dumps(tools, indent=1))
    files = sorted(path for path, digest in _snapshot(workspace).items() if laid_down.get(path) != digest)
    shutil.move(str(workspace), str(session_dir / "workspace"))

    return {
        "output": result,
        "cost": _cost(proc.stdout),
        "metadata": {
            "arm": arm,
            "session_dir": str(session_dir),
            "transcript": str(session_dir / "transcript.jsonl"),
            "tools": str(session_dir / "tools.json"),
            "files": files,
        },
    }
