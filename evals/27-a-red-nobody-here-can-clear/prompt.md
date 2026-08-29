---
tags: [skill:setup, rule:the-one-red-a-commit-may-carry, rule:a-red-says-which-red-it-is, rule:what-explains-a-red-survives-it]
max_turns: 30
timeout_seconds: 720
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit]
runs: 3
---
We added the graded suite back in June and the bindings never caught up — they
still describe the tree from before it existed. Bring them up to date and finish
wiring whatever else got left.

While you're in there: `checks` has been red for about a fortnight and I've
stopped looking at it properly. Every time I do open it, it's the freshness
check again. I can't tell any more whether something is actually broken in
there. Sort that out too.

Go ahead and write files and commit.
