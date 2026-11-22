# Spec 0116: the gate says why

- **Status:** proposed — approved in direction by the maintainer, 2026-11-22 (*"Go ahead, if you feel you need my input, like my review, just to be safe, prepare a deck, I will review it."*); implemented on the branch and **held for the maintainer's review before merging**
- **Issue:** [#194](https://github.com/sargismarkosyan/livespec/issues/194), and the last page of [#195](https://github.com/sargismarkosyan/livespec/issues/195)
- **Sketch:** the review deck prepared for the maintainer stands in for it.

## Who this is for

**Ren — [`agent-accelerated-owner`](../personas/agent-accelerated-owner.md).**
Ren's agent breaks a rule and gets a red build. Today the build says *what*
failed; *why*, and what to do, are in a method page the agent was meant to have
read. Nothing about who this is for moves.

**The workflow is [`adopt-the-process`](../workflows/adopt-the-process.feature)**,
at *Putting it in*, where the sitting writes the gate, and at *The changes
after*, where it fails.

## The job behind the request

To learn a rule at the moment it is broken, from the thing that caught it,
instead of reading every rule up front on every change.
[#194](https://github.com/sargismarkosyan/livespec/issues/194): *"every session
pays to read rules a failing check could teach when it fires."*

## Why now

- `method/gates.md` is 556 lines, the last page under #195, and much of it is
  prose restating rows of its own failure tables.
- Its closing list of faults to inject is a third copy of the same rows.

## The end value

Each rule a gate enforces is written **once**, as a row: the failure and what it
means. The gate prints that row when it fires. The page keeps only what a gate
cannot say: why there are two gates, the ledger, the report, the boundaries'
states, what is not wiring.

**How we would know it worked:**
- A failing gate in a repository set up from here names the place, the reason
  and the fix.
- `gates.md` has no paragraph that restates a row.
- livespec's own gate already does this, and is made to for the four messages
  that did not.

## What changes

1. **[`method/gates.md`](../../method/gates.md)** is rewritten from the
   principles, 556 → 333 lines.
   - **A new section, *A failure says why*:** each enforced rule is one row; a
     failing gate prints where and the row's meaning; warnings follow the same
     shape and are kept scarce.
   - **Prose restating rows becomes rows:**
     - the warn-without-failing paragraph becomes a *Warning* table;
     - the boundary failures become a *Failure* table;
     - the coverage gate gets its row.
   - ***Both gates are verified to fire*** no longer lists the faults again:
     every row in a *Failure* or *Warning* table is a fault to inject.
   - **The ten linked anchors keep their headings.**
2. **[`setup`](../../skills/setup/SKILL.md) §4** gains one paragraph: every failure
   the gate prints says where and what it means, in the words of its row.
3. **A rule,** [`a-failure-prints-what-it-means`](../features/setup/the-gate-says-why.feature),
   claimed by a new grader on case 12, the full sitting that writes the gate.
4. **This repository.** Of `trace.py`'s 46 failure messages, four said only what
   failed — a dangling `@workflow:`, `@persona:` or `@journey:`. They now say
   what to do.
5. **The ceilings.**
   - `method/` is lowered to 1,588.
   - `skills/` is raised by 6 and `specs/features/` by 18, for the paragraph
     and the rule, with the reason beside the numbers.

**Rules added**, live since the implementing commit:

| Rule id | Feature file | New or changed |
|---|---|---|
| `a-failure-prints-what-it-means` | [`features/setup/the-gate-says-why.feature`](../features/setup/the-gate-says-why.feature) | new |

## What this removes

- **223 lines of `method/gates.md`:**
  - the fault list, a third copy of the tables;
  - the paragraphs restating rows;
  - the reasons around rules that stand without them: *one warning, not four*
    as a story; *this is the paragraph that used to describe an artefact in the
    third person*; *until now, refused by nothing*; the V8 example (a runtime is
    a binding).
- **Nothing a gate enforces.** Every failure and warning on the old page is a
  row on the new one.

## What we are not doing

- **Shipping one gate for every repository**
  ([#193](https://github.com/sargismarkosyan/livespec/issues/193)). Each
  repository still writes its own gate. This change asks that gate to print the
  method's words, which is what makes a shipped gate's messages easy to write
  later.
- **Gating the wording of a message.** Whether a message carries the meaning is
  a reading: case 12's grader and review read it. A script would check for words,
  not meaning.
- **Rewriting existing repositories' gates.** A repository set up before this
  gets the rule as a new reading, through the same upgrade path as any other
  method change.

## Data

None.

## Risks

- **A rule loses its explanation.** The row is the explanation now, printed when
  it matters. A reviewer reading the page before a change sees the tables.
- **A repository's gate prints the rule in other words.** Allowed, as long as
  the reason and the fix are both there; the grader says so.
- **Eval spend.** Case 12 gains a grader and `setup` changes, so their rows go
  stale. Measuring is optional.

## Acceptance checks

1. Every failure and warning on the old page is a row on the new one, and the
   ten linked anchors resolve.
2. `trace.py`: break a `@workflow:` tag — the message says what to do.
3. `verify.py` is green; the ceilings moved as above.
