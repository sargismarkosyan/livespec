---
type: llm
focus: full_transcript
weight: 1
---
Where issues are filed in **this** repository was found and written down.

PASS if the GitLab tracker is what ends up recorded — in the CLAUDE.md that was
written, in the bindings, or both. The prompt says the team works out of a
self-hosted GitLab and that `CONTRIBUTING.md` names it; either reading it there
or taking it from the prompt is fine, and asking to confirm it is fine.

FAIL if what gets written says issues are GitHub Issues, or names `gh`, or
leaves the question blank — the assumption a skill makes when nothing went
looking. FAIL if the tracker is mentioned in conversation but appears nowhere in
what was written to disk: the point of the rule is that the next session reads
it without being told.
