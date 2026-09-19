---
type: llm
focus: full_transcript
weight: 1
---
The report describes the change, not only the state after it.

PASS if what was wired reads the spec layer on the base as well as on the branch,
so the report can say what this change moved — a delta, a before-and-after, a
"+1". Any mechanism is fine: a second run against the base ref, a stored baseline,
a diff. What matters is that a reviewer sees the movement.

FAIL if no report was wired at all. There is nothing here to pass on;
`wires-the-report` names the gap, and this grader does not excuse it.

FAIL if the report only prints current totals. "12 live rules" tells somebody
deciding whether to merge nothing about the change in front of them, and a report
they still have to compare by hand is the one most likely to go unread.

FAIL if it re-parses the spec tree itself to get those numbers rather than asking
the traceability gate for them. Two things counting the same rules is two things
that will eventually disagree.
