---
tags: [should-not-fire]
max_turns: 10
timeout_seconds: 180
allowed_tools: [Skill, Read, Glob, Grep]
runs: 3
workspace: empty — a request for a commit message; nothing should fire and nothing needs reading
---
Write me a commit message for a change that adds pagination to the task list.
Subject line plus a short body.
