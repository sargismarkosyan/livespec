"""The audit tool, held to its rules. Standard library; every test names its rule.

Each test builds a small consuming repository in a temporary directory — the
bindings from the template, filled green — and reads what the tool says about
it. The plugin the tool reads is this repository, except where a test points it
at a fixture standing in for one.
"""

from __future__ import annotations

import json
import re
from datetime import date
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


def finished(root: Path, answer: str = "clear", why: str = "run: gh api → required: [checks]") -> Path:
    """The record the tool printed, with every judgment line answered, saved beside the repository."""
    lines = doctor.emit(doctor.context(root, root / "specs" / "setup" / "README.md"))
    for line in lines:
        if line["state"] == "unanswered" and line["id"] in doctor.JUDGMENT_IDS:
            line["state"], line["evidence"] = answer, why
    text = doctor.render(doctor.context(root, root / "specs" / "setup" / "README.md"), lines)
    path = Path(tempfile.mkdtemp(prefix="finished-")) / "audit.md"
    path.write_text(text, encoding="utf-8")
    return path


def edited(path: Path, old: str, new: str) -> Path:
    path.write_text(path.read_text().replace(old, new, 1), encoding="utf-8")
    return path


def validate(root: Path, path: Path) -> tuple[list[str], str, str]:
    return doctor.validate(doctor.context(root, root / "specs" / "setup" / "README.md"), path)


