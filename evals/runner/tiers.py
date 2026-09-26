#!/usr/bin/env python3
"""The cheap tiers: what every edit is measured by (0072).

The sittings `run.py` drives are the most faithful measurement this suite has
and the one nobody can keep fresh — six real sessions a case, a person, a
shell, judge calls, and a skill edit that staled six cases cost $9. So the
freshness the board gates is held here instead, one call at a time:

    route    one real turn of `claude -p` with the plugin loaded and only the
             Skill tool: which skill fires on the case's prompt, or none.
             Staled by any skill's frontmatter, never by a body.
    first    one reply to a snapshot — the case's world as already read, the
             skill's body as already loaded, the prompt — judged by the case's
             own rubrics, both arms, so Δ survives. A rubric that only a later
             turn, a file on disk or a command could decide is marked as not
             applying rather than failed.
    review   one reading of a skill's body beside every rule the cases holding
             it claim: does the body still tell the model to do each one.

and, apart from the board because it measures the past rather than the tree:

    --transcripts   the sessions the maintainer already had, in the repositories
                    they use the plugin in (~/.claude/projects), graded against
                    the rules of each skill that fired — and the turns where one
                    should have fired and did not.

    python3 evals/runner/tiers.py --changed [--tier route|first|review] [--scaffold]
    python3 evals/runner/tiers.py --tier first --case 01-solution-shaped-request --scaffold
    python3 evals/runner/tiers.py --transcripts

**Every call is real money.** Cheaper is not free: this refuses exactly as
run.py does, prints what the selection would cost, and runs only with
`--i-approve-the-cost` — the maintainer's signature on one run, never an
agent's. Everything goes through `claude -p` on the maintainer's account, as
the sittings do: no API key, no dependency, the same session limit — a call
the limit refuses stops the run (exit 3), keeps every row already finished,
and `--changed` picks up the rest.

Calls other than the routing turn replace Claude Code's system prompt with
their own (`--system-prompt`), which is most of what makes them cheap: the
routing turn is the one place the real prompt is the thing under test.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
os.environ.setdefault("LIVESPEC_ROOT", str(ROOT))
sys.path.insert(0, str(ROOT / ".github" / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from caselib import (  # noqa: E402
    MIN_RUNS, SESSION_MODEL, TIERS, cases, frontmatter, grader_inputs, measurement_inputs, replaces,
    review_inputs, route_inputs, rule_text, skill_frontmatter, skill_rules, tier_harness_fingerprint, tier_keys,
    tier_stale_arms, tier_why_stale,
)
from provider import limit_text  # noqa: E402 — one reading of the account's refusal (0059)

BOARD = ROOT / "evals" / "board.json"
RESULTS = ROOT / "evals" / "results"

# The maintainer's signature on one run. See run.py's cost gate: the same
# refusal, for the same reason, and evalsuite.py fails if it goes missing here.
APPROVAL_FLAG = "--i-approve-the-cost"
LIMIT_EXIT = 3
ARMS = ("with", "without")

# What a call costs before the board holds a price for it — a guess, and
# printed as one. Once a row carries `cost`, the refusal quotes that instead.
# From the smoke run of 2026-09-27: a routing turn $0.04, a first reply and
# its verdict $0.18, a review $0.18; the transcript figures are scaled from
# the review, which reads about as much.
GUESS = {"route": 0.04, "first": 0.18, "review": 0.18, "firing": 0.10, "session": 0.03}

HERMETIC = ["--no-session-persistence", "--setting-sources", "project", "--strict-mcp-config"]

WORLD_LIMIT = 60_000      # characters of a case's world a snapshot carries
FILE_LIMIT = 12_000       # characters of any one file in it
SEGMENT_LIMIT = 60_000    # characters of a real session's firing a judge reads
PIECE_LIMIT = 600         # characters kept of one tool call or result


# The token counts of the last call this thread made, for the evidence: a
# price is only arguable when what it bought is on disk beside it.
_usage = threading.local()


class Limit(Exception):
    """The account said no. Carries its own words, reset time and all."""


def shown(path: Path) -> str:
    """A path as a reader wants it: relative to the repository when it is in it."""
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def _clip(text: str, limit: int = PIECE_LIMIT) -> str:
    return text if len(text) <= limit else text[:limit] + f"… [{len(text) - limit} more]"


def _middle(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    half = limit // 2
    return text[:half] + "\n\n…[truncated in the middle]…\n\n" + text[-half:]


def _envelope(stdout: str) -> dict:
    """The last JSON object on stdout — `--output-format json` prints one."""
    for line in reversed(stdout.strip().splitlines()):
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            return value
    raise ValueError("no JSON envelope on stdout")


def ask(prompt: str, *, model: str, system: str, schema: dict | None = None, timeout: int = 300) -> tuple[object, float]:
    """One call, no tools, a system prompt of our own. Returns (answer, cost):
    the structured answer when a schema was given, else the reply's text.
    Three attempts; the account's limit is never retried."""
    command = ["claude", "-p", "--model", model, "--output-format", "json", "--max-turns", "1",
               *HERMETIC, "--system-prompt", system]
    if schema is not None:
        command += ["--json-schema", json.dumps(schema)]
    else:
        # A reply, not a tool call: with no tools there is nothing to reach for,
        # and the one turn ends in words.
        command += ["--tools", ""]
    last = ""
    for attempt in range(3):
        if attempt:
            time.sleep(5)
        said = ""
        try:
            proc = subprocess.run(command, input=prompt, capture_output=True, text=True, timeout=timeout)
            said = " / ".join((proc.stderr or "").strip().splitlines()[-2:])
            envelope = _envelope(proc.stdout)
            if limit_text(envelope):
                raise Limit(limit_text(envelope))
            cost = float(envelope.get("total_cost_usd") or 0)
            _usage.last = {"cost": cost, "usage": envelope.get("usage") or {}}
            if schema is None:
                if envelope.get("is_error"):
                    raise ValueError(str(envelope.get("result") or "an error envelope"))
                return str(envelope.get("result") or ""), cost
            answer = envelope.get("structured_output")
            if not isinstance(answer, dict):
                answer = json.loads(envelope.get("result") or "")
            return answer, cost
        except Limit:
            raise
        except Exception as err:  # noqa: BLE001 — every other failure is the same failure here
            last = f"{err}" + (f" — the CLI said: {said}" if said else "")
    raise RuntimeError(f"no answer after 3 attempts: {last}")


