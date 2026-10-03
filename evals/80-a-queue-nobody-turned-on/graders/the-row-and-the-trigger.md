---
rule: several-merges-go-through-a-queue-or-its-fallback
type: command
command: 'python3 scripts/forge.py protection | grep -q "\"merge_queue\": true" && grep -q "merge_group" .github/workflows/checks.yml && grep -iE "^\| \*\*Several merges at once\*\* \|" specs/setup/README.md >/dev/null'
weight: 1
---
The queue is required on the forge, the workflow runs on the queue's event,
and the bindings carry the row.
