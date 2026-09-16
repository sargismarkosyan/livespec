"""A test that did not run claims nothing — the gates held to it. Standard library.

Each test builds the injector's green fixture in a temporary directory, changes
its one test the way a change here would, and runs the gate that must notice:
trace.py for a marker that empties a claim, tests.py for a runner that saw
fewer tests than the tree holds. See specs/changes/0051.
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
TESTS = ROOT / ".github" / "scripts" / "tests.py"

PREAMBLE = (
    "import sys\nimport unittest\nfrom pathlib import Path\n\n"
    "sys.path.insert(0, str(Path(__file__).resolve().parent))\n"
    "from rulelib import rule  # noqa: E402\n\n\n"
)


def run(gate: Path, root: Path) -> tuple[int, str]:
    result = subprocess.run([sys.executable, str(gate), str(root)], capture_output=True, text=True)
    return result.returncode, result.stdout + result.stderr


class Fixture(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp(prefix="what-ran-"))
        inject.build(self.root)
        self.addCleanup(shutil.rmtree, self.root, ignore_errors=True)
        self.thing = self.root / "tests" / "test_thing.py"

    def mark(self, marker: str) -> None:
        self.thing.write_text(self.thing.read_text().replace('    @rule("two")\n', f"    {marker}\n    @rule(\"two\")\n", 1))


class TheMarker(Fixture):
    @rule("a-test-that-did-not-run-claims-nothing")
    def test_a_skipped_rule_bound_test_fails_naming_test_marker_and_rule(self):
        self.mark('@unittest.skip("not today")')
        code, out = run(TRACE, self.root)
        self.assertEqual(code, 1, out)
        for phrase in ("Thing.test_nothing_happens", "@skip", "@rule:two", "claims nothing"):
            self.assertIn(phrase, out)

    @rule("a-test-that-did-not-run-claims-nothing")
    def test_an_expected_failure_is_the_same(self):
        self.mark("@unittest.expectedFailure")
        code, out = run(TRACE, self.root)
        self.assertEqual(code, 1, out)
        self.assertIn("@expectedFailure", out)
        self.assertIn("claims nothing", out)

    @rule("a-test-that-did-not-run-claims-nothing")
    def test_a_marker_on_the_class_empties_every_claim_in_it(self):
        self.thing.write_text(self.thing.read_text().replace("class Thing(unittest.TestCase):", '@unittest.skip("the whole class")\nclass Thing(unittest.TestCase):', 1))
        code, out = run(TRACE, self.root)
        self.assertEqual(code, 1, out)
        self.assertIn("claims nothing", out)

    @rule("a-test-that-did-not-run-claims-nothing")
    def test_a_skipped_test_that_claims_no_rule_is_not_the_gates_business(self):
        (self.root / "tests" / "test_unit.py").write_text(
            PREAMBLE + "class Unit(unittest.TestCase):\n"
            '    @unittest.skip("a unit test, and skipped")\n'
            "    def test_something_internal(self):\n"
            "        self.assertTrue(True)\n"
        )
        code, out = run(TRACE, self.root)
        self.assertEqual(code, 0, out)
        self.assertNotIn("claims nothing", out)


class TheCount(Fixture):
    @rule("fewer-ran-than-exist-is-a-failure")
    def test_a_test_the_runner_never_discovers_fails_with_both_numbers(self):
        (self.root / "tests" / "test_more.py").write_text(
            PREAMBLE + "class More:  # not a TestCase: the runner never collects it\n"
            '    @rule("one")\n'
            "    def test_the_thing_is_true(self):\n"
            "        assert True\n"
        )
        code, out = run(TESTS, self.root)
        self.assertEqual(code, 1, out)
        self.assertIn("the tree holds 2 test(s) and the runner ran 1", out)

    @rule("fewer-ran-than-exist-is-a-failure")
    def test_a_green_summary_line_does_not_stand_in_for_the_count(self):
        (self.root / "tests" / "test_more.py").write_text(
            PREAMBLE + "class More:\n"
            '    @rule("one")\n'
            "    def test_the_thing_is_true(self):\n"
            "        assert True\n"
        )
        code, out = run(TESTS, self.root)
        self.assertEqual(code, 1, out)
        self.assertIn("OK", subprocess.run(
            [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-t", "."],
            cwd=self.root, capture_output=True, text=True).stderr,
            "the runner itself reads green; that is the point")

    @rule("fewer-ran-than-exist-is-a-failure")
    def test_more_ran_than_the_tree_holds_is_not_a_failure(self):
        (self.root / "tests" / "test_inherit.py").write_text(
            PREAMBLE + "class Base(unittest.TestCase):\n"
            '    @rule("one")\n'
            "    def test_inherited(self):\n"
            "        self.assertTrue(True)\n\n\n"
            "class Child(Base):\n"
            "    pass\n"
        )
        code, out = run(TESTS, self.root)
        self.assertEqual(code, 0, out)
        self.assertIn("3 run of 2 held", out)


if __name__ == "__main__":
    unittest.main()
