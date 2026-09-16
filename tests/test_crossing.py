"""A rule names what it crosses — the gate held to its rules. Standard library.

Each test builds the injector's green fixture, whose bindings carry boundary
rows for the store and the clock, adds a @crosses: tag to one of its rules, and
reads what trace.py says. See specs/changes/0053.
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
SECOND_EXAMPLE = (
    "\n    Example: the store refusing\n"
    "      Given the store rejecting the write\n"
    "      When they save\n"
    "      Then they are told it did not save\n"
)


def trace(root: Path) -> tuple[int, str]:
    result = subprocess.run([sys.executable, str(TRACE), str(root)], capture_output=True, text=True)
    return result.returncode, result.stdout + result.stderr


class Fixture(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp(prefix="crossing-"))
        inject.build(self.root)
        self.addCleanup(shutil.rmtree, self.root, ignore_errors=True)
        self.core = self.root / "specs" / "features" / "core" / "core.feature"

    def tag(self, crossing: str) -> None:
        self.core.write_text(self.core.read_text().replace("  @rule:one\n", f"  @rule:one {crossing}\n", 1))


class NamesARow(Fixture):
    @rule("a-crossing-names-a-row")
    def test_a_crossing_to_a_boundary_with_a_row_is_read_and_nothing_is_reported(self):
        # store is a boundary row the fixture bindings carry; give it a second
        # example so the count warning does not fire and only the row check speaks.
        self.core.write_text(self.core.read_text().replace(
            "      Then the thing is there\n", "      Then the thing is there\n" + SECOND_EXAMPLE, 1))
        self.tag("@crosses:store")
        code, out = trace(self.root)
        self.assertEqual(code, 0, out)
        self.assertNotIn("no row for", out)

    @rule("a-crossing-names-a-row")
    def test_a_crossing_to_a_boundary_nobody_wrote_down_fails_naming_both(self):
        self.tag("@crosses:stripe")
        code, out = trace(self.root)
        self.assertEqual(code, 1, out)
        self.assertIn("@rule:one", out)
        self.assertIn("stripe", out)
        self.assertIn("no row for", out)

    @rule("a-crossing-names-a-row")
    def test_a_rule_that_crosses_nothing_is_asked_nothing(self):
        code, out = trace(self.root)
        self.assertEqual(code, 0, out)
        self.assertNotIn("crosses", out)


class BoundaryMisbehaving(Fixture):
    @rule("a-crossing-has-its-boundary-misbehaving")
    def test_a_crossing_with_a_single_example_warns(self):
        self.tag("@crosses:store")  # rule one has one example
        code, out = trace(self.root)
        self.assertEqual(code, 0, out)
        self.assertIn("⚠", out)
        self.assertIn("@rule:one", out)
        self.assertIn("boundary misbehaving", out)

    @rule("a-crossing-has-its-boundary-misbehaving")
    def test_a_crossing_with_the_boundary_misbehaving_beside_it_does_not_warn(self):
        self.core.write_text(self.core.read_text().replace(
            "      Then the thing is there\n", "      Then the thing is there\n" + SECOND_EXAMPLE, 1))
        self.tag("@crosses:store")
        code, out = trace(self.root)
        self.assertEqual(code, 0, out)
        self.assertNotIn("specced the demo", out)


if __name__ == "__main__":
    unittest.main()
