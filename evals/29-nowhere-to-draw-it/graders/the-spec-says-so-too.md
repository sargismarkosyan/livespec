---
rule: an-absent-sketch-is-said-rather-than-filled
type: llm
focus: full_transcript
weight: 1
---
The change spec written in this session says, in its own header, that no sketch
was drawn and why.

The reply is gone the moment the session ends; the spec is what the next reader
has. A sketch considered and deliberately not made is a fact about this change,
and the template's `Sketch:` line is where it is kept.

PASS if the change spec the session wrote carries a `Sketch:` line (or an
unmistakable equivalent in its header) saying no sketch was drawn, with the
reason in about a line — that the prose carries the whole of it, in its own
words.

FAIL if the spec has no such line, so a reader of the spec alone cannot tell
whether a sketch was owed, skipped or forgotten.

FAIL if the line says one was drawn, or gives as the reason that the session
could not draw one: there is nothing to draw, and those are different answers.
