"""The context-file checks in trace.py, held to their rules. Standard library.

Each test builds the injector's green fixture in a temporary directory — the
same one every fault is injected into — changes CLAUDE.md or the bindings the
way a real change would, and runs trace.py against it. See specs/changes/0048.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".github" / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import inject  # noqa: E402
from rulelib import rule  # noqa: E402

TRACE = ROOT / ".github" / "scripts" / "trace.py"
FIXTURE_LINES = len(inject.CONTEXT_FILE.splitlines())


def fixture() -> Path:
    root = Path(tempfile.mkdtemp(prefix="context-file-"))
    inject.build(root)
    return root


def trace(root: Path) -> tuple[int, str]:
    result = subprocess.run([sys.executable, str(TRACE), str(root)], capture_output=True, text=True)
    return result.returncode, result.stdout + result.stderr


def set_ceiling(root: Path, lines: int) -> None:
    bindings = root / "specs" / "setup" / "README.md"
    bindings.write_text(bindings.read_text().replace(f"{FIXTURE_LINES} lines", f"{lines} lines"))


class Fixture(unittest.TestCase):
    def setUp(self):
        self.root = fixture()
        self.addCleanup(shutil.rmtree, self.root, ignore_errors=True)
        self.context = self.root / "CLAUDE.md"


class TheCeiling(Fixture):
    @rule("a-context-file-past-its-ceiling-fails-the-build")
    def test_a_file_grown_past_the_number_fails_naming_both(self):
        self.context.write_text(inject.CONTEXT_FILE + "\nOne more line than the bindings allow.\n")
        code, out = trace(self.root)
        self.assertEqual(code, 1, out)
        self.assertIn(f"against a ceiling of {FIXTURE_LINES}", out)
        self.assertIn(f"is {FIXTURE_LINES + 2} lines", out)

    @rule("a-context-file-past-its-ceiling-fails-the-build")
    def test_the_number_raised_in_the_same_change_passes(self):
        grown = inject.CONTEXT_FILE + "\nOne more line, and the room for it.\n"
        self.context.write_text(grown)
        set_ceiling(self.root, len(grown.splitlines()))
        code, out = trace(self.root)
        self.assertEqual(code, 0, out)

    @rule("a-context-file-past-its-ceiling-fails-the-build")
    def test_a_ceiling_above_the_readers_limit_fails_naming_both(self):
        set_ceiling(self.root, 250)
        code, out = trace(self.root)
        self.assertEqual(code, 1, out)
        self.assertIn("250", out)
        self.assertIn("200", out)
        self.assertNotIn("against a ceiling of", out, "the ceiling is refused before the file's size is read")

    @rule("a-context-file-past-its-ceiling-fails-the-build")
    def test_a_number_nobody_wrote_is_not_a_pass(self):
        bindings = self.root / "specs" / "setup" / "README.md"
        bindings.write_text(bindings.read_text().replace(inject.ROW_CEILING + "\n", ""))
        code, out = trace(self.root)
        self.assertEqual(code, 1, out)
        self.assertIn("names no CLAUDE.md ceiling", out)


class TheShape(Fixture):
    @rule("a-context-file-without-its-shape-fails-the-build")
    def test_three_lines_fail_naming_the_three_absences(self):
        self.context.write_text("# fixture\n\nA thing.\n")
        code, out = trace(self.root)
        self.assertEqual(code, 1, out)
        for phrase in ("no numbered list", "no fenced block", "does not link to specs/setup/README.md"):
            self.assertIn(phrase, out)
        self.assertNotIn("against a ceiling", out, "three lines are under the ceiling; that is not what fails them")

    @rule("a-context-file-without-its-shape-fails-the-build")
    def test_a_loop_of_nine_steps_fails_naming_the_length(self):
        nine = inject.context_file(9)
        self.context.write_text(nine)
        set_ceiling(self.root, len(nine.splitlines()))
        code, out = trace(self.root)
        self.assertEqual(code, 1, out)
        self.assertIn("9 steps", out)
        self.assertIn("at most 8", out)

    @rule("a-context-file-without-its-shape-fails-the-build")
    def test_a_loop_of_eight_steps_passes(self):
        eight = inject.context_file(8)
        self.context.write_text(eight)
        set_ceiling(self.root, len(eight.splitlines()))
        code, out = trace(self.root)
        self.assertEqual(code, 0, out)

    @rule("a-context-file-without-its-shape-fails-the-build")
    def test_no_file_at_the_root_fails(self):
        self.context.unlink()
        code, out = trace(self.root)
        self.assertEqual(code, 1, out)
        self.assertIn("no CLAUDE.md at the root", out)


class WhatOnlyAMindCanRead(Fixture):
    @rule("what-only-a-mind-can-read-is-left-to-the-sitting")
    def test_a_stale_path_and_a_copied_paragraph_pass_the_gate(self):
        text = inject.CONTEXT_FILE.replace(
            "A synthetic repository, not an application.",
            "A synthetic repository, not an application. The code is the source of truth and the spec "
            "is where the context lives — see [the old guide](docs/guide.md), which moved last spring.",
        )
        self.context.write_text(text)
        code, out = trace(self.root)
        self.assertEqual(code, 0, out)
        self.assertNotIn("docs/guide.md", out)
        self.assertNotIn("source of truth", out)

    @rule("what-only-a-mind-can-read-is-left-to-the-sitting")
    def test_a_second_short_list_is_not_mistaken_for_the_loop(self):
        text = inject.CONTEXT_FILE.replace(
            "## Commands\n", "## Two things\n\n1. The first thing.\n2. The second thing.\n\n## Commands\n"
        )
        self.context.write_text(text)
        set_ceiling(self.root, len(text.splitlines()))
        code, out = trace(self.root)
        self.assertEqual(code, 0, out)


if __name__ == "__main__":
    unittest.main()
