"""The run beside the claim, held to its rules. Standard library.

Two things are code here: the reader that finds the run block in a pull
request's body, and the report that prints the pipeline's own run beside it.
Both are pure — a body and a command in, a block or a refusal out; a run and a
body in, a section out — so the tests hand them text. See specs/changes/0052.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".github" / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import report  # noqa: E402
from releaselib import ReleaseInputError, extract_run, touches_the_run, verification_command  # noqa: E402
from rulelib import rule  # noqa: E402

COMMAND = "python3 gate.py"
BODY = (
    "Intro.\n\n## Changelog\n\nThe entry.\n\n"
    "```gherkin\n  Rule: it holds\n```\n\n"
    "```\n$ python3 gate.py\n✔ traceability: 3 live rule(s) traced\n✘ verification is waiting on a measurement run\n```\n"
)
HEAD = {
    "personas": {"live": 1, "retired": 0}, "journeys": 1, "workflows": {"total": 1, "planned": 0},
    "features": 1, "rules": {"live": 1, "planned": 0}, "cases": {"total": 1, "claiming": 1, "negative": 0},
    "failures": 0, "warnings": 0,
}
PIPELINE = "── traceability ──\n✔ traceability: 3 live rule(s) traced\n✔ local checks green — 5 of 6 gates\n"


class TheBlock(unittest.TestCase):
    @rule("a-claim-of-green-carries-the-run")
    def test_the_run_under_the_command_is_read(self):
        block = extract_run(BODY, COMMAND)
        self.assertEqual(block.splitlines()[0], "$ python3 gate.py")
        self.assertIn("waiting on a measurement run", block)

    @rule("a-claim-of-green-carries-the-run")
    def test_a_claim_with_no_run_is_refused_naming_the_block_and_the_command(self):
        with self.assertRaises(ReleaseInputError) as caught:
            extract_run("## Changelog\n\nThe tests pass, 66 of 66.\n", COMMAND)
        self.assertIn("carries no run block", str(caught.exception))
        self.assertIn(COMMAND, str(caught.exception))

    @rule("a-claim-of-green-carries-the-run")
    def test_a_run_of_some_other_command_is_refused_naming_the_right_one(self):
        with self.assertRaises(ReleaseInputError) as caught:
            extract_run("```\n$ npm test\n12 passing\n```\n", COMMAND)
        self.assertIn("not the verification command", str(caught.exception))
        self.assertIn(COMMAND, str(caught.exception))

    @rule("a-claim-of-green-carries-the-run")
    def test_the_command_alone_is_not_a_run(self):
        with self.assertRaises(ReleaseInputError) as caught:
            extract_run("```\n$ python3 gate.py\n```\n", COMMAND)
        self.assertIn("no output under it", str(caught.exception))

    @rule("a-claim-of-green-carries-the-run")
    def test_a_gherkin_block_is_not_mistaken_for_the_run(self):
        with self.assertRaises(ReleaseInputError):
            extract_run("```gherkin\n  Rule: it holds\n```\n", COMMAND)

    @rule("a-claim-of-green-carries-the-run")
    def test_a_change_that_touches_no_test_owes_none(self):
        self.assertEqual(touches_the_run(["method/gates.md", "specs/changes/0001-x.md", "evals/README.md"]), [])
        self.assertEqual(
            touches_the_run(["tests/test_a.py", "evals/01-x/prompt.md", ".github/scripts/trace.py"]),
            ["tests/test_a.py", "evals/01-x/prompt.md", ".github/scripts/trace.py"],
        )

    @rule("a-claim-of-green-carries-the-run")
    def test_the_command_is_read_from_the_bindings_verification_row(self):
        self.assertEqual(verification_command("| | |\n|---|---|\n| **Verification** | `python3 gate.py` |\n"), COMMAND)
        with self.assertRaises(ReleaseInputError):
            verification_command("# Bindings\n\nno table here\n")


class TheReport(unittest.TestCase):
    @rule("the-report-prints-its-own-run-beside-the-claim")
    def test_the_body_block_and_the_pipeline_tail_sit_side_by_side(self):
        out = report.build(HEAD, None, None, None, run_text=PIPELINE, body_text=BODY, command=COMMAND)
        self.assertIn("## The run", out)
        self.assertIn("$ python3 gate.py", out)
        self.assertIn("waiting on a measurement run", out)
        self.assertIn("local checks green", out)

    @rule("the-report-prints-its-own-run-beside-the-claim")
    def test_the_two_disagreeing_is_printed_and_never_judged(self):
        out = report.build(HEAD, None, None, None, run_text=PIPELINE, body_text=BODY, command=COMMAND)
        self.assertIn("waiting on a measurement run", out)
        self.assertIn("5 of 6 gates", out)
        for verdict in ("mismatch", "FAIL", "does not match", "fabricat"):
            self.assertNotIn(verdict, out)

    @rule("the-report-prints-its-own-run-beside-the-claim")
    def test_a_body_with_no_block_is_said_and_fails_nothing(self):
        out = report.build(HEAD, None, None, None, run_text=PIPELINE, body_text="## Changelog\n\nno block", command=COMMAND)
        self.assertIn("no run block", out)
        self.assertIn("gate's to say", out)
        self.assertIn("local checks green", out)

    @rule("the-report-prints-its-own-run-beside-the-claim")
    def test_a_missing_pipeline_run_is_said(self):
        out = report.build(HEAD, None, None, None, run_text=None, body_text=BODY, command=COMMAND)
        self.assertIn("not available", out)
        self.assertIn("$ python3 gate.py", out)

    @rule("the-report-prints-its-own-run-beside-the-claim")
    def test_a_report_handed_neither_prints_no_run_section(self):
        out = report.build(HEAD, None, None, None)
        self.assertNotIn("## The run", out)


if __name__ == "__main__":
    unittest.main()
