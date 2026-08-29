# Spec 0026: what else is wrong

- **Status:** proposed
- **Issue:** [#70](https://github.com/sargismarkosyan/livespec/issues/70)

## Who this is for

[`agent-accelerated-owner`](../personas/agent-accelerated-owner.md), in
[`adopt-the-process`](../workflows/adopt-the-process.feature) — at the end of it,
where the attempt finishes at a pull request in their own repository and the
pipeline answers.

The persona line this turns on is *"a failing pipeline gets fixed. It does not
get bypassed."* Somebody who fixes every red they are shown is exactly the person
harmed by a red that shows them one thing at a time: they will do the round trip,
correctly, as many times as they are asked to.

**It lengthens adoption, and the [workflows README](../workflows/README.md) says
that has to name what it shortens.** What `setup` wires gains a clause. What it
buys back is a round trip on every later change whose build is red for the
[sanctioned reason](0025-which-red-it-is.md) — paid once at the install, saved
for as long as the repository has a graded suite. That is the direction the trade
is supposed to run.

## The job behind the request

Learn everything a build has to say about a change in one run, rather than one
finding per attempt.

The shape of it has nothing to do with any particular gate. A run stops at its
first failing check, which is correct while every red can be cleared in the
minute after it is read: you fix it, you re-run, and everything below speaks
then. It stops being correct the moment a red can *stand* — and since
[`0013`](0013-the-board-of-latest-measurements.md) one can, for days, because
clearing it takes a spend nobody in the session can approve. "Stop at the first
failure" quietly became "hide every other verdict until the bill is settled".

## Why now

[`0025`](0025-which-red-it-is.md) fixed this shape for the report and left it in
place for the gate directly above it. On a sanctioned red the repository now
*reports* and does not *gate*: the release-input gate was skipped on **twelve of
the last twelve** failing runs, and nothing distinguishes *the label is fine*
from *the label was never looked at*.

**Nothing can merge through the gap, and the fix should not be sold as if it
could.** The job fails either way, `repository checks` is required, and a pull
request with no label is blocked by the very failure that hid the gate. What it
costs is the round trip: settle a ~$15 measurement bill, push, and only then
learn the `## Changelog` section was empty. [#69](https://github.com/sargismarkosyan/livespec/pull/69)
sat in exactly that state — its release inputs were dry-run locally and were
never once checked by the gate that exists to check them. That local dry-run is
the workaround, and a workaround for a gate is the clearest evidence available
that the gate is not speaking.

The same argument reaches the `plugin validate` job, where three independent
schema validations run in a row and the first failure hides the other two.

## The end value

A red build says everything it knows in one run. When the only thing standing is
a measurement waiting on a spend, settling it is the *last* thing left rather
than the first of two — because everything else already had its say on the run
that reported the stale board.

**How we would know it worked:** on the next pull request pushed with a stale
board, `Release inputs` reports a verdict rather than `skipped` — readable in
`gh run view <id> --json jobs`, which is how #70 was evidenced in the first
place. The failure mode that ends is *pay, push, discover the label was missing*.

## What changes

- A gate that does not depend on a failing one runs anyway, on the same run, and
  its verdict is in the run.
- It still gates. Running late changes **when it speaks and never whether it
  blocks** — no `continue-on-error`, no softening, and a change that fails it
  still cannot merge.
- A gate whose prerequisite never ran is left alone, so nothing reports a second
  failure that is only the first one restated.

**Rules added or changed** — the `@rule:` ids in [`specs/features/`](../features/):

| Rule id | Feature file | New or changed |
|---|---|---|
| `a-red-does-not-hide-the-gates-after-it` | [`features/verification/which-red.feature`](../features/verification/which-red.feature) | new |

### Two rules, not one, and the reason is the safety argument

[`what-explains-a-red-survives-it`](../features/verification/which-red.feature)
already says a thing may run on a red build. It is not this rule, and stretching
it to cover gates would break the argument that makes it safe. That rule's second
example is the whole licence: *a report that cannot rescue a build by running*.
A report may run late **because it cannot gate**. A gate that runs late is the
opposite claim, and it needs its own guarantee — that lateness moves nothing
about its authority — which is why the new rule carries that sentence as an
example rather than inheriting one.

Everything in [`gates.md`](../../method/gates.md) about the report staying
harmless stays exactly as it is. This adds a paragraph beside it, not a
qualification to it.

### And this repository does it to itself

Both jobs in [`checks.yml`](../../.github/workflows/checks.yml), because fixing
one and leaving the other is the criticism this issue makes of `0025`, repeated:

- `repository checks` — `Release inputs` gains the `!cancelled()` guard the three
  reporting steps below it already have, and **not** their `continue-on-error`.
- `plugin validate` — the three validations gain the same guard, conditioned on
  the install step having succeeded. That condition is the third example doing
  its job: without it, a failed `npm install` produces three more failures that
  all say *the CLI is not installed*.

The comment above the reporting steps currently reads *"Everything below is
reporting"*. After this it is false — there is a gate below a failing gate — and
it gets corrected in the same change rather than left to be believed.

### The ledger stamp moves

By [the bindings' own test](../setup/README.md#gate-wiring): re-stamp when the
wiring actually moved. `0025` set the precedent in as many words — *"a change to
when wiring runs, which is wiring"* — and this is that change again, for gates
rather than for the report. `0024` left the stamp alone and was right to; this
one may not.

### The case that holds it

[`27-a-red-nobody-here-can-clear`](../../evals/27-a-red-nobody-here-can-clear/prompt.md)
is extended rather than joined by a case 28. Its fixture already stages a
sanctioned red and a workflow file; what it does not have is a **second gate
below the failing one** — its `checks.yml` runs `./check` and then the report,
which is the report shape and not this one. It gains that step and a fourth
`rule:` tag.

**This stales its board entry**, and clearing that costs about **$2.31** for one
case at `runs: 3`. The flag is the maintainer's signature: the implementing
change can be committed and pushed with the entry stale, saying so, under
[`the-one-red-a-commit-may-carry`](../features/verification/which-red.feature) —
which is this same feature file being used for the change that extends it.

**The stale is already here, and part of it is not real.** Writing this spec
staled 27 before any fixture moved, because the rule it claims that sat *last* in
`which-red.feature` had its slice run to the end of the file — so appending a
rule after it changed its recorded text by exactly one newline and nothing else.
That is a defect in how a rule's text is bounded rather than a rule that moved,
it will fire again for anybody who appends a rule to a file some case claims from,
and it is **filed separately rather than fixed here** — a one-line change to a
gate does not belong inside a change about what a gate reports. It does mean the
$2.31 above is owed from this commit rather than from the implementing one.

## What we are not doing

- **Reordering the steps.** Putting `Release inputs` above `Verify` trades this
  for its mirror image and buys nothing.
- **Making `repository checks` pass while a measurement is stale.** Ruled out by
  [#65](https://github.com/sargismarkosyan/livespec/issues/65) and it stays out.
- **A second case.** Case 28 would cost its first measurement and then a share of
  every full suite run forever. Extending 27 costs one re-measure and nothing
  after that.
- **Touching the report's rules.** `the-report-cannot-fail-the-build` and
  `what-explains-a-red-survives-it` are unchanged in wording and in force.
- **Any general licence to continue past a failure.** The rule is about gates
  that do not depend on the failing one. Two gates reading the same thing, where
  the second only fails because the first did, are outside it — that is the
  cascade the third example refuses.
- **A ledger row for any of this.** No gate is added, removed, or made to cover
  anything new; three existing gates start being reachable on a run where they
  were skipped. The rows already read *automated*.

## Data

None. There is no storage contract here — [`spec.md`](../spec.md) says what a
version leaves behind, and this changes nothing in that list. `board.json` gains
no field; one entry goes stale and is re-measured in the ordinary way.

## Risks

- **`always-green` is the promise nearest this**, and the risk runs opposite to
  the report's. The report's danger was failing a build it must not fail; this
  step's danger is *not* failing one it must. `!cancelled()` alone leaves a
  step's failure fatal to the job — `continue-on-error` is what would break it,
  and it is deliberately absent here. Worth stating because the three steps
  below carry it, and copying the guard together with it is the plausible slip.
- **A run gets noisier on an ordinary red.** Two findings instead of one, on a
  build where one would have been enough. That is the price of the round trip
  and it is the right way round: the reader was going to fix both anyway.
- **The third example is the one that will be got wrong.** `!cancelled()` pasted
  onto a step whose prerequisite failed produces confident nonsense, and it is
  the version somebody reaches for when copying the guard down a file.

## Acceptance checks

There is no screen. What a person does by hand:

1. Open the implementing pull request with a deliberately missing release label
   while the board is stale. `gh run view <id> --json jobs` shows `Verify`
   failed **and** `Release inputs` failed — neither `skipped`.
2. Put the label back. The run reports `Release inputs` passing on a build still
   red for the stale board.
3. Confirm the change is still blocked from merging while the label is missing —
   the gate speaking late has not stopped it gating.
4. Read `checks.yml` top to bottom and confirm no comment still claims that
   everything below `Release inputs` is reporting.
