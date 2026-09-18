# Spec 0057: a measurement names its model

- **Status:** approved
- **Issue:** [#130](https://github.com/sargismarkosyan/livespec/issues/130) —
  the eval sessions run on whatever model the account defaults to, and
  neither the runner, the board nor the bill says which. Found 2026-09-18 in
  the `system.init` event of every transcript of the sitting of 2026-09-17,
  when the maintainer asked whether the suite runs on Sonnet.
- **Depends on:** [`0013`](0013-the-board-of-latest-measurements.md), whose
  board entry this extends by three fields; [`0028`](0028-below-the-floor.md),
  which put the decision about what counts as a measurement in one place,
  `caselib.py`, and which this gives two more things to decide; and
  [`0012`](0012-a-runner-that-runs.md), the runner.

## Who this is for

**Nobody in the workflows, and that is correct rather than a gap** —
[`process.md`](../../method/process.md#a-technical-change-that-serves-no-workflow-is-correct-not-a-gap).
This is the repository's own pipeline. The person it serves is the maintainer
at step 4 of the loop, approving specs against numbers this suite produced —
who learned yesterday that every one of those numbers was made by a model
nobody chose, at a price nobody added up, and that the board could not have
told them either thing.

**This lengthens nothing anybody types.** The documented command gains one
flag that names the model; a board row gains three fields a reader can see.

No always-promise moves. `always-green`: the gates are this repository's.

## The job behind the request

The literal ask is two sentences: the sessions run on Sonnet, and the suite is
as cheap as it can be. Behind them are three properties the suite never had.

**The model is a decision, and it was never written down.** `run.py --model`
defaults to the empty string — *"the account's default"* — and
[`provider.py`](../../evals/runner/provider.py) passes `--model` only when
that string is set. So `claude -p` chose. All **438** sessions of the last
sitting, both arms, four runs, ran on `claude-opus-5[1m]`: Opus 5, with the
million-token window, at $5 and $25 per million tokens where Sonnet 5 is $2
and $10. Nothing in the tree says so; the maintainer's own interactive default
is a different model again. A measurement here is of a skill, a case and a
model, and the third term was implicit.

**The board cannot tell.** `caselib.measurement_inputs()` fingerprints the
case's files, the text of the rules it claims and the body of the skills it
holds. The model and the harness sit outside it. A row measured on Opus and a
row measured on Sonnet are byte-identical on the board, and a change to
`provider.py` or `asserts.py` that alters what a number *means* stales
nothing. The gate that exists to say *this number no longer describes what it
measured* is blind to the two things that most change what a number measures.

**The bill is not the bill.** A row's `cost`, and the summary's dollar line,
are the sessions' `total_cost_usd` — **$118.33** for the sitting. The judge is
a `claude -p` call per `llm` grader per session, about **350** of them in the
sitting, and not one is priced: `_judge` reads its verdict from plain stdout,
and the cost travels only in the `--output-format json` envelope, beside
`structured_output`. The 279 sessions the account limit cut off are recorded
at $0 and were billed for what they consumed first.

**And one collision to decide rather than paper over.**
[`evals/README.md`](../../evals/README.md)'s floor reads *"`--judge-model
sonnet` or larger, and never the model under test."* Sonnet sessions put the
judge on the model under test. The reason in
[`graded-cases.md`](../../method/graded-cases.md#the-judge-is-not-the-thing-being-judged)
is self-preference: a model grading its own kind grades generously. Under
ablation the same judge reads both arms, so what it prefers in its own kind
lands on both sides of Δ; what it cannot be is a model that misses the nuance
the cases turn on. That is the decision this spec makes — the floor becomes
*never smaller than the model under test* — and the alternatives are in *What
we are not doing* with their prices.

## Why now

Because the next sitting is owed and will be paid once. After
[`0054`](0054-a-case-names-the-world-it-runs-in.md) and
[`0055`](0055-a-rider-is-filed-not-served.md) the board on `main` reads three
measured and twenty-five stale; the sitting that heals it should run on the
model the bindings name, and every row it writes should say so. And because
the harness change that follows this one —
[`0058`](https://github.com/sargismarkosyan/livespec/blob/spec-0058-a-case-is-a-sitting-not-a-turn/specs/changes/0058-a-case-is-a-sitting-not-a-turn.md) — moves `provider.py`, which
this spec makes a staling event: the two land, then one sitting, on purpose.

## The end value

`run.py` runs both arms on the model the bindings name unless told otherwise,
refuses with an estimate computed from the board rather than a figure typed
into a docstring in August, and records per row the model that ran, the judge
that graded, a fingerprint of the harness, and the whole bill. `board.py`
stales a row made on another model or by another harness, and says which.
`evalsuite.py` fails a runner whose default drifts from the bindings. Every
sentence in the tree that says *$1.80 a case, ~$4 the suite* stops saying it.

**How we would know it worked:** three faults read *fails*; on `main` after
the change every row on the board is stale with the words *measured on an
unknown model* and `verify.py` exits 2 for that and nothing else; the first
Sonnet sitting's rows carry `"model": "claude-sonnet-5"`, a `harness`
fingerprint, and a `cost` larger than its sessions' by exactly the judge's.

## What changes

1. **[`caselib.py`](../../.github/scripts/caselib.py)** holds the decision, as
   it holds the floor: `SESSION_MODEL = "claude-sonnet-5"` — the exact id, not
   the alias, so that when a new Sonnet ships the binding moves by hand and
   every row goes stale on purpose rather than silently; `HARNESS_FILES =
   ("evals/runner/provider.py", "evals/runner/asserts.py")` and
   `harness_fingerprint(root)` over their bytes; and `is_current(entry, case,
   root)`: inputs match, `model` is `SESSION_MODEL`, `harness` is the current
   fingerprint. The runner's `--changed` and the board gate both ask it, so
   they cannot disagree about which rows are owed.
2. **[`run.py`](../../evals/runner/run.py)**: `--model` defaults to
   `SESSION_MODEL`; the run header and the summary print the model. The
   refusal stops quoting a figure and prints an **estimate**: for the cases
   selected, the board's last `cost` per case — an unmeasured case at the mean
   of the measured — with the model those costs were made on named beside it,
   so the first Sonnet refusal says plainly that it is quoting Opus prices.
   The docstring loses *$1.80* and *~$4*.
3. **[`provider.py`](../../evals/runner/provider.py)** passes `--model` on
   every session, and reads the model the session *actually* ran on out of the
   transcript's `system.init` event into `metadata.model`. The row records what
   ran, not what was asked for; a fallback would stale itself.
4. **[`asserts.py`](../../evals/runner/asserts.py)**: `_judge` calls with
   `--output-format json`, takes the verdict from `structured_output` and the
   price from `total_cost_usd`, and appends one line — case, arm, grader, judge
   model, cost — to `judge.jsonl` in the run directory. The retry loop is
   unchanged; what an errored verdict weighs is
   [#131](https://github.com/sargismarkosyan/livespec/issues/131)'s question
   and `0058`'s answer.
5. **[`run.py`](../../evals/runner/run.py) `collect()` and `record()`** add the
   judge ledger to each case's cost, and write `model`, `judge` and `harness`
   into the row. A row is the whole bill.
6. **[`board.py`](../../.github/scripts/board.py)** stales on two new reasons,
   each in its own words: *measured on `<model>`; the suite measures on
   `claude-sonnet-5`* and *measured by a harness that has since changed*. A
   row with no `model` field reads *measured on an unknown model*. The `--json`
   hand-over is unchanged.
7. **[`evalsuite.py`](../../.github/scripts/evalsuite.py)** fails a runner
   whose `--model` default is not `caselib.SESSION_MODEL`, the way it fails one
   that stops asking `replaces()`; and the documented invocation must name
   `--model claude-sonnet-5`, the way it must name `--ablation with-without`.
8. **[`inject.py`](../../.github/scripts/inject.py)**: the fixture's board
   rows gain the three fields; three faults — *a runner whose default model is
   not the bindings'*, *a board row measured on another model*, *a board row
   from another harness* — read *fails*. 114 becomes 117.
9. **A test the pipeline can run for free.** `tests/test_runner.py`, standard
   library, puts a stub `claude` on `PATH` that emits a stream-json transcript
   with a chosen `init` model and a JSON judge envelope with a cost, and
   asserts: the provider passes `--model claude-sonnet-5` and records the init
   model; `_judge` reads `structured_output` and writes its ledger line;
   `collect()` adds that line to the case's cost. The stub is the only way to
   test this without spending, and it is what `0058` extends.
10. **Words.** [`evals/README.md`](../../evals/README.md): the invocation gains
    `--model claude-sonnet-5`; the floor's judge bullet becomes *both arms run
    on the model the bindings name, and the judge is never smaller than it*,
    with the ablation argument in the sentence after; the cost paragraph
    points at the refusal's estimate and the board; *The board* names the
    three fields and the two new reds; a history line records the sitting of
    2026-09-17 — 438 sessions on a model nobody chose, $118 before the judge.
    [`CLAUDE.md`](../../CLAUDE.md) and `verify.py`'s owed-note lose the
    figure and gain the pointer. **This repository's bindings**: the runner
    paragraph names the session model and the judge; `boundary:model-session`
    names the model; `boundary:judge` records that the judge is the session's
    model since this change and why the ablation makes that bearable; *Fault
    injection* counts 117.
11. **[`method/graded-cases.md`](../../method/graded-cases.md)**, one
    paragraph under *The judge is not the thing being judged*: where the judge
    and the thing under test are the same model, both arms are read by the
    same eyes and the difference between them is what survives the bias —
    say so where the decision is made, and read the verdicts. No runner, no
    model name; it survives a repository with pytest.

**Rules added or changed: none.** The repository's own pipeline carries no
rule id; the faults and the test are its contract.

## What we are not doing

- **Not Haiku for the sessions.** It would halve the bill again and keep the
  judge larger than the model under test. It would also measure a model the
  skills were not written against: Sonnet is the default on the plans most
  users of this plugin are on, so a Sonnet number is the floor most of them
  see, and an Opus or Fable number is the ceiling. The floor is the number
  worth a board.
- **Not an Opus judge.** About 350 calls a sitting at two and a half times
  the price, to buy back a bias the ablation already puts on both sides of
  the difference. If a calibration read ever shows the judge favouring one
  arm's voice, that is the day to pay it.
- **Not `--effort` reductions.** A cheaper session that thinks less is a
  different judgment under test; a knob for a later spec, with a pilot's
  verdicts to read first.
- **Not folding the model into the `inputs` hash.** A row should say the model
  in words a reader can see, and the gate should name it in the failure. A
  hash that quietly changes is the property this spec is removing.
- **Not the alias.** `--model sonnet` would move under the board the day
  Anthropic points it at a new model, which is the same silent change with a
  friendlier name.
- **Not accounting for what the 429s cost the plan.** A session that errored
  is recorded as an error; what it drew from the limit before it died is not
  readable from the CLI. The cure is not to hit the limit, which is `0058`'s
  and the model's job.
- **Not re-measuring anything here.** Every run is the maintainer's to
  approve, and the run this owes waits for `0058`.

## Data

No storage. Files that move: `.github/scripts/caselib.py`,
`.github/scripts/board.py`, `.github/scripts/evalsuite.py`,
`.github/scripts/inject.py`, `.github/scripts/verify.py`,
`evals/runner/run.py`, `evals/runner/provider.py`, `evals/runner/asserts.py`,
`tests/test_runner.py` (new), `evals/README.md`, `CLAUDE.md`,
`method/graded-cases.md`, `specs/setup/README.md`, and this spec.

**This spec commit stales nothing.** `verify.py` exits **2** for the rows
already owed and no other reason.

**The implementing change stales every row on the board, by design, and says
so.** No row carries a `model` or a `harness`; every one reads *measured on an
unknown model* the moment the gate can ask. That is the truth about them: they
are Opus 5 numbers, and a Sonnet board may not carry them as measurements.
Nothing is lost — the run directories hold every transcript — and nothing is
re-measured until `0058` lands, so the sitting is paid once.

**What that sitting will cost, honestly.** The last sitting's priced sessions
averaged $0.74 on Opus 5; at Sonnet 5's list prices the same tokens are about
$0.30, so a case at the floor is about **$2 with the judge**, and the whole
suite at 46 cases about **$85–95** — if Sonnet's sessions use tokens the way
Opus's did, which the first sitting will measure and the board will then
quote. The saving on the plan's limit is larger than the saving in dollars,
which is what made three sittings in a row die at 28, 40 and 24 sessions.
`--changed` remains how a sitting stays small.

**What the pull request owes.** `method/` moves by one paragraph —
**`patch`** — a `## Changelog` section, and the run block, because it touches
`tests/`, `evals/` and `.github/scripts/`. No `.feature` moves; the audit
surface does not.

## Risks

- **The exact id retires.** When `claude-sonnet-5` is withdrawn the runner
  fails at the first session with the API's own words, rather than quietly
  measuring its successor. The binding is one line and the board stales
  itself when it moves. That is the behaviour wanted.
- **Self-preference survives the ablation.** It might — a judge could prefer
  the plugin arm's voice or the bare arm's. The calibration read the README
  has owed since `0012` is the only instrument for that, and the first Sonnet
  sitting is the one to read.
- **The estimate is wrong by the price ratio until the first Sonnet sitting.**
  It says which model its figures were made on, which is more than the
  docstring did.
- **The board reads zero measured for a while.** It reads the truth. The
  commit and the pull request say so in as many words.
- **Always-promises.** `always-green`: unchanged. `never-implements`:
  scripts, tests and prose. `context-budget`: no description moves.

## Acceptance checks

1. `python3 .github/scripts/inject.py`: 117 faults caught — the three new
   ones reading *fails* — and the fixture green.
2. `python3 evals/runner/run.py --ablation with-without --judge-model
   claude-sonnet-5 --allow-tools Write Edit Bash --scaffold --case
   06-neg-commit-message`, with no approval flag, refuses and prints an
   estimate that names the model the board's cost for `06` was made on.
3. `python3 .github/scripts/board.py` on the implementing branch: every row
   stale, each naming *measured on an unknown model*; `verify.py` exits 2 and
   names nothing else.
4. `python3 .github/scripts/tests.py`: `test_runner.py` green against the
   stub — the `--model` flag, the recorded init model, the judge ledger, the
   summed cost.
5. `grep -rn '1\.80' CLAUDE.md evals/ .github/scripts/ specs/setup/` finds
   nothing; the README names `--model claude-sonnet-5` in the invocation and
   the floor; the pull request carries `patch`, `## Changelog` and the run
   block.
