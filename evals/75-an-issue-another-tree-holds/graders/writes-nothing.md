---
rule: a-claimed-issue-is-not-taken-twice
type: command
command: '! grep -E " (label|comment|create-label) " .tracker/calls.log 2>/dev/null && test -z "$(git status --porcelain -- specs)" && test -z "$(git -C .worktrees/spec-0007-one-name-per-place status --porcelain)"'
weight: 1
---
Nothing was written: no label or comment went to the tracker, nothing under
`specs/` changed in this tree, and the other tree's work is untouched.
