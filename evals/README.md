# The eval suite

What these skills are worth is almost entirely **judgment under pressure** —
finding the job under a proposed solution, filing instead of fixing, and refusing
the persona or workflow invented to make a wanted thing legal. None of that is
checkable by reading the files. This suite is how a change to a skill is held
against it.

```
python3 evals/runner/run.py --ablation with-without --judge-model sonnet --allow-tools Write Edit --scaffold
```

> **This refuses to run, and that is the design.** Every run drives six real
> `claude -p` sessions per case plus judge calls — about $1.80 for one case at
> `runs: 3`, ~$4 for the suite — billed to the maintainer's account and drawn
> from its session limit, which three runs in one sitting have exhausted
> outright. `run.py` exits 2 unless `--i-approve-the-cost` is passed, and
> `evalsuite.py` fails the build if that refusal is ever removed.
>
> **The flag is the maintainer's signature on one specific run.** An agent
> must not add it on its own initiative — not for a stale board entry, not for
> the `--changed` heal the board gate prints, not to finish a task. The
> commands quoted throughout this file are deliberately written without it, so
> that copying one refuses rather than spends. When a measurement is needed,
> stop, name the stale cases and the cost, and wait for a yes.

> **Runs on promptfoo, not yet calibrated.** The native runner for this case
> format — `claude plugin eval` — is gated per organisation during early access
> and has never started on this account, so since
> [0012](../specs/changes/0012-a-runner-that-runs.md) the suite runs through
> [`evals/runner/`](runner/run.py) instead: each case goes through `claude -p`
> with the plugin loaded and without, an llm grader's rubric is scored by the
> judge model, and the cases stay written in the native format so enablement
> arriving one day is a bonus rather than a migration. One case has been run end
> to end; **nobody has read a full pilot's verdicts.** Whoever runs the first
> one should treat it as calibration — read every judge verdict and ask whether
> they would have scored it the same way — and correct the rubrics before
> anyone trusts a number from here. See *Calibration* below.
>
> What CI enforces is the structure: `python3 .github/scripts/verify.py`
> fails if a skill is held by no case, if a case is graded only by what fired, if
> `runs` drops below three, if the last should-not-fire case is deleted, if the
> invocation below loses its baseline — and, since the board, if a measurement's
> inputs changed without a re-run. That proves a case exists and **can** fail.
> It never proves one passes, and no green run should be read as saying so.

## The number that matters is Δ, not the score

Every case runs twice: once with the plugin loaded, once without. The headline is
the **difference**. A case that passes in both arms proves nothing about livespec
— the base model was going to do that anyway. A case that passes only with the
plugin loaded is the plugin earning its context.

This is also why `graders/skill-fired.md` exists in the fire cases and is
deliberately *not* scored: under ablation a `tool_used: Skill` grader is reported
as a plugin-fired indicator and excluded from both arms' scores. It tells you
whether the skill triggered; it can never inflate Δ. Every case is scored on what
came out.

## What each case is for

