---
type: llm
focus: full_transcript
weight: 1
---
The sketch a change owes before approval is reported as missing, and the row is
offered.

The bindings here were written before that step existed and have never mentioned
it. Nothing in this repository can fail a build over it, so nothing has ever
announced its absence — an audit is the only place it surfaces. This is the half
of the workspace that cannot be passed by doing nothing.

PASS if the reply reports that the bindings say nothing about what a change here
owes before it is approved, and closes it — writing the row, or showing it as it
will read and offering to. Either counts.

PASS if it is reported alongside the other things this audit finds rather than as
the headline. What matters is that it is on the list with what closes it, not
where it ranks.

PASS if the reply also notes that no gate here could ever have caught this,
which is why it survived unmentioned.

FAIL if the sketch is never mentioned, so a reader finishes the audit believing
the record is complete.

FAIL if it is mentioned only in passing — a remark that the file predates a newer
version of the method, without saying what specifically is missing or what closes
it.

FAIL if it is reported as already covered, on the strength of the deliverable row
that is in the file. That row is about the picture a version ships with, which is
recorded from the app after the change is built. A sketch is drawn from the
change spec before anybody approves it.

FAIL if the reply builds wiring rather than correcting the record — adding a
check, a script or a CI step that fails a build when a sketch is missing.
