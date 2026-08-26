---
tags: [skill:setup, rule:the-bindings-say-what-a-change-here-must-show]
max_turns: 25
timeout_seconds: 660
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit]
runs: 3
---
Half of this is done already — the traceability gate is wired and `npm run
verify` runs it. What's missing is the file the skills are supposed to read:
there's no specs/setup/README.md. Write it, and go ahead and write files.
