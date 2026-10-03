#!/usr/bin/env python3
"""Reading eval cases — shared by the traceability gate and the eval-suite gate.

Both gates ask the same question of `evals/`: which cases are there, what does
each one claim, and what grades it. This is that reader, in one place, so the two
gates cannot disagree about what a case is.

Not a gate itself. It reports what it finds and leaves the judging to the caller.
"""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

# A case is a directory holding a prompt and its graders. `case.yaml` carries
# what prompt.md cannot — a scaffold, the shell it lends, the binaries its
# fixture requires; when both exist the CLI merges them, and so do we — tags
# from either count as claimed. A `person.md` beside them is the human the
# sitting would have had: what they know, and how many replies they give (0058).
CASE_FILES = ("case.yaml", "prompt.md")
PERSON_FILE = "person.md"
DEFAULT_REPLIES = 2

def _flat_fields(lines: list[str]) -> dict[str, str]:
    """A flat key: value reader, which is all a case file or a grader has.

    List values arrive either inline (`tags: [a, b]`) or as following `- `
    lines; both come back as the raw string for `tag_values` to split.
    """
    fields: dict[str, str] = {}
    key = None
    for line in lines:
        match = re.match(r"^([A-Za-z][\w-]*):\s*(.*)$", line)
        if match:
            key = match.group(1)
            fields[key] = match.group(2).strip()
        elif key and line.strip().startswith("-"):
            fields[key] += " " + line.strip().lstrip("- ").strip()
        elif key and line.startswith((" ", "\t")):
            fields[key] += " " + line.strip()
    return fields


def frontmatter(path: Path) -> tuple[dict[str, str], str]:
    """Read a leading --- block. Returns (fields, body)."""
    text = path.read_text()
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text
    try:
        end = lines.index("---", 1)
    except ValueError:
        return {}, text
    return _flat_fields(lines[1:end]), "\n".join(lines[end + 1 :])


def fields_of(source: Path) -> dict[str, str]:
    """The fields of one case source: a prompt.md keeps them fenced in
    frontmatter; a case.yaml is nothing but fields, so the whole file reads."""
    if source.suffix in (".yaml", ".yml"):
        return _flat_fields(source.read_text().splitlines())
    return frontmatter(source)[0]


def tag_values(raw: str) -> list[str]:
    """Split a tags: value, inline-list or block-list, into bare tags."""
    return [t for t in re.split(r"[\s,\[\]\"']+", raw or "") if t]


def list_values(raw: str) -> list[str]:
    """Split a list whose items may hold spaces — `shell: [python3, claude plugin]` —
    on commas only, brackets and quotes stripped."""
    return [item.strip().strip("\"'") for item in (raw or "").strip().strip("[]").split(",") if item.strip().strip("\"'")]


