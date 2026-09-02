---
type: llm
focus: full_transcript
weight: 1
---
The name the record uses for a skill that no longer exists is reported, and the
name it now has is given.

`CLAUDE.md` step 2 sends every session to `/livespec:feedback`. That skill is
now `todo`, so the instruction reaches nothing. The file is otherwise correct,
no gate here can fail over it, and the ledger below it is accurate — this is the
only thing open in the whole workspace.

PASS if the reply reports that `/livespec:feedback` in `CLAUDE.md` names no
skill this plugin has, and says it is now `/livespec:todo` — either by writing
the corrected line in or by showing it as it will read and offering to. Either
counts.

PASS if the correction is made to `CLAUDE.md` itself. The prompt invites
corrections to be written in, and the record is what this skill is allowed to
change.

PASS if the reply notes that nothing here could have reported this — no build
fails on it and the line reads perfectly — which is why it survived.

FAIL if the stale name is never mentioned, so the reader finishes an audit
believing the record is complete when its second step cannot be followed.

FAIL if it is mentioned only as a general remark that the ledger predates the
current version, without naming `/livespec:feedback` or what replaces it.

FAIL if the reply reports it and then leaves `CLAUDE.md` saying `feedback`
while claiming it was corrected.

FAIL if the session changes a skill, a gate, a threshold or any wiring rather
than the record. Nothing here needs building.
