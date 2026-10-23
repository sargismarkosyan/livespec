# Spec 0084: a workflow names its phase

- **Status:** approved — by the maintainer in advance, 2026-10-23: implemented end to end, reviewed at the merge request
- **Issue:** [#120](https://github.com/sargismarkosyan/livespec/issues/120)
- **Sketch:** skipped — approval was given in advance, so there was no decision for one to support.

## Who this is for

**Ren — [`agent-accelerated-owner`](../personas/agent-accelerated-owner.md).**
They read the workflows, the journeys and the personas, and never the
documentation. The journey is the file they open to see where the product
stands in somebody's life. Nothing about who this is for moves.

**The workflow is [`adopt-the-process`](../workflows/adopt-the-process.feature).**
- The sitting fills the journey and workflow layers at *Putting it in*,
  step 6 of [`trusting-the-spec-again`](../journeys/trusting-the-spec-again.md).
- `refine-workflows` and `refine-journeys` run again at *The changes after*,
  step 8, whenever an attempt is added or re-cut.
- The gate the sitting wires runs on every change after that.

## The job behind the request

To look at a journey and see which attempts the product supports at each
phase, and which phases it does not reach. Today the journey is read in one
file and the workflows in another, and the join between them is in
somebody's head.

**What the request says** ([#120](https://github.com/sargismarkosyan/livespec/issues/120),
written in a hurry): journeys have stages, in order and sometimes looping;
a workflow may say which stage or stages it contributes to; it is optional;
it helps build a journey map.

**What it is read as:**
- A journey already has ordered stages: the columns of its map, which the
  template has called **phases** since the layer began. This change keeps
  *phase*, the word the template, `refine-journeys` and a live rule already
  use. Calling them *stages* too would be two words for one thing.
- What is missing is a way for a workflow to name one, a check that the name
  is real, and the generated map that follows from both.
- A loop is a fact about the arc. The template has no place to say it today,
  and a map read left to right says there is no loop.

## Why now

- **The workflow → journey link stops at the journey.** `@journey:` on a
  workflow says which arc. Where in the arc is written only in change specs'
  *Who this is for* sections, as prose: "at *The changes after*, step 8".
  Dozens of them say it, and nothing checks any of them.
- **The journey's *Ownership and metrics* table asks "what answers it
  today".** That is filled by hand, and a hand-kept list of what implements
  what has already drifted ([`gates.md`](../../method/gates.md#the-second-half-of-the-output-is-the-map)).
- **The one journey here goes round, and its map cannot say so.** Its span
  says it is "many short returns over days and weeks". The map reads as
  one pass from *Before* to *Coming back*.

## The end value

A workflow can say which phases of its journey it is made in, the gate
refuses one that names a phase the journey does not have, and the gate's map
lists each journey's phases in order with the attempts that sit in each. A
phase nothing sits in shows up as empty. A journey that goes round says
where, in one line.

**How we would know it worked:**
- Here: `trace.py` prints *trusting-the-spec-again* with
  `adopt-the-process` under *Putting it in* and *The changes after*, and
  *Before*, *Where it does not fit* and *Coming back* reading *(nothing
  names it)*.
- Rename a phase heading in the journey, and verification fails, naming the
  workflow and the phases that exist.
- In a consuming repository, `refine-workflows` writes `@phase:` on a new
  workflow where the journey has a phase the attempt is made in, and
  `refine-journeys` writes the loop line where the arc goes round.

## What changes

1. **The tag, `@phase:<name>`, on a workflow.** Optional, and it may repeat.
   - **The name is the phase's heading in the journey's map,** lower case,
     with every run of other characters as one hyphen: *Putting it in* is
     `putting-it-in`.
   - So the journey carries no id. Its prose stays free of tags, as the
     template has always asked.
   - It is looked up in the journeys the workflow's `@journey:` names.
     A workflow naming a phase and no journey has nowhere to look it up.

2. **A gate, `gate:workflow-to-phase`.**
   - **A workflow naming a phase that no journey it names has fails.** The
     message names the phases that do exist.
   - **A workflow naming no phase passes, silently.** It is not a warning:
     the tag is optional, and a warning nobody is meant to act on is
     wallpaper ([`gates.md`](../../method/gates.md#the-same-loop-one-layer-up),
     *One warning, not four*).
   - It is a row in [`gates.md`](../../method/gates.md#the-ids) with `since`
     reading `next`, in the failure table, the fault table and the id
     system, and in the [template ledger](../../templates/bindings.md) and
     `tools/doctor.py`'s registry.
   - `setup` wires it by reading the gate table, so it needs no new text.
     `doctor`'s `check:row-per-gate` reports the row missing in a ledger
     written before this, the way every new gate has arrived.

3. **The map, in [`gates.md`](../../method/gates.md#the-second-half-of-the-output-is-the-map).**
   It gains a second half: every journey, its phases in order, and under
   each the workflows that name it. A phase nothing names says so. A
   workflow naming the journey and no phase is listed apart, as not yet
   placed. Generated, never typed, like the rest of the map.

4. **The journey template, [`journey.md`](../../templates/journey.md).**
   - **The comment at the top:** the phase headings are names a workflow
     points at, so keep them short, and renaming one moves every workflow
     naming it.
   - **A paragraph under the map, *Where it goes round*:** where the arc
     goes back to an earlier phase, say so in one line under the table,
     naming both phases by their headings. A loop is a way between two
     phases, never a column of its own. A one-pass arc says nothing.

5. **The workflow template, [`workflow.feature`](../../templates/workflow.feature).**
   The first line gains an optional `@phase:<name>`, and a comment says
   what it names and that it may be left off.

6. **[`refine-workflows`](../../skills/refine-workflows/SKILL.md).**
   - **When writing the file, it names the phase or phases of the journey
     the attempt is made in,** read from the journey's map, where one
     plainly fits. Where none fits, it leaves the tag off and says so. It
     never adds or renames a phase: that is the journey's change.
   - The gates table gains the row.

7. **[`refine-journeys`](../../skills/refine-journeys/SKILL.md).**
   - **The spine says where the arc goes round,** in one line under the
     map, naming both phases. It is never a phase of its own.
   - **Renaming or removing a phase a workflow names** breaks that tag, and
     the gate says so. The workflow is retagged in the same change: a tag
     is not a re-cut.
   - The gates table gains the row.

8. **This repository.**
   - `trace.py` reads the map's header row of each journey, checks every
     `@phase:`, and prints the journey half of the map.
   - `inject.py`'s fixture gains a map and a phase. It gains the fault *a
     workflow naming a phase its journey does not have*, and the ledger
     row in its fixture bindings.
   - The bindings' ledger and fault record gain their rows.
   - `tests/` gains a test for each of the two wiring rules, run against
     `trace.py` on the injector's fixture, as `test_change_numbers.py`
     does for 0078's gate.
   - [`adopt-the-process`](../workflows/adopt-the-process.feature) names
     `@phase:putting-it-in @phase:the-changes-after`.
   - [`trusting-the-spec-again`](../journeys/trusting-the-spec-again.md)
     gains its loop line: from *Coming back* and from *Where it does not
     fit*, it goes back round to *The changes after*.

9. **The cases.**
   - **93,** `refine-workflows` on fieldnote, whose journey has phases.
     Asked to write up an attempt, it names the phase the attempt is made
     in, and adds none to the journey. It claims
     `a-workflow-names-the-phase-it-is-made-in`.
   - **94,** `refine-journeys` on fieldnote, whose journey reads as one
     pass through a year that starts again every spring. It writes the
     loop line naming two phases the map has, and adds no column for the
     loop. It claims `a-journey-says-where-it-goes-round`.

**Rules added**, live since the implementing commit:

| Rule id | Feature file | New or changed |
|---|---|---|
| `a-workflow-names-only-phases-its-journey-has` | [`features/wiring/a-workflow-names-its-phase.feature`](../features/wiring/a-workflow-names-its-phase.feature) | new |
| `the-map-places-each-workflow-in-its-phases` | [`features/wiring/a-workflow-names-its-phase.feature`](../features/wiring/a-workflow-names-its-phase.feature) | new |
| `a-workflow-names-the-phase-it-is-made-in` | [`features/refining/where-an-attempt-sits-in-the-arc.feature`](../features/refining/where-an-attempt-sits-in-the-arc.feature) | new |
| `a-journey-says-where-it-goes-round` | [`features/refining/where-an-attempt-sits-in-the-arc.feature`](../features/refining/where-an-attempt-sits-in-the-arc.feature) | new |

## What we are not doing

- **The word *stage*.** The request's word, and a second one for what the
  template already calls a phase.
- **Ids in the journey.** A journey names no workflow and carries no tag,
  and that stays true. The heading is the name. The cost is that a renamed
  heading breaks its workflows' tags, and the gate catches that rather than
  letting it pass.
- **A qualified tag such as `@phase:<journey>/<phase>`.** A workflow almost
  always names one journey, and the phase is looked up there. A workflow
  naming two journeys passes if either has the phase.
- **Gating or generating the loop.** It is one line of prose for a person to
  read. A workflow names a phase, not the way between two, and a check on
  the line would be a gate on prose, which `refine-journeys` refuses.
- **Making the phase required, or warning on its absence.** The request says
  optional, and a workflow that spans the whole arc is honest without one.
- **Rewriting *Who this is for* in past change specs.** They are a record of
  what was decided then, and nothing reads them as tags.
- **Filling the journey's *Ownership and metrics* table from the map.** That
  table is about opportunities, and an attempt sitting in a phase does not
  say whether it answers one.

## Data

No storage contract moves. Consuming repositories gain one gate row, and
nothing they already have fails: no workflow carries `@phase:` today. A
journey whose map has no table names no phases, so a workflow naming one
there fails, which is correct.

## Risks

- **A renamed phase heading turns the build red.** That is the gate doing
  its job, and the message names the phases that exist, so the fix is one
  tag. `refine-journeys` is told to retag in the same change.
- **A heading with punctuation slugs in a way nobody guessed.** The rule is
  one line in the method and the message lists the names it read, so a
  wrong guess is corrected from the failure.
- **`always-green`.** The gate runs only where a repository wires it, and
  reads only files in the tree.
- **Eval spend.** Editing `refine-workflows` and `refine-journeys` stales
  any tier rows they hold, and cases 93 and 94 start unmeasured. Named in the
  pull request, and nothing runs without the maintainer's yes.

## Acceptance checks

1. Run `verify.py` and read the map: *trusting-the-spec-again* in order, with
   `adopt-the-process` under two phases and the others saying nothing names
   them.
2. Change `@phase:the-changes-after` to `@phase:the-change-after` in
   `adopt-the-process.feature`. See verification fail, naming the workflow,
   the journey and its five phases.
3. Remove both `@phase:` tags. See verification pass, with no warning, and
   the workflow listed as not yet placed.
4. Read the journey template and confirm the journey prose still carries no
   tag.
