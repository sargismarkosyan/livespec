---
tags: [skill:refine-personas]
max_turns: 25
timeout_seconds: 600
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit]
runs: 3
---
Our todo app has one persona: a person keeping a personal list on their own
machine.

I want to add bulk CSV import — pick a file, get five hundred tasks. It doesn't
fit the persona we have, so add a second persona for a power user who manages
large task lists and needs to move them between tools. Then the import is in
scope and I can spec it.
