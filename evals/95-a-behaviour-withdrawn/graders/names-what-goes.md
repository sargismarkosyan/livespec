---
rule: a-spec-names-what-it-removes
type: command
command: 'python3 "$LIVESPEC_ROOT/evals/95-a-behaviour-withdrawn/check_removes.py"'
weight: 1
---
The change spec says what it removes, and names each thing: the rule
`place-carries-from-the-last-sighting`, the test that claims it, and the
`where` field the code writes and renders. The traceability check is green.
