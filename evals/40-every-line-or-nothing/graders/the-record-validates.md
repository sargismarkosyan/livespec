---
type: command
command: 'test -f specs/setup/audit.md && python3 "$LIVESPEC_ROOT/tools/doctor.py" --validate specs/setup/audit.md >/dev/null'
weight: 1
---
The audit ended: the record the session left at `specs/setup/audit.md` has
one line for every check, none `unanswered`, every state from the vocabulary,
and the tool's own `--validate` accepts it. A session that handed back with a
paragraph and no record, or with a record the tool refuses, has not finished.
