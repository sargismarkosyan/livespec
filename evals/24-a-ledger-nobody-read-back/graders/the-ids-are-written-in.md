---
rule: old-rows-are-matched-by-alias
type: llm
focus: full_transcript
weight: 1
---
The ledger predates ids, and the audit matches its rows by their labels and
writes the ids in — without moving the columns.

Each row in the gate wiring table that matched one id gains that id (a
`gate:` or `wiring:` id from the method's list) as a correction to the record.
A row that could be two ids is reported with both and left as it was. The
tables keep the shape they were typed in — the reshaping is named as the
sitting's, and the reply ends with the command that starts it.

Fails if the audit invents ids the method does not have, rewrites the tables
into a new shape itself, or reports the old shape without writing any id in.
