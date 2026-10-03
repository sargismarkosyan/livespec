---
type: command
command: 'python3 "$LIVESPEC_ROOT/evals/58-a-rename-the-tests-walk/check_rename.py"'
weight: 1
---
The tree left behind carries the rename the only way it can land in a spec
change: the old id still live and still walked by its test, the new id present
and marked `@planned` for the implementing change to pick up, the tests
untouched, and the traceability check green. The script names whichever of
those is missing — including the two tempting wrong answers, renaming in
place and landing the new id live with nothing walking it.
