# Spec 0074: an issue is taken once

- **Status:** approved — by the maintainer, 2026-10-03
- **Issue:** [#171](https://github.com/sargismarkosyan/livespec/issues/171)

## Who this is for

**Ren — [`agent-accelerated-owner`](../personas/agent-accelerated-owner.md) —
with several changes in flight in one repository, one tree each.** That line
is already in the persona, observed on the day
[`0073`](0073-a-second-tree-as-ready-as-the-first.md) was written: six trees
in one repository, two of them opening merge requests five minutes apart.
Nothing about who this is for moves. 0073 made a second tree as ready as the
first. This spec makes sure two trees are not working on the same issue.

**Whatever harness they drive it through.** The maintainer works in Claude
Code, Pi and Codex. The claim lives in the tracker, which every harness can
reach, and it names the harness and the session in the harness's own words.
It never names a harness's command for resuming one.

**The workflow is [`adopt-the-process`](../workflows/adopt-the-process.feature).**
The claim itself happens at *The changes after*, step 8 of
[`trusting-the-spec-again`](../journeys/trusting-the-spec-again.md), every
time an issue is picked up, many times a day. The sitting gains one row and
one offer (steps 5–6), and the audit gains two lines. The
[workflows README](../workflows/README.md#reading-this-as-a-map) asks what a
longer adoption buys. Here it buys every pickup after it: a pickup no longer
risks a whole spec and build that one of two trees then throws away.

## The job behind the request

To say "pick up issue 12", or "pick up the next one", to an agent in a fresh
tree without first remembering which of the other trees is already on what.
And, when one of those trees has gone quiet, to know which session to go back
to rather than starting the work again.

**What they do today instead** is keep it in their head. The issue reads the
same whether nobody is on it or three trees are. The spec branch is named
`spec-NNNN-<slug>`, after the spec number, so even a look at the branches
does not say which issue a branch is working on. Nothing has been taken twice
yet, and the issue says so. What has happened is everything around it: six
trees in one repository (0073), five pull requests merging as ten rebases
(#169), and four pull requests stranded on a merged parent (#170). An issue
taken twice is the same kind of collision, one step earlier, and it costs
more: a whole spec and a whole build.

## Why now

- **0073 made the parallel case the ordinary one.** A tree is now one command
  away. With a second tree that cheap, issues get handed out faster, and that
  is exactly where nothing checks.
- **The record that would answer it already exists, and nothing reads it.**
  The tracker shows labels and comments. A pull request saying `Closes #N`
  links itself. The repository's own list of trees knows every branch on the
  machine. A refining skill reads the issue and stops there:
  `skills/refine-spec/SKILL.md`, *the issue, if there is one*. `rg -i
  "assign|in flight|claim"` over `skills/` and `method/` finds nothing.
- **The duplicate is only found at the end.** Two trees on one issue look
  like two healthy trees until the second pull request opens, or until a
  number collides (#167). By then both specs exist.

## The end value

Picking up an issue tells you, before anything is written, whether another
session already has it, where that work is, and which session to resume.
Picking up "the next one" never lands on an issue another tree holds. A claim
nobody is working on any more is reported to the person, not taken over
quietly.

**How we would know it worked:**

- In this repository, after this ships, every issue a refining skill picked
  up carries the label and one comment naming the branch, the tree, the
  harness and the session id. A second session asked for the same issue says
  so and writes nothing.
- `doctor` lists a claim whose branch, tree and pull request are all gone,
  with its age and session. It never removes one.
- In a repository set up after this ships, the bindings name the label, and
  the tracker has it.

## What changes

1. **The method, [`repository.md`](../../method/repository.md).** A paragraph
   in *Several changes at once*, *An issue is taken once*. It names no
   command, label or harness. It says:
   - **work on an issue starts with a claim, in the tracker**, because the
     tracker is the one place every tree and every machine can read. A file in
     one tree is invisible to the next;
   - **the claim is a marker the bindings name plus one comment** saying where
     the work is: the branch, the tree, the harness, and the session's id as
     that harness gives it. When the harness gives no id the session can
     read, the comment says *not exposed* rather than inventing one. The
     marker is what a list of issues filters on. The comment is what lets the
     person resume the right session rather than start again;
   - **the claim is read before anything is written**, and a claimed issue
     is reported, not taken. That includes choosing "the next issue";
   - **nothing releases a claim by age.** A claim with no branch, no tree and
     no pull request behind it is shown to the person, with its age. Taking
     it over is their call, and the new comment names the claim it replaced.
     A session cannot tell a slow session from a dead one, and guessing wrong
     throws away somebody's work;
   - **the claim ends with the pull request that closes the issue**, or with
     the session that drops the work, which takes the marker off and says
     why;
   - **an unread claim is not an absent claim.** A tracker that does not
     answer is said, and the person decides.

2. **The bindings template, [`bindings.md`](../../templates/bindings.md) — one
   row, *Claiming an issue*.** The marker, the command that puts it on and
   takes it off, and the command that lists the issues carrying it. Or *not
   applicable, decided* when there is no tracker.

3. **The four refining skills:
   [`refine-spec`](../../skills/refine-spec/SKILL.md),
   [`refine-personas`](../../skills/refine-personas/SKILL.md),
   [`refine-workflows`](../../skills/refine-workflows/SKILL.md),
   [`refine-journeys`](../../skills/refine-journeys/SKILL.md).** Where each
   reads its issue, a short step:
   - read the claim before writing anything;
   - claimed: report the branch, tree, harness, session id and age, and stop
     until the person answers;
   - unclaimed: put the marker on and write the comment;
   - asked for the next issue, choose among the unclaimed and say which ones
     were skipped;
   - the hand-back of a spec the person turns down takes the marker off,
     with a comment.

   The full rule lives in the method. Each skill carries the step in a few
   lines and links to the method, so four skill bodies are not four copies
   of it. No `description` changes, so the always-on cost does not move.

4. **[`setup`](../../skills/setup/SKILL.md).** Where it writes the tracker
   row, it also writes the claim row:
   - it reads the tracker's existing labels, and reuses one that already
     means *in progress*;
   - where there is none, it offers to create `in-progress`, with the
     command, and waits. Writing to somebody's tracker is outward-facing, the
     same as the hook offer;
   - a refusal is written into the row, along with who can make the label.

5. **[`doctor`](../../skills/doctor/SKILL.md) and
   [`tools/doctor.py`](../../tools/doctor.py) — two checks.**
   - `check:claim-row`, *mechanical, record*: the bindings carry the row.
     Missing is *open*, closed by the sitting. When present, the tool
     pre-fills the next line with the marker.
   - `check:claims-in-flight`, *judgment, record*: lists the open issues
     carrying the marker and reads each comment's branch against the
     repository's list of trees, the remote's branches and the open pull
     requests. Each claim with all three gone is listed with its age and
     session. The line is *open* when any is listed, or when the marker does
     not exist in the tracker, and *not-read*, with why, when the tracker
     does not answer. The audit releases no claim.

6. **[`gates.md`](../../method/gates.md#the-checks-an-audit-makes) — the two
   ids**, with `since` reading `next`. The pull request carries `## Ids`:
   added `check:claim-row`, `check:claims-in-flight`.

7. **This repository.**
   - Its bindings gain the row: label `in-progress`, put on and taken off
     with `gh issue edit --add-label` / `--remove-label`, listed with
     `gh issue list --label in-progress`.
   - The label is created in `sargismarkosyan/livespec` at implementation.
   - The open issues this session is about to work through are claimed as
     each is picked up, starting with this one.

**Prose moved with it:** **claim** in [`spec.md`](../spec.md)'s vocabulary,
in this spec's commit.

8. **The cases and the tests.**
   - A unit test under `tests/` claims `the-claim-row-is-there` against
     `doctor.py`.
   - Eval cases claim the rest. Each world is a scaffolded repository with a
     stand-in tracker CLI on `PATH`, which answers with the issue, its labels
     and its comments and records what was called. The expected cut is four:
     - `refine-spec` on a free issue: it claims before writing, and the
       person then turns the spec down, so the claim comes off
       (`an-issue-is-claimed-before-anything-is-written`,
       `a-dropped-claim-is-released-by-whoever-dropped-it`). Built as
       [`74`](../../evals/74-an-issue-nobody-has-taken/prompt.md). The
       release first sat in the next case, but nothing is claimed there to
       release;
     - `refine-spec` on an issue another tree holds: it reports and writes
       nothing (`a-claimed-issue-is-not-taken-twice`), built as
       [`75`](../../evals/75-an-issue-another-tree-holds/prompt.md);
     - `setup` with a tracker lacking the label
       (`the-claim-marker-is-bound`), built as
       [`76`](../../evals/76-a-tracker-with-no-claim-marker/prompt.md);
     - `doctor` with one stranded claim
       (`a-claim-with-nothing-behind-it-is-listed`), built as
       [`77`](../../evals/77-a-claim-nobody-is-behind/prompt.md).
   - The tracker in every case is the fixture's own client script, which
     the bindings name. A real `gh` lent to a session could write to a live
     repository.

**Rules added**, live since the implementing commit:

| Rule id | Feature file | New or changed |
|---|---|---|
| `an-issue-is-claimed-before-anything-is-written` | [`features/refining/an-issue-already-taken.feature`](../features/refining/an-issue-already-taken.feature) | new |
| `a-claimed-issue-is-not-taken-twice` | same | new |
| `a-dropped-claim-is-released-by-whoever-dropped-it` | same | new |
| `the-claim-marker-is-bound` | [`features/setup/claiming-an-issue.feature`](../features/setup/claiming-an-issue.feature) | new |
| `the-claim-row-is-there` | [`features/wiring/claims-in-flight.feature`](../features/wiring/claims-in-flight.feature) | new |
| `a-claim-with-nothing-behind-it-is-listed` | same | new |

The rules that read or write the tracker carry
`@crosses:consuming-repository`. That is the row covering a consuming
repository's real tracker, which no case reaches. So each one has an example
of the tracker refusing or not answering, and the stand-in plays that part.

## What we are not doing

- **Branch names carrying the issue number.** That is #167's, and the claim
  comment makes it unnecessary here: it names the branch, whatever the branch
  is called.
- **The assignee as the claim.** Every agent runs as the same account, so an
  assignee would only ever say *the maintainer*, which they already know.
- **A draft pull request at the start.** It would open a pull request for
  every spec, including the ones turned down, and it says nothing about the
  session.
- **Releasing a claim by age, or a threshold in the bindings.** A slow session
  and a dead one look the same from outside. The person is asked.
- **A command for resuming a session.** Each harness has its own, and naming
  one would bind the method to it. The comment carries the harness and the
  id, and the person knows their harness.
- **A claim file in the repository.** One tree's file is invisible to every
  other tree until it merges, which is too late.
- **`todo` claiming.** It files issues and works on none. Filing is not taking.
- **The merge queue (#169) and stacked pull requests (#170).** Both get their
  own specs.

## Data

No storage contract moves. Consuming repositories' bindings gain one row, and
their trackers gain one label once the sitting is accepted. Bindings written
before this ship without the row, so the first audit after the upgrade
reports `check:claim-row` *open* and names the sitting, the same way every row
since 0.21.0 has arrived. Issues already in flight carry no claim. The first
session to pick one up claims it, and the audit says nothing about an
unclaimed issue.

## Risks

- **Comment noise.** One comment per pickup, and one more per drop or
  takeover. For the persona that is a line per change, on issues they file
  and read anyway.
- **A claim left behind by a session that crashed.** That is the point of
  `check:claims-in-flight`: it shows the claim and never releases it.
- **The session id is a harness detail.** One harness gives it in its
  environment, another in a command, another not at all. The method asks for
  the id *as the harness gives it, or not exposed*, so a harness with none
  costs one line of honesty, not a broken claim.
- **`never-implements`.** Writing a label and a comment is tracker work, the
  same kind `todo` already does. No application code is touched.
- **`always-green`.** Nothing here reaches a user's build. The claim is never
  a gate in CI.
- **Eval spend.** Editing `refine-spec`, `refine-personas`,
  `refine-workflows`, `refine-journeys`, `setup` and `doctor` stales every
  tier row that holds them, and the four new cases start unmeasured. The
  stale set is read off the board at implementation and named in the pull
  request. None of it runs without the maintainer's yes.

## Acceptance checks

1. Read *An issue is taken once* in `repository.md` and confirm it names no
   command, label or harness.
2. In this repository, from one tree, run `refine-spec` on an open issue. See
   the label and the comment arrive before the spec file does.
3. From a second tree, in a different harness, ask for the same issue. See it
   named as in flight, with the first session's harness and id, and see
   nothing written.
4. Delete the first tree's branch without a pull request and run `doctor`.
   See the claim listed with its age, and see the label still on the issue.
