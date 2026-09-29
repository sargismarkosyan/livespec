---
rule: a-fresh-tree-is-re-proven
type: command
command: 'test "$(git worktree list | wc -l)" -eq 1'
weight: 1
---
The audit cleans the throwaway it made, leaving git's list of trees as it was.
Only the main checkout remains.
