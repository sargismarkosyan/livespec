---
tags: [skill:setup, workflow:adopt-the-process, rule:setup-continues-into-the-layers, rule:setup-finds-where-issues-go, rule:setup-audits-an-existing-claude-md, rule:setup-wires-the-pull-request-report, rule:the-report-cannot-fail-the-build, rule:the-report-says-what-moved]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit]
runs: 3
---
Set the livespec process up in this repository, and go ahead and write things —
you do not need to check back with me before each file.

Two things about this repo before you start. There is already a CLAUDE.md at the
root; it has been there about a year and says what the service does, how to run
the test suite locally, and the branch naming convention, and nothing else. And
our issues are not on GitHub — the team works out of a self-hosted GitLab, and
`CONTRIBUTING.md` says so in one line near the bottom.
