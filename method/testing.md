# Writing tests

*From: every promise is checked by something that can fail.* Each rule here
is how a test earns the claim that a rule is true.

## First: what proves a rule is true here

Everything below assumes there is code to call. **Ask before assuming it**, and
record the answer in `specs/setup/README.md`: both gates rest on it, and nothing
in the method can derive it for you. There are two honest answers.

- **An ordinary test suite** — the common one, and the rest of this page.
  Behaviour is proved by calling the thing and asserting what came back, and a
  test names its rule through the repository's binding helper.
- **Graded cases**, where the product is *judgment* — instructions an agent
  reads, a prompt, a policy — and there is no function to call. Behaviour is
  proved by running it against a situation and grading what came out.
  **[graded-cases.md](graded-cases.md) is the rest of it**, read before the first
  run.

**They are not equals.** A graded case is slow, costs money per run and is
scored by a model, so a green gate over a suite of them usually means *the cases
exist and can fail*, not *they passed* — and it proves only that judgment held on
one prompt. Where there is code to call, call it; a repository with both does
not test the same behaviour twice. The second answer exists because the first
is impossible somewhere, not as an alternative to it.

**Do not invent a third.** Use the tooling that already builds that kind of
suite; a format invented in a setup sitting has one user and nobody to ask.
Where that tooling cannot run where the suite has to, the fallback is another
platform that already runs such suites — and the cases stay in the format the
gates read, so the tool that could not run remains a runner to gain, not a
migration owed.

## The two kinds

```
tests/behaviour/    answers to a Gherkin rule. Everything user-visible.
tests/workflows/    one walkthrough per workflow, end to end.
tests/unit/         internals. The one exemption from rule references.
tests/support/      helpers. Not tests; not run.
```

The discovery pattern is the repository's — `specs/setup/README.md`.

## Behaviour tests

Every behaviour test declares the rule it exists for, through the repository's
`rule()` helper (where it lives and its imports are bindings):

```js
rule('add-goes-to-top', () => {
  test('a new one appears above the older ones', () => {
    // ...
    assert.deepEqual(app.contents(), ['the new one', 'the older one']);
  });
});
```

- `rule()` throws at once if the id does not exist or is still `@planned`, and
  lists the ids that do. It wraps the runner's grouping call, so the id and the
  rule's text appear in the output:

  ```
  ▶ [add-goes-to-top] A new one goes to the top
    ✔ a new one appears above the older ones
  ```

  `ruleText(id)` from the same helper returns the parsed rule.
- **Every `test()` in a behaviour file sits inside a `rule()` block**; one at the
  top level is untraced, and the gate rejects it. A rule may have several tests
  and a file several rules, but a file stays about one component, like the
  feature file it mirrors.
- **A test that did not run claims nothing.** A skip, an only, an expected
  failure leaves its rule untested; the gate empties the claim and names the
  marker. The runner reports what it ran, per test, in a form the gate can count:
  fewer run than the tree holds fails, whatever the summary says. Every
  fabricated result on record was a summary. The markers and the report's form
  are bindings.
- **A test given no world tests nothing.** A test presupposing state it was not
  given — a row, a file, a branch, a service — measures whether the assumption
  held, in both directions. Say what world a test runs in, and make its absence a
  failure.

### Write them against the rule, not the implementation

The `Example:` blocks say what to assert. If the rule says one line reads above
another, assert the rendered order, not that a sort function was called. A
behaviour test that passes while the screen is wrong is worse than none: it
costs the gate its meaning.

## Unit tests

For internals no Gherkin rule describes — a parser, a serialiser, an id
generator, the gate tooling itself. No `rule()` call, no reference.

**This exemption is what makes the rest honest.** Without a place for internals
tests, coverage pressure turns behaviour tests into filler that names a rule and
asserts nothing. If you can name the rule a test answers to, it is a behaviour
test; if you cannot, it is a unit test. The gate warns when a unit test claims a
rule — usually a file in the wrong folder.