class TheRecord(unittest.TestCase):
    @rule("one-line-per-check-or-it-does-not-end")
    def test_one_line_short_is_refused_naming_the_id(self):
        root = repo()
        path = finished(root)
        edited(path, "| `check:mocked-clock` |", "| `check:mocked-clocks` |")
        problems, _, _ = validate(root, path)
        self.assertTrue(any("missing: check:mocked-clock" in p for p in problems), problems)
        self.assertFalse(doctor.record_path_of(doctor.context(root, root / "specs" / "setup" / "README.md")).exists(), "a refused record was written")

    @rule("one-line-per-check-or-it-does-not-end")
    def test_a_judgment_nobody_made_is_refused(self):
        root = repo()
        path = finished(root)
        edited(path, "| `check:merge-blocked` | clear |", "| `check:merge-blocked` | unanswered |")
        problems, _, _ = validate(root, path)
        self.assertTrue(any("still unanswered: check:merge-blocked" in p for p in problems), problems)

    @rule("one-line-per-check-or-it-does-not-end")
    def test_a_state_of_somebodys_own_is_refused(self):
        root = repo()
        path = finished(root)
        edited(path, "| `check:merge-blocked` | clear |", "| `check:merge-blocked` | done |")
        problems, _, _ = validate(root, path)
        self.assertTrue(any("unknown state 'done' on check:merge-blocked" in p for p in problems), problems)

    @rule("a-finding-carries-what-closes-it-and-a-skip-carries-why")
    def test_open_with_nothing_after_it_is_refused(self):
        root = repo()
        path = finished(root)
        edited(path, "| `check:merge-blocked` | clear | ", "| `check:merge-blocked` | open | ")
        text = path.read_text()
        head, _, tail = text.partition("| `check:merge-blocked` | open |")
        rest = tail.split("|", 3)  # since, evidence, remainder
        path.write_text(head + "| `check:merge-blocked` | open |" + rest[1] + "|  |" + "\n" + rest[3].split("\n", 1)[1], encoding="utf-8")
        problems, _, _ = validate(root, path)
        self.assertTrue(any("open with nothing that closes it" in p for p in problems), problems)

    @rule("a-finding-carries-what-closes-it-and-a-skip-carries-why")
    def test_not_read_with_why_validates_and_the_reply_says_so(self):
        root = repo()
        path = finished(root, answer="not-read", why="gh: not logged in — run from a machine with credentials")
        problems, _, answer = validate(root, path)
        self.assertEqual(problems, [])
        self.assertIn("## Not read — ", answer)
        self.assertIn("`check:merge-blocked` — gh: not logged in", answer)

    @rule("a-finding-carries-what-closes-it-and-a-skip-carries-why")
    def test_clear_with_no_receipt_is_refused(self):
        root = repo()
        path = finished(root, answer="clear", why="looked fine")
        problems, _, _ = validate(root, path)
        self.assertTrue(any("no command beside it" in p for p in problems), problems)

    @rule("the-record-is-kept-where-the-bindings-say")
    def test_a_line_that_did_not_change_keeps_its_date_and_one_that_did_resets(self):
        root = repo()
        record = doctor.record_path_of(doctor.context(root, root / "specs" / "setup" / "README.md"))
        first = finished(root)
        problems, text, _ = validate(root, first)
        self.assertEqual(problems, [])
        self.assertTrue(record.exists())
        old_date = "2025-01-01"
        record.write_text(record.read_text().replace(f"| `check:stamp-present` | clear | {date.today().isoformat()} |", f"| `check:stamp-present` | clear | {old_date} |"), encoding="utf-8")
        second = finished(root, answer="not-read", why="no network today")
        problems, text, answer = validate(root, second)
        self.assertEqual(problems, [])
        self.assertIn(f"| `check:stamp-present` | clear | {old_date} |", text, "an unchanged line lost its date")
        self.assertIn(f"| `check:merge-blocked` | not-read | {date.today().isoformat()} |", text, "a changed line kept an old date")
        self.assertIn("· audit 2**", text)
        self.assertIn("Since ", answer)

    @rule("the-record-is-kept-where-the-bindings-say")
    def test_a_line_that_closed_is_named_once_in_the_reply(self):
        root = repo(inject.green_bindings("0.6.0"))
        path = finished(root)
        problems, _, first = validate(root, path)
        self.assertEqual(problems, [])
        self.assertIn("`check:stamp-range` (record)", first)
        bindings = root / "specs" / "setup" / "README.md"
        bindings.write_text(bindings.read_text().replace("livespec 0.6.0 on", f"livespec {INSTALLED} on"), encoding="utf-8")
        problems, _, second = validate(root, finished(root))
        self.assertEqual(problems, [])
        self.assertIn("closed: check:stamp-range", second)

    @rule("corrections-touch-only-the-record")
    def test_a_fix_that_strayed_is_refused_naming_the_file(self):
        root = repo()
        subprocess.run(["git", "init", "-q"], cwd=root, check=True)
        subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@example.test", "add", "-A"], cwd=root, check=True)
        subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@example.test", "commit", "-q", "-m", "x"], cwd=root, check=True)
        (root / "src").mkdir()
        (root / "src" / "app.js").write_text("// wiring\n")
        subprocess.run(["git", "add", "src/app.js"], cwd=root, check=True)
        (root / "src" / "app.js").write_text("// changed\n")
        path = finished(root)
        problems, _, _ = validate(root, path)
        self.assertTrue(any("src/app.js" in p and "doctor wires nothing" in p for p in problems), problems)

    @rule("corrections-touch-only-the-record")
    def test_a_change_to_the_bindings_alone_validates(self):
        root = repo()
        subprocess.run(["git", "init", "-q"], cwd=root, check=True)
        subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@example.test", "add", "-A"], cwd=root, check=True)
        subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@example.test", "commit", "-q", "-m", "x"], cwd=root, check=True)
        bindings = root / "specs" / "setup" / "README.md"
        bindings.write_text(bindings.read_text() + "\nA corrected sentence.\n", encoding="utf-8")
        problems, _, _ = validate(root, finished(root))
        self.assertEqual(problems, [])


