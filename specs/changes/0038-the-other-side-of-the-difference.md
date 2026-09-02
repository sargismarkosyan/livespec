# Spec 0038: the other side of the difference

- **Status:** approved
- **Issue:** [#92](https://github.com/sargismarkosyan/livespec/issues/92)
- **Depends on:** nothing to build. It stands behind
  [`0032`](0032-the-repository-does-not-know-it-is-owed.md),
  [`0036`](0036-a-row-that-was-right-once.md) and
  [`0037`](0037-a-name-that-already-belonged.md), each of which cut the same seam
  and each of which had to ship a rule of its own to reach a repository set up
  before it. This is the mechanism those three are special cases of.

## Who this is for

[`agent-accelerated-owner`](../personas/agent-accelerated-owner.md), in
[`adopt-the-process`](../workflows/adopt-the-process.feature), at the seam the
last three changes named — **between having adopted the process and the process
moving on underneath them** — for the fourth time, and the first time as the
seam itself rather than as one thing found sitting in it.

Three persona lines decide the shape:

- **"more than one repository at once."** Every repository was set up on the
  version that existed that week, and the ledger in each records which. Nothing
  in any of them says what the method has asked for since.
- **"They read the spec layer and not the documentation."** `CHANGELOG.md` is
  documentation, and by their own account they will never open it — *"I have
  not read it. It only for AI."* So the one record of what moved is written for
  exactly the reader this change hands it to: the agent, at the audit, reading
  it so that they do not have to. [`0032`](0032-the-repository-does-not-know-it-is-owed.md)
  stated the job as *without reading a changelog to find out what moved*; this
  is the half of that sentence that says who reads it instead.
- **"A setup they did not agree to gets stopped and questioned rather than
  inherited."** What the method now asks of a repository *is* a setup they did
  not agree to — it arrived by `/plugin update`, in the skills and not in the
  record. Bringing it to them as a list of items, each saying what closes it,
  is the questioning. Leaving it in the skills is the inheriting.

**This does not lengthen adoption.** The
[workflows README](../workflows/README.md) requires a change that adds a step to
the sitting to name the later attempt it shortens; `doctor` runs after the
sitting is over, on a repository that already has the process.

## The job behind the request

To have a repository that adopted the process weeks ago be brought level with
the process as it now is — every difference named, and each one either corrected
or on the clock — without its owner knowing the method moved, and without this
plugin shipping a rule for every change in order to reach it.

## Why now

Because the audit is asked to spot a difference while holding one side of it.

[`doctor`](../../skills/doctor/SKILL.md) §1 says *start from the stamp, and read
against `gates.md` as it now stands*. `gates.md` says what the method asks now;
nothing anywhere says what it asked at the stamp. So the instruction has no
mechanism under it, and the audit either re-derives every row from scratch or
reports nothing — which is what `0036` found, and why it shipped a rule for the
one row it was about.

**Three changes in five versions have each shipped a rule of their own to reach
a repository set up before them.** `0032` for the sketch row (0.29.0). `0036` for
a demand read off a report (0.31.0). `0037` for a record naming a skill that
moved (1.0.0). Each is right, each cost a rule, a case and a session, and each
catches exactly one thing. The fourth thing is already sitting there uncaught.

**The live case**, read on 2026-09-02. `toil-tracker` is stamped *reconciled
against livespec **0.25.0** on 2026-08-30*; `main` here is **1.0.0**. Seven
entries between. Read the way this change would read them:

| Entry | What it asks of a consuming repository | `toil-tracker` today | Caught today by |
|---|---|---|---|
| 0.26.0 | nothing — a floor on this plugin's own board; the rule it adds to `graded-cases.md` reaches only a repository with graded cases, and this one has none | — | passed over |
| 0.27.0 | the loop's step 4 says what the person holds — the spec, and the sketch drawn from it | `CLAUDE.md` step 4: *"Human approves, or asks for changes"* | **nothing** |
| 0.28.0, 0.30.0 | the coverage demand is the whole of what is in scope, exclusions in the tool's own config | a ratchet at 82.37% branches, exclusions in prose — filed by that repository itself as a workaround row | `0036`'s rule |
| 0.29.0 | a sketch row beside the picture's | *sketch* appears 0 times in its bindings and 0 in its `CLAUDE.md` | `0032`'s rule |
| 0.31.0 | nothing the repository holds — it is what the audit now does, and it is the arrival that repository's workaround row names as *what would end it* | the row is waiting on it | [`0019`](0019-what-would-end-it.md)'s mechanism |
| 1.0.0 | the record names `todo` where it named `feedback` | `CLAUDE.md` step 2: `/livespec:feedback` | `0037`'s rule |

Four things owed. Three have a rule each; the fourth has none, and would have
none until somebody wrote a fifth rule for it. Six readings are recorded in that
ledger, and the sixth, dated 2026-08-31, ends *"livespec is still 0.25.0, so the
stamp is not touched"* — 0.26.0 had shipped the day before. Nothing in the audit
reads even the version installed, let alone what came with it.

**This repository's own record is behind in the same place.** Its ledger is
stamped 0.25.0, and its [`CLAUDE.md`](../../CLAUDE.md) step 4 reads *"The human
approves the spec, or asks for changes"* — the spec named, the sketch not, four
versions after the method put it there.

`0036` refused the obvious fix and gave the reason: *a generated diff between
method versions is a second copy of the method waiting to disagree with it.*
That refusal stands, and it does not reach this. [`CHANGELOG.md`](../../CHANGELOG.md)
is not generated for this purpose — it exists, the release pipeline writes it
from each pull request's `## Changelog` section verbatim
([`release.py`](../../.github/scripts/release.py)), and every install carries it
at the plugin root beside the manifest that says which version is installed.
Reading the record that shipped is not manufacturing a parallel one.

## The end value

Running `doctor` in a repository set up weeks ago comes back with everything the
method has changed since, as items — corrected where they are record, on the
clock where they are wiring — and the next change to the method reaches that
repository at its next audit without this plugin shipping a rule to carry it.

**How we would know it worked:** an audit of `toil-tracker` names `CLAUDE.md`'s
step 4, which no rule today reaches, and corrects it. And the next change here
that obliges a repository to hold something ships without a `doctor` rule of its
own — `0032`, `0036` and `0037` were the last three, and there is no fourth.

## What changes

- **`doctor` §1 reads the range.** After the stamp is read, the plugin's
  changelog — the one it ships, two levels up from the skill file, beside the
  manifest that says which version is installed — is read from the entry after
  the stamp to the entry for the version installed. **Each entry says where to
  look; `gates.md`, [`claude-md.md`](../../method/claude-md.md) and the skill as
  they now stand say what is asked.** Entries are freeform prose written for a
  person: reliable about *which skill moved*, unreliable as a checklist. An entry
  that is mostly the reasoning for a change is passed over rather than turned
  into a task, and so is one that moved nothing this repository holds — a change
  to how this plugin measures itself, a rule reaching only a kind of repository
  this is not — in a line saying so.
- **The reading directs the checks that already exist; it is not a second list.**
  §1's four questions, §2's read-back and §3's gaps are what is done where an
  entry points. A row `0036` would find is found once, under the entry that
  moved it, and not again.
- **Three degenerate ranges are said in a line.** A stamp at the version
  installed reports *nothing between to reconcile*, never an empty finding. A
  stamp ahead of the version installed — a downgrade, or a stamp somebody typed
  — is reported with both versions named and no range read. A changelog that
  cannot be reached from the session is said once, with what would read it, and
  the audit carries on with the ledger — the same rule as §2's platform that
  cannot be reached, and
  [the same one](../../method/process.md#a-step-you-cannot-take-here-is-said-once-not-searched-for)
  every other skill here follows.
- **What the reading finds is corrected where it is record and becomes a row
  where it is wiring.** The record is the bindings **and `CLAUDE.md`** — the
  maintainer's instruction on this change is that *`doctor` or `setup` can and
  must update `CLAUDE.md` if needed*, which settles what `0032` left out and
  `0037` half let in. A loop step that changed reads as it now should, in place,
  and is never handed back as a line for `setup` to write. **A skill that was
  renamed is corrected everywhere the record instructs by its old name**, in
  `CLAUDE.md` and in the bindings alike; a dated account of what once ran under
  that name is left as written. Wiring the method now asks for and the repository
  lacks becomes a *deferred* row naming the change it has been deferred since and
  the version of the method that moved it — so it is on the two-change clock, and
  the fact survives the next reading. The report's last line names `setup` with
  those rows.
- **The stamp does not move.** `doctor` §4's rule stands as written: the stamp
  follows the wiring, and a reading that corrected the record and wrote the rows
  leaves it where it was. What that costs is in *The three decisions* below.
- **`gates.md` carries the portable half**, beside the sentence that already says
  what the stamp is for: what changed between the stamp and the version installed
  is read from the record the plugin ships with each version, never regenerated
  from the method; and that record is where to look rather than what to do.
- **The record the reading depends on is held to its shape here.** Every
  version already reaches `CHANGELOG.md`: `version_gate.py` fails a shipping
  change with no `## Changelog` section or an empty one, `release.py` writes the
  entry under `## <version> — <date>` and refuses a version that already has
  one, and since [`0034`](0034-a-release-that-did-not-happen-is-still-owed.md)
  it reads from the last release tag, so a failed run strands nothing. All of
  that is inject-proven. **What nothing holds is the shape the audit reads
  by** — that the file is at the plugin root, that every heading parses as a
  release and a date, and that the manifest's `version` has an entry.
  `checks.py` gains that check, reading the file through `releaselib.py`, the
  one reader the gate and the release job already share; `inject.py` gains two
  faults so it is proven to fire — a heading the reader cannot parse, and a
  manifest version with no entry — and both land in *The fault injection
  record* the bindings generate from the injector. The release job runs
  `verify.py --local` after writing both files, so the check holds there too.
  **What cannot be gated from here is that the cache carries the file.** That is
  the packaging's, so it is recorded in the bindings as an observation with its
  date and path — `~/.claude/plugins/cache/livespec/livespec/0.27.0/` holds
  `CHANGELOG.md`, read 2026-09-02 — beside the skill's own fallback, that the
  file is two levels up from the skill file, and the *cannot be reached* rule
  for the session where it is not.
- **`spec.md` gains the word.** *stamp* was used in the skill, two feature files
  and every ledger and defined nowhere; it joins the vocabulary with what moves
  it, the `CHANGELOG.md` line under *What a version leaves behind* says what the
  file is now also for, and the gloss on the stamp — *what was this last checked
  against* — becomes *what is this wiring level with*, so the prose agrees with
  the rule. **Done in this spec commit**, as the prose half of the same decision.

**Rules added or changed** — the `@rule:` ids in `specs/features/`:

| Rule id | Feature file | New or changed |
|---|---|---|
| `the-entries-between-are-where-to-look` | `features/wiring/what-changed-since-the-stamp.feature` | new, `@planned` |
| `a-range-with-nothing-in-it-is-said-not-computed` | `features/wiring/what-changed-since-the-stamp.feature` | new, `@planned` |
| `a-reading-leaves-the-stamp-where-it-was` | `features/wiring/what-changed-since-the-stamp.feature` | new, `@planned @refusal` |
| `what-the-reading-finds-is-corrected-as-record-or-written-as-a-row` | `features/wiring/what-changed-since-the-stamp.feature` | new, `@planned` |

A new file rather than four more rules in
[`wiring/what-an-audit-reads.feature`](../features/wiring/what-an-audit-reads.feature):
that one is at 3 of its 6 rules and 75 of its 120 lines, and four more would put
it past both. It is about *what an audit reads and against which version*; this
is about *what it reads for between two versions*.

**No description changes, so no should-not-fire case is owed.** `doctor`'s
description already carries *"to say whether the process still holds here"*,
which is this question exactly. `context-budget` stays at 4321 of 5000.

### The three decisions, and who made them

The issue put a boundary question in front of any Gherkin. It was asked, with
two more, before this was written.

- **Who applies what the reading finds.** The maintainer was indifferent between
  `doctor` and `setup`. What decided it is that only one of the three shapes on
  the table rewrites no promise: `doctor` corrects the record and writes the
  rows, which is what it has done since
  [`0021`](0021-asked-not-assumed.md); `setup` wires, which is what it has done
  since 0.4.0, and its §5 already reads a ledger's deferred rows and offers to
  wire them. The cost is a second invocation, paid only when wiring is owed, by
  somebody already holding the audit's output that says so.
- **Whether a reading moves the stamp.** Recommended: yes, once every entry's
  obligation is a correction or a row. **Chosen: no** — the stamp follows the
  wiring, as `doctor` §4 and [`setup`](../../skills/setup/SKILL.md) §5 already
  say and as `toil-tracker` has practised through six readings. The cost,
  accepted in the open: **the range never shrinks by reading.** Every audit of a
  repository whose wiring is behind re-reads the same entries until `setup`
  brings the wiring level, and a repository whose owed items were all record
  corrections stays stamped behind after they are made. The rule is pinned
  `@refusal`, so that a session in a hurry does not re-stamp for having looked.
- **Whether `CLAUDE.md` is corrected in place.** Yes — *"`doctor` or `setup`
  skills can and must update `CLAUDE.md` files if needed"*, in the maintainer's
  words, with one addition of theirs: a renamed skill is corrected in every
  repository's record that instructs by it, wherever that record names it.
  Bounded by the reading rather than by a file: `doctor` corrects what the range
  moved and what its own checks reach, and does not run `setup` §6's
  requirement-by-requirement audit of the whole file.

## What we are not doing

- **Not moving the stamp for a reading.** Above. Named again here because it is
  the alternative most likely to be relitigated, and the prose that used to
  invite it — *last checked against* — is corrected in this commit.
- **Not wiring anything from `doctor`.** Its first refusal is *"Wiring
  anything"*, `0021` and `0036` argued it, and the maintainer did not ask for it
  to move. A skill that both grades and repairs has no way to be wrong out loud.
- **Not a ninth skill.** It would cost its description in every session forever,
  against `context-budget`, and need a should-not-fire case of its own, to do
  what an existing description already covers.
- **Not editing `setup`.** [`0019`](0019-what-would-end-it.md) left `setup`'s
  ledger-diff alone on purpose — *one skill, the one with the transcript* — and
  the join here needs no edit: a deferred row is what `setup` §5 already reads
  and offers to wire. A line telling it to start from the rows an audit wrote
  would say what the ledger already says, and stale ten cases to say it.
- **Not generating a diff of the method, and not a machine-readable changelog.**
  `0036`'s refusal stands. The changelog is read as it is written, for a person,
  and the method and the skill are read for what is actually asked. An
  obligations list generated per version is the second copy of the method that
  refusal was about.
- **Not retiring `0032`'s, `0036`'s or `0037`'s rules.** Each holds when the
  changelog cannot be reached, each is cheaper than a reading, and the reading
  directs them rather than replacing them. What changes is that the *next* one
  does not need writing.
- **Not reading the changelog as a checklist.** Held by its own example, because
  it is the failure this will produce on the first entry that is mostly
  rationale — 0.25.0's is three paragraphs on what *depends on* means, and asks
  nothing of anyone.
- **Not rewriting dated prose.** A reading dated 2026-08-30 that says
  `/livespec:doctor` ran is history, and a record edited to agree with the
  present is not a record. What gets corrected is an instruction, not an account.
- **Not backfilling `toil-tracker` by hand**, and **not making anybody run the
  audit.** The same two limits `0036` recorded; nothing here fires unasked.
- **Not gating that the cache carries the file.** It cannot be, from inside
  this repository — packaging is Claude Code's — so it is observed and recorded
  in the bindings with the date and the path, the way *What loads here* already
  records what a session was seen to load, and the shape of the file is what
  the gate holds instead.

## Data

No storage contract here, and none in a consuming repository is touched. What
this writes in a consuming repository is the **record** — rows in its ledger,
and its `CLAUDE.md` where the method moved what that file must carry — and never
its stamp, its config or its CI. The plugin's own `CHANGELOG.md` and manifest
are read and never written.

**This spec commit stales nothing.** It writes one feature file whose rules are
`@planned` and claimed by nobody, edits `spec.md`, which no measurement hashes,
and this file. `verify.py` exits **2** on it, as it does on `main` today, for
the same 22 rows and no other reason.

**The implementing change adds no stale row.** The board today reads *0
measured, 22 stale, 6 below the floor, 7 never measured*: every case that holds
`doctor` — `24`, `25`, `28` measured; `32`, `34`, `35` never — is already owed,
so editing its body moves nothing that is not already red. What it adds is the
new cases: one fixture with a stamp behind and several obligations in its range,
expected to claim three of the four rules, and one for the degenerate ranges —
roughly **$1.80 each at the floor**. Which of the 22 are worth re-measuring is
the maintainer's spend to approve; the commit and the pull request finish with a
gap where the numbers go.

**The guardrail adds no case.** A gate script is unit here — *The substitution*
in the bindings puts `.github/scripts/` under `inject.py` rather than under a
rule — and the two faults are the whole of its proof.

## Risks

- **An entry read as a task list.** The likeliest failure, and it produces
  confident nonsense: a repository told to do something the method does not ask,
  because a paragraph of rationale mentioned it. The rule says the entry is where
  to look and the method is what is asked, and the rationale-heavy entry is an
  example rather than a sentence, because a sentence is what a session in a hurry
  reads past.
- **The audit gets longer with the plugin's age.** The range is read every time
  until the wiring is brought level — the stamp decision, taken in the open.
  Bounded by the releases since the stamp, and it shrinks the moment `setup`
  wires what is deferred; a repository that never does stays on the long audit,
  and it is the same repository that would otherwise stay silently behind.
- **A case whose fixture grows with every release.** A case for this reads the
  live changelog, so its range gains an entry per release. Its graders assert
  what the reading finds and the decoys it leaves alone, never that nothing else
  is reported; and the *nothing between* example needs a fixture stamped at
  whatever is installed, which the scaffold cannot know on its own. How the
  runner tells it is the implementing change's to settle.
- **`never-implements`, and `doctor`'s own boundary, in the most tempting form
  yet.** The audit will be holding the entry that says exactly what to wire, the
  file, and the line. Held by the fourth rule's last example, the way `0036` held
  the threshold.
- **The changelog is not where the skill expects it, or not in the shape it
  reads by.** Three guards, one per way it can go: the shape is a gate here,
  inject-proven, so a heading the reader cannot parse or a manifest version
  with no entry never reaches `main`; that the cache carries the file is not
  gateable from here and is recorded as an observation, dated — every install
  shape seen keeps the root files, and a directory marketplace is the working
  tree itself; and a local `.claude/skills/` copy shadowing the plugin has no
  changelog beside it, which is the case the *cannot be reached* example is for.
  Said once, and the ledger is audited without it.
- **`always-green` is not at risk.** Nothing here runs in anybody's build.
  **`context-budget` is untouched** — no description moves.

## Acceptance checks

There is no app; this repository's deliverable is the pull request description.
What is checked by hand:

1. Run `doctor` in `toil-tracker`. The open list names all four items above —
   including `CLAUDE.md`'s step 4, which no rule today reaches — each under the
   entry that moved it; 0.26.0 and 0.31.0 are passed over in a line each; step 2
   and step 4 are corrected in `CLAUDE.md`; the coverage row reads *deferred*
   naming 0.28.0; `vitest.config.ts` is unmodified; the stamp still reads
   0.25.0; the last line names `setup` with that row.
2. Run it again, after the first run's corrections. Nothing new is reported, the
   stamp is still 0.25.0, and the deferred row is on the clock.
3. Run it in a repository stamped at the version installed. It reports *nothing
   between to reconcile* and audits the ledger as before.
4. Stamp a fixture at a version ahead of the plugin. Both versions are named; no
   range is read.
5. Run it where the changelog cannot be reached — a copy of the skill with
   nothing two levels up. It says so once, and the rest of the audit arrives.
6. Run it against this repository's own bindings. At `a9dc9bb`, before the
   implementing change, they were stamped 0.25.0 and this `CLAUDE.md`'s step 4
   named the spec and not the sketch: the reading finds that line and nothing
   else, the sketch row being present here. The implementing change corrected
   the line and re-stamped, because `checks.py` gained a check; after it the
   audit reports *nothing between to reconcile*.
7. `python3 .github/scripts/verify.py` — exit 2 on this spec commit for the 22
   rows already owed, and nothing else red. All four rules drop `@planned` in
   the implementing change, each claimed by a case tagged `rule:<id>`.
8. Break the record by hand, on a throwaway branch: strip the date from the
   newest heading, or bump `version` in the manifest without an entry.
   `verify.py` exits **1** naming the check, and `inject.py` reports both faults
   firing on every ordinary run.
