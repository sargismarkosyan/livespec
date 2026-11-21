---
rule: a-release-note-only-where-one-is-published
type: command
command: 'python3 "$LIVESPEC_ROOT/evals/89-a-body-that-buries-its-point/check_body.py" release-note'
weight: 1
---
fieldnote's bindings name no changelog that is published from a pull request,
so `pr-body.md` carries no release note: no heading or line titled release
note or changelog.
