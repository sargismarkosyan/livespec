"""What a change costs each workflow walk — tools/walkcost.py held to its rules. Standard library.

Each test writes the samples a repository's walks would write and a policy
file into a temporary directory, runs the comparison as a consuming
repository's CI would, and reads its exit code and its report.
See specs/changes/0089.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from rulelib import rule  # noqa: E402

WALKCOST = ROOT / "tools" / "walkcost.py"
POLICY = {
    "rounds": 5,
    "measures": {"load-ms": {"kind": "time", "noise": 3, "allowance": 10},
                 "requests": {"kind": "count", "allowance": 0}},
    "budgets": {"checkout": {"requests": 42}},
}
STEADY = [100, 101, 99, 100, 102]


def samples(workflow: str, measure: str, base: list, branch: list) -> list:
    return ([{"workflow": workflow, "measure": measure, "side": "base", "value": v} for v in base]
            + [{"workflow": workflow, "measure": measure, "side": "branch", "value": v} for v in branch])


class Walk(unittest.TestCase):
    def setUp(self):
        self.dir = Path(tempfile.mkdtemp(prefix="walkcost-"))
        self.addCleanup(shutil.rmtree, self.dir, ignore_errors=True)

    def run_it(self, rows: list, policy: dict = POLICY, base_policy: dict | None = None, gate: bool = False,
               body: str | None = None):
        (self.dir / "s.jsonl").write_text("\n".join(json.dumps(r) for r in rows) + "\n")
        (self.dir / "p.json").write_text(json.dumps(policy))
        args = [sys.executable, str(WALKCOST), "--samples", str(self.dir / "s.jsonl"), "--policy", str(self.dir / "p.json")]
        if base_policy is not None:
            (self.dir / "b.json").write_text(json.dumps(base_policy))
            args += ["--base-policy", str(self.dir / "b.json")]
        if body is not None:
            (self.dir / "body.md").write_text(body)
            args += ["--body", str(self.dir / "body.md")]
        if gate:
            args.append("--gate")
        result = subprocess.run(args, capture_output=True, text=True)
        return result.returncode, result.stdout + result.stderr

    def row(self, text: str, workflow: str) -> str:
        return next((line for line in text.splitlines() if line.startswith(f"| {workflow} |")), "")


class TheBranchAgainstItsBase(Walk):
    @rule("the-cost-is-the-branch-against-its-base")
    def test_a_walk_slower_every_round_reads_worse_and_the_rest_read_no_change_once(self):
        code, out = self.run_it(samples("checkout", "load-ms", STEADY, [130, 131, 129, 132, 130])
                                + samples("search", "load-ms", STEADY, STEADY)
                                + samples("search", "requests", [7] * 5, [7] * 5))
        self.assertEqual(code, 0, out)
        self.assertIn("past its allowance", self.row(out, "checkout"))
        self.assertIn("+30", self.row(out, "checkout"))
        self.assertIn("**No change:** search · load-ms, search · requests.", out)
        self.assertEqual(self.row(out, "search"), "", out)

    @rule("the-cost-is-the-branch-against-its-base")
    def test_a_difference_inside_the_noise_shows_no_number(self):
        code, out = self.run_it(samples("checkout", "load-ms", STEADY, [101, 102, 100, 101, 103]))
        self.assertEqual(code, 0, out)
        self.assertIn("**No change:** checkout · load-ms.", out)
        self.assertNotIn("%", out)

    @rule("the-cost-is-the-branch-against-its-base")
    def test_the_same_samples_give_the_same_report(self):
        rows = samples("checkout", "load-ms", STEADY, [104, 99, 108, 103, 101])
        self.assertEqual(self.run_it(rows), self.run_it(rows))


class InconclusiveIsSaid(Walk):
    @rule("an-unclear-cost-is-inconclusive")
    def test_an_interval_across_the_noise_is_inconclusive_with_its_reason(self):
        code, out = self.run_it(samples("checkout", "load-ms", STEADY, [96, 112, 101, 109, 98]))
        self.assertEqual(code, 0, out)
        self.assertIn("**inconclusive** — the interval reaches both sides of the 3% noise; more rounds would decide it",
                      self.row(out, "checkout"))
        self.assertNotIn("No change", out)

    @rule("an-unclear-cost-is-inconclusive")
    def test_a_base_with_no_samples_is_inconclusive_and_the_gate_passes(self):
        code, out = self.run_it([r for r in samples("checkout", "requests", [42] * 5, [43] * 5) if r["side"] == "branch"],
                                gate=True)
        self.assertEqual(code, 0, out)
        self.assertIn("the base has no samples", self.row(out, "checkout"))

    @rule("an-unclear-cost-is-inconclusive")
    def test_too_few_rounds_and_a_count_that_varies_are_inconclusive(self):
        code, out = self.run_it(samples("checkout", "load-ms", [100, 101], [150, 151])
                                + samples("search", "requests", [7, 7, 8], [7, 7, 7]))
        self.assertEqual(code, 0, out)
        self.assertIn("too few rounds to bound the change: 2 on the base, 2 on the branch", self.row(out, "checkout"))
        self.assertIn("it varies between rounds of one side", self.row(out, "search"))


class SaidNotRefused(Walk):
    @rule("a-slower-walk-is-said-not-refused")
    def test_a_walk_twice_as_slow_leads_the_report_and_the_gate_passes(self):
        code, out = self.run_it(samples("search", "load-ms", STEADY, [108, 109, 108, 110, 109])
                                + samples("checkout", "load-ms", STEADY, [200, 202, 198, 201, 203]), gate=True,
                                body="## Performance\n\n- checkout: the new card form loads its fonts, accepted\n")
        self.assertEqual(code, 0, out)
        table = [line for line in out.splitlines() if line.startswith("| ") and "Walk" not in line and "---" not in line]
        self.assertTrue(table[0].startswith("| checkout |"), out)
        self.assertIn("past its allowance", table[0])
        self.assertIn("within its allowance", table[1])


class OnlyACountGates(Walk):
    @rule("a-budget-gates-only-a-count")
    def test_a_count_over_its_budget_fails_the_gate_naming_all_four(self):
        code, out = self.run_it(samples("checkout", "requests", [42] * 5, [43] * 5), gate=True)
        self.assertEqual(code, 1, out)
        self.assertIn("**The gate fails:** the checkout walk's requests is 43 against a budget of 42.", out)

    @rule("a-budget-gates-only-a-count")
    def test_without_the_gate_flag_the_same_samples_only_report(self):
        code, out = self.run_it(samples("checkout", "requests", [42] * 5, [43] * 5))
        self.assertEqual(code, 0, out)
        self.assertIn("over budget", self.row(out, "checkout"))

    @rule("a-budget-gates-only-a-count")
    def test_a_budget_on_a_time_is_refused_before_anything_is_compared(self):
        policy = json.loads(json.dumps(POLICY))
        policy["budgets"]["checkout"]["load-ms"] = 2000
        code, out = self.run_it(samples("checkout", "load-ms", STEADY, STEADY), policy=policy)
        self.assertEqual(code, 2, out)
        self.assertIn("a time cannot carry a budget", out)
        self.assertNotIn("What this change costs", out)


class TheLayerIsNamed(Walk):
    @rule("the-report-names-the-layer")
    def test_one_measure_in_two_layers_is_two_lines_each_naming_its_layer(self):
        rows = [dict(r, layer="front end") for r in samples("checkout", "load-ms", STEADY, [130, 131, 129, 132, 130])]
        rows += [dict(r, layer="end to end") for r in samples("checkout", "load-ms", STEADY, [160, 161, 159, 162, 160])]
        code, out = self.run_it(rows)
        self.assertEqual(code, 0, out)
        self.assertIn("| checkout · front end | load-ms |", out)
        self.assertIn("| checkout · end to end | load-ms |", out)


SLOWER = samples("checkout", "load-ms", STEADY, [130, 131, 129, 132, 130])
ANSWER = "checkout: the new card form loads its fonts, accepted"


class ARegressionIsAnswered(Walk):
    @rule("a-regression-past-its-allowance-is-acknowledged")
    def test_a_walk_past_its_allowance_with_no_section_fails_naming_it(self):
        code, out = self.run_it(SLOWER, gate=True, body="Adds the card form.\n\n## Changelog\n\nCard form.\n")
        self.assertEqual(code, 1, out)
        self.assertIn("the checkout walk's load-ms is past its allowance, and the pull request does not name "
                      "checkout under ## Performance", out)

    @rule("a-regression-past-its-allowance-is-acknowledged")
    def test_naming_the_walk_under_performance_passes(self):
        code, out = self.run_it(SLOWER, gate=True, body=f"## Performance\n\n- {ANSWER}\n\n## Changelog\n\nx\n")
        self.assertEqual(code, 0, out)

    @rule("a-regression-past-its-allowance-is-acknowledged")
    def test_a_walk_named_only_outside_the_section_or_as_part_of_a_word_is_unanswered(self):
        body = "checkout is fine.\n\n## Performance\n\n- checkout-v2: unrelated\n\n## Notes\n\ncheckout\n"
        code, out = self.run_it(SLOWER, gate=True, body=body)
        self.assertEqual(code, 1, out)

    @rule("a-regression-past-its-allowance-is-acknowledged")
    def test_within_its_allowance_nothing_is_owed(self):
        code, out = self.run_it(samples("checkout", "load-ms", STEADY, [108, 109, 108, 110, 109]), gate=True, body="")
        self.assertEqual(code, 0, out)
        self.assertIn("within its allowance", self.row(out, "checkout"))


class TheAnswerIsQuoted(Walk):
    @rule("the-acknowledgement-is-quoted-beside-the-walk")
    def test_the_line_that_answered_sits_on_the_walks_line(self):
        code, out = self.run_it(SLOWER, gate=True, body=f"## Performance\n\n- {ANSWER}\n")
        self.assertEqual(code, 0, out)
        self.assertIn(f"answered: “{ANSWER}”", self.row(out, "checkout"))


class AChangedBudgetIsShown(Walk):
    @rule("a-changed-budget-is-shown-beside-the-change")
    def test_a_raised_budget_is_listed_and_the_walk_is_read_against_it(self):
        raised = json.loads(json.dumps(POLICY))
        raised["budgets"]["checkout"]["requests"] = 50
        code, out = self.run_it(samples("checkout", "requests", [42] * 5, [43] * 5), policy=raised,
                                base_policy=POLICY, gate=True)
        self.assertEqual(code, 0, out)
        self.assertIn("- the checkout walk's requests budget: moved from 42 to 50", out)
        self.assertNotIn("over budget", out)

    @rule("a-changed-budget-is-shown-beside-the-change")
    def test_an_unchanged_policy_lists_nothing(self):
        code, out = self.run_it(samples("checkout", "requests", [42] * 5, [42] * 5), base_policy=POLICY)
        self.assertEqual(code, 0, out)
        self.assertNotIn("The policy moved", out)


if __name__ == "__main__":
    unittest.main()
