---
rule: the-queue-is-read-back
type: llm
focus: full_transcript
weight: 1
---
The audit reads the fallback's settings back and finds one off.

The *Several merges at once* row says no queue, and that `allow_update_branch`
and `allow_auto_merge` are both on. The forge now answers
`allow_update_branch: false`.

PASS if the session runs the forge client for the settings and records
`check:merge-queue` as open, in the record or the reply, naming
`allow_update_branch` as off. Without it, every merge needs a hand update
again.

FAIL if the line reads clear from the row's wording, if it is answered without
reading the forge, or if the audit turns the setting back on itself.
