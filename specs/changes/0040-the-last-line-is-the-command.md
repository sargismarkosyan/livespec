# Spec 0040: the last line is the command

- **Status:** proposed
- **Issue:** none — a direct request, made in chat on 2026-09-08 after the
  first audit to run under 1.2.0: *"doctor should suggest running
  /livespec:setup if needed."*
- **Depends on:** nothing to build. It stands behind
  [`0038`](0038-the-other-side-of-the-difference.md), which priced the second
  invocation this is about, and [`0039`](0039-the-world-a-test-runs-in.md),
  whose table was the first thing that price was paid for.

## Who this is for

[`agent-accelerated-owner`](../personas/agent-accelerated-owner.md), in
[`adopt-the-process`](../workflows/adopt-the-process.feature), at the seam
`0038` named — between having adopted the process and the process moving on
underneath them — at the moment the audit hands back.

Two persona lines decide the shape:

- **"They read the spec layer and not the documentation."** Which skill owns
  the wiring and which owns the record is documentation. It is argued in
  [`0021`](0021-asked-not-assumed.md) and [`0038`](0038-the-other-side-of-the-difference.md)
  and written into two skill bodies, and by their own account they will never
  open any of it. A last line that says *two things are setup's* asks them to
  know that split in order to act; a last line that says what to type does not.
- **"Investing in the pipeline is what they do when they are short of time."**
  A command is acted on. A fact about ownership is read, agreed with, and left
  where it is — which is what happened.

**This does not lengthen adoption.** `doctor` runs after the sitting, on a
repository that already has the process, and this changes one line of what it
says.

## The job behind the request

The literal ask: *doctor should suggest running /livespec:setup if needed.*

The job: **after an audit, to know what to type next without knowing which
skill owns what.** The audit already knows — it wrote the rows and handed them
over — and the person holding its output is the one person in the loop who
should not have to reconstruct the plugin's internal split to act on it.

The trigger, this evening: the ninth audit of `toil-tracker` under 1.2.0 wrote
the row `0039` obliges, corrected the record in three commits, and ended
*"Two things are `setup`'s: the coverage demand, now past its clock, and the
boundaries table."* The maintainer read that as the audit having produced no
change, and asked whether the changelog was broken. It was not. The line was
met to the letter of the rule that governs it — *the report ends by naming
setup with that row* — and missed in effect.

## Why now

Because `0038` recorded the cost of its own design and this is the first time
it was paid. That spec chose `doctor` correcting the record and `setup` wiring,
and wrote: *the cost is a second invocation, paid only when wiring is owed, by
somebody already holding the audit's output that says so.* The output did say
so. It said so as a possessive, in the middle of a paragraph about what the
audit had read, and the second invocation did not happen. A cost accepted in
the open is still a cost, and the first evidence about how it is actually paid
says the line that asks for it has to be an instruction rather than a fact.

## The end value

An audit that leaves wiring to be built ends with the command that builds it,
typed as somebody would type it, and the rows that command will be asked to
wire. Ren reads the last line and types it.

**How we would know it worked:** the next audit of `toil-tracker` ends with
`/livespec:setup` and its two rows, and the maintainer's next action is that
command rather than a question about the changelog.

## What changes

1. **[`doctor`](../../skills/doctor/SKILL.md) §4's last line becomes a
   command.** Where wiring is missing, the reply ends with the command that
   starts the sitting — `/livespec:setup`, in the prefixed form every
   repository's record already uses for a skill — followed by the rows it will
   be asked to wire, one per line. Not the skill's name as a noun: *two things
   are setup's* is a fact about ownership, and the person holding the report
   has to know what to type without knowing the split between the two skills.
   The same line closes the reading's record in the bindings, so the next
   person to open the ledger sees the command rather than the possessive.
   Where nothing is left for the sitting, no such line: the reply ends on what
   was corrected, and nobody is sent to a sitting nobody needs.
2. **One more refusal, one line.** `doctor` does not start the sitting. The
   command is said, not run: a setup nobody asked for gets stopped and
   questioned, and `setup`'s own first section is where that stop lives.
3. **The example in [`what-changed-since-the-stamp.feature`](../features/wiring/what-changed-since-the-stamp.feature)
   that says *the report ends by naming setup with that row*** is reworded in
   place to say the reply ends with the command that starts the sitting, with
   that row after it. Same rule, same id — a reworded example is the same
   promise stated the way this change now means it, and leaving *naming setup*
   there would have one rule saying what another refuses.

