# Spec 0007: trusting the spec again

- **Status:** approved
- **Issue:** [#14](https://github.com/sargismarkosyan/livespec/issues/14)

## Who this is for

[`@persona:agent-accelerated-owner`](../personas/agent-accelerated-owner.md),
across the whole span rather than inside any one attempt. The arc is the one
[`adopt-the-process`](../workflows/adopt-the-process.feature) sits in, and this
is the change that lets that workflow say so.

**Provenance.** One interview, 2026-08-25, third leg of the `setup` chain: four
retrospective questions about the gaps rather than the sittings, plus the arc
observable in `../todo-change` — twenty-eight change specs across about three
days. Same n = 1 as [`0005`](0005-the-first-persona.md) and
[`0006`](0006-adopt-the-process.md), and here it bites hardest, because the one
person who has lived this arc is also the person who built the thing the arc is
about.

**One answer shaped the file more than the other three.** Asked whether there was
ever a point of nearly stopping, the answer was *"Nope"*. That is the answer this
skill is most at risk from — a journey where every phase goes well is what it
refuses — so the post-install dip in the map is not drawn from felt experience.
It is drawn from what actually happened and was filed:
[#10](https://github.com/sargismarkosyan/livespec/issues/10),
[#12](https://github.com/sargismarkosyan/livespec/issues/12),
[#6](https://github.com/sargismarkosyan/livespec/issues/6). The feeling row there
reads ▃ rather than ▁ for the same reason: a shallow dip is what the evidence
supports, and deepening it to make a better story would be the wish this layer
exists to keep out.

## The job behind the request

Knowing whether the thing that was installed is still working — not on the day it
went in, but three weeks and forty changes later, when nobody has looked. No
single attempt can answer that, because the question is about what happens
between them.

## Why now

The chain: [`0005`](0005-the-first-persona.md) gave the layer a person and
[`0006`](0006-adopt-the-process.md) gave it an attempt, and both left a marker
pointing here. `adopt-the-process` named no arc, which the gate reported as the
only warning in the run — deliberately left standing so that this change is what
clears it. And [#14](https://github.com/sargismarkosyan/livespec/issues/14) named
all three layers; this is the last of them.

## The end value

The layer that carries the seams exists, and the run has **no warnings in it for
the first time**.

The concrete return is three rows reading *nothing yet* — the first findings this
repository has produced from somebody's experience rather than from its own
introspection. Two of them are the same moment: coming back cold and believing
what you read. That moment is the entire claim of the product and nothing
currently reaches it.

**How we would know it worked:** the next change that argues about scope cites a
seam from this file rather than an opinion — and the first time a proposed change
is turned down because it serves no phase of this arc, the layer has paid for
itself.

## What changes

- `specs/journeys/trusting-the-spec-again.md` — new. Lens, five phases in time
  order with a moving feeling curve, four seams, an ownership table with three
  *nothing yet* rows, and what the file does not know.
- `specs/workflows/adopt-the-process.feature` — gains `@journey:` on its first
  line. **The dependency runs that way on purpose**: the attempt knows which arc
  it belongs to; the arc cannot know what will be built inside it.
- `specs/journeys/README.md` — the layer stops saying *Empty*, and **two claims
  it made before anybody had lived the arc are corrected rather than deleted.**

**The two corrections**, because they are the finding and not an edit:

| It said | The one lived arc says |
|---|---|
| the span is **months** | days and weeks, with no dormancy — the spec moves with every change, so there is never a coming-back-to-it |
| the trough is **the first time a gate blocks a merge**, and the install goes fine | neither. A gate blocking is not a low for somebody who fixes the pipeline. The trough is *before the product* — a stale spec still being trusted |

The second correction is flagged in place as the one most likely to be wrong for
anybody else: being blocked by a gate you wrote is not the experience of being
blocked by one you inherited.

**Rules added or changed:** none, and not owed. Nothing in this layer is
asserted — a checkable sentence would belong in the workflow instead.

**Ledger:** nothing to move. `journey → workflow` reads *automated* and
`workflow → journey` reads *automated, as a warning*, both wired at 0.6.0 and
proven by faults in `inject.py`.

## What we are not doing

- **Not writing a second journey.** One per change, and there is one attempt to
  sit in an arc so far.
- **Not turning the seams into specs.** A seam is not a defect — nobody is at
  fault in any of the four — and two of them (*nothing says whether the install
  took*, *a workaround has no expiry*) are candidates for issues on their own
  terms, filed by the person who owns the tracker rather than folded in here.
- **Not building the check that is deliberately missing.** Whether a journey has
  been looked at since the attempts under it moved is a git question, and
  [`gates.md`](../../method/gates.md) leaves it out because CI checks out one
  commit and would answer it with silence forever. `refine-journeys` is explicit:
  never invent a gate for prose. Doing it by hand is the job.
- **Not deleting the two wrong claims.** A guess that was recorded and then found
  wrong is worth more than a clean page.

## Data

`@journey:trusting-the-spec-again` is permanent —
`ids-are-permanent` in [spec.md](../spec.md#the-promises-that-belong-to-no-single-workflow).
A journey id is named in every workflow that sits in the arc, so renaming it
breaks the layer above rather than the layer below.

## Risks

- **This skill's own refusal is the risk.** Four of five phases go well and the
  person says they never nearly stopped. That is what a brochure looks like from
  the outside, and the only defences are that the trough is real and sits before
  the product, the dip is evidenced by filed issues rather than felt, and the
  ownership table names three moments the product does not reach.
- **n = 1, and the 1 built the gates.** Every previous spec in this chain carries
  this; here it is load-bearing, because the corrected trough claim is precisely
  the one that would differ for somebody who inherited the process.
- **The span may be an artifact of the observer.** Days-and-weeks with no
  dormancy is what somebody in the loop many times a day would see. Whoever is in
  it monthly may find the dormancy phase this file says does not exist.
- **A journey rots silently and nothing reports it.** The workflows under this
  one will move, the gate will stay green, and this prose will go on describing
  something that changed. That is the layer's standing condition rather than this
  change's fault, and the mitigation is a person re-reading it, which is what
  `refine-journeys` is for.

## Acceptance checks

1. `python3 .github/scripts/verify.py` is green **with no warnings at all** —
   the first run in this repository's history where that is true.
2. `specs/journeys/trusting-the-spec-again.md` names no workflow, no rule id and
   no tag anywhere in its prose. Read it once looking only for that.
3. The feeling row moves across all five phases. A flat row means the arc is
   wrong or nobody was asked.
4. Read the map's *Before* column and check it is the repository as it actually
   was — a spec with no gate, going stale while still being trusted — rather than
   the absence of a spec.
5. Read the four seams and confirm nobody is at fault in any of them. Any seam
   with a culprit is a defect and belongs in the tracker instead.
