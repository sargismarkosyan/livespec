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
CHECKS = SCRIPTS / "checks.py"
TRACE = SCRIPTS / "trace.py"
SUITE = SCRIPTS / "evalsuite.py"
BOARD = SCRIPTS / "board.py"
TESTS = SCRIPTS / "tests.py"
DOCTOR = SCRIPTS.parents[1] / "tools" / "doctor.py"
REPO = SCRIPTS.parents[1]
REPORT = SCRIPTS / "report.py"

GRADER = """---
type: llm
focus: last_message
weight: 1
---
The reply does the thing.
"""

def context_file(steps: int = 3) -> str:
    """A CLAUDE.md in the shape the gate reads — a numbered loop, a fenced block
    of commands, a link to the bindings. `steps` is the length of its loop. The
    ceiling row in green_bindings() is this file's own size. See specs/changes/0048."""
    loop = "".join(f"{n}. Step {n} of the loop.\n" for n in range(1, steps + 1))
    return (
        "# fixture\n\nA synthetic repository, not an application.\n\n"
        "## The loop\n\n" + loop
        + "\n## Commands\n\n```sh\npython3 gate.py\n```\n\n"
        "The bindings are [specs/setup/README.md](specs/setup/README.md).\n"
    )


CONTEXT_FILE = context_file()
ROW_CEILING = f"| **CLAUDE.md ceiling** | {len(CONTEXT_FILE.splitlines())} lines, `wc -l CLAUDE.md`, set at 0001 |"

FIXTURE: dict[str, str] = {
    "CLAUDE.md": CONTEXT_FILE,
    "skills/refine-spec/SKILL.md": "---\nname: refine-spec\ndescription: Turns a request into a spec.\n---\n\n# Refine\n\nThe gates are in [gates.md](../../method/gates.md).\n",
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
    # checks.py reads these two against each other. Minimal on purpose: the
    # fixture is here to be broken, not to be a second copy of the plugin.
    ".claude-plugin/plugin.json": json.dumps(
        {
            "name": "livespec",
            "version": "0.0.0",
            "description": "A synthetic fixture, not the plugin.",
            "license": "MIT",
            "repository": "https://example.test/fixture",
        },
        indent=1,
    ),
    ".claude-plugin/marketplace.json": json.dumps(
        {"name": "fixture", "plugins": [{"name": "livespec", "source": "./"}]}, indent=1
    ),
    # checks.py holds this to the shape an audit reads by, against the manifest.
    "CHANGELOG.md": "# Changelog\n\n## 0.0.0 — 2026-01-01\n\nThe fixture's one release.\n",
    # The latest change number, for the two-change clocks the tool reads.
    "specs/changes/0001-first.md": "# Spec 0001: the first\n",
    # The one test: standard library, bound to a rule through rulelib.rule().
    # tests.py holds every test to a rule; trace.py reads the call as a claim.
    "tests/__init__.py": "",
    "tests/test_thing.py": (
        "import sys\nimport unittest\nfrom pathlib import Path\n\n"
        "sys.path.insert(0, str(Path(__file__).resolve().parent))\n"
        "from rulelib import rule  # noqa: E402\n\n\n"
        "class Thing(unittest.TestCase):\n"
        "    @rule(\"two\")\n"
        "    def test_nothing_happens(self):\n"
        "        self.assertTrue(True)\n"
    ),
}


def record_rows() -> list[tuple[str, str]]:
    """Every fault this module holds, in the order it applies them.

    The one definition, called by the fixture below and by checks.py against the
    real bindings. A fourth list of faults is wired in here and nowhere else —
    the previous shape had this expression written out twice, and the second copy
    was found by adding a list and watching only one of them notice.
    """
    return (
        [(f[0], f[3]) for f in FAULTS]
        + [(f[0], "fails") for f in RELEASE_FAULTS]
        + [(f[0], "fails") for f in VERDICT_FAULTS]
        + [(f[0], "fails") for f in DOCTOR_FAULTS]
        + [(f[0], "fails") for f in VALIDATE_FAULTS]
    )


ROW_STRUCTURE = "| `gate:structure` | one feature per file, unique ids, every rule with an example, no example outside a rule | automated | `python3 gate.py` |"
ROW_COVERAGE = "| `gate:coverage` | lines, branches, functions | not applicable | no coverage here |"
ROW_PR_REPORT = "| `wiring:pr-report` | the pull-request report | unobserved | `report.py`, posted by CI |"
ROW_RULE_BOUND = "| `wiring:rule-bound-measure` | the rule-bound measure, reported beside the gated number | not applicable | no coverage here |"
ROW_RUN = "| `wiring:run-beside-claim` | the run beside the claim | unobserved | `report.py` prints the pipeline's run beside the body's block |"
ROW_STORE = "| `boundary:store` | the store | real | 0001 | `docker compose up db` starts it; leaves uncovered: production volume |"
ROW_CLOCK = "| `boundary:clock` | the clock | mocked | 0001 | a fake clock nothing checks; cover: none |"
ROW_SKETCH = "| **A sketch is owed** | by every change spec, before approval |"
ROW_SHOW = "| **What a change here must show** | a screenshot of the list, on docs/screenshots/ |"
GATE_HEADER = "| id | gate | state | evidence |\n|---|---|---|---|"
WIRING_HEADING = "### The wiring that must never gate"