# --- the world a case runs in -------------------------------------------------

def lay_down(case: dict, scaffold: bool) -> Path:
    """A fresh directory holding the case's world — its scaffold run in it, or
    nothing. In system tmp, never under the repository, for the reason the
    sittings give: a session run inside the repo reads livespec's own CLAUDE.md."""
    workspace = Path(tempfile.mkdtemp(prefix=f"livespec-tier-{case['name']}-"))
    if case["scaffold"] is not None and scaffold:
        build = subprocess.run(["bash", str(case["scaffold"])], cwd=workspace, capture_output=True,
                               text=True, timeout=120)
        if build.returncode != 0:
            shutil.rmtree(workspace, ignore_errors=True)
            raise RuntimeError(f"scaffold exited {build.returncode}: {_clip(build.stdout + build.stderr, 400)}")
    return workspace


def world_text(workspace: Path) -> str:
    """The world as a session would have read it: every text file, whole up to
    a limit, and the history when the world is a repository — cases that date
    a drift read `git log`."""
    pieces: list[str] = []
    for path in sorted(p for p in workspace.rglob("*") if p.is_file() and ".git" not in p.relative_to(workspace).parts):
        try:
            text = path.read_text()
        except (UnicodeDecodeError, OSError):
            continue
        pieces.append(f"=== {path.relative_to(workspace)} ===\n{_clip(text, FILE_LIMIT)}")
    if (workspace / ".git").exists():
        log = subprocess.run(["git", "-C", str(workspace), "log", "--date=short",
                              "--format=%h %ad %s", "--name-status", "-n", "40"],
                             capture_output=True, text=True)
        if log.stdout.strip():
            pieces.append("=== git log --name-status ===\n" + log.stdout.strip())
    if not pieces:
        return "(the directory is empty)"
    return _middle("\n\n".join(pieces), WORLD_LIMIT)


def prompt_of(case: dict) -> str:
    prompt = case["dir"] / "prompt.md"
    return frontmatter(prompt)[1].strip() if prompt.exists() else ""


def skill_body(skill: str) -> str:
    path = ROOT / "skills" / skill / "SKILL.md"
    text = path.read_text() if path.exists() else ""
    return text[len(skill_frontmatter(path)):].strip() if text.startswith("---") else text.strip()


# --- route ------------------------------------------------------------------

def _fired(stdout: str) -> tuple[str, float, str]:
    """(skill fired or "", cost, limit text) from a stream-json routing turn."""
    fired, cost, limit = "", 0.0, ""
    for line in stdout.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") == "assistant" and not fired:
            for block in (event.get("message") or {}).get("content") or []:
                if isinstance(block, dict) and block.get("type") == "tool_use" and block.get("name") == "Skill":
                    fired = str((block.get("input") or {}).get("skill") or "")
                    break
        elif event.get("type") == "result":
            cost = float(event.get("total_cost_usd") or cost)
            limit = limit or limit_text(event)
    return fired, cost, limit


def route_once(case: dict, model: str, scaffold: bool) -> tuple[str, float]:
    """One routing turn: the real Claude Code system prompt, the plugin loaded,
    Skill the only tool, one turn. What it reaches for first is the answer."""
    workspace = lay_down(case, scaffold)
    try:
        command = ["claude", "-p", "--verbose", "--output-format", "stream-json", "--model", model,
                   "--max-turns", "1", *HERMETIC, "--plugin-dir", str(ROOT),
                   "--tools", "Skill", "--allowedTools", "Skill"]
        last = ""
        for attempt in range(3):
            if attempt:
                time.sleep(5)
            proc = subprocess.run(command, input=prompt_of(case), capture_output=True, text=True,
                                  cwd=workspace, timeout=300)
            fired, cost, limit = _fired(proc.stdout)
            if limit:
                raise Limit(limit)
            # A turn that fired and then hit its one-turn ceiling exits non-zero
            # and is exactly the answer; a turn with no result at all is not.
            if '"type":"result"' in proc.stdout.replace(" ", "") or fired:
                return fired, cost
            last = " / ".join((proc.stderr or "").strip().splitlines()[-2:]) or f"exit {proc.returncode}"
        raise RuntimeError(f"the routing turn produced nothing after 3 attempts: {last}")
    finally:
        shutil.rmtree(workspace, ignore_errors=True)


def short(skill: str) -> str:
    return skill.split(":", 1)[1] if skill.startswith("livespec:") else skill


def label(fired: str) -> str:
    """What a routing turn reached for, as the row says it: one of ours by its
    own name, anybody else's as `other:<name>`, or `none`."""
    if not fired:
        return "none"
    ours = {p.parent.name for p in (ROOT / "skills").glob("*/SKILL.md")}
    if fired.startswith("livespec:") or (":" not in fired and fired in ours):
        return short(fired)
    return f"other:{fired}"


