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

So the bindings carry a **ledger**: one row per gate named on this page, and
nothing in it that is not one.

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
| a module well under the coverage thresholds | fails |
| a fully covered module | passes |

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
