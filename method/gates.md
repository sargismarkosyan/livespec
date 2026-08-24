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
belongs with the behaviour tests — and when a feature file grows past the repo's
soft size limits.

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
— earns its place only if it **cannot fail the build**. It runs after both gates
have passed, so it only ever describes a green run.

And it recomputes nothing. If the traceability gate passed, that *is* the proof
every live rule has a test; a report that re-derives it is a second copy of the
gate's logic waiting to drift out of sync.

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

**A gate that has never failed is not known to be a gate.**
