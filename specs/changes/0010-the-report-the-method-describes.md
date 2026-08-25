# Spec 0010: the report the method already describes

- **Status:** approved
- **Issue:** [#30](https://github.com/sargismarkosyan/livespec/issues/30) and
  [#31](https://github.com/sargismarkosyan/livespec/issues/31), taken together at
  the human's direction.

## Who this is for

[`@persona:agent-accelerated-owner`](../personas/agent-accelerated-owner.md), in
[`adopt-the-process`](../workflows/adopt-the-process.feature) — and the workflow
names this failure in *Where it breaks* as flatly as it names the others:

> A pull request with nothing in it to look at.

**Half of this change serves no workflow, and that is correct rather than a
gap.** Wiring livespec's own CI to post a comment is this repository's
infrastructure, the same kind of thing as `verify.py` and `release.py`, and
[`process.md`](../../method/process.md#a-technical-change-that-serves-no-workflow-is-correct-not-a-gap)
documents the case. It carries no rule for the same reason none of them do. The
half that *does* serve the workflow is `setup` wiring a report in somebody
else's repository, and that is where the three rules are.

The always-promise most at risk is **`always-green`**
([spec.md](../spec.md#the-promises-that-belong-to-no-single-workflow)) — *nothing
in this repository can fail a user's build.* A report is the one artefact in the
method that is defined by not being able to fail one, and the first version of it
that can is a promise broken rather than a feature added.

## The job behind the request

Know what a change did to the spec layer at the moment of deciding whether to
merge it — without running anything, and without reading the diff to work it out.

## Why now

**Because it was watched happening.** The human compared a livespec pull request
against one from the reference repository and the difference was a comment that
was not there. The change being looked at was
[`0008`](0008-the-gate-gets-something-to-hold.md), which took the spec layer from
`0 live rule(s)` to `6` — the entire point of that version — and **nothing on the
pull request said so.** The number existed, in a CI log, in a step nobody opens.

**Because the method has described this since before the spec layer existed.**
[`gates.md`](../../method/gates.md) has a section titled *"The report is not a
gate"*, and it is the only artefact on that page that nothing produces and no
skill wires. `grep -rln "report.mjs\|pull-request report\|PR comment" skills/
method/ templates/` returns nothing.

**Because the absence is recorded nowhere.** The gate wiring ledger carries one
row per gate, and reasons — correctly — that the report gets none because it is
not a gate. The effect is that a repository can be fully reconciled against
`gates.md` and still be missing the one thing on that page it never had.

**And because this is the third version in a row spent on the same defect.**
[`0008`](0008-the-gate-gets-something-to-hold.md) built the pull-request rule the
method described and nothing enforced.
[`0009`](0009-whose-repository-whose-tracker.md) built the repository rule the
method assumed and nothing stated. This is the third: an artefact described in
`gates.md` that nothing produces. The pattern is worth naming out loud —
**this repository has been shipping a method ahead of its own implementation of
it**, and the reference repository is where the implementation actually lives.

## The end value

Opening a pull request tells you what it did to the spec layer. Not the totals —
what *moved*. And a repository that adopts the process gets that from the first
sitting rather than after somebody hand-builds it, which is the only way it was
ever obtained.

**How we would know it worked:** the sharper half is the negative one. A change
whose description claims it moves the spec layer, and which moves nothing, shows
a delta of zero on its own pull request. Nobody can perform that check today
without doing by hand exactly what the report would do.

## What changes

1. **`trace.py` grows a structured mode.** It already computes every number the
   report needs — live rules, planned rules, the workflow map, personas,
   journeys, the case suite — and exposes none of it. This is the whole design
   constraint: `gates.md` says the report *"recomputes nothing… a report that
   re-derives it is a second copy of the gate's logic waiting to drift out of
   sync."* So the report reads the gate's own output, and the gate is the only
   thing that parses `specs/`.

2. **A report script**, consuming that output for the branch and for the base.
   The delta is the half worth having and it needs both, so CI checks out the
   base ref and runs the gate there too — no stored state, nothing to go stale,
   and it survives a rebase.

3. **CI posts it as one comment per pull request**, rewritten in place rather
   than appended, so pushing does not bury the thread in near-identical reports.
   It runs **after** both gates have passed, so it only ever describes a green
   run, and it cannot fail the job.

4. **The bindings gain a report row.** That is where "is it wired here" gets
   answered, and it keeps the gate ledger a ledger of gates — the reasoning
   `gates.md` gives for excluding it stands, and this is the place that was
   missing rather than a hole in that argument.

5. **What it says here is spec health and the suite, not coverage.** There is no
   coverage gate and the ledger records why. The eval suite is this repository's
   substitute and the bindings already say so, so the second table is cases,
   skills held, and how many claim a rule — the numbers that would move if the
   suite were quietly weakened.

6. **`gates.md` says the report must be wired, not only what it would contain.**
   Today it describes an artefact in the third person. It gains the same standing
   the gates have: something a repository is expected to end up with.

7. **`setup` wires it**, in the repository's own language, alongside the gates —
   and says so in the hand-back when it cannot, rather than leaving the gap
   silent. This is the half that ships.

**Rules added or changed** — the `@rule:` ids in `specs/features/`:

| Rule id | Feature file | New or changed |
|---|---|---|
| `setup-wires-the-pull-request-report` | `features/report/wiring.feature` | new |
| `the-report-cannot-fail-the-build` | `features/report/wiring.feature` | new |
| `the-report-says-what-moved` | `features/report/wiring.feature` | new |

All three are about what `setup` leaves behind in somebody else's repository,
which is why they are rules at all. **Livespec's own CI wiring gets none**, for
the reason *Who this is for* gives.

**Ledger:** no new row, deliberately. See item 4.

**One addition beyond this spec, made during implementation and recorded rather
than absorbed.** *Risks* names `always-green` as the promise this could break
quietly, and nothing was holding it: `report.py` exiting non-zero would turn a
build red however carefully the workflow was written. `inject.py` gains a
**control** — not a fault, because there is nothing to break when the promise is
that nothing breaks — asserting the report exits zero on every degenerate input.
It was confirmed the way this repository confirms anything: by making `report.py`
able to fail and watching the control report it.

## What we are not doing

- **Not writing rules for this repository's own report.** `0003` tried the
  equivalent for the release pipeline and reserved five ids that are still owed,
  because a feature serving no workflow fails the gate and
  [#20](https://github.com/sargismarkosyan/livespec/issues/20) is the change that
  would let them land. Reserving a fourth batch behind the same blocker would
  make the debt look like progress. **`verify.py`, `checks.py` and `release.py`
  carry no rules either**, and that has been the honest answer every time.
- **Not fixing [#20](https://github.com/sargismarkosyan/livespec/issues/20).** It
  is now on the critical path for the second time and it is a `gates.md` change
  of its own — the traceability gate needs an answer for a feature that correctly
  belongs to no workflow, and inventing one inside a spec about reports is how a
  method decision gets made by accident.
- **Not adding a coverage section.** Still *not applicable* here, and a table of
  empty rows would teach every adopter that the report is mostly blanks.
- **Not letting the report fail anything, ever, including on its own errors.** A
  report step that goes red because it could not build a report is a gate nobody
  declared. If it cannot run, it says nothing and the build is unaffected.
- **Not generating the Gherkin block that [#21](https://github.com/sargismarkosyan/livespec/issues/21)
  suggested the tooling could emit.** Closer than it was, since the structured
  output now exists — but it is a separate promise and belongs to whoever picks
  up that thread.

## Data

None. There is no storage contract — the plugin ships prose, and what a version
leaves behind is listed in [spec.md](../spec.md#what-a-version-leaves-behind).
Item 2 deliberately stores nothing: a report comparing against a number nobody
can see is worse than one that recomputes.

## Risks

- **Two issues in one version again, and this time the dependency runs the wrong
  way.** #31 ships to users; #30 does not. Building the reference and the
  instruction to adopters in the same commit means no version exists in which
  anybody used the reference before it was recommended. That is the risk the
  alternative — #30 first — was there to avoid, and it was declined
  deliberately. What limits it: the reference is 30 lines of CI, and the
  reference repository has been running the equivalent for months.
- **`always-green` is the promise this could break quietly.** A report that
  cannot fail is a claim about a CI step's exit code, and CI steps fail for
  reasons nobody wrote — a missing token, a rate limit, a base ref that will not
  check out. Every one of those has to leave the build green, which means the
  step swallows its own errors. **A step that swallows errors is also a step that
  can silently stop working**, and the honest form of that trade is that the
  report going missing is a thing nobody will be told about either.
- **The delta doubles the gate run.** Cheap today — the gate takes six seconds —
  and it is a cost that grows with the spec layer rather than staying flat.
- **A report nobody reads is wallpaper.** The reference repository's version is
  two tables and a footer, and the discipline that keeps it readable is that it
  says what moved rather than everything that exists. The first time a section is
  added because a number was available rather than because somebody wanted it,
  this starts becoming the thing it replaced.
- **`setup` gets longer, and adoption is the attempt that must not.** The
  workflows README requires a change that lengthens adoption to name which later
  attempt it shortens. This one shortens *taking a version through review* —
  every review, forever, in the repository that adopted it. That is the trade, and
  it is the right way round.

## Acceptance checks

1. `python3 .github/scripts/verify.py` green, and `trace.py`'s structured output
   parses — the same numbers as the human-readable run, from one code path.
2. Open a pull request that adds a live rule. The comment appears, shows `+1`,
   and appears **once** after a second push rather than twice.
3. Break the report deliberately — a bad base ref. The comment is absent, both
   required checks still pass, and the pull request is mergeable.
4. Open a pull request that changes only prose. The report shows a delta of
   zero rather than being absent, because "nothing moved" is the answer the
   negative check in *The end value* depends on.
5. Read the comment on a pull request against the reference repository's, and
   check the missing coverage table reads as a decision rather than as an
   omission.
6. Run a setup sitting in a repository whose pull requests cannot carry a
   comment. The hand-back says the report is not wired and why.
