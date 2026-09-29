---
rule: a-fresh-tree-is-watched-going-green
type: command
command: 'test "$(git worktree list | wc -l)" -eq 1'
weight: 1
---
The throwaway tree is cleaned by the command, leaving git's list of trees as
it was. Only the main checkout remains. A proof that leaves its tree behind
has added one more tree nobody can tell apart from the ones holding work.
