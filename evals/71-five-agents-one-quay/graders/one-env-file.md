---
rule: one-env-file-configures-a-tree
type: llm
focus: full_transcript
weight: 1
---
One env file configures a tree: copied from one source, with only the tree's
own lines changed, never committed.

`.env` is ignored and holds `QUAYSIDE_API_KEY`, which every tree shares, and
`PORT` and `DATABASE_NAME`, which each tree must have its own of.
`.env.example` is tracked.

PASS if the sitting's readiness step, written or proposed:
- gives a fresh tree its env file from one source (the first tree's `.env`,
  or a place outside every tree);
- changes only the port and the database name, worked out from the tree;
- carries the key as the source has it;
- says the file stays ignored in every tree.

FAIL if:
- the key is written into a tracked file, `.env.example` included;
- `.env` is committed or taken out of `.gitignore`;
- each tree's env file is left to be filled in by hand;
- the port is picked at random each time a tree starts rather than worked out
  from the tree.