def route_right(case: dict, said: str) -> bool:
    """A should-not-fire case is right when none of ours fired; any other is
    right when one of the skills it holds did. `said` is a label."""
    if case["negative"]:
        return said == "none" or said.startswith("other:")
    return said in case["claims"]["skills"]


def measure_route(case: dict, runs: int, model: str, scaffold: bool, stop: threading.Event) -> dict | None:
    fired: list[str] = []
    cost = 0.0
    for _ in range(runs):
        if stop.is_set():
            return None
        skill, spent = route_once(case, model, scaffold)
        fired.append(label(skill))
        cost += spent
    hits = sum(1 for said in fired if route_right(case, said))
    return {
        "expected": "none" if case["negative"] else " or ".join(case["claims"]["skills"]),
        "fired": fired, "hits": hits, "runs": runs, "score": round(hits / runs, 2),
        "cost": round(cost, 4), "model": model,
        "inputs": route_inputs(case, ROOT),
    }


# --- first ------------------------------------------------------------------

FIRST_SYSTEM = """You are Claude Code, an AI coding agent, working in the user's repository.

In this turn you cannot run tools. Everything you would have read before replying has already been read, and is shown below: the repository's files, and — when one applies — the skill you loaded for this request. Reply to the user exactly as you would at this point in the session: what you say to them, any question you would ask and wait on, and what you would do next. If you would write or change a file now, show what you would write."""

JUDGE_FIRST = {
    "type": "object",
    "properties": {"verdicts": {"type": "array", "items": {
        "type": "object",
        "properties": {"id": {"type": "integer"}, "applies": {"type": "boolean"},
                       "pass": {"type": "boolean"}, "reason": {"type": "string"}},
        "required": ["id", "applies", "pass", "reason"], "additionalProperties": False}}},
    "required": ["verdicts"], "additionalProperties": False,
}

JUDGE_FIRST_SYSTEM = """You grade an automated agent's reply against rubrics. Apply each rubric exactly as written: add no criteria of your own, and do not excuse a FAIL condition because the attempt was reasonable.

The reply you are shown is the agent's FIRST reply in a session — it could read the repository but could not run tools, write files or hear back from the person. So, for each rubric, first decide whether it can be decided from a first reply at all:

- applies = true when the rubric is about what the agent says, asks, refuses, proposes, or says it would write or do next. A rubric about content the agent would write can be judged from what the reply shows it would write.
- applies = false only when the rubric can be decided solely by something a first reply cannot contain: files actually on disk at the end, a later turn after the person answered, a command actually run, the order of tool calls. Decide this from the rubric, not from how good this reply is.

When applies is false, set pass to false and say why it does not apply. Judge every rubric on its own; one verdict may not influence another. Give each a reason that quotes what in the reply decided it."""


def first_prompt(case: dict, world: str, arm: str) -> str:
    parts = [f"<repository>\n{world}\n</repository>"]
    if arm == "with":
        for skill in case["claims"]["skills"]:
            parts.append(f'<skill name="livespec:{skill}">\nYou loaded this skill for the request below; follow it.\n'
                         f"Base directory for this skill: {ROOT / 'skills' / skill}\n\n{skill_body(skill)}\n</skill>")
    parts.append(f"<request>\n{prompt_of(case)}\n</request>")
    return "\n\n".join(parts)


def llm_graders(case: dict) -> list[dict]:
    return [g for g in case["graders"] if g["type"] == "llm" and g["body"]]


def judge_first(case: dict, reply: str, judge: str) -> tuple[dict[str, dict], float]:
    graders = llm_graders(case)
    rubrics = "\n\n".join(f"### Rubric {n}\n\n{g['body']}" for n, g in enumerate(graders, 1))
    prompt = (f"## The agent's first reply\n\n{reply.strip() or '(nothing)'}\n\n## The rubrics\n\n{rubrics}"
              f"\n\nReturn exactly {len(graders)} verdicts, ids 1 to {len(graders)}.")
    for _ in range(2):
        answer, cost = ask(prompt, model=judge, system=JUDGE_FIRST_SYSTEM, schema=JUDGE_FIRST)
        rows = {int(r["id"]): r for r in (answer.get("verdicts") or []) if isinstance(r, dict) and "id" in r}
        if set(rows) == set(range(1, len(graders) + 1)):
            return ({g["path"].name: {"applies": bool(rows[n]["applies"]), "pass": bool(rows[n]["pass"]),
                                      "reason": str(rows[n].get("reason") or "")[:600]}
                     for n, g in enumerate(graders, 1)}, cost)
    raise RuntimeError("the judge did not return one verdict per rubric")


def first_scores(rubrics: dict) -> tuple[float | None, float | None, int]:
    """Each arm's score over the rubrics that apply at a first move. A rubric
    applies when the judge said so in at least half of every session it read,
    both arms together — decided once for the case, so the two arms are scored
    over the same rubrics and Δ compares like with like."""
    applicable = []
    for name, arms in rubrics.items():
        said = sum(arms.get(arm, {}).get("applies", 0) for arm in ARMS)
        read = sum(arms.get(arm, {}).get("n", 0) for arm in ARMS)
        if read and said * 2 >= read:
            applicable.append(name)
    scores = []
    for arm in ARMS:
        passed = sum(rubrics[name].get(arm, {}).get("pass", 0) for name in applicable)
        seen = sum(rubrics[name].get(arm, {}).get("n", 0) for name in applicable)
        scores.append(round(passed / seen, 2) if seen else None)
    return scores[0], scores[1], len(applicable)


