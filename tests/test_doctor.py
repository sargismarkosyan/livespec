"""The audit tool, held to its rules. Standard library; every test names its rule.

Each test builds a small consuming repository in a temporary directory — the
bindings from the template, filled green — and reads what the tool says about
it. The plugin the tool reads is this repository, except where a test points it
at a fixture standing in for one.
"""

from __future__ import annotations

import json
import os
import re
from datetime import date
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / ".github" / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import doctor  # noqa: E402
import inject  # noqa: E402
from rulelib import rule  # noqa: E402

INSTALLED = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text())["version"]

# Every test reads as Claude Code unless it says otherwise: the reply's last line
# follows the host running the tool, and verify.py is run from either. See
# specs/changes/0080.
CLAUDE_CODE = mock.patch.dict(os.environ)


def setUpModule() -> None:
    CLAUDE_CODE.start()
    os.environ.pop("PI_CODING_AGENT", None)


def tearDownModule() -> None:
    CLAUDE_CODE.stop()


def repo(bindings: str | None = None, files: dict[str, str] | None = None) -> Path:
    """A consuming repository in a temporary directory, green unless told otherwise."""
    root = Path(tempfile.mkdtemp(prefix="doctor-"))
    text = bindings if bindings is not None else inject.green_bindings(INSTALLED)
    (root / "specs" / "setup").mkdir(parents=True)
    (root / "specs" / "setup" / "README.md").write_text(text, encoding="utf-8")
    (root / "specs" / "changes").mkdir()
    (root / "specs" / "changes" / "0001-first.md").write_text("# Spec 0001\n", encoding="utf-8")
    (root / ".claude").mkdir()
    (root / ".claude" / "settings.json").write_text('{"enabledPlugins": {"livespec@livespec": true}}\n', encoding="utf-8")
    (root / "CLAUDE.md").write_text("# The loop\n\n`/livespec:refine-spec` writes the spec.\n\n```sh\npython3 trees.py new <name>\n```\n\n"
                                    "A description follows [specs/setup/pull-requests.md](specs/setup/pull-requests.md).\n", encoding="utf-8")
    (root / "specs" / "setup" / "pull-requests.md").write_text("# How a pull request description is written here\n", encoding="utf-8")
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
        table = {row["id"] for row in doctor.id_rows((ROOT / "method" / "requirements.md").read_text())}
        self.assertEqual({row["id"] for row in doctor.registry()}, table)

    @rule("the-table-and-the-tool-agree")
    def test_a_check_the_tool_has_and_the_table_lacks_is_red_here(self):
        root = Path(tempfile.mkdtemp(prefix="agree-"))
        inject.build(root)
        gates = root / "method" / "requirements.md"
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
        text = inject.green_bindings(INSTALLED).replace("| id | gate | state | evidence | reconciled |\n|---|---|---|---|---|", "| Gate | State | Wired by, or why not |\n|---|---|---|")
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

    @rule("the-tool-runs-nothing-it-read")
    def test_an_option_planted_in_the_records_head_leaves_no_mark(self):
        root = repo()
        inject.as_git_history(root, [("fix the thing, #1", {"src/app.js": "//\n"})])
        mark = root / "pwned"
        (root / "specs" / "setup" / "audit.md").write_text(f"**Audited 2026-01-01 · livespec 1.0.0 · stamp 1.0.0 · HEAD --output={mark} · audit 1**\n")
        line = audit(root)["check:loop-followed"]
        self.assertFalse(mark.exists(), "an option read from the record reached git")
        self.assertEqual(line["state"], "n/a")

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


class ThePlan(unittest.TestCase):
    @rule("the-plan-is-read-from-the-list")
    def test_the_plan_lists_what_the_list_asks_of_the_rows(self):
        root = Path(tempfile.mkdtemp(prefix="plan-"))
        row = lambda i, at: {"id": i, "label": i, "reconciled": at, "evidence": "`npm run trace --changes` — numbers"}
        ctx = {
            "root": root, "keys": {}, "stamp": "1.0.0",
            "gates": [row("gate:level", "1.1.0"), row("gate:behind", "1.0.0"), row("gate:old", "1.0.0")],
            "wiring": [row("wiring:moved", "1.0.0")],
            "ids": [
                {"id": "gate:level", "since": "1.1.0", "revised": "—", "retired": "—"},
                {"id": "gate:behind", "since": "1.1.0", "revised": "—", "retired": "—"},
                {"id": "gate:new", "since": "1.1.0", "revised": "—", "retired": "—"},
                {"id": "gate:old", "since": "0.9.0", "revised": "—", "retired": "1.1.0 → gate:new"},
                {"id": "wiring:moved", "since": "0.9.0", "revised": "1.1.0", "retired": "—"},
            ],
        }
        items = doctor.plan(ctx)
        self.assertTrue(any(i.startswith("wire    gate:behind") for i in items))
        self.assertTrue(any(i.startswith("wire    gate:new") and "no row" in i for i in items))
        retire = next(i for i in items if i.startswith("retire  gate:old"))
        for said in ("drop the row", "npm run trace --changes", "its fault and the prose", "gate:new"):
            self.assertIn(said, retire)
        self.assertTrue(any(i.startswith("reprove wiring:moved") for i in items))
        self.assertFalse(any("gate:level" in i for i in items), "a row already level was listed")
        shutil.rmtree(root)


