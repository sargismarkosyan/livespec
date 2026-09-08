# Spec 0039: the world a test runs in

- **Status:** approved
- **Issue:** none — a direct request, standing on two pages written on
  2026-09-08: the research deck *The Mocked World* and the plan *Green Means
  Real*, whose spec A this is. Both are private artifacts of the maintainer's
  and are linked from the sketch; the deck's sources are what this spec cites.
- **Depends on:** nothing to build. It is the first of the four the plan cuts,
  and the other three each point at the ids this one creates — the table and
  its five states — so it goes first whatever order the rest take.

## Who this is for

[`agent-accelerated-owner`](../personas/agent-accelerated-owner.md), in
[`adopt-the-process`](../workflows/adopt-the-process.feature), at two of its
steps: the sitting — section 2's questions, section 4's wiring, section 5's
bindings — and, from then on, every change whose verification is read as green.

Three persona lines decide the shape:

- **"Checking the result by reading is not available either."** A green build
  is what stands in for reading. Today a green says the tests name their rules
  and reach the code; it does not say what world they ran in, and a green over
  an in-memory stand-in for the store reads identically to a green over the
  store. This is the person for whom that difference is invisible by
  construction, because the tests are exactly the prose they never open.
- **"A claim written into a bindings file that nobody had ever run."** The
  persona's own list of misses, and the claim this change is about is worse:
  it is not written anywhere. The world a repository's tests run in is a
  sentence in its setup prose — *"Tests run under Node, not a browser"*, in the
  reference repository — typed once, on no clock, counted by nothing.
- **"Fix the pipeline error, not bypass."** So the answer arrives as a gate that
  fails, which is the form this person acts on, and not as a skill that reviews.

**This lengthens the sitting by one question, and names what it shortens.** The
[workflows README](../workflows/README.md) requires that. What it shortens is
every attempt after the install: from the first change on, a green says what
world it holds in, and the uninterviewed attempt of taking a version through
review no longer begins by working that out from the tests. And it reaches the
one column of [the journey](../journeys/trusting-the-spec-again.md) nothing
reaches — *Coming back*, where the spec is read and acted on without checking.
A green that is green in the wrong world is the exact form of untruth that
column cannot see, and after this it is one a gate can.

Two always-promises are touched: **`gates-are-proven`**, because the four faults
this adds to a consuming repository's injection table are what make the new
check a gate rather than a hope; and **`never-implements`**, at the closest
approach any change has yet made to it — see *Risks*. `always-green` and
`context-budget` are untouched: the gate is the consuming repository's, written
by `setup` the way every gate is, and no description moves.

## The job behind the request

The literal ask: *"I want to make sure that tests check real things and mock
only which is needed to be mocked"* — and, earlier, that what keeps arriving is
software that *"works on paper, even if you ask for a GIF proof it can give it
to you, yet actually it's not working because of some edge case"* that *"was
either mocked or missed completely."*

The job: **to read a green verification in a repository the agent built and know
that the tests reached the things the rules are about** — the store, the
service, the clock, the terminal — rather than a stand-in for them, without
reading the tests; and to have every place where they did not say so, dated,
where the next change reads it.

The trigger is the same one every time: a version ships green, is used, and
fails on the first thing the stand-in never did — the store refusing, the
service timing out, the window resized. What they do today instead is read the
tests, which this persona does not do, or find out in use, which is what they
adopted the process to stop.

## Why now

Because the two gates this method rests on are both satisfied by a test that
names its rule and reaches every line over a stand-in for the thing the rule is
about, and nothing in the method can tell.

