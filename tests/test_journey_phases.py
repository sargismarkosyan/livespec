"""A workflow names the phases of its journey it is made in — the gate and the map held to their rules. Standard library.

Each test builds the injector's green fixture, whose journey `arc` has a map
headed *Before* and *Coming back* and whose workflow `read-it` names
`@phase:coming-back`, changes one thing, and reads what trace.py says.
See specs/changes/0084.
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


class AWorkflowNamesItsPhase(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp(prefix="phases-"))
        inject.build(self.root)
        self.addCleanup(shutil.rmtree, self.root, ignore_errors=True)
        self.workflow = self.root / "specs" / "workflows" / "read-it.feature"
        self.journey = self.root / "specs" / "journeys" / "arc.md"

    def edit(self, path: Path, old: str, new: str) -> None:
        text = path.read_text()
        self.assertIn(old, text)
        path.write_text(text.replace(old, new, 1))

    def map_of(self, out: str) -> list[str]:
        lines = out.splitlines()
        start = next(i for i, line in enumerate(lines) if "the journeys —" in line)
        block = []
        for line in lines[start + 1 :]:
            if not line.startswith("    "):
                break
            block.append(line.strip())
        return block

    @rule("a-workflow-names-only-phases-its-journey-has")
    def test_a_phase_the_journey_does_not_have_fails_naming_the_phases_it_has(self):
        self.edit(self.workflow, "@phase:coming-back", "@phase:the-change-after")
        code, out = trace(self.root)
        self.assertEqual(code, 1, out)
        self.assertIn("specs/workflows/read-it.feature", out)
        self.assertIn("@phase:the-change-after, which no journey it names has", out)
        self.assertIn("arc has before, coming-back", out)

    @rule("a-workflow-names-only-phases-its-journey-has")
    def test_a_phase_renamed_in_the_journey_fails_until_the_workflow_is_retagged(self):
        self.edit(self.journey, "**Coming back**", "**Going back to it**")
        code, out = trace(self.root)
        self.assertEqual(code, 1, out)
        self.assertIn("@phase:coming-back, which no journey it names has", out)
        self.assertIn("arc has before, going-back-to-it", out)
        self.edit(self.workflow, "@phase:coming-back", "@phase:going-back-to-it")
        code, out = trace(self.root)
        self.assertEqual(code, 0, out)

    @rule("a-workflow-names-only-phases-its-journey-has")
    def test_a_workflow_naming_no_phase_passes_without_a_warning(self):
        self.edit(self.workflow, " @phase:coming-back", "")
        code, out = trace(self.root)
        self.assertEqual(code, 0, out)
        self.assertNotIn("⚠", out)
        self.assertNotIn("@phase:", out)

    @rule("a-workflow-names-only-phases-its-journey-has")
    def test_a_phase_with_no_journey_to_find_it_in_fails(self):
        self.edit(self.workflow, " @journey:arc", "")
        code, out = trace(self.root)
        self.assertEqual(code, 1, out)
        self.assertIn("names @phase:coming-back and no @journey: to find it in", out)

    @rule("the-map-places-each-workflow-in-its-phases")
    def test_the_map_lists_the_phases_in_order_with_the_workflow_under_its_own(self):
        self.edit(self.journey, "| **Before** |", "| **Before** | **Putting it in** |")
        self.edit(self.journey, "| 1. Keeps a list |", "| 1. Keeps a list | 2. Starts one |")
        self.edit(self.journey, "|---|---|---|", "|---|---|---|---|")
        code, out = trace(self.root)
        self.assertEqual(code, 0, out)
        self.assertEqual(
            self.map_of(out),
            [
                "@journey:arc",
                "before: (nothing names it)",
                "putting-it-in: (nothing names it)",
                "coming-back: @workflow:read-it",
            ],
        )

    @rule("the-map-places-each-workflow-in-its-phases")
    def test_a_workflow_naming_the_journey_and_no_phase_is_listed_as_not_yet_placed(self):
        (self.root / "specs" / "workflows" / "skim-it.feature").write_text(
            "@workflow:skim-it @persona:reader @journey:arc @planned\n"
            "Feature: Skim the thing\n\n"
            "  Example: a glance\n    Given a list\n    When they glance\n    Then they see the top\n"
        )
        code, out = trace(self.root)
        self.assertEqual(code, 0, out)
        self.assertEqual(
            self.map_of(out),
            [
                "@journey:arc",
                "before: (nothing names it)",
                "coming-back: @workflow:read-it",
                "not yet placed in a phase: @workflow:skim-it",
            ],
        )


if __name__ == "__main__":
    unittest.main()
