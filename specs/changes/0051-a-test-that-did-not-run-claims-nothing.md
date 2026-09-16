# Spec 0051: a test that did not run claims nothing

- **Status:** approved
- **Issue:** none — spec B of the plan *Green Means Real* (2026-09-08), the
  second of four the maintainer ordered A, B, C, D, taken up now that the
  CLAUDE.md report is closed. Spec A shipped as
  [`0039`](0039-the-world-a-test-runs-in.md).
- **Depends on:** [`0039`](0039-the-world-a-test-runs-in.md), whose shape it
  has — a check folded into the traceability gate, with ids, rows and faults
  — and [`0041`](0041-an-audit-that-cannot-stop-early.md), which gave this
  repository the ordinary tests this change is first proved on.

## Who this is for

[`agent-accelerated-owner`](../personas/agent-accelerated-owner.md), in
[`adopt-the-process`](../workflows/adopt-the-process.feature), at the sitting
that wires the gates and at every change after it whose verification is read
as green. The persona line is the one spec A stood on: *"checking the result
by reading is not available"* — a green build is what stands in for reading.
Today a green says every live rule has a test naming it. It does not say the
test ran. A rule-bound test under a skip marker, or in a class the runner
stopped discovering, leaves the build exactly as green as before, and the
person who does not read the tests has no way to tell.

**This lengthens the sitting by nothing anybody types.** Section 4 writes a
few more lines into the gate script it already writes and one line into the
bindings beside the discovery pattern. What it shortens is every change after:
a skip landed to get a red build green is refused, where today it is the
cheapest way past a failing test that nothing notices.

Two always-promises are touched and held. **`gates-are-proven`**: two faults
prove the new checks fire, here and in the method's table for every sitting.
**`always-green`**: the gate is the consuming repository's, written by `setup`
the way every gate is.

## The job behind the request

The literal ask is the plan's: *"A test that did not run claims nothing. Skip,
only and expected-failure markers untest the rule; the runner's count must
match the tree's."* Behind it, the deck's mechanisms: failing tests skipped or
weakened and the work declared complete; a summary that read *4966 of 4966*
when the run was *4985 of 4992*; a harness that escaped.

The job: **a green verification should mean the rule-bound tests ran, not that
they exist.** Both gates today are satisfied by a test that names its rule and
never executes, because the traceability gate reads the claim off the source
and the runner's summary line reads green with a skip in it. This repository
is the first proof, made on 2026-09-16 on its own tests, and reverted:

- `@unittest.skip` on one rule-bound test under `tests/`: `tests.py` printed
  *OK (skipped=1)* and exited 0; `trace.py` counted the claim and printed *90
  live rules traced*. Nothing red.
- The class holding two rule-bound tests made no longer a `TestCase`, so the
  runner never discovers it: `tests.py` printed *OK*, ran two fewer tests than
  the tree holds, and said nothing about the difference; `trace.py` counted
  both claims. Nothing red.

livespec already refuses exactly this one layer up: the injection record holds
*a case with no row in the table* and *a row for a case nobody has*, both
failing. This is the same reconciliation for the tests a repository runs.

## Why now

Because the CLAUDE.md report is closed and this is the next item in the
maintainer's own order. And because the count is now measurable here: since
`0041` this repository runs fifty-nine ordinary tests bound to rules, which is
enough to have the gap and enough to prove the fix on before any consuming
repository is asked to wire it.

## The end value

A rule-bound test that did not run claims nothing, and the build says so:
naming the marker where there is one, and the two numbers where the runner saw
fewer tests than the tree holds. A skip is a way of making a rule untested in
the open, never a way of making it pass.

**How we would know it worked:** the two runs above go red — the first naming
`test_no_file_at_the_root_fails`, its skip marker and the rule it leaves
untested; the second saying the tree holds fifty-nine and the runner ran
fifty-seven — and the same two edits, undone, go green again. In a consuming
repository, the sitting's fault record carries both.

