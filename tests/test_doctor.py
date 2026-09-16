"""The audit tool, held to its rules. Standard library; every test names its rule.

Each test builds a small consuming repository in a temporary directory — the
bindings from the template, filled green — and reads what the tool says about
it. The plugin the tool reads is this repository, except where a test points it
at a fixture standing in for one.
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
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / ".github" / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import doctor  # noqa: E402
import inject  # noqa: E402
from rulelib import rule  # noqa: E402

INSTALLED = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text())["version"]


def repo(bindings: str | None = None, files: dict[str, str] | None = None) -> Path:
    """A consuming repository in a temporary directory, green unless told otherwise."""
    root = Path(tempfile.mkdtemp(prefix="doctor-"))
    text = bindings if bindings is not None else inject.green_bindings(INSTALLED)
    (root / "specs" / "setup").mkdir(parents=True)
    (root / "specs" / "setup" / "README.md").write_text(text, encoding="utf-8")
    (root / "specs" / "changes").mkdir()
    (root / "specs" / "changes" / "0001-first.md").write_text("# Spec 0001\n", encoding="utf-8")
    (root / "CLAUDE.md").write_text("# The loop\n\n`/livespec:refine-spec` writes the spec.\n", encoding="utf-8")
    for relative, content in (files or {}).items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    return root


def audit(root: Path) -> dict[str, dict[str, str]]:
    ctx = doctor.context(root, root / "specs" / "setup" / "README.md")
    return {line["id"]: line for line in doctor.emit(ctx)}


class TheList(unittest.TestCase):
    @rule("every-check-has-a-permanent-id")
    def test_the_ids_are_one_table_and_every_one_is_well_formed(self):
        rows = doctor.registry()
        ids = [row["id"] for row in rows]
        self.assertEqual(len(ids), len(set(ids)), "an id appears twice in the registry")
        for row in rows:
            self.assertRegex(row["id"], r"^(gate|wiring|check):[a-z0-9]+(?:-[a-z0-9]+)*$")
            self.assertIn(row["kind"], ("gate", "wiring", "mechanical", "judgment"))
            self.assertIn(row["severity"], doctor.SEVERITY_ORDER)
            self.assertTrue(row["meaning"], f"{row['id']} has no meaning")

    @rule("every-check-has-a-permanent-id")
    def test_a_retired_id_reads_retired_never_unknown(self):
        root = repo()
        ctx = doctor.context(root, root / "specs" / "setup" / "README.md")
        ctx["ids"] = [{"id": "gate:rule-to-test", "since": "0.6.0", "retired": "9.9.0 → superseded-by gate:rule-to-case"}]
        state, evidence = doctor.c_row_per_gate(ctx)
        self.assertEqual(state, "open")
        self.assertIn("retired", evidence)
        self.assertNotIn("unknown", evidence)

    @rule("the-table-and-the-tool-agree")
    def test_the_registry_and_the_table_hold_the_same_ids(self):
        table = {row["id"] for row in doctor.id_rows((ROOT / "method" / "gates.md").read_text())}
        self.assertEqual({row["id"] for row in doctor.registry()}, table)

    @rule("the-table-and-the-tool-agree")
    def test_a_check_the_tool_has_and_the_table_lacks_is_red_here(self):
        root = Path(tempfile.mkdtemp(prefix="agree-"))
        inject.build(root)
        gates = root / "method" / "gates.md"
        gates.write_text(gates.read_text().replace("| `check:ledger-shape` |", "| `check:ledger-shapes` |", 1))
        result = subprocess.run([sys.executable, str(ROOT / ".github" / "scripts" / "checks.py"), str(root)], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("check:ledger-shape", result.stdout + result.stderr)
        shutil.rmtree(root)

    @rule("a-repository-may-add-rows-of-its-own")
    def test_a_local_row_is_read_like_any_other_and_required_by_nothing(self):
        text = inject.green_bindings(INSTALLED).replace(
            "| `gate:verified-to-fire` |",
            "| `local:lint` | the linter | automated | `make lint` |\n| `gate:verified-to-fire` |", 1,
        )
        lines = audit(repo(text))
        self.assertEqual(lines["check:row-per-gate"]["state"], "clear")
        self.assertIn("1 local: row", lines["check:row-per-gate"]["evidence"])
        self.assertEqual(lines["check:row-state-legal"]["state"], "clear")

    @rule("a-repository-may-add-rows-of-its-own")
    def test_a_row_with_no_prefix_is_reported_with_candidates(self):
        text = inject.green_bindings(INSTALLED).replace(
            "| `gate:verified-to-fire` |",
            "| `` | rule → case | automated | `trace.py` |\n| `gate:verified-to-fire` |", 1,
        )
        lines = audit(repo(text))
        self.assertEqual(lines["check:row-per-gate"]["state"], "open")
        self.assertIn("gate:rule-to-test", lines["check:row-per-gate"]["evidence"])


class TheShape(unittest.TestCase):
    @rule("the-bindings-are-written-from-one-template")
    def test_the_fixture_is_the_template_filled_and_the_tool_reads_it_as_such(self):
        root = repo()
        ctx = doctor.context(root, root / "specs" / "setup" / "README.md")
        self.assertTrue(doctor.in_shape(ctx))
        template = (ROOT / "templates" / "bindings.md").read_text()
        for header in ("| id | gate | state | evidence |", "| id | wiring | state | evidence |", "| id | boundary | state | since | evidence |"):
            self.assertIn(header, template)
            self.assertIn(header, inject.green_bindings(INSTALLED))

    @rule("a-ledger-not-in-shape-is-a-finding-not-a-crash")
    def test_a_pre_template_ledger_is_a_finding_and_the_rest_goes_on(self):
        text = inject.green_bindings(INSTALLED).replace("| id | gate | state | evidence |\n|---|---|---|---|", "| Gate | State | Wired by, or why not |\n|---|---|---|")
        lines = audit(repo(text))
        self.assertEqual(lines["check:ledger-shape"]["state"], "open")
        self.assertEqual(lines["check:row-per-gate"]["state"], "n/a")
        self.assertIn("ledger-shape", lines["check:row-per-gate"]["evidence"])
        self.assertEqual(lines["check:stamp-present"]["state"], "clear")
        self.assertEqual(lines["check:skill-names"]["state"], "clear")

    @rule("old-rows-are-matched-by-alias")
    def test_an_old_label_matches_its_id_and_an_ambiguous_one_does_not(self):
        self.assertEqual(doctor.match_alias("rule → case", doctor.GATES), ["gate:rule-to-test"])
        self.assertEqual(doctor.match_alias("workflow → case (walked end to end)", doctor.GATES), ["gate:workflow-walked"])
        self.assertEqual(doctor.match_alias("coverage — lines, branches, functions", doctor.GATES), ["gate:coverage"])
        self.assertEqual(doctor.match_alias("something nobody named", doctor.GATES), [])

    @rule("old-rows-are-matched-by-alias")
    def test_reshape_writes_the_matched_id_and_moves_no_row(self):
        old = (
            "# Bindings\n\n## Gate wiring\n\n**Reconciled against livespec 0.9.0 on 2026-01-01.**\n\n"
            "| Gate | State | Wired by, or why not |\n|---|---|---|\n"
            "| rule → case | automated | `trace.py` |\n"
            "| persona → workflow | not applicable | no personas exist |\n\n"
            "### The wiring that must never gate\n\n| Wiring | State | How |\n|---|---|---|\n| the pull-request report | unobserved | `report.py` |\n\n"
            "### The boundaries\n\n| Boundary | Row | Leaves uncovered |\n|---|---|---|\n| the store | **mocked** since 0003 | volume |\n"
        )
        root = repo(old)
        ctx = doctor.context(root, root / "specs" / "setup" / "README.md")
        shaped = doctor.reshape(ctx)
        self.assertIn("| `gate:rule-to-test` | rule → case | automated | `trace.py` |", shaped)
        self.assertIn("| `gate:persona-to-workflow` | persona → workflow | not applicable | no personas exist |", shaped)
        self.assertIn("| `wiring:pr-report` | the pull-request report | unobserved | `report.py` |", shaped)
        self.assertIn("| `boundary:the-store` | the store | mocked | 0003 |", shaped)
        self.assertIn("Reconciled against livespec 0.9.0 on 2026-01-01", shaped)


class TheTool(unittest.TestCase):
    @rule("a-check-a-script-can-answer-is-answered-by-a-script")
    def test_the_same_ledger_twice_gives_identical_lines(self):
        root = repo()
        first = {k: (v["state"], v["evidence"]) for k, v in audit(root).items()}
        second = {k: (v["state"], v["evidence"]) for k, v in audit(root).items()}
        self.assertEqual(first, second)

    @rule("a-check-a-script-can-answer-is-answered-by-a-script")
    def test_the_kind_of_repository_does_not_reach_the_mechanical_lines(self):
        base = {k: (v["state"], v["evidence"]) for k, v in audit(repo()).items() if v["who"] == "script"}
        for shape in (
            {"src/app.py": "raise SystemExit('never read')", "pyproject.toml": "[project]\nname='x'\n"},
            {"web/index.html": "<html>", "package.json": '{"dependencies": {"react": "1"}}'},
            {"cmd/main.go": "package main", "go.mod": "module x\n"},
            {},
        ):
            other = {k: (v["state"], v["evidence"]) for k, v in audit(repo(files=shape)).items() if v["who"] == "script"}
            self.assertEqual(base, other, f"a mechanical line moved for {sorted(shape)}")

    @rule("the-tool-runs-nothing-it-read")
    def test_a_command_planted_in_a_bindings_cell_leaves_no_mark(self):
        root = repo()
        mark = root / "pwned"
        planted = f"touch {mark}"
        text = (root / "specs" / "setup" / "README.md").read_text().replace("`python3 gate.py trace`", f"`{planted}`")
        (root / "specs" / "setup" / "README.md").write_text(text)
        lines = audit(root)
        subprocess.run([sys.executable, str(ROOT / "tools" / "doctor.py"), "specs/setup/README.md"], cwd=root, capture_output=True, text=True)
        self.assertFalse(mark.exists(), "the tool ran a command it read from the bindings")
        self.assertEqual(lines["check:real-not-doubled"]["state"], "unanswered", "the line is handed to a mind, not answered by running anything")

    @rule("a-judgment-line-arrives-with-its-command")
    def test_the_platform_line_carries_the_command_the_bindings_name(self):
        lines = audit(repo())
        for check in ("check:merge-blocked", "check:check-name", "check:who-bypasses"):
            self.assertEqual(lines[check]["state"], "unanswered")
            self.assertIn("run: gh api repos/o/r/rulesets", lines[check]["evidence"])

    @rule("a-judgment-line-arrives-with-its-command")
    def test_a_row_naming_no_command_says_the_row_must_name_one(self):
        text = inject.green_bindings(INSTALLED).replace("`gh api repos/o/r/rulesets`", "read from the settings page")
        lines = audit(repo(text))
        self.assertEqual(lines["check:merge-blocked"]["state"], "unanswered")
        self.assertIn("name one", lines["check:merge-blocked"]["evidence"])

    @rule("every-mechanical-check-is-proven-to-fire")
    def test_every_mechanical_check_has_a_fault_that_flips_it(self):
        targeted = {fault[1] for fault in inject.DOCTOR_FAULTS}
        self.assertEqual(set(doctor.MECHANICAL), targeted)


class WhenThingsMove(unittest.TestCase):
    @rule("a-check-newer-than-the-stamp-is-reported-until-the-wiring-catches-up")
    def test_a_gate_that_arrived_after_the_stamp_is_named_and_open_for_want_of_a_row(self):
        text = inject.green_bindings("0.6.0")
        text = "\n".join(line for line in text.splitlines() if "gate:boundary-double" not in line) + "\n"
        lines = audit(repo(text))
        self.assertEqual(lines["check:stamp-range"]["state"], "open")
        self.assertIn("gate:boundary-double", lines["check:stamp-range"]["evidence"])
        self.assertEqual(lines["check:row-per-gate"]["state"], "open")
        self.assertIn("no row for gate:boundary-double", lines["check:row-per-gate"]["evidence"])

    @rule("a-check-newer-than-the-stamp-is-reported-until-the-wiring-catches-up")
    def test_the_stamp_is_left_where_it_was(self):
        root = repo(inject.green_bindings("0.6.0"))
        before = (root / "specs" / "setup" / "README.md").read_text()
        audit(root)
        self.assertEqual(before, (root / "specs" / "setup" / "README.md").read_text())

    @rule("the-tree-is-inventoried-and-the-rows-are-held-to-it")
    def test_two_languages_and_one_coverage_row_names_the_other(self):
        files = {"pyproject.toml": "[project]\nname='api'\n", "package.json": '{"name": "web", "dependencies": {}}'}
        lines = audit(repo(files=files))
        evidence = lines["check:row-uncovered"]["evidence"]
        self.assertEqual(lines["check:row-uncovered"]["state"], "unanswered")
        self.assertIn("python", evidence)
        self.assertIn("javascript/typescript", evidence)

    @rule("the-tree-is-inventoried-and-the-rows-are-held-to-it")
    def test_a_service_no_boundary_row_names_is_named(self):
        files = {"package.json": '{"dependencies": {"stripe": "1", "axios": "1"}}'}
        evidence = audit(repo(files=files))["check:row-uncovered"]["evidence"]
        self.assertIn("a payment service", evidence)
        self.assertIn("the network", evidence)


if __name__ == "__main__":
    unittest.main()
