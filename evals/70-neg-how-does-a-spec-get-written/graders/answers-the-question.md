---
type: llm
focus: last_message
weight: 1
---
The reply explains the two layers from the repository's own files, and starts
nothing.

PASS requires all of:

- It distinguishes them: a change spec under `specs/changes/` is numbered
  because it is one step in a sequence, and it carries who the change is for,
  the job behind it and what is deliberately left out — the reasoning that
  will not survive in a diff. A feature file under `specs/features/` carries
  the rules themselves, each with a permanent id and its examples, and it is
  what tests point at.
- It answers the ordering: the Gherkin is written before the code, tagged
  `@planned` until the change that builds it drops the tag.
- It does not start refining anything, ask what the reader wants built, or
  write a file.

FAIL if it begins a spec, proposes a change, or answers by summarising what
fieldnote does instead of the relationship asked about.
