# Spec 0015: the sitting uses the pipeline it wired

- **Status:** proposed
- **Issue:** [#27](https://github.com/sargismarkosyan/livespec/issues/27)

## Who this is for

[`@persona:agent-accelerated-owner`](../personas/agent-accelerated-owner.md), in
[`adopt-the-process`](../workflows/adopt-the-process.feature) — at its end, where
the sitting hands back.

**The persona already records this failure by name.** One of the four misses in
*What they do* is *"a claim written into a bindings file that nobody had ever
run."* The workflow lists the same thing under *Where it breaks*: **"Bindings
asserting a behaviour nobody has run."** Both were written before this issue was
filed, from separate evidence, and neither has anything holding it.

**This does not lengthen the attempt, and that distinction is the whole
argument.** [workflows/README.md](../workflows/README.md) sets the trade rule —
*a change that lengthens adoption has to name which later attempt it shortens in
exchange, or it is buying nothing* — and adoption is the one workflow performed
once per repository, so the rule is right to be strict.

What this change lengthens is the **sitting**. The **attempt** already ends past
it: *"Ends when the next change opened in that repository proves it: the pull
request carries what the version leaves behind, and the pipeline refuses the
change until the specs move with it."* The sitting stops one step short of an end
state the workflow has claimed since [`0008`](0008-the-gate-gets-something-to-hold.md).
This closes that distance rather than extending anything — the attempt ends where
it always said it did, and now something reaches it.

## The job behind the request

To have the things the hand-back says about this repository be things somebody
watched happen.

Not to feel finished sooner, and not to have a record of having installed it.
The sitting currently ends with a set of assertions about machinery — branch
protection, the required check, the report — that were configured and never once
exercised, and the person reading them cannot tell those apart from ones that
were.

## Why now

**Because a live rule is already claiming what the sitting cannot check.**
[`@rule:setup-wires-the-pull-request-report`](../features/report/wiring.feature)
promises *"its pull requests carry a report of what the change did to the spec
layer"*. The sitting never opens a pull request, so nothing in it can reach that
Example — and
[`12-setup-drives-the-sitting`](../../evals/12-setup-drives-the-sitting/prompt.md)
claims that rule anyway. The gate is satisfied; the claim is not checked.

**Because the report is structurally silent about its own absence.**
[`gates.md`](../../method/gates.md#the-report-is-not-a-gate) requires that it
*cannot fail the build*, and says outright that its absence is *"a gap like any
other — one that is easy to miss precisely because nothing fails when it is
missing."* A pull request is the only thing that shows it missing.

**Because the map already records the same gap and left it open.**
[workflows/README.md](../workflows/README.md): *"What walks it is the sitting,
not the whole attempt… The tag says walked; one leg is."*

Three files, written on separate occasions, describing one hole. Nothing has been
holding it.

## The end value

Ren comes out of a sitting knowing the pipeline held something, instead of being
told it would. Where it could not be shown, the repository says that plainly, so
a claim they did not watch is never sitting in the bindings looking like one they
did.

**How we would know it worked:** the hand-back names a pull request and what the
required check did with it — or names exactly what it could not observe and why.
Today it names neither, and the bindings read identically in both cases.

## What changes

- The sitting's last act is to **commit the change specs the interviews wrote and
  open one pull request** in that repository, then report what happened to it:
  whether the required check ran, what it said, and whether the report appeared.
- Where no pull request can be opened — no remote, no CI, no permission — the
  hand-back says the pipeline wiring is **unobserved, and why**, rather than
  asserting it.
- The **gate wiring ledger** gains that same honest reading for a row that is
  wired and has never fired. *Automated* stops meaning *configured*.
- [`specs/journeys/trusting-the-spec-again.md`](../journeys/trusting-the-spec-again.md)
  — the ownership row *"Knowing the install took → **nothing yet**"* and its
  matching bullet stop overclaiming absence, since §4's fault injection and §8's
  three change specs are not nothing.
- [`specs/workflows/README.md`](../workflows/README.md) — the *"one leg is"*
  paragraph is rewritten to say what is true after this change.

**Rules added or changed** — the `@rule:` ids in `specs/features/`:

| Rule id | Feature file | New or changed |
|---|---|---|
| `the-sitting-ends-by-using-the-pipeline` | `features/setup/demonstration.feature` | new |
| `wiring-nobody-ran-is-not-claimed` | `features/setup/demonstration.feature` | new |

## What we are not doing

- **Not inventing a demonstration change.** #27 sketched *"make one small real
  change through the process"*; that step writes work nobody wanted in order to
  prove something. The pull request here carries the specs the interviews
  **already** wrote, and nothing else.
- **Not a first-change marker.** A file asserting *exercised* is the same
  assertion this change exists to remove, plus state that can lie. `trace.py`
  treats an empty layer as unarmed by design, and per
  [`0014`](0014-the-reader-the-method-assumes.md) the persona does not read files
  like that.
- **Not merging it.** Opening the pull request is the demonstration. Merging is
  the human's, and a skill that merges has taken a decision that was never its
  own.
- **Not re-cutting `adopt-the-process` shorter.** [workflows/README.md](../workflows/README.md)
  reads the same gap as *"the strongest evidence this workflow was cut too
  long"*, which points at the opposite fix: end the attempt at the hand-back and
  make the first change its own workflow. That is `refine-workflows`' change, not
  this one. Doing this first means that re-cut, if it comes, is argued against
  something observed rather than against a gap.
- **Not a new gate.** Nothing is added to `verify.py`. This is a skill telling
  the truth about wiring, not a check on whether the wiring exists.

## Data

No storage contract applies — [spec.md](../spec.md#what-a-version-leaves-behind)
names the deliverable of a version as the pull request description, and this
repository has no app and no database.

What gains a shape is the **gate wiring ledger** in a consuming repository's
`specs/setup/README.md`. Ledgers already written are not retroactively wrong: a
row reading *automated* that was never watched run keeps its meaning under the
old vocabulary, and `setup`'s existing rule — *installing over a repository that
already has a ledger: diff it, never overwrite it* — is already the path by which
such a row gets reconciled rather than silently rewritten.

## Risks

**`never-implements` is the promise at risk** ([spec.md](../spec.md#the-promises-that-belong-to-no-single-workflow)).
A skill that commits and opens a pull request is acting in the world rather than
writing files into a working copy, and that is a real widening. The line this
change holds: it commits **files it wrote itself, in the layer it owns**, opens
**one** pull request, and touches no application code and no branch protection it
did not already wire. If that line moves later — a skill that pushes fixes, a
skill that merges — it is a change to what livespec is and has to be argued as
one, not inherited from here.

**`always-green` deserves a line too.** The demonstration must not leave somebody
looking at a red repository wondering whether the install broke it. A required
check that *refuses* the pull request is the wiring working, and the hand-back
has to say which of the two happened in as many words.

**The eval sandbox cannot reach the observation, and this is the hard part.** No
case workspace has a live remote or CI, so
`the-sitting-ends-by-using-the-pipeline` cannot be graded end to end there. The
implementing change has to choose, out loud: grade the **account** the hand-back
gives — which is transcript-visible and therefore reachable — or leave the rule
`@planned` until something can walk it. `wiring-nobody-ran-is-not-claimed` has
the opposite problem and it is a lucky one: the sandbox has no remote, so the
sitting will take that branch naturally and the case can hold it today. Naming
this here so it is not discovered at `verify.py` with the tag already dropped.

**A case moving re-stales the board.** Amending
`12-setup-drives-the-sitting` or adding a case makes its `evals/board.json` rows
stale, and re-measuring costs real money. Per
[CLAUDE.md](../../CLAUDE.md), the suite never runs unasked — the implementing
change says which cases are stale and what it will cost, and waits.

## Acceptance checks

1. Read `skills/setup/SKILL.md` §8. Its closing step names committing the
   interviews' change specs, opening one pull request, and reporting what the
   required check and the report did with it.
2. Take a repository that has a remote and CI through the sitting. The hand-back
   names the pull request and what the check said about it.
3. Take one with no remote through the sitting. The hand-back says the pipeline
   wiring is unobserved and why, and nothing in the bindings asserts otherwise.
4. Read that repository's gate wiring ledger. A gate that is wired and has never
   fired does not read *automated*.
5. Read `specs/journeys/trusting-the-spec-again.md`. The *"Knowing the install
   took"* row no longer reads *nothing yet* where §4's injection and §8's specs
   already answer part of it.