def measure_first(case: dict, arms: list[str], runs: int, model: str, judge: str, scaffold: bool,
                  stop: threading.Event, prior: dict | None, evidence: Path) -> dict | None:
    rubrics: dict[str, dict] = {g["path"].name: {} for g in llm_graders(case)}
    cost = 0.0
    workspace = lay_down(case, scaffold)
    try:
        world = world_text(workspace)
    finally:
        shutil.rmtree(workspace, ignore_errors=True)
    for arm in arms:
        for run in range(runs):
            if stop.is_set():
                return None
            reply, spent = ask(first_prompt(case, world, arm), model=model, system=FIRST_SYSTEM)
            reply_usage = getattr(_usage, "last", {})
            verdicts, judged = judge_first(case, reply, judge)
            cost += spent + judged
            (evidence / f"{case['name']}-{arm}-{run + 1}.json").write_text(json.dumps(
                {"reply": reply, "verdicts": verdicts, "reply_usage": reply_usage,
                 "judge_usage": getattr(_usage, "last", {})}, indent=1))
            for name, verdict in verdicts.items():
                tally = rubrics[name].setdefault(arm, {"pass": 0, "applies": 0, "n": 0})
                tally["n"] += 1
                tally["applies"] += int(verdict["applies"])
                tally["pass"] += int(verdict["pass"] and verdict["applies"])
    carried = [arm for arm in ARMS if arm not in arms]
    for arm in carried:
        # An arm this run did not perform keeps its tallies, and the row says so (0070).
        for name, arms_ in ((prior or {}).get("rubrics") or {}).items():
            if name in rubrics and arm in arms_:
                rubrics[name][arm] = arms_[arm]
    with_, without, applicable = first_scores(rubrics)
    row = {
        "with": with_, "without": without,
        "delta": round(with_ - without, 2) if with_ is not None and without is not None else None,
        "runs": min((max((r.get(arm, {}).get("n", 0) for r in rubrics.values()), default=0) for arm in ARMS)),
        "applicable": applicable, "rubrics": rubrics,
        "cost": round(cost, 4), "model": model, "judge": judge,
        "inputs": measurement_inputs(case, ROOT, "with"),
        "inputs_without": measurement_inputs(case, ROOT, "without"),
        "graders": grader_inputs(case),
    }
    for arm in carried:
        field = "inputs" if arm == "with" else "inputs_without"
        if prior and prior.get(field):
            row[field] = prior[field]
        row.setdefault("carried", []).append(arm)
    return row


# --- review -----------------------------------------------------------------

REVIEW_SCHEMA = {
    "type": "object",
    "properties": {"rules": {"type": "array", "items": {
        "type": "object",
        "properties": {"id": {"type": "string"}, "verdict": {"type": "string", "enum": ["held", "weakened", "missing"]},
                       "quote": {"type": "string"}, "reason": {"type": "string"}},
        "required": ["id", "verdict", "quote", "reason"], "additionalProperties": False}}},
    "required": ["rules"], "additionalProperties": False,
}

REVIEW_SYSTEM = """You review an agent skill — a file of instructions a model follows — against the rules it is meant to uphold. For each rule, decide whether the skill's text still tells the model to behave as the rule promises:

- held: the skill instructs this behaviour clearly enough that a model following it would do what the rule's examples show.
- weakened: the skill touches it, but vaguely, only in passing, or in a way a model could follow and still break an example.
- missing: nothing in the skill tells the model to do this, or the skill tells it to do something the rule forbids.

Quote the sentence of the skill that decides each verdict (empty when missing). Judge only the text you are given; do not assume the model will do the right thing unprompted."""


def measure_review(skill: str, suite: list[dict], judge: str, stop: threading.Event) -> dict | None:
    if stop.is_set():
        return None
    rules = skill_rules(skill, suite)
    skill_md = (ROOT / "skills" / skill / "SKILL.md").read_text()
    blocks = "\n\n".join(f"### {rule}\n\n{rule_text(ROOT, rule).strip()}" for rule in rules)
    prompt = (f"## The skill: {skill}\n\n{skill_md}\n\n## The rules it upholds\n\n{blocks or '(none)'}"
              f"\n\nReturn one verdict per rule, ids exactly as headed: {', '.join(rules)}.")
    answer, cost = ask(prompt, model=judge, system=REVIEW_SYSTEM, schema=REVIEW_SCHEMA)
    got = {str(r.get("id")): r for r in answer.get("rules") or [] if isinstance(r, dict)}
    not_held = [{"id": rule, "verdict": got.get(rule, {}).get("verdict", "missing"),
                 "reason": str(got.get(rule, {}).get("reason") or "no verdict returned")[:400]}
                for rule in rules if got.get(rule, {}).get("verdict") != "held"]
    return {"held": len(rules) - len(not_held), "rules": len(rules), "not_held": not_held,
            "cost": round(cost, 4), "judge": judge, "inputs": review_inputs(skill, suite, ROOT)}


# --- the board ----------------------------------------------------------------

_board_lock = threading.Lock()


def load_board() -> dict:
    try:
        board = json.loads(BOARD.read_text())
    except (OSError, json.JSONDecodeError):
        board = {"format": 1}
    board.setdefault("cases", {})
    for tier in TIERS:
        board.setdefault(tier, {})
    return board


def _sha() -> str:
    try:
        return subprocess.run(["git", "-C", str(ROOT), "rev-parse", "--short", "HEAD"],
                              capture_output=True, text=True).stdout.strip() or "unknown"
    except OSError:
        return "unknown"


