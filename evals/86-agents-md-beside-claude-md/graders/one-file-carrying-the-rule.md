---
rule: two-instructions-files-become-one
type: command
command: 'test -f AGENTS.md && test ! -e CLAUDE.md && grep -q "02:00" AGENTS.md && grep -iE "^\| \*\*Context file\*\* \|.*AGENTS\.md" specs/setup/README.md >/dev/null'
weight: 1
---
AGENTS.md is the one instructions file, it carries the rule only CLAUDE.md
knew, and the bindings name it as the context file.