def green_bindings(version: str) -> str:
    """templates/bindings.md, filled so that every line the audit tool answers reads clear or n/a.

    The one bindings text three things read: the fixture the faults are injected
    into, the tests under tests/, and — through the tool — the shape a consuming
    repository's ledger is held to. Generated, so the fault injection record and
    the *What it runs* row cannot fall behind what owns them.
    """
    record = "\n".join(
        f"| {name} | {'**warns, does not fail**' if outcome == 'warns' else 'fails'} | \u2714 |"
        for name, outcome in record_rows()
    )
    runs = ", ".join(f"`{script}`" for _, script in VERIFY_GATES)
    gates = "\n".join(
        [
            "| `gate:rule-to-test` | a live rule no test claims | automated | `python3 gate.py` |",
            "| `gate:test-to-rule` | a test claiming a rule that does not exist | automated | `python3 gate.py` |",
            "| `gate:planned-unclaimed` | a `@planned` rule or workflow that is claimed | automated | `python3 gate.py` |",
            "| `gate:feature-to-workflow` | a feature naming no workflow, or one that does not exist | automated | `python3 gate.py` |",
            "| `gate:workflow-to-feature` | a workflow claimed by no feature | automated | `python3 gate.py` |",
            "| `gate:workflow-walked` | a workflow walked by no test | automated | `python3 gate.py` |",
            "| `gate:workflow-to-persona` | a workflow naming no live persona | automated | `python3 gate.py` |",
            "| `gate:persona-to-workflow` | a persona named by no workflow | automated | `python3 gate.py` |",
            "| `gate:journey-to-workflow` | a journey naming a workflow that does not exist | automated | `python3 gate.py` |",
            "| `gate:workflow-to-journey` | a workflow naming no journey — warns | automated | `python3 gate.py` |",
            ROW_STRUCTURE,
            ROW_COVERAGE,
            "| `gate:boundary-double` | a rule-bound test doubling a boundary declared real | not applicable | no rule-bound doubles here |",
            "| `gate:boundary-fake-suite` | a fake row naming no suite against the real thing | not applicable | no rule-bound doubles here |",
            "| `gate:boundary-recorded-age` | a recorded row past its age | not applicable | no rule-bound doubles here |",
            "| `gate:boundaries-table` | rule-bound tests present and no boundaries table | not applicable | no rule-bound doubles here |",
            "| `gate:context-file-ceiling` | the context file past the ceiling the bindings name, or with no ceiling row | automated | `python3 gate.py` |",
            "| `gate:context-file-shape` | the context file missing, or without its loop, its commands, or its pointer to the bindings | automated | `python3 gate.py` |",
            "| `gate:crossing-names-a-boundary` | a rule crossing a boundary the bindings have no row for | automated | `python3 gate.py` |",
            "| `gate:skipped-test-claims-nothing` | a rule-bound test marked skipped, focused or expected to fail claims no rule | automated | `python3 gate.py` |",
            "| `gate:fewer-ran-than-exist` | the runner reporting fewer rule-bound tests than the tree holds | automated | `python3 gate.py test` |",
            "| `gate:verified-to-fire` | every gate broken on purpose and seen to fire | automated | `python3 gate.py inject` |",
        ]
    )
    return (
        "# Bindings\n\n"
        "The bindings of a synthetic fixture. Nothing here is a real repository.\n\n"
        "## The table\n\n"
        "| | |\n|---|---|\n"
        "| **Verification** | `python3 gate.py` |\n"
        "| **What it returns** | 0 green, 1 red |\n"
        f"| **What it runs** | {runs} |\n"
        "| **Language** | JavaScript |\n"
        "| **Package manager** | npm |\n"
        "| **Traceability gate** | `python3 gate.py trace` |\n"
        "| **Coverage gate** | none — see *What has no gate* |\n"
        "| **Coverage thresholds** | none |\n"
        "| **Fault injection** | `python3 gate.py inject` — the record is below |\n"
        "| **Required checks** | `checks` |\n"
        "| **Tracker** | GitHub Issues, via `gh issue create` |\n"
        "| **Where the app runs** | `npm start` |\n"
        f"{ROW_SKETCH}\n"
        f"{ROW_SHOW}\n"
        f"{ROW_CEILING}\n"
        "| **Deliverable of a version** | the screenshot |\n"
        "| **What proves a rule** | an ordinary test suite |\n"
        "| **How a test claims its rule** | `rule()` from tests/rulelib.py |\n"
        "| **Rule discovery** | specs/features/**/*.feature |\n"
        "| **Spec-bound coverage** | not applicable — no coverage here |\n"
        "| **Pull-request report** | `report.py`, posted by CI |\n"
        "| **Audit record** | `specs/setup/audit.md` |\n"
        "| **What a contributor owes a release** | a label and a changelog section |\n\n"
        "## Gate wiring\n\n"
        f"**Reconciled against livespec {version} on 2026-01-01.**\n\n"
        f"{GATE_HEADER}\n{gates}\n\n"
        f"{WIRING_HEADING}\n\n"
        "| id | wiring | state | evidence |\n|---|---|---|---|\n"
        f"{ROW_PR_REPORT}\n{ROW_RULE_BOUND}\n{ROW_RUN}\n\n"
        "### The boundaries\n\n"
        "| id | boundary | state | since | evidence |\n|---|---|---|---|---|\n"
        f"{ROW_STORE}\n{ROW_CLOCK}\n\n"
        "### Workarounds\n\n"
        "| instead | gap | filed | ends when |\n|---|---|---|---|\n\n"
        "## The fault injection record\n\n"
        "| Injected fault | Expected | Result |\n|---|---|---|\n"
        f"{record}\n\n"
        "## Branch protection\n\n"
        "Read back with `gh api repos/o/r/rulesets` on 2026-01-01: a merge is blocked when `checks` fails, and one deploy key can bypass.\n\n"
        "## What has no gate, and what that misses\n\n"
        "No coverage gate: the fixture has three lines of code, and a threshold over them would measure nothing.\n\n"
        "## Notes from the sitting\n\n"
        "Nothing runs on one machine that the pipeline does not.\n"
    )


def bindings(root: Path) -> None:
    """The bindings the fixture carries: the template filled green, at the fixture's own version."""
    path = root / "specs" / "setup" / "README.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(green_bindings("0.0.0"))


def id_table(root: Path) -> None:
    """The plugin's own id table, with every version rewritten to the fixture's one release.

    checks.py holds the table equal to the tool's registry, so the fixture must
    carry the real list rather than a stand-in for it; only the two columns the
    release writes are rewritten, to the version the fixture's changelog has.
    """
    real = (REPO / "method" / "gates.md").read_text()
    start = real.index("## The ids")
    end = real.find("\n## ", start + 10)
    lines: list[str] = []
    for line in real[start: end if end != -1 else len(real)].splitlines():
        if line.startswith("|") and not line.startswith("|--"):
            segments = line.split("|")
            if len(segments) >= 9 and segments[1].strip() != "id":
                segments[3] = " 0.0.0 "
                if segments[5].strip() not in ("", "—", "-"):
                    segments[5] = " 0.0.0 " + segments[5].strip().split(" ", 1)[1] + " " if " " in segments[5].strip() else " 0.0.0 "
                line = "|".join(segments)
        lines.append(line)
    path = root / "method" / "gates.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("# The gates\n\n" + "\n".join(lines) + "\n")


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
    # The case table, for the same reason as the bindings: generated from what it
    # describes, so the unbroken fixture is green by construction.
    readme = root / "evals" / "README.md"
    rows = "\n".join(
        f"| `{case['name']}` | holds the thing | it stops holding it |" for case in cases(root)
    )
    readme.write_text(
        readme.read_text()
        + "\n## What each case is for\n\n| Case | Holds | Fails when |\n|---|---|---|\n"
        + rows
        + "\n"
    )
    bindings(root)
    id_table(root)
    (root / "tests" / "rulelib.py").write_text((REPO / "tests" / "rulelib.py").read_text())


