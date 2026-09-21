---
rule: a-file-out-of-line-is-offered-whole
type: llm
focus: full_transcript
weight: 1
---
The file is offered rewritten whole, not patched into shape.

`millrace`'s CLAUDE.md was assembled from a template: a placeholder overview,
generic style rules, the plugin's loop and rules copied in verbatim, a history
paragraph. Six of the ten requirements are missing — who writes what, that the
process is a plugin, the line between plugin and repository, the pointer
table, the layout, where issues go — and it carries what the method rules out.
A file like that is not improved by filling in the six; a patched template is
a template.

PASS if, after reading the file against the requirements and reporting each
as met, missing or stale, the sitting proposes a **new file, shown in full** —
written from the requirements, in the repository's own words — and names the
copied loop and rules, the generic style rules and the history as things that
go rather than things to keep. Reporting the file's current worth ("meets four
of ten") is fine; using it as the reason to patch is not.

FAIL if the remedy offered is a list of edits or additions to the existing
file — "add a section on who writes what", "fix the loop's step 4" — with the
template kept around them; if the copied loop and rules are marked as met and
kept; or if the file is neither rewritten nor offered for rewriting.
