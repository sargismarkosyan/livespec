#!/usr/bin/env python3
"""Reading eval cases — shared by the traceability gate and the eval-suite gate.

Both gates ask the same question of `evals/`: which cases are there, what does
each one claim, and what grades it. This is that reader, in one place, so the two
gates cannot disagree about what a case is.

Not a gate itself. It reports what it finds and leaves the judging to the caller.
"""

from __future__ import annotations

import re
from pathlib import Path

# A case is a directory holding a prompt and its graders. `case.yaml` carries
# what prompt.md cannot (scaffolds, transcript replay); when both exist the
# CLI merges them, and so do we — tags from either count as claimed.
CASE_FILES = ("case.yaml", "prompt.md")

# Cases that predate this repository's spec layer, exempt from having to claim a
# rule. Section 7 of the setup skill: existing tests do not get retrofitted with
# references to rules that do not exist yet.
#
# **This list may only shrink.** A case leaves it when a rule it answers to gets
# written; nothing is ever added. A pull request that grows it is claiming its
# new case predates today, which is false, and the diff makes that visible.
GRANDFATHERED = {
    "01-solution-shaped-request",
    "02-feedback-from-use",
    "03-persona-to-fit-feature",
    "04-workflow-for-orphan",
    "05-future-state-journey",
    "06-neg-commit-message",
    "07-neg-gherkin-question",
    "08-fix-it-while-recording",
    "09-neg-setup-not-self-started",
}


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
        runs: int | None = None
        for source in sources:
            fields, _ = frontmatter(source)
            tags += tag_values(fields.get("tags", ""))
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
                "runs": 3 if runs is None else runs,
                "graders": graders,
                "claims": {
                    "rules": [t.split(":", 1)[1] for t in tags if t.startswith("rule:")],
                    "workflows": [t.split(":", 1)[1] for t in tags if t.startswith("workflow:")],
                    "skills": [t.split(":", 1)[1] for t in tags if t.startswith("skill:")],
                },
                "negative": "should-not-fire" in tags,
                "grandfathered": directory.name in GRANDFATHERED,
            }
        )
    return found
