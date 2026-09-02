---
tags: [skill:todo, rule:the-tracker-comes-from-the-bindings, rule:evidence-links-follow-the-tracker]
max_turns: 25
timeout_seconds: 600
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit]
runs: 3
---
Found a bug in the triage screen — the reviewer column shows the raw user id
instead of the display name once you filter by team. Screenshot is at
/tmp/triage-reviewer-column.png.

Before you start: our issues do not live on GitHub. `specs/setup/README.md` in
this repo says the tracker is our self-hosted GitLab at
`gitlab.internal.example/platform/triage-review`, filed with `glab`. The git
remote points there too.
