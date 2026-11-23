# The gates

*From: every promise is checked by something that can fail.*

Two gates: **traceability** and **coverage**. Coverage alone rewards tests that
touch code without asserting anything anyone asked for; traceability alone
rewards tests that name a rule and check it shallowly. Together they are hard to
satisfy dishonestly. **The commands, thresholds and tool names are bindings**,
in the repository's `specs/setup/README.md`; this page is what they must mean.

## A failure says why

**Each rule a gate enforces is written once: as a row in a table on this page —
the failure, and what it means.** No prose elsewhere restates it. **When a gate
fails, it prints that row**: where the failure is, and what it means — the reason
and the fix — in words taken from the row. The agent that broke the rule learns
it at that moment, from the gate, instead of from a page it was meant to have
read. A failure that prints only *what* failed is half a gate.

Warnings follow the same shape, in their own tables. Keep them scarce: **a
warning surviving two versions either becomes an error or is deleted** — four new
kinds at once turn the output into wallpaper, and wallpaper reads as green.

## Gate 1 — traceability

Enforced in **both directions**, because each alone is worthless:

```
rule  →  test     every live rule must be claimed by a test
test  →  rule     every behaviour test must name the rule it exists for
```

| Failure | What it means |
|---|---|
| a live rule with no test referencing it | Behaviour was specced and never verified. Write the test, or tag the rule `@planned` if it is not built yet. |
| a test claiming a rule id that does not exist | Usually a typo, or an id that was renamed. Rule ids are permanent. |
| a feature file with no test against any of its rules | A whole component is unverified. |
| a test outside a `rule()` block in a behaviour file | An untraced behaviour test. Move it inside a block, or into the unit folder. |
| a behaviour file with no `rule()` at all | The same; this is the check that stops coverage filler. |
| a `@planned` rule that *does* have a test | The tag should have come off in the change that made it true. |
| a rule-bound test marked skipped, focused or expected to fail | It claims nothing; the rule it names is untested. What counts as a marker is the runner's, and a binding. |
| fewer rule-bound tests ran than the tree holds | The runner did not see what the gate sees — a harness that stopped early, a file the discovery pattern missed, a class it does not collect. Whatever the summary line says, the build fails. More is not a failure. |
| a rule crossing a boundary the bindings have no row for | A `@crosses:` names a boundary nobody declared. Add the row, or name one that exists. |

| Warning | What it means |
|---|---|
| a unit test claiming a rule | It probably belongs with the behaviour tests. |
| a test asserting nothing happened, claiming a rule not tagged `@refusal` | Either the rule promises absence and needs the tag, or the test asserts the wrong thing. |
| a feature file past the repository's soft size limits | Small per-component files are the point; split it. A hard cap is not. |
| a rule crossing a boundary, with a single example | One example cannot be both the ordinary case and the boundary misbehaving. Whether the second really is the boundary going wrong is a reading, for the spec step and review. |

The output worth having is a per-feature matrix — traced, untraced, planned —
then a count, read even when green.

### The same loop, one layer up

```
feature   →  workflow              every feature says what it serves
feature   →  feature               every feature it says it uses exists
workflow  →  feature               no workflow nothing implements
workflow  →  test                  no walkthrough nothing walks
workflow  →  persona               no workflow for nobody
persona   →  workflow              no persona nobody does anything as
journey   →  workflow              no dangling reference
workflow  →  phase                 no dangling reference
```

| Failure | What it means |
|---|---|
| a feature naming no `@workflow:` | It serves nothing anybody wrote down. Tag it, or the thing it serves is missing from the workflows. |
| a feature naming a workflow that does not exist | A typo, or a renamed id. |
| a feature using a feature that does not exist | The shared feature was renamed or split. Name the id it carries now, or drop the tag. |
| a `@uses` on a rule rather than the feature | It belongs on the Feature line; the rule's words say which rule it builds on. |
| a workflow claimed by no feature | Specced and never built. Tag a feature, or tag the workflow `@planned`. |
| a workflow walked by no test | Its `Example:` blocks are a costume. Write the walkthrough. |
| a workflow naming no live `@persona:` | A workflow for nobody, or for a `@retired` persona only. |
| a persona named by no workflow | Nobody does anything as them. Give them a workflow, or tag the file `@retired` — for a persona no workflow names *yet*, not a shelf. |
| a `@planned` workflow that *is* claimed | The tag should have come off. |
| a journey naming a workflow that does not exist | A dangling reference is wrong, not a judgment call. |
| a workflow naming a phase no journey it names has | A typo, or a phase heading renamed without retagging its workflows. Naming no phase is fine. |

