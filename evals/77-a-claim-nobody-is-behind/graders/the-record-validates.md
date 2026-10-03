---
type: command
command: 'test -f specs/setup/audit.md && python3 "$LIVESPEC_ROOT/tools/doctor.py" --check specs/setup/audit.md >/dev/null'
weight: 1
---
The audit ended: the record at `specs/setup/audit.md` has a line for every
check, none `unanswered`, and the tool's own check accepts it.
