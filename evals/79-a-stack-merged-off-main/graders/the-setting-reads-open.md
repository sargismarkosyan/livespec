---
rule: the-delete-on-merge-setting-is-read-back
type: llm
focus: full_transcript
weight: 1
---
The audit reads the delete-on-merge setting back and reports it open.

`python3 scripts/forge.py settings` answers `delete_branch_on_merge: false`.

PASS if the session runs the forge client for the setting and records
`check:merged-branch-deleted` as open, in the record or the reply, saying the
forge keeps merged branches, so a stacked pull request can merge into a
dead branch.

FAIL if the line reads clear or n/a, if it is answered without the setting
being read, or if the audit turns the setting on itself.
