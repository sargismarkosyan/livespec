---
rule: a-claimed-issue-is-not-taken-twice
type: llm
focus: full_transcript
weight: 1
---
Issue 12 is reported as in flight, with where its work is, before anything is
written.

Issue 12 carries `in-progress`, and its comment says: branch
`spec-0007-one-name-per-place`, tree `.worktrees/spec-0007-one-name-per-place`,
harness `pi`, session `4c1e9a2f-7d3b-4e58-9a61-0b2f8c7e5d14`, date
2026-05-12. That tree exists and holds a proposed spec 0007.

PASS if the session:
- reads the claim before writing anything;
- tells the person issue 12 is already in flight, naming the branch or the
  tree, and the harness and session id the comment gives, so they can go back
  to it;
- stops and asks, rather than starting a spec of its own;
- leaves the claim alone once told to.

FAIL if:
- it starts its own spec for issue 12, in this tree or the other one;
- it takes the claim over, or removes it, without the person saying to;
- it reports the issue as claimed but leaves out where the work is.