## The world the tests run in

The world — a real browser, a headless DOM, no DOM — is a binding, and so is
everything the app talks to: the store, the clock, the network and each service
on it, whoever it signs people in with. Each is a boundary, with a row in the
bindings saying how a test reaches it ([gates.md](gates.md#the-boundaries)).

- **A test proves a rule in the world its row names, or nowhere.** A double
  standing in for a boundary whose row reads *real* tests the double, and the
  gate fails it.
- **A fake is honest only while something checks it against the real thing**:
  one suite runs against both, and the row says when the real half was last
  green. A fake nothing checks is *mocked*, on the same clock as a deferral.
- **What no test can reach is said, never simulated**: its row reads
  *unreachable*, and every change touching it says so where it is decided.
- **Build the world fresh per test.** Shared state is the commonest cause of a
  suite that passes in order and fails one file at a time.
- **Test without the environment whatever can be.** A test that needs a DOM to
  check a decision is testing two things and reporting one.

## Coverage

The thresholds are the repository's. The judgment is not:

- **It is worth a gate** where an agent wrote both the code and its tests:
  coverage is the only mechanical evidence the tests reach the code. Reach is all
  it proves, so it is taken beside traceability, not instead of it; together they
  are hard to satisfy dishonestly.
- **What is not covered is named**, in the runner's own exclusions, or it is a
  gap. A demand below the whole of what is in scope is an exemption nobody named.
- **Branches first.** Untested paths hide there, and line counting is generous
  about declarations.
- **Error paths in storage reads are behaviour**, not chores: corrupt the stored
  value and assert the app still opens on something usable.
- **Code no rule-bound test reaches is a question the change answers**: a
  behaviour nobody specced — write its rule — or dead — delete it. A unit test
  reaching it keeps it covered without answering, and a test pretending to reach
  an unreachable branch is worse than deleting the branch.

### Measure the rule-bound tests on their own, and never gate it

Take coverage twice: over the whole suite — the gated number — and over the
**behaviour and workflow tests alone**, which says how much of the product the
*specification* reaches. High gated and low spec-bound means the specs describe
a corner of the product. The second number goes in the report and **never in a
threshold**: gated, it would push people to write rules to move a number. It is
also what makes the unit-test exemption visible: unit tests raise the first and
not the second.

## A test that fails sometimes is worse than no test

A test that fails two runs in five teaches everyone to press re-run, and then a
real failure looks like noise. **No test may depend on chance, timing or
ordering**:

- an assertion resting on a probability — that generated values will not
  collide, that a sample falls in a range;
- a timeout, or one operation assumed to finish before another;
- state left by an earlier test.

The fix is almost never a looser threshold or a retry: either the code offers a
guarantee that makes the probability irrelevant, or the test asks a different
question. A test that passes locally and fails on CI, or passes on a re-run with
nothing changed, is a defect in the test, at the priority of a defect in the
code.

## Before committing

Run the repository's verification — the same command CI runs, named in
`specs/setup/README.md`. What each failure means is in [gates.md](gates.md).

## And again before it leaves this machine

The run that has to happen is **the one before the push**, not one per commit: a
branch that runs verification ten times to learn one thing teaches everybody the
rule is too expensive to keep. A repository may make it automatic — a `pre-push`
hook is the usual shape — running the one command the bindings name.

- **Offered, never installed unannounced.** It is proposed, in words, and
  somebody says yes or no.
- **Cost decides what goes in, and is stated as the reason.** Only checks that
  are free, fast and fixable here. **Anything that costs money per run stays
  out**: a [graded suite](graded-cases.md#neither-freshness-nor-the-score-is-gated)
  refuses to start without a per-run approval from the person paying, and a hook
  that can reach one bills them per push.
- **It takes nothing away.** Every check that blocked a merge still blocks it;
  the hook adds a fast local signal, which
  [gates.md](gates.md#and-what-is-not-wiring-at-all) says is not a gate.