def record(tier: str, key: str, row: dict, sha: str) -> bool:
    """Write one row the moment it exists, so a run the limit stops keeps what
    it finished. A run below the floor never takes a measurement's row (#75)."""
    with _board_lock:
        board = load_board()
        prior = board[tier].get(key)
        runs = row.get("runs")
        if isinstance(runs, int) and not replaces(prior, runs):
            return False
        row.update({"at": time.strftime("%Y-%m-%d"), "sha": sha, "harness": tier_harness_fingerprint(ROOT)})
        board[tier][key] = dict(sorted(row.items()))
        board[tier] = dict(sorted(board[tier].items()))
        BOARD.write_text(json.dumps(board, indent=1) + "\n")
        return True


def owed(tiers: list[str], suite: list[dict], board: dict, changed: bool, only: set[str] | None) -> list[tuple[str, str, list[str]]]:
    """(tier, key, arms) for every row this run measures."""
    work = []
    for tier in tiers:
        for key in tier_keys(tier, suite, ROOT):
            if only is not None and key not in only:
                continue
            entry = board[tier].get(key)
            reasons = tier_why_stale(tier, key, entry, suite, ROOT)
            if changed and not reasons:
                continue
            arms = list(ARMS)
            if tier == "first" and changed and not ({"model", "harness", "graders", "never measured"} & set(reasons)):
                case = next(c for c in suite if c["name"] == key)
                arms = tier_stale_arms(entry, case, ROOT) or list(ARMS)
            work.append((tier, key, arms))
    return work


def price(work: list[tuple[str, str, list[str]]], board: dict, runs: int) -> tuple[float, int]:
    """What the work would cost, from each row's last cost, else the guess."""
    total, guessed = 0.0, 0
    for tier, key, arms in work:
        # calls this row will make: a review is one; a route is one a run; a
        # first move is one reply and one verdict a run, per arm owed
        calls = 1 if tier == "review" else runs * (len(arms) if tier == "first" else 1)
        entry = board[tier].get(key)
        if isinstance(entry, dict) and isinstance(entry.get("cost"), (int, float)) and not entry.get("carried"):
            made = 1 if tier == "review" else max(int(entry.get("runs") or 1), 1) * (2 if tier == "first" else 1)
            total += float(entry["cost"]) / made * calls
        else:
            guessed += 1
            total += GUESS[tier] * calls
    return total, guessed


def refusal(what: str, total: float, guessed: int, model: str) -> str:
    guess = f" ({guessed} of them never priced, counted at a guess)" if guessed else ""
    return f"""✘ this run spends real money, and nobody approved it.

  ≈ ${total:.2f} for {what}, on {model}{guess}.
  Drawn from the maintainer's account and its session limit. Cheaper than a
  sitting is not free. A stale row is not an approval; a --changed heal is not
  an approval.

  If you are an agent: do not add {APPROVAL_FLAG} on your own initiative.
  Stop, tell the maintainer what is stale and what this costs, and add the flag
  only after they have said yes to this run.

  Approved by the maintainer, just now, for this run?
      {APPROVAL_FLAG}
"""


# --- the sessions already had ------------------------------------------------

TRANSCRIPT_JUDGE = {
    "type": "object",
    "properties": {"rules": {"type": "array", "items": {
        "type": "object",
        "properties": {"id": {"type": "string"},
                       "verdict": {"type": "string", "enum": ["held", "broken", "not-tested"]},
                       "quote": {"type": "string"}, "reason": {"type": "string"}},
        "required": ["id", "verdict", "quote", "reason"], "additionalProperties": False}}},
    "required": ["rules"], "additionalProperties": False,
}

TRANSCRIPT_SYSTEM = """You read part of a real working session in which an agent used a skill, and judge it against the rules that skill must uphold. The person in it is the real user, not a test.

For each rule: held when the session gives the situation the rule is about and the agent behaved as the rule promises; broken when the situation arose and the agent did not; not-tested when the situation never came up in this part of the session. Most rules will be not-tested in any one session — say so rather than stretch. Quote what decided each held or broken verdict."""

MISSES_SCHEMA = {
    "type": "object",
    "properties": {"findings": {"type": "array", "items": {
        "type": "object",
        "properties": {"message": {"type": "integer"}, "fired": {"type": "string"},
                       "should": {"type": "string"}, "reason": {"type": "string"}},
        "required": ["message", "fired", "should", "reason"], "additionalProperties": False}}},
    "required": ["findings"], "additionalProperties": False,
}

MISSES_SYSTEM = """You audit which skill an agent loaded for each thing a person asked, in a real session. You are given the skills' descriptions, the person's messages numbered in order, and which skill (if any) the agent loaded after each.

Report only clear mistakes: a message where a skill plainly should have been loaded and was not, or where the skill loaded was plainly the wrong one. Most messages need none — a reply to a question the agent asked, a go-ahead, a follow-up inside work already under way. `fired` is what was loaded ("none" if nothing), `should` is what should have been ("none" if nothing). Return no findings when there are none."""


def _text_of(content) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(b.get("text", "") for b in content if isinstance(b, dict) and b.get("type") == "text")
    return ""


def _human(event: dict) -> str:
    """The person's own words in a user event, or empty — tool results, skill
    bodies, local-command echoes and injected reminders are not the person."""
    if event.get("type") != "user" or event.get("isMeta") or event.get("isSidechain"):
        return ""
    content = (event.get("message") or {}).get("content")
    if isinstance(content, list) and any(isinstance(b, dict) and b.get("type") == "tool_result" for b in content):
        return ""
    text = _text_of(content).strip()
    if not text or text.startswith(("Base directory for this skill:", "Caveat:", "<local-command", "<system-reminder>")):
        return ""
    return text


