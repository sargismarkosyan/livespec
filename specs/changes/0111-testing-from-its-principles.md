# Spec 0111: testing from its principles

- **Status:** approved — by the maintainer in advance, 2026-11-22 (*"Carry on."*), as the next change under #195; implemented end to end, reviewed at the pull request
- **Issue:** [#195](https://github.com/sargismarkosyan/livespec/issues/195), the third change under it, after [0109](0109-the-process-from-its-principles.md) and [0110](0110-the-repository-from-its-principles.md)
- **Sketch:** skipped — approval was given in advance, so there was no decision left for one to support.

## Who this is for

**Ren — [`agent-accelerated-owner`](../personas/agent-accelerated-owner.md)**, whose
agent writes every test. **The workflow is [`adopt-the-process`](../workflows/adopt-the-process.feature)**,
at *The changes after*. Nothing about who this is for moves.

## The job behind the request

The same as [0109](0109-the-process-from-its-principles.md), for
`method/testing.md`: each rule once, under the principle it follows from.

## Why now

`testing.md` is 264 lines and every implementing session reads it.

## The end value

The same rules in fewer words. **How we would know it worked:** the harvest
below accounts for every section, the five linked anchors resolve, and the page
is shorter.

## What changes

1. **[`method/testing.md`](../../method/testing.md)** is rewritten from the
   principles, 264 → 190 lines. The five linked headings keep their anchors:
   - *First: what proves a rule is true here*
   - *Behaviour tests*
   - *Measure the rule-bound tests on their own, and never gate it*
   - *A test that fails sometimes is worse than no test*
   - *And again before it leaves this machine*
2. **The `method/` ceiling** is lowered to the size this change leaves.

No rule, workflow or skill moves. No Gherkin moves.

### The harvest

| Section | Kept, every one |
|---|---|
| *First* | ask and record the answer; two honest answers; graded cases are weaker and cost money, call code where there is code, never two ways for one behaviour; do not invent a third, and the fallback |
| *The two kinds* | the four folders; discovery pattern is a binding |
| *Behaviour tests* | `rule()` declares the rule, throws on unknown or `@planned`, lists ids, shows in output; `ruleText`; every test inside a `rule()`; one component per file; a test that did not run claims nothing, counted per test; a test given no world tests nothing; assert the rule, not the implementation |
| *Unit tests* | what goes there; why the exemption matters; the name-the-rule test; the gate warns on a claim |
| *The world* | world and boundaries are bindings; proved in the row's world or nowhere; a fake checked against the real or *mocked*; *unreachable* said, never simulated; fresh world per test; test without the environment what can be |
| *Coverage* | why a gate; name what is not covered; branches first; storage error paths; unreached code is a missing rule or dead |
| *Measure the rule-bound tests* | taken twice; reported, never a threshold; shows the unit-test exemption |
| *Flaky* | never chance, timing or ordering; the three sources; no looser threshold or retry; a flaky test is a defect |
| *Before committing*, *before the push* | verification as CI runs it; before the push rather than per commit; offered, never installed unannounced; cost decides; paid suites stay out; takes nothing away |

## What this removes

- **"V8's line counting"** becomes *line counting*: V8 is one runtime, and a
  runtime is a binding.
- **The incidents and asides behind rules that stand without them:** *the suite
  that holds this method learned it twice*, *a leaked key is a nasty failure to
  diagnose*, *not because doubles are wrong*, *the first thing they will do is
  find out how to turn it off*.
- **74 lines of `method/testing.md`.**

## What we are not doing

The other method files: one change each, under #195. No rule changes.

## Data

None.

## Risks

A rule loses force without its reason. The reasons cut are listed above.

## Acceptance checks

1. Every row of the harvest can be found in the new page.
2. The five linked anchors resolve; `verify.py` is green.
3. The `method/` ceiling is lowered to match.
