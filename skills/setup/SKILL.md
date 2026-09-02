---
name: setup
description: Set this process up in a repository — read what is already there, wire the two gates in that project's own language, write specs/setup/README.md as its bindings, write or audit CLAUDE.md, and then run the persona, workflow and journey interviews rather than naming them. Use when adopting livespec in a new or existing repository, when asked to initialise the specs, wire the traceability gate, "set up the process here", or when a repo has the plugin enabled but no specs/setup/README.md for the skills to read. Interviews for what only the human knows, proves every gate fires before handing back, and never writes application code.
---

# Set the process up here

Every other skill in this plugin reads `specs/setup/README.md` before it assumes
a command. **This skill is what puts that file there**, along with the gates it
describes and the CLAUDE.md that points at both.

**It writes no application code, ever.** And it does not invent a persona, a
workflow or a journey — those are [`refine-personas`](../refine-personas/SKILL.md),
[`refine-workflows`](../refine-workflows/SKILL.md) and
[`refine-journeys`](../refine-journeys/SKILL.md), each its own interview and its
own change spec. What this skill produces is the structure they land in and the
gate that keeps them honest — and then, in section 8, it starts them.

## First: say what this will do, and wait to be told to start

**Claude can start this skill. It may not start the work.** Those are different
things, and the gap between them is this section.

Setting the process up writes `CLAUDE.md`, creates a `specs/` tree, adds gate
scripts, edits `.claude/settings.json` and — since section 8 — continues into
three more interviews. That is a decision with the human's name on it, and a
repository looking ready for it is not the same as somebody asking for it.

So before anything is written, say in a few lines:

- **what you will write**, by path, and what you will edit rather than create;
- **anything that already exists and would be overwritten**, listed by name —
  a CLAUDE.md somebody wrote by hand is context, not clutter;
- **that three interviews follow the setup itself**, so the length of the sitting
  is known before it starts rather than discovered halfway through.

**Then wait.** Not a rhetorical pause — an actual stop, with nothing written
until they answer. "Yes", "go ahead", or an instruction to change the plan are
all answers. Silence is not, and neither is a request that merely sounds nearby:
somebody asking what the CI does, or tidying a `specs/` folder that already
exists, has not asked for this.

If they came here by typing `/livespec:setup`, they have already asked to start
the skill — but they have not yet seen the list, so they still get it and still
get the stop. It is shorter that time, because the answer is usually yes.

## 1. Read the repository before writing anything

Find out what is true, and say it back before you touch a file:

- **Language, test runner, coverage tool, package manager.** Whatever is already
  installed wins. Do not add a dependency to satisfy this process.
- **The command that already means "everything passes."** Most repos have one.
  It becomes the verification command; a second one nobody runs is worse than
  none.
- **CI**, if there is any: what runs, and what the required check is called.
- **Existing documentation** — a README, a CLAUDE.md, an ADR folder, a `docs/`
  tree. Some of it is already the context this process wants; it gets pointed at,
  not rewritten.
- **How issues are filed here.** A tracker and the command that reaches it, a
  `CONTRIBUTING.md` line, an issue template, a `/feedback` skill of their own.
  This is the answer to requirement #10 of
  [`claude-md.md`](../../method/claude-md.md), and **nothing else in this skill
  will go looking for it** — every other requirement falls out of work you are
  already doing, and that one does not. "There is no convention" is an answer;
  it gets said out loud rather than left blank.
- **Greenfield or occupied?** A repository with 40,000 lines already in it is a
  different job from an empty one, and section 7 is about the difference.

Say what you found in a short paragraph. If the repo has no tests and no CI at
all, say that too — the process still installs, but the coverage gate has nothing
to stand on yet and the bindings file must admit it rather than name a threshold
nobody measures.

## 2. Ask the five things you cannot find out

One round, with your recommendation attached to each. Everything else you decide
yourself and record.

- **What is being built, and what is the deliverable of a version?** A moving
  picture per version is this method's default and the reason the loop ends where
  it does. A repo with no UI answers differently — a benchmark number, a
  changelog entry, an example script that runs. Whatever it is, it has to be
  something a person can look at.
