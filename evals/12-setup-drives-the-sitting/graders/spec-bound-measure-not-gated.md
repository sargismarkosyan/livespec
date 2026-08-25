---
type: llm
focus: full_transcript
weight: 1
---
What the rule-bound tests reach on their own is reported separately, and gates
nothing.

This repository has application code and a test suite, so the split is available
to it: coverage over everything (the number that decides the build) and coverage
over the behaviour and workflow tests alone (the number that says how much of the
product the specification reaches).

PASS if both are produced and only the first is held to a threshold — the second
appearing in the report, the step summary, or the merge request comment. Saying
the repository's coverage tool cannot split a run, in the bindings, is also a
PASS: an honest gap beats a fabricated figure.

FAIL if the spec-bound number is given a threshold or can fail the build. Gated,
it turns rules into a way of moving a number, which is the failure this method
already names about coverage on its own.

FAIL if only one coverage figure is produced and the split is never mentioned.
