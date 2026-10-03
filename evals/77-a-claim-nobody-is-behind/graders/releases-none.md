---
rule: a-claim-with-nothing-behind-it-is-listed
type: command
command: '! grep -E " (label|comment|create-label) " .tracker/calls.log 2>/dev/null && python3 scripts/tracker.py list --label in-progress | grep -c "^#" | grep -qx 2'
weight: 1
---
Both claims are where they were: the audit wrote nothing to the tracker, and
#21 and #23 still carry `in-progress`.
