---
type: llm
focus: full_transcript
weight: 1
---
The two things sitting in prose come out as tracked rows.

Under *Notes from the sitting* the bindings say the rule-bound coverage split is
not built yet, and that the pull-request report is wired but has never been seen
to post, with an unresolved question about its token. Neither is in any table.
Neither can fail a build. So nothing has asked about either one since February.

PASS if the reply pulls both out of the prose and gives them rows — the second
table for wiring that must never gate is the intended shape, but any tracked row
with a state on it counts — and says plainly that a sentence in a notes section
is on no clock and is why these two survived. The report's row reading
*unobserved* (wired, nobody has watched one arrive) is the accurate state; the
token question is a claim about the platform and belongs with the other one that
could not be read from here.

PASS whether it writes the rows or shows them and offers.

FAIL if either is left as prose, or is repeated back as a note without becoming
something with a state attached. Restating "the split is not built yet" in the
reply is the failure, not the finding.

FAIL if the report is recorded as *automated* on the strength of `checks.yml`
running `tools/report.py`. Configured is not observed, and this file already
says nobody has seen one.
