# Spec 0028: below the floor

- **Status:** approved
- **Issue:** [#75](https://github.com/sargismarkosyan/livespec/issues/75)
- **Depends on:** [`0013`](0013-the-board-of-latest-measurements.md), which built
  the board and the freshness hash this corrects the reading of.

## Who this is for

[`agent-accelerated-owner`](../personas/agent-accelerated-owner.md), in
[`adopt-the-process`](../workflows/adopt-the-process.feature) — months into it,
at the moment they look at a dashboard number instead of a diff.

The persona line this turns on is the one the gates are built around: **they do
not read the docs.** `evals/README.md` has said `runs: 3` is the floor since the
suite existed, and the board has been reporting a mean over single runs the whole
time. Nobody had to ignore anything for that to happen — the two facts were on
different pages, and only one of them was on the screen.

## The job behind the request

Know which numbers on the board are worth believing, without having to go and
check how each one was produced.

## Why now

Because the failure has already happened here, in committed history, to the one
case an open issue was built on.

`26-two-seconds-before-the-push` was measured on 2026-08-28 at **Δ −0.33** over
three runs, $4.67 — the only case in the suite whose own change had made it
negative, and the subject of
[#67](https://github.com/sargismarkosyan/livespec/issues/67). A `--runs 1`
calibration pilot the next day wrote **Δ +0.33**, $1.21, into the same row. Same
magnitude, opposite sign, a third of the runs, and nothing anywhere recorded that
a replacement had taken place. Read the board on 2026-08-29 and case 26 looked
healthy.

**The sign flip is the visible half and the smaller one.** The row also carries
the `inputs` hash that `board.py` compares against the tree, so the pilot did not
only overwrite a number — it *cleared the freshness gate*. The red that had been
asking for a real run went green at the moment the run it was asking for became
most necessary. A gate that a pilot can quietly satisfy is not a gate; it is a
field that gets filled in.

Neither half needed anybody to be careless. `--runs 1` is documented under
*Calibration* and is the right thing to run before spending $4 on a full suite.
The defect is that nothing downstream of the run distinguished its output from a
measurement's.

## The end value

The number a person reads off the board is one they can act on, and the count
beside it says how much of the board is actually measured. Where it is not, that
is visible rather than averaged in.

**How we would know it worked:** run `--runs 1` against a case the board holds a
three-run entry for. The pilot's numbers print in the summary, the board's entry
does not move, and the runner says which row it kept and why.

## What changes

- **`caselib.py` owns the floor.** `MIN_RUNS = 3` moves out of `evalsuite.py`,
  and joins `is_measurement()` and `replaces()`. Three places deciding
  separately what counts as a measurement is exactly how a pilot ended up
  wearing a measurement's clothes; `measurement_inputs` already lives here for
  the same reason.
- **`run.py` asks before it writes.** A run at or above the floor takes its row
  as it always did. Below the floor it fills a row that holds nothing, or one
  holding another below-floor number, and **never** one holding a measurement —
  it keeps that entry, and prints which row it kept, what is in it, and where
  the pilot's own verdicts are.
- **`board.py` reads `runs`.** An entry below the floor is listed, kept, shown,
  **warned** about, left out of the mean, and not counted as measured.
  Staleness is still asked first and asked of every entry, because a number that
  no longer describes these files is wrong however many runs produced it.
- **`evalsuite.py` holds the runner to it**, the same way it already holds it to
  `--i-approve-the-cost`: a `run.py` that stops calling `caselib.replaces()`
  fails the gate.
- **The report gains a row.** *Below the floor — a pilot, not a measurement*,
  beside *stale* and *never measured*, so the count is on the pull request and
  not only in a local run's output.
- **`method/graded-cases.md` gains the portable half** — a run below the floor
  does not take a measurement's row, and the summary carries how many runs
  produced it so that everything reading the summary can honour that. It names
  no threshold: the page already refuses to say how many runs are enough, and
  this says only what follows once a repository has decided.

**Rules added or changed:** none. Argued below rather than left as an omission.

### Why no Gherkin moved

Every rule in [`specs/features/`](../features/) is a promise about what a
**session** does, held by a case that runs one. This change alters no session's
judgment: it changes what two scripts in `.github/scripts/` and one in
`evals/runner/` do with a JSON file. Gate mechanics in this repository are held
by [fault injection](../setup/README.md#the-fault-injection-record) — that is
what the 49-row record is for — and two rows are added there:

| Injected fault | Expected |
|---|---|
| the runner letting a run below the floor take a measurement's row | fails |
| a board entry from fewer runs than the floor | **warns, does not fail** |

Writing a rule here would mean writing a case to claim it, and that case would
measure a skill's behaviour in a consuming repository — which is a real and
different question (*does `doctor` report a below-floor number as coverage?*) and
not the one #75 asks. It is worth asking later, on its own evidence.

### What the board says the day this lands

Nothing was re-run, and both of these are the same board:

| | before | after |
|---|---|---|
| measured | 28 | 5 |
| below the floor | — | 23 |
| mean Δ | +0.29 | +0.44 |

23 rather than 22 because `27-a-red-nobody-here-can-clear` holds two runs, not
one — a third session was lost to a `429` and the entry was committed saying so.
The floor does not distinguish a pilot from a measurement that lost a session,
and should not: the board cannot tell them apart either, and both are below what
the suite says a number needs.

**The pull-request report will not show this move, and is right not to.**
[`checks.yml`](../../.github/workflows/checks.yml) runs the *current* gate
against the base tree on purpose — so the delta reports what the measurements
did, not what a change to the gate did — which means both of its columns read 5.
The table above is this repository's reading of the same board on two days, and
the only place the move is visible.

**This is a correction, not a regression.** Nothing got worse; a claim stopped
being made. The mean moving *up* is worth noticing for exactly that reason — it
is not a result, it is the arithmetic no longer including 23 numbers that were
never entitled to be in it.

## What we are not doing

- **Failing on a below-floor entry.** It is the honest-looking option and the
  maintainer ruled on it: 23 cases would go red at once, `--changed` would select
  all of them, and clearing that is roughly **$36** across several sittings,
  since three runs in one sitting have exhausted the account outright. It would
  also block this change on the bill it just discovered. The warning is not a
  softer version of that verdict — a below-floor number is the best the board
  has, and keeping it is right; what was wrong was calling it coverage.
- **Re-measuring the 23.** Named and costed, not started. The board now says
  which rows they are, which is what makes it possible to spend on them
  deliberately instead of all at once.
- **Deleting the below-floor numbers.** That trades a number nobody should
  average for no number at all, and puts 23 rows back into *never measured* —
  worse on every count.
- **A flag to force a pilot onto the board.** Any such flag is the default
  within a month. Re-running at the floor is the way to replace a measurement,
  and it is the thing that was supposed to happen anyway.
- **Touching what is gated.** The score is still never gated; freshness still is.
  This changes which entries are *called* measurements, not what passes.
- **Reopening `26`'s Δ.** Its history is written down in
  [`evals/README.md`](../../evals/README.md) so the next reader of a negative Δ
  does not re-open [#67](https://github.com/sargismarkosyan/livespec/issues/67);
  that is a record, not a change.
- **A ledger row.** No gate is added or removed. Gate 5 reads a field of its own
  input that it was already being handed.

## Data

`evals/board.json` gains no field. `runs` has been written by `run.py` since
[`0013`](0013-the-board-of-latest-measurements.md) and was the one field nothing
read; this change reads it. Every existing entry stays valid, and no entry's
`inputs` hash moves, so **no measurement goes stale** — the board's own counts
change because they are counted differently, not because anything was
re-measured.

## Risks

- **The mean going up on a change about honesty reads badly.** It is the
  arithmetic dropping 23 ineligible numbers and nothing else, and it is written
  down in three places for that reason. The mitigation is the sentence, not a
  different number.
- **Five measurements is a thin board.** True, and it was true yesterday — the
  change is that it now says so. The risk of not doing it is worse: a mean over
  single runs moves with the variance the floor exists to average out, so the
  suite's headline was reporting its own noise.
- **A pilot against a measured case now looks like it did nothing.** The runner
  prints what it kept and where the pilot's verdicts are, because a refusal
  nobody sees is indistinguishable from a bug.
- **`replaces()` is a name in a gate's string check.** `evalsuite.py` greps
  `run.py` for `replaces(`, so renaming the function silently disarms that
  check — the same fragility the `--i-approve-the-cost` check already has, kept
  deliberately consistent rather than solved twice.

## Acceptance checks

There is no screen. What a person does by hand:

1. `python3 .github/scripts/board.py` — the summary names the below-floor count
   separately, the mean is described as being over the measurements, and the
   warning lists the rows with their run counts.
2. `python3 .github/scripts/board.py --json` carries `below`, and
   `report.py` renders its row.
3. Break it on purpose: set an entry's `runs` to `1` in a copy of the tree and
   confirm the gate warns and still exits 0; move a case's prompt and confirm
   the same entry now **fails** as stale, because staleness is asked first.
4. `python3 .github/scripts/inject.py` catches 49 faults, including the two new
   ones, and the record in [the bindings](../setup/README.md) matches.
5. With a maintainer's approval, `run.py --case 26-two-seconds-before-the-push
   --runs 1` prints its numbers, leaves `evals/board.json` unchanged, and says
   which row it kept.
