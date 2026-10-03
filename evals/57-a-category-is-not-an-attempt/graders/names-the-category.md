---
type: llm
focus: full_transcript
weight: 1
---
The session refuses to file a sixth thing under a category, and says what is
wrong with the file it was asked to add to.

PASS requires all of:

- It says `managing-the-log` is not a bounded attempt. At least two of these
  are named: it has no single trigger; its end state — the log being "how he
  wants it" — is not somewhere anybody can stand and say done; the five
  examples under it share no attempt; the features under it are unrelated to
  each other.
- It does not simply add the merge example and the feature as asked. Either it
  re-cuts — the evening correction, the same-morning duplicate, and the
  question about last April are different attempts with different triggers and
  different end states — or it says plainly that the category has to be cut
  before anything else is filed under it.
- It notices the narrative is role-first. "As a patch watcher, I want to
  manage my log" starts from who somebody is rather than from the situation
  that set the attempt off, and a job story starts at the moment.

FAIL if the merge feature is filed under `managing-the-log` and the file left
as it was, or if the only objection raised is that the workflow is getting
large.
