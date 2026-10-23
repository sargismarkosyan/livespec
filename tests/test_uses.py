"""A feature names what it uses — the gate held to its rule. Standard library.

Each test builds the injector's green fixture, which holds one feature, `core`,
adds a second that builds on it, and reads what trace.py says. See
specs/changes/0083.
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

QUEUE = (
    "@feature:live-queue @workflow:read-it\n"
    "{uses}"
    "Feature: The live queue\n\n"
    "  @rule:queue-renders-through-the-card{rule_uses}\n"
    "  Rule: each issue in the queue renders as the issue card does, with its age added\n\n"
    "    Example: an issue waiting an hour\n"
    "      Given an issue that arrived an hour ago\n"
    "      When the queue is open\n"
    "      Then it shows as the card does, with its age beside it\n"
)


def trace(root: Path) -> tuple[int, str]:
    result = subprocess.run([sys.executable, str(TRACE), str(root)], capture_output=True, text=True)
    return result.returncode, result.stdout + result.stderr


class AFeatureNamesWhatItUses(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp(prefix="uses-"))
        inject.build(self.root)
        self.addCleanup(shutil.rmtree, self.root, ignore_errors=True)
        self.queue = self.root / "specs" / "features" / "core" / "queue.feature"
        # The queue's rule is live, so a case claims it and the gate stays
        # quiet about everything but the reference under test.
        prompt = self.root / "evals" / "case-rule" / "prompt.md"
        prompt.write_text(prompt.read_text().replace("rule:one]", "rule:one, rule:queue-renders-through-the-card]"))

    def write_queue(self, uses: str = "", rule_uses: str = "") -> None:
        self.queue.write_text(QUEUE.format(uses=uses, rule_uses=rule_uses))

    @rule("a-feature-uses-only-features-that-exist")
    def test_a_feature_using_one_that_exists_is_not_mentioned(self):
        self.write_queue(uses="@uses:core\n")
        code, out = trace(self.root)
        self.assertEqual(code, 0, out)
        self.assertNotIn("@uses", out)

    @rule("a-feature-uses-only-features-that-exist")
    def test_a_feature_using_one_since_renamed_fails_naming_the_file_and_the_id(self):
        self.write_queue(uses="@uses:issue-card\n")
        code, out = trace(self.root)
        self.assertEqual(code, 1, out)
        self.assertIn("specs/features/core/queue.feature: @uses:issue-card, which names no feature", out)
        self.assertIn("name the id that feature carries now, or remove the tag", out)

    @rule("a-feature-uses-only-features-that-exist")
    def test_several_uses_on_their_own_lines_are_each_read(self):
        self.write_queue(uses="@uses:core\n@uses:issue-card\n")
        code, out = trace(self.root)
        self.assertEqual(code, 1, out)
        self.assertIn("@uses:issue-card, which names no feature", out)
        self.assertNotIn("@uses:core,", out)

    @rule("a-feature-uses-only-features-that-exist")
    def test_a_feature_that_uses_nothing_is_asked_nothing(self):
        self.write_queue()
        code, out = trace(self.root)
        self.assertEqual(code, 0, out)
        self.assertNotIn("@uses", out)

    @rule("a-feature-uses-only-features-that-exist")
    def test_a_uses_on_a_rule_fails_naming_the_rule(self):
        self.write_queue(rule_uses=" @uses:core")
        code, out = trace(self.root)
        self.assertEqual(code, 1, out)
        self.assertIn("@rule:queue-renders-through-the-card carries @uses:core; @uses goes on the Feature: line", out)
