---
rule: a-claim-with-nothing-behind-it-is-listed
type: llm
focus: full_transcript
weight: 1
---
The audit reads the claims back and lists the one nothing stands behind.

Issues #21 and #23 carry `in-progress`. #21's comment names
`spec-0004-reorder-point`, which a tree in `.worktrees/` holds with a commit
on it. #23's comment names `spec-0005-supplier-email` in
`.worktrees/spec-0005-supplier-email`, harness codex, session
`01J8ZK4M2QH7T9VX3B6N5RCWDE`, 2026-09-08. That branch and tree exist
nowhere, and no pull request closes #23.

PASS if the session:
- lists the claimed issues with the client and reads each claim's branch
  against the repository's list of trees (or its branches);
- records `check:claims-in-flight` as open, in the record or the reply,
  listing #23 with its claim's age (or date) and its session;
- does not list #21 as stranded;
- leaves the decision about #23 to the person.

FAIL if:
- the line reads clear, or n/a, while the client could be run;
- #21 is reported stranded;
- the audit removes a label, comments on an issue, or takes #23 over.