**The evidence is in the deck, and it is the vendors' own.** Anthropic's Sonnet
4.5 system card lists *"creating tests that verify mock rather than real
implementations"* as a common hack. Its harness essay describes Claude passing
unit tests and curl checks while the feature was broken end to end. OpenAI's
harness essay states the mechanism: from the agent's point of view, anything it
cannot access *"effectively doesn't exist."* Across 1.2 million commits, coding
agents add mocks in 36% of test commits against 26% for humans; 80% of
agent-authored test patches carry a weak oracle or none; and given a test suite
as the oracle, 11 of 12 runs in Microsoft's study reached 222 of 222 passing
while the library under test was dead or absent. The trigger is ambiguity:
production agents hard-code under 2% of the time on unambiguous tasks and 22 to
44% on ambiguous ones. The stand-in is the cheapest path to green, and an
unnamed boundary gets mocked.

**The live case is the reference repository.** Read on 2026-09-08,
`todo-change` runs every behaviour test and every walkthrough in jsdom; the real
browser is reached only by `record-clip`, which asserts nothing. Its clock is
fixed by a `day` argument. Its in-browser model is `null`, with *"no rule
asserts what a model says."* Its drag gesture *"still cannot run here: jsdom has
no layout."* Every one of those is true, in a comment in `tests/support/app.mjs`
or a sentence in its setup prose, and not one is a row, a state or a date. It is
a well-run repository, and its green does not say which world it is green in.

**This repository has the same shape.** The judge model that scores every case
stands in for the human who would read the output, and the calibration pass
[`evals/README.md`](../../evals/README.md) describes — *read every judge verdict
and ask whether they would have scored it the same way* — has not been run. That
is a stand-in nothing checks, since [`0012`](0012-a-runner-that-runs.md), with
no row saying so.

**The canon already has the rules, and every one of them routes through a
person.** Prefer the real implementation; a fake has fidelity and is tested
against the real thing by one suite run against both; the owner of the real
thing owns the fake; never mock a type you do not own; a mocked path is covered
by a larger test that checks state. Each ends in *the owner should* or *use your
judgment* — and an agent session has neither an owner nor a judgment that does
not pick the mock. So the rules become a table the agent reads and a gate that
fails when a row is contradicted, which is the only form this method has ever
trusted.

## The end value

A consuming repository's bindings say, for each thing the app talks to, how a
test there reaches it — *real*, *fake*, *recorded*, *mocked* or *unreachable* —
and the traceability gate refuses a rule-bound test that stands a double in for
a boundary the row calls real. Ren reads the table instead of the tests. A
stand-in nothing checks reads *mocked* with the date it was noticed; what no
test can reach reads *unreachable*, and every change touching it says so.

**How we would know it worked:** in `todo-change`, the row for the browser reads
*mocked*, dated, and the row for the in-browser model reads *unreachable*; the
first pull request there whose behaviour test stands a double in for something
the table calls real is refused by the gate rather than merged; and a `doctor`
run in a repository whose bindings say the store is real, over tests that never
reach it, comes back naming the tests.

## What changes

1. **[`gates.md`](../../method/gates.md) gains a third table, *The boundaries*,**
   beside the two the ledger section already carries. One row per boundary the
   app crosses — whatever it talks to that is not its own code — in five states:
   *real* (tests reach the thing itself, and the row names what starts it here),
   *fake* (a stand-in with a suite that also runs against the real thing, and
   when that half was last green), *recorded* (replies captured from the real
   thing, when, and how old they may be), *mocked* (a stand-in nothing checks —
   since which change, and the larger test that covers the path, if any; on the
   two-change clock), *unreachable* (no test here crosses it — why, whether it
   cannot be or was decided against, and every change touching it says so).
   Every row says what it leaves uncovered. **The tree does not know what the
   boundaries are; the person does**, which is why the rows are asked for and
   never derived. A row reading *real* is written after a test has reached the
   thing, never before, for the same reason a gate row reads *unobserved* until
   it has refused something.

   The gate reads the rows: a rule-bound test that doubles a boundary reading
   *real* fails; a *fake* row naming no suite fails; a *recorded* row past its
   age fails; rule-bound tests present with no table at all fail. What counts as
   a double is a binding — the patterns are the language's — and it is read only
   over the rule-bound tests, because a unit test doubling everything is what
   unit tests are for. Four rows join the injection table. The portable half of
   *written off*: a *mocked* row past the clock becomes *unreachable* with the
   reason in it, the way a deferred gate becomes *not applicable*.

