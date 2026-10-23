---
rule: the-loop-reads-back-what-a-pull-request-closes
type: command
command: 'test ! -e CLAUDE.md && grep -q "mr closes" AGENTS.md && ! grep -qiE "(clos|fix|resolv)[a-z]*:? +\[#" AGENTS.md'
weight: 1
---
AGENTS.md is still the only instructions file; its loop reads back with
`mr closes`, and no longer tells a session to put the keyword in front of a
Markdown link.
