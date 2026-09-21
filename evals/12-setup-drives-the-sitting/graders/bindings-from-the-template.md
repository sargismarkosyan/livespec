---
rule: the-bindings-are-written-from-one-template
type: llm
focus: full_transcript
weight: 1
---
The bindings written are the plugin's template, filled — not a table invented
for this repository.

The file at `specs/setup/README.md` carries the stamp line in the template's
words (*Reconciled against livespec … on …*), and three ledger tables whose
first column is an id: every gate row reads `gate:<name>` from the method's own
list, the two wiring rows read `wiring:`, and each boundary row reads
`boundary:<name>` for a thing this repository talks to. No row carries an
invented `gate:` id, and a gate the method does not name — if the session added
one — carries `local:`.

Fails if the ledger has no id column, if any gate row's id is not one the
method lists, or if the tables were written in a shape of the session's own.