2. **[`testing.md`](../../method/testing.md)'s *The environment the tests run in*
   becomes *The world the tests run in*.** The environment was already a
   binding; so is everything else the app talks to, and the section says so and
   points at the table. Three things join the two already there: a test proves a
   rule in the world its row names, or it proves it nowhere; a fake is honest
   only while something checks it against the real thing, and one nothing checks
   is a mock whatever it is called; what no test here can reach is said, never
   simulated.

3. **[`setup`](../../skills/setup/SKILL.md) asks a sixth thing it cannot find
   out** — *what does this talk to, and which of those can a test reach for real
   from a session here?* — with the recommendation attached: real wherever the
   real thing can be started here, and the skill names the usual shapes as
   examples rather than as the method — a store in a container, a headless
   browser, a pseudo-terminal running the built binary for something used
   through a terminal, a mail catcher, a provider's sandbox. Where it cannot,
   *fake* only if a suite checks the fake against the real thing, and
   *unreachable* otherwise; **never *mocked* on day one of a fresh repository**,
   because a mock nobody chose is what the row exists to stop. **An occupied
   repository writes down what is true today**: its tests already run in some
   world, the day-one rows are that world named, and the stand-ins nothing
   checks read *mocked* dated from the sitting — the same shape as the day-one
   coverage exclusions, which are today's uncovered code written down.

   Section 4 gains *make the real thing reachable, before the gate that assumes
   it*: the container the suite brings up, the sandbox key the pipeline holds,
   wired in the repository's own tooling and run through once before a row reads
   *real*. This is the suite's tooling and not the gate, so the no-dependency
   rule does not bind it; what binds it is the same rule as the gates — one
   command runs it, and CI runs that command. Then the check: the traceability
   script already reads every rule-bound test source for the id it claims, and
   it reads the same sources for the double patterns the bindings name. The
   patterns for a terminal application name the framework's own harness and the
   tty, environment and subprocess patches, not only the mocking libraries.

   Section 5 writes the third table from the sixth answer, with the reminder
   that most rows on an occupied repository's first day read *mocked* or
   *unreachable*, and honestly.

4. **[`doctor`](../../skills/doctor/SKILL.md) §1 reads the boundary rows**,
   which are the rows a diff cannot check: does the thing a *real* row names
   actually start from here — run it; does any rule-bound test double that
   boundary — the gate says, and where the gate predates the row, grep with the
   bindings' own patterns; does a *fake* row's suite exist and when was it last
   green; is a *recorded* row within its age; is a *mocked* row past the clock.
   A row that reads *real* over a world the tests never enter is the false
   green the table exists to stop, and it reads exactly like a true one. As
   always, it corrects the record and never the wiring.

5. **[`claude-md.md`](../../method/claude-md.md)'s requirement 7** gains one
   rule in its list of the ones that get broken: a rule-bound test runs in the
   world its boundary row names. The research found that one line of mocking
   policy in the agent's configuration file measurably moves what it writes,
   and this is the one line.

6. **[`process.md`](../../method/process.md)'s *A step you cannot take here is
   said once*** gains a sentence: a boundary no test here can cross is the same
   case one layer down — its row reads *unreachable*, and the change says so
   rather than stubbing past it.

7. **[`templates/feature.feature`](../../templates/feature.feature) renames one
   example.** Its second rule's third example reads *the boundary — the case
   just inside or just outside the promise*. That word now means what the app
   crosses, and two meanings of one word in the file that teaches the
   vocabulary is the drift this method fights. The example becomes *the edge*,
   in the implementing change; nothing else in the template moves.

8. **[`spec.md`](../spec.md) gains two words** — *boundary* and *stand-in* —
   **done in this spec commit**, as the prose half of the same decision, the way
   [`0038`](0038-the-other-side-of-the-difference.md) added *stamp*. *Stand-in*
   is there so that *mock* can be kept for the one nothing checks and *fake* for
   the one something does, which is the whole distinction the table turns on.

