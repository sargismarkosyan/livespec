#!/usr/bin/env python3
"""Break every gate on purpose, one fault at a time, and check each one fires.

A gate that has never failed is not known to be a gate. This builds a minimal
green fixture in a temporary directory — one persona, one journey, one workflow,
one feature, one rule, three eval cases — proves both gates pass on it, then
applies each fault in the table below to a fresh copy and reads the message that
comes back.

The release gate needs no fixture: `releaselib` is pure, so its faults are a
label list and a pull request body handed straight to the function that reads
them.

The fixture is synthetic on purpose. It has to keep proving the gates fire while
this repository's own spec layer is still empty, and it must not go green again
just because somebody deleted the file it was pointed at.

Run: python3 .github/scripts/inject.py
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
TRACE = SCRIPTS / "trace.py"
SUITE = SCRIPTS / "evalsuite.py"
BOARD = SCRIPTS / "board.py"
REPORT = SCRIPTS / "report.py"

GRADER = """---
type: llm
focus: last_message
weight: 1
---
The reply does the thing.
"""

FIXTURE: dict[str, str] = {
    "skills/refine-spec/SKILL.md": "---\nname: refine-spec\ndescription: Turns a request into a spec.\n---\n\n# Refine\n",
    "specs/personas/reader.md": "@persona:reader\n\n# Reader — wants the thing in front of them\n",
    "specs/journeys/arc.md": "@journey:arc\n\n# Arriving with a list already in hand\n",
    "specs/workflows/read-it.feature": (
        "@workflow:read-it @persona:reader @journey:arc\n"
        "Feature: Read the thing\n\n"
        "  Example: it opens on what was left\n"
        "    Given a list\n"
        "    When they come back\n"
        "    Then it is as they left it\n"
    ),
    "specs/features/core/core.feature": (
        "@feature:core @workflow:read-it\n"
        "Feature: The core of it\n\n"
        "  @rule:one\n"
        "  Rule: the thing is true\n\n"
        "    Example: it shows the thing\n"
        "      Given a list\n"
        "      When they look\n"
        "      Then the thing is there\n\n"
        "  @rule:two @refusal\n"
        "  Rule: nothing happens when nobody asked\n\n"
        "    Example: it stays out of the way\n"
        "      Given a list\n"
        "      When they ask about something else\n"
        "      Then nothing has been added\n"
    ),
    "evals/README.md": (
        "# The eval suite\n\n"
        "```\npython3 evals/runner/run.py --ablation with-without --judge-model sonnet --allow-tools Write\n```\n"
    ),
    "evals/case-rule/prompt.md": (
        "---\ntags: [skill:refine-spec, rule:one]\nallowed_tools: [Skill, Write]\nruns: 3\n---\nDo the thing.\n"
    ),
    "evals/case-rule/graders/outcome.md": GRADER,
    "evals/case-walk/prompt.md": "---\ntags: [skill:refine-spec, workflow:read-it]\nruns: 3\n---\nWalk it.\n",
    "evals/case-walk/graders/outcome.md": GRADER,
    "evals/case-neg/prompt.md": "---\ntags: [should-not-fire, rule:two]\nruns: 3\n---\nWrite me a commit message.\n",
    "evals/case-neg/graders/outcome.md": GRADER,
}


def build(root: Path) -> None:
    for relative, content in FIXTURE.items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
    # The board is generated rather than written literally: its entries carry
    # the measurement-inputs hash of the fixture as built, so the stale fault
    # below is one edit away and the unbroken fixture is fully measured.
    entries = {
        case["name"]: {
            "delta": 0.5, "with": 1.0, "without": 0.5, "runs": 3,
            "at": "2026-08-25", "sha": "0000000", "cost": 0.1,
            "inputs": measurement_inputs(case, root),
        }
        for case in cases(root)
    }
    (root / "evals" / "board.json").write_text(json.dumps({"format": 1, "cases": entries}, indent=1))


def drop_board_entry(root: Path, name: str) -> None:
    path = root / "evals" / "board.json"
    data = json.loads(path.read_text())
    del data["cases"][name]
    path.write_text(json.dumps(data, indent=1))


def edit(root: Path, relative: str, old: str, new: str) -> None:
    path = root / relative
    text = path.read_text()
    if old not in text:  # the fixture moved and the fault stopped being the fault
        raise SystemExit(f"inject: {relative} no longer contains {old!r}; the fixture and the faults disagree")
    path.write_text(text.replace(old, new, 1))


def write(root: Path, relative: str, content: str) -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def drop(root: Path, relative: str) -> None:
    target = root / relative
    shutil.rmtree(target) if target.is_dir() else target.unlink()


# --- the release gate ----------------------------------------------------------
#
# `version_gate.py` and `release.py` read a pull request's label and body through
# `releaselib`, which is pure — no git, no network, no filesystem. That is the
# whole reason it is a module rather than two copies of a regex: it can be broken
# here. The gate this replaced was never injectable, and so shipped for three
# versions without ever being known to fire.

sys.path.insert(0, str(SCRIPTS))
from caselib import cases, measurement_inputs  # noqa: E402
from releaselib import (  # noqa: E402
    ReleaseInputError,
    bump_manifest,
    extract_entry,
    extract_gherkin,
    moves_spec,
    next_version,
    prepend_entry,
    select_increment,
)

GOOD_BODY = (
    "Intro.\n\n## Changelog\n\nBody of the entry.\n\n## Notes\n\nnot part of it\n\n"
    "```gherkin\n  Rule: it holds\n```\n"
)

# (name, what to try, a phrase the refusal must contain)
RELEASE_FAULTS = [
    ("shipping change with no release label",
     lambda: select_increment(["bug", "needs-spec"]), "no release label"),
    ("two release labels at once",
     lambda: select_increment(["minor", "patch"]), "nobody decided"),
    ("pull request body with no changelog section",
     lambda: extract_entry("Intro.\n\n## Notes\n\nnothing here"), "no `## Changelog` section"),
    ("changelog section left empty",
     lambda: extract_entry("## Changelog\n\n## Notes\n\ntext"), "is empty"),
    ("a version that already has an entry",
     lambda: prepend_entry("# Changelog\n\n## 0.9.0 — x\n\nold\n", "0.9.0", "2026-01-01", "e"),
     "already has an entry"),
    ("a manifest with no version field",
     lambda: bump_manifest('{"name": "livespec"}', "0.9.0"), "no `version` field"),
    ("a version that is not major.minor.patch",
     lambda: next_version("0.8", "minor"), "not major.minor.patch"),
    ("spec-moving change whose body carries no gherkin",
     lambda: extract_gherkin("Intro.\n\n## Changelog\n\nBody."), "carries no Gherkin"),
    ("a gherkin block with nothing in it",
     lambda: extract_gherkin("Intro.\n\n```gherkin\n\n```\n"), "gherkin block is empty"),
]


def report_control() -> None:
    """The report may never exit non-zero, whatever it is handed.

    Not a fault table: there is nothing to break, because the whole promise is
    that nothing breaks. `gates.md` declares the report **not a gate** and
    `always-green` is what a report step going red would cost — so the check is
    that every degenerate input still leaves a zero exit and something printable.
    """
    import tempfile as _tempfile

    with _tempfile.TemporaryDirectory(prefix="livespec-report-") as workspace:
        good = Path(workspace) / "good.json"
        code, output = run(TRACE, SCRIPTS.parents[1], extra=["--json"])
        assert code == 0, "the traceability gate did not produce JSON for the report"
        good.write_text(output)
        bad = Path(workspace) / "bad.json"
        bad.write_text("not json at all")
        missing = Path(workspace) / "absent.json"

        for name, args in [
            ("both readings", [str(good), str(good)]),
            ("no base to compare against", [str(good), str(missing)]),
            ("an unreadable base", [str(good), str(bad)]),
            ("nothing readable at all", [str(bad)]),
            ("no arguments", []),
        ]:
            result = subprocess.run(
                [sys.executable, str(REPORT), *args], capture_output=True, text=True
            )
            assert result.returncode == 0, f"the report exited {result.returncode} on {name}"
            assert result.stdout.strip(), f"the report printed nothing on {name}"


def release_control() -> None:
    """The unbroken inputs, which must produce a release rather than a refusal."""
    assert select_increment(["bug", "minor"]) == "minor", "the one release label is not read"
    assert extract_entry(GOOD_BODY) == "Body of the entry.", "the entry is not taken verbatim"
    assert next_version("0.8.0", "minor") == "0.9.0", "the increment does not apply"
    assert '"version": "0.9.0"' in bump_manifest('{\n  "version": "0.8.0"\n}', "0.9.0")
    log = prepend_entry("# Changelog\n\nhead\n\n## 0.8.0 — x\n\nold\n", "0.9.0", "2026-01-01", "Body.")
    assert log.index("## 0.9.0") < log.index("## 0.8.0"), "the new entry is not on top"
    assert "Body." in log, "the entry did not survive into the changelog"
    assert extract_gherkin(GOOD_BODY) == "Rule: it holds", "the quoted Gherkin is not read"
    assert extract_gherkin(
        "see https://x.test/o/r/blob/" + "a" * 40 + "/specs/features/a.feature"
    ).endswith(".feature"), "a pinned Gherkin link is not accepted"
    assert moves_spec(["specs/workflows/README.md", "specs/features/a.feature"]) == [
        "specs/features/a.feature"
    ], "the spec surface is not what triggers the Gherkin check"


# (name, gate, mutation, expected outcome, a phrase the message must contain)
FAULTS = [
    ("live rule with no case", TRACE,
     lambda r: drop(r, "evals/case-rule"), "fails", "no eval case claims it"),
    ("case claims a rule that does not exist", TRACE,
     lambda r: edit(r, "evals/case-rule/prompt.md", "rule:one", "rule:nope"), "fails", "does not exist"),
    ("@planned rule that has a case", TRACE,
     lambda r: edit(r, "specs/features/core/core.feature", "@rule:one", "@rule:one @planned"), "fails", "should have come off"),
    ("feature naming no workflow", TRACE,
     lambda r: edit(r, "specs/features/core/core.feature", " @workflow:read-it", ""), "fails", "names no @workflow:"),
    ("feature naming a workflow that does not exist", TRACE,
     lambda r: edit(r, "specs/features/core/core.feature", "@workflow:read-it", "@workflow:nope"), "fails", "does not exist"),
    ("workflow claimed by no feature", TRACE,
     lambda r: drop(r, "specs/features/core/core.feature"), "fails", "claimed by no feature"),
    ("workflow walked by no case", TRACE,
     lambda r: drop(r, "evals/case-walk"), "fails", "walked by no eval case"),
    ("workflow naming a persona that does not exist", TRACE,
     lambda r: edit(r, "specs/workflows/read-it.feature", "@persona:reader", "@persona:nope"), "fails", "does not exist"),
    ("workflow naming no persona", TRACE,
     lambda r: edit(r, "specs/workflows/read-it.feature", " @persona:reader", ""), "fails", "names no live @persona:"),
    ("persona named by no workflow", TRACE,
     lambda r: write(r, "specs/personas/nobody.md", "@persona:nobody\n\n# Nobody\n"), "fails", "named by no workflow"),
    ("persona retired while a workflow still names them", TRACE,
     lambda r: edit(r, "specs/personas/reader.md", "@persona:reader", "@persona:reader @retired"), "fails", "names no live @persona:"),
    ("workflow naming a journey that does not exist", TRACE,
     lambda r: edit(r, "specs/workflows/read-it.feature", "@journey:arc", "@journey:nope"), "fails", "does not exist"),
    ("duplicate rule id", TRACE,
     lambda r: write(r, "specs/features/core/again.feature",
                     "@feature:again @workflow:read-it\nFeature: Again\n\n  @rule:one\n  Rule: also true\n\n"
                     "    Example: shows it\n      Given a\n      When b\n      Then c\n"), "fails", "ids are unique"),
    ("rule with no example", TRACE,
     lambda r: edit(r, "specs/features/core/core.feature",
                    "    Example: it shows the thing\n      Given a list\n      When they look\n      Then the thing is there\n", ""),
     "fails", "no example is an opinion"),
    ("example outside any rule", TRACE,
     lambda r: edit(r, "specs/features/core/core.feature", "Feature: The core of it\n",
                    "Feature: The core of it\n\n  Example: loose\n    Given a\n    When b\n    Then c\n"),
     "fails", "outside any Rule:"),
    ("refusal rule losing the tag that makes its case legitimate", TRACE,
     lambda r: edit(r, "specs/features/core/core.feature", "@rule:two @refusal", "@rule:two"),
     "warns", "promises a behaviour"),
    ("workflow naming no journey", TRACE,
     lambda r: edit(r, "specs/workflows/read-it.feature", " @journey:arc", ""), "warns", "names no @journey:"),
    ("case graded only by what fired", SUITE,
     lambda r: write(r, "evals/case-rule/graders/outcome.md", "---\ntype: tool_used\ntool: Skill\nmin: 1\n---\n"),
     "fails", "never by what came out"),
    ("case run fewer times than the floor", SUITE,
     lambda r: edit(r, "evals/case-rule/prompt.md", "runs: 3", "runs: 1"), "fails", "the floor is 3"),
    ("the last should-not-fire case removed", SUITE,
     lambda r: drop(r, "evals/case-neg"), "fails", "no should-not-fire case"),
    ("a skill held by no case", SUITE,
     lambda r: write(r, "skills/orphan/SKILL.md", "---\nname: orphan\ndescription: x\n---\n"), "fails", "held by no eval case"),
    ("the documented invocation loses its baseline", SUITE,
     lambda r: edit(r, "evals/README.md", "--ablation with-without ", ""), "fails", "no longer names"),
    ("a scaffold_script that names no file", SUITE,
     lambda r: write(r, "evals/case-rule/case.yaml", "scaffold_script: nope.sh\n"),
     "fails", "does not exist in the case directory"),
    ("a scaffolded case whose documented invocation never lays the fixture down", SUITE,
     lambda r: (write(r, "evals/case-rule/case.yaml", "scaffold_script: scaffold.sh\n"),
                write(r, "evals/case-rule/scaffold.sh", "mkdir -p specs\n")),
     "fails", "does not name '--scaffold'"),
    ("a gated tool a case asks for is never granted", SUITE,
     lambda r: edit(r, "evals/README.md", " --allow-tools Write", ""), "fails", "never grants"),
    ("a measurement whose inputs moved on", BOARD,
     lambda r: edit(r, "evals/case-rule/prompt.md", "Do the thing.", "Do the other thing."), "fails", "changed since"),
    ("a measurement whose rule was reworded", BOARD,
     lambda r: edit(r, "specs/features/core/core.feature", "the thing is there", "the thing is elsewhere"), "fails", "changed since"),
    ("a case the board has never measured", BOARD,
     lambda r: drop_board_entry(r, "case-walk"), "warns", "never measured"),
    ("an llm grader with an empty rubric", SUITE,
     lambda r: write(r, "evals/case-rule/graders/outcome.md", "---\ntype: llm\nweight: 1\n---\n"),
     "fails", "will pass on anything"),
    ("every case removed", SUITE,
     lambda r: [drop(r, f"evals/{c}") for c in ("case-rule", "case-walk", "case-neg")],
     "fails", "measurement of nothing"),
]


def run(gate: Path, root: Path, extra: list[str] | None = None) -> tuple[int, str]:
    result = subprocess.run(
        [sys.executable, str(gate), str(root), *(extra or [])], capture_output=True, text=True
    )
    return result.returncode, result.stdout + result.stderr


def main() -> int:
    problems: list[str] = []
    with tempfile.TemporaryDirectory(prefix="livespec-inject-") as workspace:
        control = Path(workspace) / "control"
        build(control)
        for gate in (TRACE, SUITE):
            code, output = run(gate, control)
            if code != 0:
                problems.append(f"the unbroken fixture fails {gate.name}:\n{output}")
        if problems:
            print("\n".join(problems), file=sys.stderr)
            return 1

        for index, (name, gate, mutate, expected, phrase) in enumerate(FAULTS):
            root = Path(workspace) / f"case{index:02d}"
            build(root)
            mutate(root)
            code, output = run(gate, root)
            if expected == "fails":
                ok = code != 0 and phrase in output
            else:
                ok = code == 0 and "⚠" in output and phrase in output
            print(f"    {'✔' if ok else '✘'} {name:<48} {expected}")
            if not ok:
                problems.append(f"{name}: expected it to {expected} naming {phrase!r}; exit {code}\n{output}")

    try:
        report_control()
    except AssertionError as error:
        problems.append(f"the report can fail a build: {error}")

    try:
        release_control()
    except AssertionError as error:
        problems.append(f"the unbroken release inputs do not release: {error}")

    for name, attempt, phrase in RELEASE_FAULTS:
        try:
            attempt()
        except ReleaseInputError as refusal:
            ok = phrase in str(refusal)
            detail = str(refusal)
        else:
            ok, detail = False, "it was accepted"
        print(f"    {'✔' if ok else '✘'} {name:<48} fails")
        if not ok:
            problems.append(f"{name}: expected a refusal naming {phrase!r}; got {detail}")

    if problems:
        print(f"\n{len(problems)} gate(s) did not fire as expected:\n", file=sys.stderr)
        for problem in problems:
            print(f"  ✘ {problem}\n", file=sys.stderr)
        return 1
    total = len(FAULTS) + len(RELEASE_FAULTS)
    print(f"✔ gate fault injection: {total}/{total} faults caught")
    return 0


if __name__ == "__main__":
    sys.exit(main())
