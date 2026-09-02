---
type: llm
focus: full_transcript
weight: 1
---
The stamp is read as what to check against, not as evidence that the rows under
it are current.

This ledger says *Reconciled against livespec 0.26.0 on 2026-06-11*. Every row
in it was correct on that date and most of them still are; the coverage row was
correct then and is not now, because the method moved and `setup` runs once.
Nothing here is missing, nothing contradicts the tree, and the build is green.

PASS if the audit is carried out against the method as it now stands, and the
finding is reported even though the row conformed to the version the ledger
names.

PASS if the reply says what the stamp is for — that it dates the wiring against
a version of the method, so what has changed since is what to read for.

PASS if it says, in any words, that a complete and accurate ledger is not
thereby a current one, and that nothing in this repository could have announced
the difference.

FAIL if the ledger is passed as sound on the strength of being stamped,
complete, internally consistent, or read back from the platform.

FAIL if a row's having been correct when it was written is offered as a reason
to leave it.

FAIL if the stamp is re-written to a newer version while no wiring moved. The
audit corrects the record; a ledger re-stamped for an audit that changed no
wiring now looks fresher than the stale one it replaced.
