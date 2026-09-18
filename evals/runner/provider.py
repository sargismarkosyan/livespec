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

A session is a sitting, not a turn (0058). Its stdin stays open — `claude -p
--input-format stream-json` — and after each result, while the case has a
`person` and rounds remain, the person model answers from the sheet in the
human's voice and the reply goes in as the next user message. Each reply is a
`person` line in the transcript for the judge to read, and a line in the
ledger for the bill. Both arms get the same person. A `shell` var names the
command prefixes the case lends: `Bash` goes in as `Bash(<prefix>:*)` rules,
so a command outside them is refused by the headless session.

Not run directly: `run.py` generates the config that names this file.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

sys.path.insert(0, str(Path(os.environ["LIVESPEC_ROOT"]) / ".github" / "scripts"))
from caselib import SESSION_MODEL  # noqa: E402


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


def _init_model(raw: str) -> str:
    """The model the session says it ran on — the `init` event's word, not the
    flag's. The row records this, so a fallback or an alias that moved would
    stale itself rather than pass as the model the bindings name (0057)."""
    for line in raw.splitlines():
        if '"init"' not in line:
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") == "system" and event.get("subtype") == "init":
            return str(event.get("model") or "")
    return ""


def _cost(raw: str) -> float:
    """The sitting's cost: `total_cost_usd` is cumulative, so the last result's."""
    cost = 0.0
    for line in raw.splitlines():
        if '"total_cost_usd"' in line:
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if event.get("type") == "result":
                cost = float(event.get("total_cost_usd") or 0)
    return cost


def _ledger(case: str, arm: str, grader: str, model: str, cost: float) -> None:
    """The same ledger asserts.py keeps for the judge, one line per call the
    person model made, so the row's cost is the whole sitting (0057, 0058)."""
    run_dir = os.environ.get("LIVESPEC_RUN_DIR")
    if not run_dir:
        return
    line = json.dumps({"case": case, "arm": arm, "grader": grader, "model": model, "cost": cost})
    with (Path(run_dir) / "judge.jsonl").open("a") as ledger:
        ledger.write(line + "\n")


PERSON_SCHEMA = json.dumps({
    "type": "object",
    "properties": {"reply": {"type": "string"}, "done": {"type": "boolean"}},
    "required": ["reply", "done"],
    "additionalProperties": False,
})

PERSON_INSTRUCTION = """You are the person who asked for this work, answering a session that is working in your repository. You are not an assistant and not a reviewer. Everything you know is on the sheet below, in your own voice.

Rules:
- Answer only from the sheet. Where the session asks for something the sheet does not settle, your whole answer on that point is: Your call.
- Never add facts, requirements, preferences or context the sheet does not hold, and never answer a question that was not asked. The sheet answers; it never volunteers.
- Be brief and plain, in the sheet's voice: a few lines, one per question, no headings.
- done means there was nothing to answer: the session's message asks you nothing and is not waiting on you — it has finished, or it says what it does next without a question. Then set done to true and leave reply empty. If you answered anything at all, done is false."""


def _tail(text: str, limit: int) -> str:
    return text if len(text) <= limit else "…" + text[-limit:]


def _person(sheet: str, said: str, case: str, arm: str) -> tuple[str, bool, str]:
    """What the human would answer: (reply, done, error). The judge model, held
    to a two-field reply; three attempts, then the sitting ends and says why."""
    model = os.environ.get("LIVESPEC_JUDGE_MODEL", "sonnet")
    prompt = (PERSON_INSTRUCTION + "\n\n## What you know\n\n" + sheet.strip()
              + "\n\n## What the session just said to you\n\n" + _tail(said.strip() or "(nothing)", 8000)
              + "\n\nAnswer as the person.")
    command = [
        "claude", "-p", "--model", model, "--output-format", "json", "--max-turns", "1",
        "--no-session-persistence", "--setting-sources", "project", "--strict-mcp-config",
        "--json-schema", PERSON_SCHEMA,
    ]
    last = ""
    for attempt in range(3):
        if attempt:
            time.sleep(5)
        try:
            proc = subprocess.run(command, input=prompt, capture_output=True, text=True, timeout=180)
            envelope = json.loads(proc.stdout.strip())
            answer = envelope.get("structured_output")
            if not isinstance(answer, dict):
                answer = json.loads(envelope.get("result") or "")
            _ledger(case, arm, "person", model, float(envelope.get("total_cost_usd") or 0))
            return str(answer.get("reply") or "").strip(), bool(answer.get("done")), ""
        except Exception as err:  # noqa: BLE001 — every failure is the same failure here
            last = str(err)
    return "", True, last or "no reply"


