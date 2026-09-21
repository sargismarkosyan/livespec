---
tags: [skill:setup, rule:a-file-out-of-line-is-offered-whole, rule:what-only-the-file-knows-survives-the-rewrite, rule:a-rewrite-lands-only-on-a-yes]
max_turns: 100
timeout_seconds: 2400
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit]
runs: 3
---
Set the process up here, and go ahead and write files as you go — you don't
need to check back with me before each one.

There's a CLAUDE.md at the root already. I put it together from a template
last spring and have added to it since. `make check` is green and CI runs the
same thing.