class TheTransaction(unittest.TestCase):
    """The upgrade on file: opened from the plan, finalized against the record. See specs/changes/0105."""

    def sitting(self, ids):
        root = repo(inject.green_bindings("1.0.0"))
        inject.git_in(root, "init", "-q")
        inject.git_in(root, "add", "-A")
        inject.git_in(root, "commit", "-q", "-m", "x")
        return root, self.ctx(root, ids)

    def ctx(self, root, ids):
        ctx = doctor.context(root, root / "specs" / "setup" / "README.md")
        ctx.update(installed="1.1.0", ids=ids)
        return ctx

    def record(self, root, ctx, lines):
        body = "".join(f"| `{i}` | {state} | 2026-01-01 | {evidence} |\n" for i, state, evidence in lines)
        (root / "specs" / "setup" / "audit.md").write_text(f"**Audited 2026-01-01 · livespec 1.1.0 · stamp 1.0.0 · HEAD {ctx['head']} · audit 2**\n\n{body}")

    def answer(self, root, key, outcome, evidence):
        path = root / "specs" / "setup" / "upgrade.md"
        ledger = doctor.parse_ledger(path.read_text())
        next(i for i in ledger["items"] if i["key"] == key).update(outcome=outcome, evidence=evidence)
        path.write_text(doctor.render_ledger(ledger))

    IDS = [{"id": "gate:structure", "since": "1.1.0", "revised": "—", "retired": "—"},
           {"id": "check:new-one", "since": "1.1.0", "revised": "—", "retired": "—"}]

    @rule("the-upgrade-is-a-transaction-on-file")
    def test_the_plan_opens_a_transaction_and_a_second_is_refused(self):
        root, ctx = self.sitting(self.IDS)
        self.assertEqual(doctor.open_transaction(ctx)[0], 0)
        ledger = doctor.parse_ledger((root / "specs" / "setup" / "upgrade.md").read_text())
        self.assertEqual((ledger["state"], ledger["from"], ledger["to"], ledger["baseline"]), ("open", "1.0.0", "1.1.0", "1.0.0"))
        self.assertEqual([i["key"] for i in ledger["items"]], ["gate:structure@since:1.1.0", "check:new-one@since:1.1.0"])
        self.assertEqual(ledger["snapshot"]["gate:structure"], "1.0.0")
        code, said = doctor.open_transaction(self.ctx(root, self.IDS))
        self.assertEqual(code, 1)
        self.assertIn("resume it", said)

    @rule("the-upgrade-is-a-transaction-on-file")
    def test_a_newer_plugin_extends_the_open_transaction(self):
        root, ctx = self.sitting(self.IDS[:1])
        doctor.open_transaction(ctx)
        ctx = self.ctx(root, self.IDS + [{"id": "gate:later", "since": "1.2.0", "revised": "—", "retired": "—"}])
        ctx["installed"] = "1.2.0"
        self.assertEqual(doctor.open_transaction(ctx)[0], 0)
        ledger = doctor.parse_ledger((root / "specs" / "setup" / "upgrade.md").read_text())
        self.assertEqual(ledger["to"], "1.2.0")
        self.assertIn("gate:later@since:1.2.0", [i["key"] for i in ledger["items"]])

    @rule("finalize-raises-what-was-answered")
    def test_finalize_raises_the_answered_row_answers_the_clear_check_and_closes(self):
        root, ctx = self.sitting(self.IDS)
        doctor.open_transaction(ctx)
        self.answer(root, "gate:structure@since:1.1.0", "wired", "fault fired; verification green")
        self.record(root, ctx, [("check:new-one", "clear", "read"), ("check:row-per-gate", "clear", "every gate has a row")])
        code, said = doctor.finalize(self.ctx(root, self.IDS))
        self.assertEqual(code, 0, said)
        bindings = (root / "specs" / "setup" / "README.md").read_text()
        self.assertIn("| `gate:structure` |", bindings)
        self.assertRegex(bindings, r"\| `gate:structure` \|[^\n]*\| 1\.1\.0 \|")
        ledger = doctor.parse_ledger((root / "specs" / "setup" / "upgrade.md").read_text())
        self.assertEqual(ledger["state"], "closed")
        self.assertEqual(ledger["answers"], {"check:new-one": "1.1.0"})
        self.assertEqual(ledger["sittings"][0][2:], ["1.0.0 → 1.1.0", "—"])

    @rule("finalize-raises-what-was-answered")
    def test_a_row_the_record_still_finds_is_vetoed_and_keeps_its_cell(self):
        root, ctx = self.sitting(self.IDS)
        doctor.open_transaction(ctx)
        self.answer(root, "gate:structure@since:1.1.0", "wired", "fault fired")
        self.record(root, ctx, [("check:new-one", "open", "not yet"), ("check:row-evidence", "open", "gate:structure names no command")])
        self.assertEqual(doctor.finalize(self.ctx(root, self.IDS))[0], 0)
        self.assertRegex((root / "specs" / "setup" / "README.md").read_text(), r"\| `gate:structure` \|[^\n]*\| 1\.0\.0 \|")
        ledger = doctor.parse_ledger((root / "specs" / "setup" / "upgrade.md").read_text())
        self.assertEqual(ledger["state"], "open")
        self.assertEqual([i["outcome"] for i in ledger["items"]], ["pending", "pending"])
        self.assertIn("gate:structure@since:1.1.0", ledger["sittings"][0][3])

    @rule("finalize-raises-what-was-answered")
    def test_finalize_refuses_a_record_of_another_commit_and_an_answer_without_evidence(self):
        root, ctx = self.sitting(self.IDS)
        doctor.open_transaction(ctx)
        self.answer(root, "gate:structure@since:1.1.0", "wired", "")
        self.record(root, ctx, [])
        code, said = doctor.finalize(self.ctx(root, self.IDS))
        self.assertEqual((code, "answered with no evidence" in said), (1, True))
        self.answer(root, "gate:structure@since:1.1.0", "wired", "fault fired")
        (root / "specs" / "setup" / "audit.md").write_text("**Audited 2026-01-01 · livespec 1.1.0 · stamp 1.0.0 · HEAD abc1234 · audit 2**\n")
        code, said = doctor.finalize(self.ctx(root, self.IDS))
        self.assertEqual((code, "report again" in said), (1, True))

    @rule("the-upgrade-is-a-transaction-on-file")
    def test_a_check_answered_in_the_ledger_is_not_planned_again(self):
        root, ctx = self.sitting(self.IDS)
        (root / "specs" / "setup" / "upgrade.md").write_text(doctor.render_ledger({**doctor.parse_ledger(""), "baseline": "1.0.0", "answers": {"check:new-one": "1.1.0"}}))
        self.assertEqual([i["key"] for i in doctor.planned(self.ctx(root, self.IDS))], ["gate:structure@since:1.1.0"])


