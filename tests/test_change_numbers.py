"""Two change specs never share a number — the gate held to its rule. Standard library.

Each test builds the injector's green fixture, which holds one change spec,
adds another beside it, and reads what trace.py says. See specs/changes/0078.
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


def trace(root: Path) -> tuple[int, str]:
    result = subprocess.run([sys.executable, str(TRACE), str(root)], capture_output=True, text=True)
    return result.returncode, result.stdout + result.stderr


class OneNumberOneChange(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp(prefix="numbers-"))
        inject.build(self.root)
        self.addCleanup(shutil.rmtree, self.root, ignore_errors=True)
        self.changes = self.root / "specs" / "changes"

    @rule("two-change-specs-never-share-a-number")
    def test_two_trees_that_took_the_same_number_fail_naming_both(self):
        (self.changes / "0001-a-quieter-log.md").write_text("# Spec 0001: a quieter log\n")
        code, out = trace(self.root)
        self.assertEqual(code, 1, out)
        self.assertIn("share the number 0001", out)
        self.assertIn("0001-first.md", out)
        self.assertIn("0001-a-quieter-log.md", out)
        self.assertIn("renumber the one that has not merged yet", out)

    @rule("two-change-specs-never-share-a-number")
    def test_a_gap_left_by_a_closed_pull_request_passes_and_is_not_mentioned(self):
        (self.changes / "0003-third.md").write_text("# Spec 0003: the third\n")
        code, out = trace(self.root)
        self.assertEqual(code, 0, out)
        self.assertNotIn("0002", out)
