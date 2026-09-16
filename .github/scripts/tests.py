#!/usr/bin/env python3
"""Run the rule-bound tests, and refuse one that names no rule.

    python3 .github/scripts/tests.py [root]

`tests/` holds the ordinary tests this repository has — standard library
`unittest`, for the code it ships under `tools/`. The graded cases under
`evals/` hold the skills' judgment; this holds the code, the way method/testing.md
asks of any repository with a function to call. See specs/changes/0041.

Two things, in order. First the structural gate: every `test_*` method under
`tests/` is bound to a rule through `rulelib.rule()` — on the method, or on the
class it sits in — because a test outside a rule is an untraced test, and the
traceability gate reads those calls as claims. Then the tests themselves.

A root with no `tests/` directory is not a failure: the gates run on a fixture
that may carry none.
"""

from __future__ import annotations

import ast
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[2]
TESTS = ROOT / "tests"


def bound(decorators: list[ast.expr]) -> bool:
    for node in decorators:
        call = node if isinstance(node, ast.Call) else None
        if call is not None and getattr(call.func, "id", getattr(call.func, "attr", "")) == "rule":
            return True
    return False


def unbound_tests(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    loose: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_bound = bound(node.decorator_list)
            for item in node.body:
                if isinstance(item, ast.FunctionDef) and item.name.startswith("test_") and not (class_bound or bound(item.decorator_list)):
                    loose.append(f"{node.name}.{item.name}")
        elif isinstance(node, ast.FunctionDef) and node.name.startswith("test_") and node.col_offset == 0 and not bound(node.decorator_list):
            loose.append(node.name)
    return loose


def main() -> int:
    if not TESTS.exists():
        print("• no tests/ here — nothing to run")
        return 0
    files = sorted(TESTS.rglob("test_*.py"))
    problems: list[str] = []
    for path in files:
        for name in unbound_tests(path):
            problems.append(f"{path.relative_to(ROOT)}: {name} names no rule — wrap it in @rule('<id>'), or move it out of tests/")
    if problems:
        print("\n✘ tests outside any rule:\n", file=sys.stderr)
        for problem in problems:
            print(f"  ✘ {problem}", file=sys.stderr)
        return 1
    result = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-t", "."],
        cwd=ROOT, capture_output=True, text=True,
    )
    tail = (result.stderr or result.stdout).strip().splitlines()
    summary = tail[-1] if tail else ""
    if result.returncode != 0:
        print("\n✘ the tests are red:\n", file=sys.stderr)
        print("\n".join(tail[-40:]), file=sys.stderr)
        return 1
    print(f"✔ tests: {len(files)} file(s), every test bound to a rule — {summary}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
