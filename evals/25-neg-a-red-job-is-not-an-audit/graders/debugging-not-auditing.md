---
type: llm
focus: last_message
weight: 1
---
A red check is debugged, not audited.

One gate failed on one branch, with the reason printed: a rule that no test
claims. What is wanted is what broke and what to do about it.

PASS if the reply goes at that failure — the rule was added to a `.feature` and
no test claims it yet, so either the test is missing or the rule should be
tagged `@planned` — or asks to see the feature file and the tests. Saying what
it could not determine without the repository in front of it is a pass.

FAIL if a livespec skill is invoked to answer it.

FAIL if the answer turns into a review of the repository's process: walking the
gate wiring ledger, checking what the bindings claim, asking whether branch
protection is really enforced, listing what is unobserved. However accurate that
is, nobody asked for it and the person is still looking at a red check.

**This is the case that pays for `doctor`'s description being in context at
all.** That description says *check or audit the gates* and *whether the process
still holds here*; this prompt is a failing gate, phrased the way somebody
actually phrases one, and it is asking for none of that.
