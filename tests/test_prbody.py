"""A pull request's description held to its template and to linked references — tools/prbody.py. Standard library.

Each test writes a description, and where it matters a template, into a
temporary directory and runs the tool as a consuming repository's CI would,
reading its exit code and its report. See specs/changes/2026-11-23-the-description-gate.md.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from rulelib import rule  # noqa: E402

PRBODY = ROOT / "tools" / "prbody.py"
CHECKLIST = "## Merge Request Submission Checklist\n(To check off an item mark `x` inside the brackets)\n- [ ] This change is safe to deploy to production\n"
POINT = "Reviewers lose the point of a change in long descriptions; this keeps it first.\n\n"


def run(body: str, template: str = "", allow: tuple[str, ...] = ()) -> tuple[int, str]:
    work = Path(tempfile.mkdtemp(prefix="prbody-"))
    (work / "body.md").write_text(body, encoding="utf-8")
    args = [sys.executable, str(PRBODY), "--body-file", str(work / "body.md")]
    if template:
        (work / "template.md").write_text(template, encoding="utf-8")
        args += ["--template", str(work / "template.md")]
    for heading in allow:
        args += ["--allow", heading]
    result = subprocess.run(args, capture_output=True, text=True)
    return result.returncode, result.stdout + result.stderr


class Template(unittest.TestCase):
    @rule("a-description-out-of-its-template-fails")
    def test_headings_added_beside_a_checklist_fail_by_name(self):
        body = POINT + CHECKLIST.replace("[ ]", "[x]") + "\n## What changes\n\nx\n\n## Open questions\n\ny\n\n## Testing\n\nz\n"
        code, out = run(body, CHECKLIST)
        self.assertEqual(code, 1, out)
        for heading in ("What changes", "Open questions", "Testing"):
            self.assertIn(f"## {heading}", out)
        self.assertIn("second shape", out)

    @rule("a-description-out-of-its-template-fails")
    def test_a_missing_checkbox_fails(self):
        code, out = run(POINT + "## Merge Request Submission Checklist\n", CHECKLIST)
        self.assertEqual(code, 1, out)
        self.assertIn("checkbox", out)

    @rule("a-description-out-of-its-template-fails")
    def test_a_ticked_checkbox_with_its_note_after_it_is_there(self):
        body = POINT + CHECKLIST.replace("[ ] This change is safe to deploy to production",
                                         "[x] This change is safe to deploy to production — nothing that ships changes")
        code, out = run(body, CHECKLIST)
        self.assertEqual(code, 0, out)

    @rule("a-description-out-of-its-template-fails")
    def test_a_section_the_rules_add_is_allowed(self):
        body = POINT + CHECKLIST + "\n## Changelog\n\nWhat users see.\n"
        self.assertEqual(run(body, CHECKLIST, ("## Changelog",))[0], 0)
        self.assertEqual(run(body, CHECKLIST)[0], 1)


class References(unittest.TestCase):
    @rule("a-bare-reference-fails")
    def test_a_tracker_item_named_by_its_address_fails(self):
        code, out = run(POINT + "Hub: https://experience.example/issue/6b00cf69\n")
        self.assertEqual(code, 1, out)
        self.assertIn("https://experience.example/issue/6b00cf69", out)
        self.assertIn("link with its title", out)

    @rule("a-bare-reference-fails")
    def test_the_closing_line_passes_and_the_same_number_in_prose_fails(self):
        self.assertEqual(run(POINT + "Closes #12\n")[0], 0)
        code, out = run(POINT + "Closes #12\n\nThe cause was found in #12.\n")
        self.assertEqual(code, 1, out)
        self.assertIn("“#12” is bare", out)

    @rule("a-bare-reference-fails")
    def test_a_link_with_its_title_code_and_folded_blocks_pass(self):
        body = (POINT + "Fixes the crash in [#12 Saving a draft loses it](https://x.example/12).\n\n"
                "Run `see #13` locally.\n\n<details><summary>The run</summary>\n\nhttps://ci.example/run/1 #14\n\n</details>\n"
                "\n```\nhttps://ci.example/log #15\n```\n<!-- see #16 -->\n")
        self.assertEqual(run(body)[0], 0)


class Length(unittest.TestCase):
    @rule("the-length-is-reported-never-failed")
    def test_a_long_description_passes_and_is_counted(self):
        body = CHECKLIST.replace("[ ]", "[x]") + "\n" + " ".join(["word"] * 300) + "\n"
        code, out = run(body, CHECKLIST)
        self.assertEqual(code, 0, out)
        self.assertIn("300 words of the author's own", out)
        self.assertIn("never failed", out)


if __name__ == "__main__":
    unittest.main()