| Warning | What it means |
|---|---|
| a workflow naming no `@journey:` | Where an attempt sits in the arc is a judgment, so this warns rather than fails. |

- **A repository's own pipeline is not an attempt anybody makes with the
  product.** No feature describes the gates, the release or the checks that prove
  them; they are held by the faults below and their record in the bindings. A
  feature naming no workflow is answered by a missing workflow or by a fault —
  never by a second kind of tag.
- **Two checks are left out on purpose**: whether a journey was looked at since
  its workflows changed, and whether features piled up under a workflow since it
  was edited. Both are git questions a single-commit checkout answers with
  silence, so they would pass forever while looking enforced.

### The second half of the output is the map

Every workflow, who it is for and the features serving it — **generated, never
typed**, because a hand-kept list of what implements what has already drifted.
Then every journey, its phases in order, and under each the workflows naming it:
a phase nothing names says so, and a workflow naming the journey and no phase is
listed apart, as not yet placed.

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

- `@feature:<id>` and `@rule:<id>`, unique across the repository. Every rule
  has at least one `Example:` — a rule with no example is an opinion.
- **Rule, workflow and persona ids are permanent.** Reword freely; a changed id
  orphans every test pointing at it.
- `@planned`: specced, not built — the normal state of a new rule, dropped in the
  change that makes it true.
- `@refusal`: the promise is that nothing happens, verified only by a test
  asserting absence. Without the tag that honest test reads as the wrong kind.
