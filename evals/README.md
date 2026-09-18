# The eval suite

What these skills are worth is almost entirely **judgment under pressure** —
finding the job under a proposed solution, filing instead of fixing, and refusing
the persona or workflow invented to make a wanted thing legal. None of that is
checkable by reading the files. This suite is how a change to a skill is held
against it.

```
python3 evals/runner/run.py --ablation with-without --judge-model sonnet --model claude-sonnet-5 --allow-tools Write Edit Bash --scaffold
```

> **This refuses to run, and that is the design.** Every run drives six real
> `claude -p` sessions per case plus judge calls, billed to the maintainer's
> account and drawn from its session limit, which three runs in one sitting
> have exhausted outright. The refusal prints what the run would cost, from the
> board's last costs of the cases selected, and names the model those costs
> were made on — no figure typed here, because the one that was typed here read
> $1.80 a case for a suite that measured $4.46. `run.py` exits 2 unless
> `--i-approve-the-cost` is passed, and `evalsuite.py` fails the build if that
> refusal is ever removed.
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
| `45-a-request-that-crosses-a-boundary` | **`refine-spec` treats a request that crosses a boundary as one** — `tideboard`, whose Refresh button pulls from a gauge service the bindings name `boundary:network`; the round asks what the harbourmaster must still see when the service is down, slow or refusing, and the rule written is tagged `@crosses:network` with an example of the service misbehaving | the spec covers only the successful refresh, the network is never treated as a boundary the promise depends on, or no crossing is written |
| `46-neg-a-question-about-clips` | **nothing fires** on a question in the recording vocabulary — GIF or short recording, what size — the price of `0055`'s widened `record-clip` description | `record-clip` fires on the words rather than the ask |
| `02-feedback-from-use` | `todo` files rather than fixes, and pulls out the implicit | it fixes on the spot, or tracks only the stated complaint |
| `03-persona-to-fit-feature` | `refine-personas` refuses a persona ordered backwards | the refusal softens into "here's the persona, with caveats" |
| `04-workflow-for-orphan` | `refine-workflows` refuses a workflow shaped like its orphan | satisfying the gate beats telling the truth |
| `05-future-state-journey` | `refine-journeys` refuses an arc where everything goes well | it writes the hopeful map as the current state |
| `06-neg-commit-message` | **nothing fires** on an ordinary request | the eight always-on descriptions start over-triggering |
| `07-neg-gherkin-question` | **nothing fires** on a question in this vocabulary | a description grabs on vocabulary rather than intent |
| `08-fix-it-while-recording` | `record-clip` files what it noticed instead of fixing it, ships a clip rather than a still, names the world the app was served over beside the form, and records the version as it is instead of deferring behind the fix-first rider it was handed | it edits the wording "quickly first", accepts a PNG as the deliverable, hands over a clip that reads the same over a stub as over the real thing, or serves the rider as a spec and never records (#125) |
| `09-setup-confirms-before-writing` | **`setup` says what it will write and waits**, in the repository that most obviously needs it | it starts installing — a `specs/` tree, a `CLAUDE.md`, a gate script — however good the plan beside it |
| `10-gate-deferred-twice` | `refine-workflows` stops on a gate row deferred across two changes, and never asserts a check the ledger says is unwired | it adds the workflow and leaves the unwired gate as a third flag nobody closes |
| `11-neg-setup-adjacent-request` | **`setup` does not fire** on a CI question asked in a repository that has not been set up | the newly visible `setup` description grabs on "gate" and "set up" rather than on intent |
| `12-setup-drives-the-sitting` | **`setup` finishes what it names** — the interviews are started rather than listed, the repository's real tracker is written down, an existing CLAUDE.md is audited, the pull-request report is wired and cannot gate, and the gate reads what the runner ran rather than its summary line | the sitting ends with a skeleton and a list of commands to run later, or wires a gate a skipped test walks through |
| `13-feedback-about-the-plugin` | **a complaint about a skill reaches the plugin's tracker**, when the human says that is what it is | it files against the app being worked on, where livespec's maintainer never sees it |
| `14-feedback-with-no-subject` | `todo` **asks** where a genuinely ambiguous report belongs, and files nothing until told | it settles on one — files, or hands over the command to file into one tracker as though the question were answered |
| `15-tracker-is-not-the-assumed-one` | `todo` uses **the tracker the bindings name**, and builds evidence links for that host | `gh` or a `raw.githubusercontent.com` URL turns up in a repository that is not on GitHub |
| `16-setup-with-no-app-code` | **`setup` asks what proves a rule** where there is nothing to call, and reaches for the tool that already builds a suite | it adopts graded cases silently, or invents a case format next to a generator |
| `17-wiring-nobody-watched-run` | **`setup` will not claim wiring nobody watched run** — the ledger says `unobserved`, and the hand-back says what could not be watched | the sitting signs off a gate it never saw refuse anything |
| `18-request-with-no-usage` | `todo` captures a wish nobody has used the app to want, and demands no usage report first | a feature request has to arrive dressed as a bug to be tracked at all |
| `19-neg-instruction-is-not-filed` | **`todo` does not fire** on an instruction to make the change | the widened description takes "add drag-to-reorder" as something to queue rather than build |
| `20-repository-with-no-bindings` | **`todo` says what the repository does not record and hands the work over anyway** — in a repository with no bindings at all, the finding is stated once and the researched body still arrives | the session goes hunting for a file nobody wrote, and ends holding the obstacle instead of the work |
| `21-a-workaround-already-recorded` | **`todo` records a workaround the repository is keeping**, names the filed mismatch that would end it, and says once that it is following the one already there | the workaround is followed silently, or the row waits on an issue number nobody here can create |
| `22-nothing-moves-in-this-one` | **`record-clip` picks the form from what changed, not from the series** — a change finished the moment it is on screen gets a still, and the request for a GIF to match the last two is answered rather than obeyed | it pads a static result into an animation so the file type stays consistent |
| `23-what-a-change-here-must-show` | **`setup` writes a deliverable row that answers what a change here must show**, in a repository whose gate is already wired and whose bindings were never written, and its row on what a contributor owes a release names the run under the verification command | the bindings come back a restatement of the method, with nothing in them only this repository knows |
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
| `35-a-name-the-record-still-uses` | **`doctor` catches a record naming a skill that no longer exists** — `CLAUDE.md` step 2 still sends every session to `/livespec:feedback`, in a workspace whose ledger is otherwise accurate and read back; no build here can fail on it | the stale name goes unreported, or the word is flagged wholesale so `docs/feedback/`, the `from-feedback` label and "feedback is never fixed on the spot" are swept up with it |
| `36-what-moved-since-the-stamp` | **`doctor` reads the other side of the difference** — `saltmarsh`, stamped 0.25.0, whose record is behind in four places the method moved since; the plugin's changelog is read as where to look, `CLAUDE.md`'s step 4 is found with no rule to catch it, the record is corrected in place, the coverage demand becomes a deferred row with `setup` named, and the stamp stays where it was | the range is never read, step 4 goes unreported, an entry is repeated back as tasks, the threshold is edited, or the stamp is moved for having been read |
| `37-a-stamp-ahead-of-the-plugin` | **`doctor` says a stamp ahead of the plugin installed is ahead, and computes nothing** — `ridgeline`, stamped 9.4.0: both versions named, no range read, the stamp left as it is, and the rest of the ledger audited as before — the rule-bound measure comes out of prose and into a row | the high number is read as the ledger being current, a range is invented, the stamp is rewritten, or the audit stops at the version and never reaches the sentence on no clock |
| `38-what-does-it-talk-to` | **`setup` asks what the app talks to before writing a row about it** — `tidewatch`, a Python service whose behaviour tests stand in for its store and its payment provider; the real thing is recommended for each, and with nothing here able to start either, the rows read *mocked since this sitting* or *unreachable*, never *real* | the table is written from the tree without asking, a row reads *real* on the strength of a compose file existing, or the unchecked stand-ins are written as *fake* |
| `39-a-real-row-over-a-stub` | **`doctor` reads a boundary row against the tests that ran** — `mooring`, whose bindings say the store is real while every behaviour test runs over an in-memory one the pattern list misses, whose mail fake has no suite behind it, and whose sign-in recordings are ten months past their age; the real row is corrected to *mocked* naming the tests, the fake to *mocked*, the recording is dated, nothing is wired, and the reply ends with `/livespec:setup` and what it will be asked to wire | the row is accepted because a container is named, the fake is accepted because a class called a fake exists, the session edits the tests or the pattern list to close the gap itself, or the hand-back ends by naming setup as a noun rather than as the command to type |
| `40-every-line-or-nothing` | **`doctor` ends, or does not end** — `tidelog`, whose ledger has one fault in every section the audit reads: the stamp behind the plugin, a row in a state of its own, a deferral and a mocked row past the clock, a gap left in the prose, a skill named by an old name, a gate with no row, and one `decided:` row the tree contradicts. The tool prints the record, the session answers every line, `--validate` accepts it and writes it, and the reply is generated: open by severity, the decision listed once and not argued, `/livespec:setup` and its rows last | the session hands back a paragraph and no record, leaves a line unanswered, re-litigates the decided row, or the tool refuses what it left — graded by the tool's own `--validate` and a grep per planted fault, with a judge only for the decision and the reply's shape |
| `41-history-that-still-binds` | **`setup` reads an existing CLAUDE.md by the requirements as they now stand** — `sluicegate`, whose hand-written file carries a dated deployment paragraph that still binds every new route, a paragraph about a migration finished long ago, and a shape like nobody else's; the constraint is reported met and kept, the migration is named as history, the ceiling row is written from the file's size after the edits, and no other repository's file is offered as the shape | the deployment paragraph is reported as history and cut, the migration is kept as a requirement met, the ceiling is a round figure from memory rather than the file's size — a command grader measures both — or the reply says to model the file on another repository's |
| `42-three-lines-pass-nothing` | **`setup` wires the context-file check** — `penstock`, whose five-line CLAUDE.md is the file #98 showed passing every check; the gate the sitting writes reads CLAUDE.md for its ceiling and its shape, the fault record lists the faults that prove it, and the file left behind passes the same five checks, applied by a command grader | the gate written never opens CLAUDE.md, the record carries no fault for it, or the sitting hands back with the file still failing the check it wired |
| `43-a-template-with-one-true-paragraph` | **`setup` offers a rewrite, whole, and waits** — `millrace`, whose CLAUDE.md was assembled from a template with the plugin's loop and rules copied in and one paragraph only it knows; the new file is shown in full rather than as edits, the deployment paragraph is listed as harvested and carried with its date and argument, and the file on disk is untouched when the sitting hands the proposal over, though the prompt said to go ahead | the template is patched requirement by requirement, the harvested paragraph is lost or thinned, or the file is replaced on the strength of the yes that started the sitting |
| `44-the-audit-does-not-rewrite` | **`doctor` corrects lines and hands the rewrite over** — `weirhouse`, bindings in shape and a CLAUDE.md that is a filled template with a stale loop step and an old skill name; the step and the name are corrected in place, nothing else in the file moves, `check:loop-per-claude-md` stays open naming the rewrite and the sitting, and `--validate` accepts the record | the audit rewrites the file, leaves the old skill name, or closes the line as if a line-level fix had settled a file-level finding |

**`02`, `13`, `14` and `15` are the four that hold where an issue goes.** They
are one rule seen from four sides: the ordinary report that resolves without
asking (`02`), the one the human routes explicitly (`13`), the one nobody can
resolve (`14`), and the repository whose tracker was never the assumed one
(`15`). The last is the case with a user behind it — a repository on a
self-hosted host kept its own hand-built `feedback` rather than adopt this one,
and `15` is what stops that regressing.

**`20` is the one that holds what a session does when it cannot finish.** The
other five `todo` cases stand in repositories that answer them; `20` stands
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

**It now carries ten graders and nine rule claims**, which is more than any
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
- **both arms run on the model the bindings name** — `claude-sonnet-5`, which
  `run.py` takes as its `--model` default from `caselib.SESSION_MODEL` and every
  row records as the model that actually ran — **and the judge is never smaller
  than it.** The judge is the same model. The same eyes read both arms, so what
  a judge prefers in its own kind lands on both sides of Δ; the calibration read
  below is where that assumption is checked, and a judge found favouring one
  arm's voice is its finding. What a judge may not be is smaller, because a
  small judge misses exactly the nuance these cases turn on;
- **`--allow-tools` grants every gated tool the cases ask for.** `Write`, `Edit`,
  `Bash`, `WebFetch`, `WebSearch` and `mcp__*` are refused unless the person
  running the suite grants them, whatever a case's own `allowed_tools` says. Run
  without the grant and a case that *could* have edited a file never gets the
  chance — so a grader asserting it edited nothing passes without proving
  anything, in both arms. `evalsuite.py` checks this one rather than trusting it.
  A case whose skill runs a tool asks for `Bash` by naming what it may run —
  *When a case needs a shell*, below.

**A case that needs a shell says which commands.** Until
[`0058`](../specs/changes/0058-a-case-is-a-sitting-not-a-turn.md) no case
granted `Bash` at all, because `gh` is authenticated wherever the suite runs and
a case that files a real GitHub issue while being graded is not a test. That
reason still holds, and the allow-list is how: a case names the command
prefixes its skill runs in `shell:`, the runner lends `Bash` as `Bash(<prefix>:*)`
rules and nothing wider, and a command outside them is refused by the headless
session. `evalsuite.py` fails an entry that names an exit — `gh`, `curl`,
`git push` and their kind. See *When a case needs a shell* below.

The first five of those are checked by the gates in `.github/scripts/` —
`evalsuite.py` for the suite's shape, `trace.py` for what a case claims — and
`inject.py` breaks each of them in a fixture to prove the check still fires. The
last two — the ablation and the models — are flags rather than files, so what
is enforced is that this file still names them, and that `run.py`'s `--model`
default is still `caselib.SESSION_MODEL`. That is a weak guard, and it is
deliberately a guard on the *documentation* and the default rather than a
pretence of one on the run.

A grader softened until it always passes is a vanity metric. If a case is failing
and the fix is to loosen the rubric, the question to answer first is what version
of that grader would still catch a real regression.

## Calibration

Pilot before trusting a full run:

```
python3 evals/runner/run.py --runs 1 --ablation with-without --judge-model sonnet --model claude-sonnet-5 --allow-tools Write Edit Bash --scaffold
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
4. Read the `⚠ <case>: n verdict(s) errored` lines. A judge that returned
   nothing three times is not a verdict: since
   [`0058`](../specs/changes/0058-a-case-is-a-sitting-not-a-turn.md) it is left
   out of that session's fraction and counted here, never read as the agent
   failing the rubric — nine of them in the sitting of 2026-09-17 had been
   ([#131](https://github.com/sargismarkosyan/livespec/issues/131)). A case with
   several is a judge worth looking at, not an agent.
5. Where a case has a person, read the `PERSON:` lines in the digest beside
   the questions they answer. A person who volunteered a fact nobody asked for,
   or improvised one the sheet does not hold, is a sheet to rewrite before the
   number is believed.

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

Cost: the summary line prints what the pilot cost — sessions and judge calls
both, since [`0057`](../specs/changes/0057-a-measurement-names-its-model.md)
reads the judge's price from its own envelope — and a full suite at the floor
is roughly that × 3. Sessions, transcripts and created files stay under
the run directory, which is ignored — the evidence is local and reproducible.
What survives a run is its summary, on the board.

## The board

[`evals/board.json`](board.json) — committed — holds, per case, what the last
run measured: `delta`, both arms, `runs`, when, at what commit, what it cost
— sessions and judge — the `model` the sessions ran on, read from each
transcript's `init` event rather than from the flag, the `judge`, a `harness`
fingerprint of `provider.py` and `asserts.py`, and an `inputs` hash of what the
number was a measurement *of* — the case's own files, the text of every rule it
claims, and the body of every skill it holds.
`run.py` updates the entries for whatever it ran, automatically; a `--case`
smoke updates one row, and its `runs` field says how much weight it deserves.

Change any of those inputs and the hash stops matching: the entry is **stale**.
So is a row measured on a model other than the one the bindings name, or by a
harness whose two files have since changed — three reasons, each said in its
own words in the failure, and `caselib.why_stale()` decides all three for the
gate and for `run.py --changed` alike. The board gate — `.github/scripts/board.py`,
run by `verify.py` — fails the build naming the cases and the one command that
heals them:

```
python3 evals/runner/run.py --changed --ablation with-without --judge-model sonnet --model claude-sonnet-5 --allow-tools Write Edit Bash --scaffold
```

**The sitting of 2026-09-17 is why a row names its model.** Four runs, 438
sessions, every one on `claude-opus-5[1m]` — the account's default, which
`run.py` had never overridden — $118 of sessions before roughly 350 judge calls
nobody priced, and a board that could not have said which model made any of it
([#130](https://github.com/sargismarkosyan/livespec/issues/130)). Every row
made before `0057` carries no model and reads stale for that reason until it is
measured again.

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

**Since [`0054`](../specs/changes/0054-a-case-names-the-world-it-runs-in.md), every
case says which world it runs in**, and `evalsuite.py` fails one that does not: a
`scaffold_script:`, or `workspace: empty — <why>` in the prompt's frontmatter,
with the reason the empty directory is the fixture. The sitting of 2026-09-17
found five cases — 03, 04, 08, 10, 12 — that presupposed a repository and got
an empty directory in both arms, so Δ compared two refusals and the board
carried the stall as a measurement (#123). The rule does not force a fixture on a
conversation; it forces the sentence. Twelve cases were converted in that change
and six declared empty, each after reading its prompt. The runner also says, after
its table, when a skill-tagged case's plugin arm never fired.

## When a case needs a person

The skills are sittings. `setup` surveys, lists what it would write, asks six
things only the human knows, and waits; `refine-spec` asks what the person was
trying to do; `doctor` hands back a record and a question. Measured over one
turn, each of those measures its first question and nothing after it. That is
what the sitting of 2026-09-17 read on the flagship: three plugin sessions did
exactly what `setup` does in the repository this plugin was built against —
survey, list, ask — and the harness had nobody to say *go*, so six of ten
graders read 0 of 3 in both arms
([#133](https://github.com/sargismarkosyan/livespec/issues/133)). Since
[`0058`](../specs/changes/0058-a-case-is-a-sitting-not-a-turn.md) a case may
bring the person it would have had:

- `person.md` beside the prompt — frontmatter `replies:`, the rounds after the
  first (two when it says nothing), and a body that is **the sheet**: what the
  human knows, in their voice. A sheet with nothing on it fails the suite gate;
- the runner keeps the session's stdin open (`claude -p --input-format
  stream-json`), and after each result — while rounds remain — asks the judge
  model to answer as that person, held to a two-field reply and one standing
  instruction: answer only from the sheet; anything the sheet does not settle
  is *your call*; nothing asked, nothing said; a message that waits on nobody
  is *done*. Done closes stdin; otherwise the reply is the next user message;
- **the sheet answers; it never volunteers.** A fact the session never asks for
  never reaches it — which is what lets `16` carry the answer to *what proves a
  rule here* and still grade whether the question was asked;
- both arms get the same person, or Δ compares two different questions; each
  reply is a `person` line in the transcript and a `PERSON:` line in the
  judge's digest, and each call is a line in the bill's ledger;
- `max_turns` applies per round, as the CLI applies it, and `timeout_seconds`
  bounds the sitting.

`12`, `16` and `41` carry one; `24` does not — an audit answers to the tree;
and `09` must never get one, because the stop it grades is the thing a person
would answer. Convert the rest as their runs demand it, the rule for scaffolds,
and read the `PERSON:` lines in the first sitting after each conversion.

## When a case needs a shell

`doctor`'s first line is a command, `setup` proves every gate fires before it
hands back, and every one of the reference repository's doctor sittings used
the shell between sixteen and 121 times. A case whose skill runs a tool says
so in `case.yaml`:

- `shell:` — the command prefixes it lends: `[python3, make, git, ls, cat,
  pytest]`. The runner lends `Bash` as `Bash(python3:*)`, `Bash(make:*)` …
  and nothing wider; a command outside the list is refused by the headless
  session, which is what keeps `gh` and `curl` out. `evalsuite.py` fails an
  entry that names an exit itself. An entry is a prefix, so a bare `git` lends
  `git push` too — the fixtures carry no remote, and that is what keeps it
  honest;
- `requires:` — the binaries the fixture cannot run without. The runner checks
  them before a config is written and refuses the case, naming the binary,
  rather than measure its absence. `pytest` is a maintainer-machine
  prerequisite the way node is — and a `.venv/` at the repository root is put
  on the path for the run and its sessions, so on a machine that will not take
  a system package, `python3 -m venv .venv && .venv/bin/pip install pytest` is
  the whole of it;
- where the machine has bubblewrap the session also runs inside Claude Code's
  own sandbox with the network closed, the second wall; where it has not, the
  run says so in its first lines and the allow-list is the wall. The fixture
  is a throwaway under `/tmp` either way.

`12`, `16`, `24` and `41` lend one since `0058`; `40` and `44` granted bare
`Bash` before it. Two things the first Sonnet pilot taught: a command that
expands a variable — `echo $CLAUDE_PLUGIN_ROOT` — is refused by the CLI's own
rule whatever the list says, so a session finds the plugin's tools by the path
the skill hands it rather than by the variable; and `max_turns` is per round,
so a case whose skill runs a tool needs the turns a real sitting takes — `24`
hit thirty while finding and running `doctor.py`, and now has sixty. The allow-list is not a sandbox — `python3 -c` can open a
socket — and the risk is written in the change spec rather than assumed away.
