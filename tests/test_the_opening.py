"""The report's count of what a body says before its evidence. Standard library.

The count is pure — a body in, a number and what stopped it out — and the
report section around it is pure too, so the tests hand them text. Nothing
here judges the words; the rule is that the report counts and fails nothing.
See specs/changes/0082.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".github" / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import report  # noqa: E402
from rulelib import rule  # noqa: E402

HEAD = {
    "personas": {"live": 1, "retired": 0}, "journeys": 1, "workflows": {"total": 1, "planned": 0},
    "features": 1, "rules": {"live": 1, "planned": 0}, "cases": {"total": 1, "claiming": 1, "negative": 0},
    "failures": 0, "warnings": 0,
}
POINT_FIRST = (
    "The report now counts what a body says before its evidence.\n"
    "Read report.py, opening().\n\n"
    "## Changelog\n\nThe entry, which is not counted.\n"
)


class TheCount(unittest.TestCase):
    @rule("the-report-counts-what-comes-before-the-evidence")
    def test_a_body_that_opens_with_its_point_is_counted_to_its_first_heading(self):
        self.assertEqual(report.opening(POINT_FIRST), (14, "heading"))
        out = report.build(HEAD, None, body_text=POINT_FIRST)
        self.assertIn("## The opening", out)
        self.assertIn("**14 words** before its first heading", out)

    @rule("the-report-counts-what-comes-before-the-evidence")
    def test_a_code_block_and_a_folded_block_end_the_opening_too(self):
        self.assertEqual(report.opening("One two.\n```\n$ run\n```\n"), (2, "code block"))
        self.assertEqual(report.opening("One two three.\n\n<details><summary>Run</summary>\n"), (3, "folded block"))

    @rule("the-report-counts-what-comes-before-the-evidence")
    def test_a_title_on_the_first_line_is_skipped_and_link_targets_are_not_words(self):
        body = "## Summary\n\nSee [the rule](https://example.com/a/very/long/path) here.\n\n## Evidence\n"
        self.assertEqual(report.opening(body), (4, "heading"))
        self.assertEqual(report.opening("<!-- a template's prompt -->\nTwo words.\n## H\n"), (2, "heading"))

    @rule("the-report-counts-what-comes-before-the-evidence")
    def test_a_body_that_opens_straight_into_its_evidence_says_so(self):
        out = report.build(HEAD, None, body_text="```\n$ python3 gate.py\nok\n```\n\nIt works.\n")
        self.assertIn("opens straight into its evidence", out)
        self.assertIn("first code block", out)

    @rule("the-report-counts-what-comes-before-the-evidence")
    def test_a_long_opening_is_printed_and_judged_nothing(self):
        body = ("word " * 600) + "\n\n## Changelog\n"
        out = report.build(HEAD, None, body_text=body)
        self.assertIn("**600 words**", out)
        for verdict in ("too long", "FAIL", "exceeds", "over the"):
            self.assertNotIn(verdict, out)

    @rule("the-report-counts-what-comes-before-the-evidence")
    def test_no_body_prints_no_count_and_an_empty_one_says_so(self):
        self.assertNotIn("## The opening", report.build(HEAD, None))
        self.assertIn("The body is empty.", report.build(HEAD, None, body_text="  \n\n"))

    @rule("the-report-counts-what-comes-before-the-evidence")
    def test_a_body_with_nothing_that_ends_the_opening_is_counted_whole(self):
        out = report.build(HEAD, None, body_text="Just a sentence of six words.\n")
        self.assertIn("**6 words** and has no heading, code block or folded block", out)


if __name__ == "__main__":
    unittest.main()
