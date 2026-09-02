# Spec 0036: a row that was right once

- **Status:** proposed
- **Issue:** [#89](https://github.com/sargismarkosyan/livespec/issues/89)
- **Depends on:** nothing to build. It stands beside
  [`0032`](0032-the-repository-does-not-know-it-is-owed.md), which caught the
  other half of the same problem, and it is what
  [`0030`](0030-covered-or-named.md) and [`0035`](0035-what-the-whole-of-it-comes-to.md)
  need in order to reach a repository that was set up before either of them.

## Who this is for

[`agent-accelerated-owner`](../personas/agent-accelerated-owner.md), in
[`adopt-the-process`](../workflows/adopt-the-process.feature) — at the seam
[`0032`](0032-the-repository-does-not-know-it-is-owed.md) named: **between having
adopted the process and the process moving on underneath them.** That is what
`doctor` exists for, and this is the second thing found sitting in it.

Three persona lines decide the shape:

- **"more than one repository at once."** Every repository was set up on the
  version that existed that week, and the ledger in each one records which. There
  is no version of this problem that happens once.
- **"A setup they did not agree to gets stopped and questioned rather than
  inherited."** A threshold read off a coverage report is exactly that, and it is
  the case the persona line was written for — except that it arrives wearing a
  decision's clothes, in a row that says *automated*, in a repository where the
  build is green.
- **"They read the spec layer and not the documentation."** So the finding has to
  land in the audit's own open list and in the ledger row, not in a release note
  nobody opens.

And the fourth line is the reason nothing has told them: **"a failing pipeline
gets fixed, it does not get bypassed."** Nothing is failing. A ratchet is the one
defect that guarantees its own green build.

**This does not lengthen adoption.** The [workflows
README](../workflows/README.md) requires a change that adds a step to the sitting
to name the later attempt it shortens; `doctor` runs after the sitting is over,
on a repository that already has the process, so no step is added to the attempt
that is paid once.

## The job behind the request

To find out that a number a gate enforces was measured rather than decided — in a
repository set up before the method had an opinion about it, and without reading
a changelog to discover that the method has one now.

## Why now

Because [`0030`](0030-covered-or-named.md) shipped in **0.28.0** and
[`0035`](0035-what-the-whole-of-it-comes-to.md) in **0.30.0**, and the one
repository this process is installed in is stamped *reconciled against livespec
**0.25.0***. It was set up on **2026-08-30**, correctly, by following the
instruction as it then read. `setup` runs once, so neither change will ever
reach it.

Measured in `toil-tracker` at `32fcd64`:

| | demanded | scored | slack |
|---|---|---|---|
| statements | 91.35 | 91.35 | 0 |
| branches | **82.37** | 82.37 | 0 |
| functions | 99.39 | 99.39 | 0 |
| lines | 98.33 | 98.33 | 0 |

Nine ratchet steps, each a number read off a report, kept as a ladder of comments
above the config. **281 of 1594 branches are uncovered and named nowhere** — no
exclusion, no reason, no address. That is `0030`'s own harm statement arriving
through a repository that followed the old instruction correctly: *nobody can
then tell code that was never covered from code that stopped being.*

**The slack is zero, and that is the trap.** `0030` measured this failure as a
gap between the threshold and the score, and here there is none, because the
ratchet is tight. A ledger read for slack passes this repository. The demand is
still not the whole of what is in scope.

### Why the audit does not already catch it

Two mechanisms exist and neither fires.

`doctor` §1 asks three questions of every row — *what state does it claim*, *how
was that established*, *what does it not cover*. All three are about the row's
own text. The number is in `vitest.config.ts`. **The audit never opens the file
the gate reads.** §2 sends it outside the tree, to the platform, and the config
is inside it, so neither pass reaches the one artefact that holds the answer.

`0032`'s [`what-arrived-after-the-bindings-were-written-is-caught`](../features/showing/owed-in-this-repository.feature)
is the right shape and catches the wrong case. It reports **what the recorded
process never mentioned because it did not exist yet** — an absence. Here the
coverage row is present, accurate, and complete. Nothing is missing, so nothing
is caught. **A row that was right when it was written is the case neither rule
covers**, and it is the one that will keep recurring, because every change to the
method creates a fresh crop of them.

## The end value

Running the audit in a repository set up weeks ago tells them which of its gates
are enforcing a number nobody chose, and how much of the code that number leaves
at no address — without their having to know that the method moved.

**How we would know it worked:** an audit of `toil-tracker` produces an open item
that no previous audit could have produced — the branch demand named as a figure
that was measured rather than chosen, the 281 branches named as reachable by no
gate and named in no exclusion, and the coverage row corrected so it stops
reading as a decision somebody made. Today that audit reports the row as
*automated* and moves on.

## What changes

- **`doctor` §1 gains a fourth question per row: where did this number come
  from?** For any row whose gate enforces a number, the audit opens the config
  the gate reads and reports the demand it finds there — not the row's
  description of it. A demand equal to what the code scores is reported as
  measured rather than chosen, with the part of the repository it leaves
  unaddressed named.
- **The exception is stated with it.** A demand that is the whole of what is in
  scope and a score that reaches all of it are the same figure, and that is what
  [`0035`](0035-what-the-whole-of-it-comes-to.md) asks for. It is left alone.
  Without this line the change reports every correctly-wired repository as
  defective on the day it gets it right.
- **The same read catches the exclusions.** Where what the demand does not reach
  is listed in the bindings instead of in the tool's own config, that is
  `skills/setup/SKILL.md`'s *"a list only the bindings know about is a second copy
  of the gate"*, and it is visible from the same file being open. Folded in
  because it is the same act, not because it is the same finding.
- **`doctor` §1 reframes the stamp.** The version the ledger was reconciled
  against currently appears in the skill once, as something to re-write at the
  end. It becomes what the reading starts from: the checklist is
  [`gates.md`](../../method/gates.md) as it now stands, and a row that conforms to
  the stamped version is not thereby passed.
- **The audit still moves nothing.** The correction is to the row that called the
  number a decision. The number itself is wiring, and wiring is `setup`'s.

**Rules added or changed** — the `@rule:` ids in `specs/features/`:

| Rule id | Feature file | New or changed |
|---|---|---|
| `a-number-is-read-where-the-gate-reads-it` | `features/wiring/what-an-audit-reads.feature` | new, `@planned` |
| `the-checklist-is-the-method-as-it-now-stands` | `features/wiring/what-an-audit-reads.feature` | new, `@planned` |

A new file rather than rules added to
[`wiring/ledger-claims.feature`](../features/wiring/ledger-claims.feature): that
one is about **what a ledger is allowed to claim**, this is about **what an audit
reads and against which version**, and two more rules would put it at 5 of its 6
and 110 of its 120 lines.

**No description changes, so no should-not-fire case is owed.** `doctor`'s
description already carries *"to say whether the process still holds here"* and
*"when a bindings claim looks like nobody verified it"* — a threshold nobody
chose is both. The `context-budget` promise is untouched at 4315 of 5000.

## What we are not doing

- **Not moving any threshold, and not touching a coverage config.** `doctor`
  *"corrects the record, never the wiring"*, and the `never-implements` promise
  in [spec.md](../spec.md) is the one this change is closest to. The report ends
  by naming `setup`, which is what already does the building. Merging the two —
  an audit that fixes what it finds — was considered and dropped: a skill that
  both grades and repairs has no way to be wrong out loud, which is the argument
  `doctor`'s own opening makes.
- **Not building a machine-readable changelog of the method.** The stamp says
  which version the ledger was reconciled against and `gates.md` says what the
  method asks now; an agent reading both is the mechanism, and a generated diff
  between method versions is a second copy of the method waiting to disagree with
  it.
- **Not making anybody run the audit.** This makes `doctor` able to find the
  ratchet; it reaches a repository the next time somebody audits it, and nothing
  here causes that to happen. Named rather than hidden: `toil-tracker` keeps its
  82.37% until an audit is run there. A trigger that fires without being asked is
  a different mechanism and a different change, and no skill here has one.
- **Not re-running `setup` over an existing install.** `skills/setup/SKILL.md`
  refuses *"installing over an existing setup without saying what it will
  overwrite"*, and that refusal is correct. The route is a report that names what
  moved, which is this.
- **Not auditing every number in the repository.** Bounded to numbers a gate
  enforces. A constant in application code is not a claim the ledger makes, and
  widening this to *any* number turns an audit into a review.
- **Not retiring `0032`'s rule.** The two are complements — absence and
  obsolescence — and collapsing them into one would produce a rule whose examples
  have nothing in common but the skill they live in.

## Data

No storage contract here, and none in a consuming repository is touched. What a
version leaves behind is listed in [spec.md](../spec.md); this writes to exactly
one of the things named there in a consuming repository — the **gate wiring
ledger** in its `specs/setup/README.md`, a corrected row and, where the audit
moved no wiring, an unchanged stamp. `vitest.config.ts` and its equivalents are
read and never written.

## Risks

- **`never-implements` is the promise most at risk**, and it is at risk in the
  most tempting possible way: the audit will be holding the exact file, the exact
  line, and the correct replacement number. The fence is an example in the rule
  rather than a sentence in the skill, because a sentence is what a session in a
  hurry reads past.
- **A false positive on a repository that got it right.** A demand of 100 over a
  wholly covered scope matches the score by construction and is precisely what
  `0035` recommends. Reporting it as a ratchet would tell every correctly-wired
  repository it is broken, and would make the finding worth ignoring by the
  second one. Held by its own example.
- **The audit gets longer, and the audit is already long.** Opening one config
  per numeric row is bounded by the number of gates, which is small; but this is
  the second section-1 addition in five versions, and a fifth question will need
  to argue against the first four rather than beside them.
- **`always-green` is not at risk.** Nothing here runs in anybody's build.

## Acceptance checks

There is no app; this repository's deliverable is the pull request description.
What is checked by hand:

1. Run the audit against `toil-tracker`'s bindings at `32fcd64`. The open list
   names the branch demand as measured rather than chosen, and names the 281
   branches as reaching no exclusion and no gate.
2. Confirm the coverage config there is unmodified afterwards, and that the
   report's last line names `setup` for the number itself.
3. Run it against this repository's own bindings, whose coverage row reads
   *none — see below*. It reports nothing: there is no gate, so there is no
   number to have come from anywhere.
4. Both rules drop `@planned` in the implementing change, each claimed by a case
   tagged `rule:<id>`. Expected to be a new case rather than an extension of
   [`24-a-ledger-nobody-read-back`](../../evals/24-a-ledger-nobody-read-back/),
   whose scaffold is built for the read-back pass and holds no gate config to
   open.