class TheReply(unittest.TestCase):
    @rule("the-reply-is-generated-from-the-record")
    def test_the_dangerous_thing_comes_first_and_the_sitting_line_only_when_wiring_is_left(self):
        text = inject.green_bindings(INSTALLED)
        text = "\n".join(line for line in text.splitlines() if "gate:structure" not in line) + "\n"  # wiring left: no row
        root = repo(text)
        path = finished(root, answer="open", why="run: gh api → merges are not blocked; closes: require the check in the ruleset")
        problems, _, answer = validate(root, path)
        self.assertEqual(problems, [])
        opened = [line for line in answer.splitlines() if line.startswith("- `check:")]
        self.assertTrue(opened[0].startswith("- `check:check-name` (platform)") or opened[0].startswith("- `check:credentials-present` (platform)") or opened[0].startswith("- `check:merge-blocked` (platform)"), opened[:3])
        self.assertLess(answer.index("(platform)"), answer.index("(wiring)"))
        self.assertIn("/livespec:setup", answer)
        tail = answer.rstrip().splitlines()
        command_at = next(i for i, line in enumerate(tail) if line == "/livespec:setup")
        self.assertTrue(all(line.strip().startswith("check:") for line in tail[command_at + 1:]), "the rows for the sitting follow the command, one per line")
        self.assertIn("check:row-per-gate", "\n".join(tail[command_at + 1:]))

    @rule("the-reply-is-generated-from-the-record")
    def test_nothing_open_ends_on_what_was_read_and_sends_nobody_anywhere(self):
        root = repo()
        problems, _, answer = validate(root, finished(root))
        self.assertEqual(problems, [])
        self.assertIn("## Open — 0", answer)
        self.assertNotIn("/livespec:setup", answer)

    @rule("a-decided-exception-is-reported-once-and-never-relitigated")
    def test_a_decided_row_is_listed_once_and_is_not_a_finding(self):
        text = inject.green_bindings(INSTALLED).replace(
            "| `gate:coverage` | lines, branches, functions | not applicable | no coverage here |",
            "| `gate:coverage` | lines, branches, functions | not applicable | decided: three lines of code, nothing to measure |", 1,
        )
        root = repo(text)
        lines = audit(root)
        self.assertEqual(lines["check:na-vs-tree"]["state"], "clear")
        problems, _, answer = validate(root, finished(root))
        self.assertEqual(problems, [])
        self.assertIn("## Decided — 1", answer)
        self.assertEqual(answer.count("gate:coverage"), 1)

    @rule("a-decided-exception-is-reported-once-and-never-relitigated")
    def test_the_tree_disagreeing_with_a_decision_goes_to_a_mind_as_evidence(self):
        text = inject.green_bindings(INSTALLED).replace(
            "| `gate:coverage` | lines, branches, functions | not applicable | no coverage here |",
            "| `gate:coverage` | lines, branches, functions | not applicable | decided: no personas here, the audience is inline |", 1,
        )
        root = repo(text, files={"specs/personas/reader.md": "@persona:reader\n"})
        lines = audit(root)
        self.assertEqual(lines["check:na-vs-tree"]["state"], "clear", "a decided row was re-litigated by the tool")
        problems, _, answer = validate(root, finished(root))
        self.assertEqual(problems, [])
        self.assertIn("evidence for a mind: specs/personas/ has 1 file(s)", answer)

    @rule("a-decided-exception-is-reported-once-and-never-relitigated")
    def test_a_gap_nobody_decided_is_open(self):
        text = inject.green_bindings(INSTALLED).replace("| not applicable | no coverage here |", "| not applicable | no personas exist |", 1)
        lines = audit(repo(text, files={"specs/personas/reader.md": "@persona:reader\n"}))
        self.assertEqual(lines["check:na-vs-tree"]["state"], "open")


class TheExit(unittest.TestCase):
    @rule("the-outcome-is-readable-from-the-exit-alone")
    def test_no_bindings_exits_three_and_offers_the_sitting(self):
        empty = Path(tempfile.mkdtemp(prefix="none-"))
        result = subprocess.run([sys.executable, str(ROOT / "tools" / "doctor.py")], cwd=empty, capture_output=True, text=True)
        self.assertEqual(result.returncode, 3)
        self.assertIn("/livespec:setup", result.stdout)

    @rule("the-outcome-is-readable-from-the-exit-alone")
    def test_open_findings_are_exit_zero_and_a_refused_record_is_one(self):
        root = repo(inject.green_bindings("0.6.0"))
        printed = subprocess.run([sys.executable, str(ROOT / "tools" / "doctor.py")], cwd=root, capture_output=True, text=True)
        self.assertEqual(printed.returncode, 0)
        self.assertIn("| `check:stamp-range` | open |", printed.stdout)
        path = root / "unfinished.md"
        path.write_text(printed.stdout, encoding="utf-8")
        refused = subprocess.run([sys.executable, str(ROOT / "tools" / "doctor.py"), "--validate", str(path)], cwd=root, capture_output=True, text=True)
        self.assertEqual(refused.returncode, 1)
        self.assertIn("still unanswered: check:merge-blocked", refused.stderr)
        accepted = subprocess.run([sys.executable, str(ROOT / "tools" / "doctor.py"), "--validate", str(finished(root))], cwd=root, capture_output=True, text=True)
        self.assertEqual(accepted.returncode, 0, accepted.stderr)
        self.assertTrue(accepted.stdout.startswith("# Audit — "))


