# The gates

Two gates: **traceability** and **coverage**. Coverage alone rewards tests that
touch code without asserting anything anyone asked for. Traceability alone
rewards tests that name a rule and check it shallowly. Together they are hard to
satisfy dishonestly, and that is the only reason either is worth running.

**The commands, the thresholds and the tool names are bindings.** They live in
the repository's `specs/setup/README.md`. What follows is what those commands
have to *mean*.

## Gate 1 — traceability

Enforced in **both directions**:

```
rule  →  test     every live rule must be claimed by a test
test  →  rule     every behaviour test must name the rule it exists for
```

One direction alone is worthless. Rule→test catches behaviour that was specced
and never verified; test→rule catches tests that verify something nobody asked
for. It fails on any of:

| Failure | What it means |
|---|---|
| a live rule with no test referencing it | Behaviour was specced and never verified. Write the test, or tag the rule `@planned` if it is not built yet. |
| a test claiming a rule id that does not exist | Usually a typo, or an id that was renamed. Rule ids are permanent — see below. |
| a feature file with no test against any of its rules | A whole component is unverified. |
| a test outside a `rule()` block in a behaviour file | An untraced behaviour test. Move it inside a block, or into the unit folder. |
| a behaviour file with no `rule()` at all | Same. This is the check that stops coverage filler. |
| a `@planned` rule that *does* have a test | The tag should have come off in the change that made it true. |

It should **warn without failing** when a unit test claims a rule — it probably
belongs with the behaviour tests — when a test that asserts nothing happened
claims a rule not tagged `@refusal`, and when a feature file grows past the
repo's soft size limits.

The output worth having is a per-feature matrix — traced, untraced, planned —
followed by a count. It is worth reading even when green.

### The same loop, one layer up

The layers that say what the product *is* and who it is *for* close the same way:

```
feature   →  workflow              every feature says what it serves
workflow  →  feature                no workflow nothing implements
workflow  →  test                   no walkthrough nothing walks
workflow  →  persona                no workflow for nobody
persona   →  workflow               no persona nobody does anything as
journey   →  workflow               no dangling reference
```

| Failure | What it means |
|---|---|
| a feature naming no `@workflow:` | It serves nothing anybody wrote down. Tag it, or the thing it serves is missing from the workflows. |
| a feature naming a workflow that does not exist | A typo, or an id that was renamed. |
| a workflow claimed by no feature | Specced and never built. Tag a feature, or tag the workflow `@planned`. |
| a workflow walked by no test | Its `Example:` blocks are a costume. Write the walkthrough. |
| a workflow naming no live `@persona:` | A workflow for nobody, or one pointing only at a `@retired` persona. |
| a persona named by no workflow | Nobody does anything as them. Give them a workflow, or tag the file `@retired` — which is for a persona no workflow names *yet*, not a shelf. |
| a `@planned` workflow that *is* claimed | Same as a `@planned` rule with a test: the tag should have come off. |
| a journey naming a workflow that does not exist | A dangling reference is factually wrong, not a judgment call. |

**One warning, not four.** Where an attempt sits in the arc is a judgment, so a
workflow naming no `@journey:` warns rather than fails. Keep such warnings
scarce, and adopt the norm that **a warning surviving two versions either becomes
an error or gets deleted** — four new warning kinds at once turn the output into
wallpaper in one version, and wallpaper is indistinguishable from green.

**A repository's own pipeline is not an attempt anybody makes with the
product.** The gates on this page, the step that releases, the checks that
prove them — none of it is something the persona does, so no feature file
describes it and no rule id is reserved for it. It is held by the fault table
this page ends with, and read back from the record of that table in the
bindings. A feature naming no workflow is refused, and the answer to that
refusal is never a second kind of tag: it is either an attempt missing from
the workflows, or a contract of the repository's own, which belongs in the
faults.

**Two checks worth wanting and worth leaving out:** whether a journey has been
looked at since the workflows under it changed, and whether features have piled
up under a workflow since its file was last edited. Both are git questions rather
than file questions, and CI that checks out a single commit answers them with
silence — so both would pass forever while looking enforced. A gate that cannot
fail is worse than an absent one.