- **Who is it for?** One sentence, and one sentence on who it is *not* for. This
  is the seed for the persona layer, not the persona — do not write the file from
  this answer, hand it to `refine-personas` afterwards.
- **What is the verification command, and what is the coverage gate over?** Ask
  what is in scope and what is excluded from it, rather than what percentage to
  settle on, and recommend the whole of what is left — **100% of it**, once the
  exclusions are named. Say that figure rather than leaving it to be worked out:
  a recommendation nobody can put a number to is one nobody can refuse, while
  the wrong answer — today's score — arrives already converted. It is 100% of
  what *remains*, never of the repository. A threshold set at what the code
  scores today is a ratchet that never moves, and every point between it and the
  score is regression no build will report. An occupied repository does not get a
  lower number to fit its untested modules: those are named as exclusions, each
  with its reason, and the demand over the rest stands. Nothing fails on day one,
  because the day-one exclusion list is exactly today's uncovered code written
  down — and it shrinks in a diff instead of creeping in a number.
- **Is `main` protected, and what is the required check called?** If nobody can
  change repository settings, say so in the bindings — an unenforceable rule
  written as enforced is the worst line in any setup file. **Their answer is
  where to start looking, not what gets written down**: this is a setting on the
  platform, and section 5 reads it back from there before the row is written.
