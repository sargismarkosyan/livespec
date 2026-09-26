---
type: llm
focus: full_transcript
weight: 1
---
The session declines to write the workflow, and places the promise where it
belongs instead.

PASS requires all of:

- It says why this is not a workflow, using the definition: there is no
  trigger and no end state. The person sheet says so outright when asked —
  he never sits down to keep the log safe and would not know when he was
  finished — and the session either elicits that or reasons to it from the
  request.
- It says what it is instead: something that must always be true. It belongs
  in the product spec, where `specs/spec.md` already carries it as *it never
  loses a sighting*, and it is asserted inside ordinary features and inside
  every walkthrough rather than in a file of its own.
- It answers the follow-up about how anyone knows it is being checked, rather
  than leaving the person with a refusal and nothing: the return example that
  ends each workflow, a rule under an existing feature, or both.
- No workflow file for it is written.

FAIL if a `keeping-the-log-safe` workflow is created in any form, if the
refusal rests only on the workflow being vague, or if the person is left
without somewhere for the promise to live.
