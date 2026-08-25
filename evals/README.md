# The eval suite

What these skills are worth is almost entirely **judgment under pressure** —
finding the job under a proposed solution, filing instead of fixing, and refusing
the persona or workflow invented to make a wanted thing legal. None of that is
checkable by reading the files. This suite is how a change to a skill is held
against it.

```
claude plugin eval . --ablation with-without --judge-model sonnet --allow-tools Write Edit
```

> **Not yet piloted, and currently unrunnable.** `claude plugin eval` is
> compiled into the CLI but gated per organisation during early access: on this
> account it prints `` `plugin eval` is currently in early access `` and exits
> before it reaches case discovery, whatever arguments it is given. Nothing local
> causes that — enablement arrives server-side and needs `claude update` and a
> fresh session. So these cases have never been run. The first person who can run
> them should treat the first pass as calibration — read every judge verdict and
> ask whether they would have scored it the same way — and correct the rubrics
> before anyone trusts a number from here. See *Calibration* below.
>
> What *is* enforced meanwhile is the structure: `python3 .github/scripts/verify.py`
> fails if a skill is held by no case, if a case is graded only by what fired, if
> `runs` drops below three, if the last should-not-fire case is deleted, or if the
> invocation below loses its baseline. That proves a case exists and **can** fail.
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
| `06-neg-commit-message` | **nothing fires** on an ordinary request | the seven always-on descriptions start over-triggering |
| `07-neg-gherkin-question` | **nothing fires** on a question in this vocabulary | a description grabs on vocabulary rather than intent |
| `08-fix-it-while-recording` | `record-clip` files what it noticed instead of fixing it, and ships a clip rather than a still | it edits the wording "quickly first", or accepts a PNG as the deliverable |
| `09-setup-confirms-before-writing` | **`setup` says what it will write and waits**, in the repository that most obviously needs it | it starts installing — a `specs/` tree, a `CLAUDE.md`, a gate script — however good the plan beside it |
| `10-gate-deferred-twice` | `refine-workflows` stops on a gate row deferred across two changes, and never asserts a check the ledger says is unwired | it adds the workflow and leaves the unwired gate as a third flag nobody closes |
| `11-neg-setup-adjacent-request` | **`setup` does not fire** on a CI question asked in a repository that has not been set up | the newly visible `setup` description grabs on "gate" and "set up" rather than on intent |
| `12-setup-drives-the-sitting` | **`setup` finishes what it names** — the interviews are started rather than listed, the repository's real tracker is written down, an existing CLAUDE.md is audited, and the pull-request report is wired and cannot gate | the sitting ends with a skeleton and a list of commands to run later |
| `13-feedback-about-the-plugin` | **a complaint about a skill reaches the plugin's tracker**, when the human says that is what it is | it files against the app being worked on, where livespec's maintainer never sees it |
| `14-feedback-with-no-subject` | `feedback` **asks** where a genuinely ambiguous report belongs, and files nothing until told | it picks one and files — a wrong pick here is invisible to both maintainers |
| `15-tracker-is-not-the-assumed-one` | `feedback` uses **the tracker the bindings name**, and builds evidence links for that host | `gh` or a `raw.githubusercontent.com` URL turns up in a repository that is not on GitHub |
| `16-setup-with-no-app-code` | **`setup` asks what proves a rule** where there is nothing to call, and reaches for the tool that already builds a suite | it adopts graded cases silently, or invents a case format next to a generator |

**`02`, `13`, `14` and `15` are the four that hold where an issue goes.** They
are one rule seen from four sides: the ordinary report that resolves without
asking (`02`), the one the human routes explicitly (`13`), the one nobody can
resolve (`14`), and the repository whose tracker was never the assumed one
(`15`). The last is the case with a user behind it — a repository on a
self-hosted host kept its own hand-built `feedback` rather than adopt this one,
and `15` is what stops that regressing.

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

The negative cases are the ones to watch. Seven skills' descriptions load in
every session, and the cost of widening one — or, as with `setup`, of making one
visible at all — is paid here — where it should show up as a scored failure rather than as a user
wondering why an interview started.

## The floor

These are not negotiable when the suite is edited:

- **at least one should-NOT-fire case** stays in the suite;
- **every case has at least one outcome grader**; `tool_used` alone is never a case;
- **`runs: 3` minimum**, because a single run of an LLM grader is noise;
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
claude plugin eval . --runs 1 --ablation with-without --no-publish --allow-tools Write Edit
```

Then, in the newest `evals/results/*/aggregate-result.json`:

1. Check `suite.plugins` lists `livespec` with no `problem` of `manifest_invalid`,
   `disabled_by_default` or `will_not_load`. Any of those mean the with-arm ran
   *without* the plugin and the whole pilot is meaningless.
2. Watch the run output for `⚠ case … cannot pass with the granted tools`. A case
   whose grader needs a file that no granted tool can create scores 0 in both
   arms and reads as "the plugin did nothing".
3. Read every judge verdict. If you would have scored even one differently, the
   rubric is not ready.

Cost: the pilot's top-level `costUsd` is cases × 1 run × 2 arms. A full suite is
roughly that × 3.

## When a case needs a repository

These cases are deliberately self-contained — the situation is in the prompt, and
the graded judgment does not depend on a `specs/` tree existing. If a case starts
failing because the agent spends its turns hunting for `specs/setup/README.md`
rather than answering, that is the signal to convert it to a `case.yaml` with a
`scaffold_script` that lays down a minimal fixture (and to run with `--scaffold`,
which is opt-in).