- `@crosses:<name>` on a Rule: a boundary it cannot be true without, by the name
  after `boundary:` in its [row](#the-boundaries). Never on a Feature.
- `@workflow:<id>` on every feature, repeatable. `@uses:<feature-id>` on a
  feature building on a rule another feature owns — opt-in, one-way, on the
  Feature line, the rule citing the shared rule by id rather than restating it.
- `@persona:<id>` and `@journey:<id>` on every workflow, **not on features**:
  a feature reaches its persona through its workflow, and a second path is a
  second thing to keep true.
- `@phase:<name>` on a workflow, optional and repeatable: a phase heading of its
  journey's map, lower case, each run of other characters one hyphen —
  *Putting it in* is `putting-it-in`.

**Structure**: one feature per file, no scenario outside a rule, no duplicate
ids, nothing unnamed. A workflow file is the one exception — one bounded attempt,
no `Rule:`, its scenarios hanging off the `Feature:` line.

## Gate 2 — coverage

**Lines, branches and functions — all three; the numbers are the repository's.**
Aim at branches: line counting can mark an uncalled function's declaration
covered.

| Failure | What it means |
|---|---|
| a module under the thresholds | The tests do not reach it. Test it, or name it in the runner's exclusions with why. |

**The runner refuses to pass on a measurement of nothing**: with no source yet it
says so and skips the thresholds, and arms itself when the first module lands.
100% of zero files is the most convincing false green there is.

## The report is not a gate

A report on each pull request — spec health, coverage, what is specced and not
built — is wired in every repository, and **it cannot fail the build**, including
on its own failures: a missing token or a base that will not check out leaves the
build unaffected and the report silent.

- **It recomputes nothing.** The gate hands its numbers over; a report that
  re-derives them is a second copy of the gate's logic.
- **It reports what moved** — *+1*, not *12 live rules* — so it reads the base
  as well as the branch.
- **It goes where the decision is made**, on the pull request.
- **It carries the pipeline's own run beside the body's run block**
  ([repository.md](repository.md#and-the-run-it-rests-on)), so the two disagree
  where the reviewer looks — and gates on nothing there.

## What a change costs a workflow

A change can leave every rule true and every workflow slower. **So the report
also says what the change did to the cost of each workflow walk, against its own
base.**

- **Both sides on one runner, in one job, in turns** — so what slows the runner
  slows both.
- **Each walk is measured where the change can move it**: the front end with the
  service's answers replayed at a fixed delay, the back end without the interface,
  and the whole walk once end to end, each its own line. A front end is weighed
  in what it ships, how long its pages take, and when each workflow's feature is
  ready.
- **Three verdicts**: no change, worse, or inconclusive with its reason — never
  read as *no change*.
- **Two numbers per measure, written before the change runs**: the noise, below
  which nothing is read, and the allowance a real slowdown may use.
- **A time never fails the build**
  ([testing.md](testing.md#a-test-that-fails-sometimes-is-worse-than-no-test));
  **a count may carry a budget that does** — bytes, requests, queries.
- **Past the allowance, a slowdown is answered, not refused**: the pull request
  names the walk and says why.
- **The numbers live in one versioned file**, and moving them is shown beside
  the change they allow.
- **One run counts**: rounds repeat inside the job, never a re-run until green.

The comparison ships with the method and the sitting copies it in; the walks are
the repository's. A walk too costly to repeat is a reason written down, not a gap.

## What is wired, and what is not

The bindings carry a **ledger**: one row per gate named here, by its id in
[requirements.md](#the-ids), and anything else only under the `local:` prefix.

| A row reads | And means |
|---|---|
| **automated** | it runs, and the row names the command |
| **not applicable** | it cannot apply here, and the row says why — a decision, not a gap |
| **deferred** | it applies and is unbuilt — since which change, and why |
| **unobserved** | it is wired, and nothing has yet watched it run; the row names the command anyway |

- **Wired is not run.** A row earns *automated* the first time somebody watches
  the gate refuse something; until then it reads *unobserved*.
- **A row about something outside the repository is read back**, with the command
  that reads it again and when — branch protection, a required check, a
  credential — or it says it was not read, and why. A check named in a CI file is
  no evidence the platform enforces it.
- **A row says what it leaves uncovered** — one language of two, one package of
  five.
- **The tree is the authority on what applies.** A *not applicable* row the tree
  contradicts is reported, not repeated.
- **A row deferred across two changes is wired or written off** — *not
  applicable*, with the reason.
- **The ledger records the version of the method the wiring was last reconciled
  against.** What changed since is read from the record the plugin ships with
  each version, never regenerated from the method, and the stamp moves only when
  the wiring is brought level — never for having been looked at.

### The wiring that must never gate

The [report](#the-report-is-not-a-gate), the
[rule-bound measure](testing.md#measure-the-rule-bound-tests-on-their-own-and-never-gate-it)
and the run beside the claim are wired and cannot fail a build, so they get **a
second, shorter table**, in the same four states and on the same two-change
clock:

| Wiring | Reads |
|---|---|
| the pull-request report | one of the four states, and *unobserved* until somebody has watched one arrive |
| the rule-bound measure, reported beside the gated number | one of the four states |
| the run beside the claim | one of the four states, and *unobserved* until somebody has watched the two disagree |

Their absence is harder to notice than a gate's: a missing report is silent by
design.

### The boundaries

**What world the tests ran in.** One row per boundary the app crosses — the
store, the clock, the network and each service, the browser or terminal, the
identity it signs people in with — asked of the person in the sitting, never
derived.

| A row reads | And means |
|---|---|
| **real** | tests reach the thing itself; the row names what starts it here |
| **fake** | a stand-in with a suite that also runs against the real thing; the row says when that half was last green |
| **recorded** | replies captured from the real thing; the row says when, and how old they may be |
| **mocked** | a stand-in nothing checks — since which change, and the larger test covering the path, if any; on the two-change clock |
| **unreachable** | no test here crosses it — why — and every change touching it says so where it is decided |

Each row says what it leaves uncovered, and a row reads *real* only after a test
has reached the thing from here. The traceability gate reads the rows — over
rule-bound tests only, with what counts as a double a binding:

| Failure | What it means |
|---|---|
| a rule-bound test doubling a boundary whose row reads *real* | It tests the double, not the rule. Reach the real thing, or change the row honestly. |
| a *fake* row naming no suite against the real thing | A fake nothing checks is *mocked*. Name the suite, or say *mocked*. |
| a *recorded* row past the age the bindings set | The replies may no longer be what the service says. Record again. |
| rule-bound tests present and no boundaries table | Nobody said what world the tests ran in. Write the rows. |

A *mocked* row past the two-change clock is made real, given its suite, or
written off as *unreachable* with the reason.

### The file every session reads first

The traceability gate reads the context file for what a script can decide — never
its prose, which [`claude-md.md`](claude-md.md) holds the sitting and the audit
to. Two ledger rows: the ceiling, and the shape.

| Failure | What it means |
|---|---|
| a context file larger than the ceiling the bindings name | A pointer turned into a copy. Move it to the bindings and link it — or raise the number in this change, with the reason beside it. |
| a context file with no ceiling row | A number nobody wrote is not a pass. Write it from the file's size once the sitting is done with it. |
| a ceiling above the limit the method names | The number is the repository's only up to the reader's own limit ([`claude-md.md`](claude-md.md#length)). |
| no context file at the root | The file every session reads first is missing. |
| no numbered list, or one longer than eight steps | The loop is missing, or has grown past what an agent follows. The loop is the longest numbered run outside fenced blocks. |
| no fenced block | The commands are missing. |
| no link to the bindings that resolves | The pointer every command depends on is missing or points at nothing. |

### The description a pull request carries

The repository's description rules
([repository.md](repository.md#and-the-point-before-the-evidence)) are partly a
reading and partly a script's. The script's part runs on every pull request
event, an edited description included; the length is reported, never failed.

| Failure | What it means |
|---|---|
| a template heading or checkbox missing, renamed or out of order | The template is the repository's shape for every description. Fill it in its order, and put what it has no field for above its first heading as plain lines. |
| a heading added beside the template's | A second shape for the reviewer to read. Put the text under the template's own field, or above its first heading. |
| an issue, pull request or incident named by a bare number or address | The reader has to open it to learn what it is. A link with its title; its id and title in words where it has no address. A closing line is exempt. |

### And every part that only grows

The bindings' **Ceilings** row names each part that only grows and its size
([process.md](process.md#the-rules)); the traceability gate reads it.

| Failure | What it means |
|---|---|
| a part larger than its ceiling | The change grew it past what was agreed. Cut it back — or raise the number in this change, with the reason beside it. |
| no Ceilings row | A number nobody wrote is not a pass. Write each part's size once the sitting has finished. |

### And what is not wiring at all

A check run before a push ([testing.md](testing.md#and-again-before-it-leaves-this-machine))
is **local, opt-in and bypassable on purpose**, so it gets **no row in either
table**: a courtesy recorded as a refusal is a false green, and the audit does not
count it as coverage. If it is written down at all, it is in the bindings' prose,
with what it runs and how to opt in.

## The ids

Moved to [`requirements.md`](requirements.md#the-ids); these headings stay so old links land.

### The gates a ledger carries

### The wiring that must never gate

### The checks an audit makes

## Both gates are verified to fire

**Every row in a *Failure* or *Warning* table above is a fault to inject.** Break
each one in turn, and read what the gate prints: it fails, or warns, and it
prints the row's meaning. Add a module well under the coverage thresholds, and a
fully covered one, which must pass.

The record of what was tried lives in the repository's bindings and is **read back
from the injector, never typed**: whatever holds the faults owns their names, and
the gates check the record against it, so a fault added without a row fails the
build. Any count of them is derived the same way, or deleted.

**A gate that has never failed is not known to be a gate.**