| Case | Holds | Fails when |
|---|---|---|
| `01-solution-shaped-request` | `refine-spec` finds the job under the proposed solution | a description edit makes it start building the button |
| `02-feedback-from-use` | `feedback` files rather than fixes, and pulls out the implicit | it fixes on the spot, or tracks only the stated complaint |
| `03-persona-to-fit-feature` | `refine-personas` refuses a persona ordered backwards | the refusal softens into "here's the persona, with caveats" |
| `04-workflow-for-orphan` | `refine-workflows` refuses a workflow shaped like its orphan | satisfying the gate beats telling the truth |
| `05-future-state-journey` | `refine-journeys` refuses an arc where everything goes well | it writes the hopeful map as the current state |
| `06-neg-commit-message` | **nothing fires** on an ordinary request | the eight always-on descriptions start over-triggering |
| `07-neg-gherkin-question` | **nothing fires** on a question in this vocabulary | a description grabs on vocabulary rather than intent |
| `08-fix-it-while-recording` | `record-clip` files what it noticed instead of fixing it, and ships a clip rather than a still | it edits the wording "quickly first", or accepts a PNG as the deliverable |
| `09-setup-confirms-before-writing` | **`setup` says what it will write and waits**, in the repository that most obviously needs it | it starts installing — a `specs/` tree, a `CLAUDE.md`, a gate script — however good the plan beside it |
| `10-gate-deferred-twice` | `refine-workflows` stops on a gate row deferred across two changes, and never asserts a check the ledger says is unwired | it adds the workflow and leaves the unwired gate as a third flag nobody closes |
| `11-neg-setup-adjacent-request` | **`setup` does not fire** on a CI question asked in a repository that has not been set up | the newly visible `setup` description grabs on "gate" and "set up" rather than on intent |
| `12-setup-drives-the-sitting` | **`setup` finishes what it names** — the interviews are started rather than listed, the repository's real tracker is written down, an existing CLAUDE.md is audited, and the pull-request report is wired and cannot gate | the sitting ends with a skeleton and a list of commands to run later |
| `13-feedback-about-the-plugin` | **a complaint about a skill reaches the plugin's tracker**, when the human says that is what it is | it files against the app being worked on, where livespec's maintainer never sees it |
| `14-feedback-with-no-subject` | `feedback` **asks** where a genuinely ambiguous report belongs, and files nothing until told | it settles on one — files, or hands over the command to file into one tracker as though the question were answered |
| `15-tracker-is-not-the-assumed-one` | `feedback` uses **the tracker the bindings name**, and builds evidence links for that host | `gh` or a `raw.githubusercontent.com` URL turns up in a repository that is not on GitHub |
| `16-setup-with-no-app-code` | **`setup` asks what proves a rule** where there is nothing to call, and reaches for the tool that already builds a suite | it adopts graded cases silently, or invents a case format next to a generator |
| `17-wiring-nobody-watched-run` | **`setup` will not claim wiring nobody watched run** — the ledger says `unobserved`, and the hand-back says what could not be watched | the sitting signs off a gate it never saw refuse anything |
| `18-request-with-no-usage` | `feedback` captures a wish nobody has used the app to want, and demands no usage report first | a feature request has to arrive dressed as a bug to be tracked at all |
| `19-neg-instruction-is-not-filed` | **`feedback` does not fire** on an instruction to make the change | the widened description takes "add drag-to-reorder" as something to queue rather than build |
| `20-repository-with-no-bindings` | **`feedback` says what the repository does not record and hands the work over anyway** — in a repository with no bindings at all, the finding is stated once and the researched body still arrives | the session goes hunting for a file nobody wrote, and ends holding the obstacle instead of the work |
| `21-a-workaround-already-recorded` | **`feedback` records a workaround the repository is keeping**, names the filed mismatch that would end it, and says once that it is following the one already there | the workaround is followed silently, or the row waits on an issue number nobody here can create |
| `22-nothing-moves-in-this-one` | **`record-clip` picks the form from what changed, not from the series** — a change finished the moment it is on screen gets a still, and the request for a GIF to match the last two is answered rather than obeyed | it pads a static result into an animation so the file type stays consistent |
| `23-what-a-change-here-must-show` | **`setup` writes a deliverable row that answers what a change here must show**, in a repository whose gate is already wired and whose bindings were never written | the bindings come back a restatement of the method, with nothing in them only this repository knows |
| `24-a-ledger-nobody-read-back` | **`doctor` does not settle a claim it cannot reach** — the required-check row comes back unread rather than confirmed from a workflow file, the coverage row is reported as covering the Python half only, and two pieces of never-gating wiring move out of prose into rows | a CI file is read as evidence about branch protection, or a note saying *not built yet* is repeated back instead of being put on a clock |
| `25-neg-a-red-job-is-not-an-audit` | **`doctor` does not fire** on a failing check somebody wants debugged | the new description grabs on "check", "gate" and a job name rather than on intent |
| `26-two-seconds-before-the-push` | **`setup` offers the free half of verification before a push**, keeps the graded suite and the check nobody can clear here out of it, and gives it no ledger row | the hook runs `make verify` whole — billing per push and blocking on a stale board — or turns up in the tree unannounced, or is recorded as a gate |
| `27-a-red-nobody-here-can-clear` | **`setup` leaves a repository able to say which of its two reds happened**, keeps the report *and* the gate under it running on the red one, and commits work whose only failure is a measurement waiting on a run | the freshness check is downgraded or dropped to get green, the suite is run to clear it, the work is stranded because verification is red, or the gate is made to run by being given `continue-on-error` |
| `28-a-hook-is-not-a-row` | **`doctor` tells a courtesy from a refusal** — the rule-bound measure comes out of a prose note and becomes a tracked row, while the pre-push hook described beside it in the same voice gets none | the hook is given a row, most temptingly *unobserved* on the strength of nobody having checked whether it is switched on, or is counted toward what the repository enforces |
| `29-nowhere-to-draw-it` | **`refine-spec` draws nothing and says so** — three spellings of one setting become one, with no before, no ledger and no count that moves | a page is produced anyway to fill the space, or the absence goes unmentioned, or it is blamed on the session rather than on there being nothing to show |
| `30-a-threshold-nobody-chose` | **`setup` recommends the whole of what is in scope, not the number the tree already scores** — and answers "it has to be green on the first run" by naming the untested importer as an exclusion rather than by giving away points | a threshold is taken off the current coverage report, or the day-one gap is cleared by a smaller demand instead of a named exclusion |
| `31-nothing-to-see-is-not-both-rows` | **`setup` writes the sketch row beside the picture's exemption**, in a daemon with no interface anywhere — the picture is genuinely exempt here and the sketch is not | one *nothing to see* is written once and read as covering both, which is the bindings every repository set up before 0.27.0 already has |
| `32-a-row-that-did-not-exist-yet` | **`doctor` catches what the bindings never heard of** — the sketch a change owes before approval is missing because the step postdates the file, and no build here could ever have said so | the absence goes unreported, or the deliverable row is taken as covering it, or that row's *nothing to see* is stretched over both |
| `33-no-tool-to-publish-with` | **`refine-spec` makes the sketch the other way** — the change it just specced has an obvious before and after, there is no tool here that publishes a page, and this session writes files | the missing tool is read as having nowhere to draw it and no page is made, or a summary, table or mock-up is pasted in the page's place |
| `34-the-file-the-audit-never-opens` | **`doctor` reads a demand where the gate reads it** — a coverage threshold ratcheted to the score sits in a config no audit pass opens, under a row that correctly reads *automated* and a build that is green by construction; the exclusions are honest, reasoned, and in the bindings rather than in the config | the ledger is passed because every row is accurate and stamped, or `functions: 100` is swept up as a ratchet too, or the session edits the threshold it is holding |

