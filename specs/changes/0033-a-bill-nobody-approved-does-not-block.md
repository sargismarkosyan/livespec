# Spec 0033: a bill nobody approved does not block the merge

- **Status:** approved
- **Issue:** none — direct request, on the pull request carrying
  [`0031`](0031-a-missing-tool-is-not-a-missing-page.md) and
  [`0032`](0032-the-repository-does-not-know-it-is-owed.md).
- **Depends on:** [`0025`](0025-which-red-it-is.md), which split the two reds
  apart. This changes what the second one does to a merge and nothing about how
  it is told from the first.

## Who this is for

[`agent-accelerated-owner`](../personas/agent-accelerated-owner.md), in
[`adopt-the-process`](../workflows/adopt-the-process.feature) — at the last step
they hold, merging.

The persona line is the one this repository keeps proving: *investing in the
pipeline is what they do when they are short of time.* The line it collides with
is the other one, stated as flatly: **a failing pipeline gets fixed, it does not
get bypassed.** That is why this is a spec and not a workflow edit. The board
red is the one failure in this repository that *cannot* be fixed by whoever
meets it — its only cure is a purchase — and a rule saying "never bypass" plus a
gate nobody in the session can clear is a rule that will eventually be broken
rather than followed.

## The job behind the request

Ship work whose only outstanding item is a bill, without either paying it on the
spot or learning to walk past a red.

## Why now

Because it came up as a real choice with a real number, and the number won.

The pull request carrying 0031 and 0032 moves three skill bodies —
`refine-spec`, `setup` and `doctor` — and **seventeen cases lose their fresh
measurement**: twelve stale and five that have never had one. Costed from what
those cases last billed, and allowing for the nine measured at `runs: 1` against
a floor of 3, a `--changed` run is **about $58**. The suite's own documentation
says three runs in one sitting have exhausted the account limit outright.

The maintainer, holding that number, chose not to spend it — and the change
could not merge, because
[`the-one-red-a-commit-may-carry`](../features/verification/which-red.feature)
says in as many words that the exception has bought *"a commit and a push, never
a merge"*, and `repository checks` is a required check that exits 2 on a stale
board.

**So the standing rule makes a $58 purchase the price of merging any change that
touches a skill body.** That is not a gate finding a defect; it is a toll. And
the work it holds back is finished, green on every gate that can be run, and
already reviewed.

**The cost of leaving it is not that the board goes stale — it is what a person
learns.** A required check that can only be cleared by spending money teaches the
one habit this persona's file says they do not have, and it teaches it on every
change. The rule that survives contact is the one that can be followed.

## The end value

Work that is finished merges. What is unmeasured is still said, loudly, on the
change and in the checks list — it simply no longer stands between a finished
change and `main`.

**How we would know it worked:** the pull request carrying 0031 and 0032 merges
without a purchase, and the board still reports seventeen cases owed on the next
change that reads it. The failure mode to watch for is the opposite one: a month
of merges where nobody ever runs the suite and nobody notices, which the
*Risks* section says how to see.

## What changes

- **The freshness check moves to its own job.** `.github/workflows/checks.yml`
  gains **`measurement board`**, running `board.py` on its own.
- **`repository checks` runs `verify.py --local`** — every gate whose failure
  somebody in the session can clear. It stays a required check and stays a gate,
  and it now goes green on a tree whose only outstanding item is a bill.
- **`measurement board` is not a required check.** Read back from the platform
  on 2026-09-02: the required contexts are `repository checks` and
  `plugin validate`, and nothing else blocks. So the new job **fails visibly and
  blocks nothing** — no `continue-on-error`, because a job marked green with the
  finding buried in an annotation is a worse warning than a red one, and this
  repository's whole argument is that a silent absence is the expensive kind.
- **`verify.py` does not change.** Same five gates, same order, same exit codes,
  same `COSTS_MONEY`. A person still runs one command and still gets a 2. What
  moved is which CI job asks, not what the answer means.
- **`the-one-red-a-commit-may-carry` keeps its id and loses one example's
  conclusion.** The exception now buys the merge as well as the commit and the
  push, and what replaces the block is a red that is visible and not required.
- **A new rule says what replaced it**, so *does not block* cannot quietly
  become *is not reported*.

**Rules added or changed** — the `@rule:` ids in `specs/features/`:

| Rule id | Feature file | New or changed |
|---|---|---|
| `a-measurement-nobody-can-clear-does-not-block` | `features/verification/which-red.feature` | new, `@planned` |
| `the-one-red-a-commit-may-carry` | `features/verification/which-red.feature` | changed — its third example. Same id, same promise about commits and pushes; what it says about merging is what moves |

`a-red-says-which-red-it-is`, `what-explains-a-red-survives-it` and
`a-red-does-not-hide-the-gates-after-it` are untouched, and all three matter
more after this than before: the red that no longer blocks is the red most
worth being able to read at a glance.

### The thing this looks exactly like, said out loud

[`27-a-red-nobody-here-can-clear`](../../evals/27-a-red-nobody-here-can-clear/prompt.md)
fails a session for, among other things, *"the freshness check is downgraded or
dropped to get green"*. **This change is that shape**, it arrived on a pull
request that could not otherwise merge, and pretending otherwise would be worse
than doing it.