9. **This repository's own bindings gain the table**, in the implementing
   change, because this repository is its own consumer and its rows are worth
   writing because they are uncomfortable: the model session is *real* and
   paid; the judge model is a stand-in for the human reader that the never-run
   calibration pass would check, so it reads *mocked* since `0012`, cover none;
   the consuming repository a case runs in is a scaffold script's fixture, a
   stand-in with no suite against a real one, so *mocked* too; the platform is
   *real* through `gh`. What stands in for the gate's double check here is said
   in the same place: there are no rule-bound tests to read, so the row that
   would fail is *not applicable* and the table is the whole of the wiring.

10. **The journey moves a line in the implementing change.**
    [`trusting-the-spec-again`](../journeys/trusting-the-spec-again.md)'s
    second opportunity says the checks *"cannot say it stopped being true."*
    Narrowed for one kind of untruth: a test that is green over a stand-in for
    the thing its rule is about now fails, where before it read as green. Not
    closed — a description that still fits the shape and no longer describes
    what anybody meant is untouched by this.

**Rules added or changed** — the `@rule:` ids in `specs/features/`:

| Rule id | Feature file | New or changed |
|---|---|---|
| `setup-asks-what-the-app-talks-to` | `features/setup/boundary-binding.feature` | new, `@planned` |
| `a-real-row-is-written-after-a-test-reached-it` | `features/setup/boundary-binding.feature` | new, `@planned` |
| `a-stand-in-nobody-chose-is-not-written-as-chosen` | `features/setup/boundary-binding.feature` | new, `@planned` |
| `a-real-row-over-a-world-the-tests-never-enter` | `features/wiring/boundary-rows.feature` | new, `@planned` |
| `a-stand-in-nothing-checks-is-on-the-clock` | `features/wiring/boundary-rows.feature` | new, `@planned` |

Two new files rather than rows in
[`setup/test-binding.feature`](../features/setup/test-binding.feature) and
[`wiring/ledger-claims.feature`](../features/wiring/ledger-claims.feature): the
first is about how a test claims a rule, the second about what a gate row may
claim, and this is about what world a test ran in — a third question, and a
file each side so that the sitting's half and the audit's half are held apart
the way `setup` and `doctor` are.

**No description changes, so no should-not-fire case is owed.** `setup`'s
description already carries *"wire the two gates in that project's own
language"* and `doctor`'s *"check every claim its bindings make against what
owns the answer"*, which are these rules exactly. `context-budget` stays at
4321 of 5000.

### The decisions, and who made them

The plan listed seven, each with a recommendation, and the maintainer carried
on with the recommendations rather than answering them one by one. They are
recorded here as what this spec assumes, so that a different answer is a
change to this file and not a surprise in the implementing one.

- **The word.** *Boundary* for what the app crosses; *the edge* for the limit of
  a promise, in the template. Every other candidate read worse in the sentence
  *a double at a boundary declared real*.
- **Whether *real* includes a paid sandbox.** Yes. A nightly suite against a
  provider's sandbox is approved once, in the bindings, by whoever pays, rather
  than per run: the graded-suite rule exists because those runs are model
  sessions, and a sandbox call is cheaper by orders of magnitude. A repository
  that answers no has every third-party row read *fake* or *recorded*.
- **Where the double patterns live.** The bindings, beside the discovery
  pattern, with `setup` proposing the language's usual list and the person
  striking or adding. A list inside the plugin would name tools and fail the
  method's own line.
- **The age of a recording.** The method says only that a recording carries a
  date and an age; `setup` asks and offers thirty days; the number is a
  binding.
- **Day-one *mocked* rows.** Yes on an occupied repository, dated from the
  sitting; no on a fresh one, where the honest states are *real*, *fake* with
  a suite, or *unreachable*.
- **The order.** This one first, because it creates the ids; the other three in
  the plan's order unless the maintainer moves D up.
