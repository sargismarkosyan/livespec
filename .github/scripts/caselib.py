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
# what prompt.md cannot (scaffolds, transcript replay); when both exist the
# CLI merges them, and so do we — tags from either count as claimed.
CASE_FILES = ("case.yaml", "prompt.md")

def frontmatter(path: Path) -> tuple[dict[str, str], str]:
    """Read a leading --- block. Returns (fields, body).

    A flat key: value reader, which is all a prompt.md or a grader has. List
    values arrive either inline (`tags: [a, b]`) or as following `- ` lines;
    both come back as the raw string for `tag_values` to split.
    """
    text = path.read_text()
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text
    try:
        end = lines.index("---", 1)
    except ValueError:
        return {}, text
    fields: dict[str, str] = {}
    key = None
    for line in lines[1:end]:
        match = re.match(r"^([A-Za-z][\w-]*):\s*(.*)$", line)
        if match:
            key = match.group(1)
            fields[key] = match.group(2).strip()
        elif key and line.strip().startswith("-"):
            fields[key] += " " + line.strip().lstrip("- ").strip()
        elif key and line.startswith((" ", "\t")):
            fields[key] += " " + line.strip()
    return fields, "\n".join(lines[end + 1 :])


def tag_values(raw: str) -> list[str]:
    """Split a tags: value, inline-list or block-list, into bare tags."""
    return [t for t in re.split(r"[\s,\[\]\"']+", raw or "") if t]


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
        for source in sources:
            fields, _ = frontmatter(source)
            tags += tag_values(fields.get("tags", ""))
            allowed_tools += tag_values(fields.get("allowed_tools", ""))
            if fields.get("runs", "").strip().isdigit():
                runs = int(fields["runs"].strip())
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
