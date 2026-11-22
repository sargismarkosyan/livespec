---
rule: a-failure-prints-what-it-means
type: llm
focus: full_transcript
weight: 1
---
The traceability gate the sitting wrote says why each failure happened and what
to do, not only what failed.

PASS if every failure the gate reports carries, beside where it is — the rule,
the test, the file — what it means and the fix, in words matching that
failure's row in the method's `gates.md`. At least: a live rule with no test
says to write the test or tag the rule `@planned`; a test naming an unknown rule
id says it is usually a typo or a renamed id. Messages built from one table in
the script, keyed by the kind of failure, are a strong pass.

FAIL if the messages only state the failure (`rule foo: no test`), if the reason
is in a comment or a README but not in what the gate prints, or if no gate
script was written in this sitting.
