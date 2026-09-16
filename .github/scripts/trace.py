#!/usr/bin/env python3
"""Gate 1 — traceability, both directions.

    rule      ->  eval case     every live rule is claimed by a case
    case      ->  rule          every case names what it exists for, and a
                                should-not-fire case claims only @refusal rules
    feature   ->  workflow      every feature says what it serves
    workflow  ->  feature/case/persona/journey

The tests in this repository are eval cases: the product is judgment, and the
only way to hold judgment is to run it against a prompt and grade what comes
back. So `tags: [rule:<id>]` on a case is what `rule('<id>', ...)` is in a repo
that ships code. See specs/setup/README.md.

What this gate cannot prove is that a case *passes* — running the suite costs
money per session and is a maintainer step (evals/runner/run.py), never CI's.
This proves the case exists, claims a live rule, and meets the floor. The
judging half is that runner, and the bindings say so rather than implying this
covers it.

Run: python3 .github/scripts/trace.py [root] [--json]

`--json` prints the counts this gate already worked out, and nothing else. It
exists so the pull-request report can describe the spec layer without parsing
`specs/` a second time — `gates.md` is explicit that a report which re-derives
what the gate proved is a second copy of the gate's logic waiting to drift.
"""

from __future__ import annotations

import ast
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from caselib import cases  # noqa: E402

arguments = [a for a in sys.argv[1:] if a != "--json"]
AS_JSON = "--json" in sys.argv
ROOT = Path(arguments[0]).resolve() if arguments else Path(__file__).resolve().parents[2]

NS_TAG = re.compile(r"@(feature|rule|workflow|persona|journey|crosses):([A-Za-z0-9][A-Za-z0-9._-]*)")
FLAG = re.compile(r"@(planned|retired|refusal)\b")

# The boundaries a @crosses:<name> may name, read from this repository's
# boundaries table — the `boundary:<name>` cells 0039 writes. The tag carries
# the name after `boundary:`, the way @workflow: carries a workflow id without
# repeating its namespace, so `@crosses:store` names the `boundary:store` row.
# A crossing that names a name no row declares is a dangling reference; a
# crossing rule with one example has no case of the boundary going wrong.
# See specs/changes/0053.
BOUNDARY_NAME = re.compile(r"\|\s*`boundary:([a-z0-9][a-z0-9-]*)`")


def boundary_names() -> set[str]:
    path = ROOT / "specs" / "setup" / "README.md"
    if not path.is_file():
        return set()
    return set(BOUNDARY_NAME.findall(path.read_text(encoding="utf-8")))

# Soft limits: small per-component files are the point, and a hard cap on them
# is not. Past these, add a file rather than grow one.
MAX_FEATURE_LINES = 120
MAX_RULES_PER_FEATURE = 6

failures: list[str] = []
warnings: list[str] = []
notes: list[str] = []


def fail(where: str, message: str) -> None:
    failures.append(f"{where}: {message}")


def warn(where: str, message: str) -> None:
    warnings.append(f"{where}: {message}")


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def tags_of(lines: list[str]) -> tuple[dict[str, list[str]], set[str]]:
    """Namespaced ids and bare flags from a run of tag lines."""
    ids: dict[str, list[str]] = {}
    flags: set[str] = set()
    for line in lines:
        for namespace, value in NS_TAG.findall(line):
            ids.setdefault(namespace, []).append(value)
        flags.update(FLAG.findall(line))
    return ids, flags