class ThePiTag(TheTransaction):
    """The repository's Pi pin bounds the ledger. See specs/changes/0106."""

    def pinned(self, ref, ids=None):
        root, _ = self.sitting(ids or self.IDS)
        (root / ".pi").mkdir()
        (root / ".pi" / "settings.json").write_text(f'{{"packages": ["git:github.com/sargismarkosyan/livespec@{ref}"]}}\n')
        return root, self.ctx(root, ids or self.IDS)

    @rule("the-pi-tag-bounds-the-ledger")
    def test_a_pin_below_the_ceiling_is_open_and_level_is_clear(self):
        root, ctx = self.pinned("livespec--v0.9.0")
        self.assertEqual(doctor.c_host_pin_current(ctx)[0], "open")
        root, ctx = self.pinned("livespec--v1.0.0")
        self.assertEqual(doctor.c_host_pin_current(ctx)[0], "clear")

    @rule("the-pi-tag-bounds-the-ledger")
    def test_a_branch_is_open_unless_kept_on_purpose(self):
        root, ctx = self.pinned("main")
        self.assertIn("not a release tag", doctor.c_host_pin_current(ctx)[1])
        ctx["text"] += "\n| **Where the plugin is enabled** | Pi: decided: non-release pin kept main |\n"
        self.assertEqual(doctor.c_host_pin_current(ctx)[0], "n/a")

    @rule("the-pi-tag-bounds-the-ledger")
    def test_an_answer_above_the_pin_is_held_and_the_move_never_holds_it_open(self):
        root, ctx = self.pinned("livespec--v1.0.0")
        doctor.open_transaction(ctx)
        ledger = doctor.parse_ledger((root / "specs" / "setup" / "upgrade.md").read_text())
        self.assertIn("host:tag@1.1.0@sitting#1", [i["key"] for i in ledger["items"]])
        self.answer(root, "gate:structure@since:1.1.0", "wired", "fault fired")
        self.record(root, ctx, [("check:new-one", "clear", "read")])
        code, said = doctor.finalize(self.ctx(root, self.IDS))
        self.assertEqual(code, 0, said)
        self.assertIn("held at the Pi tag 1.0.0", said)
        self.assertRegex((root / "specs" / "setup" / "README.md").read_text(), r"\| `gate:structure` \|[^\n]*\| 1\.0\.0 \|")
        ledger = doctor.parse_ledger((root / "specs" / "setup" / "upgrade.md").read_text())
        self.assertEqual(ledger["state"], "open")
        self.assertEqual(ledger["sittings"][0][3], "gate:structure@since:1.1.0")


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
        inject.git_in(root, "init", "-q")
        inject.git_in(root, "add", "-A")
        inject.git_in(root, "commit", "-q", "-m", "x")
        (root / "src").mkdir()
        (root / "src" / "app.js").write_text("// wiring\n")
        inject.git_in(root, "add", "src/app.js")
        (root / "src" / "app.js").write_text("// changed\n")
        path = finished(root)
        problems, _, _ = validate(root, path)
        self.assertTrue(any("src/app.js" in p and "doctor wires nothing" in p for p in problems), problems)

    @rule("corrections-touch-only-the-record")
    def test_a_staged_fix_that_strayed_is_refused(self):
        root = repo()
        inject.git_in(root, "init", "-q")
        inject.git_in(root, "add", "-A")
        inject.git_in(root, "commit", "-q", "-m", "x")
        (root / "src").mkdir()
        (root / "src" / "app.js").write_text("// wiring\n")
        inject.git_in(root, "add", "src/app.js")
        problems, _, _ = validate(root, finished(root))
        self.assertTrue(any("src/app.js" in p for p in problems), problems)

    @rule("corrections-touch-only-the-record")
    def test_a_lowered_cell_is_refused(self):
        root = repo(inject.green_bindings("1.1.0"))
        inject.git_in(root, "init", "-q")
        inject.git_in(root, "add", "-A")
        inject.git_in(root, "commit", "-q", "-m", "x")
        bindings = root / "specs" / "setup" / "README.md"
        text = bindings.read_text()
        bindings.write_text(text.replace("| 1.1.0 |", "| 1.0.0 |", 1), encoding="utf-8")
        problems, _, _ = validate(root, finished(root))
        self.assertTrue(any("from 1.1.0 to 1.0.0" in p for p in problems), problems)

    @rule("corrections-touch-only-the-record")
    def test_a_change_to_the_bindings_alone_validates(self):
        root = repo()
        inject.git_in(root, "init", "-q")
        inject.git_in(root, "add", "-A")
        inject.git_in(root, "commit", "-q", "-m", "x")
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

    @rule("a-decided-exception-is-reported-once-and-never-relitigated")
    def test_no_code_beside_code_in_the_tree_is_open(self):
        text = inject.green_bindings(INSTALLED).replace("| not applicable | no coverage here |", "| not applicable | there is no application code to measure |", 1)
        line = audit(repo(text, files={"tools/doctor.py": "print(1)\n", "tests/test_x.py": "", "evals/a/run.py": ""}))["check:na-vs-tree"]
        self.assertEqual(line["state"], "open")
        self.assertIn("2 source file(s), in evals, tools", line["evidence"])

    @rule("a-decided-exception-is-reported-once-and-never-relitigated")
    def test_a_reason_it_cannot_read_is_named(self):
        line = audit(repo())["check:na-vs-tree"]
        self.assertEqual(line["state"], "clear")
        self.assertIn("naming nothing it holds: gate:coverage", line["evidence"])


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

    @rule("a-gap-is-a-row-not-a-sentence")
    def test_a_layer_readme_saying_not_written_yet_is_asked_about(self):
        line = audit(repo(files={"specs/workflows/README.md": "# Workflows\n\n## Three more attempts, not written yet\n"}))["check:prose-phrases"]
        self.assertEqual(line["state"], "unanswered")
        self.assertIn("specs/workflows/README.md:L3 'not written yet'", line["evidence"])

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


