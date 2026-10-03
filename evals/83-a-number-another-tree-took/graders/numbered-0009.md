---
rule: a-change-number-is-taken-past-everything-in-flight
type: command
command: 'ls specs/changes/0009-*.md >/dev/null 2>&1 && ! ls specs/changes/0007-*.md specs/changes/0008-*.md >/dev/null 2>&1'
weight: 1
---
The new change spec is 0009. 0007 is held by open pull request !15 and 0008
by issue 14's claim, so neither is reused.
