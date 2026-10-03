# Spec 0076: many merges, no hand rebases

- **Status:** proposed
- **Issue:** [#169](https://github.com/sargismarkosyan/livespec/issues/169)

## Who this is for

**Ren — [`agent-accelerated-owner`](../personas/agent-accelerated-owner.md) —
with several changes in flight in one repository, one tree each.** They
expect about five at once, and anyone who wants more may run more
([0073](0073-a-second-tree-as-ready-as-the-first.md), *How many at once*).
Nothing about who this is for moves.

**The workflow is [`adopt-the-process`](../workflows/adopt-the-process.feature).**
- The sitting gains one read-back and one offer (steps 5–6 of
  [`trusting-the-spec-again`](../journeys/trusting-the-spec-again.md)).
- The audit gains one line.
- What it shortens is the end of every change after that (step 8): merging
  five pull requests stops costing ten rebase-and-rerun cycles done by hand.

## The job behind the request

To merge the five changes that went green this afternoon without nursing each
one through the others' merges. And to keep what Strict guarantees: nothing
lands on `main` without having passed against the `main` it lands on.

**What they do today instead** is rebase by hand, in turn. Each merge puts
every other open pull request out of date at once. Each then needs a rebase
or a merge from `main`, a push, and a fresh CI run before it can merge. Five
pull requests cost 4 + 3 + 2 + 1 = 10 of those cycles, all for 5 merges.

## Why now

- **0073 made five trees ordinary**, and the method's protection table still
  assumes one change at a time. Strict is right about what it protects. What
  doesn't scale is who does the updating.
- **The platform has two answers, and the method names neither.**
  - A merge queue (GitHub's merge queue, GitLab's merge trains) tests each
    change against `main` plus the changes ahead of it, then merges them in
    order.
  - Where there is no queue, the platform can still update a branch from
    `main` on the server, and merge it automatically once it is green.
    Nobody rebases; the agent asks.
- **Here, the queue is not available, and that was read back rather than
  assumed.** On 2026-10-03 a ruleset with enforcement *disabled*, aimed at a
  branch that doesn't exist, was posted with a `merge_queue` rule. GitHub
  answered `422 Invalid rule 'merge_queue'`, and nothing was created. The
  owner is a personal account (`owner.type: User`), and GitHub's merge queue
  is not offered there. So this repository is the fallback case, and the
  method must not read as if every repository had a queue.
  - `allow_auto_merge` is already on.
  - `allow_update_branch` is off.

## The end value

Five green pull requests merge in order, each tested against the `main` it
lands on, and nobody rebases one by hand. The platform's queue does it where
there is one. Where there isn't, the platform's update-and-auto-merge does it,
driven by the agent. The bindings say which, read back.

**How we would know it worked:**
- In this repository, after implementation:
  - `gh api repos/sargismarkosyan/livespec --jq .allow_update_branch` reads
    `true`;
  - three open pull requests, merged as update-branch then auto-merge in
    turn, all land with no local rebase.
- In a repository whose platform offers a queue, the sitting turns it on only
  after a yes, adds the queue's event to the pipeline, and writes the row
  only once a merge has gone through the queue.

## What changes

1. **The method, [`repository.md`](../../method/repository.md) —
   *Branches and pull requests*.** One paragraph, *Several merges at once*.
   It names no platform, command or event:
   - Strict stays. Whatever merges has passed against the `main` it lands on;
   - with several changes in flight, the updating is the platform's, not a
     person's:
     - **where the platform offers a queue, merging goes through it.** Its
       required checks must run on the queue's own event, or every queued
       merge waits forever;
     - **where it offers none**, the platform updates each branch from `main`
       on the server and merges it once green, one pull request at a time and
       in order. Without a queue the reruns are still paid, but nobody types a
       rebase;
   - which of the two applies is read back from the platform, never inferred
     from the pipeline file, and a queue nobody watched one merge through is
     *unobserved*.

   The protection table's *Strict* row gains: *with several changes in
   flight, a queue or the platform's own update keeps it*.

2. **The bindings template, [`bindings.md`](../../templates/bindings.md) —
   one row, *Several merges at once*.** It holds one of two things:
   - the queue: the setting, the event the required checks run on, and the
     date a merge was watched through it;
   - *not available, decided*, with the platform's refusal, the fallback's
     two settings (update a branch, merge once green), and the commands that
     drive it.

3. **[`setup`](../../skills/setup/SKILL.md).** With the protection read-back:
   - **Availability is read from the platform.** Where the platform has a
     safe way to ask, it is asked. Where only a write would answer, the
     write is a disabled rule aimed at a branch that doesn't exist, and it is
     removed afterwards.
   - **A queue is available:** offer to require it, and to add the queue's
     event to the workflow that runs the required checks. Wait. Then watch
     one pull request merge through the queue before writing the row.
   - **No queue:** record the refusal. Offer the fallback's settings where
     they are off, and wait.
   - The refusals gain *changing a protection setting unasked*, already
     there since 0075.

4. **[`doctor`](../../skills/doctor/SKILL.md) and
   [`tools/doctor.py`](../../tools/doctor.py) — one check.**
   `check:merge-queue`, *judgment, platform*:
   - no row is *open*, closed by the sitting;
   - otherwise, the queue row (the setting and the pipeline's trigger) or
     the fallback row (its settings) is read back;
   - any of it not as the row says is *open*, naming what differs.

5. **[`gates.md`](../../method/gates.md#the-checks-an-audit-makes)** — the
   id, with `since` reading `next`. The pull request carries `## Ids`.

6. **This repository.**
   - `allow_update_branch` is turned on at implementation.
   - The bindings gain the row: *not available, decided*, with the 422, the
     date, and the fallback. The fallback is `gh pr update-branch <n>` then
     `gh pr merge <n> --auto --merge`, one pull request at a time and in
     order, with the read-back commands.
   - The step goes into `CLAUDE.md`'s loop, step 7, as the way several pull
     requests merge here. The ceiling has room for it at most as a phrase,
     and the line count is checked at implementation.

7. **The cases and tests.**
   - A unit test holds `doctor.py`'s pre-fill: no row reads open, and a row
     hands on its read-back command.
   - Two eval cases, on the fixture's own forge client as in 0075:
     - a `setup` case whose forge offers a queue nobody turned on, and whose
       pipeline runs only on pull requests: the offer, the trigger, the wait
       (`several-merges-go-through-a-queue-or-its-fallback`);
     - a `doctor` case whose row says fallback and whose forge has the update
       setting off (`the-queue-is-read-back`).

**Rules added**, all `@planned` until the implementing commit:

| Rule id | Feature file | New or changed |
|---|---|---|
| `several-merges-go-through-a-queue-or-its-fallback` | [`features/setup/many-merges.feature`](../features/setup/many-merges.feature) | new |
| `the-queue-is-read-back` | [`features/wiring/many-merges.feature`](../features/wiring/many-merges.feature) | new |

## What we are not doing

- **Dropping Strict where there is no queue.** It would remove the reruns
  and the guarantee with them: two changes each green alone can be red
  together on `main`.
- **Moving this repository to an organization** to get a queue. The
  marketplace reads this repository's URL, so every install would move with
  it. That is a decision of its own.
- **A script that drives the fallback.** It is two platform commands per pull
  request, written in the bindings. A tool for it would be one more thing the
  gates have to hold.
- **Batching or merge-method policy** (squash, rebase, merge). Whatever the
  repository already uses stays.
- **Stacks (#170, 0075), claims (#171, 0074), numbering (#167).**

## Data

No storage contract moves. Bindings written before this ship have no row, so
the first audit after the upgrade reports `check:merge-queue` *open* and
names the sitting.

## Risks

- **The availability probe is a write.** Where a platform answers
  availability only by refusing a rule, the sitting posts one that is
  disabled, aimed at a branch that doesn't exist, and removed straight
  after. A probe that unexpectedly succeeds is deleted at once, and the
  hand-back says so.
- **A queue whose checks never run.** Queued merges hang, and nothing fails.
  That is why the trigger is part of the offer, and why the row waits for one
  watched merge.
- **Fallback reruns cost CI time.** Here that is about 30 seconds a run on a
  public repository. Elsewhere it may be billed. The row names it.
- **Eval spend.** Editing `setup` and `doctor` stales their tier rows, and
  the two new cases start unmeasured. Named in the pull request, and nothing
  runs without the maintainer's yes.

## Acceptance checks

1. Read *Several merges at once* in `repository.md`. Confirm it names no
   platform, command or event.
2. Here, `allow_update_branch` reads `true`, and the bindings row records the
   422 and the fallback.
3. With two open pull requests here, run update-branch and auto-merge on each
   in order, and see both land with no local rebase.