def _slash(text: str) -> str:
    match = re.search(r"<command-name>/?livespec:([\w-]+)</command-name>", text)
    return match.group(1) if match else ""


def read_session(path: Path, ours: set[str]) -> tuple[list[dict], list[dict]]:
    """(events, firings) of one Claude Code session file. A firing is a Skill
    call naming one of our skills, or a slash command for one."""
    events: list[dict] = []
    for line in path.read_text(errors="replace").splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") in ("user", "assistant") and not event.get("isSidechain"):
            events.append(event)
    firings = []
    for index, event in enumerate(events):
        if event.get("type") == "assistant":
            for block in (event.get("message") or {}).get("content") or []:
                if isinstance(block, dict) and block.get("type") == "tool_use" and block.get("name") == "Skill":
                    skill = short(str((block.get("input") or {}).get("skill") or ""))
                    if skill in ours and str((block.get("input") or {}).get("skill", "")).startswith(("livespec:", skill)):
                        firings.append({"skill": skill, "at": index})
        elif event.get("type") == "user":
            skill = _slash(_text_of((event.get("message") or {}).get("content")))
            if skill in ours:
                firings.append({"skill": skill, "at": index})
    return events, firings


def render(events: list[dict], start: int, end: int) -> str:
    pieces: list[str] = []
    for event in events[start:end]:
        human = _human(event)
        if human:
            pieces.append("PERSON: " + _clip(human, 4000))
            continue
        content = (event.get("message") or {}).get("content")
        if event.get("type") == "assistant":
            for block in content or []:
                if not isinstance(block, dict):
                    continue
                if block.get("type") == "text" and block.get("text"):
                    pieces.append("ASSISTANT: " + block["text"])
                elif block.get("type") == "tool_use":
                    pieces.append(f"TOOL CALL {block.get('name', '?')}: " + _clip(json.dumps(block.get("input", {}))))
        elif isinstance(content, list):
            for block in content:
                if isinstance(block, dict) and block.get("type") == "tool_result":
                    pieces.append("TOOL RESULT: " + _clip(json.dumps(block.get("content", ""))))
    return _middle("\n\n".join(pieces), SEGMENT_LIMIT)


def segment(events: list[dict], firings: list[dict], n: int) -> str:
    """One firing's part of the session: from the person's message that led to
    it, to the next firing of one of our skills or the end."""
    at = firings[n]["at"]
    start = next((i for i in range(at, -1, -1) if _human(events[i]) or _slash(_text_of((events[i].get("message") or {}).get("content")))), 0)
    end = firings[n + 1]["at"] if n + 1 < len(firings) else len(events)
    return render(events, start, end)


def transcripts(args, suite: list[dict]) -> int:
    source = Path(args.source).expanduser()
    ours = {p.parent.name for p in (ROOT / "skills").glob("*/SKILL.md")}
    state_dir = RESULTS / "transcripts"
    state_path = state_dir / "graded.json"
    try:
        graded = json.loads(state_path.read_text())
    except (OSError, json.JSONDecodeError):
        graded = {}
    graded.setdefault("firings", {})
    graded.setdefault("sessions", {})
    sessions = []
    for project in sorted(p for p in source.iterdir() if p.is_dir()) if source.is_dir() else []:
        # This repository's own sessions are the plugin being built, not used.
        if "livespec" in project.name and not args.include_self:
            continue
        for path in sorted(project.glob("*.jsonl")):
            events, firings = read_session(path, ours)
            if firings:
                sessions.append((project.name, path, events, firings))
    todo_firings = [(p, path, events, firings, n) for p, path, events, firings in sessions
                    for n in range(len(firings)) if args.regrade or f"{path.name}#{n}" not in graded["firings"]]
    todo_sessions = [(p, path, events, firings) for p, path, events, firings in sessions
                     if args.regrade or path.name not in graded["sessions"]]
    if args.limit:
        todo_firings = todo_firings[: args.limit]
        todo_sessions = todo_sessions[: args.limit]
    total = GUESS["firing"] * len(todo_firings) + GUESS["session"] * len(todo_sessions)
    print(f"  {len(sessions)} session(s) under {source} fired a livespec skill; "
          f"{len(todo_firings)} firing(s) and {len(todo_sessions)} session(s) not yet graded")
    if not todo_firings and not todo_sessions:
        return summarise_transcripts(graded)
    if not args.approved:
        print(refusal(f"{len(todo_firings)} firing(s) judged against their skill's rules and "
                      f"{len(todo_sessions)} session(s) read for misses", total, len(todo_firings) + len(todo_sessions),
                      args.judge_model), file=sys.stderr)
        return 2
    state_dir.mkdir(parents=True, exist_ok=True)
    descriptions = "\n".join(f"- livespec:{p.parent.name}: " + skill_frontmatter(p).replace("\n", " ")[:900]
                             for p in sorted((ROOT / "skills").glob("*/SKILL.md")))
    lock = threading.Lock()
    stop = threading.Event()
    spent = {"cost": 0.0, "limit": ""}

    def save() -> None:
        state_path.write_text(json.dumps(graded, indent=1) + "\n")

    def grade_firing(item) -> None:
        project, path, events, firings, n = item
        if stop.is_set():
            return
        skill = firings[n]["skill"]
        rules = skill_rules(skill, suite)
        blocks = "\n\n".join(f"### {rule}\n\n{rule_text(ROOT, rule).strip()}" for rule in rules)
        prompt = (f"## The skill that fired: livespec:{skill}\n\n## Its rules\n\n{blocks}\n\n"
                  f"## The session, from the request that led to it\n\n{segment(events, firings, n)}"
                  f"\n\nReturn one verdict per rule, ids exactly as headed.")
        answer, cost = ask(prompt, model=args.judge_model, system=TRANSCRIPT_SYSTEM, schema=TRANSCRIPT_JUDGE)
        with lock:
            spent["cost"] += cost
            graded["firings"][f"{path.name}#{n}"] = {
                "project": project, "skill": skill, "graded": time.strftime("%Y-%m-%d"),
                "rules": [{k: str(r.get(k, ""))[:500] for k in ("id", "verdict", "quote", "reason")}
                          for r in answer.get("rules") or [] if isinstance(r, dict)],
            }
            save()

    def read_misses(item) -> None:
        project, path, events, firings = item
        if stop.is_set():
            return
        after: dict[int, str] = {}
        messages: list[str] = []
        fired_at = {f["at"]: f["skill"] for f in firings}
        for index, event in enumerate(events):
            human = _human(event)
            if human:
                messages.append(_clip(human, 400))
            if index in fired_at and messages:
                after[len(messages)] = fired_at[index]
        listed = "\n".join(f"{i}. {m}\n   → loaded: {('livespec:' + after[i]) if i in after else 'none'}"
                           for i, m in enumerate(messages, 1))
        prompt = f"## The skills\n\n{descriptions}\n\n## The person's messages\n\n{_middle(listed, 30_000)}"
        answer, cost = ask(prompt, model=args.judge_model, system=MISSES_SYSTEM, schema=MISSES_SCHEMA)
        with lock:
            spent["cost"] += cost
            graded["sessions"][path.name] = {
                "project": project, "graded": time.strftime("%Y-%m-%d"),
                "findings": [dict(f, text=messages[f["message"] - 1][:300] if 0 < f.get("message", 0) <= len(messages) else "")
                             for f in answer.get("findings") or [] if isinstance(f, dict)],
            }
            save()

    def guarded(fn):
        def run(item):
            try:
                fn(item)
            except Limit as limit:
                spent["limit"] = str(limit)
                stop.set()
            except Exception as err:  # noqa: BLE001
                print(f"  ✘ {item[1].name}: {err}", file=sys.stderr)
        return run

    with ThreadPoolExecutor(max_workers=args.max_concurrency) as pool:
        list(pool.map(guarded(grade_firing), todo_firings))
        list(pool.map(guarded(read_misses), todo_sessions))
    print(f"  spent ≈ ${spent['cost']:.2f}; graded state in {shown(state_path)}")
    code = summarise_transcripts(graded)
    if spent["limit"]:
        print(f"  ✋ the account's limit stopped the run: {spent['limit']} — run again to grade the rest")
        return LIMIT_EXIT
    return code


