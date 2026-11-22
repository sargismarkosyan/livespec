# Spec 0112: graded cases from their principles

- **Status:** approved — by the maintainer in advance, 2026-11-22 (*"Carry on."*, then *"yes"* to continuing page by page), as the next change under #195; implemented end to end, reviewed at the pull request
- **Issue:** [#195](https://github.com/sargismarkosyan/livespec/issues/195), the fourth change under it, after [0111](0111-testing-from-its-principles.md)
- **Sketch:** skipped — approval was given in advance, so there was no decision left for one to support.

## Who this is for

**Ren — [`agent-accelerated-owner`](../personas/agent-accelerated-owner.md)**, when
the product is judgment and its proof is a graded suite.
**The workflow is [`adopt-the-process`](../workflows/adopt-the-process.feature).**
Nothing about who this is for moves.

## The job behind the request

The same as [0109](0109-the-process-from-its-principles.md), for
`method/graded-cases.md`.

## Why now

The page is 225 lines, and its introduction says each section *"is a lesson that
cost somebody an afternoon"*. Most of the length is the afternoon, and the
lesson stands without it.

## The end value

The same rules in fewer words. **How we would know it worked:** the harvest
accounts for every section, the one linked anchor resolves, and the page is
shorter.

## What changes

1. **[`method/graded-cases.md`](../../method/graded-cases.md)** is rewritten from
   the principles, 225 → 134 lines. *Neither freshness nor the score is gated*
   keeps its anchor.
2. **The `method/` ceiling** is lowered to the size this change leaves.

No rule, workflow or skill moves. No Gherkin moves.

### The harvest

| Section | Kept, every one |
|---|---|
| Introduction | the fork from `testing.md`; nothing names a runner, grader format or threshold |
| *The session* | hermetic sessions; a case builds its repository for every arm; a case of something that asks brings the person, answering only when asked; lent tools named, confined, required or refused |
| *One arm* | two arms, same prompt and graders; the difference is the only number; a negative is a real finding |
| *Firing* | reported, never scored, and why it would inflate the difference |
| *The judge* | a separate model, a fixed reply shape, and both reasons; a grader that reads the answer in every case; read the transcript before touching rubric or verdict; the model under test as judge, bounded by the arms |
| *Neither freshness nor the score* | the fingerprint; stale shown, not counted; neither gated, and why; re-run what changed; the run never automatic, approved per run; a stale number is not a licence to spend |
| *Two speeds* | the cheap tier's three kinds, each fingerprinted by what it sees; the faithful tier and when; the cheap tier earns trust, and its blind spots are marked not applying; sessions already had: graded, local, never on the board |
| *Evidence* | evidence local, summary committed, and its fields; why both |
| *Below the floor* | the repository picks a floor; a measurement keeps its row; the summary says its runs; a below-floor number kept, shown, not counted or averaged, never over a measurement |
| *Not settled* | what a difference means; a direction, more runs, read the verdicts; writing down what is not known |

## What this removes

- **The introduction's framing of every section as a lesson that cost somebody
  an afternoon,** and the afternoons themselves: *the first day is spent fixing
  something that was never broken*, *it is the most natural mistake to make and
  the hardest to see afterwards*.
- **"Deleting it would only put the row back to empty"** and *a board that cannot
  tell the two apart publishes its own variance*. The rule they argued for stays.
- **91 lines of `method/graded-cases.md`.**

## What we are not doing

The other method files: one change each, under #195. No rule changes.

## Data

None.

## Risks

A rule loses force without its reason. The reasons cut are listed above.

## Acceptance checks

1. Every row of the harvest can be found in the new page.
2. The linked anchor resolves; `verify.py` is green.
3. The `method/` ceiling is lowered to match.