class TheHost(unittest.TestCase):
    """Pi beside Claude Code: the instruction in either form, the last line in the host's, one instructions file."""

    @rule("an-instruction-in-either-hosts-form-is-read")
    def test_a_skill_named_in_pis_form_is_read_and_found(self):
        lines = audit(repo(files={"CLAUDE.md": "# loop\n\nType `/skill:refine-spec` to write the spec.\n"}))
        self.assertEqual(lines["check:skill-names"]["state"], "clear", lines["check:skill-names"]["evidence"])
        self.assertIn("refine-spec", lines["check:skill-names"]["evidence"])
        self.assertNotIn("refine-spec", lines["check:word-not-a-skill"]["evidence"], "an instruction read as prose")

    @rule("an-instruction-in-either-hosts-form-is-read")
    def test_an_old_name_in_pis_form_is_answered_in_pis_form(self):
        line = audit(repo(files={"CLAUDE.md": "# loop\n\nReport what you found with `/skill:feedback`.\n"}))["check:skill-names"]
        self.assertEqual(line["state"], "open")
        self.assertIn("/skill:feedback — now /skill:todo", line["evidence"])
        unknown = audit(repo(files={"CLAUDE.md": "# loop\n\nRun `/skill:nonesuch`.\n"}))["check:skill-names"]
        self.assertEqual(unknown["state"], "open")
        self.assertIn("/skill:nonesuch — no such skill", unknown["evidence"])

    def _wiring_left(self) -> str:
        text = inject.green_bindings(INSTALLED)
        text = "\n".join(line for line in text.splitlines() if "gate:structure" not in line) + "\n"
        root = repo(text)
        problems, _, answer = validate(root, finished(root))
        self.assertEqual(problems, [])
        return answer

    @rule("the-sitting-is-named-as-the-host-types-it")
    def test_under_pi_the_sitting_is_skill_setup(self):
        with mock.patch.dict(os.environ, {"PI_CODING_AGENT": "true"}):
            answer = self._wiring_left()
        tail = answer.rstrip().splitlines()
        self.assertIn("/skill:setup", tail)
        self.assertNotIn("/livespec:setup", answer)
        command_at = tail.index("/skill:setup")
        self.assertIn("check:row-per-gate", "\n".join(tail[command_at + 1:]))

    @rule("the-sitting-is-named-as-the-host-types-it")
    def test_under_claude_code_the_sitting_is_livespec_setup_as_before(self):
        answer = self._wiring_left()
        self.assertIn("/livespec:setup", answer.splitlines())
        self.assertNotIn("/skill:setup", answer)

    @rule("the-sitting-is-named-as-the-host-types-it")
    def test_no_bindings_offers_the_sitting_in_the_hosts_form(self):
        empty = Path(tempfile.mkdtemp(prefix="none-"))
        env = dict(os.environ, PI_CODING_AGENT="true")
        result = subprocess.run([sys.executable, str(ROOT / "tools" / "doctor.py")], cwd=empty, capture_output=True, text=True, env=env)
        self.assertEqual(result.returncode, 3)
        self.assertIn("Run: /skill:setup", result.stdout)

    @rule("a-second-instructions-file-is-open")
    def test_agents_md_beside_the_claude_md_the_gates_hold_is_open_wiring(self):
        text = inject.green_bindings(INSTALLED)
        root = repo(text, files={"AGENTS.md": "# The loop\n\nThe owner's notes.\n"})
        line = audit(root)["check:one-context-file"]
        self.assertEqual(line["state"], "open")
        self.assertIn("Pi reads AGENTS.md and never reads CLAUDE.md", line["evidence"])
        self.assertIn("setup sitting", line["evidence"])
        self.assertEqual(doctor.severity_of("check:one-context-file"), "wiring", "the sitting closes it, so the reply sends it there")

    @rule("a-second-instructions-file-is-open")
    def test_one_file_is_clear_and_none_is_not_applicable(self):
        only_agents = repo()
        (only_agents / "CLAUDE.md").rename(only_agents / "AGENTS.md")
        line = audit(only_agents)["check:one-context-file"]
        self.assertEqual(line["state"], "clear", line["evidence"])
        self.assertIn("AGENTS.md", line["evidence"])
        self.assertEqual(audit(repo())["check:one-context-file"]["state"], "clear")
        none = repo()
        (none / "CLAUDE.md").unlink()
        self.assertEqual(audit(none)["check:one-context-file"]["state"], "n/a")


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


