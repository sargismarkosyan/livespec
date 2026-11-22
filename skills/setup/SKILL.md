---
name: setup
description: Set this process up in a repository, report on it, or bring it up to date. Setting up reads what is there, wires the two gates in the project's own language, writes specs/setup/README.md and CLAUDE.md, then runs the persona, workflow and journey interviews. Reporting re-audits a repository that already has the process — every claim its bindings make, checked against what owns the answer, branch protection read back from the platform — and corrects only the record. Bringing it up to date plans what the plugin installed asks of its ledger and wires it one approved item at a time. Use when adopting livespec, when asked to check or audit the gates or whether the process still holds, when a ledger row has been deferred too long, or after a plugin update. Never writes application code.
---

# Set the process up, report on it, or bring it up to date

Every other skill in this plugin reads `specs/setup/README.md` before it assumes
a command. **This skill is what puts that file there**, along with the gates it
describes and the CLAUDE.md that points at both — and what reads it back later,
and what brings it level when the plugin moves.

**Which of the three this is** is decided by the repository and the request, in
that order:

- **No `specs/setup/README.md`**: set it up — sections 1–8 below.
- **Bindings exist, and the request is to check, audit or ask whether the
  process still holds**: [**Report**](#report-audit-what-the-wiring-here-actually-claims).
  It changes the record and never the wiring.
- **Bindings exist, and the request is to update, upgrade or bring them level —
  or a report just ended naming wiring**: [**Bring it up to date**](#bring-it-up-to-date).

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
scripts, edits each host's settings file — `.claude/settings.json`, and
`.pi/settings.json` where Pi is in use — and — since section 8 — continues
into three more interviews. That is a decision with the human's name on it,
and a repository looking ready for it is not the same as somebody asking for
it.

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

If they came here by typing `/livespec:setup` — `/skill:setup` in Pi — they
have already asked to start the skill — but they have not yet seen the list,
so they still get it and still get the stop. It is shorter that time, because the answer is usually yes.

**A request that already says to write is the answer, given in advance.** *Go
ahead and write*, *you do not need to check back with me before each file* —
that is the yes this section waits for, said before the list. The list is still
said, in the same message, and the sitting continues into it. It is not an
answer to section 2, whose six are facts only they have and are asked either
way; and it never covers replacing a file somebody wrote by hand, which section
6 shows whole and waits on.

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
- **Which hosts run here.** The one this session is in — Pi sets
  `PI_CODING_AGENT=true` in the shell; under Claude Code the skills arrive
  named `livespec:<name>` — and any other the tree shows: a `.claude/`
  directory, a `.pi/` directory. Never assume Claude Code. Section 8 enables
  livespec for each host found, and section 6 reads the instructions files
  knowing which of them each host reads.
- **Greenfield or occupied?** A repository with 40,000 lines already in it is a
  different job from an empty one, and section 7 is about the difference.
- **What a second tree would be missing, and what two would fight over.** The
  ignored files verification and the app need, which a fresh tree would not
  have; everything the app binds, starts or connects to — ports, data
  directories, servers, containers, queues — and which of its per-tree values
  it already reads from its env file; the agent harness's own state kept in
  the tree; and where the repository's existing trees are, read from git's own
  record of them rather than from a folder. Section 4 turns this into the
  command.

Say what you found in a short paragraph. If the repo has no tests and no CI at
all, say that too — the process still installs, but the coverage gate has nothing
to stand on yet and the bindings file must admit it rather than name a threshold
nobody measures.

## 2. Ask the six things you cannot find out

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
  into — **and name the tool in the same breath: `claude plugin eval init
  <name>` writes the suite**, cases as folders of a prompt and its graders.
  Where that tool is gated or absent here, the fallback is said at the same
  moment: the cases are written in the format that tool reads, and a platform
  that already runs graded suites runs them. Under Pi it is absent — it is
  Claude Code's — and that is the same fallback: nobody is sent to install
  another host to get a tool. **A case format of this repository's own is
  never the answer**, and a sitting that finds the tool it cannot run has
  found the format, not a reason to invent one.
- **What does this talk to, and which of those can a test reach for real from a
  session here?** The store, the clock, the network and each service on it, the
  browser or terminal it is used through, whoever it signs people in with — one
  row each, per [`gates.md`](../../method/gates.md#the-boundaries). Ask for the
  list first, then for each whether the real thing can be started here, and
  recommend real wherever it can: a store in a container, a headless browser, a
  pseudo-terminal running the built binary for something used through a
  terminal, a mail catcher, a provider's sandbox. Where it cannot, the row reads
  *fake* only if a suite checks the fake against the real thing, and
  *unreachable* otherwise — never *mocked* on the first day of a fresh
  repository, because a mock nobody chose is the thing this row exists to stop.
  **An occupied repository writes down what is true today.** Its tests already
  run in some world; the day-one rows are that world, named, and a stand-in
  nothing checks reads *mocked* dated from this sitting rather than from
  nowhere — the same shape as the day-one coverage exclusions, which are
  today's uncovered code written down.

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
  walked by a test, journeys name workflows that exist;
- then the world those tests ran in: the same sources, read for the stand-ins
  they use, against the boundary rows — *Then make the real thing reachable*,
  below;
- then the file that points at all of it: CLAUDE.md within the ceiling the
  bindings name — failing where there is no row — at the root, with its loop
  as a numbered list of at most eight steps, a block of commands, and a link
  to the bindings that resolves. **Nothing about its prose**: a stale pointer
  or a copied paragraph is section 6's to catch and the audit's to re-read —
  [`gates.md`](../../method/gates.md#the-file-every-session-reads-first).
- then the parts that only grow: each against its size in the bindings'
  **Ceilings** row, failing a part past it and bindings with no such row —
  [`gates.md`](../../method/gates.md#and-every-part-that-only-grows).

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
  own suite hit exactly this; under Pi there is no `claude` to run — say so in
  one line, write the cases in the format the tool reads anyway — a folder per case holding `prompt.md`, its
  `case.yaml`, and `graders/*.md`, which is the format this plugin's own
  `evals/` is in — and set up a platform that already runs graded suites to
  run them, so the native runner arriving later is a bonus, not a migration.
  What is never done is the third thing: a layout, a tag schema and a grader
  script of this repository's own, which has one user and no documentation.

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

**The runner reports what it ran, per test, where the gate can count it.** The
form is the runner's — a per-test line, a machine-readable report — and it is
a binding, written beside the discovery pattern. The gate compares that count
with the rule-bound tests it found in the tree and fails when the runner saw
fewer; and a rule-bound test carrying the runner's skip, focus or
expected-failure marker claims nothing, which the same gate says naming the
marker — [`testing.md`](../../method/testing.md#behaviour-tests). Where the
runner cannot say per test, say so in the bindings and name what that leaves
open, rather than reading its summary line as the count. Both go into the
injection table: a skipped rule-bound test, and a run that saw fewer than the
tree holds.

### Then wire the report, and make it unable to fail the build

The last gate-shaped thing this section wires is not a gate.
[`gates.md`](../../method/gates.md#the-report-is-not-a-gate) expects a
repository to come out of this sitting posting a report on its pull requests:
what the change did to the spec layer, read from the traceability gate's own
output rather than worked out again, placed where somebody deciding whether to
merge is already looking. It runs after both gates pass and **it must not be
able to fail the build** — not on a missing token, not on its own errors.

Spell it in the words of the platform in front of you. On GitHub Actions it is
a job after the gates with `continue-on-error: true` that posts a comment on
the pull request with the token the workflow already has. On GitLab CI it is a
job with `allow_failure: true` that posts a merge-request note through the API
with the job token. On anything else it is that platform's equivalent, and the
bindings' `wiring:pr-report` row names which. Where the repository's pull
requests cannot carry a comment at all, the hand-back says the report is not
wired and why; what it must never do is read as though it were.

Wire it here, before the hook is offered below: the hook is a question, and a
sitting that runs out of turns runs out after a question, so whatever sits
after the offer is the first thing lost. The report is wiring, not a question.

### Then wire the cost of a walk, beside the report

[`gates.md`](../../method/gates.md#what-a-change-costs-a-workflow) expects each
change to say what it did to the cost of every workflow walk, against its own
base. The walks are the repository's; the comparison ships with this plugin.

1. **Copy it in.** `<plugin root>/tools/walkcost.py` (two directories up from
   this skill file; `$CLAUDE_PLUGIN_ROOT` where it is set) goes into the
   repository beside its gates, with `# livespec walkcost <version installed>`
   written as its first line. CI runs that copy, never the plugin's.
2. **Write the policy file**, its path in the bindings: the rounds per side
   (recommend 5), and for each measure its kind — `time` or `count` — its noise
   and its allowance. No budget until a count has been chosen with the person;
   a time is never given one, and asked for one, offer it reported and a count
   that stands in for it.
3. **Choose the layers and what measures each**, and name them in the
   bindings. What the repository already runs comes first; a tool is proposed
   only for a layer nothing there can measure, with what installing it adds,
   and installed only on a yes. A layer the package does not have is said, with
   why.

   | Layer | Held fixed | Counts | Times |
   |---|---|---|---|
   | front end | the service's answers, replayed (Playwright's HAR replay, or the runner's own) | bytes shipped (size-limit, or the bundler's report) | page load, and each feature's ready mark: a `performance.mark` the app sets once painted, read by the walk |
   | back end | the interface: no browser | queries per request, bytes | requests timed by a load tool (k6) or the language's benchmark library |
   | end to end | nothing | — | the whole walk |

   Each sample names its `layer`.
4. **Wire a job that walks both sides.** Check out the base into a second
   worktree, run every walkthrough on base and branch in turns on the one
   runner — base, branch, branch, base — with what the walkthroughs already run,
   each writing a sample a line as the script's docstring shows. Then run the
   copy with `--samples`, `--policy`, the base's policy as `--base-policy` where
   it has one, the pull request's body as `--body`, and `--gate`; post its
   report the way the report above is posted. The job also runs when the body
   is edited, and the context file says in a line that a walk past its
   allowance is answered under `## Performance`, naming the walk. Say what the job costs in minutes before wiring it.
5. **Write the ledger rows**, `wiring:workflow-cost`, `gate:workflow-budget`
   and `gate:workflow-regression-answered`.
   A repository whose walks cannot be repeated on every change — they bill, or
   take an hour — reads *not applicable* with that reason; one with no
   walkthrough yet reads *deferred* until the first lands.

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
criterion, so the hook carries the free and fast checks — the gates, the type
check, the unit tests, the linter — and **a graded suite stays out**: it must
refuse to start without a per-run approval from whoever is paying, a hook is
exactly the automatic trigger that rule forbids, and wiring one in bills them
per push. Where the verification command runs one, the hook runs the rest by
name, from the same list the command already reads — a second copy of that list
goes stale the first time a gate is added. A graded suite's freshness is never
a gate here or anywhere —
[`graded-cases.md`](../../method/graded-cases.md#neither-freshness-nor-the-score-is-gated).

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

### Then make the real thing reachable, before the gate that assumes it

A row reading *real* is a claim that a test here can start the thing. Wire that
now — the container the suite brings up, the sandbox key the pipeline holds,
the mail catcher — in the repository's own tooling, and run one test through it
before the row is written. This is the suite's tooling rather than the gate, so
the no-dependency rule does not bind it; what binds it is the same rule as the
gates: one command runs it, and CI runs that command. Where reaching the real
thing would need application code written — a seed script inside the app, a
fixture loader — that is the human's, said in the hand-back, and the row reads
*unreachable* until it exists. **The suite may gain tooling; the app gains
nothing.**

Then the gate: the traceability script already reads every rule-bound test
source for the id it claims. It reads the same sources for the patterns the
bindings name as doubles, and fails a test that doubles a boundary whose row
reads *real* — and a *fake* row naming no suite, a *recorded* row past its age,
and rule-bound tests with no table at all. The patterns are the language's and
go in the bindings beside the discovery pattern: propose the usual list — the
mocking, stubbing, fake-timer and interception libraries, and for a terminal
application the framework's own test harness and the tty, environment and
subprocess patches — and let the person strike or add. A hand-written stand-in
the patterns miss is what the report greps for. Add the four rows to the
injection table and break each.

### Then break them, one at a time

A gate that has never failed is not known to be a gate. Walk the
[injection table](../../method/gates.md#both-gates-are-verified-to-fire): break
each row in turn, run the gate, read the message it produces, revert. **Record
the results in `specs/setup/README.md`.**

This is the step that gets skipped, and skipping it is how a repository spends
six months with a required check that has been passing on an empty glob.

### Then make a second tree as ready as the first

Several changes in flight at once is the ordinary case —
[`repository.md`](../../method/repository.md#several-changes-at-once) says what
every tree must be. This is where it gets a directory and a command, and where
they get proved.

**Propose the home and the command, then wait**, the way the hook was offered.
The home is one directory for every tree, ignored — recommend `.worktrees/` at
the repository root: a newcomer sees it, deleting the checkout deletes the
trees, and it sits under no harness's directory. The command is the
repository's own, in its own language, with three verbs: `new` makes a tree on
a branch of the same name and makes it ready — the install, the hook, the env
file copied from its one source with only the tree's own lines changed, a
database of its own on the server already running; `list` shows every tree git
knows about, wherever it lives, with whether it is safe to remove; `clean`
removes every tree with nothing to lose, with its branch and what it held, and
lists the rest with why they stayed. Say what it would write. **Then stop.** A
decline is an answer: the row lists the steps a fresh tree needs, in order,
and the directory.

**Sort every resource from section 1 into its kind** — the tree's own, shared
and started once, or shared and contended — recommending *shared* for a server
and *own* for what lives on it, and asking only where one is contended whether
that is acceptable here. A value the app reads from its code rather than its
env file is named as a change for the app, the person's to file — the sitting
writes tooling and never application code. Where a harness in use has its own
way of making a tree, point it at `new`; never give it a second copy of the
steps, and never name the harness in the command.

**Then prove it, the way the gates were proved.** Make a throwaway tree with
`new`, run verification in it, and — where there is an app — start it beside
the first tree's. Run verification in the first tree while the throwaway
exists and compare the count, so a tool walking into the directory is caught.
Clean the throwaway with `clean` and see the tree list as it was. What came
back goes in the row with the date; a proof that could not be run — a secret
this session cannot reach — makes the row *unproven*, with why, never
*works*.

## 5. Write `specs/setup/README.md` — the bindings

This is the file every other skill reads, and it is written from
[`templates/bindings.md`](../../templates/bindings.md) — copy it and fill it,
the way a persona or a workflow is. The template carries every section a
bindings file has: the key table a person can scan — what verification is,
what runs each gate, where the rule-claiming helper lives, how tests are
discovered, what the coverage thresholds are, what the required check is
called, where the app runs, what a pull request has to carry — the stamp line,
the three ledger tables with the id of every gate already in them, the
workarounds, and the headings the rest goes under. Fill every placeholder or
say why it is empty; a bindings file with an angle bracket left in it was
pasted, not written. **Keep the table headers and the stamp line as the
template has them**: the audit tool reads those and nothing else, and a ledger
in another shape is reported as one the audit could not read.

**The `wiring:pr-report` row names the job section 4 wired** — *Then wire the
report* — or says why there is none; a row reading *deferred* for a report the
platform could carry is a sitting that stopped short, not a decision.

**The tracker row is not optional and is not cosmetic.** Section 1 already found
how issues are filed here; this is where that answer becomes something a skill
can read — the host, and the command that files there. Without it every skill
falls back to guessing, and a guess that lands in the wrong tracker is invisible
to everybody: no error, no second copy, and nobody told. Write the row even when
the answer is the obvious one, and write *"there is no tracker"* when there is
none rather than leaving it blank.

**Then the claim row, beside it — *Claiming an issue*.** With several trees,
an issue handed to two of them is found only when both specs exist, so the
refining skills claim an issue before writing about it
([`repository.md`](../../method/repository.md#several-changes-at-once)), and
they read the marker from here. Read the tracker's labels first: one that
already means *in progress* is the marker, and a second is not made beside it.
Where there is none, **offer to create `in-progress`** — the name and the
command — **and wait**: a label is a write to somebody's tracker, offered the
way the hook is. The row names the marker, the command that puts it on and
takes it off, and the command that lists the issues carrying it. A tracker
that refuses the label goes into the row as *unmade*, with the refusal and
who can make it; no tracker reads *not applicable, decided*.

**Then what a pull request will close — *What a pull request will close*.**
The step that opens a pull request reads back which issues it will close
([`repository.md`](../../method/repository.md#closing-an-issue)), with the
command this row names. **Read it from the platform this repository is on**:
on GitHub `gh pr view <n> --json closingIssuesReferences`, on GitLab
`glab api projects/<id>/merge_requests/<n>/closes_issues`, elsewhere what
that forge's own client answers. Never another platform's command because it
is the familiar one: written there, it is a check nobody can run here.
Run it against a merged pull request that named an issue before writing the
row, so the row carries the date it was watched listing one, or *unobserved*
with why; where it comes back empty, say which line closed nothing. Issues on
another host than the pull requests close nothing on merge: *not applicable,
decided*, and issues close by hand.

**Write the two tree rows from section 4** — **Trees**, with the directory, the
command and the date its proof went green, and **What trees share**, one line
per resource in its kind and the env file's one source. The audit reads the
first back and re-runs the proof.

**One of those rows is easy to leave out and expensive to add later.** A pull
request in this repository carries the deliverable — the picture, and the Gherkin
it moved, per
[`repository.md`](../../method/repository.md#every-pull-request-shows-what-it-did).
Write the row saying what that means *here*: **which changes owe a picture and in
what form**, where it goes, and which paths make the Gherkin owed. A repository
that adopts the process without that row keeps merging changed promises nobody
read.

**The row answers three things, per kind of change, never per repository**:
which changes here owe a picture, in what form — *something happens on screen*
is a recording, *the whole result is a screen sitting there* is a still — and
**which changes owe none**, and get the method's *nothing to see* line in the
pull request instead: a retry backoff, a parser, a migration nobody sees. A row
that answers only moving-or-still has left the third question to be answered
per change forever, and the answer drifts to "every pull request", which is
wrong wherever code runs unseen. A repository with no screen at all writes the
third answer as its standing case — every change owes none — and still writes
the first two as *none here*, so the row is read as decided rather than blank.

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

**Read back, with the rest, whether a merged pull request's branch is
deleted.** A pull request stacked on another merges into its base, and only
the deletion of a merged base retargets it to the main branch; with deletion
off it merges into a dead branch, reads *Merged*, and never reaches a release
([`repository.md`](../../method/repository.md#branches-and-pull-requests)).
Off: say that in a line, **offer to turn it on** — the setting and the
command — **and wait**, the way the hook is offered: it is a change to the
platform, not to the tree. On: write it into the protection table with the
command that reads it and the date. A token the platform refuses makes it
*unobserved*, with who can read it.

**Then how several pull requests merge — the *Several merges at once* row.**
Strict stays; what the row decides is who keeps it
([`repository.md`](../../method/repository.md#branches-and-pull-requests)).
Read from the platform whether it offers a merge queue here. Where only a
write would answer, the write is a rule with enforcement off, aimed at a
branch that does not exist, removed straight after — and a probe that
unexpectedly lands is removed at once and said.
- **A queue is offered:** offer to require it, and to add the queue's own
  event to the workflow that runs the required checks — without it every
  queued merge waits forever. Wait. Then watch one pull request merge through
  the queue before the row says it works.
- **None is offered:** the row reads *not available, decided*, with the
  refusal, and the fallback: the platform updates a branch from main and
  merges it once green, one pull request at a time. Where its settings are
  off, offer them and wait.

**Every fact in it is about this repository.** If a sentence could survive being
moved to another repo, it belongs in this plugin instead, and putting it here is
how the two copies start to disagree.

### The gate wiring ledger

One more table, and the one that outlives you. The template already holds a
row for **every** gate [`gates.md`](../../method/gates.md#the-ids) names, by
id — not only the ones you wired — and each reads *automated* (naming the
command), *unobserved* (wired, and nothing has watched it run), *not
applicable* (with the reason) or *deferred* (since which change, and why).
Each gate and wiring row also carries the version it was reconciled at, and the
stamp line above the table reads the oldest; once the rows are written, run
`python3 <plugin root>/tools/doctor.py --adopt`, which writes every row's version
and the line. A gate this repository has that the method does not name gets a row
too, with the `local:` prefix — held to the same states, required by nothing.
Never invent a `gate:` id: the ids are the method's and permanent, and a row
under one the table does not list is a row no audit can match.

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
same four states, same two-change clock — and a third row beside them: the
report printing the pipeline's own run next to the run block a pull request
carries, *unobserved* until the two have been watched disagreeing. Writing *not built yet* about either one
in a sentence somewhere puts it on no clock at all, and nothing will ever ask
again.

Most rows on a fresh setup say **not applicable**, and honestly: there are no
personas yet, so the gate over them cannot apply yet. Write *deferred* only where
the layer exists and the check does not — writing it where *not applicable* is
true is how a repository ends up carrying a permanent apology, and writing *not
applicable* where a gap is real is how it carries an unbuilt gate for a year.

**Then the third table: the boundaries.** One row per thing the app talks to,
from section 2's sixth answer, in the five states
[`gates.md`](../../method/gates.md#the-boundaries) names, each saying what
reaches it from here, what keeps it honest, what it leaves uncovered, and since
when. Most rows on an occupied repository's first day read *mocked* or
*unreachable*, and honestly: the point of the table is that they now say so
with a date, and a *mocked* row is on the two-change clock from this sitting.

**Re-reading this ledger later is [the report](#report-audit-what-the-wiring-here-actually-claims)**, which audits
it against this page without re-running any of the interviews. Say so when you
hand back: the ledger is the one artefact here that is typed once and trusted for
years, and the first person to read it again should not have to reconstruct this
sitting to do it.

**Installing over a repository that already has a ledger** is not this
section's: it is [*Bring it up to date*](#bring-it-up-to-date), which diffs it and never
overwrites it.

## 6. Write the context file, or audit the one that is there

**First, which file.** The context file is the instructions file the
harnesses here read first — `AGENTS.md` where the repository keeps the
cross-harness one, `CLAUDE.md` where it keeps that. Section 1 already saw
which exists: write or audit **that** one, name it in the bindings' **Context
file** row, and **never create a second beside it** — not even a line
pointing at the other; two files are two copies that start disagreeing.
Where there is none, ask which name the harnesses in use read, recommending
`AGENTS.md` when more than one harness is in use, before writing either. The
rest of this section calls it CLAUDE.md for short; it means that file.

**Where the repository already keeps both** — `AGENTS.md` and `CLAUDE.md` at
the root — it already has the two copies, and one host reads only one of
them: Pi reads the first of `AGENTS.override.md`, `AGENTS.md` and `CLAUDE.md`
in a directory and never the rest, so under Pi a `CLAUDE.md` beside an
`AGENTS.md` is never read, whichever one the gates hold. Say which file each
host found in section 1 reads. Then propose the one file every host in use
reads — `AGENTS.md` wherever Pi is one of them — harvesting what only the
other knew, as below for a rewrite. Show it, and **wait**: removing a file
somebody wrote is the same yes as replacing one. Once it is given, the other
file goes, and the **Context file** row names the one that stayed. A no
leaves both, and says that the audit will keep reporting it open.

Follow [`claude-md.md`](../../method/claude-md.md) — it says what has to be in
it, what must stay out, and why. **It is a list of requirements, not a file to
copy.** A CLAUDE.md assembled by filling in somebody else's blanks reads exactly
like one, and the agent that has to trust it can tell.

**A file that already exists does not make this step done.** It is context
somebody wrote by hand — and it is also the file every agent trusts by default,
so it gets read against the ten requirements rather than counted. Go through them
in order and mark each **met**, **missing** or **stale**; a pointer to a path that
moved is worse than no pointer. Say that list out loud before touching anything.
Then the remedy follows the finding, per
[`claude-md.md`](../../method/claude-md.md#when-it-is-out-of-line):

- **Where the only finding is a line** — a pointer at a path that moved — fix
  the line, show it, and move on.
- **Where anything is missing, or anything the method rules out is present** —
  the plugin's loop or rules copied in, an aspirational rule, history that
  binds nothing — the file is rewritten, whatever it is currently worth, and
  never patched into shape. **Harvest first**: list every fact only this file
  knows, the way you just listed the requirements. Write the new file from the
  requirements, carrying each harvested fact or naming it as dropped with the
  reason and where it lives instead. **Show it whole**, beside what was kept
  and what was dropped, **and stop.** The yes that started this sitting covered
  writing files; it did not cover replacing one somebody wrote by hand, which
  the first section lists as the thing to name before overwriting. The file on
  disk stays as it was until the answer comes; a no leaves it, with the
  line-level fixes made and the rest reported.

**Its block of commands carries the tree command** — `new`, at least — so an
agent starting a change in any harness reaches for it rather than making a
tree by hand. The audit reports the row open while the file does not carry
it.

The ones an occupied repository's own file is usually missing, because nothing
ever made anybody write them: **#2** (who writes what), **#4** (the line between
the plugin and this repository), and **#10** (where issues go — which you found
in section 1). **Do not hand back with #10 unwritten.** Every other requirement
falls out of work this skill does anyway; that one is only there if you put it
there.

**Then write the ceiling row in the bindings, from what the file is now.**
[`claude-md.md`](../../method/claude-md.md#length) puts the number in the
repository rather than in the method: once the file is written, or the audit's
edits are made, measure it and write **Context file ceiling** with the size, the
command that reads it and this change — never before the file is finished,
never from a figure the method does not have, and never above the one it does:
two hundred lines, the reader's own limit, per
[`claude-md.md`](../../method/claude-md.md#length). Raising it later is a line
in the change that needs the room, with the reason beside it. From this sitting on,
the gate wired in section 4 reads that number, so the file you leave behind has
to pass it — and the rest of what that gate reads — before the hand-back.

**And the Ceilings row, at the same moment and the same way:** the code, the
rules under `specs/features/`, and whatever else here only grows, each at its
size once the sitting has finished —
[`process.md`](../../method/process.md#the-rules), *Whatever only grows has a
ceiling*.

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
  documentation, it is a bug, and it goes through `todo` like any other.

## 8. Enable the plugin, then keep going

Declare livespec for every host section 1 found, each in that host's own
committed file, so a fresh clone gets the process without a manual install.
Merge into a file that is already there; never drop what it declared.

- **Claude Code** — declare the marketplace and enable the plugin in
  `.claude/settings.json`, as
  [`method/README.md`](../../method/README.md#wire-it-into-the-repository-instead-of-the-machine)
  shows.
- **Pi** — add livespec to `packages` in `.pi/settings.json`, pinned to the
  release tag of the plugin installed:
  `git:github.com/sargismarkosyan/livespec@livespec--v<version>`, the version
  read from `.claude-plugin/plugin.json` at the plugin root. Pi does not move
  a pinned ref on update, so the pin is what the repository runs until
  somebody moves it. **Say in the hand-back that Pi loads it only once the
  folder is trusted** — a first Pi session that looks ordinary is usually an
  untrusted folder, not a failed install.

A host nobody here runs gets no file: a `.pi/` directory in a repository only
Claude Code opens is a second thing to maintain.

Then report, short:

- the verification command, and the fact that it is green;
- which faults you injected and that each one failed the way it should;
- **which gates are not wired**, read off the ledger rather than remembered, and
  for each whether it is deferred or cannot apply here;
- **which boundaries read *mocked* or *unreachable***, read off the third
  table, and for each what would move it;
- where trees live, the command that makes them, and whether a throwaway tree
  went green — or what kept it *unproven*;
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
on the pull request. Where the change touched a test — the sitting's own rarely
does — the body carries the run under the command as the bindings name it, per
[`repository.md`](../../method/repository.md#and-the-run-it-rests-on), and the
report prints the pipeline's own beside it. A check that **refuses** it is the wiring working — say
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
[The report](#report-audit-what-the-wiring-here-actually-claims) is what re-reads them, so the next reading is a
command rather than an act of memory.

## Report: audit what the wiring here actually claims

A gate wiring ledger is typed by a person, once, usually at the end of a long
sitting. Then it is trusted forever. The report is the second reading — and the
second reading is held to a list, so that what it skipped is as visible as what
it found.

**The report changes the record and never the wiring.** A row that overstates
gets corrected; a gap gets a row. Building what is missing is the sitting's —
sections 1–8, or *Bring it up to date* — and the two are separate passes with
the report committed first, because a pass that both grades and repairs has no
way to be wrong out loud.

### R0. Run the tool first. It owns the list.

```sh
python3 <plugin root>/tools/doctor.py specs/setup/README.md
```

The plugin root is two directories up from this skill file — the harness said
where it loaded this file from — and `$CLAUDE_PLUGIN_ROOT`, where it is set,
names the same place. **The tool is never searched for**: a session running
`find` or reading the environment for it has not read this line. It prints
**the record**: one line per check the method names — the
list is [the id table in `requirements.md`](../../method/requirements.md#the-ids), and it is
enumerated nowhere else — with a state from `clear · open · n/a · unanswered`
and the evidence beside it. **Save what it printed to a scratch file** — not
over the path the bindings name as the audit record, which is the previous
run's and is what the next pass compares against — and work in that file. The lines marked *script* are answered: the stamp
and the range between it and the plugin installed, every row's state and
evidence, the clocks, the tables the method requires, the skill names the
record instructs by. They are answered the same way every time, from the
record and never from the product, and every one of them is broken on purpose
in this plugin's own checks. **Do not re-derive them, and do not argue with
them from memory of the ledger** — the line says what it read and where.

Where it exits **3**, there are no bindings: this repository has never had the
process set up. Say that in one line and stop; sections 1–8 are what it needs,
and offering that sitting is the whole reply.

Where `check:ledger-shape` reads *open*, the ledger predates the template.
The tool has matched what it can by alias; the lines that needed the tables
say so instead of guessing. Carry on with the rest, and see §2.

### R1. Answer the lines marked *unanswered*. Every one.

Each carries the id, the question, and **the command the bindings name** —
read from the row's own *read back with* column, the boundary row's *what
starts it*, the coverage row's config. For each:

1. Run the command shown, or read what it points at. **The tool printed it
   and did not run it** — a bindings cell is text somebody typed, and the
   running is yours, under the person's permission prompts.
2. Replace `unanswered` with one of `clear · open · not-read`, and put beside
   it the first line of what came back, or why it could not be run.

A line that could not be read is `not-read`, with why — no credentials, no
network, no permission. That is a legitimate answer and it validates.
**Silence does not.** A run that leaves a line `unanswered` has not finished,
and §3 will refuse to let it end. An `open` line ends with what closes it; a
`clear` or `open` judgment keeps the command it was answered by beside the
result.

Where a row names no command — a claim about the platform with nothing after
it — the line already says so: the row must name one, and that is a
correction to the record, not a reason to guess. **Handing a line to a subagent
is taking the step, not a way around it**: a second session has the same
tools and returns the same nothing where this one cannot reach the platform.
Once establishes it; write `not-read` and carry on.

**A command this session's own permissions refuse is the same nothing, and one
refusal is it.** The line reads `not-read — refused here`, naming who or what
can read it — a person with the platform's rights, the token the pipeline has
— and the reply carries that name. The same command again — alone, in pieces,
in a subagent, after a `git remote -v` that already showed the host is not
there — is a retry of a no, and the record is not improved by it.

The questions worth the judgment, and what decides them:

- **What a row leaves uncovered** (`check:row-uncovered`). The tool lists what
  the tree is made of — languages by manifest, top-level packages, the
  services the dependencies reach — beside what the rows name. A gate wired
  over one language of two, one package of five, is not a gate over this
  repository; a service the dependencies reach that no boundary row names is
  a boundary nobody wrote down. Say which part has no gate.
- **The number** (`check:number-from-config`, `demand-is-a-ratchet`,
  `exclusions-in-config`). Open the config the coverage gate reads and report
  the demand in it, not the row's description of it. A demand equal to what
  the code scores today was measured rather than chosen — a ratchet, with
  zero slack by construction — **unless it is the whole of what is in scope**,
  which equals the score by construction too and is what `setup` recommends.
  What the demand does not reach belongs in the tool's own config; a list only
  the bindings know is a second copy of the gate. Correct the row and leave
  the number — a threshold is wiring.
- **The boundaries** (`real-starts-here`, `real-not-doubled`,
  `fake-suite-green`). A *real* row over a world the tests never enter is the
  false green the table exists to stop, and it reads exactly like a true one.
  Start what the row names; run the traceability gate and read it for
  doubles. The tests are the authority on what they reach, the way the tree is
  on what applies: a *real* row the tests contradict is corrected to *mocked*,
  naming the tests; a *fake* row with no suite behind it is a mock whatever
  the row called it. A thing that cannot be started from here is `not-read`,
  and a row is not corrected on that evidence alone.
- **The platform** (`merge-blocked`, `check-name`, `who-bypasses`,
  `credentials-present`). A check named in a CI config is evidence that
  somebody wrote it down and no evidence that a merge is blocked when it
  fails; on more than one platform those are separate settings, and one is a
  project-wide switch nobody reading the pipeline file would see. Read them
  back with the command the row names: is the merge blocked, what is the
  check called as the platform has it, who can bypass including the tokens a
  pipeline uses, and is a credential the bindings call missing in fact
  present one level up.
- **Where a stack lands** (`merged-branch-deleted`, `merged-off-main`). Read
  back whether the platform deletes a merged pull request's branch — off is
  `open`, since a pull request stacked on a kept branch merges into it and
  never reaches the main branch. Then list the pull requests merged since the
  stamp's date whose base was not the main branch, and for each ask the
  repository whether its head commit is on the main branch. Each that is not
  is listed with its base and the commit, and the line reads `open`; a stack
  whose commits arrived another way is not. Move nothing: retargeting,
  cherry-picking or reopening is a change of its own.
- **How several pull requests merge** (`merge-queue`). The row says a queue
  or the fallback. A queue: read back that it is required on the main branch
  and that the required checks run on its event in the pipeline — a queue
  whose checks never run hangs every merge and fails nothing. The fallback:
  read back that both its settings are on. Anything not as the row says is
  `open`, naming it; turning a setting on is the sitting's.
- **The range** (`entry-moved-here`). The tool lists the entries between the
  stamp and the plugin installed, and the ids that arrived in them. Read each
  entry for *where to look*, never as a list of tasks: what it asks of this
  repository is read from `gates.md`, [`claude-md.md`](../../method/claude-md.md)
  and the skill as they now stand. An entry that is mostly reasoning asks
  nothing the method does not; one that moved nothing this repository holds
  is passed over in a line. A row that was right under the stamp's version
  and is not right now announces nothing — present, accurate, and stale —
  and having been correct when written is not a reason to leave it.
- **The names** (`word-not-a-skill`, `loop-per-claude-md`). The tool has
  already flagged an instruction — `/livespec:<name>`, or `/skill:<name>` as
  Pi takes it — by a name this plugin no longer has, with the name it now has. What it hands you is the rest: an
  old name in prose, which is an instruction to correct or a dated account to
  leave as written; the same word as ordinary prose, to be left alone —
  reporting one is how this check becomes noise on its second run — and the
  loop's own account, read against what `claude-md.md` now asks of each step.
- **The prose** (`prose-phrases`). The tool lists every *not built yet*,
  *to do*, *we should*, *for now* with its line. Each is a row on the clock or
  it is nothing — *nothing to do at release time* is nothing — and that is
  yours to say, not the script's.
- **What ran** (`gate:skipped-test-claims-nothing`, `gate:fewer-ran-than-exist`).
  A row reading *automated* names how the runner reports per test and what
  counts as a marker here; it reads *unobserved* until somebody has skipped a
  rule-bound test and watched the gate refuse it. A bindings sentence saying
  the runner cannot report per test is a decision to leave as written, with
  what it leaves open beside it.
- **A fresh tree** (`check:trees-row`, `check:fresh-tree-green`). The tool has
  read the row and handed you its command. Make a throwaway tree with `new`,
  outside anything the record covers, run verification there, and `clean`
  it — then read the tree list, which must be as it was. Red is `open` with the
  first failing line and the command left as it is; a secret this session
  cannot reach is `not-read`, with why. Clean nothing but the throwaway: every
  other tree may hold somebody's work, and clearing them is the person's call.
- **Claims in flight** (`check:claim-row`, `check:claims-in-flight`). The tool
  has read the row and handed you the listing command and the marker. For each
  open issue carrying it, read the claim comment's branch against the
  repository's list of trees, the remote's branches and the open pull requests.
  Each with all three gone is listed with its age and session, and the line
  reads `open`; a marker the tracker does not have is `open` too, not `clear`
  for want of issues. A tracker that does not answer is `not-read`, with why.
  **Release none**: a slow session and a dead one look alike from here, and
  taking a claim over is the person's call.
- **The run beside the claim** (`wiring:run-beside-claim`, `check:run-row`).
  The row reads *unobserved* until somebody has watched the pipeline's run and
  a pull request's run block disagree on the page; where the repository's pull
  requests carry no comment it reads *not applicable* with the reason, as the
  report's own row does.

### R2. Correct the record — and only the record

Write the corrections in place: the bindings, the context file the bindings name (`CLAUDE.md`, `AGENTS.md` — the tool says which it read), and nothing else.
`check:record-only` reads the working tree and says so if anything strayed.
Show each row as it will read, then write it. Where the ledger predates the
template, **write the id the tool matched into each row, and leave the columns
where they were** — however far from the template's shape. The id is record;
the shape is wiring. The `--reshape` the tool printed beside the matches is a
hint for the sitting the reply names, and this report is not that sitting.

- A row that claims more than was wired is corrected to what was. A row that
  reads *not applicable* and is contradicted by the tree becomes what the tree
  says; a row marked `decided:` is a choice, and is not re-litigated.
- Wiring the method now asks for and this repository lacks becomes a row
  reading *deferred* — since which change, naming the version of the method
  that moved it — so it is on the two-change clock rather than in a report.
- Two instructions files at the root (`check:one-context-file`) stay as they
  are: bringing them to one replaces a file somebody wrote, which is the
  sitting's kind of change. The line stays open, and the sitting is named.
- A row deferred across two changes is either wired or written off — written
  off is *not applicable* with the reason in it. A *mocked* boundary row past
  the clock is the same: real, given a suite, or *unreachable* with the reason.
- A gap the prose names — *not built yet*, *to do*, *we should*, *for now* —
  is a row or it is nothing; the tool listed every hit.
- A context file out of line beyond its lines — a requirement missing, the
  plugin's own rules copied into it — is **not rewritten here**. Correct the
  lines that are record, a loop step or a skill name, and leave
  `check:loop-per-claude-md` open with the rewrite as what closes it and the
  sitting as whose it is. The audit changes the record; a new file is the
  sitting's kind of change —
  [`claude-md.md`](../../method/claude-md.md#when-it-is-out-of-line).
- **Re-stamp only if the wiring moved.** The stamp follows the wiring and never
  the reading; a ledger re-stamped for an audit that changed nothing has
  learned to lie.

### R3. Let the tool decide whether the audit is finished

```sh
python3 <plugin root>/tools/doctor.py --validate <the scratch file>
```

It refuses the record — exit 1, naming the line — if any id is missing, any
line still reads `unanswered`, any state is off the vocabulary, an `open` line
names nothing that closes it, a `not-read` line gives no reason, a judgment
reads `clear` with no command beside it, or the working tree changed anything
but the record. **A refused record is an audit that has not finished**: go
back to the line it names. Nothing else is a way through — not a paragraph
explaining the gap, not a subagent, not a second scratch file.

Where it accepts the record, it answers the four lines the reply generates,
**writes the record at the path the bindings name** — replaced on every run,
each line carrying the date it last changed state, so the next audit can say
what opened and what closed — and prints **the reply**. That reply is the
hand-back, verbatim, with nothing after it:

- what is open, sorted by the severity each id carries — *platform*, then
  *boundary*, then *wiring*, then *record*; a row asserting a protection the
  platform does not enforce outranks a deferral one change old, every time;
- then what was not read, with why — a row that was checked and a row that
  was assumed never come out looking the same;
- then the decisions, once — the rows marked `decided:` — with the tree's
  contradiction, where there is one, offered as evidence and not argued;
- then, only where an open line names wiring, the command that starts setup
  as this host takes it — `/livespec:setup` in Claude Code, `/skill:setup` in
  Pi — and the rows the sitting will be asked to wire, one per line. Where nothing is left for
  the sitting, no such line, and nobody is sent to a sitting nobody needs.

Commit the record with the corrections. The same last line closes the
reading's record in the bindings. Anybody who only wants the answer — a
grader, a reviewer — asks `--check <record>` instead: the same exit, and
nothing written.

## Bring it up to date

A repository whose ledger is behind the plugin installed — a plugin update, or a
report that ended naming wiring — is brought level here. **Diff it, never
overwrite it.**

1. **Report first**, as above, and commit the record. It is what this sitting is
   measured against.
2. **Plan.** `python3 <plugin root>/tools/doctor.py --plan` lists what the plugin
   installed asks of this ledger, computed from
   [`requirements.md`](../../method/requirements.md#the-ids) rather than read from
   the changelog: each gate or wiring id that arrived or was revised after its
   row's own version, each id with no row, each retired id still carrying one,
   and each check to answer again. Add the report's open wiring lines — stale
   commands, deferrals past the clock — which are owed the same way.
3. **Each item, one at a time.** Show the change and wait for a yes. Wire it in
   the project's own language, break it on purpose and watch it fire, run the
   verification command, and commit it on its own — green. **A gate that refuses
   the tree as it stands is not committed**: its row reads *deferred*, naming the
   findings, and the hand-back offers `todo` to file them. A deferral already
   past the clock is wired or written off, never deferred again.
4. **Record what was answered.** `python3 <plugin root>/tools/doctor.py --adopt
   <ids…>` writes each answered row's version — wired, decided not applicable,
   or deferred on the clock — and the stamp line as the oldest. A row nobody
   answered keeps its version.
5. **Report again**, and open one pull request, *livespec A → B*, carrying the
   two records and each item. The rows the pipeline is watched running become
   *automated*; merging is the person's.

**A ledger written before ids existed is matched, not retyped**: each row goes
to its id by the labels the table's *aliases* column lists, and the id is
written into the row; a row two ids could claim is shown with both and left for
the person; a row no id matches is either one of this repository's own — give
it `local:` — or a row for nothing, which the person decides. Then move the
rows, verbatim, into the template's tables — `python3 <plugin
root>/tools/doctor.py --reshape`, the plugin root being two directories up from
this skill file, prints them in that shape, ids filled from the aliases,
unmatched rows marked — and apply what it printed with the person in the room.
Rows you cannot date honestly say **predates the ledger** rather than getting an
invented change number.

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
- **Changing a protection setting unasked**, deletion on merge included.
- **Creating a label in the tracker unasked.** The claim marker is offered, never
  made on the way past.
- **Removing a tree with work in it**, or a secret committed, copied into a
  tracked file, or given to a tree any way but from its one source.
- **Adding a dependency** to make the process fit. If the gate needs a library,
  it is too big.
- **A coverage number nobody chose.** Copied from another repository, or
  subtracted from this one's own score — both arrive without anybody having
  decided what the points they give away stand for.
- **Installing over an existing setup without saying what it will overwrite.**
  Show the list first; a CLAUDE.md somebody wrote by hand is context, not clutter.

**In the report, also:**

- **Cleaning anybody's trees** but the throwaway it made.
- **Releasing a claim**, or writing anything to the tracker.
- **Wiring anything.** Not a gate, not a report, not a threshold — including
  the one it just found is wrong. It writes the record; the sitting writes the wiring.
- **Running a command it read from the bindings itself.** The tool prints
  them; the running is a mind's, under the person's prompts.
- **Starting the sitting.** The last line says what to type and does not run it.
- **Reading an entry as a task list.** The entry is where to look.
- **Re-stamping for having read.** The stamp follows the wiring.
- **Reshaping the ledger.** The id goes into each row as it stands and the
  columns stay where they were; `--reshape` is the sitting's, and the reply
  ends by naming it.
- **Asking the platform twice.** One refusal is the answer; the reply names
  who can get a different one.
- **Leaving a line `unanswered`.** `not-read` with why is an answer; a blank
  is a check nobody made, and `--validate` will not let it end.
- **Handing back without the record.** The reply is what pass two printed;
  a reply recalled from the session is the thing this skill exists to stop.
- **Running the interviews.** An empty layer is section 8's.
- **Flipping every row to *unobserved* to be safe.** A row somebody watched
  fire stays *automated*.
- **Reading a green pipeline as an answer about the platform.** A build that
  passed says the job ran, nothing about what happens when it fails.
- **Auditing a repository that has no bindings**, rather than saying so and
  offering the sitting.