def cases(root: Path) -> list[dict]:
    """Every eval case under root/evals, in name order."""
    found: list[dict] = []
    evals = root / "evals"
    if not evals.is_dir():
        return found
    for directory in sorted(p for p in evals.iterdir() if p.is_dir()):
        if directory.name == "results":
            continue
        sources = [directory / name for name in CASE_FILES if (directory / name).exists()]
        if not sources:
            continue
        tags: list[str] = []
        allowed_tools: list[str] = []
        runs: int | None = None
        scaffold: Path | None = None
        workspace: str | None = None
        shell: list[str] = []
        requires: list[str] = []
        for source in sources:
            fields = fields_of(source)
            tags += tag_values(fields.get("tags", ""))
            allowed_tools += tag_values(fields.get("allowed_tools", ""))
            if fields.get("runs", "").strip().isdigit():
                runs = int(fields["runs"].strip())
            if fields.get("scaffold_script", "").strip():
                scaffold = directory / fields["scaffold_script"].strip()
            if fields.get("workspace", "").strip():
                workspace = fields["workspace"].strip()
            shell += list_values(fields.get("shell", ""))
            requires += list_values(fields.get("requires", ""))
        # A shell is a Bash grant, confined to the prefixes named: the case asks
        # for the tool by naming what it may run, and the grant check reads it.
        if shell and "Bash" not in allowed_tools:
            allowed_tools.append("Bash")
        # The person: the sheet is the body, the rounds the frontmatter.
        person_file = directory / PERSON_FILE
        person: str | None = None
        replies = 0
        if person_file.exists():
            person_fields, sheet = frontmatter(person_file)
            person = sheet.strip()
            replies = (int(person_fields["replies"].strip())
                       if person_fields.get("replies", "").strip().isdigit() else DEFAULT_REPLIES)
        graders = []
        for grader in sorted((directory / "graders").glob("*.md")):
            fields, body = frontmatter(grader)
            # The rule this grader tests — `rule: <id>`, or `rules: [a, b]` where
            # one verdict holds two — so a claim on the case can be held to a
            # grader that fails when the rule is broken (0066). A grader naming
            # none is a guard, never coverage.
            rules = tag_values(fields.get("rules", "") or fields.get("rule", ""))
            graders.append({"path": grader, "type": fields.get("type", ""), "body": body.strip(), "fields": fields,
                            "rules": rules,
                            "indicator": fields.get("type", "") == "tool_used" and not fields.get("max", "").strip().isdigit()})
        found.append(
            {
                "name": directory.name,
                "dir": directory,
                "sources": sources,
                "tags": tags,
                # The CLI's default when a case does not say. Stated here rather
                # than assumed, because the floor is a minimum on the real value.
                "allowed_tools": allowed_tools,
                "runs": 3 if runs is None else runs,
                "scaffold": scaffold,
                # The world the case runs in, when it is not a scaffold: `empty — <why>`.
                # Read here so the suite gate and the runner agree on what was declared.
                "workspace": workspace,
                # What the sitting has that a turn does not (0058): the human's
                # sheet and their rounds; the shell prefixes the case lends and
                # the binaries its fixture cannot run without.
                "person_file": person_file if person is not None else None,
                "person": person,
                "replies": replies,
                "shell": shell,
                "requires": requires,
                "graders": graders,
                "claims": {
                    "rules": [t.split(":", 1)[1] for t in tags if t.startswith("rule:")],
                    "workflows": [t.split(":", 1)[1] for t in tags if t.startswith("workflow:")],
                    "skills": [t.split(":", 1)[1] for t in tags if t.startswith("skill:")],
                },
                "negative": "should-not-fire" in tags,
            }
        )
    return found


def rule_text(root: Path, rule_id: str) -> str:
    """The block of one rule: from its @rule: tag line to the next rule's.

    Sliced from the feature file rather than parsed, because what a measurement
    covers is the *text* — a reworded example is a changed rule even when the
    structure is identical.
    """
    for feature in sorted((root / "specs" / "features").rglob("*.feature")):
        lines = feature.read_text().splitlines()
        start = None
        for index, line in enumerate(lines):
            if start is None:
                if re.search(rf"@rule:{re.escape(rule_id)}\b", line):
                    start = index
            elif re.match(r"\s*@rule:", line):
                return "\n".join(lines[start:index])
        if start is not None:
            return "\n".join(lines[start:])
    return ""


def _is_grading(path: Path, case: dict) -> bool:
    """Whether this file is read by the grader rather than by the session.

    The session is handed a prompt, a workspace a scaffold laid down and a
    person to answer it. It is never shown a rubric. So the graders, and the
    scripts a command grader runs, decide what a verdict says and decide
    nothing at all about what the session did.
    """
    relative = path.relative_to(case["dir"]).as_posix()
    return relative.startswith("graders/") or relative.startswith("check_")


def grader_inputs(case: dict) -> str:
    """Hash of what decides a verdict, given a session that already happened.

    Kept apart from `measurement_inputs` because the two answer different
    questions. Edit a rubric and every session in the run directory is still
    a faithful record of what the skill did — nothing it saw has changed — so
    what is owed is a judge call over transcripts that already exist, not a
    sitting run again. That is the difference between a few cents and a few
    dollars, and it is the commonest edit anyone makes here: reading verdicts
    and sharpening the rubric is the whole calibration loop.
    """
    digest = hashlib.sha256()
    for path in sorted(p for p in case["dir"].rglob("*") if p.is_file() and _is_grading(p, case)):
        digest.update(path.relative_to(case["dir"]).as_posix().encode())
        digest.update(path.read_bytes())
    return digest.hexdigest()[:16]


