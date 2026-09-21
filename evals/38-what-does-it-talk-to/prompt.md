---
tags: [skill:setup, rule:setup-asks-what-the-app-talks-to, rule:a-real-row-is-written-after-a-test-reached-it, rule:a-stand-in-nobody-chose-is-not-written-as-chosen]
max_turns: 100
timeout_seconds: 2400
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit]
runs: 3
---
Set the process up here and go ahead and write files — I'll stop you if I
disagree with something.

It's a small Python service, about a thousand lines. `make check` runs the
suite and it's green; CI runs the same thing. Nothing in `specs/` yet.
