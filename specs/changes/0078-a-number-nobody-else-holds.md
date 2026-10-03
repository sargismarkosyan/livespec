# Spec 0078: a number nobody else holds

- **Status:** proposed
- **Issue:** [#167](https://github.com/sargismarkosyan/livespec/issues/167)

## Who this is for

**Ren — [`agent-accelerated-owner`](../personas/agent-accelerated-owner.md) —
with several changes in flight in one repository, one tree each.** The same
person as 0073–0076. Nothing about who this is for moves.

**The workflow is [`adopt-the-process`](../workflows/adopt-the-process.feature),
at *The changes after***, step 8 of
[`trusting-the-spec-again`](../journeys/trusting-the-spec-again.md): every
change spec a refining skill writes. The sitting also wires one more gate
(steps 5–6), and the audit's row-per-gate check asks for its row.

## The job behind the request

To start five changes from the same `main` and have each one's number stay
its own, from the first link to the merge. The number names the branch, the
picture, the pull request title and every link written before the change
lands.

**What they do today instead** is number by hand, or not notice:
- In helios/pi-plugins, !20 (0024) and !21 (0023) were opened five minutes
  apart. They only avoided a collision because they were numbered by hand.
  !20 was then closed, so `main` goes 0023 → 0025 with a gap nothing explains.
- In this repository on 2026-09-29, `main` ended at 0067 while #165 held
  0068–0072, so the rule would have numbered #166's spec 0068. It was
  numbered 0073 by hand, and the spec says why.

## Why now

- **All four refining skills number "one past the highest" in their own
  tree.** `refine-spec`, `refine-personas`, `refine-workflows` and
  `refine-journeys` each carry the rule. Two trees cut from the same `main`
  compute the same number.
- **Nothing catches it at merge.** The two files have different slugs, so
  git sees no conflict, Strict sees nothing to update, and `main` ends up
  holding two 0033s.
- **0074 made the in-flight work visible.** A claim comment names its branch,
  `spec-NNNN-<slug>`, so a number taken by a claim is now readable from the
  tracker, by every tree, before its pull request exists.

## The end value

A change spec's number is one nobody else is using, read from everything in
flight rather than from one checkout. If two still collide, the build says
so before the second one merges, naming both files.

**How we would know it worked:**
- Here: open two trees from the same `main`, claim two issues, and run
  `refine-spec` in each. They get consecutive numbers, and the second
  hand-back names the number it stepped past.
- Here and in every consuming repository wired after this: two files with
  one number fail verification, naming both.

## What changes

1. **The method, [`repository.md`](../../method/repository.md), *Several
   changes at once*.** One paragraph, *A number nobody else holds*. It
   names no platform or command:
   - **a change's number is one past the highest anywhere in flight**: the
     main branch, the change specs in open pull requests, and the branches
     the open claims name. A tree's own checkout sees only the first;
   - **the claim reserves the number.** The branch named in the claim
     comment carries it, so it is taken from the moment the claim is
     written, before any pull request exists;
   - **gaps are allowed and never refilled.** A closed pull request's number
     stays unused, so a link that cited it never comes to mean something
     else;
   - **if two collide anyway, the one not yet merged is renumbered**: its
     file, its heading and every link to it. The branch may keep its old
     name;
   - **an application's own numbered files collide the same way**, for
     example database migrations numbered one past the highest. Two trees
     each generate the next one. What catches it is Strict plus a pipeline
     that runs the migrations, so the bindings name that command. Nothing
     more is wired for it.

2. **The four refining skills.** `refine-spec`, `refine-personas`,
   `refine-workflows` and `refine-journeys` each say "one past the highest".
   That becomes **"one past the highest in flight, per
   [`repository.md`](../../method/repository.md#several-changes-at-once)"**,
   plus one line: say the numbers you stepped past and where each was held,
   and say it out loud when the open pull requests could not be read.

3. **A gate, `gate:change-number-unique`.**
   - It is a row in [`gates.md`](../../method/gates.md#the-ids) with `since`
     reading `next`, and in the
     [template ledger](../../templates/bindings.md).
   - **Wiring, in every consuming repository:** two change specs with one
     number fail verification, naming both. A gap passes.
   - `setup` wires it into the repository's traceability gate. It reads the
     gate table, so it needs no new text.
   - `doctor`'s `check:row-per-gate` reports the row missing in a ledger
     written before this. Every new gate has arrived that way.

4. **This repository.**
   - `trace.py` gains the check;
   - `inject.py` gains the fault *two change specs sharing a number*;
   - the ledger in [`setup/README.md`](../setup/README.md) gains the row;
   - `tests/` gains a test claiming `two-change-specs-never-share-a-number`
     against `trace.py`, as `test_crossing.py` does for 0053's gate.

5. **The case.**
   - A `refine-spec` case on fieldnote whose stand-in tracker client lists
     an open pull request adding 0007 and a claim naming
     `spec-0008-dawn-chorus`, while `main` ends at 0006. It claims
     `a-change-number-is-taken-past-everything-in-flight`, and the new spec
     must be 0009.
   - The client gains a verb for open pull requests, the way 0075's forge
     client listed merged ones.

**Rules added**, all `@planned` until the implementing commit:

| Rule id | Feature file | New or changed |
|---|---|---|
| `a-change-number-is-taken-past-everything-in-flight` | [`features/refining/a-number-nobody-else-holds.feature`](../features/refining/a-number-nobody-else-holds.feature) | new |
| `two-change-specs-never-share-a-number` | [`features/wiring/one-number-one-change.feature`](../features/wiring/one-number-one-change.feature) | new |

## What we are not doing

- **Numbering by issue.** A direct request has no issue, and the numbers
  would stop reading as the order changes landed in.
- **Numbering at merge.** Nothing could cite a number before the change
  lands: not the branch, the pull request title, the sketch or the picture.
- **Renaming branches on renumber.** The branch is a name for a tree, and
  the spec file is the record.
- **Wiring migrations.** The method says where their collision is caught,
  and the repository's pipeline catches it.
- **A lock.** Two sessions that read the in-flight state in the same second
  can still pick the same number. The gate catches that before the second
  merge, and the window is seconds, not days.

## Data

No storage contract moves. Consuming repositories gain one gate row. Specs
already numbered keep their numbers, and existing gaps (0023 → 0025 in
pi-plugins) pass the gate. A repository that already holds two specs with one
number fails the first verification after the gate is wired. That is
correct, and the hand-back of the sitting that wires it names both files.

## Risks

- **Reading the in-flight state costs a call or two** per change spec: open
  pull requests and open claims. It's paid once per spec, not per commit.
- **A pre-existing duplicate turns a repository red on upgrade.** That's
  named above, and renumbering the later file closes it.
- **`always-green`.** The gate runs only where the repository wires it, and
  reads only files in the tree.
- **Eval spend.** Editing the four refining skills stales their tier rows,
  and the new case starts unmeasured. Named in the pull request, and nothing
  runs without the maintainer's yes.

## Acceptance checks

1. Read *A number nobody else holds* in `repository.md` and confirm it names
   no platform or command.
2. Copy a change spec here under a second slug with the same number. See
   `verify.py` fail and name both files.
3. In two trees, claim two issues and run `refine-spec` in each. See two
   consecutive numbers.
