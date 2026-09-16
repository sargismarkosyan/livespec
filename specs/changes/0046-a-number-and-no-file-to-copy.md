# Spec 0046: a number, and no file to copy

- **Status:** approved
- **Issue:** [#100](https://github.com/sargismarkosyan/livespec/issues/100) —
  one of three split from a single report on 2026-09-15, with
  [#98](https://github.com/sargismarkosyan/livespec/issues/98) (a gate for
  CLAUDE.md) and [#99](https://github.com/sargismarkosyan/livespec/issues/99)
  (a rewrite offered rather than a patch). This one goes first because the
  gate cannot be specced until it is settled: a gate reads a number, and the
  method has none.
- **Depends on:** nothing to build. It stands behind
  [`0038`](0038-the-other-side-of-the-difference.md), which made CLAUDE.md
  part of the record an audit corrects, and
  [`0039`](0039-the-world-a-test-runs-in.md), which last moved
  `claude-md.md`. The next two specs stand on it: the gate reads the number
  this writes, and the remedy names *over the ceiling* as one of its triggers.

## Who this is for

[`agent-accelerated-owner`](../personas/agent-accelerated-owner.md), in
[`adopt-the-process`](../workflows/adopt-the-process.feature), at section 6 of
the sitting — where an existing CLAUDE.md is read against the requirements —
and at every audit after it, where `check:loop-per-claude-md` hands the same
reading to a mind. Concretely, in the repository they hold up as the good
example, `toil-tracker`, whose file the method as written rules against.

Two persona lines decide the shape. *"The agent does not work out what the
repository already implies"* is the first miss on their list — and a rule
that has the agent report the most load-bearing paragraph in that file as
*history to remove* is that miss written into the method, so that a session
applying the rule faithfully deletes the sentence that stops the next
production bug. And *"READMEs, docs and comments are for the agent"*: CLAUDE.md
is the one file every session reads first and the person never opens, so a
requirement about it that two readers apply differently is checked by nobody.
The person will not catch it by reading; the rule has to be one that reads the
same way twice.

**This lengthens the sitting by nothing.** No question is added; one row is
written from a measurement the sitting already has in hand. What it shortens is
every audit after: a length verdict that is a comparison rather than an
opinion, and a *must stay out* list that does not send the auditor back to the
person to ask whether the best paragraph in the file is allowed.

No always-promise moves. The nearest is **`context-budget`**, and it is worth
saying why: a consuming repository's CLAUDE.md is that repository's always-on
cost, paid by every session there the way this plugin's descriptions are paid
here — which is the reason the file has a ceiling at all, and the reason the
number belongs to the repository that pays it.

## The job behind the request

The literal ask, from the report the three issues were split from: *"Be very
strict with CLAUDE.md files, a good example is the ../toil-tracker one, add a
separate strict gate for it, and make sure that it follows your structure and
has everything that you want him to have."* And the piece of it this spec
answers, as [#100](https://github.com/sargismarkosyan/livespec/issues/100)
found it: the requirement a gate would read cannot be applied as written, and
the file the method calls its reference is not the one the maintainer points
at.

The job: **a rule about the file every session reads first has to be one two
readers apply the same way, and it has to be right about the best file anybody
has.** Today it is neither. *One screen of scroll, and about a hundred lines*
gives three real files three verdicts depending on who reads *about* —
`todo-change` at 101 passes, `toil-tracker` at 134 and this repository at 138
either pass or fail by twenty-five and thirty-eight per cent — and *What must
stay out* rules twice against `toil-tracker`'s *Where it lives*: as *a history
of the project* and as *an explanation of a decision*. That paragraph is the
one that says the file claimed *not deployed* until 2026-09-14, that spec 0071
argued from it that a new endpoint needed no rate limit, and that a person
caught it rather than anything in the repository. It is a rule with its
evidence attached. The method reads it as a diary.

What happens today instead: the maintainer holds a file up by hand and says
*like that one*; section 6 applies its judgment once, at the sitting; and
nobody can say afterwards whether the verdict would come out the same way
again, because the rule has no number and the list has no test.

## Why now

Because the report came in on 2026-09-15, and the gate it asks for is blocked
on this. And because two things are true today that will not stay true quietly:

- **The reference implementation has drifted.** `method/claude-md.md` points at
  `todo-change`'s CLAUDE.md on `main`. Read back on 2026-09-16 — 103 lines,
  last touched 2026-08-23 — that file mentions no plugin at all: it sends the
  reader to *the loop, and the rules* in a copy of the method inside that
  repository's `specs/setup/`, lists `.claude/skills/` as where the skills
  live, and instructs by `feedback`, a skill that has been `todo` since 1.0.0
  (2026-09-02). It fails requirement 3 of the page that calls it the
  reference, and it is the two-copies-of-a-method shape the page exists to
  prevent. The plugin-era rewrite of that file exists, and sits on a branch
  that was never merged. The one CLAUDE.md the method names as the shape to
  learn from is a copy that drifted, found in the plugin's own method page.
- **A file grows in ones.** This repository's own CLAUDE.md went from 125 to
  138 lines in eight commits over nineteen days — one, three, two lines at a
  time — past a rule nobody could point to, and no diff ever showed a number
  moving. A ceiling in the bindings would have made each of those a visible
  line in a review.

## The end value

After this, a CLAUDE.md is held to a number its own bindings name, written from
what the file is and raised only in the open; the requirements admit a dated
account that still binds and rule out one that does not, by a test a second
reader gets the same answer from; and the method points at no file at all.

**How we would know it worked:** `toil-tracker`'s file read against the page as
it will stand — *Where it lives* reads met and not history, and its length is
a comparison against a number in its bindings rather than an opinion about
*about*; [#98](https://github.com/sargismarkosyan/livespec/issues/98) can be
specced, because there is a number for its gate to read; and
`grep -n "http" method/claude-md.md` finds nothing.

## What changes

1. **`method/claude-md.md`, *Length*.** *One screen of scroll, and about a
   hundred lines* goes. In its place: the file has a **ceiling**, and the
   number is a binding — the repository's `specs/setup/README.md` names it, in
   a size its gate can read, with what reads it and which change set it. The
   figure written at the sitting is what the file is when the sitting has
   finished with it, and it is raised only in the change that needs the room,
   with the reason beside the number, so growth is a line in a diff rather
   than a drift nobody sees. The method names no figure: a threshold in the
   method is a binding in the wrong file, which is the page's own line four.
   What the page keeps is the why — it is in front of every request, so it is
   the repository's always-on cost — and the what-to-do past it: something in
   it is a pointer that turned into a copy; move it and link it. It also says
   the thing *about a hundred* was standing in for: the requirements already
   bound the file — two or three sentences here, eight steps there, four or
   five lines in one block, a line per directory — so a file that meets them
   is short, and the number is what stops it growing afterwards. The *test to
   apply* paragraph stays as it is.
2. **`method/claude-md.md`, *What must stay out*.** The *history* bullet and
   the *explanations of decisions* bullet are rewritten around one test: *does
   it still change what the next change may do?* A dated account of what this
   file used to claim, until when, and which change argued wrongly from it, is
   a rule with its evidence attached and stays — it is what stops an agent
   discounting the rule as decorative, which is the failure the *aspirational*
   bullet already names. An account of something that binds nothing now is
   history, and the change specs and the version history are where it goes.
   The reasoning *behind* a decision still belongs in
   `specs/setup/constraints.md`; the rule it produced, and the one line saying
   why that rule is not aspirational, are this file's.
3. **`method/claude-md.md`, *Keeping it true*.** The reference-implementation
   paragraph goes. Nothing replaces it but the sentence the page opens with,
   restated where the paragraph was: there is no file to copy, on purpose. The
   requirements are the contract; a named exemplar is a template with extra
   steps for anyone in a hurry, and the one the page named had already
   drifted by the time anybody read it back.
4. **[`templates/bindings.md`](../../templates/bindings.md)** gains a row in
   the table: **CLAUDE.md ceiling** — the size the file may not exceed, what
   reads it, and which change set it. The template is on the audit surface, so
   the pull request carries an `## Ids` section reading *unchanged*: no check
   is added and no id moves. The row is a fact the gate in #98 and the audit
   will read; today it is a fact.
5. **[`skills/setup/SKILL.md`](../../skills/setup/SKILL.md) §6** gains a
   sentence: once the file is written, or the audit's edits are made, write
   the ceiling row from what the file then is — never before, and never from a
   figure the method does not have. **`doctor` does not move.** The number
   becomes a check when the gate does, in #98; until then
   `check:loop-per-claude-md` hands the file to a mind as it already does.
6. **This repository's own bindings** gain the row, in the implementing change:
   `CLAUDE.md` at the size it is that day — 138 lines as this spec is written —
   read with `wc -l`, set at 0046. Nothing here reads it until #98, and the row
   says so rather than implying a gate that does not exist.
7. **Three rules**, all `@planned`, in a new file:

**Rules added or changed** — the `@rule:` ids in `specs/features/`:

| Rule id | Feature file | New or changed |
|---|---|---|
| `the-ceiling-is-a-number-in-the-bindings` | `features/setup/context-file.feature` | new, `@planned` |
| `a-dated-account-that-still-binds-is-not-history` | `features/setup/context-file.feature` | new, `@planned` |
| `the-requirements-are-the-only-reference` | `features/setup/context-file.feature` | new, `@planned` |

A new file rather than rows in
[`setup/hand-back.feature`](../features/setup/hand-back.feature): that file is
about what the sitting leaves behind, this is about what one of those things
is held to, and the next two specs add to the same subject.
`setup-audits-an-existing-claude-md` keeps its id and its wording — it asks
that each requirement be reported met, missing or stale, and it still does;
what changes is what the requirements say.

**No description changes, so no should-not-fire case is owed.** `setup`'s
description already carries *write or audit CLAUDE.md*. `context-budget` stays
at 4321 of 5000.

## What we are not doing

- **Not the gate.** That is #98. This writes the number a gate will read and
  fixes the list it will read against; the split of the ten requirements into
  what a script can read and what only a session can is the gate's design, and
  is specced there.
- **Not the remedy.** That is #99. Rewrite over patch changes what section 6
  does *after* the reading; this changes what the reading finds.
- **Not naming `toil-tracker` in the method, or any file.** The maintainer's
  example is honoured by moving the rule to admit what makes that file good,
  not by a URL in a page that names no filename. This is the decision most
  likely to be overturned, and it is one paragraph to reverse: name the file,
  pinned at a commit rather than at `main`, so that it cannot drift the way
  the last one did.
- **Not a unit in the method.** Lines, here, because the file is prose wrapped
  at eighty columns and every reading of it so far — the report, the audit
  tool's own line — has counted lines. Characters would be the purer measure
  of what a session pays, and a repository whose gate reads characters writes
  characters. The method says *a size its gate can read* and leaves it there.
- **Not a figure in the method, not even a recommended one.** The sitting's
  recommendation is a rule — *what the file is when you are done with it* —
  rather than a number, the way its coverage recommendation is *the whole of
  what is in scope* rather than eighty.
- **Not touching this repository's CLAUDE.md, and not shrinking it.** It is at
  its ceiling by construction. Whether it carries copies of what the plugin
  already says is a question for the audit, and for #99's remedy.
- **Not editing `todo-change`'s file.** Its next audit reads this entry in the
  range after its stamp; the stale skill name is that repository's to correct,
  as record, and `check:skill-names` already flags it there.

## Data

No storage. Six files move: `method/claude-md.md` by three sections,
`templates/bindings.md` by a row, `skills/setup/SKILL.md` by a sentence,
`specs/setup/README.md` by a row, one new `.feature`, and this file.

**This spec commit stales nothing.** Three rules, `@planned` and claimed by
nobody; no skill body moves. `verify.py` exits **2** on it, as it does on
`main` today — *0 measured, 22 stale, 6 below the floor, 12 never measured* —
for the same rows and no other reason.

**The implementing change adds no stale row that is not already red.** It
edits `setup`'s body, and all eight measured cases holding `setup` (`09`, `11`,
`12`, `16`, `17`, `23`, `26`, `27`) are already owed a run; the other three
(`30`, `31`, `38`) have never been measured. What it adds is **one new case**,
numbered next: `setup` in an occupied repository whose existing CLAUDE.md
carries a dated deployment constraint, a paragraph about a migration finished
long ago, and a shape like nobody else's — graded on the constraint kept as
met, the finished migration named as history, the ceiling row written from the
file's size after the edits, and no other repository's file offered as the
shape. About **$1.80 at the floor**, claiming all three rules. Which of the
stale rows are worth re-measuring is the maintainer's spend to approve; the
commit and the pull request finish with a gap where the numbers go.

**What the pull request owes.** `method/`, `templates/` and a skill move —
**`minor`**, because what section 6 rules out is a changed judgment, not a
rewording — a `## Changelog` section that says where to look
(`claude-md.md`'s *Length*, *What must stay out* and *Keeping it true*, the
template's new row, `setup` §6), an `## Ids` section reading *unchanged*, and
the Gherkin block for the `.feature` that moves.

## Risks

- **A ceiling at today's size blesses a bad file.** The number is written after
  section 6 has read the file and made its edits — and, once #99 lands, after a
  rewrite where one was offered. The number says how big; the requirements say
  what. A number that is too generous is at least a number somebody can see
  and argue with, which *about a hundred* never was.
- **The number gets raised casually.** It is a line in the bindings in the same
  pull request as the growth, so the reviewer sees both. Until #98 that
  strictness is the reviewer's, as it is for a coverage exclusion; after it, a
  growth without the raise fails the build.
- **"Still binds" is judgment.** It is, and the split between what a script
  reads and what a mind does is #98's to draw. What this does is give the
  judgment a test a second reader gets the same answer from — *does it change
  what the next change may do?* — instead of a category, *history*, that the
  best example in hand fell into by accident.
- **Removing the reference removes the only worked example.** The requirements
  are worded as their own examples — *two or three sentences*, *eight steps at
  most*, *four or five lines in one block* — section 6 reads them one at a
  time, and a repository that wants an example of its own has one after a
  single sitting. Named above as the decision to reverse if the maintainer
  wants a file named.
- **A consuming repository set up under the old rule.** Nothing fires unasked,
  as with every change to the method. Its next audit reads this entry in the
  range after its stamp; the missing row is record rather than wiring, so the
  audit writes it — from the file's size that day — the way it corrects a
  loop step. The stamp stays where it was.
- **The always-promises.** `always-green`: nothing here gates anything, in any
  repository. `context-budget`: no description moves. `never-implements`: a
  row and three sections of prose. `ids-are-permanent`: three ids added, none
  renamed, `setup-audits-an-existing-claude-md` kept.

## Acceptance checks

There is no app; this repository's deliverable is the pull request description.
What is checked by hand:

1. `method/claude-md.md` after the implementing change: *Length* names no
   figure and says where the number lives; *What must stay out* admits a dated
   account that still binds, in as many words, and sends the reasoning behind
   a decision to `specs/setup/constraints.md` as before; the page carries no
   URL. `grep -rn "about a hundred" method/ skills/ templates/` finds nothing.
2. In `~/Projects/toil-tracker`, read its CLAUDE.md against the page as it
   will stand: *Where it lives* reads met — a rule with its evidence — and not
   history; its length is a comparison against a ceiling its bindings do not
   yet carry, which is the row its next audit offers.
3. `python3 .github/scripts/verify.py` on this spec commit: exit 2 for the
   rows already owed and nothing else red; three rules `@planned`, unclaimed.
4. After the implementing change: this repository's bindings carry the row at
   the size the file is that day; the new case claims the three rules, has a
   row in `evals/README.md`, and every rule has dropped `@planned`; the pull
   request carries `minor`, `## Changelog`, `## Ids: unchanged` and the
   Gherkin block; `verify.py` exits 2 for the rows already owed plus `setup`'s
   eight, and nothing else.
5. #100 closes with what was asked, what shipped, and why they differ — and
   the comment says the gate is #98's and the remedy #99's, in that order.
