# Spec 0052: the run beside the claim

- **Status:** approved
- **Issue:** none — spec C of the plan *Green Means Real* (2026-09-08), the
  third of four, in the order the maintainer set; A shipped as
  [`0039`](0039-the-world-a-test-runs-in.md) and B as
  [`0051`](0051-a-test-that-did-not-run-claims-nothing.md).
- **Depends on:** `0039`, for the boundary rows the picture names; `0051`, so
  that the run this quotes is one in which every rule-bound test ran; and
  [`0021`](0021-asked-not-assumed.md), which built the second table this
  adds a row to and the report this makes say more.

## Who this is for

[`agent-accelerated-owner`](../personas/agent-accelerated-owner.md), in
[`adopt-the-process`](../workflows/adopt-the-process.feature), at the pull
request — the one step of the loop where the person decides on a change that
exists and is asked to believe a sentence about it. The persona line is the
one every spec in this plan stands on: *"checking the result by reading is
not available"*. What they read instead is the pull request, and today the
pull request's account of its own verification is whatever the author typed:
a bullet saying the tests pass, a count, a summary line. Every fabricated
result the research deck found was a summary; none was a transcript.

**This lengthens nothing anybody types by more than a paste.** The run the
author already made goes into the body under the command as the bindings name
it. What it shortens is the reading: the reviewer sees the author's run and
the pipeline's own, side by side, in the place they are already looking, and a
claim that disagrees with the pipeline disagrees in public.

No always-promise moves. **`always-green`** is the one this comes closest to:
the report gains a section and gains no way to fail, and the presence check
sits in the pull-request gate this repository already has, which is a
property of a pull request and never of a user's build.

## The job behind the request

The literal ask is the plan's: *"The pull request carries the command, its
output and the state read back; the report prints its own run next to it; the
picture says which world it was served from."* Behind it, the deck's
mechanisms: *done, ready to test* without a run; a body quoting *162 passed*
when the exporters never wrote a file; a picture of an app on a stub, read as
a picture of the app.

The job: **the claim a pull request makes about its own verification should be
the run, not a description of the run — and the pipeline's own run should sit
beside it where the reviewer looks.** Today a pull request here owes a label,
a changelog entry, the Gherkin it moved and an `## Ids` section, and the gate
checks each is present. What it says about verification is free prose; this
repository's own recent pull requests said *106/106* and *66 run of 66 held*
in bullets, true and unverifiable from the page. The report beneath them
prints the spec layer's counts and the board's, and nothing about the run
that just happened above it.

The third piece is the picture. `record-clip` reports the form a picture took
and why; it says nothing about the world the app was served over when it was
taken, and a clip over an in-memory store looks exactly like a clip over the
store. Since `0039` the bindings name that world in rows; the hand-back can
name the rows.

## Why now

Because it is the next item in the maintainer's order, and because `0051`
just made the run worth quoting: a green run now means every rule-bound test
ran, so a run block is a claim with something behind it.

## The end value

A pull request that changes the tests, or what runs them, carries the run:
the verification command as the bindings name it and the runner's output
under it. One that carries none, or quotes some other command, cannot merge.
The report prints the pipeline's own tail beside the block, and gates on
nothing, including the two disagreeing. A version's picture arrives with the
world it was taken in named.

**How we would know it worked:** this pull request is the first to carry the
block, and its report is the first to print the pipeline's run beside it; a
body that says the tests pass and quotes nothing is refused by the same gate
that refuses a missing Gherkin block; and a `record-clip` hand-back names the
boundary rows before it names the frames.

## What changes

1. **[`repository.md`](../../method/repository.md) gains a subsection after
   *And the Gherkin it moved*: *And the run it rests on*.** A pull request
   that claims green carries the run — the verification command as the
   bindings name it, its output as the runner printed it, and, for a change
   crossing a boundary, the state read back afterwards. Not a summary. The
   report reads the same command's output from its own run and prints it
   beside the block; it never gates on the difference, and what it does is
   make the difference visible. What a gate can prove is that the block is
   there and opens with the command the bindings name — the same check the
   Gherkin block gets, for the same reason.
2. **[`gates.md`](../../method/gates.md).** *The report is not a gate* gains
   the paragraph that the report carries its own run beside the claim. *The
   wiring that must never gate* gains a row: the run beside the claim,
   *unobserved* until somebody has watched the two disagree. The id table
   gains two rows, `since: next`:

   | id | kind | severity | meaning |
   |---|---|---|---|
   | `wiring:run-beside-claim` | wiring | wiring | the report re-running the verification command and printing what it saw beside what the body says — unobserved until the two were watched disagreeing |
   | `check:run-row` | mechanical | wiring | the second table holds the row for the run beside the claim |

3. **This repository's pull-request gate.** `releaselib` gains
   `extract_run(body, command)`: a fenced block whose first line is the
   verification command as the bindings name it, with output beneath; absent,
   empty, or opening with a different command is refused with a message that
   says what the block is and where the command is named. `version_gate.py`
   asks for it when the change touches the tests or what runs them — `tests/`,
   `evals/`, `.github/scripts/` — the way it asks for Gherkin when the change
   touches a `.feature`, reading the command from the bindings' *Verification*
   row. Three release faults hold it; the control shows a good block read.
4. **The report.** The `Verify` step keeps its output; the workflow hands
   `report.py` that file and the pull request's body; the report gains a
   section, *The run*, with the body's block on one side and the last lines
   of the pipeline's run on the other, or a line saying which of the two it
   could not read. Nothing in it can exit non-zero, as before.