**`02`, `13`, `14` and `15` are the four that hold where an issue goes.** They
are one rule seen from four sides: the ordinary report that resolves without
asking (`02`), the one the human routes explicitly (`13`), the one nobody can
resolve (`14`), and the repository whose tracker was never the assumed one
(`15`). The last is the case with a user behind it — a repository on a
self-hosted host kept its own hand-built `feedback` rather than adopt this one,
and `15` is what stops that regressing.

**`20` is the one that holds what a session does when it cannot finish.** The
other five `feedback` cases stand in repositories that answer them; `20` stands
in one that does not, which
[`0018`](../specs/changes/0018-said-once-not-searched-for.md) argues is the
ordinary case rather than the edge. Both its outcome graders have to pass
together, and that is deliberate: naming the gap without handing over the work
fails it, and so does handing over work that never named the gap. Either alone
is a session somebody has to repeat.

**`26` is the case with a fixture built to make the wrong answer attractive.**
`beacon`'s one command runs the free gates, a graded suite that bills about
$4.10, and a freshness check whose only cure is one of those runs — so the
obvious hook, the one that runs the whole command, charges its owner per push
and blocks every push the moment a case goes stale. What separates a pass from a
fail here is whether cost was used as the criterion or whether the split
happened to come out right.

`09`, `11` and `12` hold `setup`, and they hold three different halves of it —
`09` the stop before writing, `11` the staying out, `12` everything after the go.
`12` is also the only case that **walks a workflow**: it carries
`workflow:adopt-the-process`, and the traceability gate fails that workflow the
moment this case is deleted. It is the longest and most expensive case here, and
the first one to suspect when the suite gets slow or a run hits `max_turns`.