- **What proves a rule is true here, and how does a test say which rule it is
  answering?** Both gates rest on this and nothing else can derive it.
  [`testing.md`](../../method/testing.md#first-what-proves-a-rule-is-true-here)
  has the two honest answers — an ordinary test suite, or graded cases where the
  product is judgment rather than code and there is no function to call.
  **Recommend what the repository already runs**, and never stand up a second way
  of testing alongside one that works. Where the answer is graded cases, say
  plainly that they prove a weaker thing, so it is chosen rather than drifted
  into.

## 3. Put the skeleton in, and nothing more

```
specs/
  spec.md                what it is, the vocabulary, the storage contract
  personas/README.md     the layer's own rules
  workflows/README.md
  journeys/README.md
  features/
  changes/
  setup/README.md        the bindings — section 5
tests/
  behaviour/  unit/  workflows/
docs/screenshots/        or whatever the deliverable turned out to be
```

**Create a directory when something goes in it, not before.** A tree of empty
folders and placeholder files reads as a process that was installed and never
run, and the traceability gate cannot tell an empty layer from a broken one.

The layer READMEs are worth writing now, because they are what stops the layers
being filled in wrong. Everything else waits for the skill that owns it.

## 4. Wire the gates, in the project's own language

[`gates.md`](../../method/gates.md) says what they have to mean. This is where
that gets turned into commands.

**Traceability**, both directions, is the one that has to be built rather than
configured:

- read the `.feature` files, collect every `@rule:` id and its `@planned` state;
- read the test sources and collect every rule id they claim — a function call,
  a decorator, a docstring tag, whatever suits the language;
- fail when a live rule has no test, when a test names an id that does not exist,
  when a behaviour test claims nothing at all;
- then the layer above: features name workflows, workflows name personas and are
  walked by a test, journeys name workflows that exist.

**Write the smallest thing that does that.** One script, no dependencies, in the
language already in the repo. It is a few hundred lines at most and it belongs in
the repository rather than in this plugin, because CI has no plugins installed —
the moment verification depends on something an agent session installs, it stops
being the thing CI runs.

**The rule binding is part of the gate, not a convenience.** Section 2's fifth
answer decides its shape; either way the sitting leaves behind the thing a test
uses to name its rule.

- **An ordinary test suite** gets a helper that wraps the runner's grouping call
  — `rule('<id>', …)` — looks the id up in `specs/features/`, and **throws where
  the test is written** if it does not exist or is still `@planned`. Without it,
  a rule id is a string inside a test name: unchecked, undiscoverable, and
  impossible to rename from the spec. That failing at authoring time rather than
  in CI is most of what this binding buys.
- **Graded cases** get their suite from the tool that already builds one.
  `claude plugin eval init <name>` writes it, interviewing in a terminal by
  default, with `--bare` for a blank template; the case-folder layout is the
  non-interactive path. **Point at the tool and read what it produces — do not
  describe its output from memory, and do not hand-roll a case format.** A
  bespoke layout invented in a sitting has one user and no documentation.
  **And run the tool before the sitting recommends it.** Where it is gated or
  absent — `plugin eval` is behind early access on some accounts, and livespec's
  own suite hit exactly this — set up a platform that already runs graded
  suites (promptfoo is one) and keep the cases in the format the repository's
  gates read, so the native runner arriving later is a bonus, not a migration.

**Coverage** is whatever the language already has. Lines, branches and functions
if the tool reports all three; the demand and the exclusions are the ones agreed
in section 2. If the tool reports only lines, say so in the bindings and say what
that misses.

**The exclusions go where the tool reads them**, in its own config rather than in
a paragraph beside it. A list only the bindings know about is a second copy of
the gate, and the two disagree the first time either moves. Where the tool cannot
exclude anything, the binding names a number and says that is the shape it is on.

**Take it twice.** The gated number is over everything; the second pass is over
the rule-bound tests alone, and it says how much of the product the specification
actually reaches. It goes in the report and
[**never in a threshold**](../../method/testing.md#measure-the-rule-bound-tests-on-their-own-and-never-gate-it)
— gated, it turns rules into a way of moving a number. Where the repository's
tooling cannot split a coverage run, say so in the bindings rather than reporting
one figure twice.

**One command runs both**, and CI runs that same command. Not a longer list in CI
than a person can run locally.

### Then offer to run it before the push

One command that a person can run locally is the precondition for the thing
nobody has yet been offered: **firing it automatically before the work leaves
this machine.** Ask.
[`testing.md`](../../method/testing.md#and-again-before-it-leaves-this-machine)
is the rule; this is where it gets proposed to somebody who can say no.

**Say what it would be, and wait.** A `pre-push` hook is the usual shape —
`.githooks/pre-push` running the command, and `git config core.hooksPath
.githooks` to turn it on — and the second line is the whole opt-in, so it is
worth saying out loud that a clone without it has nothing installed. **Then stop
and let them answer.** A hook that turns up unannounced is the same defect as a
gate nobody agreed to, and it gets switched off rather than argued with.

**Pre-push, not pre-commit**, and give the reason rather than the preference: a
ten-commit branch runs the same checks ten times to learn the same thing once,
and a check that expensive stops being kept somewhere around the fourth commit.
Push is the last moment the work is still only yours.

**Then say what will not be in it, in the same breath.** Cost is the selection
criterion, so the hook carries the free and fast half — the gates, the type
check, the unit tests, the linter — and two things stay out even though the one
command runs them:

- **a graded suite**, which must refuse to start without a per-run approval from
  whoever is paying. A hook is exactly the automatic trigger that rule forbids,
  and wiring one in bills them per push.
- **any check whose failure cannot be cleared here for free** — stale eval
  bookkeeping being the usual one. Red for a reason the method sanctions, fixable
  only by a run somebody has to pay for, and indistinguishable to a hook from a
  broken gate. Leave it to the pipeline.

**Leaving it to the pipeline is only an answer if the pipeline can say which red
it is.** So where the verification command can fail for a reason the method
sanctions, the repository leaves this sitting able to tell that apart from a
broken gate — in what the command returns as much as in its last line — and with
its pull-request report **not** skipped on the failure it exists to describe.
[`graded-cases.md`](../../method/graded-cases.md#freshness-is-gated-the-score-never-is)
says why this is not a nicety: a red nobody can act on gets investigated a few
times, found innocent every time, and then stops being read — and a gate nobody
reads still counts as coverage to everybody looking at the list.

Where the verification command runs both kinds, **the hook runs the free part by
name, from the same list the command already reads.** A hook with its own copy of
that list is a second answer to *what does verification mean here*, and it goes
stale the first time a gate is added.

**It is not a gate, and it does not become one.** No row in either ledger table —
[`gates.md`](../../method/gates.md#and-what-is-not-wiring-at-all) says why a
bypassable courtesy recorded as a refusal is worse than no record. **And nothing
comes out of CI because a hook exists**: every check that blocked a merge before
this still blocks it. If it is written down, it goes in the bindings' prose as
something true of one machine — what it runs, what it leaves to the pipeline, and
the line somebody types to opt in.

**Declining is an answer, and it ends here.** Write nothing, say nothing about it
in the ledger, and carry on with section 5.

**A repository with two languages in it has one coverage gate, not two.** Two
per-language checks, each with its own threshold and its own way of failing, are
two gates nobody agreed to and no single number anybody can quote — and the third
language, added a year later by somebody who never read this file, silently gets
none at all. Blend them into one measurement where the tooling allows it. Where
it does not, the gate still runs once and the ledger row **says which part of the
repository it does not cover**, because a row that stays quiet about that will be
read as covering everything.

### Then break them, one at a time

A gate that has never failed is not known to be a gate. Walk the
[injection table](../../method/gates.md#both-gates-are-verified-to-fire): break
each row in turn, run the gate, read the message it produces, revert. **Record
the results in `specs/setup/README.md`.**

This is the step that gets skipped, and skipping it is how a repository spends
six months with a required check that has been passing on an empty glob.

## 5. Write `specs/setup/README.md` — the bindings

This is the file every other skill reads. It has to answer, in one table a person
can scan: what verification is, what runs each gate, where the rule-claiming
helper lives, how tests are discovered, what the coverage thresholds are, what
the required check is called, where the app runs, what a pull request has to
carry, and anything else a skill would otherwise have to guess.

**Wire the report too, and say so when you cannot.**
[`gates.md`](../../method/gates.md#the-report-is-not-a-gate) expects a repository
to end up posting one on its pull requests: what the change did to the spec
layer, read from the traceability gate's own output rather than worked out again,
placed where somebody deciding whether to merge is already looking. It runs after
both gates pass and **it must not be able to fail the build** — not on a missing
token, not on its own errors. Where the repository's pull requests cannot carry a
comment at all, the hand-back says the report is not wired and why; what it must
never do is read as though it were.

**The tracker row is not optional and is not cosmetic.** Section 1 already found
how issues are filed here; this is where that answer becomes something a skill
can read — the host, and the command that files there. Without it every skill
falls back to guessing, and a guess that lands in the wrong tracker is invisible
to everybody: no error, no second copy, and nobody told. Write the row even when
the answer is the obvious one, and write *"there is no tracker"* when there is
none rather than leaving it blank.

**One of those rows is easy to leave out and expensive to add later.** A pull
request in this repository carries the deliverable — the picture, and the Gherkin
it moved, per
[`repository.md`](../../method/repository.md#every-pull-request-shows-what-it-did).
Write the row saying what that means *here*: **which changes owe a picture and in
what form**, where it goes, and which paths make the Gherkin owed. A repository
that adopts the process without that row keeps merging changed promises nobody
read.

The form half is the one that gets left as a habit. *Something happens on screen*
and *the whole result is a screen sitting there* are answered per change forever
unless the row says how this repository decides, and a repository with no screen
at all writes **that** down — the method's *nothing to see* line becomes the
standing case here rather than the exception somebody invokes.

**Then write the second row, and do not let the first one absorb it.** A change
here also owes a **sketch** before it is approved — the evidence its change spec
argues from, per
[`process.md`](../../method/process.md#the-rules). Say which changes here owe
one. The two rows are one word apart and the exemption only belongs to the
first: the picture is recorded from the app, the sketch is drawn from the change
spec, and **a repository with no screen still has change specs.** Writing
*nothing to see* once and letting it cover both is the failure this row exists
to stop, and it is likelier than leaving the row out.

It also carries what cannot live in a diff: the branch protection settings, the
CI wiring, and the record of the fault injection from section 4.

**Read those settings back from the platform before writing them down, and put
the command that reads them again beside the table.** A required check named in
a CI config says a job runs; whether a merge is *blocked* when that job fails is
a different setting, often somewhere else entirely, and on some platforms it is a
project-wide switch that nothing in the pipeline file mentions. A table filled in
from what the tree implies is confident, tidy and about nothing —
[`repository.md`](../../method/repository.md#branches-and-pull-requests) says why
this is the one gate that gets that treatment. The same goes for a credential the
wiring needs: *there is no token for this* is a claim about the platform, and
tokens inherited from a level above the repository are invisible to anybody
reading the repository.

**Every fact in it is about this repository.** If a sentence could survive being
moved to another repo, it belongs in this plugin instead, and putting it here is
how the two copies start to disagree.

### The gate wiring ledger

One more table, and the one that outlives you: a row for **every** gate named in
[`gates.md`](../../method/gates.md#what-is-wired-and-what-is-not) — not only the
ones you wired — each reading *automated* (naming the command), *unobserved*
(wired, and nothing has watched it run), *not applicable* (with the reason) or
*deferred* (since which change, and why). Above it, the date and the version of
livespec the wiring was reconciled against.

**A gate you wired in section 4 reads *unobserved*, not *automated*.** Breaking
it against the injection table proves the gate; it does not prove this
repository's pipeline runs it. Section 8 is where those rows get their answer.

**A row about anything outside the repository carries how it was read**, per
[`gates.md`](../../method/gates.md#what-is-wired-and-what-is-not) — the command
that reads it again, and when. That is a second axis rather than a fifth state:
branch protection read back from the platform is still *unobserved* until it has
stopped something. And **a row says what it does not cover**, so a gate wired
over part of this repository is not recorded as covering it.

**Then the second table: the wiring that must never gate.** The pull-request
report and the rule-bound coverage measure are both expected here and neither can
fail a build, which is exactly why both go missing quietly. They get
[their own short table](../../method/gates.md#the-wiring-that-must-never-gate),
same four states, same two-change clock. Writing *not built yet* about either one
in a sentence somewhere puts it on no clock at all, and nothing will ever ask
again.

Most rows on a fresh setup say **not applicable**, and honestly: there are no
personas yet, so the gate over them cannot apply yet. Write *deferred* only where
the layer exists and the check does not — writing it where *not applicable* is
true is how a repository ends up carrying a permanent apology, and writing *not
applicable* where a gap is real is how it carries an unbuilt gate for a year.

**Re-reading this ledger later is [`doctor`](../doctor/SKILL.md)**, which audits
it against this page without re-running any of the interviews. Say so when you
hand back: the ledger is the one artefact here that is typed once and trusted for
years, and the first person to read it again should not have to reconstruct this
sitting to do it.

**Installing over a repository that already has a ledger: diff it, never
overwrite it.** Read what it was reconciled against, compare its rows to the
gates that page names now, and report the difference — rows the method has since
gained, rows naming a command that no longer exists, deferrals past the
two-change limit. Then offer to wire what is missing. Re-stamp the version only
when the wiring actually moved; a ledger re-stamped for a run that changed
nothing has learned to lie. Rows you cannot date honestly say **predates the
ledger** rather than getting an invented change number.

## 6. Write CLAUDE.md, or audit the one that is there

Follow [`claude-md.md`](../../method/claude-md.md) — it says what has to be in
it, what must stay out, and why. **It is a list of requirements, not a file to
copy.** A CLAUDE.md assembled by filling in somebody else's blanks reads exactly
like one, and the agent that has to trust it can tell.

**A file that already exists does not make this step done.** It is context
somebody wrote by hand — and it is also the file every agent trusts by default,
so it gets read against the ten requirements rather than counted. Go through them
in order and mark each **met**, **missing** or **stale**; a pointer to a path that
moved is worse than no pointer. Say that list out loud before touching anything,
then show the edit and make it.

The ones an occupied repository's own file is usually missing, because nothing
ever made anybody write them: **#2** (who writes what), **#4** (the line between
the plugin and this repository), and **#10** (where issues go — which you found
in section 1). **Do not hand back with #10 unwritten.** Every other requirement
falls out of work this skill does anyway; that one is only there if you put it
there.

## 7. An existing codebase does not get retroactive specs

The temptation is to spec what is already built. Do not.

- **Write nothing about behaviour that already exists** except where a change is
  about to touch it. Forty backfilled change specs are forty documents nobody
  checked against the code, and the gate cannot tell an accurate one from a
  guess.
- **The spec layer starts at today.** The first change spec is numbered `0001`
  and describes the next change, not the history.
- **Existing tests do not have to claim a rule.** They are unit tests as far as
  this process is concerned until a rule exists that they answer to. Say this in
  the bindings, or someone will spend a week retrofitting decorators.
- The exception is a rule the codebase *already* breaks: that is not
  documentation, it is a bug, and it goes through `feedback` like any other.

## 8. Enable the plugin, then keep going

Declare the marketplace and enable the plugin in the repository's
`.claude/settings.json`, so a fresh clone gets the process without a manual
install.

Then report, short:

- the verification command, and the fact that it is green;
- which faults you injected and that each one failed the way it should;
- **which gates are not wired**, read off the ledger rather than remembered, and
  for each whether it is deferred or cannot apply here;
- the requirement list from section 6, and anything in CLAUDE.md still missing;
- **what is still empty** — the personas, the workflows and the journeys.

### Then fill them, in the same sitting

**Naming the next command is not handing over — it is stopping one step early.**
A repository that ends here has a correct skeleton and a list somebody now has to
remember, which is section 3's warning wearing a different hat.

So say that three interviews follow, and run them in order:
[`refine-personas`](../refine-personas/SKILL.md), then
[`refine-workflows`](../refine-workflows/SKILL.md), then
[`refine-journeys`](../refine-journeys/SKILL.md). The order is not a preference —
a workflow written for nobody has to be written twice, and a journey over
workflows that do not exist yet is a guess.

**The sittings are chained. The approvals are not.** Each of those skills runs
its own interview, writes its own numbered change spec, and gets its own
confirmation before the next one starts. That separation is
[process.md](../../method/process.md)'s rule about a change to the personas or
the workflows, and a chain collecting three approvals in one breath has broken
it rather than gone faster.

**Stop the moment they say stop.** It is a long sitting, and "that is enough for
today" is a complete answer. A skill in the chain that stops on its own — on a
ledger row deferred twice, say — ends the chain there too, and that is the ledger
working rather than the chain failing. Either way, hand back with where it
stopped and what is left, which is a shorter list than the one you started with.

### Then land it, and watch the pipeline hold it

The interviews wrote change specs. **Commit them and open one pull request in
this repository** — that is the last act of the sitting, and the first time
anything here has been more than configured.

What is on trial is not the specs. It is the wiring, so report what came back:
whether the required check ran and what it said, and whether the report arrived
on the pull request. A check that **refuses** it is the wiring working — say
which of the two happened in as many words, because a red tick nobody explains
reads as an install that broke something.

**Do not merge it.** Opening it is the demonstration; merging is a decision that
was never yours. And nothing else goes in it — the spec layer this sitting
wrote, and no application code.

**Where you cannot: say so, and mark those ledger rows *unobserved*.** No
remote, no CI, no permission to open one — all fine, and all different from
having watched it work. Never leave a bindings row asserting a behaviour nobody
ran; that is the miss this whole step exists to stop, and it is the one an
adopter finds months later with no way to tell which claims were real.

**And name what closes them.** Those rows come back to *automated* the first time
somebody watches the wiring do its job — the hand-back says that
[`doctor`](../doctor/SKILL.md) is what re-reads them, so the next reading is a
command rather than an act of memory.

## What this skill refuses

- **Starting the work because it was asked to consider it.** Claude may now
  reach this skill on its own. What it may not do is write the first file before
  the list above has been shown and answered — including when the repository
  obviously needs it, which is every repository this skill ever runs in.
- **Writing application code.** Not one line, including a test for code that
  already exists.
- **Merging what it opened.** The pull request at the end of section 8 is
  evidence, not a change somebody approved.
- **Inventing a persona or a workflow** from the seed in section 2. The seed is
  an answer to "who is this for", not a design artifact, and treating it as one
  is how a product ends up built for somebody nobody ever met.
- **Answering the interviews it starts.** Section 8 runs three skills; it does
  not supply their replies. A chain that fills in the human's answers has
  installed the process on top of a persona nobody chose.
- **Adding a dependency** to make the process fit. If the gate needs a library,
  it is too big.
- **A coverage number nobody chose.** Copied from another repository, or
  subtracted from this one's own score — both arrive without anybody having
  decided what the points they give away stand for.
- **Installing over an existing setup without saying what it will overwrite.**
  Show the list first; a CLAUDE.md somebody wrote by hand is context, not clutter.