5. **[`tools/doctor.py`](../../tools/doctor.py)** gains `check:run-row` — the
   second table holds the run's row — the same shape as the report's and the
   measure's checks, with a fault that removes the row; the registry gains
   both ids. **[`templates/bindings.md`](../../templates/bindings.md)** gains
   the row and the *owes a release* placeholder names the run.
6. **[`record-clip`](../../skills/record-clip/SKILL.md)** gains a rule beside
   *the form is reported*: so is the world — the boundary rows the app was
   served over, named in the same breath, because a picture over a stand-in
   is a picture of the stand-in. **[`setup`](../../skills/setup/SKILL.md)** §5:
   the *owes a release* row names the run block, and the second table its
   row; where the repository's pull requests cannot carry a comment, the
   report half reads as not wired, as it already does. **[`doctor`](../../skills/doctor/SKILL.md)** §1:
   the run row is *unobserved* until the two were watched disagreeing.
7. **This repository's bindings**: the second table's new row, the *owes a
   release* row naming the block, the fault record regenerated.
8. **Three rules**, `@planned`; **tests** claiming the first two by running
   the reader and the report over bodies and runs; **case 23** gains a grader
   claiming the first — the bindings row it writes names the run block — and
   **case 08** gains one claiming the third — the hand-back names the world
   before the frames. Two re-runs, no new case.

**Rules added or changed** — the `@rule:` ids in `specs/features/`:

| Rule id | Feature file | New or changed |
|---|---|---|
| `a-claim-of-green-carries-the-run` | `features/showing/the-run-it-rests-on.feature` | new, `@planned` — tests and case 23 |
| `the-report-prints-its-own-run-beside-the-claim` | `features/showing/the-run-it-rests-on.feature` | new, `@planned` — tests |
| `the-picture-names-its-world` | `features/showing/the-run-it-rests-on.feature` | new, `@planned` — case 08 |

**No description changes, so no should-not-fire case is owed.**
`record-clip`'s description already says *record the picture a version ships
with*; `setup`'s and `doctor`'s are untouched. `context-budget` stays at 4321
of 5000.

## What we are not doing

- **Not checking that the pasted output is real.** The gate proves the block
  is there and opens with the right command; the report puts the pipeline's
  run beside it so the reading is cheap. A gate on the difference would be a
  gate that fails a build for a wording change in a log line.
- **Not the two measures the plan lists beside this.** Assertions per
  rule-bound test reported beside the coverage split, and the rule-bound
  snapshots a change rewrote named beside the run, are a different mechanism
  — reading the tests, not the pull request — and get their own spec after
  this one.
- **Not gating on a change to the method.** A page of prose owes a label and
  an entry; it does not owe a run block, because a run block for a change the
  verification does not read is ceremony, which is the thing that gets
  skipped on the pull request that needed it.
- **Not reading the state back mechanically.** For a change crossing a
  boundary the method asks for the state read back — the row, the file, the
  reply — as part of the block; what that is depends on the boundary, and it
  is a reading.

## Data

No storage. Files that move: `method/repository.md`, `method/gates.md`,
`.github/scripts/releaselib.py`, `.github/scripts/version_gate.py`,
`.github/scripts/report.py`, `.github/workflows/checks.yml`,
`.github/scripts/inject.py`, `tools/doctor.py`, `templates/bindings.md`,
`skills/record-clip/SKILL.md`, `skills/setup/SKILL.md`,
`skills/doctor/SKILL.md`, `specs/setup/README.md`, one new `.feature`, one new
test file, `evals/08-fix-it-while-recording/`,
`evals/23-what-a-change-here-must-show/`, `evals/README.md`, and this spec.

**This spec commit stales nothing.** Three rules, `@planned`, claimed by
nobody. `verify.py` exits **2** for the rows already owed and no other
reason.

**The implementing change adds no stale row that is not already red.** It
edits three skill bodies and two cases, all already owed; it adds no case.

**What the pull request owes.** `method/`, `templates/`, `tools/` and skills
move — **`minor`** — a `## Changelog` section, a Gherkin block for the new
`.feature`, an `## Ids` section — *added `wiring:run-beside-claim`,
`check:run-row`* — and, for the first time, **the run block**: this change
touches the tests and what runs them, so its own gate asks it for one.

## Risks

- **The block becomes a paste nobody reads.** The report prints the
  pipeline's run beside it; the two are read together or not at all, and a
  body that disagrees with the pipeline disagrees on the page.
- **The local run and the pipeline's differ by design.** Here a person runs
  the whole of verification and the required check runs `--local`; the tails
  differ in one line, the board. The report says which run it prints, and the
  difference is the point rather than a defect.
- **A consuming repository whose pull requests cannot carry a report.** The
  row reads *not applicable* with the reason, as the report's own row already
  does there; the block in the body still stands.
- **Always-promises.** `always-green`: the report gains no exit but zero.
  `ids-are-permanent`: two ids added, none renamed. `never-implements`:
  scripts, workflow and prose.

## Acceptance checks

1. `python3 .github/scripts/inject.py`: 110 faults caught — three release
   faults and one doctor fault new — the fixture and the release inputs green.
2. This pull request's body carries the block; its report prints *The run*
   with the block beside the pipeline's tail; a draft body with the block
   removed is refused by the release-inputs job naming the block.
3. `tests.py`: green, the new file's tests each naming a rule.
4. `checks.py`: the tool and the table one list, the two new ids in both.
5. `verify.py` exits 2 for the rows already owed; the pull request carries
   `minor`, `## Changelog`, `## Ids` with the two ids, the Gherkin block and
   the run block.
