---
rule: what-is-shown-is-not-the-spec-again
type: llm
focus: full_transcript
weight: 1
---
The sketch carries evidence, and leaves the argument to the spec.

Read the sketch file's content in the transcript.

PASS if the page links or names the change spec, and does not restate who
this is for, the job behind the request, why now, or the end value as prose
sections of its own.

FAIL if the page has sections arguing the case (a "why" or "who it is for"
section, or the end value restated), or if it never points at the spec.
