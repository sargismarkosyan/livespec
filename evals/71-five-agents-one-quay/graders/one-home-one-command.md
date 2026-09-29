---
rule: trees-have-one-home-and-one-command
type: llm
focus: full_transcript
weight: 1
---
Every tree gets one home and one command, and neither belongs to a harness.

The owner runs up to five agents at once, one worktree each, sometimes under
Pi and sometimes under Claude Code. Nothing in quayside says where a tree goes
or how one is made ready.

PASS if the sitting proposes, or writes into the bindings:
- one directory every tree lives in, ignored. It must not sit under a
  harness's own directory (`.claude/`, `.cursor/`, `.pi/`);
- one command that makes a tree, lists every tree with whether it is safe to
  remove, and cleans the safe ones. It is the repository's own, in its own
  language or its Makefile, and names no harness.

Offering the command and writing only the row is a pass. So is a row listing
the steps in order because the command was declined. A harness's own tree
mechanism pointed at the command is a pass.

FAIL if:
- trees are put under `.claude/worktrees/` or any harness's directory;
- the only answer is a harness feature (`.worktreeinclude`,
  `.cursor/worktrees.json`, `claude --worktree`);
- there is a way to make a tree but none to list or clean them;
- parallel work is not addressed at all despite the prompt raising it.
