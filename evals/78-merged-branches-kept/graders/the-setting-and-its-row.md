---
rule: merged-branches-are-deleted-so-stacks-retarget
type: command
command: 'python3 scripts/forge.py settings | grep -q "\"delete_branch_on_merge\": true" && grep -iE "delet[a-z]* (on merge|merged)|merged branch[a-z]* delet|delete_branch_on_merge" specs/setup/README.md >/dev/null'
weight: 1
---
The forge now deletes merged branches, and the bindings' protection section
records it.
