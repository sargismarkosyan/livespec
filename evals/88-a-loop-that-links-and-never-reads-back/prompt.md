---
tags: [skill:setup, rule:the-loop-reads-back-what-a-pull-request-closes]
max_turns: 60
timeout_seconds: 1500
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]
runs: 3
---
Three merge requests merged last week and the issues they named stayed open.
Run the sitting for the context file — only the loop's step that opens a merge
request; the rest of the file and the wiring are fine.
