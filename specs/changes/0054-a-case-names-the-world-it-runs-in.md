# Spec 0054: a case names the world it runs in

- **Status:** approved
- **Issue:** [#123](https://github.com/sargismarkosyan/livespec/issues/123) —
  cases 08, 10 and 12 stall on an empty workspace in both arms; #38's scaffold
  was never swept across the suite. Found by reading the transcripts of the
  sitting of 2026-09-17, after [#122](https://github.com/sargismarkosyan/livespec/pull/122)
  landed its numbers.
- **Depends on:** [`0039`](0039-the-world-a-test-runs-in.md), whose lesson
  this is — the world a test runs in is part of what it measures — applied one
  layer in, to this repository's own tests; and the scaffold mechanism
  [#38](https://github.com/sargismarkosyan/livespec/issues/38) built, which
  this makes mandatory to *declare* rather than to *have*.

## Who this is for

**Nobody in the workflows, and that is correct rather than a gap** —
[`process.md`](../../method/process.md#a-technical-change-that-serves-no-workflow-is-correct-not-a-gap).
This is the repository's own pipeline: the eval suite is the test layer here,
and a test layer is not an attempt anybody makes with the product. So there is
no persona, no `.feature`, and no rule id; per
[`gates.md`](../../method/gates.md), it is held by the fault table and read
back from the bindings' record of it.

The person it serves all the same is the maintainer at step 4 of the loop, who
approves specs holding numbers this suite produced. Yesterday they paid $52.91
for 17 measurements and were told the plugin earned +0.50 on refine-personas.
It did not. That case, and at least four others, never reached the skill: the
session found an empty directory where the prompt promised a repository, and —
correctly — stopped. Both arms stopped the same way, so Δ was a comparison of
two refusals, and the score was whichever arm refused more gracefully.

**This lengthens nothing anybody types.** A case gains one line saying which
world it runs in, or a scaffold that lays that world down. What it shortens
is the reading of every number after it.

No always-promise moves. `always-green`: the suite gate is this repository's,
and it fails here rather than in any user's build.

## The job behind the request

The literal ask is #123's: scaffolds for the three cases that provably stall.
Behind it is the shape of the defect, which is not three missing files. It is
that **an empty workspace nobody chose reads exactly like one somebody chose.**
Thirteen cases were written before the scaffold mechanism existed; some of
them are genuinely self-contained — a todo report is a conversation, and a
setup run on a repository with nothing in it is the point of case 16 — and
some presuppose a branch, a ledger, a persona file. Nothing in the tree
distinguishes the two. `evalsuite.py` fails a case that *declares* a scaffold
that does not exist, with the exact words *"would run against an empty
workspace and measure the stall, not the judgment"* — and passes, silently, a
case that declares nothing and does the same thing.

The job: **every case says which world it runs in, and a case that says
nothing fails.** Then the only way to measure the stall is to write down that
you meant to.

What the transcripts showed, plugin arm, every run, sitting of 2026-09-17:

| case | prompt presupposes | what happened | the number it produced |
|---|---|---|---|
| 03-persona-to-fit-feature | a `specs/personas/` tree | refine-personas fired; *"There's no repo here"*; wrote nothing | +0.50 — read as a gain |
| 04-workflow-for-orphan | an orphan `.feature` | refine-workflows fired 2 of 3; *"I can't see the repo"*; wrote nothing | +0.00 |
| 08-fix-it-while-recording | *"Spec 0012 … on the branch"* | record-clip never fired; *"no spec 0012, no branch"* | +0.00, fired 0/3 |
| 10-gate-deferred-twice | a ledger reading *deferred since 0005* | refine-workflows never fired; *"the repo you're describing isn't here"* | −0.17, fired 0/3 |
| 12-setup-drives-the-sitting | a repository with a branch and a `CLAUDE.md` | setup fired; *"true of a repo I cannot see from here"*; every verdict: *found the directory empty and stopped* | 0.33 both arms — read as setup scoring low |
| 05-future-state-journey | workflows to draw an arc over | wrote a journey anyway in 2 of 3, noting the empty directory | +0.33, on a world it invented |

08's and 12's older measurements, from August, read the same way in every
session. The board has carried them as measurements since.

## Why now

Because the sitting just bought the evidence, and because the next sitting is
a spend: the maintainer should not pay again to measure the stall. The
cases that hold this repository's most recent work — 41 to 45 — all have
scaffolds; it is the older half of the suite that was never swept.

## The end value

Every case in `evals/` carries either a `scaffold_script:` or a line
`workspace: empty — <why the empty directory is the fixture>`, and the suite
gate fails one that carries neither, or that says *empty* and not why. The
six cases that presuppose a repository get one. The runner says, after its
table, when the skill under test never fired in the plugin arm. And the method
carries the sentence this repository just learned the expensive way.

**How we would know it worked:** a case with no declaration fails
`verify.py` naming the line it owes; the fixture's cases carry the line and
two faults prove the gate fires; the next sitting's transcripts for 03, 04,
08, 10 and 12 reach the skill instead of the directory listing.

## What changes

1. **[`caselib.py`](../../.github/scripts/caselib.py)** reads a `workspace:`
   field from `case.yaml` or the prompt's frontmatter into the case, beside
   `scaffold`. The one reader, so the gate and the runner cannot disagree
   about what a case declared.
2. **[`evalsuite.py`](../../.github/scripts/evalsuite.py)** fails a case that
   declares neither a `scaffold_script:` nor a `workspace:`, naming #123 and
   the stall; and fails `workspace: empty` with nothing after it — an empty
   directory is a decision only when its reason is written where the gate
   reads it. The existing check, a declared scaffold that does not exist,
   stays beside them.
3. **[`inject.py`](../../.github/scripts/inject.py)**: the fixture's three
   cases gain the line; two faults — *a case that declares no workspace*, *a
   case that says empty and not why* — read *fails*. The record in the
   bindings regenerates.
4. **Scaffolds** for the cases whose prompt presupposes a repository — **03,
   04, 08, 10, 12, and 05** unless its prompt reads otherwise at build — each
   laying down what its prompt names and no more, per the README's rule that a
   fixture may leave out on purpose what the case grades. 08's carries the
   branch with spec 0012 on it and the search box; 10's the ledger reading
   *deferred since 0005*; 12's the repository the two sentences describe;
   03's a persona tree; 04's the orphan feature; 05's the workflows.
5. **The other twelve** — 02, 06, 07, 09, 11, 13, 16, 18, 19, 25, 29, 33 —
   gain `workspace: empty — <why>`, each reason written after reading its
   prompt. Any found to presuppose a repository gets a scaffold instead; the
   count in item 4 is a floor.
6. **[`run.py`](../../evals/runner/run.py)** prints, after its table, one line
   per `skill:`-tagged case that is not should-not-fire whose plugin arm fired
   0 of N: *the skill under test never fired in the plugin arm; the case may
   not reach it.* A report line; the `fired` column already holds the number,
   and this makes it loud. It would have named 08 and 10 yesterday, and not 12
   — which is why the gate is the fix and this is the aid.
7. **[`evals/README.md`](../../evals/README.md)**, *When a case needs a
   repository*, gains the rule and the two forms, and #123 joins #38, #40 and
   #58 in the history of cases converted after a run showed the empty
   workspace was what got measured.
8. **[`method/testing.md`](../../method/testing.md)** gains one paragraph
   after *A test that did not run claims nothing*: **a test given no world
   tests nothing** — a behaviour test that presupposes state it was not given,
   a row, a file, a branch, a service, measures whether the assumption held
   and not whether the rule does; say what world a test runs in, and make its
   absence a failure rather than a quiet pass in both directions.
9. **This repository's bindings**: the *Case discovery* row names the
   declaration every case carries; the fault record regenerates.

**Rules added or changed: none.** The repository's own pipeline carries no
rule id; the two faults are its contract.

## What we are not doing

- **Not excluding the `workspace:` line from the measurement hash.** The hash
  is every byte in the case directory, shared by the runner and the board so
  they cannot disagree; a special case for one frontmatter line to dodge a
  bill is the kind of exception that makes two machines disagree later. A
  declaration of the world a case runs in is an input, exactly as a scaffold
  is. The cost is in *Data*, and most of it can be deferred.
- **Not refusing to count a run in which the skill never fired.** It would
  have caught 08 and 10 and missed 12, where setup fired and then stalled;
  a rule that catches the easy half teaches the reader to trust the hard half.
  The declaration is the fix; the runner's line is a pointer.
- **Not scaffolding every case.** Twelve are conversations. Forcing a fixture
  on them is one more thing to keep true for no discrimination gained; the
  README's rule stands. What they owe is the sentence, not the tree.
- **Not detecting presupposition mechanically.** A prompt that names
  `specs/` is a hint, not a proof, and a gate on hints is wallpaper. The
  declaration makes the question unavoidable; answering it is a reading, done
  once per case in this change.
- **Not re-measuring anything here.** Every run is the maintainer's to
  approve.

## Data

No storage. Files that move: `.github/scripts/caselib.py`,
`.github/scripts/evalsuite.py`, `.github/scripts/inject.py`,
`evals/runner/run.py`, `evals/README.md`, `method/testing.md`,
`specs/setup/README.md`, six case directories gaining `case.yaml` and
`scaffold.sh`, twelve prompts gaining one frontmatter line, and this spec.

**This spec commit stales nothing.** `verify.py` exits **2** for the rows
already owed and no other reason.

**The implementing change stales fresh rows, by design, and says so.** The
hash covers every byte of a case, so:

| cases | why they go stale | what it means |
|---|---|---|
| 03, 04, 05 | a scaffold lands | measured yesterday in the wrong world; the numbers were never the skill's. Re-measuring them is the point |
| 08, 12 | a scaffold lands | already stale; their August numbers were the stall too |
| 10 | a scaffold lands | a pilot at one run; never counted |
| 02, 06, 07, 09, 11, 13, 16 | one line naming the world they already ran in | the world did not move. Their numbers are still true of it, and re-measuring can wait for the next real reason to run |

Of yesterday's 15 measurements at the floor, **10 go stale**: three for real,
seven by bookkeeping. The board will read about five measured until a run
somebody pays for. At the floor of three runs, the six scaffolded cases are
about **$11** to measure for the first time in their own world; the seven
bookkeeping rows about **$13** if the maintainer wants the board clean, and
nothing if they do not. Committing on the resulting exit 2 is sanctioned, and
the commit will say which rows and which of the two reasons.

**What the pull request owes.** `method/` moves by one paragraph —
**`patch`** — a `## Changelog` section, and the run block, because it touches
`evals/` and `.github/scripts/`. No `.feature` moves; the audit surface does
not.

## Risks

- **A case's reason is written to pass the gate.** *"empty — no repo needed"*
  twelve times. The gate cannot read intent; what it can do is make the line
  exist where a reviewer sees it beside the prompt, and #123's table is what a
  reviewer compares it to. Twelve reasons written once, in one change, by one
  reader, is the cheapest this ever gets.
- **The board halves and reads as a regression.** It is the opposite: the
  numbers going stale for real were never measurements, and the board saying
  so is the board working. The commit and the pull request say it in as many
  words.
- **A scaffold answers the question the case asks.** The README's rule: a
  fixture leaves out on purpose what the case grades. 12's must not pre-write
  the bindings it grades setup on writing; 08's must not draw the picture.
- **Always-promises.** `always-green`: unchanged. `never-implements`: scripts,
  fixtures and prose. `context-budget`: no description moves.

## Acceptance checks

1. `python3 .github/scripts/inject.py`: 114 faults caught — the undeclared
   case and the unreasoned *empty* both reading *fails* — the fixture green.
2. Remove the `workspace:` line from case 02 by hand: `evalsuite.py` exits 1
   naming the line it owes and #123. Restore: green.
3. `python3 evals/runner/run.py` over yesterday's `results.json` prints the
   never-fired line for 08 and 10 and for nothing else.
4. Each of the six scaffolds lays down what its prompt names — checked by
   running it in an empty directory and reading the tree — and none of them
   what its graders grade.
5. `verify.py` exits 2, naming the ten rows and which reason each has; the
   pull request carries `patch`, `## Changelog` and the run block.
