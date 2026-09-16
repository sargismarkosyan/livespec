# Spec 0048: the file every session reads first

- **Status:** proposed
- **Issue:** [#98](https://github.com/sargismarkosyan/livespec/issues/98) —
  the second of three split from the CLAUDE.md report of 2026-09-15, after
  [`0046`](0046-a-number-and-no-file-to-copy.md) settled the number it reads
  and before [#99](https://github.com/sargismarkosyan/livespec/issues/99), the
  remedy.
- **Depends on:** [`0046`](0046-a-number-and-no-file-to-copy.md), for the
  ceiling row in the bindings — this spec is written on its branch and builds
  once it has merged. Beside [`0039`](0039-the-world-a-test-runs-in.md), whose
  shape it borrows: a check folded into the traceability gate rather than a
  third gate, with ids, ledger rows and faults; and
  [`0047`](0047-a-warning-that-has-never-fired.md), which proved the soft
  limits in the same script the day before.

## Who this is for

[`agent-accelerated-owner`](../personas/agent-accelerated-owner.md), in
[`adopt-the-process`](../workflows/adopt-the-process.feature), at the sitting
that wires the gates and at every change after it. The persona's two lines that
decide the shape are the ones [`0039`](0039-the-world-a-test-runs-in.md) stood
on: *"checking the result by reading is not available"* — the person does not
open CLAUDE.md, ever; the agent does, first, every session — and *"fix the
pipeline error, not bypass"* — so the answer arrives as a gate that fails,
which is the form this person acts on, and not as a skill that reviews.

**This lengthens the sitting by nothing anybody types.** No question is added;
section 4 writes a few more lines into the gate script it already writes, and
section 5's ledger gains two rows the template already carries. What it
shortens is every change after: today a change that guts CLAUDE.md, or grows it
into a copy of the method, reaches `main` with every check green, and the
first thing that notices is the next session behaving strangely. After this,
the build notices.

Two always-promises are touched and held. **`gates-are-proven`**: seven faults
prove the new checks fire, in this repository's injector and in the method's
table for every sitting. **`always-green`**: the gate is the consuming
repository's, written by `setup` into its own script the way every gate is,
and this plugin still cannot fail anybody's build.

## The job behind the request

The literal ask: *"Be very strict with CLAUDE.md files … add a separate strict
gate for it, and make sure that it follows your structure and has everything
that you want him to have."*

The job: **the file every session reads first should be held the way rules,
cases and ledger rows are held — by something that fails, not by a judgment
exercised once.** [#98](https://github.com/sargismarkosyan/livespec/issues/98)
showed the gap in one command: replace this repository's CLAUDE.md with three
lines and run verification, and the output is byte-identical. Nine of the ten
requirements gone, and nothing moves. Today CLAUDE.md is the one artefact in
the method whose entire enforcement is `setup` §6 at adoption and
`check:loop-per-claude-md` at an audit somebody remembers to run.

What is *strict* here has to be split, because the ten requirements are two
kinds. A script can read a size against a number, count the steps in a list,
see that a fenced block exists and that a link resolves. Only a mind can read
that a pointer is stale, that a paragraph is a copy of what the plugin already
says, that a rule is aspirational. The first kind gates. The second stays with
the sitting and the audit, and the gate says so rather than pretending.

## Why now

Because [`0046`](0046-a-number-and-no-file-to-copy.md) put the number in the
bindings and wrote, in this repository's own row, *nothing reads it yet*. A
number nothing reads is a sentence, and the reason it was written was this
gate. And because the report that asked for it is a day old, its three issues
are open, and the one thing the maintainer asked for in as many words —
*a separate strict gate* — is the one not yet delivered.

## The end value

A CLAUDE.md that is gutted, grown past its number, or left without its loop,
its commands or its pointer to the bindings fails the build in the repository
it belongs to, naming what is wrong. What a script cannot decide is left alone,
out loud. The row that said *nothing reads it yet* reads `trace.py`.

**How we would know it worked:** #98's own reproduction — three lines in place
of this repository's CLAUDE.md — fails verification naming three absences,
where today it changes nothing; this repository's real file passes on day one
without an edit; and `toil-tracker`'s next audit offers two rows it did not
have, reading *deferred*, with the sitting that wires them named last.

## What changes

1. **[`gates.md`](../../method/gates.md) gains a subsection after *The
   boundaries*: *The file every session reads first*.** It says what the gate
   reads, and only that: the file is at the root; its size is within the
   ceiling the bindings name, and a context file with no ceiling row fails
   rather than passing unmeasured; it carries the loop as a numbered list of
   at most eight steps; it carries a block of commands; it carries a link to
   the bindings that resolves. And what it does not read: prose. A failure
   table, the same shape as the boundaries'. **It is the traceability gate
   that reads it, not a third one** — the same script that reads the spec
   layer for its shape reads the file that points at it, and a third gate
   renames *both gates* in every ledger, every injector and every bindings
   file already written. The *Both gates are verified to fire* table gains
   seven rows. The id table gains two gate rows, `since: next`:

   | id | severity | meaning |
   |---|---|---|
   | `gate:context-file-ceiling` | wiring | the context file larger than the ceiling the bindings name, or a context file with no ceiling row, fails |
   | `gate:context-file-shape` | wiring | the context file missing, or without its loop, its commands, or its pointer to the bindings, fails |

2. **`trace.py` here reads the file.** From the root it already takes: the
   ceiling from the bindings' **CLAUDE.md ceiling** row, in lines; the longest
   numbered run outside fenced blocks, which must be between one and eight;
   at least one fenced block; a relative link to `specs/setup/README.md` that
   resolves. Each failure names what it found — *141 lines against a ceiling
   of 138*, *no numbered list*, *a list of nine steps*, *no link to the
   bindings*. Nothing in it warns.
3. **`inject.py`.** The fixture gains a CLAUDE.md that meets the shape, and
   its bindings gain the ceiling row at that file's size, so the green fixture
   stays green. Seven faults, all against `trace.py`, all *fails*: a context
   file past its ceiling; a context file with no ceiling row; no context file
   at the root; a context file with no numbered list; a loop of nine steps; a
   context file with no fenced block; a context file that does not link to
   the bindings.
4. **[`tools/doctor.py`](../../tools/doctor.py)'s registry** gains the two
   gate rows, so `checks.py` finds the tool and the table one list. Nothing
   else in the tool moves: `check:row-per-gate` already reports a gate the
   table names and a ledger lacks, which is how a consuming repository learns
   of these — the way it learned of the boundary gates.
5. **[`templates/bindings.md`](../../templates/bindings.md)** gains the two
   ledger rows.
6. **[`setup`](../../skills/setup/SKILL.md) §4** gains one bullet in the
   traceability list — *then the file that points at all of it* — naming the
   five things the gate reads and the one thing it does not. §6's sentence
   from `0046` gains a clause: the gate wired in section 4 reads that number
   from here on, so the file the sitting leaves must pass it before the
   hand-back.
7. **This repository's bindings.** Two ledger rows, *automated*, `trace.py`;
   the ceiling row's *nothing reads it yet* becomes *read by `trace.py` since
   0048*; the fault record regenerates; *What proves a rule* names the
   ordinary tests for the context-file checks in `trace.py` beside those for
   `tools/doctor.py`.
8. **A test file and a case.** `tests/test_context_file.py` runs `trace.py`
   against fixtures and claims the first three rules — the gate is code, and
   code is proved the ordinary way. Case `42`, `setup` in an occupied
   repository whose CLAUDE.md is a title, a test command and a branch
   convention, claims the fourth: the gate script the sitting writes reads
   the file, the fault record lists its faults, and the file left behind
   passes.

**Rules added or changed** — the `@rule:` ids in `specs/features/`:

| Rule id | Feature file | New or changed |
|---|---|---|
| `a-context-file-past-its-ceiling-fails-the-build` | `features/wiring/context-file.feature` | new, `@planned` — proved by a test |
| `a-context-file-without-its-shape-fails-the-build` | `features/wiring/context-file.feature` | new, `@planned` — proved by a test |
| `what-only-a-mind-can-read-is-left-to-the-sitting` | `features/wiring/context-file.feature` | new, `@planned @refusal` — proved by a test asserting a pass |
| `the-sitting-wires-the-context-file-check` | `features/wiring/context-file.feature` | new, `@planned` — claimed by case 42 |

A new file under `wiring/` rather than rows in
[`setup/context-file.feature`](../features/setup/context-file.feature): that
file is what the sitting holds the file to by reading it, this is what the
build refuses, and the two are held apart the way `setup` and the gate are.

**No description changes, so no should-not-fire case is owed.** `setup`'s
description already carries *wire the two gates in that project's own
language*. `context-budget` stays at 4321 of 5000.

## What we are not doing

- **Not gating the ten requirements as sections.** The method has no headings
  to look for, on purpose — a file assembled from prescribed headings is the
  template `claude-md.md` refuses to be. What a script can see of the ten is
  the loop, the commands and the pointer; the rest is read by a mind.
- **Not gating skill names or the link to the plugin in a consuming
  repository.** Its CI has no plugin installed, so a gate there cannot know
  which skills exist; that stays `check:skill-names`, an audit's. The link to
  the plugin is one URL among any, and a check for *some external link* would
  pass anything. Both stay with the sitting and the audit.
- **Not gating every relative link.** This repository's `checks.py` already
  resolves every link in every markdown file here; the method asks a consuming
  repository's gate for the one link that matters, the pointer to the
  bindings, and leaves general link-checking to whatever that repository
  already has.
- **Not a third gate.** Above. And not a warning: a check that warns about the
  file every session reads first is the wallpaper the gates page names.
- **Not reading `.claude/CLAUDE.md`.** The method's *Where it goes* puts the
  file at the root and calls the other location legitimate but exceptional; a
  repository that keeps it there says so in its bindings and its gate reads
  there. Here, the root.
- **Not the remedy.** A file that fails the shape is fixed by the sitting;
  whether it is patched or rewritten is #99.

## Data

No storage. Files that move: `method/gates.md`, `.github/scripts/trace.py`,
`.github/scripts/inject.py`, `tools/doctor.py`, `templates/bindings.md`,
`skills/setup/SKILL.md`, `specs/setup/README.md`, one new `.feature`, one new
test file, one new case, `evals/README.md`, and this spec.

**This spec commit stales nothing.** Four rules, `@planned`, claimed by nobody;
no skill moves. `verify.py` exits **2** on it for the rows already owed and no
other reason.

**The implementing change adds no stale row that is not already red.** It
edits `setup`'s body; every measured case holding `setup` is already owed. It
adds one case, numbered next, at about **$1.80 at the floor**, never measured
until the maintainer approves a run.

**What the pull request owes.** `method/`, `templates/`, `tools/` and a skill
move — **`minor`**, a gate the sitting now wires — a `## Changelog` section
that says where to look, a Gherkin block for the `.feature`, and, the audit
surface having moved, an `## Ids` section: *added `gate:context-file-ceiling`,
`gate:context-file-shape`*. The release writes the two `since` values.

**Day one here:** this repository's CLAUDE.md is 138 lines against a ceiling of
138, carries one numbered run of eight, two fenced blocks and two links to the
bindings. It passes without an edit. The ceiling stays at 138: this change
adds no line to it.

## Risks

- **A numbered list that is not the loop.** The check is on the longest run
  of consecutive numbers outside fenced blocks: a short list elsewhere is
  harmless, and a nine-item list that is not the loop fails a file the method
  already says should be about a hundred lines of pointers. The failure names
  the list, so the fix is a minute.
- **A repository that updated the plugin and never re-ran the sitting.** Its
  gate script is the one it has; nothing fails there until the sitting wires
  the check, and until then its audit offers two *deferred* rows — the same
  path the boundary gates took.
- **A consuming repository whose CLAUDE.md lives under `.claude/`.** Its
  sitting writes the path into the bindings and reads it there; the method's
  default is the root. Named above.
- **The gate becomes a template by the back door.** It asks for a numbered
  list, a fenced block and one link — the three things every CLAUDE.md the
  method has ever asked for already has — and nothing about their words or
  their order. The refusal rule holds the line, with a test asserting a pass.
- **`never-implements`**: untouched, a gate script and prose.
  **`ids-are-permanent`**: two ids added, none renamed.

## Acceptance checks

1. `python3 .github/scripts/inject.py`: 103 faults caught, the seven new ones
   reading *fails*, the fixture green without them.
2. `printf '# livespec\n\nA thing.\n' > CLAUDE.md; python3 .github/scripts/trace.py` —
   exit 1 naming the loop, the commands and the pointer to the bindings; then
   `git checkout -- CLAUDE.md` and it passes. #98's own reproduction, inverted.
3. `python3 .github/scripts/tests.py`: green, the new file's tests each naming
   a rule.
4. `python3 .github/scripts/checks.py`: the tool and the table one list, the
   two new ids in both, `since` reading `next` until the release.
5. `cd ~/Projects/toil-tracker && python3 ~/Projects/livespec/tools/doctor.py specs/setup/README.md`:
   `check:row-per-gate` reads open, naming the two gates its ledger lacks.
6. `verify.py` exits 2 for the rows already owed; the pull request carries
   `minor`, `## Changelog`, `## Ids` with the two ids added, and the Gherkin
   block.
