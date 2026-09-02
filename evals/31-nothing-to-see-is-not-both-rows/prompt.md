---
tags: [skill:setup, rule:the-bindings-say-a-sketch-is-owed-here]
max_turns: 25
timeout_seconds: 660
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit]
runs: 3
---
The traceability gate is wired already and `make verify` runs it. What is
missing is the file the skills are supposed to read — there is no
specs/setup/README.md. Write it.

Worth knowing before you do: there is no interface in this thing anywhere. It is
a daemon. Everything it does is a log line and an exit code, and nobody has ever
opened it on a screen. Go ahead and write files.