def _sitting(command: list[str], prompt: str, cwd: Path, timeout: int, sheet: str, replies: int,
             case: str, arm: str) -> tuple[str, int, int, bool, str]:
    """Drive one session as a sitting. Returns (transcript, returncode, rounds,
    timed_out, stderr_tail). The first user message is the prompt; after each
    result the person answers, up to `replies` times; stdin closes when the
    person is done, the rounds run out, or there is no person at all."""
    proc = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            text=True, cwd=cwd, bufsize=1)
    lines: list[str] = []
    stderr: list[str] = []
    killed = {"yes": False}

    def kill() -> None:
        killed["yes"] = True
        proc.kill()

    def drain() -> None:
        stderr.append(proc.stderr.read() if proc.stderr else "")

    watchdog = threading.Timer(timeout, kill)
    watchdog.start()
    draining = threading.Thread(target=drain, daemon=True)
    draining.start()

    def send(text: str) -> None:
        assert proc.stdin is not None
        proc.stdin.write(json.dumps({"type": "user", "message": {"role": "user", "content": text}}) + "\n")
        proc.stdin.flush()

    rounds = 0
    try:
        send(prompt)
        while True:
            said = None
            while True:
                line = proc.stdout.readline() if proc.stdout else ""
                if not line:
                    break
                lines.append(line.rstrip("\n"))
                try:
                    event = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if event.get("type") == "result":
                    said = event.get("result") or ""
                    break
            if said is None or not sheet or rounds >= replies:
                break
            reply, done, error = _person(sheet, said, case, arm)
            if error:
                lines.append(json.dumps({"type": "person", "round": rounds + 1, "error": error}))
                break
            # A reply is sent whenever there is one. The first pilot's person
            # answered all six questions and set done beside them — "I have
            # answered; nothing more from me" — and the answers were dropped.
            # Done ends the sitting only when there was nothing to say.
            if not reply:
                lines.append(json.dumps({"type": "person", "round": rounds + 1, "done": True}))
                break
            rounds += 1
            lines.append(json.dumps({"type": "person", "round": rounds, "text": reply, "done": bool(done)}))
            send(reply)
        try:
            if proc.stdin:
                proc.stdin.close()
        except OSError:
            pass
        rest = proc.stdout.read() if proc.stdout else ""
        lines += [l.rstrip("\n") for l in rest.splitlines()]
        proc.wait()
    finally:
        watchdog.cancel()
        draining.join(timeout=5)
    tail = " / ".join((stderr[0] if stderr else "").strip().splitlines()[-3:])
    return "\n".join(lines) + ("\n" if lines else ""), proc.returncode, rounds, killed["yes"], tail


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
        "--input-format", "stream-json",
        "--output-format", "stream-json",
        "--no-session-persistence",
        "--setting-sources", "project",
        "--strict-mcp-config",
        "--max-turns", str(vars_.get("max_turns") or 25),  # per round, as the CLI applies it
    ]
    if os.environ.get("LIVESPEC_SANDBOX") == "1":
        # Claude Code's own sandbox, the network closed — the second wall behind
        # a lent shell's allow-list, where the machine has bubblewrap. run.py
        # sets this only when it found one; a machine without says so at the
        # top of the run instead.
        command += ["--settings", json.dumps({"sandbox": {"enabled": True, "autoAllowBashIfSandboxed": False,
                                                          "network": {"allowLocalBinding": False}}})]
    disallowed = [t for t in str(vars_.get("disallowed_tools") or "").split() if t]
    if disallowed:
        command += ["--disallowedTools", ",".join(disallowed)]
    if with_plugin:
        command += ["--plugin-dir", root]
    # Always named, never left to the account: every session of the sitting of
    # 2026-09-17 ran on a model nobody chose, and no row could say which. The
    # runner sets the variable from caselib.SESSION_MODEL or the --model flag;
    # the constant is the fallback so a bare call cannot drift either (#130).
    command += ["--model", os.environ.get("LIVESPEC_SESSION_MODEL") or SESSION_MODEL]
    allowed = [t for t in str(vars_.get("allowed_tools") or "").split() if t]
    shell = [s.strip() for s in str(vars_.get("shell") or "").split(",") if s.strip()]
    if shell and "Bash" in allowed:
        # The shell the case lends, and no more: each prefix becomes a rule the
        # session may run without asking; anything else asks, and a headless
        # session's ask is a refusal. `gh` and `curl` never run here (0058).
        allowed = [t for t in allowed if t != "Bash"] + [f"Bash({prefix}:*)" for prefix in shell]
    if allowed:
        # one comma-joined argument: --allowedTools is variadic and would
        # otherwise swallow everything after it
        command += ["--allowedTools", ",".join(allowed)]

    sheet = ""
    person_path = str(vars_.get("person") or "")
    if person_path and Path(person_path).exists():
        # frontmatter off, the sheet only — caselib read the rounds already
        text = Path(person_path).read_text()
        parts = text.split("---", 2)
        sheet = (parts[2] if text.lstrip().startswith("---") and len(parts) == 3 else text).strip()
    replies = int(vars_.get("replies") or 0) if sheet else 0

    timeout = int(vars_.get("timeout_seconds") or 600)
    transcript, code, rounds, timed_out, tail = _sitting(command, prompt, workspace, timeout, sheet, replies, case, arm)
    (session_dir / "transcript.jsonl").write_text(transcript)
    if timed_out:
        shutil.move(str(workspace), str(session_dir / "workspace"))
        return {"error": f"session timed out after {timeout}s — transcript in {session_dir}"}
    if code != 0:
        shutil.move(str(workspace), str(session_dir / "workspace"))
        return {"error": f"claude exited {code}: {tail or 'no stderr'} — {session_dir}"}

    result, tools = _read_stream(transcript)
    (session_dir / "tools.json").write_text(json.dumps(tools, indent=1))
    files = sorted(path for path, digest in _snapshot(workspace).items() if laid_down.get(path) != digest)
    shutil.move(str(workspace), str(session_dir / "workspace"))

    return {
        "output": result,
        "cost": _cost(transcript),
        "metadata": {
            "arm": arm,
            "model": _init_model(transcript),
            "rounds": rounds,
            "person": bool(sheet),
            "session_dir": str(session_dir),
            "transcript": str(session_dir / "transcript.jsonl"),
            "tools": str(session_dir / "tools.json"),
            "files": files,
            "workspace": str(session_dir / "workspace"),
        },
    }
