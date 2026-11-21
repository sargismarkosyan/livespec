# Spec 0085: less is the default

- **Status:** approved — by the maintainer in advance, 2026-11-19 (*"I agree with all. Please carry on with implementation."*), after the walkthrough deck of seven moves; implemented end to end, reviewed at the pull request
- **Issue:** [#192](https://github.com/sargismarkosyan/livespec/issues/192). The other six moves are [#193](https://github.com/sargismarkosyan/livespec/issues/193)–[#198](https://github.com/sargismarkosyan/livespec/issues/198)
- **Sketch:** skipped — approval was given in advance, holding the deck, so there was no decision left for one to support.

## Who this is for

**Ren — [`agent-accelerated-owner`](../personas/agent-accelerated-owner.md).**
Agents write all of their code and all of their rules, and nobody reads
either line by line. Whatever the agents add, Ren has to keep. Nothing about
who this is for moves.

**The workflow is [`adopt-the-process`](../workflows/adopt-the-process.feature).**
- The sitting writes the bindings and the context file at *Putting it in*,
  step 6 of [`trusting-the-spec-again`](../journeys/trusting-the-spec-again.md).
- Every change after that is written to this rule, at *The changes after*,
  step 8.

## The job behind the request

To keep a codebase, and the rules that hold it, small enough that the
person keeping it can still hold all of it. The request in the maintainer's
words: *"less code and less rules are always better"*. A second message
clarified that this is method, for every repository livespec is used in:
*"This is the rules that livespec should introduce whenever it is used as a plugin. Of course, his own refl is the first example."*

## Why now

- **Nothing in the method makes anything smaller.**
  - The implementation step is one line: [`process.md`](../../method/process.md), step 5.
  - The only line about the shape of code is about an unreachable branch: [`testing.md`](../../method/testing.md), *Coverage*.
- **Removing costs more than adding.** *No silent scope growth* makes code
  that this change made dead into "something else". Removing it then needs
  its own issue and spec, while adding the code is the normal path.
- **livespec itself is the evidence.**
  - What it ships grew from 2,717 to 7,194 lines (v0.9.0 to v1.29.0).
  - None of 63 spec pull requests had a net deletion; the smallest was +34.
  - The two parts with a ceiling stayed under it: the always-on descriptions, and this repository's context file.

## The end value

The default direction of every change is smaller.
- A change spec says what it removes before it is approved.
- An implementing agent deletes what its change made dead, in the same change.
- Whatever only grows has a ceiling. Growth then becomes a line in a diff, with its reason beside it, instead of a drift nobody sees.

**How we would know it worked:**
- Here: verification fails when a ceiling is exceeded.
  - For example, add a line to a skill body without raising the `skills/` ceiling. Verification fails, naming the part, its size and its ceiling.
- In a consuming repository: `refine-spec` asked to withdraw a behaviour writes a spec whose *What this removes* names:
  - the rule,
  - the test that claims it,
  - the code only that rule needed.
- The sitting writes a **Ceilings** row and wires the gate that reads it.

## What changes

1. **[`process.md`](../../method/process.md).**
   - **Step 5 of the loop:** the smallest change that makes the rules true,
     and what it made dead goes with it.
   - **The rule *No silent scope growth* becomes *Less is the default*,**
     and it keeps its old half:
     - reuse before writing;
     - add nothing no rule asks for;
     - what this change made dead goes in this change;
     - anything else found on the way is still filed, never fixed inline.
   - **A change whose whole value is less is a change like any other.**
   - **A new rule, *Whatever only grows has a ceiling*,** generalising the
     context-file ceiling: named in the bindings, lowered when the part shrinks,
     raised only in the change that needs the room, with the reason beside the
     number.

2. **[`testing.md`](../../method/testing.md), *Coverage*.**
   - **Its unreachable-branch bullet widens:** code no rule-bound test reaches
     is either a behaviour nobody specced (write its rule) or dead (delete it).
   - **A unit test reaching it keeps it covered, and does not answer the
     question.** The unit-test exemption stays exactly as it is. Its own
     section argues it is load-bearing.

3. **[`claude-md.md`](../../method/claude-md.md), requirement 7.** The rules
   worth having in front of an implementing agent gain *less is the default*.
   This is the one place that reaches the session that writes the code, since
   no skill implements.

4. **[`templates/change.md`](../../templates/change.md)** gains **What this
   removes**: the code, tests, rules and files the change deletes. *Nothing*
   needs its reason.

5. **[`templates/feature.feature`](../../templates/feature.feature).** Under
   *Changing this file later*: before adding a rule, see whether an existing
   one, reworded, already promises it.

6. **[`refine-spec`](../../skills/refine-spec/SKILL.md), *5. Shrink it*.**
   - It fills *What this removes*: what the change makes dead, by name.
   - It rewords an existing rule before adding one.

7. **A gate, `gate:part-past-its-ceiling`.**
   - **A part larger than the ceiling the bindings name fails.**
   - **So do bindings with no Ceilings row:** a number nobody wrote is not a pass.
   - It is a row in [`gates.md`](../../method/gates.md#the-ids) with `since`
     reading `next`, in the failure table and the fault table, and in the
     [template ledger](../../templates/bindings.md) and `tools/doctor.py`'s
     registry. The bindings template gains the **Ceilings** row.
   - `setup` writes the row from each part's size when the sitting has
     finished, the way it writes the context-file ceiling, and wires the gate
     by reading the gate table.

8. **This repository.**
   - **The Ceilings row:** `skills/`, `method/`, `templates/`, `tools/`,
     `.github/scripts/` and `specs/features/`, each at its size once this change
     is in. Lowering them is [#197](https://github.com/sargismarkosyan/livespec/issues/197).
   - **`trace.py`** reads the row and counts the lines git tracks under each part.
   - **`inject.py`'s fixture** gains a Ceilings row and two faults:
     - a part past its ceiling;
     - bindings with no Ceilings row.
   - The bindings' ledger and fault record gain their rows.
   - **`tests/test_ceilings.py`** holds the wiring rule against `trace.py` on
     the injector's fixture.
   - **Step 5 of [`CLAUDE.md`](../../CLAUDE.md)'s loop** says the same as the
     method's, within the file's ceiling.

9. **Case 95,** `refine-spec` on fieldnote, reusing case 69's scaffold
   rather than copying it.
   - The person asks for the place to go. It is always the weir, and he stopped filling it.
   - The spec's *What this removes* names:
     - the rule `place-carries-from-the-last-sighting`,
     - the test that claims it,
     - the `where` field the code writes and renders.
   - No source is edited. It claims `a-spec-names-what-it-removes`.

**Rules added**, live since the implementing commit:

| Rule id | Feature file | New or changed |
|---|---|---|
| `a-part-past-its-ceiling-fails` | [`features/wiring/a-ceiling-on-what-grows.feature`](../features/wiring/a-ceiling-on-what-grows.feature) | new |
| `a-spec-names-what-it-removes` | [`features/refining/what-a-change-removes.feature`](../features/refining/what-a-change-removes.feature) | new |

## What this removes

- **The rule *No silent scope growth*** as its own bullet. Its half that
  still holds is folded into *Less is the default*.
- **The unreachable-branch bullet** in *Coverage*. It is folded into the wider
  bullet that replaces it.
- **Nothing else, and this change grows the method.** The reason is that it
  adds the rule that stops the next change growing silently. The ceilings are
  set at the sizes this change leaves, so from the next change on, growth has
  to be argued.

## What we are not doing

- **A retired-id list for rules.** A deleted rule's id is still never reused
  (`ids-are-permanent`). A list and a gate holding it would be machinery for
  a failure nothing here has seen.
- **A new rule for rewording before adding.** Case 69,
  [`the-rule-keeps-its-id`](../../evals/69-the-rule-keeps-its-id/prompt.md),
  already grades the move: an existing rule reworded keeps its id. The
  template line and the skill line point at it.
- **Dropping the unit-test exemption.** It was proposed in the walkthrough
  and withdrawn there: [`testing.md`](../../method/testing.md#unit-tests)
  argues it is load-bearing.
- **A size line in the pull-request report.** The ceilings and *What this
  removes* already make growth visible where it is decided. A third place
  would be more report.
- **Merging `gate:context-file-ceiling` into the new gate.** It carries the
  reader's own limit, which the new gate has no use for. It is left for
  [#194](https://github.com/sargismarkosyan/livespec/issues/194).
- **Lowering any ceiling.** That is [#197](https://github.com/sargismarkosyan/livespec/issues/197),
  after the moves that remove enough to fit.

## Data

No storage contract moves. Consuming repositories gain one gate row and one
bindings row. A repository set up before this has no Ceilings row. `doctor`'s
`check:row-per-gate` reports the gate missing from its ledger, the way every
new gate has arrived.

## Risks

- **Parallel changes collide on the Ceilings row.** Every change that grows
  a part edits that row, so two in flight touch the same cell. That is the
  friction this rule is for: the second to merge argues its growth against
  the first's.
- **A ceiling becomes a chore that gets raised without thought.** The reason
  sits beside the number in the diff, where a reviewer reads it. Nothing more
  can be done here without judging prose.
- **`always-green`.** The gate runs only where a repository wires it, and
  reads only files in the tree.
- **Eval spend.**
  - Editing `refine-spec` stales its tier rows.
  - Editing case 69's scaffold path stales nothing, because it is not edited.
  - Case 95 starts unmeasured.
  - All of this is named in the pull request, and nothing runs without the maintainer's yes.

## Acceptance checks

1. Run `verify.py`: green, or exit 2 for stale tier rows only.
2. Add one line to any skill body. Verification fails, naming `skills/`, its
   size and its ceiling. Revert.
3. Delete the Ceilings row from the bindings. Verification fails, saying a
   number nobody wrote is not a pass. Revert.
4. Read [`templates/change.md`](../../templates/change.md) and confirm *What
   this removes* sits after *What changes*.
