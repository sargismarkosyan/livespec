"""The shipped prose, held to working under either host. Standard library.

livespec is loaded by Claude Code, as a plugin, and by Pi, as a package. Pi has
no plugin namespace, so a skill is typed `/skill:<name>` there rather than
`/livespec:<name>`, and it sets no `$CLAUDE_PLUGIN_ROOT`. These tests read what
ships — every skill, the method, the templates and the README — for the two
places a sentence can work under one host and silently not under the other.
See specs/changes/0080.
"""

from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from rulelib import rule  # noqa: E402

SHIPPED = sorted(
    [*ROOT.glob("skills/*/SKILL.md"), *ROOT.glob("method/*.md"), *ROOT.glob("templates/*"), ROOT / "README.md"]
)
PLUGIN_ROOT_PATH = re.compile(r"\$\{?CLAUDE_PLUGIN_ROOT\}?/")
CLAUDE_CODE_FORM = re.compile(r"/livespec:([a-z][a-z-]*|<name>)")


def paragraphs(path: Path) -> list[tuple[int, str]]:
    """Each blank-line-separated block, with the line it starts on."""
    blocks: list[tuple[int, str]] = []
    start, lines = 1, []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if line.strip():
            if not lines:
                start = number
            lines.append(line)
        elif lines:
            blocks.append((start, "\n".join(lines)))
            lines = []
    if lines:
        blocks.append((start, "\n".join(lines)))
    return blocks


@rule("a-skill-names-both-hosts-where-they-differ")
class EitherHost(unittest.TestCase):
    def test_the_prose_reads_files_to_scan(self):
        self.assertGreaterEqual(len([p for p in SHIPPED if p.name == "SKILL.md"]), 8, "the scan found no skills to read")

    def test_no_path_is_built_on_a_variable_only_claude_code_sets(self):
        found = [
            f"{path.relative_to(ROOT)}:{number}"
            for path in SHIPPED if path.is_file()
            for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1)
            if PLUGIN_ROOT_PATH.search(line)
        ]
        self.assertEqual(found, [], "a tool reached through $CLAUDE_PLUGIN_ROOT, which Pi never sets — use <plugin root>, "
                                   "two directories up from the skill file")

    def test_every_command_to_type_names_pis_form_beside_claude_codes(self):
        missing = []
        for path in SHIPPED:
            if not path.is_file():
                continue
            for start, block in paragraphs(path):
                for name in sorted(set(CLAUDE_CODE_FORM.findall(block))):
                    if f"/skill:{name}" not in block:
                        missing.append(f"{path.relative_to(ROOT)}:{start} /livespec:{name} without /skill:{name}")
        self.assertEqual(missing, [])


if __name__ == "__main__":
    unittest.main()
