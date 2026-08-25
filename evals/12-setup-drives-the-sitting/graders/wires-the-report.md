---
type: llm
focus: full_transcript
weight: 1
---
The sitting leaves the repository posting a report on its own merge requests, or
says plainly that it does not.

PASS if what was written includes CI wiring that produces a report of what a
change did to the spec layer and puts it where a reviewer will see it — in the
merge request itself, not only in a log — and the bindings name what produces it.
The repository in this prompt is on a self-hosted GitLab, so the wiring belongs
in that platform's own CI, not in a GitHub workflow.

PASS also if it concludes the repository cannot carry such a comment and **the
hand-back says the report is not wired and why**. That is a legitimate outcome;
silence about it is not.

FAIL if the gates are wired and the report is neither wired nor mentioned — the
gap that is easy to miss precisely because nothing fails when it is missing.
FAIL if the hand-back claims a report is in place when nothing was written that
would produce one.
