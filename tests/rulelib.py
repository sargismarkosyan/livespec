"""`rule()` — how a test here names the rule it exists for.

    from rulelib import rule

    @rule("the-tool-runs-nothing-it-read")
    def test_a_planted_command_leaves_no_mark(self): ...

This is the repository's own binding for what method/testing.md calls the
`rule()` helper: it looks the id up in specs/features/ and refuses at import
time if the id does not exist or is still tagged `@planned`, listing the ids
that do. trace.py reads the same calls as claims, so a live rule no test claims
fails the traceability gate, and a `@planned` rule a test claims fails it too.

Standard library only. Decorate the test method, or the whole TestCase where
every test in it answers to one rule.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FEATURES = ROOT / "specs" / "features"
RULE_TAG = re.compile(r"@rule:([a-z0-9]+(?:-[a-z0-9]+)*)")


def rules() -> dict[str, bool]:
    """Every rule id under specs/features/, and whether it is still @planned."""
    found: dict[str, bool] = {}
    for path in sorted(FEATURES.rglob("*.feature")):
        for line in path.read_text(encoding="utf-8").splitlines():
            match = RULE_TAG.search(line)
            if match:
                found[match.group(1)] = "@planned" in line
    return found


def rule(rule_id: str):
    known = rules()
    if rule_id not in known:
        raise LookupError(
            f"no @rule:{rule_id} under specs/features/. Rule ids are permanent; this is usually a typo. "
            f"Ids that exist: {', '.join(sorted(known))}"
        )
    if known[rule_id]:
        raise LookupError(
            f"@rule:{rule_id} is still @planned. The tag comes off in the change that makes the rule true, "
            "which is the change that writes this test."
        )

    def bind(target):
        target.__rule__ = rule_id
        return target

    return bind
