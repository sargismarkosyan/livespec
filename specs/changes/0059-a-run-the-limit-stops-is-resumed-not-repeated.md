# Spec 0059: a run the limit stops is resumed, not repeated

- **Status:** approved — merged by the maintainer as #145 on 2026-09-20
- **Issue:** [#144](https://github.com/sargismarkosyan/livespec/issues/144) —
  every paid sitting since 2026-08-25 has ended at the account's session
  limit, and every session after the cut was lost: cases `42`–`45` have been
  paid for four times and measured never. Found 2026-09-20 while answering
  *where are we, and what do the evals not do yet*.
- **Depends on:** [`0058`](0058-a-case-is-a-sitting-not-a-turn.md), whose
  sittings are the sessions this keeps — a flagship sitting is seven dollars
  and a hundred turns, and losing three of them to a one-line refusal is what
  made the loss expensive enough to see; and
  [`0057`](0057-a-measurement-names-its-model.md), whose refusal prices a run
  from the board, so a resumed run can be priced too.

## Who this is for

**Nobody in the workflows, and that is correct rather than a gap** —
[`process.md`](../../method/process.md#a-technical-change-that-serves-no-workflow-is-correct-not-a-gap).
This is the repository's own pipeline. The person it serves is the maintainer
who pays for a sitting and reads the board afterwards, and who has so far read
*errored* where the money went.

**This lengthens nothing anybody types.** The documented invocation does not
change. One flag arrives, `--resume <run-dir>`, and it is the one the run
prints when it stops.

No always-promise moves. `never-implements`: nothing here writes application
code.

## The job behind the request

The literal ask is the issue's: keep what ran, name what did not, run only
that. Behind it is what the runner is.

**What the limit looks like.** The session gets one `result` event and it is
unambiguous — `is_error: true`, `api_error_status: 429`, *"You've hit your
session limit · resets 1pm (Asia/Yerevan)"*, cost zero — and the CLI exits 1
with nothing on stderr. The judge and the person get the same envelope. It is
the cheapest event in the transcript to read, and nothing reads it.

**What the runner does with it.** [`run.py`](../../evals/runner/run.py) hands
the whole run to promptfoo in one `npx` call and reads `results.json` once at
the end. Past the cut every remaining session still starts, meets the wall,
and is reported as `claude exited 1: no stderr`; a case with one such session
has fewer than three runs, so `record()` holds the floor and writes nothing,
and the sessions that did run are written off with their cost. The same
happens from the other side when the machine kills a run: since `8594558` the
transcripts are on disk, and nothing can take them up.

| run | sessions the limit took | what was lost |
|---|---|---|
| part 1, 2026-09-17 | 32 of 270 | 15, 21, 23, 25, 31, 34, 43, 45 — the sessions before the cut in each |
| part 2 | ~44 of 72 | 27, 28, 41–45; 26 kept one session of six |
| part 4, 2026-09-18 | ~24 of 48 | 42–45, for the third time; 41's three plugin sessions |
| two pilots, 2026-09-19 | killed in flight | two sittings each, transcripts on disk, nothing to read them |

**What promptfoo is doing here.** One job: a thread pool over case × arm ×
run that calls [`provider.py`](../../evals/runner/provider.py) and then
[`asserts.py`](../../evals/runner/asserts.py). For that the runner needs
node, a pinned version, `REQUEST_TIMEOUT_MS` raised over its worker, a
results shape nobody chose, and its viewer to read a verdict. The case format
was never promptfoo's — [`0012`](0012-a-runner-that-runs.md) kept the folders
native so the gated `claude plugin eval` could take them one day — and the
loop it runs is thirty lines of the standard library.

The job: **a run is a directory of finished sessions and verdicts, written as
they finish; the limit stops it from starting more, says what is owed and
when; and one command runs exactly that.**

## Why now

Because the board is owed one whole sitting on Sonnet — 46 cases, none
current — and the limit has ended every attempt at a whole sitting. A run
that can be stopped and resumed is a sitting that can be paid for in the
parts the account allows, on the days it allows them, and still make one
number per case from the whole.

## The end value

A run directory holds, per session, the transcript, the files it wrote, its
result and its verdicts, each written the moment it exists. The first session
or verdict that meets the limit stops the run from starting another; the
summary says how many sessions and verdicts are owed and when the limit
resets, and prints the one command that resumes. `--resume <run-dir>` runs
only what is missing — a session that never finished, a verdict the judge
never returned — and the case's row is made from the whole set. A resumed run
is still a spend: it refuses without the maintainer's flag, and the refusal
prices only what is missing. Nothing in the runner needs node.

**How we would know it worked:** the stub-driven control drives a run into a
stubbed limit, finds the sessions before it graded and the one after it owed,
resumes, meets the limit again in the judge, resumes again, and finds every
session run once and every verdict returned; and the next paid sitting ends
with *resume with* rather than *errored*.

## What changes

1. **[`run.py`](../../evals/runner/run.py) drives its own sessions.** The
   plan — the cases selected, their variables and graders, the model, the
   judge, the grant, the scaffold flag and the runs — is written to
   `run.json` in the run directory. A thread pool of `--max-concurrency`
   workers takes one job each, `(case, arm, run)`: it calls
   `provider.call_api`, writes `session.json`, then calls `asserts.get_assert`
   for each grader and writes `verdicts.json`, all under
   `sessions/<case>/<arm>-<run>/` beside the transcript, the tool log and the
   workspace the provider already leaves. `results.json` is assembled from
   those files, in the row shape `collect()` already reads — a case, an arm,
   a response or an error, its verdicts with their weights — so `collect()`,
   `record()` and the board do not move. promptfoo, `npx`, the pin and
   `REQUEST_TIMEOUT_MS` go.
2. **The limit is read, not inferred.** [`provider.py`](../../evals/runner/provider.py)
   reads a `result` event whose `api_error_status` is 429, or whose error text
   says the limit was hit, as the limit: the session returns an error marked
   `limit`, with the reset time the text names. The person's envelope is read
   the same way and ends the sitting as a limit, not as a person who could
   not be reached. [`asserts.py`](../../evals/runner/asserts.py) reads the
   judge's envelope the same way and returns an errored verdict marked
   `limit` without the two retries, since the wall does not move in ten
   seconds. The first job that meets it sets a flag; a job that starts after
   the flag does not run and is recorded as owed. Jobs already running finish
   on their own — they meet the same wall, one line each.
3. **The run says what it owes.** After the summary: how many sessions never
   ran and how many verdicts were never returned, the reset time the limit
   named, and `python3 evals/runner/run.py --resume evals/results/<stamp>`.
   The exit code is **3** — not 0, which is a completed measurement, and not
   1, which is a broken harness. A run the machine kills leaves the same
   directory and resumes with the same command.
4. **`--resume <run-dir>`** reads `run.json` for everything the first
   invocation said — a resumed run is the same run, so `--ablation`,
   `--judge-model`, `--model`, `--allow-tools`, `--scaffold`, `--case` and
   `--runs` are not taken beside it — and performs only the jobs that are
   owed: a session with no `session.json`, or one whose error was the limit,
   is run; a verdict marked `errored` is judged again over the session that
   already exists, which costs the judge's price and not the session's. A
   session that errored for any other reason — a timeout, a scaffold that
   failed — is left as it is, because a resume is for what the limit or the
   kill took and not a second try at a measurement. The refusal prices what
   is missing: each case's last cost on the board, times the share of its
   jobs still owed. `record()` runs at the end of every resume over the whole
   directory, so a case completed on the second day writes its row then.
5. **[`inject.py`](../../.github/scripts/inject.py)** — the stub `claude`
   answers the limit's envelope when a flag file names it, once for a session
   and once for the judge, and `runner_control()` drives the run described
   under *The end value* through `run.py`'s own `drive()` and `assemble()`,
   with the stub's argument log proving the resumed session was not run
   twice. The control counts as before; no fault is added, because the
   runner's behaviour is a control's subject and not a gate's (0057).
6. **Words.** [`evals/README.md`](../../evals/README.md): the *Runs on
   promptfoo* box becomes *Runs its own sessions*; *Calibration* reads a
   verdict from `verdicts.json` rather than promptfoo's viewer; a section
   *When the limit stops a run* says what the directory holds, what the
   summary prints and what `--resume` does and does not do. **This
   repository's bindings**: the runner paragraph loses promptfoo and node and
   gains the directory, the exit code and the flag; the `boundary:model-session`
   row's *leaves uncovered* line — the account's session limit — becomes what
   covers it. [`CLAUDE.md`](../../CLAUDE.md), one line, at its ceiling, so the
   count holds; [`CONTRIBUTING.md`](../../CONTRIBUTING.md), one line.

**Rules changed: none.** The pipeline's own changes carry no rule id; the
control is their contract. Nothing under `skills/`, `method/`, `templates/`
or `tools/` moves, so nothing ships and the pull request carries no label.

## What we are not doing

- **Not waiting for the reset.** A run that sleeps until *1pm* is a run that
  holds a terminal and a task manager for hours and gets killed by the second
  — which is how two pilots died. The run stops, says when, and the maintainer
  runs one command later.
- **Not retrying errors that are not the limit.** A timeout is a session that
  ran for its whole budget and is not a spend to repeat unasked; a scaffold
  that failed is a case to fix. Both stay as errors, named in the summary,
  and a fresh run is how they are tried again.
- **Not changing what a session is.** `provider.py` gains a reading of one
  event and a name for its directory; the sitting, the person, the shell and
  the digest are `0058`'s and do not move. The harness fingerprint moves
  because the file does, and every row is stale already.
- **Not a sweep of the never-measured eighteen.** All forty fixture scripts
  run clean on this machine, checked today; what those cases need is the
  sitting this makes affordable, not a change of their own.
- **Not re-measuring anything here.**

## Data

No storage. Files that move: `evals/runner/run.py`, `evals/runner/provider.py`,
`evals/runner/asserts.py`, `.github/scripts/inject.py`, `evals/README.md`,
`specs/setup/README.md`, `CLAUDE.md`, `CONTRIBUTING.md`, and this spec.

**This spec commit stales nothing.** `verify.py` exits **2** for the rows
already owed and no other reason.

**The implementing change stales what `0057` already staled**: every row,
through the harness fingerprint. Nothing new is owed by it.

**What the pull request owes.** Nothing ships — no label, no changelog. It
touches `evals/` and `.github/scripts/`, so it carries the run block.

## Risks

- **A thread pool is not promptfoo.** What promptfoo gave beyond the loop was
  a progress bar and a viewer, and neither was used on a non-TTY. What it
  took was a worker timeout that killed a session mid-measurement once. The
  provider's own watchdog is the session's timeout and always was.
- **Two workers meet the limit at once.** Each records its own session as
  the limit's; both are owed; the resume runs both. Nothing is double-counted
  because a job is a directory and a directory is written once.
- **The reset time is a string.** It is printed as the CLI printed it, never
  parsed into a wait; see *not waiting for the reset*.
- **A resume after the case moved.** `run.json` holds the plan, not the
  case's files; a case edited between the two halves is measured half on
  each. The board's inputs hash is taken at `record()`, so the row would read
  current while its first half is not. The resume prints the cases whose
  inputs hash differs from the plan's, as a warning, and the maintainer
  decides; a fresh run is one command.
- **Always-promises.** `always-green`: unchanged. `never-implements`: nothing
  is written but the runner and prose. `context-budget`: no description
  moves.

## Acceptance checks

1. `python3 .github/scripts/inject.py`: 119 faults caught, the runner control
   green — a run into the stubbed limit, one session owed, resumed; the judge
   meets it, one verdict owed, resumed; every session run once by the stub's
   log, every verdict returned, both cases in `collect()`'s measured set.
2. `run.py` over a run directory the limit stopped exits 3 and prints the
   resume command; `run.py --resume <dir>` without the flag refuses, pricing
   only what is owed.
3. `run.py --resume <dir> --i-approve-the-cost` on the directory of
   `20260918-084138` would run the owed sessions of `42`–`45` and no other —
   said here as the reading of the plan, not run: that directory has no
   `run.json`, and a run before this spec is not resumable.
4. `verify.py` exits 2 for the board only; the pull request carries the run
   block and no label.
5. The first paid sitting after this lands ends, if the limit bites, with
   *resume with* and an exit code of 3, and the resume the next day writes
   the rows — read the summary of each half before the floor is believed.
