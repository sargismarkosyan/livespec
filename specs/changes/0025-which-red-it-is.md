# Spec 0025: which red it is

- **Status:** approved
- **Issue:** [#65](https://github.com/sargismarkosyan/livespec/issues/65)
- **Depends on:** nothing. It corrects three sentences written before
  [`0013`](0013-the-board-of-latest-measurements.md) created a failure that is not
  a defect, and takes the granularity [`0024`](0024-before-it-leaves-this-machine.md)
  established for a hook and applies it to the result itself.

## Who this is for

[`@persona:agent-accelerated-owner`](../personas/agent-accelerated-owner.md), in
[`@workflow:adopt-the-process`](../workflows/adopt-the-process.feature), at the
point where a change has been pushed and the checks come back red. Ren's line
about a pipeline is one of the few things this repository has in their own words —
*"Fix the pipeline error, not bypass."* This change is about keeping that
instruction executable, because a red that cannot be fixed and must not be
bypassed is the one case it has no answer for.

It also touches a promise that belongs to no workflow: **`always-green`**. Part of
this change makes the pull-request report run in a state it has never run in — a
failing build — and the whole of that promise is that the report cannot decide
whether anything merges. It is argued under *Risks* rather than assumed.

## The job behind the request

The literal ask, from the issue: two rules in `method/` contradict each other, and
the tree obeys the second.

The job under it is not consistency. It is that **a red check has stopped carrying
information**, and the person it stopped carrying information for is the one whose
whole discipline is to act on it.

The numbers say it plainly. **Every one of the last twenty `checks` failures on
this repository was `✘ verification failed: measurement board`.** Not most —
twenty out of twenty, across four branches, with zero broken gates among them:

```console
$ for id in $(gh run list --workflow=checks.yml --status=failure --limit 20 \
      --json databaseId -q '.[].databaseId'); do
    gh run view "$id" --log-failed | grep -o "✘ verification failed:.*"
  done | sort | uniq -c
     20 ✘ verification failed: measurement board
```

So for twenty consecutive failures, red has meant *a number is waiting on the
maintainer's approval* and has never once meant *something is broken*. A person
who checks the first few and finds nothing wrong stops checking, and the gates
this repository exists to install become decoration in the one repository that
ships them.

**What is done today instead:** the contradiction is resolved in this
repository's own `CLAUDE.md` — *"The commit and the pull request can be finished
with a gap where the numbers go."* The issue is right that this is a
binding-shaped sentence in one repository's instructions, and that **it does not
ship**. An adopter who wires a graded suite gets
[`repository.md`](../../method/repository.md)'s absolute and no exception to it.

## Why now

**Three sentences in `method/` were all written when a red could only mean
broken**, and [`0013`](0013-the-board-of-latest-measurements.md) invented a red
that means something else without revisiting any of them:

- [`repository.md`](../../method/repository.md) — *"Never commit a state that
  fails verification."*
- [`graded-cases.md`](../../method/graded-cases.md) — *"the work can be finished
  with a gap where the numbers go"*, which sanctions exactly the state the line
  above forbids, on a different page, with no reference between them.
- [`gates.md`](../../method/gates.md) — *"It runs after both gates have passed,
  so it only ever describes a green run."*

**The third one has already cost something, and that is what makes this urgent
rather than tidy.** `board.py --json` was deliberately built to exit 0 whatever it
finds, with a comment saying why: *"a stale board can still be reported — which is
when the row matters."* `checks.yml` carries the same intent. The report has a
row, **Stale — inputs changed since**, built to carry precisely this number.

It has never once been able to. The report runs after `Verify`, and a job stops at
its first failing step, so on the run where the board goes stale the report is
skipped:

```console
$ gh run view 33140790702 --json jobs -q '...'
4 failure   Verify
5 skipped   Release inputs
6 skipped   The spec layer, here and on the base
7 skipped   Build the report
8 skipped   Comment it on the pull request
```

**The one mechanism built to say which red it is, is unreachable on every run that
is that red.** The head column of that row can only ever read zero. That is not an
oversight in the workflow file — it is `checks.yml` correctly implementing the
sentence in `gates.md` that says a report only ever describes a green run.

**And the hook now depends on this.** [`0024`](0024-before-it-leaves-this-machine.md)
kept the board gate out of `verify.py --local` for exactly this reason, and
[`setup`](../../skills/setup/SKILL.md) says so in as many words —
*"indistinguishable to a hook from a broken gate"*. The sentence names the defect
and then stops, because at the time there was nothing to point at.

## The end value

A red check either names something to fix or names who is waiting on what, and
never leaves the reader to work out which. The person who pushed can tell in one
line whether the ball is with them or with whoever pays for the runs — and the
commit they pushed is one the method actually permits, rather than one it forbids
in writing while every rule around it says to do exactly that.

**How we would know it worked:** the next time seven measurements go stale here —
which is this change, on merge — the branch is red, the last line of the failing
step says a run is owed rather than that verification failed, the exit status
differs from the one a broken gate produces, and the report arrives on the pull
request carrying the count. Today the branch is red, the line is identical to a
broken gate's, and no report is posted at all.

## What changes

### The three sentences, corrected together

- **[`repository.md`](../../method/repository.md), under *Commits*.** The absolute
  keeps its force and gains its one exception, stated so it cannot be widened: a
  state may be committed and pushed when its **only** failure is one whose cure is
  a spend nobody in the session can approve. What it owes: the commit says which
  measurements are waiting and that nothing here clears them. **And it stops
  there** — the exception buys a commit and a push, never a merge. The mechanism
  is on the conditional page rather than here, because most repositories can never
  enter this state and should not be paying context to read about it.
- **[`graded-cases.md`](../../method/graded-cases.md), under *Freshness is gated;
  the score never is*.** The half-sentence about finishing with a gap gains the
  rest of itself — what the gap obliges, that it is the one red a commit may
  carry, and who clears it. Then the requirement the issue asked for: **a
  verification that can fail for a reason the method sanctions has to say which
  failure happened in its result**, not only in prose somebody has to be reading.
  How is the repository's own business; that it must is not.
- **[`gates.md`](../../method/gates.md), under *The report is not a gate*.** The
  sentence about only ever describing a green run is corrected. A report is
  written to explain a state, and the state most needing explanation is the
  sanctioned red — so what explains a build survives the build failing. The
  never-gates rule is untouched and is what makes this safe: a report that runs on
  a red build still cannot turn it green, and one that cannot be built still says
  nothing and fails nothing.

### `setup` stops one clause short and now finishes

[Section 4](../../skills/setup/SKILL.md) already reaches the exact sentence — *"Red
for a reason the method sanctions, fixable only by a run somebody has to pay for,
and indistinguishable to a hook from a broken gate. Leave it to the pipeline."* It
gains the consequence: leaving it to the pipeline is only an answer if the pipeline
can say which red it is, so a repository whose verification can be sanctioned-red
comes out of the sitting able to tell the two apart, and its report is not skipped
on the failure it exists to describe.

The `description` does not move. This is behaviour inside a sitting that has
already started, so it is paid for in the body, where it costs nothing until
`setup` fires.

**[`doctor`](../../skills/doctor/SKILL.md) is not touched**, on
[`0024`](0024-before-it-leaves-this-machine.md)'s reasoning: its section 0 says the
checklist is `gates.md` and not itself. The corrected paragraph lives on that page,
which is where doctor reads it from, and restating it would break doctor's own
instruction while staling two more measurements to say the same thing twice.

### And this repository does it to itself

- **`verify.py` exits 2 when every failure it saw is in `COSTS_MONEY`**, and 1
  when anything else failed — including when a broken gate and a stale board fail
  together, because a real defect must never be reported as a bill. The last line
  changes with it: not *verification failed* but a line naming the waiting cases,
  what a run costs, and that the maintainer is who approves one. **2 is not a new
  convention here** — `run.py` already exits 2 for *a spend is required and nobody
  approved it*, which is the same sentence from the other side.
- **The required check does not change.** A non-zero exit is a non-zero exit;
  `checks.yml` still runs `verify.py` whole and CI is still red while a
  measurement is waiting. This adds a distinction to the red and removes nothing
  from it.
- **The report steps run on a failing build.** Guarded on `!cancelled()` rather
  than `always()`, still `continue-on-error`, still pull-requests only — so the
  **Stale** row reaches the reader on the one run it was built for.
- **The bindings** get the exit-code contract in *The table*, and the report's new
  run condition in *The wiring that must never gate*, where the report's row
  already says it is watched rather than inferred.
- **`inject.py` gains one fault:** a broken gate **and** a stale measurement at
  once, expected to exit 1 rather than 2. That is the dangerous direction — a real
  defect hidden behind a sanctioned red — and `gates-are-proven` means it does not
  ship without a fault that makes it fire. *The fault injection record* is
  generated from the injector, so the row appears there by itself.

**Rules added or changed** — the `@rule:` ids in `specs/features/`:

| Rule id | Feature file | New or changed |
|---|---|---|
| `the-one-red-a-commit-may-carry` | `features/verification/which-red.feature` | new |
| `a-red-says-which-red-it-is` | `features/verification/which-red.feature` | new |
| `what-explains-a-red-survives-it` | `features/verification/which-red.feature` | new |

All three are claimed by one new case, `27-a-red-nobody-here-can-clear`, with a
scaffold laying down a repository whose one verification command runs free gates
and a freshness check on a graded suite. A new case rather than another claim on
`26` or `12`: [`evals/README.md`](../../evals/README.md) has warned about growing
those for three versions running, and a claim added to an existing case stales a
measurement, where a new case only warns.

## What we are not doing

- **Nothing that makes the required check pass while a measurement is stale.** The
  issue puts it out of scope and it stays out. The merge waits on the run; what
  changes is what the red says, never whether it is red.
- **Not making the board gate a warning.** It is the obvious alternative and it is
  wrong: a number that no longer describes the tree is a lie, and
  [`graded-cases.md`](../../method/graded-cases.md) gates the bookkeeping for that
  reason. Downgrading it would end the contradiction by deleting the half that
  works.
- **No gate on the pull-request body.** A gate requiring the body to explain a
  waiting measurement would fire only on branches already blocked by the very
  check it is explaining — a second refusal stacked on a refusal, buying nothing.
  The obligation sits with the commit and the body, like the commit-message format
  beside it.
- **Nothing about `never measured`.** `board.py` warns there and does not fail, so
  it creates no red and needs no exception.
- **No second flag on `verify.py`.** `--local` already exists and is the hook's
  answer; this changes what a full run *says*, not what it runs. A flag that
  skipped the board in CI would be the out-of-scope change above wearing a
  different hat.

## Data

Nothing. No storage contract here, and what a version leaves behind is unchanged.
`board.json` keeps its shape; only who reads it and when changes.

## Risks

**`always-green` is the one to argue.** The report now runs on failing builds,
which is a state it has never run in. Three things hold it: every report step
keeps `continue-on-error`, so a failure inside one leaves the build exactly as it
was; the guard is `!cancelled()` rather than `always()`, so a cancelled run still
stops; and `report.py` is already held by a control in `inject.py` asserting it
exits zero on every degenerate input. What is new is that its inputs can now come
from a tree that failed verification — `trace.py --json` and `board.py --json`
both already exit 0 by design, which is what makes this the small change it looks
like. **A report has never been built against a red tree here**, and that is the
line in this spec most worth disbelieving until check 4 below has been run.

**A second kind of red is a second thing to understand.** Mitigated by making it
derive from `COSTS_MONEY`, the constant [`0024`](0024-before-it-leaves-this-machine.md)
already added: there is one list of what costs money, `--local` filters on it and
the exit code branches on it. A future expensive gate joins that set and nothing
else moves.

**Exit 2 could be read as worse than exit 1.** It is not an ordering; it is a
different kind. The last line carries the meaning and the exit code carries the
machine-readable half, which is why both move together rather than the code alone.

**The exception is the kind of rule that gets widened.** *Only* failure, cure is a
spend, nobody in the session can approve it — three conditions, and the second
example in the Gherkin is the boundary case where a real defect sits underneath
one. The `inject.py` fault is that boundary made enforceable, because prose about
not widening a rule is exactly what this repository does not rely on.

**Seven measurements go stale on merge, and the numbers are not in this branch.**
Every `skill:setup` case moves because the skill body does: `09`, `11`, `12`, `16`,
`17`, `23`, `26`, whose last measurements cost **$15.93** and were run on
2026-08-29. That flag is the maintainer's signature and not this session's, so the
gap is left open here — which is, exactly, the state this spec exists to make
legitimate, carried by the change that legitimises it.

## Acceptance checks

1. With the board green, `python3 .github/scripts/verify.py` exits 0 and prints
   what it always did. Nothing about a green run changed.
2. Stale one measurement by hand. `verify.py` exits **2**, and its last line names
   the case, what a run costs, and who approves one — the words *verification
   failed* do not appear. `verify.py --local` is still green and still says it left
   the board to CI.
3. Break a rule's traceability **as well**, and `verify.py` exits **1** and reports
   the broken gate. Exit 2 is unreachable while anything outside `COSTS_MONEY` is
   failing.
4. On this pull request, whose board goes stale on merge: the `repository checks`
   job is red, `Verify` has failed, and *Build the report* and *Comment it on the
   pull request* have **run rather than been skipped**. The comment's **Stale**
   row reads seven. Read back with `gh run view <id> --json jobs` and
   `gh pr view <n> --json comments`, not from the workflow file.
5. `python3 .github/scripts/inject.py` reports the new combined fault caught, and
   `checks.py` accepts *The fault injection record* with its generated row.
6. `grep -n "only ever describes a green run" method/gates.md` finds nothing, and
   what replaced it says in the same paragraph that the report still cannot fail a
   build.
7. Case `27` runs and its outcome graders discriminate: the fixture's freshness
   check is the attractive wrong answer to *leave it out of the hook*, and a
   passing run is one that left it in the pipeline **and** made the pipeline say
   which red it is.