def drop_board_entry(root: Path, name: str) -> None:
    path = root / "evals" / "board.json"
    data = json.loads(path.read_text())
    del data["cases"][name]
    path.write_text(json.dumps(data, indent=1))


def board_runs(root: Path, name: str, runs: int) -> None:
    """Put one entry below the floor without touching anything it measured.

    The inputs hash stays valid on purpose: this is the fault where the number
    is perfectly fresh and still not a measurement, which is the one the board
    could not see until #75.
    """
    path = root / "evals" / "board.json"
    data = json.loads(path.read_text())
    data["cases"][name]["runs"] = runs
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
import verify  # noqa: E402
from verify import GATES as VERIFY_GATES  # noqa: E402
from releaselib import (  # noqa: E402
    ReleaseInputError,
    bump_manifest,
    entries,
    extract_entry,
    extract_gherkin,
    extract_run,
    moves_spec,
    touches_the_run,
    verification_command,
    next_version,
    prepend_entry,
    select_increment,
    stamp_ids,
    stamp_ledger,
    check_ids_section,
    moves_audit_surface,
    NEXT,
)

# The id table, in the three shapes the release contract is held against: as
# the base has it, with a row that arrived (reading next, as a new row must),
# and with the same row typed as a version somebody guessed. See 0042.
TABLE_BASE = (
    "# The gates\n\n## The ids\n\n"
    "| id | kind | since | severity | retired | aliases | meaning |\n"
    "|---|---|---|---|---|---|---|\n"
    "| `gate:rule-to-test` | gate | 0.0.0 | wiring | — | rule → test | a live rule no test claims fails |\n"
)
TABLE_ADDED = TABLE_BASE + "| `check:new-thing` | mechanical | next | record | — | | arrived with this change |\n"
TABLE_TYPED = TABLE_BASE + "| `check:new-thing` | mechanical | 0.0.0 | record | — | | arrived with this change |\n"

GOOD_BODY = (
    "Intro.\n\n## Changelog\n\nBody of the entry.\n\n## Notes\n\nnot part of it\n\n"
    "```gherkin\n  Rule: it holds\n```\n"
)

BODY_IDS_ADDED = GOOD_BODY + "\n## Ids\n\nadded: check:new-thing\n"
BODY_IDS_UNCHANGED = GOOD_BODY + "\n## Ids\n\nunchanged\n"
BODY_IDS_GHOST = GOOD_BODY + "\n## Ids\n\nadded: check:ghost\n"
BODY_IDS_BULLETS = GOOD_BODY + "\n## Ids\n\n- added: check:new-thing\n- retired: none\n"
BODY_IDS_BULLET_RETIRES = GOOD_BODY + "\n## Ids\n\n- retired: check:new-thing\n"

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
     lambda: prepend_entry("# Changelog\n\n## 0.9.0 — 2026-01-01\n\nold\n", "0.9.0", "2026-01-02", "e"),
     "already has an entry"),
    ("a manifest with no version field",
     lambda: bump_manifest('{"name": "livespec"}', "0.9.0"), "no `version` field"),
    ("a version that is not major.minor.patch",
     lambda: next_version("0.8", "minor"), "not major.minor.patch"),
    ("spec-moving change whose body carries no gherkin",
     lambda: extract_gherkin("Intro.\n\n## Changelog\n\nBody."), "carries no Gherkin"),
    ("a gherkin block with nothing in it",
     lambda: extract_gherkin("Intro.\n\n```gherkin\n\n```\n"), "gherkin block is empty"),
    # The list an audit is held to moves only where somebody said so, and the
    # version it moved in is written by the release, never typed. See 0042.
    ("a new id row with a typed version",
     lambda: check_ids_section(BODY_IDS_ADDED, TABLE_BASE, TABLE_TYPED), "reads next"),
    ("the audit surface moved with no ## Ids section",
     lambda: check_ids_section(GOOD_BODY, TABLE_BASE, TABLE_ADDED), "no `## Ids` section"),
    ("## Ids reading unchanged while a row was added",
     lambda: check_ids_section(BODY_IDS_UNCHANGED, TABLE_BASE, TABLE_ADDED), "says unchanged"),
    ("## Ids naming an id the table does not have",
     lambda: check_ids_section(BODY_IDS_GHOST, TABLE_BASE, TABLE_BASE), "does not have"),
    ("a row still reading next after the release",
     lambda: stamp_ids(TABLE_ADDED, NEXT), "still read next"),
    ("a ledger whose stamp the release cannot find",
     lambda: stamp_ledger("# Bindings\n\nno stamp here\n", "0.9.0", "2026-01-02"), "no stamp line"),
    ("a bullet list that retires what the table added",
     lambda: check_ids_section(BODY_IDS_BULLET_RETIRES, TABLE_BASE, TABLE_ADDED), "was added and `## Ids` does not name it"),
    # The run a claim of green rests on: the body quotes the verification
    # command as the bindings name it, with the runner's output beneath, or a
    # change touching the tests cannot merge. See specs/changes/0052.
    ("a change to the tests whose body carries no run block",
     lambda: extract_run(GOOD_BODY, "python3 gate.py"), "carries no run block"),
    ("a run block quoting a different command",
     lambda: extract_run(GOOD_BODY + "\n```\n$ npm test\nok\n```\n", "python3 gate.py"), "not the verification command"),
    ("a run block with no output under the command",
     lambda: extract_run(GOOD_BODY + "\n```\n$ python3 gate.py\n```\n", "python3 gate.py"), "no output under it"),
]

BODY_WITH_RUN = GOOD_BODY + "\n```\n$ python3 gate.py\n✔ 3 tests, every gate green\n```\n"


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