### The second half of the output is the map

Every workflow, who it is for, and the feature files serving it — **generated,
never typed**. A hand-maintained list of what implements what is a list that has
already drifted; the only question is whether anybody has noticed yet.

## The id system

```gherkin
@feature:<id>
Feature: <what this component does>

  @rule:<id>
  Rule: <one thing that must be true>

    Example: <the case that shows it>
      When ...
      Then ...
```

- `@feature:<id>` on every feature, `@rule:<id>` on every rule, both unique
  across the whole repository.
- Every rule needs at least one `Example:`. A rule with no example is an opinion.
- **Rule ids are permanent.** Reword a `Rule:` line as much as you like — it is
  the same rule. Changing its id orphans every test pointing at it, and the gate
  reports the test as claiming something that does not exist.
- `@planned` marks a rule that is specced but not built. Specs land before code,
  so this is the normal state of a new rule, and dropping the tag is part of the
  change that makes it true.
- **`@refusal` marks a rule whose promise is that nothing happens** — the product
  staying out of something it was not asked for. Such a rule is verified by a
  test asserting absence and by nothing else, so the tag is what stops the gate
  reporting its only honest test as the wrong kind. Without it the choice is a
  permanent warning or a `@planned` tag on built behaviour, and both teach the
  reader to stop believing a tag.
- `@workflow:<id>` on every feature, saying what it serves. It may repeat: one
  feature can serve two workflows.
- `@persona:<id>` and `@journey:<id>` on every workflow. **Not on features** —
  every feature reaches a persona through its workflow, and a second path to the
  same fact is a second thing to keep true.
- **Workflow and persona ids are permanent for the same reason rule ids are.**

The reader should also enforce structure: one feature per file, no scenario
outside a rule, no duplicate ids, nothing unnamed. **A workflow file is the one
exception** — it has no `Rule:` at all, because it is one bounded attempt rather
than a set of them, and its scenarios hang off the `Feature:` line as
walkthroughs of the whole thing.

Soft limits on file length and rules per file produce warnings rather than
failures, because small per-component files are the point and a hard cap on them
is not.

## Gate 2 — coverage

**Lines, branches and functions — all three, and the number is the repo's.**

All three matter. Line coverage is the weakest of them: V8 counts a function's
declaration line as covered even when the body never runs, so an uncalled
function can show 100% lines while function coverage correctly reports 50%. Aim
at branches; lines follow.

**The runner must refuse to pass on a measurement of nothing.** While there is no
source to measure it says so and skips the thresholds, and it arms itself the
moment the first module lands. A coverage gate that reports 100% of zero files is
the most convincing false green there is.

## The report is not a gate

A report on a pull request — spec health, coverage, what is specced but not built
— earns its place only if it **cannot fail the build**.

And it recomputes nothing. If the traceability gate passed, that *is* the proof
every live rule has a test; a report that re-derives it is a second copy of the
gate's logic waiting to drift out of sync. **So the gate has to be able to hand
its numbers over** — whatever else it prints, there is a way to ask it for what
it worked out. A gate that only speaks to humans forces the report to parse the
tree again, and that is the drift arriving through the door marked *it is only a
report*.

**It reports what moved, not what exists.** A total is trivia to somebody
deciding whether to merge: *12 live rules* tells them nothing about the change in
front of them, and *+1* is the entire point. That means reading the base as well
as the branch, and a repository that cannot do that has a report worth half of
one.

**It goes where the decision is made.** The numbers already exist — in a log,
behind a command somebody could run. Being available is not the same as being
read, and a report that requires anybody to go and look has not solved the
problem it was built for.

**A repository is expected to end up with one.** This is the paragraph that used
to describe an artefact in the third person, as though it were something a
repository might acquire. It is part of what gets wired, and its absence is a gap
like any other — one that is easy to miss precisely because nothing fails when it
is missing.

