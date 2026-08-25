# The arc

| Journey | Whose | What it covers |
|---|---|---|
| [`trusting-the-spec-again`](trusting-the-spec-again.md) | [`agent-accelerated-owner`](../personas/agent-accelerated-owner.md) | a spec that had gone quietly wrong, through the gates going in, to a return days later that is acted on without being checked |

One file per journey, `@journey:<id>` on the first line, prose and tables and
never Gherkin, and the structure is in [the template](../../templates/journey.md).
A journey points at nothing: the workflow files say which arc they sit in.

## What the arc is here

Adoption over time, not a session. It runs from *before* it is installed — the
repository where the spec has already drifted and nobody trusts it — through the
changes that follow, to the return where the specs are either still true or have
quietly stopped being read.

## Two things this section asserted before anybody had lived the arc

Corrected here rather than deleted. Being wrong in a recorded way is most of the
reason for writing a guess down at all.

- It said the span was **months**. The one arc anybody has lived runs over days
  and weeks and contains no dormancy at all: the spec moves with every change, so
  there is never a coming-back-to-it. The months-long shape may well exist —
  nobody has reached it.
- It said **the trough is the first time the gate blocks something somebody
  wanted to merge**, and that the install goes fine. For the one person observed
  it is neither. A gate blocking is not a low point for somebody whose response
  is to fix the pipeline. The trough is *before the product*: a spec still being
  trusted some time after it stopped being true.

**Both corrections come from one person, and the second is the one most likely to
be wrong for somebody else** — the person observed also wrote the gates, and
being blocked by your own gate is not the same experience as being blocked by
one you inherited. Observed for this persona; untested for anybody else.

**Current state only.** An arc where every phase goes well is a wish, and this
repository has a whole eval case holding that line.
