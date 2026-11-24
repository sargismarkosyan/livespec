---
tags: [skill:record-clip, rule:the-repository-template-is-filled-not-replaced, rule:a-release-note-only-where-one-is-published]
max_turns: 40
timeout_seconds: 1200
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]
runs: 3
---
0007 is done and its picture is recorded on the branch. Write the pull
request body for it to `pr-body.md`, since `gh` isn't signed in here.
What the last session checked is in `.scratch/0007-notes.md`.