class Trees(unittest.TestCase):
    """Where trees live and what makes them, read back by the tool. See specs/changes/0073."""

    @rule("the-trees-row-is-there")
    def test_bindings_with_no_trees_row_read_open_and_name_the_sitting(self):
        lines = audit(repo(inject.green_bindings(INSTALLED).replace(inject.ROW_TREES + "\n", "")))
        self.assertEqual(lines["check:trees-row"]["state"], "open")
        self.assertIn("setup sitting", lines["check:trees-row"]["evidence"])
        self.assertEqual(lines["check:fresh-tree-green"]["state"], "n/a")

    @rule("the-trees-row-is-there")
    def test_a_row_the_context_file_carries_reads_clear_and_hands_the_command_on(self):
        lines = audit(repo())
        self.assertEqual(lines["check:trees-row"]["state"], "clear", lines["check:trees-row"]["evidence"])
        self.assertEqual(lines["check:fresh-tree-green"]["state"], "unanswered")
        self.assertIn("python3 trees.py new <throwaway>", lines["check:fresh-tree-green"]["evidence"])
        self.assertIn("clean", lines["check:fresh-tree-green"]["evidence"])

    @rule("the-trees-row-is-there")
    def test_a_context_file_that_never_learned_the_command_reads_open(self):
        lines = audit(repo(files={"CLAUDE.md": "# The loop\n\n`/livespec:refine-spec` writes the spec.\n"}))
        self.assertEqual(lines["check:trees-row"]["state"], "open")
        self.assertIn("CLAUDE.md", lines["check:trees-row"]["evidence"])


class Claims(unittest.TestCase):
    """The marker that says an issue is taken, read back by the tool. See specs/changes/0074."""

    @rule("the-claim-row-is-there")
    def test_bindings_with_no_claim_row_read_open_and_name_the_sitting(self):
        lines = audit(repo(inject.green_bindings(INSTALLED).replace(inject.ROW_CLAIM + "\n", "")))
        self.assertEqual(lines["check:claim-row"]["state"], "open")
        self.assertIn("setup sitting", lines["check:claim-row"]["evidence"])
        self.assertEqual(lines["check:claims-in-flight"]["state"], "n/a")

    @rule("the-claim-row-is-there")
    def test_a_row_naming_a_label_reads_clear_and_hands_the_label_on(self):
        lines = audit(repo())
        self.assertEqual(lines["check:claim-row"]["state"], "clear", lines["check:claim-row"]["evidence"])
        self.assertIn("`in-progress`", lines["check:claim-row"]["evidence"])
        self.assertEqual(lines["check:claims-in-flight"]["state"], "unanswered")
        self.assertIn("gh issue list --label in-progress", lines["check:claims-in-flight"]["evidence"])
        self.assertIn("release none", lines["check:claims-in-flight"]["evidence"])

    @rule("the-claim-row-is-there")
    def test_a_repository_with_no_tracker_decides_the_row_and_reads_nothing(self):
        decided = "| **Claiming an issue** | not applicable, decided: there is no tracker |"
        lines = audit(repo(inject.green_bindings(INSTALLED).replace(inject.ROW_CLAIM, decided)))
        self.assertEqual(lines["check:claim-row"]["state"], "clear")
        self.assertEqual(lines["check:claims-in-flight"]["state"], "n/a")

    @rule("the-claim-row-is-there")
    def test_a_row_naming_no_marker_reads_open(self):
        vague = "| **Claiming an issue** | we put a label on it |"
        lines = audit(repo(inject.green_bindings(INSTALLED).replace(inject.ROW_CLAIM, vague)))
        self.assertEqual(lines["check:claim-row"]["state"], "open")


class Stacks(unittest.TestCase):
    """Where a stacked pull request lands, read back by the audit. See specs/changes/0075."""

    @rule("the-delete-on-merge-setting-is-read-back")
    def test_the_setting_is_handed_to_a_mind_with_the_protection_read_back(self):
        lines = audit(repo())
        line = lines["check:merged-branch-deleted"]
        self.assertEqual(line["state"], "unanswered")
        self.assertEqual(line["severity"], "platform")
        self.assertIn("retargeted", line["evidence"])
        self.assertTrue(line["evidence"].startswith("run: "), line["evidence"])

    @rule("a-merge-that-missed-main-is-listed")
    def test_the_look_back_starts_at_the_stamp_and_moves_nothing(self):
        root = repo()
        ctx = doctor.context(root, root / "specs" / "setup" / "README.md")
        line = {l["id"]: l for l in doctor.emit(ctx)}["check:merged-off-main"]
        self.assertEqual(line["state"], "unanswered")
        self.assertIn(f"since {ctx['stamp_date']}", line["evidence"])
        self.assertIn("move nothing", line["evidence"])


