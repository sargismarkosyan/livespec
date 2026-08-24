#!/usr/bin/env python3
"""Break both gates on purpose, one fault at a time, and check each one fires.

A gate that has never failed is not known to be a gate. This builds a minimal
green fixture in a temporary directory — one persona, one journey, one workflow,
one feature, one rule, three eval cases — proves both gates pass on it, then
applies each fault in the table below to a fresh copy and reads the message that
comes back.

The fixture is synthetic on purpose. It has to keep proving the gates fire while
this repository's own spec layer is still empty, and it must not go green again
just because somebody deleted the file it was pointed at.

Run: python3 .github/scripts/inject.py
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
TRACE = SCRIPTS / "trace.py"
SUITE = SCRIPTS / "evalsuite.py"

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
        "      Then the thing is there\n"
    ),
    "evals/README.md": (
        "# The eval suite\n\n"
        "```\nclaude plugin eval . --ablation with-without --judge-model sonnet\n```\n"
    ),
    "evals/case-rule/prompt.md": "---\ntags: [skill:refine-spec, rule:one]\nruns: 3\n---\nDo the thing.\n",
    "evals/case-rule/graders/outcome.md": GRADER,
    "evals/case-walk/prompt.md": "---\ntags: [skill:refine-spec, workflow:read-it]\nruns: 3\n---\nWalk it.\n",
    "evals/case-walk/graders/outcome.md": GRADER,
    "evals/case-neg/prompt.md": "---\ntags: [should-not-fire]\nruns: 3\n---\nWrite me a commit message.\n",
    "evals/case-neg/graders/outcome.md": GRADER,
}


def build(root: Path) -> None:
    for relative, content in FIXTURE.items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)


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


# (name, gate, mutation, expected outcome, a phrase the message must contain)
FAULTS = [
    ("live rule with no case", TRACE,
     lambda r: drop(r, "evals/case-rule"), "fails", "no eval case claims it"),
    ("case claims a rule that does not exist", TRACE,
     lambda r: edit(r, "evals/case-rule/prompt.md", "rule:one", "rule:nope"), "fails", "does not exist"),
    ("case claims neither a rule nor a workflow", TRACE,
     lambda r: edit(r, "evals/case-rule/prompt.md", ", rule:one", ""), "fails", "claims neither"),
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
    ("an llm grader with an empty rubric", SUITE,
     lambda r: write(r, "evals/case-rule/graders/outcome.md", "---\ntype: llm\nweight: 1\n---\n"),
     "fails", "will pass on anything"),
    ("every case removed", SUITE,
     lambda r: [drop(r, f"evals/{c}") for c in ("case-rule", "case-walk", "case-neg")],
     "fails", "measurement of nothing"),
]


def run(gate: Path, root: Path) -> tuple[int, str]:
    result = subprocess.run([sys.executable, str(gate), str(root)], capture_output=True, text=True)
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

    if problems:
        print(f"\n{len(problems)} gate(s) did not fire as expected:\n", file=sys.stderr)
        for problem in problems:
            print(f"  ✘ {problem}\n", file=sys.stderr)
        return 1
    print(f"✔ gate fault injection: {len(FAULTS)}/{len(FAULTS)} faults caught")
    return 0


if __name__ == "__main__":
    sys.exit(main())
