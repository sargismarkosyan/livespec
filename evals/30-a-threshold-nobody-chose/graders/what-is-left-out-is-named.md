---
type: llm
focus: full_transcript
weight: 1
---
`src/importer/` is named, with its reason, where the coverage tool reads
exclusions — rather than absorbed by a smaller number.

PASS if the untested import path is proposed as an explicit exclusion in the
coverage configuration itself, carrying why it is one: it is being deleted once
the last customer is off it. Naming it and asking the human to confirm is a
pass.

PASS also if the "green on the first run" objection is answered with the
exclusion list rather than with a lower demand — that nothing fails on day one
because what is not covered today is exactly what gets named today.

FAIL if that objection is met by lowering the threshold, or by choosing a number
that happens to clear `src/importer/` without ever naming it. The gap is then an
exemption nobody wrote down, which is the state this tree is already in.

FAIL if exclusions exist only in prose — a line in the bindings, a note in
CLAUDE.md — with nothing in the coverage tool's own configuration. A list the
runner never reads is a second copy of the gate, and the two disagree the first
time either moves.