def verdict_control() -> None:
    """The two reds verify.py must keep apart, asserted from the correct side.

    Not faults: nothing is broken here. It is the boundary the fault below sits
    just outside of, and it is worth stating because the whole promise is that a
    bill and a defect look different — which cannot be proved by breaking things
    alone.
    """
    code, line = verify.verdict([])
    assert code == 0 and not line, "a green run is not silent"

    code, line = verify.verdict(["measurement board"])
    assert code == verify.OWED, f"a bill exits {code}, not {verify.OWED}"
    assert "verification failed" not in line, "a bill still reads as a failure"
    assert "approve" in line, "a bill does not say who can clear it"


def release_control() -> None:
    """The unbroken inputs, which must produce a release rather than a refusal."""
    stamped = stamp_ids(TABLE_ADDED, "0.9.0")
    assert "| `check:new-thing` | mechanical | 0.9.0 |" in stamped, "the new row was not stamped"
    assert NEXT not in stamped, "stamping left a row reading next"
    untouched = lambda text: [line for line in text.splitlines() if "check:new-thing" not in line]  # noqa: E731
    assert untouched(stamped) == untouched(TABLE_ADDED), "stamping touched a line it does not own"
    assert stamp_ids(TABLE_BASE, "0.9.0") == TABLE_BASE, "a table with nothing to stamp was changed"
    assert check_ids_section(BODY_IDS_ADDED, TABLE_BASE, TABLE_ADDED)["added"] == ["check:new-thing"]
    assert check_ids_section(BODY_IDS_UNCHANGED, TABLE_BASE, TABLE_BASE)["added"] == []
    assert check_ids_section(BODY_IDS_BULLETS, TABLE_BASE, TABLE_ADDED)["added"] == ["check:new-thing"], "a bullet list is refused"
    ledger = "# Bindings\n\nReconciled against livespec **0.8.0** (`method/`) on **2026-01-01** — the sitting.\n\n| a | b |\n"
    stamped = stamp_ledger(ledger, "0.9.0", "2026-01-02")
    assert "livespec **0.9.0** (`method/`) on **2026-01-02** — the sitting." in stamped, "the stamp was not moved in place"
    assert stamped.replace("0.9.0", "0.8.0").replace("2026-01-02", "2026-01-01") == ledger, "stamping the ledger touched something else"
    assert moves_audit_surface(["skills/doctor/SKILL.md", "README.md", "method/gates.md"]) == [
        "skills/doctor/SKILL.md", "method/gates.md",
    ], "the audit surface is not read from the paths"
    assert select_increment(["bug", "minor"]) == "minor", "the one release label is not read"
    assert extract_entry(GOOD_BODY) == "Body of the entry.", "the entry is not taken verbatim"
    assert next_version("0.8.0", "minor") == "0.9.0", "the increment does not apply"
    assert '"version": "0.9.0"' in bump_manifest('{\n  "version": "0.8.0"\n}', "0.9.0")
    log = prepend_entry("# Changelog\n\nhead\n\n## 0.8.0 — 2026-01-01\n\nold\n", "0.9.0", "2026-01-02", "Body.")
    assert log.index("## 0.9.0") < log.index("## 0.8.0"), "the new entry is not on top"
    assert "Body." in log, "the entry did not survive into the changelog"
    assert entries(log) == [("0.9.0", "2026-01-02"), ("0.8.0", "2026-01-01")], "the entries are not read back newest first"
    assert extract_gherkin(GOOD_BODY) == "Rule: it holds", "the quoted Gherkin is not read"
    assert extract_gherkin(
        "see https://x.test/o/r/blob/" + "a" * 40 + "/specs/features/a.feature"
    ).endswith(".feature"), "a pinned Gherkin link is not accepted"
    assert moves_spec(["specs/workflows/README.md", "specs/features/a.feature"]) == [
        "specs/features/a.feature"
    ], "the spec surface is not what triggers the Gherkin check"
    assert extract_run(BODY_WITH_RUN, "python3 gate.py").splitlines()[0] == "$ python3 gate.py", "the run block is not read"
    assert touches_the_run(["tests/test_x.py", "evals/README.md", "evals/case-rule/prompt.md", "method/gates.md"]) == [
        "tests/test_x.py", "evals/case-rule/prompt.md"
    ], "the run surface is not read from the paths"
    assert verification_command("| **Verification** | `python3 gate.py` |\n") == "python3 gate.py", "the verification command is not read from the bindings"


# (name, gate, mutation, expected outcome, a phrase the message must contain)
def seven_rules() -> str:
    """A feature one rule past the soft limit. Every rule is planned and has an
    example, so the only thing wrong with the file is its size. See specs/changes/0047."""
    rules = "".join(
        f"\n  @rule:seven-{n} @planned\n  Rule: thing {n} is true\n\n"
        f"    Example: it shows thing {n}\n      Given a list\n      When they look\n      Then thing {n} is there\n"
        for n in range(1, 8)
    )
    return "@feature:seven @workflow:read-it\nFeature: Seven of them\n" + rules