def measurement_inputs(case: dict, root: Path, arm: str = "with") -> str:
    """Hash of what a measurement of this case, in this arm, measures.

    Three things can move under a number: the case's own files, the text of
    every rule it claims, and the body of every skill it holds. The first two
    move under both arms. **The third moves under one.** The bare arm runs
    `claude -p` with no `--plugin-dir`, so no skill body is in its context and
    no edit to one can change what it did — a skill rewritten from top to
    bottom leaves the bare arm measuring exactly what it measured before.

    That is why this takes an arm. `with` hashes all three; `without` hashes
    the first two. A skill edit then stales half a row instead of a whole one,
    and the commonest change in this repository costs half of what it did.
    What it does not do is let a stale baseline hide: change the prompt, the
    fixture, a grader or a rule and both arms go, because both saw those.

    Content-addressed — bytes only, never timestamps or git metadata — so two
    machines agree about staleness. Shared between the runner (which records
    it) and the board gate (which checks it) for the same reason this reader
    is shared: so the two cannot disagree about what a measurement is.
    """
    digest = hashlib.sha256()
    for path in sorted(p for p in case["dir"].rglob("*") if p.is_file() and not _is_grading(p, case)):
        digest.update(str(path.relative_to(case["dir"])).encode())
        digest.update(path.read_bytes())
    for rule in sorted(case["claims"]["rules"]):
        digest.update(f"rule:{rule}".encode())
        digest.update(rule_text(root, rule).encode())
    if arm == "with":
        for skill in sorted(case["claims"]["skills"]):
            digest.update(f"skill:{skill}".encode())
            skill_md = root / "skills" / skill / "SKILL.md"
            if skill_md.exists():
                digest.update(skill_md.read_bytes())
    return digest.hexdigest()[:16]


# The model both arms run on. The exact id rather than an alias, so that a new
# Sonnet is a line somebody moves here — and every row on the board goes stale
# the moment it moves — rather than a change nobody sees. The judge's model is
# a flag on the run, and the row records both. Held here, beside the floor, for
# the same reason: the runner, the suite gate and the board gate read one
# decision. See specs/changes/0057 and #130.
SESSION_MODEL = "claude-sonnet-5"

# The two files whose bytes decide what a session is and how it is graded. A
# change to either changes what a number means, so their fingerprint travels
# with every row and a mismatch stales it. run.py is orchestration and
# bookkeeping and is left out on purpose: a reworded refusal is not a new
# measurement.
HARNESS_FILES = ("evals/runner/provider.py", "evals/runner/asserts.py")


def harness_fingerprint(root: Path) -> str:
    """Content hash of the harness files, the way measurement_inputs hashes a case."""
    digest = hashlib.sha256()
    for relative in HARNESS_FILES:
        digest.update(relative.encode())
        path = root / relative
        if path.exists():
            digest.update(path.read_bytes())
    return digest.hexdigest()[:16]


def why_stale(entry: dict | None, case: dict, root: Path) -> list[str]:
    """Every reason a board entry no longer describes what it claims to measure.

    Empty means current. Three reasons, each named so the gate can say it in
    words: `inputs` — the case, a rule it claims or a skill it holds moved;
    `model` — it was made on a model other than the one the bindings name, or
    on one it never recorded; `harness` — provider.py or asserts.py changed
    since. Shared by the runner's --changed and the board gate, so the two
    cannot disagree about which rows a run is owed for.
    """
    if not isinstance(entry, dict):
        return ["never measured"]
    reasons: list[str] = []
    if stale_arms(entry, case, root):
        reasons.append("inputs")
    if "graders" in entry and entry.get("graders") != grader_inputs(case):
        reasons.append("graders")
    if entry.get("model") != SESSION_MODEL:
        reasons.append("model")
    if entry.get("harness") != harness_fingerprint(root):
        reasons.append("harness")
    return reasons