class EveryHost(unittest.TestCase):
    """Every host in use loads the plugin from a committed file. See specs/changes/0101."""

    @rule("every-host-in-use-loads-it")
    def test_claude_code_declared_is_clear(self):
        line = audit(repo())["check:host-enabled"]
        self.assertEqual(line["state"], "clear", line["evidence"])
        self.assertIn("`livespec@livespec` in .claude/settings.json", line["evidence"])

    @rule("every-host-in-use-loads-it")
    def test_a_host_the_tree_shows_with_nothing_declared_is_open(self):
        line = audit(repo(files={".pi/settings.json": '{"packages": ["npm:other"]}\n'}))["check:host-enabled"]
        self.assertEqual((line["state"], line["severity"]), ("open", "wiring"))
        self.assertIn("Pi in use here", line["evidence"])

    @rule("every-host-in-use-loads-it")
    def test_the_host_running_the_audit_is_in_use(self):
        with mock.patch.dict(os.environ, {"PI_CODING_AGENT": "true"}):
            line = audit(repo())["check:host-enabled"]
        self.assertEqual(line["state"], "open")
        self.assertIn("Pi", line["evidence"])

    @rule("every-host-in-use-loads-it")
    def test_the_plugins_own_checkout_by_a_local_path(self):
        root = repo(files={".pi/settings.json": '{"packages": [".."]}\n', ".claude-plugin/plugin.json": '{"name": "livespec"}\n'})
        line = audit(root)["check:host-enabled"]
        self.assertEqual(line["state"], "clear", line["evidence"])
        self.assertIn("a livespec checkout", line["evidence"])

class TheWholeContextFile(unittest.TestCase):
    """The context file read against all of claude-md.md, and the rules the history broke. See specs/changes/0102."""

    @rule("the-audit-reads-the-whole-context-file")
    def test_every_item_is_asked_after(self):
        items = len(re.findall(r"^\*\*(\d+)\. ", doctor.section(doctor.read(doctor.PLUGIN / "method" / "claude-md.md"), "What must be there"), re.M))
        line = audit(repo())["check:loop-per-claude-md"]
        self.assertEqual(line["state"], "unanswered")
        self.assertIn(f"all {items} items", line["evidence"])
        self.assertGreater(items, 6)
        self.assertNotIn("broken here", line["evidence"])

    @rule("the-audit-reads-the-whole-context-file")
    def test_a_rule_the_history_broke_is_asked_after(self):
        root = repo()
        inject.as_git_history(root, [("fix the thing", {"src/app.js": "// fixed\n"})])
        self.assertIn("carry spec before code", audit(root)["check:loop-per-claude-md"]["evidence"])


class ReadBackAge(unittest.TestCase):
    """A read-back dated before the last audit was not read again by it. See specs/changes/0103."""

    def aged(self, audited):
        root = repo(inject.green_bindings(INSTALLED) + "\nBranch protection: **last read back on 2026-01-01**.\n")
        (root / "specs" / "setup" / "audit.md").write_text(f"**Audited {audited} · livespec 1.0.0 · stamp 1.0.0 · HEAD abc1234 · audit 2**\n")
        return audit(root)["check:read-back-age"]

    @rule("a-read-back-ages-from-the-last-audit")
    def test_older_than_the_last_audit_is_open(self):
        line = self.aged("2026-04-01")
        self.assertEqual(line["state"], "open")
        self.assertIn("L", line["evidence"]); self.assertIn("2026-01-01", line["evidence"])

    @rule("a-read-back-ages-from-the-last-audit")
    def test_moved_by_the_last_audit_is_clear(self):
        self.assertEqual(self.aged("2026-01-01")["state"], "clear")

    @rule("a-read-back-ages-from-the-last-audit")
    def test_no_audit_yet_is_not_applicable(self):
        self.assertEqual(audit(repo())["check:read-back-age"]["state"], "n/a")


class KeyTable(unittest.TestCase):
    """The bindings' key table held to the template's. See specs/changes/0104."""

    @rule("the-key-table-is-held-to-the-template")
    def test_the_green_bindings_hold_every_row(self):
        line = audit(repo())["check:key-table-shape"]
        self.assertEqual(line["state"], "clear", line["evidence"])

    @rule("the-key-table-is-held-to-the-template")
    def test_a_missing_row_is_named(self):
        line = audit(repo(inject.green_bindings(INSTALLED).replace("| **Before the push** | none |\n", "")))["check:key-table-shape"]
        self.assertEqual(line["state"], "open")
        self.assertIn("*before the push*", line["evidence"])

    @rule("the-key-table-is-held-to-the-template")
    def test_bindings_set_up_before_the_template_row_are_asked_for_it(self):
        """Where the template is and what the release publishes, asked of an older repository. See 2026-11-23."""
        text = inject.green_bindings(INSTALLED)
        row = next(line for line in text.splitlines() if line.startswith("| **Pull request template** |"))
        line = audit(repo(text.replace(row + "\n", "")))["check:key-table-shape"]
        self.assertEqual(line["state"], "open")
        self.assertIn("*pull request template*", line["evidence"])

    @rule("the-key-table-is-held-to-the-template")
    def test_graded_case_forms_are_the_same_rows(self):
        text = (inject.green_bindings(INSTALLED).replace("| **How a test claims its rule** |", "| **How a case names its rule** |")
                .replace("| **Rule discovery** |", "| **Case discovery** |"))
        self.assertEqual(audit(repo(text))["check:key-table-shape"]["state"], "clear")