Four things are different, and they are the whole of the argument:

1. **Nothing is downgraded.** `verify.py` is untouched: same gates, same order,
   still exit 2, and the local command a person runs is unchanged. What moved is
   which CI job asks it.
2. **Nothing is dropped.** The check runs on every change, on its own line, and
   goes red. It is louder than it was as one of five failures in a shared job.
3. **It was not decided by the session that wanted to merge.** The maintainer
   was given the seventeen cases and the $58 and chose this instead, which is
   exactly the decision that case says belongs to them.
4. **What case 27 is actually about is unaffected.** Its subject is a session
   *reaching for* a way to make a red go away in order to get its own work
   through. This is a standing decision about what the check is for, taken in
   the open, with a spec.

The case is not edited and its rubric keeps that line. If a future session tries
this on its own initiative, it should still fail.

### What is genuinely given up

**A change can now reach `main` with none of its cases measured.** That is not a
side effect; it is the change. The board stops being a condition of merging and
becomes a standing report of what nobody has paid for yet.

Two things that were never true stay untrue: the score was never gated, and a
green `verify.py` never meant the cases passed. What is lost is the smaller,
real thing — the guarantee that no skill body reaches `main` without somebody
having been made to decide about its measurements. After this they are still
told, on every change, and can still say *not now* forever.

## What we are not doing

- **Changing `verify.py`, its exit codes, or `COSTS_MONEY`.** The 1/2 split is
  the whole reason this change is one line of YAML rather than a redesign, and
  [`0025`](0025-which-red-it-is.md) bought it.
- **`continue-on-error` on the new job.** It would mark the job green and put
  the finding in an annotation. Considered and rejected: this repository's
  argument against silence applies to its own checks list first.
- **Making the board a required check again under another name.** That is the
  same block with an extra step.
- **Touching the pre-push hook.** `--local` is what it already runs; this change
  gives that flag a second caller and no new meaning.
- **Un-gating anything else.** `COSTS_MONEY` holds one name and this change does
  not widen it. A gate somebody in the session can clear stays a gate.
- **A threshold, a decay, or an age at which a stale board starts blocking
  again.** Attractive, and it is a second decision about somebody else's budget
  wearing a rule's clothes. If merges pile up unmeasured, that is a fact worth
  seeing before it is automated against.

## Data

No storage contract moves and `specs/spec.md` needs no new vocabulary.

**This change stales nothing that was not already stale.** It edits one live
rule's example and adds one `@planned` rule, both in
`features/verification/which-red.feature`, whose only claimant is
[`27-a-red-nobody-here-can-clear`](../../evals/27-a-red-nobody-here-can-clear/) —
already stale on this branch because `setup` moved, and already in the bill
0032 costed. `method/gates.md`, the bindings and the workflow file are held by
no case.

The new rule ships `@planned` and is claimed by nobody. **That is a debt this
spec is choosing rather than hiding**: a case for it would have to watch a
merge happen, which no case here can do, and the honest alternative — writing a
softer rule a session could pass — is the dishonesty
[`evals/README.md`](../../evals/README.md) warns about. It is the same shape as
the two `@planned` rules [`0029`](0029-drawn-before-it-is-built.md) left behind.

## Risks

- **Nobody ever runs the suite again.** The likeliest outcome and the one this
  change cannot prevent. What makes it *visible* is that the count is on every
  pull request already — the report carries it, and
  [`what-explains-a-red-survives-it`](../features/verification/which-red.feature)
  keeps that true on exactly the red this creates. Seventeen owed is a number
  somebody can watch grow. A hundred owed is a different repository, and it will
  say so.
- **The red stops being read.** A check that fails on most pull requests and
  blocks none is a check people learn to scroll past — the same fate as any
  warning. There is no mitigation inside this change; the honest note is that
  the previous arrangement solved it by making the red unignorable and unpayable
  at once, and that is what was traded.
- **`gates-are-proven` is untouched.** `inject.py` still runs inside
  `verify.py --local` and still proves every gate fires.
- **`always-green` is untouched.** Nothing here reaches a consuming repository's
  build.
- **`context-budget` is untouched.** No description moves.
- **A future session bypasses a *gate* by citing this.** The reason the new rule
  is written narrowly — a measurement nobody in the session can clear — rather
  than as *reds that are inconvenient*. A broken gate is still a 1 and still
  blocks, and a mixed failure is still a 1.

## Acceptance checks

1. Push a branch whose only failure is a stale board. `repository checks` is
   **green**, `measurement board` is **red**, and the pull request is mergeable.
2. Break a gate on the same branch. `repository checks` goes red and the pull
   request is not mergeable.
3. Read the checks list on this repository's own open pull request. The job
   names say which of the two happened without opening a log.
4. `python3 .github/scripts/verify.py` locally — unchanged: still exit 2, still
   naming the cases, the cost and who can approve a run.
5. `gh api repos/sargismarkosyan/livespec/rules/branches/main` — the required
   contexts are still exactly `repository checks` and `plugin validate`, and
   `measurement board` is not among them.