def summarise_transcripts(graded: dict) -> int:
    tally: dict[tuple[str, str], dict[str, int]] = {}
    broken = []
    for key, firing in graded.get("firings", {}).items():
        for rule in firing.get("rules", []):
            counts = tally.setdefault((firing["skill"], rule.get("id", "?")), {"held": 0, "broken": 0, "not-tested": 0})
            counts[rule.get("verdict", "not-tested")] = counts.get(rule.get("verdict", "not-tested"), 0) + 1
            if rule.get("verdict") == "broken":
                broken.append((firing["skill"], rule.get("id"), firing.get("project", "?"), key, rule.get("quote", "")))
    tested = {k: v for k, v in tally.items() if v["held"] or v["broken"]}
    print(f"\n  Real use: {len(graded.get('firings', {}))} firing(s) graded; "
          f"{len(tested)} rule(s) met the situation they are about at least once")
    for (skill, rule), counts in sorted(tested.items()):
        print(f"    {skill:<17} {rule:<60} held {counts['held']:>2}  broken {counts['broken']:>2}")
    for skill, rule, project, key, quote in broken:
        print(f"  ✘ {skill} broke {rule} in {project}/{key}: {_clip(quote, 200)}")
    misses = [(s.get("project", "?"), name, f) for name, s in graded.get("sessions", {}).items() for f in s.get("findings", [])]
    for project, name, finding in misses:
        print(f"  ⚠ {project}/{name} message {finding.get('message')}: loaded {finding.get('fired')}, "
              f"should have been {finding.get('should')} — {_clip(str(finding.get('reason', '')), 200)}")
    if not broken and not misses:
        print("  ✔ nothing broken and no routing mistakes found in what was graded")
    return 0


# --- running ------------------------------------------------------------------

