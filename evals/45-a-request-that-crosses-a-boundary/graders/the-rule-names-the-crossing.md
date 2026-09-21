---
rule: refine-spec-asks-for-the-boundary-misbehaving
type: llm
focus: full_transcript
weight: 1
---
The rule written names the boundary it crosses and carries an example of it
misbehaving.

The method's tag for a rule that cannot be true without a boundary is
`@crosses:<id>`, naming the boundary's row — here `@crosses:network` — and the
rule carries an Example of that boundary going wrong, not only of it working.

PASS if the Gherkin the session writes for the refresh includes a rule tagged
`@crosses:network` (or the boundary id the bindings use for the gauge service)
with an Example of the service down, slow or refusing — the harbourmaster shown
that the reading is stale, or an error, rather than an old reading passed off as
current. Writing the crossing tag and a misbehaving example both count; a
misbehaving example without the tag is a partial pass worth noting, the tag
alone is not.

FAIL if the rule carries only a happy-path example, if no crossing tag is
written where the boundaries table names the service, or if the session writes
no feature file at all.
