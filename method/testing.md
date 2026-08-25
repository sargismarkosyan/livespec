# Writing tests

## First: what proves a rule is true here

Everything below assumes there is code to call. **Ask before assuming that**, and
record the answer in `specs/setup/README.md` — it is the binding both gates rest
on, and it is the one nothing else in this method can derive for you.

There are two honest answers.

**An ordinary test suite.** The common one, and the rest of this page. Behaviour
is proved by calling the thing and asserting what came back, and a test names the
rule it exists for through the repository's own binding helper.

**Graded cases**, for a repository whose product is *judgment* rather than code —
a set of instructions an agent reads, a prompt, a policy. There is no function to
call. Behaviour is proved by running the thing against a situation and grading
what came out, and a case names the rule it answers to the way its runner
supports.

**These are not equals, and a repository choosing the second should know why.** A
graded case is slow, costs money every time it runs, and is scored by a model
rather than asserted — so a suite of them is rarely run on every commit, and a
green gate over them usually means *the cases exist and can fail*, not *the cases
passed*. Above all it proves a weaker thing: that judgment held on one prompt,
not that a function is correct. Where there is code to call, calling it is the
better answer, and a repository that has both should not run two ways of testing
the same behaviour.

The second answer exists because the first is impossible in some repositories,
not because it is a modern alternative to it.

**Do not invent a third.** Whatever the answer, use the tooling that already
builds that kind of suite. A bespoke format invented during a setup sitting is a
format with one user, no documentation and nobody to ask. And when that tooling
cannot run where the suite has to — gated, unreleased, wrong platform — the
fallback is another platform that already runs such suites, never a format of
one's own. Keep the cases in the format the repository's gates read, so the
tool that could not run stays a runner the suite might gain rather than a
migration it owes.

## The two kinds

```
tests/behaviour/    answers to a Gherkin rule. Everything user-visible.
tests/workflows/    one walkthrough per workflow, end to end.
tests/unit/         internals. The one exemption from rule references.
tests/support/      helpers. Not tests; not run.
```

The discovery pattern is the repository's — `specs/setup/README.md`.

## Behaviour tests

Every behaviour test declares the rule it exists for:

```js
rule('add-goes-to-top', () => {
  test('a new one appears above the older ones', () => {
    // ...
    assert.deepEqual(app.contents(), ['the new one', 'the older one']);
  });
});
```

The `rule()` helper is the repository's — `specs/setup/README.md` says where it
lives and what the imports are.

`rule()` looks the id up in `specs/features/` and throws immediately if it does
not exist, or if it is still tagged `@planned`. The error lists the ids that do
exist, which is usually enough to spot the typo.

It wraps the runner's grouping call, so the rule id and its text appear in the
test output:

```
▶ [add-goes-to-top] A new one goes to the top
  ✔ a new one appears above the older ones
```

Every `test()` in a behaviour file must sit **inside** a `rule()` block. One at
the top level is an untraced behaviour test and the gate rejects it.

One rule may have several tests, and one file may cover several rules — but a
file should stay recognisably about one component, like the feature file it
mirrors.

### Write them against the rule, not the implementation

The Gherkin `Example:` blocks are the specification of what to assert. If the
rule says one line reads above another, assert the rendered order — not that a
sort function was called. A behaviour test that
passes while the screen is wrong is worse than no test, because it costs the
gate its meaning.

`ruleText(id)` from the same helper returns the parsed rule if a test wants to
read its text.

## Unit tests

For internals no Gherkin rule describes: a parser, a serialiser, an id
generator, the gate tooling itself. No `rule()` call, no reference.

**This exemption is the reason the rest works.** Without an honest place to put
an internals test, coverage pressure turns behaviour tests into filler that names
a rule and asserts nothing. The rule of thumb: if you cannot name the Gherkin
rule it answers to, it is a unit test — and if you can, it does not belong here.

The gate warns when a unit test claims a rule, which usually means the file is in
the wrong folder.

## The environment the tests run in

Whatever it is — a real browser, a headless DOM, no DOM at all — it is a binding,
and `specs/setup/README.md` describes it. Two things about it are method:

- **Build the world fresh per test.** Shared state between tests is the commonest
  cause of a suite that passes in order and fails one file at a time, and a
  leaked key from an earlier test is a genuinely nasty failure to diagnose.
- **Everything that can be tested without that environment should be.** A test
  that needs a DOM to check a decision is testing two things and reporting one.

## Coverage

The thresholds are the repository's. The judgment is not:

- Aim at branches first. Lines follow; branches are where the untested paths
  hide, and V8's line counting is generous about function declarations.
- Error-handling paths in storage reads are real behaviour with real rules behind
  them, not coverage chores. Corrupt the stored value and assert the app still
  opens on something usable.
- If a branch is genuinely unreachable, it should not be there. Deleting it is a
  better fix than a test that pretends to reach it.

### Measure the rule-bound tests on their own, and never gate it

Take coverage twice: once over the whole suite — that is the gated number — and
once over the **behaviour and workflow tests alone**. The second says how much of
the product the *specification* actually reaches, which is a different question
from how much of it is covered, and it is invisible unless the split exists. A
repository where the gated number is high and the spec-bound number is low has
specs describing a corner of what it does.

It belongs in the report and **never in a threshold**. Gated, it would push people
to write rules in order to move a number, which is the failure this method
already names about coverage on its own — and the whole point of the second
figure is that it is diagnostic rather than a bar to clear.

It is also the number that makes the unit-test exemption legible: unit tests
raise the gated figure and not this one, which is exactly right and only visible
once both are printed.

## A test that fails sometimes is worse than no test

Both gates are only worth what their reliability is worth. A test that fails two
runs in five teaches everyone to press re-run, and from then on a real failure
looks like the usual noise.

**No test may depend on chance, timing, or ordering to pass.** The usual
sources, in the order they tend to appear:

- an assertion resting on a probability rather than a guarantee — that generated
  values will not collide, that a sample falls within a range;
- a timeout, or anything assuming one operation completes before another;
- state left behind by an earlier test, so the suite passes in order and the
  file fails on its own.

When an assertion is probabilistic, the fix is almost never a looser threshold
or a retry. Either the code should offer a guarantee strong enough that the
probability stops mattering, or the test is asking a question that cannot be
answered reliably and needs to ask a different one.

The tell is a test that passes locally and fails on CI, or that passes on a
re-run with nothing changed. Treat it as a defect in the test, at the same
priority as a defect in the code, because a gate nobody trusts is not a gate.

## Before committing

Run the repository's verification — both gates, the same thing CI runs. The
command is in `specs/setup/README.md`; what each failure *means* is in
[gates.md](gates.md).
