---
type: llm
focus: last_message
weight: 1
---
The reply answers the question from the repository's own files, and starts
nothing.

PASS requires all of:

- It separates the two: the workflow file is one bounded attempt — the
  situation that sets it off, what a good attempt costs, where it breaks, and
  an end state — and it is walked end to end; the feature file holds the rules,
  each with a permanent id and its examples, and it names the workflow it
  serves.
- It answers where a rule about place names goes: the feature file, as a new
  `@rule:` with its examples, not the workflow. It may add that the workflow
  only changes if the new rule turns out to be a different attempt.
- It does not offer to re-cut anything, ask what Marek attempts, or write
  anything.

FAIL if it proposes edits to either file, starts an interview, or answers by
restating both files' contents instead of the distinction asked for.