def long_feature() -> str:
    """A feature past the line limit: one planned rule under the kind of comment
    the template ships with, repeated until the file is longer than the soft limit."""
    padding = "".join(f"  # line {n} of a file that has grown past the soft limit\n" for n in range(1, 121))
    return (
        "@feature:long @workflow:read-it\nFeature: A long one\n\n" + padding
        + "\n  @rule:long-one @planned\n  Rule: the thing is true\n\n"
        "    Example: it shows the thing\n      Given a list\n      When they look\n      Then the thing is there\n"
    )


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
    # The two soft limits. Warnings on purpose — small files are the point and a
    # hard cap is not — and until these two, the one shape check in trace.py
    # nothing had ever seen speak. See specs/changes/0047.
    ("a feature holding more rules than the soft limit", TRACE,
     lambda r: write(r, "specs/features/core/seven.feature", seven_rules()), "warns", "soft limit"),
    ("a feature longer than the soft limit", TRACE,
     lambda r: write(r, "specs/features/core/long.feature", long_feature()), "warns", "soft limit"),
    # The file every session reads first. Seven ways it fails, none of them
    # about what it says — that is the sitting's and the audit's. See
    # specs/changes/0048.
    ("a context file past its ceiling", TRACE,
     lambda r: write(r, "CLAUDE.md", CONTEXT_FILE + "\nOne more line than the bindings allow.\n"),
     "fails", "against a ceiling of"),
    ("a context file with no ceiling row", TRACE,
     lambda r: edit(r, "specs/setup/README.md", ROW_CEILING + "\n", ""), "fails", "names no CLAUDE.md ceiling"),
    ("a ceiling above the reader's limit", TRACE,
     lambda r: edit(r, "specs/setup/README.md", ROW_CEILING,
                    ROW_CEILING.replace(f"{len(CONTEXT_FILE.splitlines())} lines", "250 lines")),
     "fails", "above the 200"),
    ("no context file at the root", TRACE,
     lambda r: drop(r, "CLAUDE.md"), "fails", "no CLAUDE.md at the root"),
    ("a context file with no numbered list", TRACE,
     lambda r: write(r, "CLAUDE.md", CONTEXT_FILE.replace(
         "1. Step 1 of the loop.\n2. Step 2 of the loop.\n3. Step 3 of the loop.\n", "The loop is described elsewhere.\n")),
     "fails", "no numbered list"),
    ("a loop of nine steps", TRACE,
     lambda r: (write(r, "CLAUDE.md", context_file(9)),
                edit(r, "specs/setup/README.md", ROW_CEILING,
                     ROW_CEILING.replace(f"{len(CONTEXT_FILE.splitlines())} lines", f"{len(context_file(9).splitlines())} lines"))),
     "fails", "at most 8"),
    ("a context file with no fenced block", TRACE,
     lambda r: write(r, "CLAUDE.md", CONTEXT_FILE.replace("```sh\npython3 gate.py\n```\n", "python3 gate.py\n")),
     "fails", "no fenced block"),
    ("a context file that does not link to the bindings", TRACE,
     lambda r: write(r, "CLAUDE.md", CONTEXT_FILE.replace("(specs/setup/README.md)", "(specs/README.md)")),
     "fails", "does not link to"),
    # A rule names what it crosses. The green fixture carries no crossing; these
    # two introduce one. `boundary:store` is a row the fixture's bindings carry,
    # so the second warns rather than fails. See specs/changes/0053.
    ("a rule crossing a boundary the bindings have no row for", TRACE,
     lambda r: edit(r, "specs/features/core/core.feature", "@rule:one\n", "@rule:one @crosses:ghost\n"),
     "fails", "no row for"),
    ("a crossing rule with a single example", TRACE,
     lambda r: edit(r, "specs/features/core/core.feature", "@rule:one\n", "@rule:one @crosses:store\n"),
     "warns", "boundary misbehaving"),
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
    ("a case with no row in the table", SUITE,
     lambda r: edit(r, "evals/README.md", "| `case-walk` | holds the thing | it stops holding it |\n", ""),
     "fails", "no row in 'What each case is for'"),
    ("a row for a case nobody has", SUITE,
     lambda r: edit(r, "evals/README.md", "|---|---|---|\n",
                    "|---|---|---|\n| `case-gone` | holds the thing | it stops holding it |\n"),
     "fails", "which is not a case directory"),
    ("the runner losing its refusal of an unapproved run", SUITE,
     lambda r: write(r, "evals/runner/run.py", "# a runner that just runs, spending whatever it spends\n"),
     "fails", "no longer refuses an unapproved run"),
    ("the runner letting a run below the floor take a measurement's row", SUITE,
     lambda r: write(r, "evals/runner/run.py",
                     "# refuses without --i-approve-the-cost, and writes the board whatever it ran\n"),
     "fails", "caselib.replaces()"),
    ("a measurement whose inputs moved on", BOARD,
     lambda r: edit(r, "evals/case-rule/prompt.md", "Do the thing.", "Do the other thing."), "fails", "changed since"),
    ("a measurement whose rule was reworded", BOARD,
     lambda r: edit(r, "specs/features/core/core.feature", "the thing is there", "the thing is elsewhere"), "fails", "changed since"),
    ("a case the board has never measured", BOARD,
     lambda r: drop_board_entry(r, "case-walk"), "warns", "never measured"),
    ("a board entry from fewer runs than the floor", BOARD,
     lambda r: board_runs(r, "case-walk", 1), "warns", "below the floor"),
    ("an llm grader with an empty rubric", SUITE,
     lambda r: write(r, "evals/case-rule/graders/outcome.md", "---\ntype: llm\nweight: 1\n---\n"),
     "fails", "will pass on anything"),
    ("every case removed", SUITE,
     lambda r: [drop(r, f"evals/{c}") for c in ("case-rule", "case-walk", "case-neg")],
     "fails", "measurement of nothing"),
    # The record of what was injected is itself something a gate holds. Until these
    # four, checks.py was the one gate here that could never be broken on purpose —
    # it took no root — and so the one never known to fire.
    ("the fault injection record losing a row", CHECKS,
     lambda r: edit(r, "specs/setup/README.md", "| live rule with no case | fails | \u2714 |\n", ""),
     "fails", "has no row for"),
    ("the record naming a fault nobody injects", CHECKS,
     lambda r: edit(r, "specs/setup/README.md", "| Injected fault | Expected | Result |\n|---|---|---|\n",
                    "| Injected fault | Expected | Result |\n|---|---|---|\n| a fault nobody injects | fails | \u2714 |\n"),
     "fails", "which inject.py does not hold"),
    ("a recorded fault whose expected result was flipped", CHECKS,
     lambda r: edit(r, "specs/setup/README.md",
                    "| workflow naming no journey | **warns, does not fail** | \u2714 |",
                    "| workflow naming no journey | fails | \u2714 |"),
     "fails", "inject.py expects it to warns"),
    ("the bindings losing a gate verify.py runs", CHECKS,
     lambda r: edit(r, "specs/setup/README.md", "`board.py`, ", ""),
     "fails", "verify.py runs"),
    # The record an audit in a consuming repository reads by. Every version
    # reaches an entry — the release faults below hold that — but nothing held
    # the shape the reading depends on until these two. See specs/changes/0038.
    ("a changelog heading the reader cannot parse", CHECKS,
     lambda r: edit(r, "CHANGELOG.md", "## 0.0.0 — 2026-01-01", "## 0.0.0"),
     "fails", "is not `## <version> — <date>`"),
    ("a manifest version with no changelog entry", CHECKS,
     lambda r: edit(r, ".claude-plugin/plugin.json", '"version": "0.0.0"', '"version": "0.0.1"'),
     "fails", "has no CHANGELOG.md entry"),
    # The one list an audit is held to. An id whose since names a release nobody
    # shipped would send an audit reading "arrived after your stamp" to a version
    # that does not exist; the same id twice is two rows for one promise. See
    # specs/changes/0041.
    ("an id whose since names a release the changelog does not have", CHECKS,
     lambda r: edit(r, "method/gates.md", "| `check:stamp-present` | mechanical | 0.0.0 |",
                    "| `check:stamp-present` | mechanical | 0.0.9 |"),
     "fails", "has no CHANGELOG.md entry; an audit would report"),
    ("the same id twice in the id table", CHECKS,
     lambda r: duplicate_row(r, "method/gates.md", "| `check:stamp-present` |"),
     "fails", "appears twice"),
    # The tool and the table are one list, and the tests are bound to rules.
    # See specs/changes/0041, part two.
    ("a check the tool answers that the id table does not name", CHECKS,
     lambda r: drop_row(r, "method/gates.md", "| `check:ledger-shape` |"),
     "fails", "the tool performs check:ledger-shape and the id table does not name it"),
    ("an id in the table no function answers", CHECKS,
     lambda r: edit(r, "method/gates.md", "| `check:stamp-present` |", "| `check:ghost` | mechanical | 0.0.0 | record | — | | nobody answers this |\n| `check:stamp-present` |"),
     "fails", "names check:ghost and no function"),
    ("a test claiming a rule that does not exist", TRACE,
     lambda r: edit(r, "tests/test_thing.py", 'rule("two")', 'rule("nope")'),
     "fails", "does not exist"),
    ("a test outside any rule", TESTS,
     lambda r: edit(r, "tests/test_thing.py", '    @rule("two")\n', ""),
     "fails", "names no rule"),
    ("a failing test", TESTS,
     lambda r: edit(r, "tests/test_thing.py", "assertTrue(True)", "assertTrue(False)"),
     "fails", "the tests are red"),
    ("a test naming a rule that is still @planned", TESTS,
     lambda r: edit(r, "specs/features/core/core.feature", "@rule:two @refusal", "@rule:two @refusal @planned"),
     "fails", "the tests are red"),
    # A test that did not run claims nothing. The marker empties the claim in
    # the traceability gate; the count is the runner's gate's. See specs/changes/0051.
    ("a skipped rule-bound test claiming a rule", TRACE,
     lambda r: edit(r, "tests/test_thing.py", '    @rule("two")\n', '    @unittest.skip("not today")\n    @rule("two")\n'),
     "fails", "claims nothing"),
    ("the runner ran fewer rule-bound tests than the tree holds", TESTS,
     lambda r: write(r, "tests/test_more.py",
                     "import sys\nfrom pathlib import Path\n\n"
                     "sys.path.insert(0, str(Path(__file__).resolve().parent))\n"
                     "from rulelib import rule  # noqa: E402\n\n\n"
                     "class More:  # not a TestCase: the runner never collects it\n"
                     "    @rule(\"one\")\n"
                     "    def test_the_thing_is_true(self):\n"
                     "        assert True\n"),
     "fails", "the runner ran"),
]


