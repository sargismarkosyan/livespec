---
tags: [skill:setup, rule:trees-have-one-home-and-one-command, rule:every-resource-is-own-or-shared, rule:one-env-file-configures-a-tree]
max_turns: 100
timeout_seconds: 2400
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit]
runs: 3
---
Set the process up here and go ahead and write files — I'll stop you if I
disagree with something.

It's a small Python web app. `make check` is green and CI runs it. I run
several agents on this repository at once, each in its own worktree, so
whatever you set up has to hold for that too.
