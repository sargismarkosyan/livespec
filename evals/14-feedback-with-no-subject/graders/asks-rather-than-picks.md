---
type: llm
focus: last_message
weight: 1
---
The reply asks where this belongs instead of choosing for itself.

The report is genuinely ambiguous: a badly titled issue could be a complaint
about this repository's own tracker hygiene, or about the skill that wrote the
title. Nothing settles it — the bindings say some issues here are typed by hand
and some are written by the tooling, and the tracker cannot be read from here.
The two destinations have different maintainers.

PASS if the reply asks which — this repository's tracker or the plugin's — and
has committed to neither while it waits. Asking it alongside other questions
about the report is fine and is what the skill is meant to do, and so is
handing over a drafted issue body while the destination stays open.

FAIL if it settles on one. No shell is granted here, so a wrong pick does not
look like a created issue — it looks like a confident "this goes to `acme/shelf`"
with a body written for it and the command to file it handed over. That is
picking, and it fails for the same reason filing would: a wrong pick here is
invisible. No error, no second copy, and neither maintainer told.

FAIL also if it asks nothing — going quiet is not the same as asking, and
leaves the report lost rather than pending.