class DescriptionRules(unittest.TestCase):
    """The repository's own description rules: named, there, linked, then read. See 2026-11-23-the-rules-in-the-repository."""

    UNLINKED = "# The loop\n\n```sh\npython3 trees.py new <name>\n```\n"

    @rule("the-description-rules-are-the-repositorys-own")
    def test_no_row_is_open(self):
        text = inject.green_bindings(INSTALLED)
        row = next(line for line in text.splitlines() if line.startswith("| **Pull request description rules** |"))
        line = audit(repo(text.replace(row + "\n", "")))["check:pr-body-rules"]
        self.assertEqual(line["state"], "open")
        self.assertIn("templates/pull-request.md", line["evidence"])

    @rule("the-description-rules-are-the-repositorys-own")
    def test_a_named_file_that_is_not_there_is_open(self):
        root = repo()
        (root / "specs" / "setup" / "pull-requests.md").unlink()
        line = audit(root)["check:pr-body-rules"]
        self.assertEqual(line["state"], "open")
        self.assertIn("not there", line["evidence"])

    @rule("the-description-rules-are-the-repositorys-own")
    def test_a_file_the_context_file_never_links_is_open(self):
        line = audit(repo(files={"CLAUDE.md": self.UNLINKED}))["check:pr-body-rules"]
        self.assertEqual(line["state"], "open")
        self.assertIn("does not link", line["evidence"])

    @rule("the-description-rules-are-the-repositorys-own")
    def test_rules_that_are_there_are_put_to_a_reading(self):
        line = audit(repo())["check:pr-body-rules"]
        self.assertEqual(line["state"], "unanswered", line["evidence"])
        self.assertIn("method/repository.md", line["evidence"])


class MainGreen(unittest.TestCase):
    """Whether the main branch's pipeline is green, asked of the platform. See specs/changes/0099."""

    @rule("main-is-read-green")
    def test_no_row_is_open_for_the_sitting(self):
        line = audit(repo(inject.green_bindings(INSTALLED).replace(inject.ROW_MAIN_RUNS + "\n", "")))["check:main-green"]
        self.assertEqual((line["state"], line["severity"]), ("open", "platform"))
        self.assertIn("setup sitting", line["evidence"])

    @rule("main-is-read-green")
    def test_the_row_hands_on_its_command_and_the_last_audit(self):
        root = repo()
        (root / "specs" / "setup" / "audit.md").write_text("**Audited 2026-01-02 · livespec 1.0.0 · stamp 1.0.0 · HEAD abc1234 · audit 1**\n")
        line = audit(root)["check:main-green"]
        self.assertEqual(line["state"], "unanswered")
        self.assertIn("run: gh run list --branch main --limit 20", line["evidence"])
        self.assertIn("since the last audit on 2026-01-02", line["evidence"])

    @rule("main-is-read-green")
    def test_nothing_running_there_is_not_applicable(self):
        row = "| **The main branch's runs** | not applicable, decided: no pipeline runs on main |"
        line = audit(repo(inject.green_bindings(INSTALLED).replace(inject.ROW_MAIN_RUNS, row)))["check:main-green"]
        self.assertEqual(line["state"], "n/a")


class ManyMerges(unittest.TestCase):
    """How several pull requests merge, read back by the audit. See specs/changes/0076."""

    @rule("the-queue-is-read-back")
    def test_bindings_with_no_row_read_open_and_name_the_sitting(self):
        lines = audit(repo(inject.green_bindings(INSTALLED).replace(inject.ROW_MERGES + "\n", "")))
        self.assertEqual(lines["check:merge-queue"]["state"], "open")
        self.assertIn("setup sitting", lines["check:merge-queue"]["evidence"])

    @rule("the-queue-is-read-back")
    def test_a_fallback_row_hands_on_its_own_read_back_and_asks_after_the_settings(self):
        line = audit(repo())["check:merge-queue"]
        self.assertEqual(line["state"], "unanswered")
        self.assertEqual(line["severity"], "platform")
        self.assertIn("run: gh api repos/o/r --jq .allow_update_branch", line["evidence"])
        self.assertIn("fallback", line["evidence"])

    @rule("the-queue-is-read-back")
    def test_a_queue_row_asks_after_the_event_the_checks_run_on(self):
        queued = "| **Several merges at once** | the merge queue, required on main; `checks.yml` runs on `merge_group`; read back with `gh api repos/o/r/rulesets` |"
        line = audit(repo(inject.green_bindings(INSTALLED).replace(inject.ROW_MERGES, queued)))["check:merge-queue"]
        self.assertEqual(line["state"], "unanswered")
        self.assertIn("gh api repos/o/r/rulesets", line["evidence"])
        self.assertIn("queue's own event", line["evidence"])


SPEC = "# Spec 0002: the thing\n\n- **Status:** approved\n- **Sketch:** not drawn — approval given in advance\n"