## What changes

1. **[`gates.md`](../../method/gates.md), Gate 1's failure table**, two rows:
   *a rule-bound test marked skipped, focused, or expected to fail* — it
   claims nothing; the rule it names is untested, and the gate says so rather
   than counting the marker as a test — and *fewer rule-bound tests ran than
   the tree holds* — the runner did not see what the gate sees: a harness that
   stopped early, a file the discovery pattern missed, a class the runner does
   not collect, or a count somebody edited; whatever the summary line says,
   the build fails. The id table gains two gate rows, `since: next`:

   | id | severity | meaning |
   |---|---|---|
   | `gate:skipped-test-claims-nothing` | wiring | a rule-bound test marked skipped, focused or expected to fail claims no rule, and fails |
   | `gate:fewer-ran-than-exist` | wiring | the runner reporting fewer rule-bound tests than the tree holds fails |

   The *Both gates are verified to fire* table gains the two faults.
2. **[`testing.md`](../../method/testing.md)**, under *Behaviour tests*: a
   test that did not run claims nothing — a skip, an only, an expected
   failure, whatever the runner calls it, leaves the rule it names untested
   and the gate reads it that way; and the runner says what it ran, per test,
   in a form the gate can count, because the summary line is what gets quoted
   and every fabricated result on record was a summary. What counts as a
   marker, and the form of the report, are bindings.
3. **`trace.py` here** reads the tests by their syntax rather than by a
   regular expression: a function bound with `rule()` that also carries one
   of the markers the bindings name — for this repository, `unittest`'s
   `skip`, `skipIf`, `skipUnless` and `expectedFailure` — claims nothing, and
   the gate fails naming the test, the marker and the rule. **`tests.py` here**
   counts the test methods the tree holds and compares with the *Ran N* the
   runner prints; fewer fails with both numbers, and more does not.
4. **`inject.py`**: two faults. *A skipped rule-bound test claiming a rule* —
   the fixture's one test under `@unittest.skip` — fails the traceability
   gate; *the runner ran fewer rule-bound tests than the tree holds* — a
   second test file whose class is not a `TestCase`, so the runner never
   collects it — fails the tests gate with the two numbers.
5. **[`tools/doctor.py`](../../tools/doctor.py)'s registry** gains the two
   gate rows, and **[`templates/bindings.md`](../../templates/bindings.md)**
   the two ledger rows, so a consuming repository learns of them at its next
   audit the way it learned of the boundary gates.
6. **[`setup`](../../skills/setup/SKILL.md) §4**, under *One command runs
   both*: the runner reports what it ran, per test, where the gate can count
   it; the form is a binding beside the discovery pattern; the gate compares
   and fails on fewer; where the runner cannot say per test, the bindings say
   so and name what that leaves open, rather than reading the summary line as
   the count. **[`doctor`](../../skills/doctor/SKILL.md) §1** gains the
   reading: the two rows read *unobserved* until somebody has skipped a
   rule-bound test and watched the gate refuse it.
7. **This repository's bindings**: two rows *automated* — `trace.py` for the
   marker, `tests.py` for the count — the *How a case names its rule* row
   saying which markers empty a claim here, and the fault record regenerated.
8. **Three rules**, `@planned`, in a new file; **a test file** claiming the
   first two by running the gates against the injector's fixture; and
   **case 12 gains a grader and a tag** for the third — the sitting leaves a
   gate that reads the runner's per-test report and a fault record with the
   two rows, or says why it cannot. One re-run rather than a new case, as the
   plan chose.

**Rules added or changed** — the `@rule:` ids in `specs/features/`:

| Rule id | Feature file | New or changed |
|---|---|---|
| `a-test-that-did-not-run-claims-nothing` | `features/wiring/what-ran.feature` | new, `@planned` — proved by tests |
| `fewer-ran-than-exist-is-a-failure` | `features/wiring/what-ran.feature` | new, `@planned` — proved by tests |
| `the-sitting-wires-what-ran` | `features/wiring/what-ran.feature` | new, `@planned` — claimed by case 12 |

