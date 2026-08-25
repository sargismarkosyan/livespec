#!/usr/bin/env python3
"""The grading end of the runner: one grader file, applied to one session.

promptfoo calls `get_assert` once per grader x session, with the grader named
in the assert's config. The rubric bodies stay untouched in `graders/` — this
reads them through the same `caselib` frontmatter reader the gates use, so the
runner and the gates cannot disagree about what a grader says.

Three kinds, matching what the suite contains:

- `llm` — the rubric plus what the session produced go to the judge model
  through `claude -p --json-schema`, which returns `{pass, reason}` and nothing
  else. `focus: full_transcript` sends a digest of the whole session;
  `last_message` sends the final text.
- `regex` — over the files the session wrote (`target: files`), the only
  target in use. A scaffold's fixture is excluded before the list reaches here.
- `tool_used` — with `max:` set it is a scored should-not-fire assertion, which
  can only ever cost the plugin arm points. With `min:` alone it is the
  plugin-fired indicator from the ablation contract: reported, weight zero,
  never in either arm's score — firing must not be able to inflate delta.

Not run directly: `run.py` generates the config that names this file.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(os.environ["LIVESPEC_ROOT"]) / ".github" / "scripts"))
from caselib import frontmatter  # noqa: E402

DIGEST_LIMIT = 120_000  # characters of transcript a judge is shown, at most
PIECE_LIMIT = 1_500     # characters kept of any one tool call or result

VERDICT_SCHEMA = json.dumps({
    "type": "object",
    "properties": {"pass": {"type": "boolean"}, "reason": {"type": "string"}},
    "required": ["pass", "reason"],
    "additionalProperties": False,
})


def _unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "'\"":
        return value[1:-1]
    return value


def _clip(text: str, limit: int = PIECE_LIMIT) -> str:
    return text if len(text) <= limit else text[:limit] + f" …[{len(text) - limit} more]"


def _digest(transcript_path: str) -> str:
    """A judge-readable rendering of a stream-json transcript."""
    pieces: list[str] = []
    for line in Path(transcript_path).read_text().splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        kind = event.get("type")
        if kind == "assistant":
            for block in (event.get("message") or {}).get("content") or []:
                if not isinstance(block, dict):
                    continue
                if block.get("type") == "text" and block.get("text"):
                    pieces.append("ASSISTANT: " + block["text"])
                elif block.get("type") == "tool_use":
                    pieces.append(f"TOOL CALL {block.get('name', '?')}: " + _clip(json.dumps(block.get("input", {}))))
        elif kind == "user":
            content = (event.get("message") or {}).get("content")
            for block in content if isinstance(content, list) else []:
                if isinstance(block, dict) and block.get("type") == "tool_result":
                    pieces.append("TOOL RESULT: " + _clip(json.dumps(block.get("content", ""))))
        elif kind == "result":
            pieces.append("FINAL REPLY: " + (event.get("result") or "(empty)"))
    digest = "\n\n".join(pieces)
    if len(digest) > DIGEST_LIMIT:
        half = DIGEST_LIMIT // 2
        digest = digest[:half] + "\n\n…[transcript truncated]…\n\n" + digest[-half:]
    return digest


def _judge(rubric: str, content: str) -> dict:
    prompt = (
        "You are grading one automated-agent eval transcript against a rubric. "
        "Apply the rubric exactly as written — do not add criteria of your own, "
        "and do not excuse a FAIL condition because the attempt was reasonable.\n\n"
        "## Rubric\n\n" + rubric.strip() +
        "\n\n## What the agent produced\n\n" + (content.strip() or "(nothing)") +
        "\n\nReturn your verdict."
    )
    command = [
        "claude", "-p", "--model", os.environ.get("LIVESPEC_JUDGE_MODEL", "sonnet"),
        "--max-turns", "1", "--no-session-persistence", "--json-schema", VERDICT_SCHEMA,
    ]
    # Retried: a judge that returns nothing once is a transient harness wobble,
    # and scoring it 0 would pollute one arm's number with a non-verdict. Only
    # after three attempts is the failure shown as one — legible in the
    # calibration read, never mistaken for the agent failing the rubric.
    last: Exception | None = None
    for attempt in range(3):
        if attempt:
            time.sleep(5)
        try:
            proc = subprocess.run(command, input=prompt, capture_output=True, text=True, timeout=180)
            verdict = json.loads(proc.stdout.strip())
            return {"pass": bool(verdict["pass"]), "score": 1.0 if verdict["pass"] else 0.0,
                    "reason": str(verdict.get("reason", ""))[:800]}
        except Exception as err:
            last = err
    return {"pass": False, "score": 0.0, "reason": f"judge error after 3 attempts: {last}"}


def get_assert(output, context):
    config = (context or {}).get("config") or {}
    root = Path(os.environ["LIVESPEC_ROOT"])
    metadata = ((context or {}).get("providerResponse") or {}).get("metadata") or {}
    fields, body = frontmatter(root / config["grader"])
    kind = fields.get("type", "")

    if kind == "llm":
        if fields.get("focus", "last_message") == "full_transcript" and metadata.get("transcript"):
            content = _digest(metadata["transcript"])
        else:
            content = str(output or "")
        return _judge(body, content)

    if kind == "regex":
        pattern = re.compile(_unquote(body), re.I if "i" in fields.get("flags", "") else 0)
        files = metadata.get("files") or []
        hits = [f for f in files if pattern.search(f)]
        wanted = fields.get("match", "contains") != "not_contains"
        ok = bool(hits) if wanted else not hits
        return {"pass": ok, "score": 1.0 if ok else 0.0,
                "reason": f"{len(hits)} of {len(files)} session-written file(s) match" + (f": {hits[:5]}" if hits else "")}

    if kind == "tool_used":
        tools = json.loads(Path(metadata["tools"]).read_text()) if metadata.get("tools") else []
        match = _unquote(fields.get("input_match", ""))
        count = sum(
            1 for t in tools
            if t.get("name") == fields.get("tool") and (not match or re.search(match, t.get("input", "")))
        )
        low = int(fields.get("min", "0") or 0)
        if fields.get("max", "").strip().isdigit():
            ok = low <= count <= int(fields["max"])  # scored: over-firing costs the plugin arm
            return {"pass": ok, "score": 1.0 if ok else 0.0,
                    "reason": f"{fields.get('tool')} fired {count}x (allowed {low}..{fields['max']})"}
        fired = count >= low  # indicator: reported, never scored
        return {"pass": True, "score": 1.0,
                "reason": f"plugin-fired indicator: {'fired' if fired else 'did not fire'} ({count}x, min {low})"}

    return {"pass": False, "score": 0.0, "reason": f"unknown grader type {kind!r} in {config['grader']}"}
