# Spec 0050: regardless of its current value

- **Status:** proposed
- **Issue:** [#99](https://github.com/sargismarkosyan/livespec/issues/99) —
  the last of three split from the CLAUDE.md report of 2026-09-15, after
  [`0046`](0046-a-number-and-no-file-to-copy.md) settled what the file is held
  to, [`0048`](0048-the-file-every-session-reads-first.md) made the build
  refuse one out of shape, and [`0049`](0049-the-readers-own-limit.md) bounded
  its length.
- **Depends on:** those three, all released. The remedy this spec writes
  rewrites *to* their requirements and their limit, and hands back a file
  the gate they built will pass.

## Who this is for

[`agent-accelerated-owner`](../personas/agent-accelerated-owner.md), in
[`adopt-the-process`](../workflows/adopt-the-process.feature), at section 6
of the sitting — the moment an existing CLAUDE.md is read and something is
done about it — and at every audit after, which is where the file is next
read whole. Two persona lines decide the shape. *"A setup they did not agree
to gets stopped and questioned rather than inherited"*: a rewrite of a file
they wrote by hand is the setup most worth stopping, so it is shown whole and
waits, even in a sitting told to go ahead. And *"the hand-built local version
stays"* where the tool does not fit — which is why the rewrite harvests before
it writes: the facts only that file knows are the local version, and a
rewrite that drops them is a regression with a tidy diff.

**This lengthens the sitting by one stop**, and names what it shortens: every
session after, in every repository whose CLAUDE.md was a filled template.
The persona never opens the file; the agent opens it first, every time. A
file patched requirement by requirement keeps the property that made it bad,
and every session pays for that property in attention until somebody rewrites
it — which, without this, nobody is asked to.

No always-promise moves. **`never-implements`** is closest and untouched: a
CLAUDE.md is context, not application code, and `setup` has written it since
0008.

## The job behind the request

The literal ask: *"Regardless of its current value always suggest complete
rewrite if anything is not aligned with livespec motto."*

The job: **a CLAUDE.md that is out of line should be replaced by one written
for the agent that reads it, keeping only what the old file alone knew — not
improved by the twenty per cent a patch adds.** Today the two places a
CLAUDE.md is judged both patch. `setup` §6 reads the file against the
requirements, marks each met, missing or stale, *"then shows the edit and
makes it"*. `doctor` §2 corrects *"in place"*, a line at a time, and is
forbidden more. Neither has a path to a new file. So a file assembled from
somebody else's blanks — the shape [`claude-md.md`](../../method/claude-md.md)
opens by refusing — gets its blanks filled in better, and reads like a filled
template to every session forever, with all ten requirements marked met.

*Aligned with the motto* has to become something a session applies the same
way twice. The motto is [`spec.md`](../spec.md)'s first sentence — installed
so that the specification cannot quietly stop being true — and for this file
it cashes out as the requirements 0046 fixed and the shape 0048 gates. So the
trigger is the reading's own verdict: **a requirement missing, or anything
the method rules out present** — a copied loop, a copied rule, an
aspirational one, history that binds nothing — offers the rewrite, whatever
else the file gets right. **A path that moved is a fix**, because a line is
the whole finding, and the method already says a stale pointer is corrected
in the change that moved it.

What happens today instead: the maintainer holds a file up and says *like that
one*; the sitting patches; the next session reads the patched template.

## Why now

Because the other two thirds of the report have shipped and left the remedy
as the gap: since 0048, a build fails a CLAUDE.md that is out of shape, and
the sitting's only answer to that failure is a patch. And because the
rewrite now has a bound to rewrite to — two hundred lines — which it did not
have when the issue was filed.

## The end value

A CLAUDE.md the reading finds out of line is offered whole: a new file written
from the requirements, carrying every fact the old one alone knew, shown beside
what was kept and what was dropped, and written only on a yes. The audit,
finding the same, corrects the lines it can and leaves the rewrite named for
the sitting instead of doing it. A patch is what happens to a line, not to a
file.

**How we would know it worked:** a sitting in a repository whose CLAUDE.md is a
filled template proposes a new file rather than a diff, lists the one
paragraph in it worth keeping before writing, and has not touched the file on
disk when it hands the proposal over; an audit of the same repository corrects
the stale step, writes nothing else into the file, and leaves its line open
naming the rewrite and the sitting; `toil-tracker`'s deployment paragraph, put
through the rewrite, comes out the other side with its date and its argument.

## What changes

1. **[`claude-md.md`](../../method/claude-md.md) gains a section, *When it
   is out of line*.** A stale path is a fix, in the change that moved the
   path. A file missing a requirement, or carrying what must stay out, is not
   fixed by the line: it is rewritten from the requirements, whatever it is
   currently worth, because a patched template is a template. Before the
   rewrite, harvest — list every fact only this file knows — and carry each
   into the new file or name it as dropped with the reason. Show the new file
   whole and wait; a rewrite that lands unasked is worse than the patch it
   replaced. The sitting does this; the audit corrects a line and leaves a
   file that needs rewriting open, naming the sitting.
2. **[`setup`](../../skills/setup/SKILL.md) §6** replaces *show the edit and
   make it* with the procedure: the met/missing/stale list as now; then, where
   anything is missing or ruled out, the harvest, the new file written from
   the requirements and carrying it, shown whole beside kept and dropped, and
   a stop — the yes at the start of the sitting does not cover replacing a
   hand-written file, which the skill's first section already lists as the
   thing to name before overwriting. Where the only finding is a line, the
   line. Then the ceiling row, from the file as it ends.
3. **[`doctor`](../../skills/doctor/SKILL.md) §2** gains a sentence: a
   CLAUDE.md out of line beyond its lines is not rewritten by the audit;
   correct the lines that are record, and leave `check:loop-per-claude-md`
   open with the rewrite as what closes it and the sitting as whose it is.
   The tool does not move: an open record line is already printed with what
   closes it, and the generated last line stays what 0040 made it.
4. **The 0038 rule** `what-the-reading-finds-is-corrected-as-record-or-written-as-a-row`
   gains an example, id kept, that scopes *in place* to a line and leaves a
   rewrite to the sitting — the conflict the issue named, resolved without
   renaming anything.
5. **Three rules**, `@planned`, in a new file — the sitting's half.
6. **Two cases**, numbered next, at build time: `setup` in a repository whose
   CLAUDE.md is a filled template with one paragraph worth keeping, told to
   go ahead at the start; and `doctor` in a repository with bindings in shape
   and the same kind of file, which must correct the stale step in place,
   rewrite nothing, and leave the line open naming the sitting.

**Rules added or changed** — the `@rule:` ids in `specs/features/`:

| Rule id | Feature file | New or changed |
|---|---|---|
| `a-file-out-of-line-is-offered-whole` | `features/setup/rewriting-the-context-file.feature` | new, `@planned` |
| `what-only-the-file-knows-survives-the-rewrite` | `features/setup/rewriting-the-context-file.feature` | new, `@planned` |
| `a-rewrite-lands-only-on-a-yes` | `features/setup/rewriting-the-context-file.feature` | new, `@planned @refusal` |
| `what-the-reading-finds-is-corrected-as-record-or-written-as-a-row` | `features/wiring/what-changed-since-the-stamp.feature` | changed — one example added, id kept |

A new file rather than three more rules in
[`setup/context-file.feature`](../features/setup/context-file.feature), which
holds three and is about what the file is held to; this is about what is done
when it is not, and a file at the soft limit is a file that has stopped being
about one thing.

**No description changes, so no should-not-fire case is owed.** `setup`'s
description already carries *write or audit CLAUDE.md*; `doctor`'s already
carries *corrects the record, never the wiring*. `context-budget` stays at
4321 of 5000.

## What we are not doing

- **Not rewriting on a single stale pointer.** The maintainer's *anything* is
  read as anything the method rules out or requires, not as any line that
  aged: a moved path is the case `claude-md.md`'s *Keeping it true* already
  assigns to the change that moved it, and rewriting a good file for one line
  is the churn that teaches people to say no to the offer.
- **Not letting the audit rewrite.** The audit changes the record and never
  the wiring, and a whole new CLAUDE.md is the sitting's kind of change —
  shown, stopped for, and written under the person's name. `doctor`'s last
  line already hands the sitting what it could not build; this hands it what
  it would not.
- **Not writing a template to rewrite from.** The rewrite is from the ten
  requirements, as the method has always said; the difference is that it is
  whole rather than a patch. A template would recreate the file this exists
  to replace.
- **Not scoring the file.** *Eight of ten met* is reported and is not a
  threshold; a file with copies in it is offered the rewrite at nine of ten.
- **Not touching the gate.** 0048's gate reads shape; this is what the sitting
  does about a file that fails it, or passes it and is still noise.

## Data

No storage. Files that move: `method/claude-md.md`, `skills/setup/SKILL.md`,
`skills/doctor/SKILL.md`, two `.feature` files, two new cases with their
scaffolds and graders, `evals/README.md`, and this spec.

**This spec commit stales nothing that is not already red.** Three rules,
`@planned`, claimed by nobody; one example added to a rule claimed by cases
`36` and `40`, both never measured. `verify.py` exits **2** for the rows
already owed and no other reason.

**The implementing change adds no stale row that is not already red.** It
edits both skill bodies; every measured case holding `setup` or `doctor` is
already owed. It adds two cases at about **$1.80 each at the floor**, never
measured until the maintainer approves a run.

**What the pull request owes.** `method/` and two skills move — **`minor`**,
a changed remedy — a `## Changelog` section, a Gherkin block for the two
`.feature` files, and — `skills/doctor/` being on the audit surface — an
`## Ids` section reading *unchanged*.

## Risks

- **The rewrite drops something.** The harvest is listed before the file is
  written and each item is accounted for as kept or dropped with the reason;
  the second rule holds it and the setup case grades the one paragraph that
  matters most.
- **The offer becomes the default and nobody reads it.** It is shown whole
  beside kept and dropped, and it waits; a sitting that writes it without the
  yes fails the refusal rule, which is graded on the file on disk.
- **Two skills disagree on the same file.** They cannot: the audit corrects
  lines and hands the rest over; the sitting rewrites. The example on the
  0038 rule is where that line is drawn, in as many words.
- **A repository whose file is out of line and whose owner says no.** Then it
  stays as it is, patched where a line was the finding, and the audit's line
  stays open — a decision made in the open, which is what the ledger is for.

## Acceptance checks

1. Run `setup` in a scratch repository whose CLAUDE.md is a filled template
   with one real paragraph, saying *go ahead and write files*. It reads the
   file against the ten, lists the paragraph as harvested, shows a whole new
   file beside kept and dropped, and stops; `git status` shows CLAUDE.md
   unchanged until the answer.
2. Run `doctor` in the same repository with bindings in shape. The stale loop
   step is corrected in place; nothing else in the file moves;
   `check:loop-per-claude-md` reads open with the rewrite and the sitting
   named; `--validate` accepts the record.
3. In `~/Projects/toil-tracker`, put *Where it lives* through the harvest by
   hand: it is listed, and it reads in the proposed file with its date and
   the change it names.
4. `verify.py` exits 2 for the rows already owed; the pull request carries
   `minor`, `## Changelog`, `## Ids: unchanged` and the Gherkin block.
5. #99 closes with what was asked, what shipped, and why they differ.
