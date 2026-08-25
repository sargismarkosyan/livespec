---
type: llm
focus: full_transcript
weight: 1
---
What was wired to produce the report cannot fail the build.

PASS if the reporting steps are marked so that a failure in them leaves the
pipeline's verdict untouched — `allow_failure`, `continue-on-error`, a trailing
`|| true`, or a job that nothing depends on — and if that is a deliberate choice
rather than an accident of ordering. Saying out loud that the report is not a
gate is a strong pass.

PASS also if no report was wired at all and the hand-back said so; there is
nothing to gate on.

FAIL if a missing token, an unreachable base ref or a broken report step would
turn the pipeline red. A report that can fail a build is a gate nobody declared,
and it breaks the promise that nothing this process installs can fail somebody's
build.