def duplicate_row(root: Path, relative: str, prefix: str) -> None:
    path = root / relative
    lines = path.read_text().splitlines(keepends=True)
    hit = next((line for line in lines if line.startswith(prefix)), None)
    if hit is None:
        raise SystemExit(f"inject: {relative} has no row starting {prefix!r}")
    path.write_text("".join(line + hit if line == hit else line for line in lines))


def drop_row(root: Path, relative: str, prefix: str) -> None:
    path = root / relative
    lines = path.read_text().splitlines(keepends=True)
    if not any(line.startswith(prefix) for line in lines):
        raise SystemExit(f"inject: {relative} has no row starting {prefix!r}")
    path.write_text("".join(line for line in lines if not line.startswith(prefix)))


def git_in(root: Path, *args: str) -> None:
    subprocess.run(["git", "-c", "user.name=fixture", "-c", "user.email=fixture@example.test", *args], cwd=root, capture_output=True, check=True)


def as_git_repo_with_a_stray_change(root: Path) -> None:
    git_in(root, "init", "-q")
    git_in(root, "add", "-A")
    git_in(root, "commit", "-q", "-m", "fixture")
    (root / "src").mkdir(exist_ok=True)
    (root / "src" / "app.js").write_text("// a fix that strayed into the wiring\n")
    git_in(root, "add", "-A")
    (root / "src" / "app.js").write_text("// changed after being added\n")