def stale_arms(entry: dict | None, case: dict, root: Path) -> list[str]:
    """Which arms of this row no longer describe what they measured.

    A row records a hash per arm. A row written before this existed carries
    one `inputs` hash and no `inputs_without` — and that hash covered all
    three things, so it is a superset of the bare arm's: if it still matches,
    the case files and the rules have not moved either, and both arms are
    current. If it does not match, an old row cannot say which of the three
    moved, so both arms go.
    """
    if not isinstance(entry, dict):
        return ["with", "without"]
    with_stale = entry.get("inputs") != measurement_inputs(case, root, "with")
    if "inputs_without" not in entry:
        return ["with", "without"] if with_stale else []
    stale = ["with"] if with_stale else []
    if entry.get("inputs_without") != measurement_inputs(case, root, "without"):
        stale.append("without")
    return stale


def is_current(entry: dict | None, case: dict, root: Path) -> bool:
    return not why_stale(entry, case, root)


# The floor a number has to clear before it is a measurement of anything. One
# run of an LLM grader is noise, and a suite that lets noise onto the board is
# measuring its own variance. Shared with the runner and the board gate for the
# same reason `measurement_inputs` is: three places deciding separately what
# counts as a measurement is how a pilot ends up wearing a measurement's clothes.
MIN_RUNS = 3


def is_measurement(entry: dict | None) -> bool:
    """Whether a board entry was produced by enough runs to be believed.

    Below the floor the number is still worth keeping — it is what the board has
    — but it is not coverage, it does not go into a mean, and it may not stand
    in for a measurement.
    """
    return isinstance(entry, dict) and isinstance(entry.get("runs"), int) and entry["runs"] >= MIN_RUNS


def replaces(prior: dict | None, runs: int) -> bool:
    """Whether a run of `runs` sessions may take `prior`'s row on the board.

    A run at or above the floor always may. Below it, a run may only fill a row
    that holds nothing or holds another number below the floor — it may never
    overwrite a measurement. That is not tidiness: an entry carries the inputs
    hash that clears the freshness gate, so a pilot written over a measurement
    both loses the number and turns the red that was asking for a real run
    green. Both halves happened on 2026-08-29 (issue #75).
    """
    return runs >= MIN_RUNS or not is_measurement(prior)


# --- the cheap tiers (0072) ----------------------------------------------------
#
# A sitting is the most faithful measurement this suite has and the one nobody
# can afford to keep fresh: a skill edit staled six cases and cost $9, a
# harness edit $200. So freshness is held one tier down, where a measurement is
# one call rather than a sitting, and each tier is staled only by what it can
# see:
#
#   route   one real turn with only the Skill tool: does the right skill fire,
#           or none. It sees every skill's frontmatter and the case's prompt
#           and world. It never sees a skill's body.
#   first   one reply to a snapshot — the world as already read, the skill's
#           body as already loaded, the prompt — judged by the case's own
#           rubrics, both arms. It sees what a sitting's first move sees.
#   review  one reading of a skill's body beside the rules the cases holding it
#           claim: is each rule still something the body tells the model to do.
#
# The sittings stay, as the canary pool: runnable, shown, never averaged when
# stale, and no longer what a commit owes. See specs/changes/0072.

TIERS = ("route", "first", "review")

# The file whose bytes decide what a tier's call is and how it is judged — the
# same job HARNESS_FILES does for the sittings, kept apart so an edit to one
# harness does not stale the other's rows.
TIER_HARNESS_FILES = ("evals/runner/tiers.py",)


def tier_harness_fingerprint(root: Path) -> str:
    digest = hashlib.sha256()
    for relative in TIER_HARNESS_FILES:
        digest.update(relative.encode())
        path = root / relative
        if path.exists():
            digest.update(path.read_bytes())
    return digest.hexdigest()[:16]


def skill_frontmatter(skill_md: Path) -> str:
    """The block the router reads: everything between the opening `---` and the
    closing one. The body is loaded only after a skill fires, so it is not here."""
    text = skill_md.read_text() if skill_md.exists() else ""
    if not text.startswith("---"):
        return ""
    end = text.find("\n---", 3)
    return text[: end + 4] if end != -1 else text