FIXTURES = ROOT / "tests" / "fixtures" / "bindings"


def fixture_repo(name: str, latest: str = "0040") -> Path:
    """A consuming repository carrying a bindings file somebody else typed, at a plausible change number."""
    return repo((FIXTURES / name).read_text(encoding="utf-8"), files={f"specs/changes/{latest}-later.md": "# later\n"})


def live_repo() -> Path:
    """This repository's own bindings as they stand, in a temporary root."""
    return repo((ROOT / "specs" / "setup" / "README.md").read_text(encoding="utf-8"), files={"specs/changes/0043-later.md": "# later\n"})


class BindingsSomebodyElseTyped(unittest.TestCase):
    @rule("the-record-is-read-as-typed-not-as-templated")
    def test_toil_trackers_bold_stamp_with_a_parenthetical_is_read(self):
        lines = audit(fixture_repo("toil-tracker-3cd5b19.md"))
        self.assertEqual(lines["check:stamp-present"]["state"], "clear", lines["check:stamp-present"]["evidence"])
        self.assertIn("1.3.0 on 2026-09-08", lines["check:stamp-present"]["evidence"])
        self.assertEqual(lines["check:stamp-range"]["state"], "open", "1.3.0 is behind the plugin installed")

    @rule("the-record-is-read-as-typed-not-as-templated")
    def test_toil_trackers_longer_heading_still_finds_the_table(self):
        evidence = audit(fixture_repo("toil-tracker-3cd5b19.md"))["check:ledger-shape"]["evidence"]
        self.assertIn("gates: pre-template", evidence)
        self.assertNotIn("gates: missing", evidence)
        matched = int(re.search(r"(\d+) row\(s\) match an id by alias", evidence).group(1))
        self.assertGreaterEqual(matched, 10, evidence)

    @rule("the-record-is-read-as-typed-not-as-templated")
    def test_toil_trackers_second_table_rows_are_found_in_their_own_words(self):
        lines = audit(fixture_repo("toil-tracker-3cd5b19.md"))
        self.assertEqual(lines["check:rule-bound-row"]["state"], "clear", lines["check:rule-bound-row"]["evidence"])
        self.assertEqual(lines["check:pr-report-row"]["state"], "clear", lines["check:pr-report-row"]["evidence"])

    @rule("the-record-is-read-as-typed-not-as-templated")
    def test_the_reference_repository_reads_without_a_crash_and_truthfully(self):
        lines = audit(fixture_repo("todo-change-c89e9dc.md"))
        self.assertEqual(len(lines), len(doctor.CHECKS), "one line per check the method has, however many that is today")
        self.assertIn("gates: missing", lines["check:ledger-shape"]["evidence"])
        self.assertEqual(lines["check:stamp-present"]["state"], "open")
        self.assertEqual(lines["check:second-table"]["state"], "open")

    @rule("the-record-is-read-as-typed-not-as-templated")
    def test_this_repository_at_1_3_0_is_matched_by_alias(self):
        lines = audit(fixture_repo("livespec-1.3.0.md"))
        self.assertIn("pre-template", lines["check:ledger-shape"]["evidence"])
        matched = int(re.search(r"(\d+) row\(s\) match an id by alias", lines["check:ledger-shape"]["evidence"]).group(1))
        self.assertGreaterEqual(matched, 13)
        self.assertEqual(lines["check:stamp-range"]["state"], "open")
        self.assertIn("gate:boundary-double", lines["check:stamp-range"]["evidence"])

    @rule("a-judgment-line-arrives-with-its-command")
    def test_the_command_in_toil_trackers_fenced_block_reaches_the_platform_line(self):
        lines = audit(fixture_repo("toil-tracker-3cd5b19.md"))
        self.assertIn("run: gh api repos/sargismarkosyan/toil-tracker/branches/main/protection", lines["check:merge-blocked"]["evidence"])

    @rule("a-judgment-line-arrives-with-its-command")
    def test_this_repositorys_block_wins_over_the_inline_mention_said_to_fail(self):
        evidence = audit(live_repo())["check:merge-blocked"]["evidence"]
        handed = evidence.split(" — ")[0]
        self.assertIn("run: gh api repos/sargismarkosyan/livespec/rules/branches/main", handed, evidence)
        self.assertNotIn("branches/main/protection", handed, "the inline mention the section says will 404 was handed over")

    @rule("a-judgment-line-arrives-with-its-command")
    def test_a_step_that_needs_no_credential_is_not_a_missing_one(self):
        self.assertEqual(audit(live_repo())["check:credentials-present"]["state"], "n/a")
        text = inject.green_bindings(INSTALLED).replace("## Notes from the sitting\n\n", "## Notes from the sitting\n\nThe report token is not set in CI.\n\n")
        line = audit(repo(text))["check:credentials-present"]
        self.assertEqual(line["state"], "unanswered")
        self.assertIn("claim a credential is missing", line["evidence"])

    @rule("a-judgment-line-arrives-with-its-command")
    def test_a_phrase_in_the_prose_is_a_question_not_a_finding(self):
        text = inject.green_bindings(INSTALLED).replace("## Notes from the sitting\n\n", "## Notes from the sitting\n\nThere is nothing to do at release time.\n\n")
        line = audit(repo(text))["check:prose-phrases"]
        self.assertEqual(line["state"], "unanswered")
        self.assertIn("'to do'", line["evidence"])

    @rule("a-skill-the-record-names-is-one-that-exists")
    def test_only_the_instruction_form_of_an_old_name_is_the_scripts_to_report(self):
        prose = repo(files={"CLAUDE.md": "# loop\n\nThe `feedback` skill was renamed to `todo` in 0.19.0.\n"})
        lines = audit(prose)
        self.assertEqual(lines["check:skill-names"]["state"], "clear", lines["check:skill-names"]["evidence"])
        self.assertIn("dated account", lines["check:word-not-a-skill"]["evidence"])
        instruction = repo(files={"CLAUDE.md": "# loop\n\nReport what you found with `/livespec:feedback`.\n"})
        line = audit(instruction)["check:skill-names"]
        self.assertEqual(line["state"], "open")
        self.assertIn("now /livespec:todo", line["evidence"])


class CheckOnly(unittest.TestCase):
    @rule("a-record-can-be-checked-without-being-rewritten")
    def test_check_leaves_the_record_byte_identical_and_prints_no_reply(self):
        root = repo()
        problems, _, _ = validate(root, finished(root))
        self.assertEqual(problems, [])
        record = doctor.record_path_of(doctor.context(root, root / "specs" / "setup" / "README.md"))
        before = record.read_bytes()
        result = subprocess.run([sys.executable, str(ROOT / "tools" / "doctor.py"), "--check", str(record)], cwd=root, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(result.stdout.startswith("✔ the record"), result.stdout)
        self.assertNotIn("# Audit —", result.stdout)
        self.assertEqual(record.read_bytes(), before, "check rewrote the record")

    @rule("a-record-can-be-checked-without-being-rewritten")
    def test_a_refused_record_checked_names_the_line(self):
        root = repo()
        path = finished(root)
        edited(path, "| `check:merge-blocked` | clear |", "| `check:merge-blocked` | unanswered |")
        result = subprocess.run([sys.executable, str(ROOT / "tools" / "doctor.py"), "--check", str(path)], cwd=root, capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn("still unanswered: check:merge-blocked", result.stderr)
