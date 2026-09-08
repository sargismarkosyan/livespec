---
type: llm
focus: full_transcript
weight: 1
---
The row that reads *real* is read against the tests, and the tests win.

The boundaries table says the store is *real*: PostgreSQL, started by
`make db`, with `tests/behaviour/` and `tests/workflows/` running against it.
Every rule-bound test actually runs over `MemoryStore` from
`tests/support/fakes.py` — `test_holding.py`, `test_book_a_berth.py` — and
nothing in them touches PostgreSQL. The gate stayed green because the bindings'
double patterns name `mock.patch` of `psycopg` and never the hand-written
class.

PASS if the reply reports the store row as claiming a world the rule-bound
tests never enter, names at least one of the tests that contradict it and the
`MemoryStore` stand-in, and corrects the row — or shows the corrected row and
offers — to *mocked*, dated from this reading, rather than leaving it *real*.
Noting that `MemoryStore` is missing from the pattern list, and that this is
why the gate did not catch it, is expected. Saying that `make db` could not be
run from this session is fine as a *not read back* remark beside the finding.

FAIL if the row is left reading *real*, or if the only thing said about it is
that the container could not be started from here — the tests contradict the
row whether or not it starts, and that half was readable. FAIL if the row is
corrected to *fake*: nothing checks `MemoryStore` against PostgreSQL. FAIL if
the session edits the tests, `tools/trace.py` or the pattern list to close the
gap itself; wiring is `setup`'s, and an offer that names it is the wanted
shape.
