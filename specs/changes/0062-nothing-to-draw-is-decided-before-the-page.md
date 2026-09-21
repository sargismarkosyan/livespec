# Spec 0062: nothing to draw is decided before the page

- **Status:** approved — built on the maintainer's *merge all of them and carry on*, 2026-09-21
- **Issue:** [#150](https://github.com/sargismarkosyan/livespec/issues/150) —
  `refine-spec` drew a page for a rename, twice in three plugin sessions of
  `29-nowhere-to-draw-it` at the floor (`evals/results/20260921-015658`,
  `claude-sonnet-5`), where its own paragraph says to draw nothing.
- **Depends on:** [`0058`](0058-a-case-is-a-sitting-not-a-turn.md) and
  [`0059`](0059-a-run-the-limit-stops-is-resumed-not-repeated.md), the harness
  and the sitting that measured the case at the floor for the first time.

## Who this is for

[`agent-accelerated-owner`](../personas/agent-accelerated-owner.md), in
[`adopt-the-process`](../workflows/adopt-the-process.feature), at step 4 —
deciding on a spec they cannot check by reading, holding the sketch drawn from
it. For a change that picks one name out of three, the sketch they were handed
was a styled page titled *One name for the grace period*, carrying the three
names and the one chosen. Everything on it fits in the sentence that says so.
A page for that is not evidence; it is the padding the skill names as the
failure this step exists to prevent, and a reader who opens it learns to stop
opening them.

**This lengthens nothing anybody types.** No always-promise moves; the
description does not move.

## The job behind the request

The subsection *And draw the sketch, before approval is asked for* opens with
the instruction to make a page — *so make one page carrying the evidence* —
then gives the two ways to make one and the four things it carries. The
sentence that says when not to — *where there is nothing the prose cannot
carry — a renamed constant, a corrected path — say so and draw nothing* — is
the seventh paragraph, under *Two absences*, after a session that read the
heading as the instruction has reached for the second way and written the
file. Two of three did exactly that; the third said in a line that nothing
was drawn. The rule `29` claims, `an-absent-sketch-is-said-rather-than-filled`,
read 1 of 3.

The job: **whether there is anything to draw is decided first, from the four
things a sketch carries, and a page is made only when the prose cannot carry
them.**

## What changes

1. **[`skills/refine-spec/SKILL.md`](../../skills/refine-spec/SKILL.md)**:
   the heading gains its other half — *or say in a line that there is nothing
   to draw* — and the subsection's second paragraph is the decision: a sketch
   carries four things, and where every one of them fits in a line of prose —
   a renamed constant, a corrected path, one name chosen out of three — the
   hand-back says so in that line and no page is made; only when the prose
   cannot carry the evidence is a page made. *Two absences* keeps the second
   absence and points at the first as already decided.

**Rules changed: none.** The rule `29` claims already says it. `skills/`
moves: **`patch`**; the description does not move.

## What we are not doing

- **Not changing what a sketch carries or how it is published.** The four
  things and the two ways stand.
- **Not re-measuring here**; `29` re-stales through the skill body and is in
  the next sitting's first part.

## Data

Files that move: `skills/refine-spec/SKILL.md`, and this spec. The
implementing change stales the refine-spec cases through the skill body.

## Acceptance checks

1. The subsection reads as above; `verify.py` exits 2 for the board only.
2. `29`'s plugin arm at the floor says nothing is drawn, three of three, and
   `33` — where a page *is* owed — still writes one.