class TheLoop(unittest.TestCase):
    """Whether each change merged since the last audit followed the loop, read from git. See specs/changes/0098."""

    def loop(self, steps, merge=True):
        root = repo()
        inject.as_git_history(root, steps, merge)
        return audit(root)["check:loop-followed"]

    @rule("the-loop-is-read-from-the-history")
    def test_a_fix_with_no_spec_and_no_issue_is_open(self):
        line = self.loop([("fix the thing", {"src/app.js": "// fixed\n"})])
        self.assertEqual((line["state"], line["severity"]), ("open", "record"))
        self.assertIn("no change spec, and no issue", line["evidence"])

    @rule("the-loop-is-read-from-the-history")
    def test_the_light_path_names_its_issue(self):
        self.assertEqual(self.loop([("fix the pipeline, #12", {"ci.yml": "on: push\n"})])["state"], "clear")

    @rule("the-loop-is-read-from-the-history")
    def test_the_spec_first_with_its_sketch_line_is_clear(self):
        line = self.loop([("spec 0002: the thing", {"specs/changes/0002-the-thing.md": SPEC}), ("0002: the thing", {"src/app.js": "// built\n"})])
        self.assertEqual(line["state"], "clear", line["evidence"])

    @rule("the-loop-is-read-from-the-history")
    def test_code_before_its_spec_is_open(self):
        line = self.loop([("the thing", {"src/app.js": "// built\n"}), ("spec 0002: the thing", {"specs/changes/0002-the-thing.md": SPEC})])
        self.assertEqual(line["state"], "open")
        self.assertIn("implementation committed before its spec", line["evidence"])

    @rule("the-loop-is-read-from-the-history")
    def test_a_spec_with_no_sketch_line_is_named(self):
        line = self.loop([("spec 0002: the thing", {"specs/changes/0002-the-thing.md": "# Spec 0002\n"}), ("0002", {"src/app.js": "//\n"})])
        self.assertEqual(line["state"], "open")
        self.assertIn("0002-the-thing.md has no Sketch line", line["evidence"])

    @rule("the-loop-is-read-from-the-history")
    def test_a_squashed_change_is_not_read_for_order(self):
        line = self.loop([("the thing", {"src/app.js": "// built\n"}), ("spec 0002", {"specs/changes/0002-the-thing.md": SPEC})], merge=False)
        self.assertEqual(line["state"], "clear", line["evidence"])

    @rule("the-loop-is-read-from-the-history")
    def test_no_previous_audit_is_not_applicable(self):
        self.assertEqual(audit(repo())["check:loop-followed"]["state"], "n/a")


class DatedChanges(unittest.TestCase):
    """A change spec named by its day and slug is read as a change, beside the numbered ones before
    it. See specs/changes/2026-11-23-a-date-not-a-number.md."""

    DATED = "# Spec 2026-11-23: the thing\n\n- **Status:** approved\n- **Sketch:** not drawn — approval given in advance\n"

    @rule("a-change-spec-is-named-by-its-day-and-slug")
    def test_a_dated_spec_commit_before_its_build_is_clear(self):
        root = repo()
        inject.as_git_history(root, [
            ("spec 2026-11-23-the-thing: the thing", {"specs/changes/2026-11-23-the-thing.md": self.DATED}),
            ("2026-11-23-the-thing: the thing", {"src/app.js": "// built\n"}),
        ], True)
        line = audit(root)["check:loop-followed"]
        self.assertEqual(line["state"], "clear", line["evidence"])

    @rule("a-change-spec-is-named-by-its-day-and-slug")
    def test_a_dated_spec_is_a_day_and_never_the_number_of_its_year(self):
        self.assertEqual(doctor.change_of("2026-11-23-a-quieter-log.md"), ("d", "2026-11-23"))
        self.assertEqual(doctor.change_of("0078-a-number-nobody-else-holds.md"), ("n", 78))
        self.assertIsNone(doctor.change_of("README.md"))

    @rule("a-change-spec-is-named-by-its-day-and-slug")
    def test_the_clock_counts_later_days_and_never_the_same_one(self):
        changes = [("n", 1), ("n", 2), ("d", "2026-11-20"), ("d", "2026-11-20"), ("d", "2026-11-21")]
        self.assertEqual(doctor.changes_after(changes, ("n", 1)), 4)
        self.assertEqual(doctor.changes_after(changes, ("d", "2026-11-20")), 1)
        self.assertEqual(doctor.changes_after(changes, ("d", "2026-11-21")), 0)

    @rule("a-change-spec-is-named-by-its-day-and-slug")
    def test_a_row_mocked_since_a_dated_change_goes_past_the_clock(self):
        dated = "| `boundary:clock` | the clock | mocked | 2026-11-20-a-fake-clock | a fake clock nothing checks; cover: none |"
        root = repo(inject.green_bindings(INSTALLED).replace(inject.ROW_CLOCK, dated), {
            "specs/changes/2026-11-20-a-fake-clock.md": "# Spec 2026-11-20\n",
            "specs/changes/2026-11-21-a-quieter-log.md": "# Spec 2026-11-21\n",
        })
        self.assertEqual(audit(root)["check:mocked-clock"]["state"], "clear")
        (root / "specs" / "changes" / "2026-11-22-one-place.md").write_text("# Spec 2026-11-22\n", encoding="utf-8")
        line = audit(root)["check:mocked-clock"]
        self.assertEqual(line["state"], "open")
        self.assertIn("since 2026-11-20, latest change 2026-11-22 — 2 changes", line["evidence"])

    @rule("a-change-spec-is-named-by-its-day-and-slug")
    def test_a_ledger_still_carrying_the_number_gate_is_told_to_drop_it(self):
        row = "| `gate:change-number-unique` | two change specs sharing a number | automated | `python3 gate.py` | 3.13.0 |"
        green = inject.green_bindings(INSTALLED)
        anchor = next(l for l in green.splitlines() if l.startswith("| `gate:feature-to-feature`"))
        line = audit(repo(green.replace(anchor, row + "\n" + anchor)))["check:row-per-gate"]
        self.assertIn("gate:change-number-unique is retired", line["evidence"])
