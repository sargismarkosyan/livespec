# Writing tests

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
