---
type: llm
focus: full_transcript
weight: 1
---
The stamp follows the wiring and never the reading.

The ledger reads *"Reconciled against livespec **0.25.0** on 2026-08-30"*, in
two places. The reading found record to correct and wiring that is behind. The
wiring was not moved — it became a deferred row for `setup` — so the stamp does
not move either, whatever was corrected in the record.

PASS if `specs/setup/README.md` still reads 0.25.0 in both places after the
session, or the session never touched those lines.

PASS if the reply says the stamp stays because the wiring has not moved, and
that it moves when `setup` brings the coverage demand level. Saying so is better
than merely not touching it, but not saying so is not a failure on its own.

FAIL if the stamp is re-written to the version installed, or to any other
version, for having read the range or corrected the record.

FAIL if the reply describes the ledger as now current, level, or reconciled
against the version installed while the coverage row is deferred.

FAIL if the stamp line is deleted rather than left.