# (name, the check whose line must move, how to break the fixture, the state it must read)
#
# One fault per check the tool answers from a file. A check no fault flips is
# red here — doctor_control() below holds this list to the tool's own registry
# — because a check that has never been made to fail is not known to be a
# check. See specs/changes/0041, every-mechanical-check-is-proven-to-fire.
DOCTOR_FAULTS = [
    ("a ledger in the shape it had before ids", "check:ledger-shape",
     lambda r: edit(r, "specs/setup/README.md", GATE_HEADER, "| Gate | State | Wired by, or why not |\n|---|---|---|"), "open"),
    ("a ledger with no stamp line", "check:stamp-present",
     lambda r: edit(r, "specs/setup/README.md", "**Reconciled against livespec 0.0.0 on 2026-01-01.**", ""), "open"),
    ("a stamp behind the plugin installed", "check:stamp-range",
     lambda r: (edit(r, ".claude-plugin/plugin.json", '"version": "0.0.0"', '"version": "0.0.1"'),
                edit(r, "CHANGELOG.md", "## 0.0.0 — 2026-01-01", "## 0.0.1 — 2026-01-02\n\nA later release.\n\n## 0.0.0 — 2026-01-01")), "open"),
    ("a stamp ahead of the plugin installed", "check:stamp-ahead",
     lambda r: edit(r, "specs/setup/README.md", "livespec 0.0.0 on", "livespec 9.9.9 on"), "open"),
    ("a stamp that is not at the plugin installed", "check:range-empty-said",
     lambda r: edit(r, "specs/setup/README.md", "livespec 0.0.0 on", "livespec 9.9.9 on"), "n/a"),
    ("a changelog the tool cannot read", "check:changelog-reachable",
     lambda r: edit(r, "CHANGELOG.md", "## 0.0.0 — 2026-01-01", "## 0.0.0"), "open"),
    ("a row in a state of somebody's own", "check:row-state-legal",
     lambda r: edit(r, "specs/setup/README.md", ROW_STRUCTURE, ROW_STRUCTURE.replace("| automated |", "| maybe |")), "open"),
    ("an automated row naming no command", "check:row-evidence",
     lambda r: edit(r, "specs/setup/README.md", ROW_STRUCTURE, ROW_STRUCTURE.replace("`python3 gate.py`", "the gate")), "open"),
    ("a not-applicable reason the tree contradicts", "check:na-vs-tree",
     lambda r: edit(r, "specs/setup/README.md", ROW_COVERAGE, ROW_COVERAGE.replace("no coverage here", "no personas exist")), "open"),
    ("a gate with no row", "check:row-per-gate",
     lambda r: edit(r, "specs/setup/README.md", ROW_STRUCTURE + "\n", ""), "open"),
    ("a recording past its age", "check:recorded-age",
     lambda r: edit(r, "specs/setup/README.md", ROW_CLOCK, "| `boundary:clock` | the clock | recorded | 0001 | recordings from 2020-01-01, allowed 30 days |"), "open"),
    ("a mocked row two changes old", "check:mocked-clock",
     lambda r: write(r, "specs/changes/0003-later.md", "# Spec 0003\n"), "open"),
    ("no table for the wiring that must never gate", "check:second-table",
     lambda r: edit(r, "specs/setup/README.md", WIRING_HEADING, "### Two rows that used to be a table"), "open"),
    ("the second table losing the report's row", "check:pr-report-row",
     lambda r: edit(r, "specs/setup/README.md", ROW_PR_REPORT + "\n", ""), "open"),
    ("the second table losing the measure's row", "check:rule-bound-row",
     lambda r: edit(r, "specs/setup/README.md", ROW_RULE_BOUND + "\n", ""), "open"),
    ("the second table losing the run's row", "check:run-row",
     lambda r: edit(r, "specs/setup/README.md", ROW_RUN + "\n", ""), "open"),
    ("no row saying a sketch is owed", "check:sketch-row",
     lambda r: edit(r, "specs/setup/README.md", ROW_SKETCH + "\n", ""), "open"),
    ("the sketch row and the picture row saying one thing", "check:picture-row",
     lambda r: edit(r, "specs/setup/README.md", ROW_SKETCH, "| **A sketch is owed** | a screenshot of the list, on docs/screenshots/ |"), "open"),
    ("a record instructing by a skill this plugin no longer has", "check:skill-names",
     lambda r: write(r, "CLAUDE.md", "# The loop\n\nReport what you found with `/livespec:feedback`.\n"), "open"),
    ("a row deferred across two changes", "check:deferred-clock",
     lambda r: (edit(r, "specs/setup/README.md", ROW_STRUCTURE, "| `gate:structure` | structure | deferred | since 0001 — later |"),
                write(r, "specs/changes/0003-later.md", "# Spec 0003\n")), "open"),
    ("a local hook given a row", "check:hook-no-row",
     lambda r: edit(r, "specs/setup/README.md", ROW_STRUCTURE, ROW_STRUCTURE + "\n| `local:hook` | the pre-push hook | automated | `.githooks/pre-push` |"), "open"),
    ("a change outside the record in the working tree", "check:record-only",
     as_git_repo_with_a_stray_change, "open"),
]


def finished_record(root: Path) -> Path:
    """The record the tool prints for the fixture, with every judgment line answered as a mind would."""
    result = subprocess.run(
        [sys.executable, str(DOCTOR), "specs/setup/README.md", "--plugin", str(root)],
        cwd=root, capture_output=True, text=True,
    )
    lines = []
    for line in result.stdout.splitlines():
        if line.startswith("| `check:") and "| unanswered |" in line and "← model" in line:
            cells = line.split("|")
            cells[2] = " clear "
            cells[4] = " run: gh api repos/o/r/rulesets → required: [checks], strict "
            line = "|".join(cells)
        lines.append(line)
    path = root / "finished.md"
    path.write_text("\n".join(lines) + "\n")
    return path


def run_validate(root: Path, finished: Path) -> tuple[int, str]:
    result = subprocess.run(
        [sys.executable, str(DOCTOR), "specs/setup/README.md", "--plugin", str(root), "--validate", str(finished)],
        cwd=root, capture_output=True, text=True,
    )
    return result.returncode, result.stdout + result.stderr


def with_record_line(root: Path, old: str, new: str) -> None:
    path = root / "finished.md"
    text = path.read_text()
    if old not in text:
        raise SystemExit(f"inject: the finished record no longer contains {old!r}")
    path.write_text(text.replace(old, new, 1))


# (name, how to break the finished record, a phrase the refusal must contain)
#
# Pass two of the tool. A record that is refused is an audit that has not
# finished, and each of these is one way to hand back early. See 0041,
# one-line-per-check-or-it-does-not-end and the two rules after it.
VALIDATE_FAULTS = [
    ("a record one line short",
     lambda r: with_record_line(r, "| `check:mocked-clock` |", "| `check:mocked-clocks` |"), "missing: check:mocked-clock"),
    ("a judgment nobody made",
     lambda r: with_record_line(r, "| `check:merge-blocked` | clear |", "| `check:merge-blocked` | unanswered |"), "still unanswered: check:merge-blocked"),
    ("a state of somebody's own",
     lambda r: with_record_line(r, "| `check:merge-blocked` | clear |", "| `check:merge-blocked` | done |"), "unknown state 'done'"),
    ("an open line naming nothing that closes it",
     lambda r: blank_line(r, "check:merge-blocked", "open"), "open with nothing that closes it"),
    ("a not-read line with no reason",
     lambda r: blank_line(r, "check:merge-blocked", "not-read"), "gives no reason"),
    ("a judgment clear with no command beside it",
     lambda r: with_record_line(r, "run: gh api repos/o/r/rulesets → required: [checks], strict", "looked fine"), "no command beside it"),
    ("a fix that strayed into the wiring",
     as_git_repo_with_a_stray_change, "doctor wires nothing"),
]