**It never gates, including on its own failures.** A report step that goes red
because it could not build a report is a gate nobody declared. If the token is
missing, the base will not check out, or the tooling breaks, it says nothing and
the build is unaffected. The honest cost of that: a report going missing is
itself silent, and nobody is told.

**And it describes a red build too.** The obvious wiring puts the report after
the gates, where it only ever runs on a green one — which is backwards for any
repository whose verification can fail for a reason the method sanctions, such as
[bookkeeping waiting on a run somebody pays for](graded-cases.md#freshness-is-gated-the-score-never-is).
That build is the one whose state most needs explaining, and a report skipped on
failure is unreachable on precisely the runs where its numbers would change what
somebody does. **So what explains a build survives the build failing**, and the
numbers a gate hands over are worth handing over when the gate is red.

That is safe because of the rule above rather than despite it: a report that runs
on a red build cannot turn it green, and one that cannot be built still says
nothing and still fails nothing. What it must not become is a second opinion — it
reports which failure happened, and never whether the failure counts.

## A gate that does not depend on a failing one

The same wiring hides more than the report. A run stops at its first failing
check, which is right while every red clears in the minute after it is read: it
gets fixed, the run happens again, and everything below speaks then. It stops
being right the moment a red can **stand** — and where bookkeeping waits on a
spend nobody in the session can approve, one can, for days. "Stop at the first
failure" then quietly means "hide every other verdict until the bill is settled",
and somebody pays the expensive thing only to be told the cheap thing was wrong
all along.

So a gate that does not depend on the failing one runs anyway, and its verdict is
in the same run. Nothing is being let through: **the build fails either way**.
What changes is how much of what is wrong gets said per attempt, and the reader
was going to fix all of it regardless.

The guarantee that makes this different from the report is the one worth writing
down, because it is the opposite guarantee. A report may run late *because it
cannot gate*. A gate may run late only if running late leaves it gating — so
**running late changes when it speaks and never whether it blocks**. Whatever
softening a report is given so it can fail harmlessly is exactly what a gate must
not be given when the same guard is copied down a file. That copy is the
plausible mistake, and it turns a gate into a report while looking like tidiness.

**Depends on** is doing real work in that sentence, and it is not a synonym for
*comes after*. Two checks reading different things cannot fail for each other's
reasons; a check that cannot start until an earlier step has prepared something
can, and forcing it to run then reports one failure a second time in language
that suggests two. So the condition is that the prerequisite got there, not
merely that the run is still alive.

## What is wired, and what is not

A repository rarely gets every gate on this page on the day the process arrives.
The layers land one at a time, and a gate over a layer that does not exist yet is
correctly left unbuilt. What is not correct is nobody being able to say, a year
later, which of them were ever built — an answer split across each layer's own
README is four honest quarters of a fact and no way to add them up.

So the bindings carry a **ledger**: one row per gate named on this page — by
the id [the list below](#the-ids) gives it — and a row for anything else only
under the `local:` prefix, which says the repository added it and the method
does not require it.

| A row reads | And means |
|---|---|
| **automated** | it runs, and the row names the command that runs it |
| **not applicable** | it cannot apply here, and the row says why. A decision, not a gap |
| **deferred** | it applies and is unbuilt — since which change, and why |
| **unobserved** | it is wired, and nothing has yet watched it run. The row names the command anyway |

**Wired is not run, and the ledger is the only place that can tell them apart.**
A gate configured in a sitting and a gate that has refused something read
identically from the tree — both are a command in a file. So a row earns
*automated* the first time somebody watches it do its job, and reads
*unobserved* until then. That is not a deferral: there is nothing left to build,
and the row is a claim waiting on evidence rather than work waiting on somebody.
It is also the one row that closes itself — the first refusal makes it
*automated*, and a row still reading *unobserved* long after the repository
started merging changes is saying the gate has never once had an opinion.

**A row about something that is not in the repository is read back, or it is not
written as fact.** Branch protection, whether a named check is actually required,
whether the credential a step needs exists — none of that is in the tree, so
nothing about it can be inferred from the tree. A check named in a CI config is
evidence that somebody wrote it down, and no evidence at all that the platform
enforces it; the two look identical from inside a diff, which is the whole reason
this record exists. **So the row carries how it was read** — the command that
reads it again, and when it was last read — or it says plainly that it was not
read, and why. That is a second axis, not a fifth state: a row can be read back
from the platform and still be *unobserved*, because reading a setting is not
watching it stop something.

**And a row says what it leaves uncovered.** A gate wired over one language of
two, one package of five, one directory of a monorepo, is not a gate over the
repository — and a row reading *automated* with nothing after it will be read as
one, by somebody who was not in the room. Name the part that has no gate. A gate
that covers everything says so in the same breath and costs a clause.

**The tree is the authority on what applies; the ledger only says what is
wired.** A row reading *not applicable — no personas exist* in a repository that
has personas contradicts the tree, and a skill reading the ledger says so instead
of repeating it. That cross-check is what stops a typed record drifting — and
typed is what it has to be, because a record of what is *not* automated cannot be
generated by the automation that does not exist.

**A row deferred across two changes is either wired or written off.** The same
norm as a warning surviving two versions, for the same reason: a gap flagged in
every change and closed in none is indistinguishable from a gap nobody noticed.
Written off means the row becomes *not applicable*, with the reason in it — one
decision, made in the open, instead of an apology repeated forever.

### The wiring that must never gate

Two things on this page have to be wired and must never be able to fail a build:
the [report](#the-report-is-not-a-gate), and the
[rule-bound measure](testing.md#measure-the-rule-bound-tests-on-their-own-and-never-gate-it)
taken beside the gated coverage number. Neither is a gate, so neither belongs in
the table above — and the ledger's own *nothing in it that is not a gate* line is
what has been quietly displacing them. A repository names one as *not built yet*
in a sentence somewhere and nothing ever asks again, because a sentence is not on
any clock.

So the bindings carry **a second, shorter table**, in the same place and with the
same four states, for wiring that is expected and cannot gate:

| Wiring | Reads |
|---|---|
| the pull-request report | one of the four states, and *unobserved* until somebody has watched one arrive |
| the rule-bound measure, reported beside the gated number | one of the four states |

The same two-change clock applies, for the same reason. **Their absence is
harder to notice than a gate's, not easier** — a gate that is missing eventually
lets something through, and a report that is missing is silent by design.

The ledger also records **which version of the method the wiring was last
reconciled against**, so a later `setup` run diffs what the repository has
against what this page now names and offers the difference, rather than
re-deriving the state from scratch. That is a record about the installed process.
It is not provenance for a commit, and nothing else in the repository gains any.

**What changed between that version and the one installed is read from the
record the plugin ships with each version, never regenerated from the method.**
A generated list of what each version obliges is a second copy of the method
waiting to disagree with it; the record that shipped is where to look, and this
page and the skills as they now stand are what is asked. **And the stamp follows
the wiring, not the reading.** An audit that read every entry between, corrected
the record and wrote a row for each gap leaves it where it was; it moves when the
wiring is brought level. A stamp moved for having been looked at would read as
current over rows that are not.

### The boundaries

The two tables above say what refuses a change. This one says **what world the
tests that pass those gates ran in** — because both gates are satisfied by a
test that names its rule and reaches every line over a stand-in for the store,
and nothing else on this page can tell.

One row per boundary the app crosses: whatever it talks to that is not its own
code — the store, the clock, the network and each service on it, the browser or
terminal it is used through, the identity it signs people in with. **The tree
does not know what these are; the person does**, which is why the rows are
asked for in the sitting and never derived.

| A row reads | And means |
|---|---|
| **real** | tests reach the thing itself, and the row names what starts it here |
| **fake** | a stand-in with a suite that also runs against the real thing; the row says when that half was last green |
| **recorded** | replies captured from the real thing; the row says when, and how old they may be |
| **mocked** | a stand-in nothing checks — since which change, and the larger test that covers the path, if any. On the two-change clock |
| **unreachable** | no test here crosses it — why, whether it cannot be or was decided against — and every change touching it says so where the change is decided |

And every row says what it leaves uncovered, in the same breath, the way a gate
row says which part of the repository it does not cover. A real store at test
volume is not a real store at production volume, and the row says so.

**A row reading *real* is written after a test has reached the thing from here,
never before**, for the same reason a gate row reads *unobserved* until it has
refused something: a claim about what the tests reach is evidence or it is a
memory, and the two look identical on the page.

**The gate reads the rows, and it is the traceability gate rather than a third
one** — the same script that reads a rule-bound test for the id it claims reads
it for the stand-ins it uses. A rule-bound test that stands a double in for a
boundary reading *real* fails; a *fake* row naming no suite against the real
thing fails; a *recorded* row past its age fails; rule-bound tests present with
no table at all fail. What counts as a double is a binding — the patterns are
the language's, and a terminal application's name the framework's own test
harness beside the mocking libraries — and it is read only over the rule-bound
tests, because a unit test doubling everything is what unit tests are for.

**A *mocked* row past the two-change clock is either made real, given the suite
that makes it a fake, or written off** — and written off means *unreachable*
with the reason in the row, the way a deferred gate becomes *not applicable*: a
decision made in the open, after which every change touching that boundary says
so.

### The file every session reads first

CLAUDE.md is read by every session before anything under `specs/`, written by
the sitting and corrected by the audit — and, until now, refused by nothing. A
change that gutted it to three lines, or grew it into a copy of the method,
reached the default branch with every check green, and the first thing to
notice was the next session behaving strangely.

**The gate reads only what a script can decide**, and says so:

| Failure | What it means |
|---|---|
| a context file larger than the ceiling the bindings name | Something in it is a pointer that turned into a copy. Move the copy to the bindings and link it — or raise the number in the same change, with the reason beside it, so the growth is a line in a diff. |
| a context file with no ceiling row | A number nobody wrote is not a pass. The sitting writes the row from the file's size once it has finished with the file. |
| no context file at the root | The file every session reads first is missing. |
| no numbered list, or one longer than eight steps | The loop is missing, or has grown past what an agent follows at the moment it matters. The loop is the longest numbered run outside fenced blocks. |
| no fenced block | The commands are missing. |
| no link to the bindings that resolves | The one pointer every other command depends on is missing or points at nothing. |

What it does not read is prose. A stale pointer, a paragraph copied from the
plugin, a rule nobody follows — [`claude-md.md`](claude-md.md) rules all three
out, and only a mind can see them. They stay with the sitting that writes the
file and the audit that re-reads it, and a gate that claimed them would be
wallpaper by its second run.

**The traceability gate reads it, and it is not a third one**, for the reason
the boundaries were folded in: the same script that reads the spec layer for
its shape reads the file that points at it, and a third gate renames *both
gates* in every ledger, every injector and every bindings file already
written. Two rows in the ledger, one for the ceiling and one for the shape,
because a repository can have the file in shape and no number yet.

### And what is not wiring at all

A check that runs on somebody's own machine before they push — the
[run before the work leaves it](testing.md#and-again-before-it-leaves-this-machine)
— is neither of the two things above. It is not a gate, and it is not wiring
that must never gate. It is **local, opt-in, and bypassable on purpose**: every
version control that offers a hook offers a flag that skips it, and that flag
will be used, correctly, by somebody in a hurry at the end of a bad day.

So it gets **no row, in either table**. A row is a claim about what this
repository refuses, and a courtesy recorded as a refusal is the false green this
page exists to prevent — worse than no record, because a reader adding up the
rows would now count a check that anybody can walk past. An audit of the ledger
does not count it as coverage either, for the same reason.

If it is written down at all it belongs with the other things that are true of
one machine rather than of the repository, in the bindings' own prose: what it
runs, what it deliberately leaves to the pipeline, and the line somebody types to
opt in. Nothing reads it to decide whether a gate exists.

## The ids

Everything an audit of the ledger is held to is one list, here, and nothing an
audit checks is enumerated anywhere else. Three tables: the gates a ledger
carries a row for, the two pieces of wiring that must never gate, and the
checks an audit makes. **Every id is permanent** — the same promise a rule id
carries, for the same reason: a ledger in a consuming repository names these
ids, and a renamed one orphans every ledger at once. A check that is no longer
asked is retired *in place*, with the version and what replaced it, so an old
row reads *retired — drop it* rather than *unknown id*. A rename is a
retirement and a new id. The *aliases* column carries the labels ledgers used
before ids existed, so an audit can match an old row to its id and write the
id in.

*kind* says who answers a check: **mechanical** — a script, from the record,
the same way every time; **judgment** — a person or a model, from the command
the bindings name. *since* is the plugin release the check or gate arrived in,
and a consuming repository whose stamp is earlier than a row's *since* has
never been asked it. **It is written by the release, never by a person**: a
new row reads `next` until the merge that ships it, and the release step
writes the version in the same commit as the manifest and the changelog
entry. A retirement reads `next` the same way. The pull request that adds or
retires a row says so in an `## Ids` section, and the gate holds what it says
to the table's diff. *severity* orders what an audit reports — *platform*
before *boundary* before *wiring* before *record*.

### The gates a ledger carries

| id | kind | since | severity | retired | aliases | meaning |
|---|---|---|---|---|---|---|
| `gate:rule-to-test` | gate | 0.6.0 | wiring | — | rule → test · rule → case | a live rule no test claims fails |
| `gate:test-to-rule` | gate | 0.6.0 | wiring | — | test → rule · case → rule | a test claiming a rule that does not exist fails |
| `gate:planned-unclaimed` | gate | 0.6.0 | wiring | — | planned rule with a test | a `@planned` rule or workflow that is claimed fails — the tag should have come off |
| `gate:feature-to-workflow` | gate | 0.6.0 | wiring | — | feature → workflow | a feature naming no workflow, or a workflow that does not exist, fails |
| `gate:workflow-to-feature` | gate | 0.6.0 | wiring | — | workflow → feature | a workflow claimed by no feature fails |
| `gate:workflow-walked` | gate | 0.6.0 | wiring | — | workflow → test · workflow → case (walked end to end) | a workflow walked by no test fails |
| `gate:workflow-to-persona` | gate | 0.6.0 | wiring | — | workflow → persona | a workflow naming no live persona fails |
| `gate:persona-to-workflow` | gate | 0.6.0 | wiring | — | persona → workflow | a persona named by no workflow fails |
| `gate:journey-to-workflow` | gate | 0.6.0 | wiring | — | journey → workflow | a journey naming a workflow that does not exist fails |
| `gate:workflow-to-journey` | gate | 0.6.0 | wiring | — | workflow → journey | a workflow naming no journey warns, and does not fail |
| `gate:structure` | gate | 0.6.0 | wiring | — | structure | one feature per file, unique ids, every rule with an example, no example outside a rule |
| `gate:coverage` | gate | 0.6.0 | wiring | — | coverage · coverage — lines, branches, functions | a module under the thresholds fails |
| `gate:boundary-double` | gate | 1.2.0 | boundary | — | a rule-bound test doubling a boundary declared real | a rule-bound test standing a double in for a boundary reading real fails |
| `gate:boundary-fake-suite` | gate | 1.2.0 | boundary | — | | a fake row naming no suite against the real thing fails |
| `gate:boundary-recorded-age` | gate | 1.2.0 | boundary | — | | a recorded row past the age the bindings set fails |
| `gate:boundaries-table` | gate | 1.2.0 | boundary | — | | rule-bound tests present and no boundaries table fails |
| `gate:context-file-ceiling` | gate | 1.9.0 | wiring | — | | the context file larger than the ceiling the bindings name, or a context file with no ceiling row, fails |
| `gate:context-file-shape` | gate | 1.9.0 | wiring | — | | the context file missing, or without its loop, its commands, or its pointer to the bindings, fails |
| `gate:verified-to-fire` | gate | 0.6.0 | wiring | — | both gates verified to fire | every gate is broken on purpose and seen to fire |

### The wiring that must never gate

| id | kind | since | severity | retired | aliases | meaning |
|---|---|---|---|---|---|---|
| `wiring:pr-report` | wiring | 0.21.0 | wiring | — | the pull-request report | the report on every pull request, unobserved until one was watched arriving |
| `wiring:rule-bound-measure` | wiring | 0.21.0 | wiring | — | the rule-bound measure | the rule-bound measure reported beside the gated number |

Two prefixes a repository fills itself and this table never lists:
`boundary:<name>`, one per thing the app talks to, named in the sitting and
never derived; and `local:<name>`, a gate the repository added that the method
does not name — held to the same states, required by nothing.

### The checks an audit makes

| id | kind | since | severity | retired | aliases | meaning |
|---|---|---|---|---|---|---|
| `check:ledger-shape` | mechanical | 1.6.0 | record | — | | the three tables and the stamp line are in the shape the template gives them |
| `check:stamp-present` | mechanical | 0.21.0 | record | — | | the ledger carries the version it was reconciled against |
| `check:stamp-range` | mechanical | 1.1.0 | record | — | | the entries between the stamp and the plugin installed are listed |
| `check:stamp-ahead` | mechanical | 1.1.0 | record | — | | a stamp ahead of the plugin installed is said, and no range read |
| `check:range-empty-said` | mechanical | 1.1.0 | record | — | | a stamp at the plugin installed is said in a line |
| `check:changelog-reachable` | mechanical | 1.1.0 | record | — | | the plugin's changelog can be read from here |
| `check:entry-moved-here` | judgment | 1.1.0 | record | — | | each entry in the range moved something this repository holds, or is passed over in a line |
| `check:row-state-legal` | mechanical | 0.21.0 | record | — | | every ledger row is in one of the four states |
| `check:row-evidence` | mechanical | 0.21.0 | record | — | | an automated or unobserved row names a command; a deferred row names its change; a row about the outside carries how it was read |
| `check:row-uncovered` | judgment | 0.21.0 | wiring | — | | what a row leaves uncovered is named, and true |
| `check:number-from-config` | judgment | 0.31.0 | wiring | — | | a number a gate enforces is read from the config the gate reads |
| `check:demand-is-a-ratchet` | judgment | 0.31.0 | wiring | — | | a demand equal to today's score is reported as measured rather than chosen, unless it is the whole of what is in scope |
| `check:exclusions-in-config` | judgment | 0.31.0 | wiring | — | | what the demand does not reach lives in the tool's config, not only in the bindings |
| `check:na-vs-tree` | mechanical | 0.21.0 | record | — | | a not-applicable row's reason is not contradicted by the tree |
| `check:row-per-gate` | mechanical | 0.21.0 | wiring | — | | every gate in the table above has a row |
| `check:real-starts-here` | judgment | 1.2.0 | boundary | — | | what a real row names can be started from here |
| `check:real-not-doubled` | judgment | 1.2.0 | boundary | — | | no rule-bound test stands a double in for a boundary reading real |
| `check:fake-suite-green` | judgment | 1.2.0 | boundary | — | | a fake row's suite against the real thing exists, and was last green when the row says |
| `check:recorded-age` | mechanical | 1.2.0 | boundary | — | | a recorded row is within the age the bindings set |
| `check:mocked-clock` | mechanical | 1.2.0 | boundary | — | | a mocked row is not past the two-change clock |
| `check:merge-blocked` | judgment | 0.21.0 | platform | — | | a merge is actually blocked when the required check fails |
| `check:check-name` | judgment | 0.21.0 | platform | — | | the required check's name is the one the platform has |
| `check:who-bypasses` | judgment | 0.21.0 | platform | — | | who can bypass is read back, tokens and keys included |
| `check:credentials-present` | judgment | 0.21.0 | platform | — | | a credential the bindings claim is missing is read back from where the platform keeps it |
| `check:read-back-or-not` | mechanical | 0.21.0 | record | — | | every judgment line is read back with its command, or not read with why |
| `check:prose-phrases` | judgment | 0.21.0 | record | — | | the prose is read for *not built yet*, *to do*, *we should*, *for now* |
| `check:second-table` | mechanical | 0.21.0 | wiring | — | | the table for wiring that must never gate exists |
| `check:pr-report-row` | mechanical | 0.21.0 | wiring | — | | it holds the row for the pull-request report |
| `check:rule-bound-row` | mechanical | 0.21.0 | wiring | — | | it holds the row for the rule-bound measure |
| `check:sketch-row` | mechanical | 0.27.0 | record | — | | the bindings say which changes owe a sketch |
| `check:picture-row` | mechanical | 0.29.0 | record | — | | the bindings say what a change here must show, and it is not the sketch row |
| `check:skill-names` | mechanical | 1.0.0 | record | — | | every skill the record instructs by exists in this plugin |
| `check:word-not-a-skill` | judgment | 1.0.0 | record | — | | the same word used as ordinary prose is left alone |
| `check:loop-per-claude-md` | judgment | 1.1.0 | record | — | | the loop's own account says what the method now asks of each step |
| `check:deferred-clock` | mechanical | 0.21.0 | wiring | — | | no row is deferred across two changes |
| `check:hook-no-row` | mechanical | 0.26.0 | record | — | | a local hook has no row in either table |
| `check:sorted-by-severity` | mechanical | 0.21.0 | record | — | | what is open is reported dangerous first |
| `check:record-only` | mechanical | 0.21.0 | record | — | | the audit's corrections touched the record and nothing else |
| `check:last-line-command` | mechanical | 1.3.0 | record | — | | where wiring is left, the last line is the command that starts the sitting, with the rows after it |
| `check:no-line-when-clear` | mechanical | 1.3.0 | record | — | | where nothing is left for the sitting, no such line |

## Both gates are verified to fire

They are tested against deliberate violations rather than assumed to work. Break
each one in turn and read the message it produces:

| Injected fault | Expected |
|---|---|
| live rule with no test | fails |
| test names a nonexistent rule | fails |
| behaviour test outside a `rule()` block | fails |
| behaviour file with no `rule()` at all | fails |
| `@planned` rule that has a test | fails |
| a refusal test claiming a rule that is not `@refusal` | warns, does not fail |
| feature naming no workflow | fails |
| feature naming a workflow that does not exist | fails |
| workflow claimed by no feature | fails |
| workflow walked by no test | fails |
| workflow naming a persona that does not exist | fails |
| persona named by no workflow, tag removed | fails |
| journey naming a workflow that does not exist | fails |
| workflow naming no journey | warns, does not fail |
| a feature holding more rules than the soft limit | warns, does not fail |
| a feature longer than the soft limit | warns, does not fail |
| a module well under the coverage thresholds | fails |
| a fully covered module | passes |
| a rule-bound test doubling a boundary whose row reads real | fails |
| a fake row naming no suite against the real thing | fails |
| a recorded row past the age the bindings set | fails |
| rule-bound tests present and no boundaries table | fails |
| a context file past its ceiling | fails |
| a context file with no ceiling row | fails |
| no context file at the root | fails |
| a context file with no numbered list | fails |
| a loop of nine steps | fails |
| a context file with no fenced block | fails |
| a context file that does not link to the bindings | fails |

If you change either gate, re-check it the same way, and keep the results in the
repository's bindings where somebody can read what was actually tried.

**That record is read back from the injector, never typed.** It is the evidence
for the promise that no gate ships without a fault that makes it fire, and a
hand-copied list of what was injected drifts exactly the way a hand-maintained
map does — silently, and in the direction of looking finished. Whatever holds the
faults is the one that owns their names; the gates check the record against it,
so a fault added without a row fails the build rather than going unrecorded. The
same applies to any count of them: a total nobody derives is a claim that can
only go stale, and is better deleted than corrected.

**A gate that has never failed is not known to be a gate.**
