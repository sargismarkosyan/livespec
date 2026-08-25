# Spec 0008: the gate gets something to hold

- **Status:** proposed
- **Issue:** [#21](https://github.com/sargismarkosyan/livespec/issues/21), and the
  rule debt [`0002`](0002-setup-finishes-what-it-names.md) and
  [`0004`](0004-setup-can-be-offered.md) each reserved and could not pay.

## Who this is for

[`@persona:agent-accelerated-owner`](../personas/agent-accelerated-owner.md), in
[`adopt-the-process`](../workflows/adopt-the-process.feature) — and specifically
at the end of it, which is the part of that attempt nothing has reached yet. The
workflow ends *"when the next change opened in that repository proves it: the
pull request carries what the version leaves behind, and the pipeline refuses the
change until the specs move with it."* Half of that end state describes something
this plugin has never built.

The persona file is what makes this the right person rather than the author:
*"they read the spec layer and not the documentation"*, and *"what does get read
is the spec layer: the workflows, the journeys, the personas. So when one of
those quietly stops being true, nothing stands between that and finding out
months later."* A traceability gate that passes over an empty layer is that
sentence with a green check on top of it.

The always-promise most at risk is **`gates-are-proven`**
([spec.md](../spec.md#the-promises-that-belong-to-no-single-workflow)) — *no gate
ships without a fault that makes it fire*. This change adds one gate behaviour
and narrows another, and both are things `inject.py` has to be able to break.

## The job behind the request

Know whether the spec layer is still true, without reading it.

That is the whole product, and today this repository does not have it. The
traceability gate reports `0 live rule(s), 0 planned, 0 claimed by 11 eval
case(s)` — it is green because there is nothing in it, and there is no way to
tell that reading from a green run over a layer that holds. The gate that is
supposed to fail when a spec stops being true cannot currently fail.

The second half is the same job one step later: when a change *does* move the
spec, put what moved where the person reviewing it already looks — which is the
pull request, not the branch.

## Why now

Three things arrive at once, and two of them are on a clock somebody else set.

**The debt is two versions old and named.**
[`0002`](0002-setup-finishes-what-it-names.md) reserved three rule ids and marked
all three **owed**; [`0004`](0004-setup-can-be-offered.md) reserved three more on
the same grounds. Both were blocked on one thing — *"`trace.py` fails any feature
naming no live `@workflow:`, and workflows/ is empty"* — and
[`0006`](0006-adopt-the-process.md) cleared it.

**`0006` named this change and wrote its success test.** *"The next change that
writes a feature file tags it `@workflow:adopt-the-process`, drops `@planned`
from the workflow in the same commit, and the gate goes from mapping one workflow
to nothing, to mapping one workflow to a feature and a case."*

**And `0006` left one blocker standing, which this change clears rather than
argues past.** Its risks record that the tag *"cannot come off until
[#21](https://github.com/sargismarkosyan/livespec/issues/21) does, and that is a
dependency nobody would find by reading the file alone."* #21 is still open. So
#21 lands here, first, and the tag comes off because its end state became true —
not because a gate insisted.

## The end value

The handful of files this persona actually reads are held by something that can
fail. Six rules go live, each claimed by a case, and the first time one of those
skills changes in a way the rule no longer describes, the run says so instead of
staying green.

And a pull request that moved the Gherkin shows the Gherkin, in the body, where
somebody deciding whether to merge is already looking.

**How we would know it worked:** two lines change and both are readable off a
terminal. `trace.py` goes from `0 live rule(s) traced` to six, mapped to two
feature files and the cases claiming them. And a pull request that edits
`specs/features/` while saying nothing about it in its body **fails CI**, where
today it merges green.

## What changes

**This is larger than one step, deliberately and at the human's direction.** See
*Risks* — the three parts that must be atomic are marked, and the two that could
have been their own versions are named.

1. **#21 lands in the method.**
   [`repository.md`](../../method/repository.md#every-pull-request-carries-a-moving-picture)
   gains a sibling to the moving picture: a pull request that adds or changes a
   `.feature`, a workflow walk or an e2e test **quotes the Gherkin it moved** in
   the body — the Rule and its Examples, inline or linked at the committed SHA.
   Conditional, not ceremony: a change touching no spec surface says nothing, the
   same exemption the picture already has.

2. **The bindings say what that means here.**
   [`setup/README.md`](../setup/README.md) already records that this repository
   has no moving picture because it has no app; so the Gherkin block is the whole
   of the deliverable here, and the row saying so goes next to the existing one.

3. **`version_gate.py` checks it.** A pull request whose diff touches
   `specs/features/` or `specs/workflows/` and whose body carries no Gherkin
   block fails, with the same message shape as the missing `## Changelog`
   section. The predicate goes in `releaselib.py` — the one reader the gate and
   the release job share — and `inject.py` gains the fault that breaks it.

4. **`@planned` comes off `adopt-the-process`.** *(Atomic with 5 and 6.)* Its end
   state is true once 1–3 ship: the pull request carries what the version leaves
   behind, and the pipeline refuses the change until the specs move with it.

5. **Two feature files land.** *(Atomic with 4 and 6.)*
   `specs/features/setup/invocation.feature` and
   `specs/features/setup/hand-back.feature`, six rules, all six ids exactly as
   reserved. The Gherkin is below.

6. **One new eval case walks the workflow.** *(Atomic with 4 and 5.)*
   `12-setup-drives-the-sitting` — the driven-setup case
   [`0002`](0002-setup-finishes-what-it-names.md) called *"the first thing to
   write when the runner unblocks"*. It tells setup to go, and is graded on the
   hand-back: the chain continued into the interviews without a command being
   typed, CLAUDE.md names where issues actually go, and the existing CLAUDE.md
   was scored against the ten requirements rather than counted as done. It
   carries `workflow:adopt-the-process` and all three `hand-back` rule claims.

7. **Cases 09 and 11 gain the claims they have always held.** No prompt or grader
   moves — `09-setup-confirms-before-writing` claims `setup-can-be-offered` and
   `setup-confirms-before-writing`; `11-neg-setup-adjacent-request` claims
   `setup-ignores-an-adjacent-request`.

8. **`trace.py` learns that a refusal rule is verified by a refusal case.** Today
   it warns on *any* should-not-fire case claiming a rule — *"a case asserting
   nothing fires cannot verify one"* — which is true of a rule that promises a
   behaviour and false of a rule that promises restraint. Without this, item 7
   ships a warning that can never be cleared, and
   [`gates.md`](../../method/gates.md) says a warning surviving two versions is
   either promoted or deleted. `inject.py` gains the fault.

9. **`setup` writes the convention into a consuming repository.** Section 5's
   bindings table gains the row, so an adopted repository carries #21's rule
   rather than this one being the only repository that has it.

### The Gherkin

Both files land in the implementing commit, not with this spec — `trace.py`
refuses a feature naming a `@planned` workflow, and refuses a live workflow that
no case walks, so 4, 5 and 6 are one commit or none. That is the same wall
[`0002`](0002-setup-finishes-what-it-names.md) hit and recorded, and it is why
the rules are quoted here rather than linked.

```gherkin
@feature:setup-invocation @workflow:adopt-the-process
Feature: Reaching setup, and setup knowing it was not the thing asked for

  @rule:setup-can-be-offered
  Rule: In a repository with the plugin and no bindings, asking for the process reaches setup

    Example: the ask arrives in plain words
      Given a consuming repository with the plugin enabled and no bindings
      When somebody asks for the process to be set up there
      Then setup is what answers
      And no specs/ tree of the agent's own invention is offered in its place

  @rule:setup-confirms-before-writing
  Rule: Setup says what it would write, and waits to be told to start

    Example: the sitting is sized before it begins
      Given somebody has asked for the process
      When setup answers
      Then it names the files it would write, and the interviews that follow it
      And nothing has been written

  @rule:setup-ignores-an-adjacent-request
  Rule: A request that only sounds like setup gets the answer it asked for

    Example: a question about the checks already there
      Given a consuming repository with the plugin enabled and the process not set up
      When somebody asks what the existing checks run
      Then they are told what the checks run
      And the process is not installed in place of the answer
```

```gherkin
@feature:setup-hand-back @workflow:adopt-the-process
Feature: What a setup sitting leaves behind

  @rule:setup-continues-into-the-layers
  Rule: The sitting continues into the layers rather than naming them

    Example: the interviews follow without being asked for
      Given setup has written the skeleton, the gates and CLAUDE.md
      When it hands back
      Then the persona, workflow and journey interviews have been started
      And nobody had to type the command that starts them

    Example: the chain is stopped partway
      Given the interviews have begun
      When somebody says to stop
      Then the sitting ends there
      And the hand-back names which layers are still empty

  @rule:setup-finds-where-issues-go
  Rule: The repository's own way of filing issues is found and written down

    Example: the tracker is not the one a skill would have assumed
      Given a consuming repository whose issues are filed somewhere other than GitHub
      When the sitting ends
      Then CLAUDE.md names where issues actually go there

    Example: there is no convention to find
      Given a consuming repository with no way of filing issues
      When the sitting ends
      Then that is reported rather than left blank

  @rule:setup-audits-an-existing-claude-md
  Rule: An existing CLAUDE.md is read against the requirements, not counted as done

    Example: the file is already there
      Given a consuming repository that already has a CLAUDE.md
      When setup reaches it
      Then each requirement is reported as met, missing or stale
      And the file existing has not counted as the step being finished
```

**Rules added or changed** — the `@rule:` ids in `specs/features/`:

| Rule id | Feature file | New or changed |
|---|---|---|
| `setup-can-be-offered` | `features/setup/invocation.feature` | new — reserved by [`0004`](0004-setup-can-be-offered.md) |
| `setup-confirms-before-writing` | `features/setup/invocation.feature` | new — reserved by [`0004`](0004-setup-can-be-offered.md) |
| `setup-ignores-an-adjacent-request` | `features/setup/invocation.feature` | new — reserved by [`0004`](0004-setup-can-be-offered.md) |
| `setup-continues-into-the-layers` | `features/setup/hand-back.feature` | new — reserved by [`0002`](0002-setup-finishes-what-it-names.md) |
| `setup-finds-where-issues-go` | `features/setup/hand-back.feature` | new — reserved by [`0002`](0002-setup-finishes-what-it-names.md) |
| `setup-audits-an-existing-claude-md` | `features/setup/hand-back.feature` | new — reserved by [`0002`](0002-setup-finishes-what-it-names.md) |

**All six land live rather than `@planned`**, which is the one place this change
departs from the ordinary loop. `@planned` means specced and not built; all six
behaviours shipped in 0.8.0 and 0.9.0 and the ids were reserved at the time. Both
reserving specs said so — *"with the rules live rather than `@planned`, because
by then the behaviour will already be built."* Writing the tag on and taking it
off in the same version would be a costume.

**Ledger:** nothing moves. Every row this change exercises already reads
*automated* in [setup/README.md](../setup/README.md#gate-wiring). What the ledger
gains is nothing at all, and that is the correct outcome: the rows were wired at
0.6.0 against faults, and this is the first change that gives two of them real
content to hold rather than an empty layer to pass over.

## What we are not doing

- **Not writing the other three workflows.** Filing what they found, getting a
  request specced, taking a version through review — still real, still
  uninterviewed, and [`0006`](0006-adopt-the-process.md) already refused to cut
  them from a guess. Nothing here changes that.
- **Not building the tooling that emits the Gherkin block.** #21 names it as a
  bonus — *"the trace/report tooling could later emit the block automatically for
  the author to paste."* A generator is worth having and is not what makes the
  rule true; the gate that refuses a body without one is. Its own issue.
- **Not writing the second walking case.** The return leg — coming back cold
  weeks later and acting on what is written — is where
  [`trusting-the-spec-again`](../journeys/trusting-the-spec-again.md) says the
  value actually lands, and no eval case can reach it. Faking it with a case that
  merely re-reads a fixture would be the costume the workflows README warns
  about.
- **Not retroactively speccing the other five skills.** `specs/README.md` is
  explicit that the layer starts at the next change rather than at the history,
  and these six ids are the exception it already carved: they were reserved by
  changes that could not spend them, not invented now to fill a directory.
- **Not promoting `trace.py`'s warning to an error.** Item 8 narrows what warns;
  it does not decide what a should-not-fire case claiming a *behaviour* rule
  should cost. That warning stays a warning and stays on the two-change clock.
- **Not adding a coverage gate.** Still *not applicable* for the reason the
  bindings give, and six live rules do not change it.

## Data

None. There is no storage contract — the plugin ships prose, and what a version
leaves behind is listed in [spec.md](../spec.md#what-a-version-leaves-behind).
Item 1 adds to that list in the method's terms rather than this repository's;
item 2 is where it becomes a fact about this repository.

## Risks

- **Size is the real risk, and it was chosen with the alternative on the table.**
  This is three versions' worth: #21 and its gate, the trace.py narrowing, and
  the rules with their case. Items 4, 5 and 6 genuinely cannot be split —
  `trace.py` forces them into one commit, and that was verified rather than
  assumed. Items 1–3 and item 8 could each have been their own version, and were
  not. **One change spec = one step = one version** is the rule in
  [`process.md`](../../method/process.md) this bends, and the mitigation is that
  it is written here rather than discovered in review.
- **The walk is partial and the tag will not say so.** The new case walks the
  sitting. The attempt ends at a pull request in somebody's repository days
  later, which no eval case can reach — so `@workflow:adopt-the-process` will
  read as walked when what is walked is the first leg. This is the strongest
  argument the workflow was cut too long, and if it is re-cut later, this is the
  evidence.
- **The new case is the most expensive in the suite and has never been run.**
  Nothing here has: `claude plugin eval` is still behind early access. This case
  drives setup through a whole sitting, so it is the one most likely to hit
  `max_turns` and score zero in both arms, which reads as *the plugin did
  nothing*. It also needs a repository with an existing CLAUDE.md and a tracker
  to find. The suite's convention is that the situation lives in the prompt; if
  that proves too thin, the case converts to a `case.yaml` with a
  `scaffold_script` and the documented invocation gains `--scaffold`, which is
  a change to what `evalsuite.py` checks and is called out here so it is not a
  surprise.
- **A body-text gate is satisfied by a fence with nothing in it.** Item 3 can
  check that a Gherkin block is present, never that it is the right one. Same
  weakness the `## Changelog` check already carries and the same answer: it stops
  the silent case, which is a body that says nothing at all.
- **`ids-are-permanent` is spent six times in one version.** Every id was
  published in an approved spec already, so the promise was made in 0.8.0 and
  0.9.0 rather than here — but this is the change that makes them load-bearing in
  every consuming repository at once.
- **Item 8 narrows a check, and narrowing a check is how one stops firing.** The
  fault in `inject.py` has to break the *narrowed* rule, not the old one, or the
  gate keeps a green record of a check it no longer performs.

## Acceptance checks

1. `python3 .github/scripts/verify.py` is green **with no warnings**, and its
   traceability line reads six live rules traced, two feature files, one workflow
   mapped to both and walked by a case.
2. Open a pull request that edits a file under `specs/features/` and put nothing
   about it in the body. CI fails, and the message names the Gherkin block rather
   than the changelog.
3. Add the block. CI passes. Then delete the fence's contents and confirm it
   still passes — that is the known hole in *Risks*, checked rather than assumed.
4. Read the six `Rule:` lines once looking only for interface detail — a
   command, a filename, a flag. Any rule that would need rewording when the
   skill's wording changed is written at the wrong altitude and will rot.
5. `git log --oneline` shows the spec commit before the implementation commit,
   and the implementation commit contains items 4, 5 and 6 together. A commit
   with the feature files and not the case did not exist at any point.
6. Read `specs/workflows/adopt-the-process.feature` line 1. `@planned` is gone,
   and [#21](https://github.com/sargismarkosyan/livespec/issues/21) is closed
   with a comment saying what was asked, what shipped and why they differ.