def blank_line(root: Path, check_id: str, state: str) -> None:
    """One record line rewritten to a state with nothing after it."""
    path = root / "finished.md"
    out = []
    for line in path.read_text().splitlines():
        if line.startswith(f"| `{check_id}` |"):
            cells = line.split("|")
            cells[2], cells[4] = f" {state} ", "  "
            line = "|".join(cells)
        out.append(line)
    path.write_text("\n".join(out) + "\n")


def validate_control(root: Path) -> None:
    """The finished fixture record validates, is written where the bindings say, and the reply is generated."""
    finished = finished_record(root)
    code, output = run_validate(root, finished)
    assert code == 0, f"the finished fixture record was refused:\n{output}"
    record = root / "specs" / "setup" / "audit.md"
    assert record.exists(), "the record was not written where the bindings say"
    assert "| `check:read-back-or-not` | clear |" in record.read_text(), "the generated line was not answered"
    assert output.startswith("# Audit — "), "the reply is not generated from the record"
    assert "## Decided — " in output and "## Open — 0" in output, "the reply's sections are missing"
    assert "/livespec:setup" not in output, "the green fixture was sent to a sitting"


def audit_fixture(root: Path) -> dict[str, str]:
    """The state the tool gives every check, reading the fixture as both repository and plugin."""
    result = subprocess.run(
        [sys.executable, str(DOCTOR), "specs/setup/README.md", "--plugin", str(root)],
        cwd=root, capture_output=True, text=True,
    )
    states: dict[str, str] = {}
    for line in result.stdout.splitlines():
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) >= 2 and cells[0].startswith("`check:"):
            states[cells[0].strip("`")] = cells[1]
    if not states:
        raise AssertionError(f"the tool printed no record (exit {result.returncode}):\n{result.stdout}{result.stderr}")
    return states


def doctor_control(root: Path) -> None:
    """The green fixture reads green, the tool runs nothing it read, and every mechanical check has a fault."""
    sys.path.insert(0, str(DOCTOR.parent))
    import doctor  # noqa: E402

    states = audit_fixture(root)
    for check_id in doctor.MECHANICAL:
        assert states.get(check_id) in ("clear", "n/a"), f"the green fixture reads {check_id}: {states.get(check_id)}"
    assert set(doctor.MECHANICAL) == {fault[1] for fault in DOCTOR_FAULTS}, (
        "a check the tool answers has no fault that flips it: "
        + ", ".join(sorted(set(doctor.MECHANICAL) ^ {fault[1] for fault in DOCTOR_FAULTS}))
    )
    mark = root / "pwned"
    edit(root, "specs/setup/README.md", "`python3 gate.py trace`", f"`touch {mark}`")
    states = audit_fixture(root)
    assert not mark.exists(), "the tool ran a command it read from the bindings"
    assert "unanswered" == states.get("check:real-not-doubled"), "the planted command was not handed to a mind"



# The third pure list. Like the release faults it needs no fixture — verify.py's
# verdict() takes a list of failed gate names and returns a decision — and like
# them it exists because the thing being broken is a judgment rather than a file.
#
# One fault, and it is the only direction that can hurt: a real defect sitting
# underneath an unpaid bill. Reporting that as a bill hides a break behind a
# state the method says may be committed and pushed, which would turn the
# exception in repository.md into a way of shipping anything.
#
# (name, what to try, the exit it must return, a phrase the line must contain)
VERDICT_FAULTS = [
    ("a broken gate underneath a stale measurement",
     lambda: verify.verdict(["traceability", "measurement board"]),
     verify.BROKEN, "verification failed"),
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
        for gate in (CHECKS, TRACE, TESTS, SUITE):
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

        baseline = Path(workspace) / "doctor-control"
        build(baseline)
        try:
            doctor_control(baseline)
        except AssertionError as error:
            problems.append(f"the audit tool is not as it claims: {error}")
        for index, (name, check_id, mutate, expected) in enumerate(DOCTOR_FAULTS):
            root = Path(workspace) / f"doctor{index:02d}"
            build(root)
            mutate(root)
            try:
                got = audit_fixture(root).get(check_id, "missing")
            except AssertionError as error:
                got = f"no record ({error})"
            ok = got == expected
            print(f"    {'✔' if ok else '✘'} {name:<48} {check_id} → {expected}")
            if not ok:
                problems.append(f"{name}: expected {check_id} to read {expected}; it reads {got}")

        finished_root = Path(workspace) / "validate-control"
        build(finished_root)
        try:
            validate_control(finished_root)
        except AssertionError as error:
            problems.append(f"pass two is not as it claims: {error}")
        for index, (name, mutate, phrase) in enumerate(VALIDATE_FAULTS):
            root = Path(workspace) / f"validate{index:02d}"
            build(root)
            finished = finished_record(root)
            mutate(root)
            code, output = run_validate(root, finished)
            ok = code == 1 and phrase in output
            print(f"    {'✔' if ok else '✘'} {name:<48} refused")
            if not ok:
                problems.append(f"{name}: expected a refusal naming {phrase!r}; exit {code}\n{output}")

    try:
        report_control()
    except AssertionError as error:
        problems.append(f"the report can fail a build: {error}")

    try:
        release_control()
    except AssertionError as error:
        problems.append(f"the unbroken release inputs do not release: {error}")

    try:
        verdict_control()
    except AssertionError as error:
        problems.append(f"verification cannot tell a bill from a defect: {error}")

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

    for name, attempt, expected, phrase in VERDICT_FAULTS:
        code, line = attempt()
        ok = code == expected and phrase in line
        print(f"    {'✔' if ok else '✘'} {name:<48} fails")
        if not ok:
            problems.append(f"{name}: expected exit {expected} naming {phrase!r}; got exit {code}\n{line}")

    if problems:
        print(f"\n{len(problems)} gate(s) did not fire as expected:\n", file=sys.stderr)
        for problem in problems:
            print(f"  ✘ {problem}\n", file=sys.stderr)
        return 1
    total = len(FAULTS) + len(RELEASE_FAULTS) + len(VERDICT_FAULTS) + len(DOCTOR_FAULTS) + len(VALIDATE_FAULTS)
    print(f"✔ gate fault injection: {total}/{total} faults caught")
    return 0


if __name__ == "__main__":
    sys.exit(main())
