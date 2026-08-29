# Spec 0023: a case nobody described

- **Status:** approved
- **Issue:** [#62](https://github.com/sargismarkosyan/livespec/issues/62)
- **Depends on:** [`0022`](0022-nobody-types-the-record.md) — the same defect, one
  file over, and the argument for gating an enumeration rather than correcting it
  is made there.

## Who this is for

**Not [`@persona:agent-accelerated-owner`](../personas/agent-accelerated-owner.md),
no workflow, and no always-promise.** This is livespec's own test suite and its
own gate script — a contribution step, which
[`workflows/README.md`](../workflows/README.md) keeps out of the workflow layer
on purpose and
[`process.md`](../../method/process.md#a-technical-change-that-serves-no-workflow-is-correct-not-a-gap)
says is correct rather than a gap.

Who it is for is the person reviewing a change to a skill. The suite is the only
thing standing between a widened `description` and a regression nobody sees for
four versions, and *What each case is for* in
[`evals/README.md`](../../evals/README.md) is how anyone sees what is in it
without opening twenty-five directories. A case with no row is a case that gets
reviewed by nobody.

## The job behind the request

The literal ask: *"You don't need to have the actual data here, you should have a
gate script to cover that up, and in each eval file you should mention the rule &
feature that it backs up."*

Two halves, and they need separating. **The gate is right and this change builds
it.** The tags are the right shape for a repository whose rules came first — and
this is not one, which the bindings say in as many words and *Not doing* quotes
in full.

The job under both: **what a case holds should be visible in one place, and that
place should not be able to fall behind.** It fell three rows behind — `21`, `22`
and `23` had no row until [`0022`](0022-nobody-types-the-record.md) added them —
and nothing anywhere would have said so.

**What is done today instead:** the row is written when somebody remembers.
Three times out of five recently, nobody did.

## Why now

[#59](https://github.com/sargismarkosyan/livespec/issues/59) found this table
three rows short in the same breath as the fault injection record was found six
short. `0022` fixed the record properly — the enumeration is now read back from
`inject.py` and cannot drift — and fixed this one by typing the three missing
rows, which is the fix `0022` itself argues against.

So the defect is still here, in the state `0022` described as the one that comes
back in four versions.

**And the issue that reported it is wrong about the cause**, which is worth
saying because the wrong cause is the expensive one. `#62` reads six cases
claiming no rule as an oversight nothing catches. It is neither. Those six are
part of the nine that predate the spec layer, and their exemption is a decision
recorded in three places — including
[`setup`](../../skills/setup/SKILL.md) section 7, which ships to every user:

> **Existing tests do not have to claim a rule.** They are unit tests as far as
> this process is concerned until a rule exists that they answer to. Say this in
> the bindings, or someone will spend a week retrofitting decorators.

The bindings say it. Retrofitting them here would be this repository doing what
the plugin tells everybody else not to.

## The end value

Somebody opening `evals/README.md` sees every case in the suite, because
`verify.py` fails if one is missing. The table stops being a thing somebody
remembered to update.

**How we would know it worked:** add a case directory and no row. `verify.py`
goes red naming the case. That is what did not happen three times.

## What changes

- **`evalsuite.py` checks the case table both ways.** Every directory under
  `evals/` has a row in *What each case is for*; no row names a case that is not
  there. It goes in the block that already reads `evals/README.md` for the
  documented invocation, because that file is already this gate's business.
- **`inject.py` gains two faults**: a case with no row, and a row naming a case
  nobody has. The fixture's `evals/README.md` gains a table generated from the
  fixture's own cases, so it is green by construction and each fault is one edit
  from it — the same shape `0022` gave the bindings.
- **`08-fix-it-while-recording` claims
  [`the-form-follows-what-changed`](../features/showing/what-a-change-shows.feature).**
  Its `insists-on-a-clip` grader is that rule's first Example seen from the other
  side: `08` holds *the change is only legible while it happens, so a single
  frame is not offered in its place*, and `22` holds the still. Nothing
  retroactive about it — the rule was written for
  [`0020`](0020-enough-to-say-yes.md) on its own terms and has been live since.
  Its other grader, `files-rather-than-fixes`, still claims nothing, and that is
  the exemption working rather than failing.
- **The tag contract stops counting.** `specs/setup/README.md` says *"A case is
  not required to claim a rule, and six now do"* — a typed count, in the file
  `0022` was about, one edit from being wrong. The exemption is the point of that
  sentence; the tally is not.

**Rules added or changed:** none. `08` claims a rule that already exists and no
rule text moves, so nothing here touches the spec surface. The gate is
livespec-local machinery, as in
[`0013`](0013-the-board-of-latest-measurements.md) and `0022`.

## What we are not doing

- **Not requiring every case to claim a rule.** This is the boundary the issue
  asked to move, and it is moved on purpose or not at all. Three files record it:
  [`specs/README.md`](../README.md) (*"the nine eval cases predate this layer and
  were not retroactively specced"*), the tag contract in
  [`specs/setup/README.md`](../setup/README.md) (*"A case is not required to
  claim a rule"*), and `setup` section 7, quoted above. The five rules it would
  take — for `refine-spec`, `refine-personas`, `refine-workflows`,
  `refine-journeys` and `record-clip` — would each be derived from the grader
  that already asserts it, which is a spec written backwards from its own test.
  They get a rule when a change touches that skill, which is exactly how `22`
  got its two in `0020`.
- **Not deleting the table.** With the exemption standing, it is not a second
  copy: for the six exempt cases it is the *only* statement of what they hold,
  and the argument paragraphs beneath it refer to its rows by number.
- **Not gating what a row says**, only that there is one. A row reading *"holds
  the thing"* passes. The alternative is a gate on prose quality, which is not a
  gate.
- **Not re-measuring `08`.** Claiming a rule changes the case's own file, so
  `measurement_inputs` moves and the board entry goes stale — `verify.py` stays
  red on that one row until somebody runs it. That somebody is the maintainer:
  one case at `runs: 3`, about $1.80, and `--i-approve-the-cost` is their
  signature. The command is in *Acceptance checks*; this change stops in front of
  it.

## Data

No storage contract; this repository has none. One row of `evals/board.json` goes
stale by design and is healed by a run, not by an edit.

## Risks

**The branch is red until `08` is re-measured**, and that is the whole of it —
every other check passes. A reviewer seeing a red required check should read the
board failure rather than assume the change is broken, which is what the pull
request body is for.

**A gate that reads prose can be defeated by reformatting.** Somebody reflowing
the table could make it pass while saying nothing. Mitigated the way `0022`
mitigated it: the faults break it in both directions, a missing row and an
invented one, rather than only checking that a green tree stays green.

**The exemption now has a gate leaning against it.** Every case must appear in
the table, and six of them appear there with no rule to point at. That is the
honest state — but the next person to read this may take the table's completeness
as evidence the suite is fully specced. The tag contract paragraph is where that
is answered, and it says so.

## Acceptance checks

1. `python3 .github/scripts/verify.py` fails on exactly one thing: the board
   entry for `08-fix-it-while-recording`. Every other gate is green.
2. Add a directory `evals/26-nothing/` with a `prompt.md` and a grader.
   `verify.py` names it as having no row. Remove it.
3. Add a row for `` `99-not-a-case` `` to the table. `verify.py` names it as a
   row for a case that does not exist. Remove it.
4. `python3 evals/runner/run.py --case 08-fix-it-while-recording --ablation
   with-without --judge-model sonnet --allow-tools Write Edit --scaffold`
   refuses without `--i-approve-the-cost`. **The maintainer runs it with the
   flag; nobody else adds it.** `verify.py` is green afterwards.