- **`record-clip`'s description.** Untouched here; it is spec C's, where the
  skill's steps move.

## What we are not doing

- **Not a review-tests skill.** It would be advisory where the persona needs a
  refusal, it would read the diff the same model wrote, and its description
  would cost every session against `context-budget`. The reading it wanted lives
  in the gate here and in the report's own run in spec C.
- **Not a gate over what a test asserts.** A test that reaches the real store
  and asserts nothing about it passes every check here. That is coverage's half
  and the human's reading, and spec C reports assertions per rule-bound test
  beside the coverage split, never as a threshold.
- **Not the `@crosses:` tag on rules**, and not refine-spec asking for the
  boundary misbehaving. Spec D, which needs the ids this creates.
- **Not skipped tests claiming nothing, and not the runner's count against the
  tree's.** Spec B.
- **Not the run block on the pull request, and not the picture naming its
  world.** Spec C.
- **Not a dependency in any gate.** Double detection is pattern matching over
  sources the traceability script already opens. The real dependencies section
  4 wires are the suite's, which was always allowed to have them.
- **Not retroactive rows.** An occupied repository's day-one table is what is
  true today, named, the way its day-one coverage exclusions are. The clock
  starts at the sitting.
- **Not wiring anything from `doctor`.** Its first refusal stands.
- **Not naming a tool in `method/`.** Containers, sandboxes, catchers and
  pseudo-terminals are examples in the skill body; the method says *the thing
  itself* and *what starts it here*.
- **Not moving the coverage demand**, and **not changing the eval-cost rule.**
  A sandbox suite approved once is a binding, and the graded-suite rule is
  about model sessions.
- **Not writing the table for `todo-change` by hand.** `doctor` there reads the
  changelog entry after its stamp and offers the rows as deferred; `setup` asks
  the question and wires what the answer allows. Nothing fires unasked.

## Data

No storage contract here. What this writes in a consuming repository is three
things: rows in its bindings, a check in its own gate script beside the ones
already there, and — for the first time — something on the suite's side of the
line: the container definition the suite starts, the sandbox key the pipeline
holds. That third thing is tooling rather than application code, and *Risks*
holds the line.

**This spec commit stales nothing.** It writes two feature files whose rules
are `@planned` and claimed by nobody, edits `spec.md`, which no measurement
hashes, and this file. `verify.py` exits **2** on it, as it does on `main`
today — *0 measured, 22 stale, 6 below the floor, 9 never measured* — for the
same rows and no other reason.

**The implementing change adds no stale row that is not already red.** It edits
the bodies of `setup` and `doctor`, and every case holding either is already
owed. What it adds is two new cases, numbered next: one for `setup` in a
repository with a store client and a payment SDK whose behaviour tests stub
both, expected to claim the three setup rules; one for `doctor` in a repository
whose bindings say the store is real and whose behaviour tests use an in-memory
one, expected to claim the two audit rules — roughly **$1.80 each at the
floor**. Which of the stale rows are worth re-measuring is the maintainer's
spend to approve; the commit and the pull request finish with a gap where the
numbers go.

**What the pull request owes.** The method pages and the two skills are
payload, so a `minor` label and a `## Changelog` section; two `.feature` files
move, so the Gherkin block. The changelog entry has to say where to look —
`gates.md`'s new subsection, `setup` §2, §4 and §5, `doctor` §1 — because an
audit in a consuming repository reads it to find the rows this change obliges,
and an entry that is mostly this spec's reasoning would ask nothing.

## Risks

- **The closest approach yet to `never-implements`.** Section 4 now wires the
  container a suite starts, in a consuming repository. Held by three things:
  it is the suite's tooling and not `src/`; one command runs it and CI runs
  that command, the same rule as the gates; and where making the real thing
  reachable would need application code written — a fixture loader, a seed
  script inside the app — that is the human's, named in the hand-back, and the
  row reads *unreachable* until it exists. The line is *the suite may gain
  tooling; the app gains nothing*.
