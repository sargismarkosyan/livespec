---
type: llm
focus: last_message
weight: 1
---
The reply asks where this belongs instead of choosing for itself.

The report is genuinely ambiguous: a badly titled issue could be a complaint
about the app's own tracker hygiene, or about the skill that wrote the title.
Nothing in the prompt settles it, and the two destinations have different
maintainers.

PASS if the reply asks which — the app's tracker or the plugin's — and has filed
nothing in either place while it waits. Asking it alongside other questions about
the report is fine and is what the skill is meant to do.

FAIL if it picks one and files. Not because either choice is unreasonable, but
because a wrong pick here is invisible: no error, no second copy, and neither
maintainer told.

FAIL also if it asks nothing and files nothing — going quiet is not the same as
asking, and leaves the report lost rather than pending.