def _case_files_digest(case: dict, digest) -> None:
    for path in sorted(p for p in case["dir"].rglob("*") if p.is_file() and not _is_grading(p, case)):
        digest.update(str(path.relative_to(case["dir"])).encode())
        digest.update(path.read_bytes())


def route_inputs(case: dict, root: Path) -> str:
    """Hash of what a routing turn sees: the case's prompt and world, and the
    frontmatter of **every** skill — a description edit can move any prompt's
    routing, so it stales every routing row. A body edit stales none."""
    digest = hashlib.sha256()
    _case_files_digest(case, digest)
    for skill_md in sorted((root / "skills").glob("*/SKILL.md")):
        digest.update(f"skill:{skill_md.parent.name}".encode())
        digest.update(skill_frontmatter(skill_md).encode())
    return digest.hexdigest()[:16]


def skill_rules(skill: str, suite: list[dict]) -> list[str]:
    """The rules a skill answers for: every rule claimed by a case that holds it."""
    return sorted({rule for case in suite if skill in case["claims"]["skills"] for rule in case["claims"]["rules"]})


def review_inputs(skill: str, suite: list[dict], root: Path) -> str:
    """Hash of what a review reads: the skill's whole file and the text of every
    rule it answers for."""
    digest = hashlib.sha256()
    skill_md = root / "skills" / skill / "SKILL.md"
    if skill_md.exists():
        digest.update(skill_md.read_bytes())
    for rule in skill_rules(skill, suite):
        digest.update(f"rule:{rule}".encode())
        digest.update(rule_text(root, rule).encode())
    return digest.hexdigest()[:16]


def first_move_holds(case: dict) -> bool:
    """Whether a case has a first move to judge: it holds a skill, is not a
    should-not-fire case — the routing tier holds those — and has a rubric."""
    return (not case["negative"] and bool(case["claims"]["skills"])
            and any(g["type"] == "llm" and g["body"] for g in case["graders"]))


def tier_keys(tier: str, suite: list[dict], root: Path) -> list[str]:
    """What a tier owes a row for: every case to route, every case with a first
    move, every skill to review."""
    if tier == "route":
        return [case["name"] for case in suite]
    if tier == "first":
        return [case["name"] for case in suite if first_move_holds(case)]
    return sorted(p.parent.name for p in (root / "skills").glob("*/SKILL.md"))


def tier_stale_arms(entry: dict | None, case: dict, root: Path) -> list[str]:
    """The first-move tier's arms, staled as a sitting's are (0070): a skill
    edit moves the with-arm only; the bare arm never saw a skill body."""
    if not isinstance(entry, dict):
        return ["with", "without"]
    stale = []
    if entry.get("inputs") != measurement_inputs(case, root, "with"):
        stale.append("with")
    if entry.get("inputs_without") != measurement_inputs(case, root, "without"):
        stale.append("without")
    return stale


def tier_why_stale(tier: str, key: str, entry: dict | None, suite: list[dict], root: Path) -> list[str]:
    """Every reason a tier row no longer describes what it measured; empty is
    current. Shared by the tier runner's --changed and the board gate, so the
    two cannot disagree about which rows a run is owed for."""
    if not isinstance(entry, dict):
        return ["never measured"]
    reasons: list[str] = []
    if tier == "review":
        if entry.get("inputs") != review_inputs(key, suite, root):
            reasons.append("inputs")
    else:
        case = next((c for c in suite if c["name"] == key), None)
        if case is None:
            return ["gone"]
        if tier == "route":
            if entry.get("inputs") != route_inputs(case, root):
                reasons.append("inputs")
        else:
            if tier_stale_arms(entry, case, root):
                reasons.append("inputs")
            if entry.get("graders") != grader_inputs(case):
                reasons.append("graders")
        if entry.get("model") != SESSION_MODEL:
            reasons.append("model")
    if entry.get("harness") != tier_harness_fingerprint(root):
        reasons.append("harness")
    return reasons
