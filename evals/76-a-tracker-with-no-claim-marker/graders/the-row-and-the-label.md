---
rule: the-claim-marker-is-bound
type: command
command: 'grep -iE "^\| \*\*Claiming an issue\*\* \|.*\`in-progress\`" specs/setup/README.md >/dev/null && python3 scripts/tracker.py labels | grep -q "^in-progress "'
weight: 1
---
The bindings carry the *Claiming an issue* row naming `in-progress`, and the
tracker has the label.
