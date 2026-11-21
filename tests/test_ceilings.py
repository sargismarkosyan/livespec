"""A part that only grows is held to the ceiling the bindings name. Standard library.

Each test builds the injector's green fixture, whose bindings carry a Ceilings
row naming `specs/` and `tests/`, changes one thing, and reads what trace.py
says. See specs/changes/0085.
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


class APartPastItsCeiling(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp(prefix="ceilings-"))
        inject.build(self.root)
        self.addCleanup(shutil.rmtree, self.root, ignore_errors=True)
        self.bindings = self.root / "specs" / "setup" / "README.md"

    def trace(self) -> tuple[int, str]:
        result = subprocess.run([sys.executable, str(TRACE), str(self.root)], capture_output=True, text=True)
        return result.returncode, result.stdout + result.stderr

    def set_row(self, row: str) -> None:
        text = self.bindings.read_text()
        self.assertIn(inject.ROW_CEILINGS, text)
        self.bindings.write_text(text.replace(inject.ROW_CEILINGS + "\n", row))

    @rule("a-part-past-its-ceiling-fails")
    def test_every_part_within_its_ceiling_says_nothing(self):
        code, out = self.trace()
        self.assertEqual(code, 0, out)
        self.assertNotIn("Ceilings", out)

    @rule("a-part-past-its-ceiling-fails")
    def test_a_part_past_its_ceiling_fails_naming_the_part_its_size_and_the_ceiling(self):
        self.set_row("| **Ceilings** | `tests/` 1,000 lines · `specs/` 10 lines |\n")
        code, out = self.trace()
        self.assertEqual(code, 1, out)
        line = next(line for line in out.splitlines() if "against a ceiling of 10 " in line)
        self.assertIn("specs/", line)
        self.assertRegex(line, r"is [\d,]+ lines")
        self.assertIn("raise the number in this change with the reason beside it", line)
        self.assertNotIn("tests/: is", out)

    @rule("a-part-past-its-ceiling-fails")
    def test_no_ceilings_row_fails(self):
        self.set_row("")
        code, out = self.trace()
        self.assertEqual(code, 1, out)
        self.assertIn("carries no Ceilings row", out)
        self.assertIn("a number nobody wrote is not a pass", out)


if __name__ == "__main__":
    unittest.main()
