---
rule: the-sitting-names-the-context-file
type: command
command: 'test ! -e CLAUDE.md && test -f AGENTS.md && grep -iE "^\| \*\*Context file\*\* \|.*AGENTS\.md" specs/setup/README.md >/dev/null'
weight: 1
---
AGENTS.md is still the only instructions file, and the bindings name it as
the context file.