**Rules added or changed** — the `@rule:` ids in `specs/features/`:

| Rule id | Feature file | New or changed |
|---|---|---|
| `the-last-line-is-the-command-to-run` | `features/wiring/hand-back.feature` | new, `@planned` |
| `what-the-reading-finds-is-corrected-as-record-or-written-as-a-row` | `features/wiring/what-changed-since-the-stamp.feature` | changed — one example reworded, id kept |

A new file rather than a fifth rule in `what-changed-since-the-stamp.feature`:
that one is about what an audit reads between two versions, and this is about
how it hands over, which every audit does whether or not there was a range.

**No description changes, so no should-not-fire case is owed.** `doctor`'s
description already ends *building what is missing is setup*; what moves is
how that is said at the end of a run. `context-budget` stays at 4321 of 5000.

### The one decision, and who made it

**Suggest, or start.** The request says *suggest*, and that is what this
does. The alternative — `doctor` invoking `setup` at the end of a run, the way
`setup` runs the three interviews rather than naming them — is real and is
not taken here: `doctor`'s first refusal is wiring anything, a sitting nobody
asked for is the thing this persona stops and questions, and `setup`'s stop
before writing would make the chain end in a list anyway. If the command at
the end of an audit turns out to go untyped as often as the possessive did,
that is the next change, and it is argued from evidence this one will produce.

## What we are not doing

- **Not starting `setup` from `doctor`.** Above.
- **Not moving the stamp**, and not wiring anything from `doctor`. The split
  stands; what changes is the sentence that hands over.
- **Not a ninth skill**, and not a line in `CLAUDE.md`. The record already
  names `doctor`; what it hands to is `doctor`'s to say.
- **Not touching `setup`.** It already diffs an existing ledger rather than
  overwriting it and offers to wire the deferred rows; the command this adds
  lands on that behaviour as it stands.

## Data

No storage contract here. What this writes in a consuming repository is one
line at the end of the reading's record, and nothing else.

**This spec commit stales nothing.** One feature file whose rule is `@planned`
and claimed by nobody, and this file. `verify.py` exits **2** on it, as it does
on `main` today — *0 measured, 22 stale, 6 below the floor, 11 never measured*
— for the same rows and no other reason.

**The implementing change adds no case and no stale row that is not already
red.** It edits `doctor`'s body, and every case holding `doctor` is already
owed. [`39-a-real-row-over-a-stub`](../../evals/39-a-real-row-over-a-stub/prompt.md)
leaves wiring for `setup` — the pattern that missed `MemoryStore`, and making
the store real — so it gains a grader on its last message and claims the new
rule; it has never been measured, so nothing new goes stale. The reworded
example belongs to a rule [`36`](../../evals/36-what-moved-since-the-stamp/prompt.md)
claims, and `36` has never been measured either.

**What the pull request owes.** One skill body moves, so a `minor` label and a
`## Changelog` section; two `.feature` files move, so the Gherkin block.

## Risks

- **The command is read as having been run.** A reply that ends with a command
  can look like a skill that started it. The refusal line and the word *run*
  before the command are what separate the two, and the third example holds
  the case where no command belongs there at all.
- **A local copy shadows the plugin.** Where `.claude/skills/` carries a bare
  `setup`, the prefixed form reaches nothing. The prefixed form is what every
  record instructs by and what [`0037`](0037-a-name-that-already-belonged.md)
  reads names against, so it is the right form to print; a repository shadowing
  the plugin has the problem `0037` already describes, and this does not add to
  it.
- **The rows after the command go stale in the record.** They are the rows as
  they read at that reading, dated by it, the way every reading's record is.
  The next audit rewrites the line.

## Acceptance checks

There is no app; this repository's deliverable is the pull request description.

1. Run `doctor` in `toil-tracker`. The reply ends with `/livespec:setup` and,
   after it, the coverage demand and the boundaries table; the ledger's tenth
   reading ends with the same line; the stamp is still 0.25.0.
2. Run `doctor` on a fixture that corrects only record — `35`'s, whose one
   finding is a renamed skill. The reply ends on the correction and sends
   nobody to a sitting.
3. `python3 .github/scripts/verify.py` — exit 2 on this spec commit for the
   rows already owed and nothing else red. The rule drops `@planned` in the
   implementing change, claimed by `39`.
