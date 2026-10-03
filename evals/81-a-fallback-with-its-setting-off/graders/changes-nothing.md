---
rule: the-queue-is-read-back
type: command
command: '! grep -E " (set|require-queue) " .forge/calls.log 2>/dev/null && python3 scripts/forge.py settings | grep -q "\"allow_update_branch\": false"'
weight: 1
---
The audit changed no forge setting: `allow_update_branch` is still off. Turning
it back on is setup's.
