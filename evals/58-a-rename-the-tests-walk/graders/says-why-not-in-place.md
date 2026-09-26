---
type: llm
focus: full_transcript
weight: 1
---
The session explains why the rename cannot simply be done, in terms of what
names the id.

PASS requires all of:

- It says a workflow id is named from outside the file — the walkthrough test
  walks it, and the features and any journey point at it — so renaming in
  place breaks them, and a spec commit that leaves the gate red is not a spec
  commit.
- It says what happens instead: the old id stays live, the new one lands
  `@planned`, and the change that implements it carries the rename across the
  tests. Naming this as two changes is the form asked for.
- It does not edit the walkthrough test. Tests are not this skill's to move,
  and the sitting says so rather than quietly leaving them alone.

FAIL if the rename is performed in place, if the new id is landed live with
nothing walking it, if the tests are edited, or if the reason given is only
that renaming is risky in general.
