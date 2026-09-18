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
- `regex` — over the paths of the files the session wrote (`target: files`), or
  over their contents (`target: contents`). A scaffold's fixture is excluded
  before the list reaches here.
- `command` — runs `command:` in the session's workspace, with `LIVESPEC_ROOT`
  set, and passes on exit 0. The deterministic grader: what it runs is a
  script, so a case can be graded by the tool it is about rather than by a
  judge. See specs/changes/0041.
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
        elif kind == "person":
            # The human the sitting had (0058): what they answered between
            # rounds, so a judge reads the question and the answer together.
            if event.get("text"):
                pieces.append("PERSON: " + str(event["text"]))
            elif event.get("error"):
                pieces.append(f"PERSON: (could not be reached: {event['error']})")
            else:
                pieces.append("PERSON: (nothing to answer; the sitting ends here)")
        elif kind == "result":
            if event.get("subtype") == "error_max_turns" and not event.get("result"):
                pieces.append("FINAL REPLY: (none — the round hit its turn ceiling here; what is above is where it stopped)")
            else:
                pieces.append("FINAL REPLY: " + (event.get("result") or "(empty)"))
    digest = "\n\n".join(pieces)
    if len(digest) > DIGEST_LIMIT:
        half = DIGEST_LIMIT // 2
        digest = digest[:half] + "\n\n…[transcript truncated]…\n\n" + digest[-half:]
    return digest


def _ledger(case: str, arm: str, grader: str, model: str, cost: float) -> None:
    """One line per verdict in the run directory: what the judge cost, so the
    row's `cost` is the whole bill rather than the sessions' half of it. Before
    0057 roughly 350 judge calls a sitting were priced nowhere (#130)."""
    run_dir = os.environ.get("LIVESPEC_RUN_DIR")
    if not run_dir:
        return
    line = json.dumps({"case": case, "arm": arm, "grader": grader, "model": model, "cost": cost})
    with (Path(run_dir) / "judge.jsonl").open("a") as ledger:
        ledger.write(line + "\n")


def _judge(rubric: str, content: str, case: str = "?", arm: str = "?", grader: str = "?") -> dict:
    prompt = (
        "You are grading one automated-agent eval transcript against a rubric. "
        "Apply the rubric exactly as written — do not add criteria of your own, "
        "and do not excuse a FAIL condition because the attempt was reasonable.\n\n"
        "## Rubric\n\n" + rubric.strip() +
        "\n\n## What the agent produced\n\n" + (content.strip() or "(nothing)") +
        "\n\nReturn your verdict."
    )
    model = os.environ.get("LIVESPEC_JUDGE_MODEL", "sonnet")
    # `--output-format json` wraps the verdict in an envelope that also carries
    # `total_cost_usd`; the verdict itself sits in `structured_output`. Plain
    # stdout carried the verdict alone, and the judge's price with it went
    # nowhere.
    command = [
        "claude", "-p", "--model", model, "--output-format", "json",
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
            envelope = json.loads(proc.stdout.strip())
            verdict = envelope.get("structured_output")
            if not isinstance(verdict, dict):
                verdict = json.loads(envelope.get("result") or "")
            _ledger(case, arm, grader, model, float(envelope.get("total_cost_usd") or 0))
            return {"pass": bool(verdict["pass"]), "score": 1.0 if verdict["pass"] else 0.0,
                    "reason": str(verdict.get("reason", ""))[:800]}
        except Exception as err:
            last = err
    # Not a verdict: run.py leaves it out of the session's fraction and counts
    # it in the summary, so a judge that said nothing never reads as the agent
    # failing the rubric (#131, 0058).
    return {"pass": False, "score": 0.0, "errored": True, "reason": f"judge error after 3 attempts: {last}"}


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
        return _judge(body, content, case=str(((context or {}).get("vars") or {}).get("case") or "?"),
                      arm=str(metadata.get("arm") or "?"), grader=Path(config["grader"]).stem)

    if kind == "regex":
        pattern = re.compile(_unquote(body), re.I if "i" in fields.get("flags", "") else 0)
        files = metadata.get("files") or []
        if fields.get("target", "files") == "contents":
            workspace = Path(metadata.get("workspace") or "")
            hits = []
            for name in files:
                try:
                    if pattern.search((workspace / name).read_text(errors="replace")):
                        hits.append(name)
                except OSError:
                    continue
        else:
            hits = [f for f in files if pattern.search(f)]
        wanted = fields.get("match", "contains") != "not_contains"
        ok = bool(hits) if wanted else not hits
        return {"pass": ok, "score": 1.0 if ok else 0.0,
                "reason": f"{len(hits)} of {len(files)} session-written file(s) match" + (f": {hits[:5]}" if hits else "")}

    if kind == "command":
        command = _unquote(fields.get("command", ""))
        workspace = metadata.get("workspace")
        if not command or not workspace:
            return {"pass": False, "score": 0.0, "reason": "command grader with no command, or no workspace to run it in"}
        env = dict(os.environ, LIVESPEC_ROOT=str(root))
        try:
            proc = subprocess.run(command, shell=True, cwd=workspace, env=env, capture_output=True, text=True, timeout=120)
        except subprocess.TimeoutExpired:
            return {"pass": False, "score": 0.0, "reason": f"`{command}` did not finish in 120s"}
        tail = (proc.stdout + proc.stderr).strip().splitlines()[-3:]
        return {"pass": proc.returncode == 0, "score": 1.0 if proc.returncode == 0 else 0.0,
                "reason": f"`{command}` exited {proc.returncode}" + (": " + " / ".join(tail) if tail else "")}

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