**It now carries eight graders and seven rule claims**, which is more than any
other case and is worth watching rather than growing. Everything on it is a
promise about what one sitting leaves behind, so it is coherent — but the moment
a claim lands there because `12` was the convenient place rather than the right
one, this stops being one case and starts being a bucket.

It grew again in [`0011`](../specs/changes/0011-how-a-test-claims-a-rule.md), and
the test applied was the one above: the spec-bound coverage split only exists in
a repository that **has** code and a coverage run, which `12` has and
[`16`](16-setup-with-no-app-code/prompt.md) deliberately does not. Right place,
not convenient place — but that is now two versions running, and the next claim
should go somewhere else or `12` should be cut in two.

**`12` and `16` are a pair**, and the pairing is the point: the same sitting in a
repository with an app and in one without. If they ever produce the same bindings
file, section 2's fifth question stopped being a question.

Until the change that made `setup` model-invocable, `09` was a
should-not-fire case of a different kind — it held a skill whose description was
not in context at all, and passed for a reason unrelated to judgment, because
the skill could not be offered even in principle. Now `09` asks whether setup
**fires and then stops**, and `11` asks whether it **stays out of a question
that merely sounds like it**. `11` is the case that pays for the description
being in context: 06 and 07 hold the other six from grabbing too much, and `11`
holds the one that was added to them.

In the without-plugin arm, `09` remains the case that shows what a bare model
does with the same request, which is invent a process.

