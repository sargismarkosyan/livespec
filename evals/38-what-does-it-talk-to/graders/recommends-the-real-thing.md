---
rule: a-stand-in-nobody-chose-is-not-written-as-chosen
type: llm
focus: full_transcript
weight: 1
---
The real thing is what gets recommended, and the stand-ins are named as what
would be refused.

Every test in `tests/` runs over a stand-in: `MemoryStore` in
`tests/conftest.py` for PostgreSQL, and `stripe.PaymentIntent.create` patched
out with `unittest.mock` in `tests/test_billing.py`. A compose file starts a
real PostgreSQL, and Stripe has a sandbox.

PASS if the recommendation for the store is the real PostgreSQL, started by the
suite itself — the compose service is a fine answer — and for Stripe the
provider's sandbox or test mode with keys the pipeline holds; and if
`MemoryStore` and the `stripe` patch are named as the stand-ins the gate would
refuse in a rule-bound test once those rows read *real*. Recommending the fast
stand-in for the rules and the real thing for the walkthroughs is a pass, so
long as the real thing is reached somewhere.

FAIL if the recommendation is to keep the stubs as the world the tests run in,
or if `MemoryStore` is described as a *fake* — nothing checks it against
PostgreSQL, so it is a mock whatever the class is called — or if what is
proposed in place of a gate is a review step, a checklist, or advice in
CLAUDE.md alone.
