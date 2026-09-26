# Spec 0071: one judge call per session, not one per rubric

- **Status:** approved
- **Issue:** none — the maintainer, on being handed the bill

## Who this is for

The maintainer paying for the suite. The measuring apparatus again, and it
says so.

## The job behind the request

A judge call's cost is almost all input, and the input is almost all the
session. `12-setup-drives-the-sitting` carries nine llm rubrics; grading it
sends that sitting's digest to the judge **nine times** and asks one question
of each copy.

The rubrics are independent judgments about the same evidence. There is no
reason the evidence has to travel nine times.

## Why now

Measured across the suite: **131 llm graders over 70 cases**. Grouped by the
evidence they read — `focus`, which decides whether a rubric sees the last
message or the whole digest — they need **75 calls instead of 131**, which is
**43% fewer**, and far more than 43% fewer tokens because the cases with the
most rubrics are the ones with the longest sittings.

The judge was 41–47% of the bill in the last two runs.

## The end value

The same verdicts for roughly half the judge's money, and the saving is
largest exactly where the suite is most expensive.

**How we would know it worked:** the run's ledger shows `batch:<n>` entries in
place of runs of single-grader entries, and the judge's share of a run's cost
falls.

## What changes

- `asserts.judge_many()` takes every llm grader a session still owes, groups
  them by `focus`, and for each group of two or more asks one call carrying
  the evidence once and the rubrics numbered after it. It returns a verdict
  per grader.
- The judge is told plainly that each rubric is judged on its own and that no
  rubric's verdict may influence another's.
- **A rubric the batch does not return is asked for on its own.** A batch that
  comes back short, malformed, or not at all returns nothing for that group,
  and every rubric in it goes down the existing one-call path. Nothing about
  accuracy depends on the batch succeeding.
- `run.py` asks for the batch once per session, over the graders still owed,
  so a resume judges what it owes and not what it already has.
- A group of one is left alone: one rubric is already one call.

## What we are not doing

- **Not batching across sessions or arms.** The evidence would differ, which
  is the whole reason a group shares a call.
- **Not batching graders that read different evidence.** A rubric on the last
  message and one on the whole digest cannot share an input.
- **Not touching the single-call path.** It stays exactly as it was, because
  it is the fallback and the thing every batched verdict is compared against.

## Data

The ledger gains `batch:<n>` as a grader name. `judge_costs()` sums by case
and is unaffected.

## Risks

**A judge asked nine questions at once may answer each less carefully than a
judge asked one.** That is a real risk to the numbers rather than to the bill,
and it cannot be argued away from here — it has to be read. The first run
after this lands is a calibration read like any other: the verdicts are read
against what a single-call judge said on the same cases, and if the reasons
get thinner the grouping is wrong and this is reverted.

The mitigation in the design is that the fallback is total: nothing is lost by
turning batching off, because the one-call path never changed.

## Acceptance checks

1. A run over a case with several llm rubrics of one focus writes one
   `batch:<n>` line to `judge.jsonl` in place of several single lines.
2. A case with one llm rubric is unchanged.
3. A malformed or short batch reply leaves every rubric in that group judged
   singly, with its ordinary verdict.
4. `python3 .github/scripts/verify.py` is green but for the board.