def summarise(results: list[tuple[str, str, dict]]) -> None:
    for tier, key, row in sorted(results):
        if tier == "route":
            mark = "✔" if row["hits"] == row["runs"] else ("~" if row["hits"] else "✘")
            print(f"  {mark} route  {key:<52} expected {row['expected']:<18} fired {', '.join(row['fired'])}")
        elif tier == "first":
            if row["with"] is None:
                print(f"  · first  {key:<52} no rubric applies at the first move — the canary holds it")
            else:
                print(f"  {'✔' if (row['delta'] or 0) > 0 else '·'} first  {key:<52} with {row['with']:.2f}  "
                      f"without {row['without']:.2f}  Δ {row['delta']:+.2f}  over {row['applicable']} rubric(s)")
        else:
            print(f"  {'✔' if not row['not_held'] else '✘'} review {key:<52} {row['held']}/{row['rules']} rules held")
            for item in row["not_held"]:
                print(f"      {item['verdict']:<9} {item['id']}: {_clip(item['reason'], 160)}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--tier", action="append", choices=TIERS,
                        help="measure only this tier (repeatable); all three by default")
    parser.add_argument("--changed", action="store_true",
                        help="only the rows the board holds nothing fresh for — the heal the board gate prints")
    parser.add_argument("--case", action="append", help="only this case (route, first; repeatable)")
    parser.add_argument("--skill", action="append", help="only this skill (review; repeatable)")
    parser.add_argument("--runs", type=int, default=MIN_RUNS,
                        help=f"calls per case and arm (default {MIN_RUNS}, the floor; below it is a pilot and "
                             "never takes a measurement's row)")
    parser.add_argument("--model", default=SESSION_MODEL,
                        help=f"the model routing turns and first replies run on (default caselib.SESSION_MODEL, {SESSION_MODEL})")
    parser.add_argument("--judge-model", default="sonnet", help="judge for first-move rubrics, reviews and transcripts")
    parser.add_argument("--scaffold", action="store_true",
                        help="run each case's scaffold_script to lay its world down — author-supplied bash, run as you")
    parser.add_argument("--max-concurrency", type=int, default=4)
    parser.add_argument("--transcripts", action="store_true",
                        help="grade the sessions already had in other repositories, instead of the tiers")
    parser.add_argument("--from", dest="source", default="~/.claude/projects",
                        help="where Claude Code keeps its sessions (with --transcripts)")
    parser.add_argument("--include-self", action="store_true",
                        help="also read this repository's own sessions (with --transcripts)")
    parser.add_argument("--regrade", action="store_true", help="grade again what was graded before (with --transcripts)")
    parser.add_argument("--limit", type=int, help="at most this many firings and sessions (with --transcripts)")
    parser.add_argument(APPROVAL_FLAG, action="store_true", dest="approved",
                        help="the maintainer's approval for this one run. Required — never add it on an agent's own initiative")
    args = parser.parse_args()

    suite = cases(ROOT)
    if args.transcripts:
        return transcripts(args, suite)

    tiers = args.tier or list(TIERS)
    board = load_board()
    only = set(args.case or []) | set(args.skill or []) or None
    if only:
        known = {c["name"] for c in suite} | {p.parent.name for p in (ROOT / "skills").glob("*/SKILL.md")}
        unknown = sorted(only - known)
        if unknown:
            print(f"✘ no such case or skill: {', '.join(unknown)}", file=sys.stderr)
            return 1
    work = owed(tiers, suite, board, args.changed, only)
    if not work:
        print("✔ every tier row is current — nothing has changed since it was measured"
              if args.changed else "✘ nothing selected", file=sys.stderr if not args.changed else sys.stdout)
        return 0 if args.changed else 1
    by_name = {c["name"]: c for c in suite}
    unlaid = sorted({key for tier, key, _ in work if tier != "review" and by_name[key]["scaffold"] is not None})
    if unlaid and not args.scaffold:
        print(f"✘ {len(unlaid)} selected case(s) lay their world down with a scaffold_script "
              f"({', '.join(unlaid[:4])}{'…' if len(unlaid) > 4 else ''}); pass --scaffold, or they are measured "
              "in an empty directory where the fixture should be", file=sys.stderr)
        return 1

    counts = {tier: sum(1 for t, _, _ in work if t == tier) for tier in tiers}
    what = ", ".join(f"{n} {tier} row(s)" for tier, n in counts.items() if n) + f" at {args.runs} call(s) a row"
    total, guessed = price(work, board, args.runs)
    if not args.approved:
        print(refusal(what, total, guessed, args.model), file=sys.stderr)
        return 2

    sha = _sha()
    stop = threading.Event()
    limit = {"text": ""}
    evidence = RESULTS / f"tiers-{time.strftime('%Y%m%d-%H%M%S')}"
    evidence.mkdir(parents=True, exist_ok=True)
    results: list[tuple[str, str, dict]] = []
    held: list[str] = []
    lock = threading.Lock()
    print(f"  {what}, on {args.model}, judged by {args.judge_model} — evidence in {shown(evidence)}")

    def one(item: tuple[str, str, list[str]]) -> None:
        tier, key, arms = item
        try:
            if tier == "route":
                row = measure_route(by_name[key], args.runs, args.model, args.scaffold, stop)
            elif tier == "first":
                row = measure_first(by_name[key], arms, args.runs, args.model, args.judge_model, args.scaffold,
                                    stop, load_board()["first"].get(key), evidence)
            else:
                row = measure_review(key, suite, args.judge_model, stop)
        except Limit as reached:
            limit["text"] = str(reached)
            stop.set()
            return
        except Exception as err:  # noqa: BLE001 — a row that errored is not a row of zero
            print(f"  ✘ {tier} {key}: {err}", file=sys.stderr)
            return
        if row is None:
            return
        with lock:
            if record(tier, key, row, sha):
                results.append((tier, key, row))
            else:
                held.append(f"{tier} {key}")

    with ThreadPoolExecutor(max_workers=args.max_concurrency) as pool:
        list(pool.map(one, work))

    summarise(results)
    spent = sum(float(row.get("cost") or 0) for _, _, row in results)
    print(f"\n  {len(results)} of {len(work)} row(s) written to evals/board.json; spent ≈ ${spent:.2f}")
    for name in held:
        print(f"  ✋ {name}: below the floor of {MIN_RUNS} and the board holds a measurement — kept; "
              "the pilot's replies are in the evidence directory")
    if limit["text"]:
        print(f"  ✋ the account's limit stopped the run: {limit['text']}\n"
              f"     every finished row is on the board; `--changed` measures the rest")
        return LIMIT_EXIT
    return 0 if len(results) + len(held) == len(work) else 1


if __name__ == "__main__":
    sys.exit(main())