**No description changes, so no should-not-fire case is owed.** `setup`'s
description carries *wire the two gates in that project's own language*;
`doctor`'s carries *check every claim its bindings make*. `context-budget`
stays at 4321 of 5000.

## What we are not doing

- **Not catching a test that runs and asserts nothing.** That is spec C's
  reported measure and the reviewer's reading; a count cannot see it.
- **Not naming the markers in the method.** `skip`, `only`, `xfail`,
  `expectedFailure` are the runners' words; the bindings carry the list for
  the language in hand, and `setup` proposes the runner's usual set.
- **Not failing on a skipped unit test.** A test outside the rule-bound
  folders that claims no rule may skip as it likes; the gate reads markers
  only where a claim is made, for the same reason it reads doubles only
  there.
- **Not failing on more ran than exist.** Inherited and generated tests run
  more than the tree's static count; the failure is fewer, which is the only
  direction that hides anything.
- **Not a third gate.** As in `0039` and `0048`: the traceability gate reads
  the claim, and here the runner's own gate reads the count.
- **Not touching the eval cases' reconciliation.** The board's faults already
  hold it for cases, and the bindings say so.

## Data

No storage. Files that move: `method/gates.md`, `method/testing.md`,
`.github/scripts/trace.py`, `.github/scripts/tests.py`,
`.github/scripts/inject.py`, `tools/doctor.py`, `templates/bindings.md`,
`skills/setup/SKILL.md`, `skills/doctor/SKILL.md`, `specs/setup/README.md`,
one new `.feature`, one new test file, `evals/12-setup-drives-the-sitting/`,
`evals/README.md`, and this spec.

**This spec commit stales nothing.** Three rules, `@planned`, claimed by
nobody. `verify.py` exits **2** for the rows already owed and no other
reason.

**The implementing change adds no stale row that is not already red.** It
edits both skill bodies and case 12, all already owed; it adds no case.

**What the pull request owes.** `method/`, `templates/`, `tools/` and two
skills move — **`minor`**, two new failures in a gate — a `## Changelog`
section, a Gherkin block for the new `.feature`, and an `## Ids` section:
*added `gate:skipped-test-claims-nothing`, `gate:fewer-ran-than-exist`*.

## Risks

- **A runner that cannot report per test.** Then the bindings say so and name
  what that leaves open, and the row reads *not applicable* with the reason —
  a decision in the open, which the third rule's second example holds.
- **A static count that disagrees with a legitimate run.** Inherited and
  generated tests are the known case, and they run *more*; the gate fails
  only on fewer. A repository whose runner legitimately runs fewer than the
  tree holds — a platform-conditional test — marks it with the skip marker,
  which is the first rule's business and names the rule it leaves untested.
- **The marker list drifts from the runner.** It is a binding beside the
  discovery pattern, and the audit's `check:number-from-config` habit
  applies: read it where the gate reads it.
- **Always-promises.** `always-green`: the failure is the consuming
  repository's own gate. `ids-are-permanent`: two ids added, none renamed.
  `never-implements`: gate scripts and prose.

## Acceptance checks

1. `python3 .github/scripts/inject.py`: 106 faults caught, the two new ones
   reading *fails*, the fixture green.
2. Skip `test_no_file_at_the_root_fails` by hand: `trace.py` exits 1 naming
   the test, `@unittest.skip` and its rule. Make `WhatOnlyAMindCanRead` a
   plain class: `tests.py` exits 1 with *the tree holds 59 test(s); the runner
   ran 57*. Restore both: green.
3. `tests.py`: green, the new file's tests each naming a rule.
4. `checks.py`: the tool and the table one list, the two ids in both.
5. `verify.py` exits 2 for the rows already owed; the pull request carries
   `minor`, `## Changelog`, `## Ids` with the two ids added, and the Gherkin
   block.