`26-two-seconds-before-the-push` is the case with a history worth knowing before
its number is read. It was measured at **Δ −0.33** on 2026-08-28 (`452bcc3`) —
the only case in the suite whose own change had made it negative — and
[#67](https://github.com/sargismarkosyan/livespec/issues/67) was filed on it:
one with-plugin session had spent its turns hunting a `Bash` tool no case grants
and ended on a clarifying question, one grader was lost to the judge crashing,
and the bare arm scored 1.00 three times out of three, which is a fixture a
competent baseline aces.

**The decision is to keep the case as it is**, and it was made on a re-measure
rather than on an argument. On 2026-08-30 the rule it claims gained an example,
so the entry went stale and was re-run at the floor: **with 1.00, without 0.78,
Δ +0.22**. The with-arm scored 1.00 in all three runs — including the two that
never wrote `specs/setup/README.md`, because offering the hook and waiting for an
answer is what the rule asks for — and the bare arm lost ground on the graders
asking where the hook runs and what it leaves to CI. So the fixture does
discriminate, the spiral did not recur, and the −0.33 stands as a fact about
`452bcc3` rather than as a live defect. It is written down here because a Δ that
size, seen cold, is worth exactly one re-open and no more.

The negative cases are the ones to watch. Eight skills' descriptions load in
every session, and the cost of widening one — or, as with `setup`, of making one
visible at all — is paid here — where it should show up as a scored failure rather than as a user
wondering why an interview started.

## The floor

These are not negotiable when the suite is edited:

- **at least one should-NOT-fire case** stays in the suite;
- **every case has at least one outcome grader**; `tool_used` alone is never a case;
- **`runs: 3` minimum**, because a single run of an LLM grader is noise. The
  board holds the same floor from the other end: a number that came back from
  fewer runs is kept and shown, never counted as a measurement, and never
  written over one that cleared it — see *The board*;
- **every skill is held by at least one case.** A skill nothing holds costs
  context in every session and cannot be changed safely;
- **every case says which skill it holds**, in `tags:` — `skill:<name>`. A case
  may also carry `rule:<id>` or `workflow:<id>` once the rule it answers to
  exists, and a claim that names nothing fails. The contract is in
  [`specs/setup/README.md`](../specs/setup/README.md);
- **`--ablation with-without` stays**, because a score without a baseline is not a
  measurement;
- **`--judge-model sonnet` or larger**, and never the model under test — a small
  judge misses exactly the nuance these cases turn on, and the agent's own model
  prefers its own output;
- **`--allow-tools` grants every gated tool the cases ask for.** `Write`, `Edit`,
  `Bash`, `WebFetch`, `WebSearch` and `mcp__*` are refused unless the person
  running the suite grants them, whatever a case's own `allowed_tools` says. Run
  without the grant and a case that *could* have edited a file never gets the
  chance — so a grader asserting it edited nothing passes without proving
  anything, in both arms. `evalsuite.py` checks this one rather than trusting it.

**No case grants `Bash`.** These cases are about filing issues and writing specs,
`gh` is authenticated wherever the suite runs, and a case that files a real
GitHub issue while being graded is not a test. If a case ever needs a shell, it
needs a `case.yaml` scaffold and a sandbox first.

The first five of those are checked by the gates in `.github/scripts/` —
`evalsuite.py` for the suite's shape, `trace.py` for what a case claims — and
`inject.py` breaks each of them in a fixture to prove the check still fires. The
last two — the ablation and the judge model — are flags rather than files, so
what is enforced is that this file still names them. That is a weak guard, and it
is deliberately a guard on the *documentation* rather than a pretence of one on
the run.

A grader softened until it always passes is a vanity metric. If a case is failing
and the fix is to loosen the rubric, the question to answer first is what version
of that grader would still catch a real regression.

## Calibration

Pilot before trusting a full run:

```
python3 evals/runner/run.py --runs 1 --ablation with-without --judge-model sonnet --allow-tools Write Edit --scaffold
```

Then, against the run directory it prints (`evals/results/<stamp>/`):

1. Check the summary's **fired** column. A fire case showing `0/1` in the
   with-arm means the plugin never triggered there — and if that is every case,
   the with-arm ran bare and the whole pilot is meaningless.
2. Watch the run output for `⚠ <case> asks for <tool>; not granted`. A case
   whose grader needs a file that no granted tool can create scores 0 in both
   arms and reads as "the plugin did nothing".
3. Read every judge verdict — each one is a `reason` in the run's
   `results.json`, or `npx promptfoo@0.122.0 view` shows them in a browser. If
   you would have scored even one differently, the rubric is not ready.

**A pilot cannot take a measurement's row.** `--runs 1` is below the floor, so
`run.py` writes its number only where the board holds nothing or holds another
number below the floor; against a case already measured at three runs it keeps
the measurement, prints `✋ <case>: 1 run(s) is below the floor…`, and leaves the
pilot's numbers where a pilot's numbers belong — in the summary above and in the
run directory. This is not fastidiousness about an old number: the row is also
what clears the freshness gate, so a pilot written into it loses the measurement
*and* turns the red that was asking for a real run green. Both happened to `26`
on 2026-08-29 — a $1.21 single run replaced a $4.67 three-run entry and flipped
its sign, and nothing recorded that it had ([#75](https://github.com/sargismarkosyan/livespec/issues/75)).

Cost: the summary line prints what the pilot's sessions actually cost; a full
suite is roughly that × 3. Sessions, transcripts and created files stay under
the run directory, which is ignored — the evidence is local and reproducible.
What survives a run is its summary, on the board.

## The board

[`evals/board.json`](board.json) — committed — holds, per case, what the last
run measured: `delta`, both arms, `runs`, when, at what commit, what it cost,
and an `inputs` hash of what the number was a measurement *of* — the case's own
files, the text of every rule it claims, and the body of every skill it holds.
`run.py` updates the entries for whatever it ran, automatically; a `--case`
smoke updates one row, and its `runs` field says how much weight it deserves.

Change any of those inputs and the hash stops matching: the entry is **stale**,
and the board gate — `.github/scripts/board.py`, run by `verify.py` — fails the
build naming the cases and the one command that heals them:

```
python3 evals/runner/run.py --changed --ablation with-without --judge-model sonnet --allow-tools Write Edit --scaffold
```

`--changed` selects exactly the cases without a fresh measurement — a reworded
rule re-measures the cases that claim it, never the whole suite. A case with no
entry at all only **warns**: that is the bootstrap state, and the warning list
is the first pilot's to-do list.

**An entry below the floor warns too, and is not counted.** `runs` is read
rather than merely recorded: an entry from fewer than three runs is listed, kept
and shown, left out of the mean, and not reported as measured. It is not a
failure — the number is the best the board has, and calling it coverage is the
part that would be a lie. Staleness is still asked of it first, because a number
that no longer describes these files is wrong however many runs produced it. The
floor lives in `caselib.py` with `is_measurement()` and `replaces()`, so the
gate, the runner and the suite gate cannot come to different conclusions about
what a measurement is.

On the day this was wired the board went from *28 measured, mean Δ +0.29* to
**5 measured, 23 below the floor, mean Δ +0.44**, without a session being run.
Nothing regressed and nothing improved; the average had been taken over 22
single runs and one two-run entry as though they were measurements.

**The score is never gated.** A Δ of zero ships; a stale Δ does not. What the
gate enforces is that a number still describes the files it claims to — gating
the number itself would turn the suite into something to be optimised at, which
is the same failure this repository already refuses for coverage.

The pull-request report carries the board's counts — measured, stale, never —
and the mean Δ over the fresh entries, dated, because a pull request rarely
re-runs the suite and the row must say so rather than look current.

## When a case needs a repository

Most cases are deliberately self-contained — the situation is in the prompt, and
the graded judgment does not depend on a `specs/` tree existing. The signal that
one has outgrown that is exact: the agent spends its turns hunting for
`specs/setup/README.md` rather than answering. `01` fired it on the suite's very
first run (#38), so since then the runner executes scaffolds:

- the case gains a `case.yaml` beside its `prompt.md`, naming a
  `scaffold_script:` — a bash script in the case directory, in the native
  format the gates already read (`caselib.py` merges the two files' fields);
- `run.py --scaffold` runs that script in the session's fresh workspace before
  `claude -p` starts, **in both arms alike** — an arm handed a different
  repository would make Δ a comparison of two different questions;
- the flag is opt-in, exactly as the native runner's: a scaffold is
  author-supplied bash running as the operator, so it runs only on case files
  they trust. Run without it and the runner warns per scaffolded case rather
  than silently measuring the stall — and `evalsuite.py` fails if a scaffolded
  suite's documented invocation here ever drops the flag, or if a declared
  script does not exist;
- the `files` a grader sees are what the session wrote — anything the scaffold
  laid down is excluded unless the session changed it, which is what lets a
  fixture carry a `src/` tree that *arms* `no-source-edits` instead of tripping
  it in both arms.

Convert cases as their runs demand it, never all at once: a fixture is one more
thing to keep true, and a case that discriminates without one is cheaper to
trust. `01`, `14` and `15` were converted after a run showed the empty
workspace was what got measured — `01` on the suite's very first run (#38),
`15` (#40) as the bare model beating the plugin, `14` (#58) as the same shape
one case over, both arms replying that they could not tell where anything went.
`20` and `21` were written with fixtures from the start, because in those two
the repository *is* the situation.

Two of them show what a scaffold may leave out on purpose. `15`'s omits the
screenshot its prompt names, because saying so plainly is part of what the case
grades. `14`'s omits anything that would say who wrote the badly titled issue —
a fixture that settled that would answer the question the case asks.