def parse_gherkin(path: Path) -> dict:
    """One Gherkin file, read for its tags and its shape."""
    lines = path.read_text().splitlines()
    doc = {
        "path": path,
        "lines": len(lines),
        "ids": {},
        "flags": set(),
        "name": "",
        "features": 0,
        "rules": [],
        "loose_examples": 0,
    }
    pending: list[str] = []
    current: dict | None = None
    for number, raw in enumerate(lines, 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("@"):
            pending.append(line)
            continue
        if line.startswith("Feature:"):
            doc["features"] += 1
            doc["ids"], doc["flags"] = tags_of(pending)
            doc["name"] = line[len("Feature:") :].strip()
            if not doc["name"]:
                fail(rel(path), f"line {number}: the Feature: line has no name")
            current = None
        elif line.startswith("Rule:"):
            ids, flags = tags_of(pending)
            name = line[len("Rule:") :].strip()
            if not name:
                fail(rel(path), f"line {number}: the Rule: line has no name")
            current = {
                "id": (ids.get("rule") or [None])[0],
                "name": name,
                "planned": "planned" in flags,
                "refusal": "refusal" in flags,
                "crosses": ids.get("crosses", []),
                "examples": 0,
                "line": number,
            }
            doc["rules"].append(current)
        elif line.startswith(("Example:", "Scenario:", "Scenario Outline:")):
            if not line.split(":", 1)[1].strip():
                fail(rel(path), f"line {number}: the {line.split(':')[0]}: line has no name")
            if current is None:
                doc["loose_examples"] += 1
            else:
                current["examples"] += 1
        else:
            continue
        pending = []
    return doc


def parse_markdown_tags(path: Path) -> tuple[dict[str, list[str]], set[str]]:
    """A persona or journey declares itself on its first non-empty line."""
    for line in path.read_text().splitlines():
        if line.strip():
            return tags_of([line])
    return {}, set()


# --- read the layers --------------------------------------------------------

feature_files = sorted((ROOT / "specs" / "features").rglob("*.feature")) if (ROOT / "specs" / "features").is_dir() else []
workflow_files = sorted((ROOT / "specs" / "workflows").glob("*.feature")) if (ROOT / "specs" / "workflows").is_dir() else []
persona_files = sorted(p for p in (ROOT / "specs" / "personas").glob("*.md") if p.name != "README.md") if (ROOT / "specs" / "personas").is_dir() else []
journey_files = sorted(p for p in (ROOT / "specs" / "journeys").glob("*.md") if p.name != "README.md") if (ROOT / "specs" / "journeys").is_dir() else []

features = [parse_gherkin(p) for p in feature_files]
workflows = [parse_gherkin(p) for p in workflow_files]
suite = cases(ROOT)

seen_ids: dict[str, str] = {}


def unique(kind: str, value: str, where: str) -> None:
    """Ids are permanent and unique across the whole repository."""
    key = f"{kind}:{value}"
    if key in seen_ids:
        fail(where, f"@{key} is already declared in {seen_ids[key]}; ids are unique across the repository")
    else:
        seen_ids[key] = where


personas: dict[str, dict] = {}
for path in persona_files:
    ids, flags = parse_markdown_tags(path)
    value = (ids.get("persona") or [None])[0]
    if not value:
        fail(rel(path), "declares no @persona: on its first line")
        continue
    unique("persona", value, rel(path))
    personas[value] = {"path": path, "retired": "retired" in flags}

journeys: dict[str, dict] = {}
for path in journey_files:
    ids, _ = parse_markdown_tags(path)
    value = (ids.get("journey") or [None])[0]
    if not value:
        fail(rel(path), "declares no @journey: on its first line")
        continue
    unique("journey", value, rel(path))
    journeys[value] = {"path": path}

crossable = boundary_names()
live_rules: dict[str, dict] = {}
planned_rules: dict[str, dict] = {}
for doc in features:
    where = rel(doc["path"])
    if doc["features"] != 1:
        fail(where, f"holds {doc['features']} Feature: lines; one feature per file")
    if not doc["ids"].get("feature"):
        fail(where, "declares no @feature: id")
    for value in doc["ids"].get("feature", []):
        unique("feature", value, where)
    if doc["loose_examples"]:
        fail(where, f"has {doc['loose_examples']} example(s) outside any Rule:; every example belongs to a rule")
    if doc["lines"] > MAX_FEATURE_LINES:
        warn(where, f"is {doc['lines']} lines (soft limit {MAX_FEATURE_LINES}); add a file rather than grow this one")
    if len(doc["rules"]) > MAX_RULES_PER_FEATURE:
        warn(where, f"holds {len(doc['rules'])} rules (soft limit {MAX_RULES_PER_FEATURE})")
    for rule in doc["rules"]:
        if not rule["id"]:
            fail(where, f"line {rule['line']}: rule {rule['name']!r} carries no @rule: id")
            continue
        unique("rule", rule["id"], where)
        if not rule["examples"]:
            fail(where, f"@rule:{rule['id']} has no Example:; a rule with no example is an opinion")
        for cross in rule["crosses"]:
            if cross not in crossable:
                fail(where, f"@rule:{rule['id']} @crosses:{cross}, a boundary the bindings declare no row for; add a boundary row, or name one that exists")
        if rule["crosses"] and rule["examples"] < 2:
            warn(where, f"@rule:{rule['id']} crosses {', '.join(rule['crosses'])} and has {rule['examples']} example(s); a crossing with no example of the boundary misbehaving has specced the demo")
        (planned_rules if rule["planned"] else live_rules)[rule["id"]] = {"doc": doc, "rule": rule}

workflow_index: dict[str, dict] = {}
for doc in workflows:
    where = rel(doc["path"])
    value = (doc["ids"].get("workflow") or [None])[0]
    if doc["rules"]:
        fail(where, "holds a Rule:; a workflow is one bounded attempt, and its examples hang off the Feature: line")
    if not value:
        fail(where, "declares no @workflow: id")
        continue
    unique("workflow", value, where)
    workflow_index[value] = {
        "doc": doc,
        "personas": doc["ids"].get("persona", []),
        "journeys": doc["ids"].get("journey", []),
        "planned": "planned" in doc["flags"],
        "features": [],
        "walked_by": [],
    }

# --- direction 1: rule -> case, feature -> workflow -------------------------

claimed_rules: dict[str, list[str]] = {}
claimed_workflows: dict[str, list[str]] = {}
for case in suite:
    for value in case["claims"]["rules"]:
        claimed_rules.setdefault(value, []).append(case["name"])
    for value in case["claims"]["workflows"]:
        claimed_workflows.setdefault(value, []).append(case["name"])

# The second kind of claim: a test under tests/ names its rule through
# rulelib.rule("<id>"), the method's ordinary shape, for the code this
# repository ships. The call is the claim — read off the syntax, so that a
# marker beside it can empty it: a test the runner skips, or expects to fail,
# did not run, and a test that did not run claims nothing. The markers are
# this repository's binding, unittest's own. See specs/changes/0041 and 0051.
SKIP_MARKERS = {"skip", "skipIf", "skipUnless", "expectedFailure"}


def decorator_name(node: ast.expr) -> str:
    target = node.func if isinstance(node, ast.Call) else node
    return getattr(target, "attr", getattr(target, "id", ""))


def rule_of(decorators: list[ast.expr]) -> str | None:
    for node in decorators:
        if isinstance(node, ast.Call) and decorator_name(node) == "rule" and node.args and isinstance(node.args[0], ast.Constant):
            return str(node.args[0].value)
    return None


def marker_of(decorators: list[ast.expr]) -> str | None:
    for node in decorators:
        if decorator_name(node) in SKIP_MARKERS:
            return decorator_name(node)
    return None


def test_claims(path: Path) -> list[tuple[str, str, str | None]]:
    """(test, rule id, marker) for every rule-bound test in a file. A rule or a
    marker on the class applies to every test method in it."""
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    found: list[tuple[str, str, str | None]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_rule, class_marker = rule_of(node.decorator_list), marker_of(node.decorator_list)
            for item in node.body:
                if isinstance(item, ast.FunctionDef) and item.name.startswith("test_"):
                    value = rule_of(item.decorator_list) or class_rule
                    if value:
                        found.append((f"{node.name}.{item.name}", value, marker_of(item.decorator_list) or class_marker))
        elif isinstance(node, ast.FunctionDef) and node.col_offset == 0 and node.name.startswith("test_"):
            value = rule_of(node.decorator_list)
            if value:
                found.append((node.name, value, marker_of(node.decorator_list)))
    return found


tests_claiming = 0
for path in (sorted((ROOT / "tests").rglob("test_*.py")) if (ROOT / "tests").exists() else []):
    where = rel(path)
    for name, value, marker in test_claims(path):
        if marker:
            fail(
                where,
                f"{name} is marked @{marker} and claims @rule:{value}; a test that did not run claims nothing, "
                "and the rule is untested until the marker comes off",
            )
            continue
        tests_claiming += 1
        claimed_rules.setdefault(value, []).append(where)
        if value not in live_rules and value not in planned_rules:
            fail(where, f"claims @rule:{value}, which does not exist. Rule ids are permanent; this is usually a typo or a rename.")

for value, entry in sorted(live_rules.items()):
    if value not in claimed_rules:
        fail(
            rel(entry["doc"]["path"]),
            f"@rule:{value} is live and no eval case claims it. Write the case, or tag the rule @planned if it is not built yet.",
        )

for value, entry in sorted(planned_rules.items()):
    if value in claimed_rules:
        fail(
            rel(entry["doc"]["path"]),
            f"@rule:{value} is @planned but {', '.join(claimed_rules[value])} claims it; the tag should have come off in the change that made it true",
        )

for doc in features:
    where = rel(doc["path"])
    named = doc["ids"].get("workflow", [])
    if not named:
        fail(where, "names no @workflow:; it serves nothing anybody wrote down")
    for value in named:
        if value not in workflow_index:
            fail(where, f"names @workflow:{value}, which does not exist")
        else:
            workflow_index[value]["features"].append(where)

# --- direction 2: case -> rule, workflow -> everything ----------------------

for case in suite:
    where = f"evals/{case['name']}"
    if case["negative"]:
        # A case asserting nothing fires cannot verify a rule that promises a
        # behaviour — but a rule whose whole promise is that nothing happens is
        # verified by exactly this and nothing else. `@refusal` is what tells
        # them apart, and without it the only honest options were a permanent
        # warning or a @planned tag on built behaviour.
        for value in case["claims"]["rules"]:
            entry = live_rules.get(value) or planned_rules.get(value)
            if entry is None:
                fail(where, f"claims @rule:{value}, which does not exist. Rule ids are permanent; this is usually a typo or a rename.")
            elif not entry["rule"]["refusal"]:
                warn(
                    where,
                    f"is a should-not-fire case and claims @rule:{value}, which promises a behaviour; "
                    "a case asserting nothing fires cannot verify one. Tag the rule @refusal if its "
                    "promise is that nothing happens.",
                )
        continue
    # A case that claims nothing is not a failure. `rule -> case` already fails a
    # rule nothing verifies, and that direction needs no list of exempt names to
    # work while the spec layer is still empty.
    for value in case["claims"]["rules"]:
        if value not in live_rules and value not in planned_rules:
            fail(where, f"claims @rule:{value}, which does not exist. Rule ids are permanent; this is usually a typo or a rename.")
    for value in case["claims"]["workflows"]:
        if value not in workflow_index:
            fail(where, f"claims @workflow:{value}, which does not exist")
        else:
            workflow_index[value]["walked_by"].append(case["name"])

for value, entry in sorted(workflow_index.items()):
    where = rel(entry["doc"]["path"])
    if not entry["features"] and not entry["planned"]:
        fail(where, f"@workflow:{value} is claimed by no feature; tag a feature with it, or tag this workflow @planned")
    if entry["features"] and entry["planned"]:
        fail(where, f"@workflow:{value} is @planned but {', '.join(entry['features'])} claims it; the tag should have come off")
    if not entry["walked_by"] and not entry["planned"]:
        fail(where, f"@workflow:{value} is walked by no eval case; its Example: blocks are a costume until one walks it")
    live_personas = [p for p in entry["personas"] if p in personas and not personas[p]["retired"]]
    for named in entry["personas"]:
        if named not in personas:
            fail(where, f"names @persona:{named}, which does not exist")
    if not live_personas:
        fail(where, f"@workflow:{value} names no live @persona:; a workflow for nobody, or one pointing only at a @retired persona")
    for named in entry["journeys"]:
        if named not in journeys:
            fail(where, f"names @journey:{named}, which does not exist")
    if not entry["journeys"]:
        # Where an attempt sits in the arc is a judgment, so this warns. A warning
        # surviving two versions either becomes an error or gets deleted.
        warn(where, f"@workflow:{value} names no @journey:; where it sits in the arc is unrecorded")

named_personas = {p for entry in workflow_index.values() for p in entry["personas"]}
for value, entry in sorted(personas.items()):
    if value not in named_personas and not entry["retired"]:
        fail(
            rel(entry["path"]),
            f"@persona:{value} is named by no workflow; nobody does anything as them. Give them a workflow, or tag the file @retired.",
        )

# --- the file every session reads first -------------------------------------
#
# CLAUDE.md is read by every session before anything under specs/, and until
# 0048 nothing refused a change that gutted it or grew it into a copy of the
# method. What is read here is only what a script can decide: the size against
# the ceiling the bindings name, that it is at the root, that it carries the
# loop as a numbered list of at most eight steps, a block of commands, and a
# link to the bindings that resolves. What it says is a mind's to read — setup
# §6 at the sitting, the audit after — and nothing here pretends otherwise.

CONTEXT_FILE = "CLAUDE.md"
BINDINGS = Path("specs") / "setup" / "README.md"
MAX_LOOP_STEPS = 8
# The one number the method carries: the reader's own target for a CLAUDE.md,
# past which its documentation says adherence drops. A repository's ceiling is
# its own only up to here. See method/claude-md.md, Length, and specs/changes/0049.
MAX_CONTEXT_FILE_LINES = 200
CEILING_ROW = re.compile(r"^\|\s*\*\*CLAUDE\.md ceiling\*\*\s*\|(.*)\|\s*$", re.IGNORECASE)
FENCE = re.compile(r"^\s*(```|~~~)")
ORDERED = re.compile(r"^\s*(\d+)\.\s")
LINK_TARGET = re.compile(r"\]\((?!https?:|#|mailto:)([^)\s]+)\)")


def ceiling_in(bindings_text: str) -> int | None:
    """The first number in the bindings' CLAUDE.md ceiling row, or None where there is no row."""
    for line in bindings_text.splitlines():
        match = CEILING_ROW.match(line)
        if match:
            number = re.search(r"\d[\d,]*", match.group(1))
            return int(number.group(0).replace(",", "")) if number else None
    return None


def longest_numbered_run(lines: list[str]) -> int:
    """The longest run of consecutive 1., 2., 3. … items outside fenced blocks —
    the loop, if there is one. Blank and indented lines inside a run continue it."""
    longest = run = expected = 0
    fenced = False
    for raw in lines:
        if FENCE.match(raw):
            fenced = not fenced
            continue
        if fenced:
            continue
        match = ORDERED.match(raw)
        if match and int(match.group(1)) == 1:
            run, expected = 1, 2
        elif match and int(match.group(1)) == expected:
            run, expected = run + 1, expected + 1
        elif match or (raw.strip() and not raw.startswith((" ", "\t"))):
            run, expected = 0, 0
        longest = max(longest, run)
    return longest


context_path = ROOT / CONTEXT_FILE
if not context_path.is_file():
    fail(CONTEXT_FILE, "no CLAUDE.md at the root; the file every session reads first is missing")
else:
    context_lines = context_path.read_text(encoding="utf-8").splitlines()
    bindings_path = ROOT / BINDINGS
    ceiling = ceiling_in(bindings_path.read_text(encoding="utf-8")) if bindings_path.is_file() else None
    if ceiling is None:
        fail(str(BINDINGS), "names no CLAUDE.md ceiling; a number nobody wrote is not a pass — write the row from the file's size")
    elif ceiling > MAX_CONTEXT_FILE_LINES:
        fail(
            str(BINDINGS),
            f"names a CLAUDE.md ceiling of {ceiling} lines, above the {MAX_CONTEXT_FILE_LINES} the reader's own "
            "documentation allows; the number is the repository's only up to there",
        )
    elif len(context_lines) > ceiling:
        fail(
            CONTEXT_FILE,
            f"is {len(context_lines)} lines against a ceiling of {ceiling} in {BINDINGS}; move a copy to the "
            "bindings and link it, or raise the number in this change with the reason beside it",
        )
    steps = longest_numbered_run(context_lines)
    if steps == 0:
        fail(CONTEXT_FILE, "carries no numbered list; the loop, numbered, is what an agent follows")
    elif steps > MAX_LOOP_STEPS:
        fail(CONTEXT_FILE, f"carries a numbered list of {steps} steps; the loop is at most {MAX_LOOP_STEPS}")
    if sum(1 for line in context_lines if FENCE.match(line)) < 2:
        fail(CONTEXT_FILE, "carries no fenced block; the commands go in one")
    targets = LINK_TARGET.findall("\n".join(context_lines))
    resolved = {(context_path.parent / target.split("#", 1)[0]).resolve() for target in targets}
    if bindings_path.resolve() not in resolved:
        fail(CONTEXT_FILE, f"does not link to {BINDINGS}, the bindings; every command a session runs is read from there")

# --- the map, generated, never typed ----------------------------------------

if AS_JSON:
    # Nothing human goes to stdout in this mode: whoever asked for JSON is going
    # to parse it, and a table printed above it is a parse error with a friendly
    # face.
    pass
elif not features and not workflow_index and not personas:
    # An empty layer and a broken one look the same to a gate that reports a
    # percentage. This one says which it is.
    print("    the spec layer is empty — 0 features, 0 rules, 0 workflows. Nothing to trace yet;")
    print("    the gate arms itself the moment the first feature file lands.")
else:
    for doc in features:
        traced = sum(1 for r in doc["rules"] if r["id"] in claimed_rules)
        planned = sum(1 for r in doc["rules"] if r["planned"])
        total = len(doc["rules"])
        print(f"    {rel(doc['path']):<52} {traced}/{total} traced, {planned} planned")
    print(f"    {len(live_rules)} live rule(s), {len(planned_rules)} planned, "
          f"{len(claimed_rules)} claimed by {len(suite)} eval case(s)")

if workflow_index and not AS_JSON:
    print("\n  the map — every workflow, who it is for, what serves it")
    for value, entry in sorted(workflow_index.items()):
        who = ", ".join(entry["personas"]) or "nobody"
        print(f"    @workflow:{value}  for {who}")
        for served in entry["features"] or ["(nothing yet)"]:
            print(f"      {served}")

cases_claiming = sum(1 for c in suite if c["claims"]["rules"] or c["claims"]["workflows"])
notes.append(f"{len(suite)} eval case(s), {cases_claiming} claiming a rule or a workflow")

if AS_JSON:
    # One code path produces both readings. A second traversal for the report
    # would be the drift `gates.md` names, arriving through the door marked
    # "it is only a report".
    print(json.dumps({
        "personas": {
            "live": sum(1 for p in personas.values() if not p["retired"]),
            "retired": sum(1 for p in personas.values() if p["retired"]),
        },
        "journeys": len(journeys),
        "workflows": {
            "total": len(workflow_index),
            "planned": sum(1 for w in workflow_index.values() if w["planned"]),
        },
        "features": len(features),
        "rules": {"live": len(live_rules), "planned": len(planned_rules)},
        "cases": {
            "total": len(suite),
            "claiming": cases_claiming,
            "negative": sum(1 for c in suite if c["negative"]),
        },
        "failures": len(failures),
        "warnings": len(warnings),
    }, indent=2))
    sys.exit(1 if failures else 0)

for note in notes:
    print(f"  {note}")
for warning in warnings:
    print(f"  ⚠ {warning}")

if failures:
    print(f"\n{len(failures)} traceability problem(s):\n", file=sys.stderr)
    for problem in failures:
        print(f"  ✘ {problem}", file=sys.stderr)
    sys.exit(1)

print(f"✔ traceability: {len(live_rules)} live rule(s) traced, {len(workflow_index)} workflow(s) mapped")