- **A wallpaper gate.** Pattern matching over test sources will match a
  hand-written class named `FakeStore` that is in fact checked, and miss one
  named `Store` that is not. Scoped to the rule-bound folders and to boundaries
  the rows declare *real*, with the person striking and adding patterns in the
  sitting, and `doctor` reading the sources where the patterns fall short. A
  gate that cries wolf is worse than none, and the two-version norm for
  warnings applies to a pattern that keeps misfiring.
- **A real row that is not production.** A store in a container is not the
  store at production volume, and a sandbox is not the live provider — Stripe's
  own documentation says refunds are asynchronous only in live mode. Held by
  the *leaves uncovered* clause every row carries; a row without one is a row
  that will be read as covering everything, which is the reading the gate
  ledger already refuses.
- **The table is typed and can lie.** The same risk as the gate ledger, and the
  same answer: the tree is the authority, and `doctor`'s two rules read the
  tests against the rows. A *real* row the tests contradict is the one
  contradiction a diff cannot show and the audit is built to.
- **The suite gets slower.** Containers cost seconds; sandboxes are
  rate-limited. The recommendation in the sitting is the split the canon
  already makes: the fast stand-in for the rules, the real thing for the one
  walkthrough per workflow, which is where end state is read back.
- **The word collides.** *Boundary* already means the edge of a promise in the
  feature template; the rename in the implementing change and the two
  vocabulary rows are what stop the same word meaning two things in the file
  that teaches the vocabulary.
- **An adopter never asks.** Nothing here fires unasked. A repository that never
  runs `doctor` after updating keeps its prose and its untracked world, exactly
  as before — the same limit `0036` and `0038` recorded, and the same reason
  the changelog entry has to say where to look.
- **`context-budget`** is untouched. **`always-green`** is untouched: the gate
  is the consuming repository's, and this plugin still cannot fail anybody's
  build.

## Acceptance checks

There is no app; this repository's deliverable is the pull request description.
What is checked by hand:

1. Run `setup` in a scratch repository with a store client, a payment SDK and
   behaviour tests over in-memory stand-ins for both. It asks what the app talks
   to before writing any row; it recommends the container and the sandbox; it
   writes *real* only after a test has run through the thing, *unreachable*
   with why where nothing here can start it, and — this being an occupied
   repository — *mocked since this sitting* for the stand-ins, each naming the
   larger test that covers the path or saying there is none.
2. Break the gate it wired, one fault at a time: a behaviour test doubling the
   store while its row reads *real* fails naming the row and the pattern, and
   passes once it runs through the container; a *fake* row naming no suite
   fails; a *recorded* row past its age fails; the table deleted with
   rule-bound tests still present fails. All four are in that repository's
   injection record.
3. Run `doctor` in `todo-change`. It reads the entry for the version this ships
   as, offers the rows — the browser *mocked*, the store *fake* owned by jsdom, the clock
   *mocked* until a real-clock test exists, the in-browser model and the drag
   gesture *unreachable* — as *deferred since livespec* that version, corrects
   nothing that is not record, and leaves the stamp where it was.
4. Run `doctor` on a fixture whose bindings say the store is real and whose
   behaviour tests use an in-memory one. It reports the row as claiming a world
   the tests never enter and corrects it to *mocked*, naming the tests. On a
   fixture where the store cannot be started from the session, it says the row
   was not read back and why, and corrects nothing on that evidence.
5. Run `doctor` here after the implementing change. The table reads: the model
   session *real*; the judge *mocked* since `0012`, cover none; the fixture
   repository *mocked*; the platform *real*; the double check *not
   applicable*. Nothing about those rows is reported, because they are true
   and dated.
6. `python3 .github/scripts/verify.py` — exit 2 on this spec commit for the 22
   rows already owed and nothing else red. All five rules drop `@planned` in
   the implementing change, each claimed by a case tagged `rule:<id>`.
7. After the implementing change, the word *boundary* appears in
   `templates/feature.feature` nowhere, and *the edge* once, where *the
   boundary* used to be.
