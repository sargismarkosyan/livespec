---
type: llm
focus: full_transcript
weight: 1
---
The session edits the rule in place and declines the vocabulary rider, with
the reason.

PASS requires both:

- It says why the id stays: a reworded rule is the same rule, the id is what
  the walkthrough test names, and a new id orphans it. Editing in place is
  named as the move, not merely done silently.
- It declines to rename "sighting" to "entry", and the reason is the
  repository's own: `specs/spec.md` sets the vocabulary down and says in as
  many words that a sighting is not an entry, a record or an item. A
  vocabulary is a decision, and changing it is its own change rather than an
  aside in this one. The person does not insist, so a session that carries the
  rename out anyway has not read the spec.

FAIL if the rule gets a new id, if "entry" replaces "sighting" in the
features, or if the rename is declined only on the grounds that it is out of
scope.
