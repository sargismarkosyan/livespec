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
            graders.append({"path": grader, "type": fields.get("type", ""), "body": body.strip(), "fields": fields})
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


def measurement_inputs(case: dict, root: Path) -> str:
    """Hash of what a measurement of this case measures.

    Three things go in: the case's own files, the text of every rule it
    claims, and the body of every skill it holds. When any of them moves, a
    number measured before the move describes something that no longer exists.
    Content-addressed — bytes only, never timestamps or git metadata — so two
    machines agree about staleness.

    Shared between the runner (which records it) and the board gate (which
    checks it) for the same reason this reader is shared: so the two cannot
    disagree about what a measurement is.
    """
    digest = hashlib.sha256()
    for path in sorted(p for p in case["dir"].rglob("*") if p.is_file()):
        digest.update(str(path.relative_to(case["dir"])).encode())
        digest.update(path.read_bytes())
    for rule in sorted(case["claims"]["rules"]):
        digest.update(f"rule:{rule}".encode())
        digest.update(rule_text(root, rule).encode())
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
    if entry.get("inputs") != measurement_inputs(case, root):
        reasons.append("inputs")
    if entry.get("model") != SESSION_MODEL:
        reasons.append("model")
    if entry.get("harness") != harness_fingerprint(root):
        reasons.append("harness")
    return reasons


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
