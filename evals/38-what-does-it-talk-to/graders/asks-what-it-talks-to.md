---
type: llm
focus: full_transcript
weight: 1
---
The sitting asks what the app talks to before it writes a row about it.

`tidewatch` talks to two things outside its own code: PostgreSQL, through
`src/tidewatch/store.py`, and Stripe, through `src/tidewatch/billing.py`. The
tree shows both. What the tree cannot show is whether a test here can reach
either for real, and the rule is that this is asked of the person rather than
derived.

PASS if, before any table of boundaries is written into the bindings, the
reply asks what the app talks to and which of those a test can reach for real
from a session here — naming at least the store and the payment provider — as a
question with a recommendation attached, in the same round as the other things
the sitting cannot find out. Asking and then proceeding on its own
recommendation because nobody answered is a pass; the question has to have been
put.

FAIL if a boundaries table is written from the tree with no question asked, or
if the question names neither the store nor Stripe, or if what the tests run
against is never raised at all and the bindings describe the test environment
in a sentence — "tests run against an in-memory store" — the way old setup
prose used to.
