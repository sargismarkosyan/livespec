#!/usr/bin/env python3
"""Repository checks for the livespec plugin.

Deterministic, dependency-free, and offline. `claude plugin validate` covers the
manifest schemas; this covers what only this repository knows about itself.

Run: python3 .github/scripts/checks.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# Always-on context is the one budget every session pays. Each skill's name and
# description load whether or not it fires; the bodies do not.
DESCRIPTION_MAX = 1024
ALWAYS_ON_BUDGET_CHARS = 5000

NUMBER_WORDS = {
    1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six",
    7: "seven", 8: "eight", 9: "nine", 10: "ten", 11: "eleven", 12: "twelve",
}

failures: list[str] = []
notes: list[str] = []


def fail(where: str, message: str) -> None:
    failures.append(f"{where}: {message}")


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def frontmatter(path: Path) -> dict[str, str] | None:
    """Read the leading --- block. Flat string keys only, which is all a SKILL.md has."""
    lines = path.read_text().splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    try:
        end = lines.index("---", 1)
    except ValueError:
        return None
    fields: dict[str, str] = {}
    key = None
    for line in lines[1:end]:
        match = re.match(r"^([A-Za-z][\w-]*):\s*(.*)$", line)
        if match:
            key = match.group(1)
            fields[key] = match.group(2).strip()
        elif key and line.startswith((" ", "\t")):
            fields[key] += " " + line.strip()
    return fields


def markdown_files() -> list[Path]:
    return sorted(p for p in ROOT.rglob("*.md") if ".git" not in p.parts)


# --- 1. manifests agree with each other ------------------------------------

plugin_json = ROOT / ".claude-plugin" / "plugin.json"
marketplace_json = ROOT / ".claude-plugin" / "marketplace.json"

plugin: dict = {}
try:
    plugin = json.loads(plugin_json.read_text())
except Exception as exc:  # noqa: BLE001 - report, do not raise
    fail(rel(plugin_json), f"does not parse: {exc}")

try:
    marketplace = json.loads(marketplace_json.read_text())
except Exception as exc:  # noqa: BLE001
    fail(rel(marketplace_json), f"does not parse: {exc}")
    marketplace = {"plugins": []}

entries = [e for e in marketplace.get("plugins", []) if e.get("name") == plugin.get("name")]
if not entries:
    fail(
        rel(marketplace_json),
        f"has no entry named {plugin.get('name')!r}; the marketplace and the plugin must agree",
    )
for entry in entries:
    # plugin.json always wins, silently. A version here can only mask one there.
    if "version" in entry:
        fail(
            rel(marketplace_json),
            "the plugin entry sets 'version'; plugin.json is the authority and "
            "always wins, so this can only go stale. Remove it.",
        )

for field in ("version", "description", "license", "repository"):
    if not plugin.get(field):
        fail(rel(plugin_json), f"missing {field!r}")

# --- 2. skills load, and their frontmatter is honest ------------------------

skill_files = sorted((ROOT / "skills").glob("*/SKILL.md"))
if not skill_files:
    fail("skills/", "no SKILL.md found")

always_on_chars = 0
for skill in skill_files:
    where = rel(skill)
    fields = frontmatter(skill)
    if fields is None:
        fail(where, "no YAML frontmatter block")
        continue
    name = fields.get("name", "")
    description = fields.get("description", "")
    if name != skill.parent.name:
        fail(where, f"frontmatter name {name!r} does not match its directory {skill.parent.name!r}")
    if not description:
        fail(where, "no description; it is the only thing the model sees before firing")
    elif len(description) > DESCRIPTION_MAX:
        fail(where, f"description is {len(description)} chars (max {DESCRIPTION_MAX})")
    always_on_chars += len(name) + len(description)

if always_on_chars > ALWAYS_ON_BUDGET_CHARS:
    fail(
        "skills/",
        f"always-on cost is {always_on_chars} chars across {len(skill_files)} skills "
        f"(budget {ALWAYS_ON_BUDGET_CHARS}). Every session pays this whether or not a skill fires.",
    )
else:
    notes.append(
        f"always-on cost: {always_on_chars} chars across {len(skill_files)} skills "
        f"(budget {ALWAYS_ON_BUDGET_CHARS})"
    )

# --- 3. the skill count is stated consistently ------------------------------

count = len(skill_files)
word = NUMBER_WORDS.get(count, str(count))
stated = re.compile(r"\b(" + "|".join(NUMBER_WORDS.values()) + r")\s+skills\b", re.IGNORECASE)

for path in [ROOT / "README.md", ROOT / "method" / "README.md", plugin_json]:
    if not path.exists():
        continue
    for match in stated.finditer(path.read_text()):
        if match.group(1).lower() != word:
            fail(
                rel(path),
                f"says {match.group(0)!r} but skills/ holds {count} ({word})",
            )

# --- 4. relative links resolve ---------------------------------------------

# templates/ is written to be copied into a consuming repository's specs/, so its
# relative links resolve there rather than here. Everything else must resolve now.
LINK = re.compile(r"\[[^\]]*\]\((?!https?:|#|mailto:)([^)\s]+)\)")

linked: set[Path] = set()

for path in markdown_files():
    text = path.read_text()
    for target in LINK.findall(text):
        bare = target.split("#", 1)[0]
        if not bare:
            continue
        resolved = (path.parent / bare).resolve()
        if path.is_relative_to(ROOT / "templates"):
            continue
        if not resolved.exists():
            fail(rel(path), f"link {target!r} points at nothing")
        else:
            linked.add(resolved)

# --- 5. payload nobody points at is payload nobody reads --------------------

# method/, templates/ and tools/ are not plugin components. Claude Code never
# loads them; they are reachable only because a SKILL.md or a method doc names
# them. One that nothing names ships to every user and is read by no one.
# A markdown link counts, and so does a bare path in prose or a shell line
# (tools/clip.py is invoked, not linked).
corpus = "\n".join(p.read_text() for p in markdown_files())

for directory in ("method", "templates", "tools"):
    for payload in sorted((ROOT / directory).rglob("*")):
        if not payload.is_file() or payload.name == "README.md":
            continue
        if payload.resolve() in linked or rel(payload) in corpus:
            continue
        fail(rel(payload), "is referenced by no skill, method doc, or README — it ships to every user unread")

# --- report ----------------------------------------------------------------

for note in notes:
    print(f"  {note}")

if failures:
    print(f"\n{len(failures)} problem(s):\n", file=sys.stderr)
    for problem in failures:
        print(f"  ✘ {problem}", file=sys.stderr)
    sys.exit(1)

print(f"\n✔ checks passed ({count} skills)")
