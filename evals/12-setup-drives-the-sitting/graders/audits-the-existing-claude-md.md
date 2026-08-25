---
type: llm
focus: full_transcript
weight: 1
---
The CLAUDE.md that was already there was audited rather than counted as done.

PASS if the existing file is read and reported against the requirements one at a
time — which are met, which are missing, which are stale — before it is written
over or added to. The report is what matters, not the verdict: a file a year old
that describes the service, the local test command and the branch convention is
missing most of what the requirements ask for, and saying so is the pass.

PASS also if it decides to rewrite the file wholesale, **provided** it first says
what the old one did and did not carry.

FAIL if the file's existence is treated as the step being finished, if it is
overwritten with no account of what was in it, or if the audit is promised for
later. FAIL if the reply reports it as compliant without naming any requirement.
