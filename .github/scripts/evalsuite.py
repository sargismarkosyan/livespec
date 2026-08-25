#!/usr/bin/env python3
"""Gate 2 — the eval suite, in place of coverage.

A repository that ships code measures lines, branches and functions. This one
ships judgment, and there is nothing here for a coverage tool to measure: the
product is seven skills' worth of prose that a model reads. The honest analogue
is **which promises are actually exercised** — every skill held by at least one
case, every case scored on what came out rather than on whether something fired,
and the floor in evals/README.md made executable instead of aspirational.

What this cannot do is run the cases: they cost money per session, and CI pays
for nothing. The runner is `evals/runner/run.py` (the native `claude plugin
eval` stays gated behind early access); this gate is the structural half — the
cases exist, they cover every skill, and none of them has been softened into a
case that cannot fail.

Run: python3 .github/scripts/evalsuite.py [root]
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from caselib import cases  # noqa: E402

ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[2]

# A single run of an LLM grader is noise, not a measurement.
MIN_RUNS = 3

# Graders that score what came out. `tool_used` says only that something fired —
# and under ablation it is excluded from the score entirely, so a case graded by
# nothing else scores zero in both arms and measures nothing at all.
OUTCOME_TYPES = {"llm", "regex", "file_exists", "baseline", "tool_order"}

# The invocation the suite is meaningless without. A score with no baseline is
# not a measurement, and the agent's own model prefers its own output.
REQUIRED_INVOCATION = ["--ablation with-without", "--judge-model"]

# `--allow-tools` is an operator grant: these are refused whatever a case's own
# `allowed_tools` says. A case that lists one it is never granted runs without
# it — and a grader asserting "no file under src/ was created" then passes
# because the agent could not create anything at all. That grader is not
# strict, it is inert, and it reads as green in both arms.
GATED_TOOLS = {"Bash", "Write", "Edit", "WebFetch", "WebSearch"}

failures: list[str] = []
notes: list[str] = []


def fail(where: str, message: str) -> None:
    failures.append(f"{where}: {message}")


suite = cases(ROOT)
skills = sorted(p.parent.name for p in (ROOT / "skills").glob("*/SKILL.md"))

if not suite:
    # The coverage rule that matters most: refuse to pass on a measurement of
    # nothing. An empty suite reporting green is the most convincing false green
    # there is.
    fail("evals/", "holds no cases; this gate will not report green on a measurement of nothing")

for case in suite:
    where = f"evals/{case['name']}"
    if not case["graders"]:
        fail(where, "has no graders; a case that grades nothing cannot fail")
        continue
    for grader in case["graders"]:
        name = grader["path"].name
        if not grader["type"]:
            fail(f"{where}/graders/{name}", "has no type: in its frontmatter")
        if grader["type"] == "llm" and not grader["body"]:
            fail(f"{where}/graders/{name}", "is an llm grader with an empty rubric; it will pass on anything")
    if not any(g["type"] in OUTCOME_TYPES for g in case["graders"]):
        fail(
            where,
            "is graded only by what fired, never by what came out. tool_used alone is never a case — "
            "under ablation it is excluded from the score, so this measures nothing.",
        )
    if case["runs"] < MIN_RUNS:
        fail(where, f"runs {case['runs']} time(s); the floor is {MIN_RUNS}, because a single run of an LLM grader is noise")
    if case["scaffold"] is not None and not case["scaffold"].is_file():
        fail(
            where,
            f"declares scaffold_script: {case['scaffold'].name}, which does not exist in the case directory — "
            "the case would run against an empty workspace and measure the stall, not the judgment",
        )
    for skill in case["claims"]["skills"]:
        if skill not in skills:
            fail(where, f"is tagged skill:{skill}, which is not a skill in skills/")

negatives = [c for c in suite if c["negative"]]
if not negatives:
    fail(
        "evals/",
        "has no should-not-fire case. Seven descriptions load in every session; the cost of widening "
        "one is paid here, or by a user wondering why an interview started.",
    )

covered: dict[str, list[str]] = {skill: [] for skill in skills}
for case in suite:
    for skill in case["claims"]["skills"]:
        if skill in covered:
            covered[skill].append(case["name"])

for skill, holders in sorted(covered.items()):
    if not holders:
        fail(
            f"skills/{skill}",
            "is held by no eval case. Every skill costs context in every session; one that nothing "
            "holds cannot be changed safely. Tag a case with skill:" + skill + ".",
        )

readme = ROOT / "evals" / "README.md"
if not readme.exists():
    fail("evals/README.md", "is missing; it is where the floor is written down")
else:
    text = readme.read_text()
    for required in REQUIRED_INVOCATION:
        if required not in text:
            fail("evals/README.md", f"no longer names {required!r}; the floor says the suite is run with it")

    if any(case["scaffold"] for case in suite) and "--scaffold" not in text:
        fail(
            "evals/README.md",
            "does not name '--scaffold' in the documented invocation; a case carries a scaffold_script, "
            "and a run without the flag measures an empty workspace where the fixture should be",
        )

    needed = sorted({tool for case in suite for tool in case["allowed_tools"] if tool in GATED_TOOLS})
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith(("python3 evals/runner/run.py", "claude plugin eval")):
            continue
        granted = re.split(r"\s--", line + " --")
        grant = next((part for part in granted if part.startswith("allow-tools")), "")
        missing = [tool for tool in needed if tool not in grant.split()]
        if missing:
            fail(
                "evals/README.md",
                f"the documented invocation `{line}` never grants {', '.join(missing)}, which case "
                f"`allowed_tools` ask for. Graders that check what the agent created cannot fail "
                f"when it was never able to create anything.",
            )

for skill, holders in sorted(covered.items()):
    held = ", ".join(holders) if holders else "— nothing"
    print(f"    {skill:<18} {held}")
notes.append(
    f"{len(suite)} case(s), {len(negatives)} should-not-fire, "
    f"{sum(len(c['graders']) for c in suite)} graders, minimum {MIN_RUNS} runs each"
)

for note in notes:
    print(f"  {note}")

if failures:
    print(f"\n{len(failures)} eval-suite problem(s):\n", file=sys.stderr)
    for problem in failures:
        print(f"  ✘ {problem}", file=sys.stderr)
    sys.exit(1)

print(f"✔ eval suite: {len(skills)} skill(s) held by {len(suite)} case(s)")
