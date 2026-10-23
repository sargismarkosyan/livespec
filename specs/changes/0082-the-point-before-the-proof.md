# Spec 0082: the point before the proof

- **Status:** approved — by the maintainer in advance, 2026-10-23: implemented end to end, reviewed at the merge request
- **Issue:** [#180](https://github.com/sargismarkosyan/livespec/issues/180)
- **Number:** given by the maintainer, not read from what is in flight; 0080
  and 0081 are held by changes in other trees.
- **Sketch:** skipped, because approval was given in advance.

## Who this is for

**Ren — [`agent-accelerated-owner`](../personas/agent-accelerated-owner.md) —
at the merge**, and whoever Ren asks to review. The persona line this rests on
is *"checking the result by reading is not available"*: what Ren reads instead
is the spec layer and the pull request. A pull request is the one piece of
prose an agent writes that a person is still expected to read, so a body too
long to read takes away the one check they have left. The reviewer in the
report is a second person. The persona file expects contributors and has
not met one yet, and this is the first report of what one of them needs. This
spec does not edit the persona; see *What we are not doing*.

**The workflow is [`adopt-the-process`](../workflows/adopt-the-process.feature),
at its end**: *the pull request carries what the version leaves behind*. Its
*Where it breaks* already lists *a pull request with nothing in it to look at*.
This is the opposite failure: a pull request with so much in it that the thing
to look at cannot be found.

## The job behind the request

The literal ask: add a rule to *Every pull request shows what it did* saying
that the point comes first, the evidence follows and backs it, each fact is
stated once, no word the session coined appears, and the review request message
follows the same rule. Optionally, add a length check to the pull-request
report.

The job: **somebody deciding on a change can tell what they are deciding, and
where to look, within the first minute of opening it.** Today the method says
what a body must *carry* (the picture, the Gherkin it moved, the run) and
nothing about how it is *read*. An agent following it writes down everything it
checked, and every item is owed or looks owed. In the report from a downstream
adopter, a two-file diff came with about 440 words and its seven-file companion
with about 650. Both carried the same before-and-after block, harness caveats,
a 16-case matrix, lockfile notes, and the limits stated twice. The reviewer put
an hour on understanding the change without an AI's help. They said: *"I
understand less and less the point and meaning of the change… it's hard to
extract the main things I as a human should concentrate my attention on."* The
message asking them to review used a name the agent had coined during the
session (*"the disclosed harness"*), which they had never seen.

**What they do today instead:** read it with an AI's help. That is the outcome
the method exists to prevent. If the review needs an agent, the agent that
wrote the change is effectively checking its own work.

**Is the proposal the best answer?** Mostly. The four points are the right ones,
and they go in the method because every consuming repository's agent writes
pull requests. Two additions:

- **The evidence is not cut.** A rule that says "be short" is read as "drop
  things", and every item it would drop is owed by one of the subsections
  above it. So the rule says where the evidence goes, not that it goes away.
- **The length check is advisory.** It goes in the report, not a gate. See
  *What we are not doing* for why.

## Why now

The three subsections of *Every pull request shows what it did* were each added
by a change that found something missing: the picture, the promise, the run.
Each was right, and together they make the body longer every time. No rule
pulls the other way, and the report from use says the body is now past what a
reviewer can read. This repository is one of the places it happens: recent pull
requests here open with the changelog paragraph and then several screens of
argument.

## The end value

A reviewer opening a pull request reads what changed, why, and where to look,
in the first few lines, and reads the evidence only if they want to check it.
The reviewer is never handed a word they have to ask about.

**How we would know it worked:**

- this pull request's own body opens with three lines and a pointer into the
  diff, and folds the rest;
- the report prints how many words come before a body's first heading, code
  block or folded block, so a body that buries its point shows as a number;
- the next report from a downstream reviewer does not say they could not find
  the change.

## What changes

1. **[`repository.md`](../../method/repository.md), *Every pull request shows
   what it did*, gains a fourth subsection: *And the point, before the
   evidence*.** It says the body is written for the person reading it:
   - **the point comes first**: what changed and why in two or three plain
     lines, then what to look at in the diff;
   - **the evidence comes after and backs the point**: all of it still owed,
     none dropped for length. The picture stays inline under the point. The
     long blocks are folded or linked;
   - **each fact once**: a caveat where it applies and nowhere else; two pull
     requests that belong together link each other instead of copying a block;
   - **in words the reviewer has**: a name the session coined is replaced with
     what it names;
   - **the message asking for review** follows the same rule;
   - **no gate can hold it**, and why: a report that already reads the body
     can count what comes before the evidence and print it, gating on nothing.

   The *Closing an issue* section of the same file is not touched; another
   change in flight edits it.

2. **[`record-clip`](../../skills/record-clip/SKILL.md)** owns step 6 of the
   loop, *opens the pull request with it in the body*. Its rules gain one
   bullet: the body around the picture is written for the reviewer, the four
   points in a line each, with a link to the subsection. Its description does
   not change, so no should-not-fire case is owed.

3. **The report, [`report.py`](../../.github/scripts/report.py)**, gains a
   section, *The opening*: the number of words the body says before its first
   heading, code block or folded block (a heading on the first line titles the
   opening and is skipped). When there are none, it says the body opens
   straight into its evidence. When there is no body, it prints no section.
   It gates on nothing, like the rest of the report. `inject.py`'s report
   control hands it degenerate bodies (empty, only a folded block, an unclosed
   fence, bytes that are not text, a very long one) and checks that each
   still exits zero with something printed.

4. **This repository's bindings**: the *Pull-request report* row names the new
   section, and the *Fault injection* row says the report's control now
   includes bodies.

5. **One eval case, 89**, on fieldnote, tagged `skill:record-clip`. Spec 0012
   is on the branch with its picture already recorded. The notes the session
   kept hold a 40-line run, a 16-row case matrix, three caveats (one written
   twice), a companion pull request in another repository, and a name the
   session coined for its fixture. The prompt asks for the pull request body
   and the message asking for review, written to files because `gh` is not
   signed in there. Graders:
   - an `llm` grader claiming `the-point-comes-before-the-evidence`;
   - an `llm` grader claiming `each-fact-once-in-words-the-reviewer-has`;
   - a `command` grader claiming the first rule: the body's opening, counted
     the way the report counts it, is between one and a hundred and twenty
     words, and the run block is still in the body.

   Case number 90 is left unused.

6. **Tests**: `tests/test_the_opening.py` claims
   `the-report-counts-what-comes-before-the-evidence` by building the report
   over bodies.

**Rules added** — `@planned` in this commit, live in the implementing one:

| Rule id | Feature file | New or changed |
|---|---|---|
| `the-point-comes-before-the-evidence` | [`features/showing/the-point-before-the-evidence.feature`](../features/showing/the-point-before-the-evidence.feature) | new — case 89 |
| `each-fact-once-in-words-the-reviewer-has` | same | new — case 89 |
| `the-report-counts-what-comes-before-the-evidence` | same | new — tests |

## What we are not doing

- **Not gating on length.** A count cannot tell a point from padding. Forty
  words of jargon would pass and a hundred and fifty plain words a change
  genuinely needs would fail, and a refusal on length is met by cutting words,
  not by putting the point first. The method's line for every pull-request
  check is that a gate proves a block is *there* and the reading is review's.
  Where the point is in the body is a reading. The report makes it cheap the
  way it makes the run cheap: a number printed where the reviewer is already
  looking.
- **No threshold in the report.** A threshold would be a binding, and the
  bindings would need a row, `setup` a question and `doctor` a check, all for
  a number nobody has measured. The count is printed bare. If reading it shows
  where the line is, a later change can put it in the bindings.
- **Not wiring the count into consuming repositories.** The method says a
  report *can* count. It does not say every report must, so `setup`, `doctor`,
  `gates.md` and the ledger template are unchanged and the audit surface does
  not move. A consuming repository that wants the count has the method's
  sentence and this repository's report to copy from.
- **Not cutting what is owed.** The picture, the Gherkin block, the run block,
  the `## Ids` section and the changelog all stay required. This spec decides
  where they sit, not whether they are there.
- **Not editing the persona.** The reviewer in the report is a second person,
  and the persona file says contributors *"are expected and have not
  arrived"*. Recording what they need is `refine-personas`' job and needs its
  own confirmation. It is noted in the hand-back, not done here.
- **Not rewriting this repository's own `CLAUDE.md` or `process.md`.** Step 6
  already links *Every pull request shows what it did*, and the new subsection
  sits under it.
- **Not sweeping past pull request bodies.** They are history.

## Data

No storage. Files that move: `method/repository.md`,
`skills/record-clip/SKILL.md`, `.github/scripts/report.py`,
`.github/scripts/inject.py`, `specs/setup/README.md`, one new `.feature`, one
new test file, `evals/89-a-body-that-buries-its-point/`, and this spec.

**This spec commit stales nothing new.** The three rules are `@planned` and no
case or test claims them. `verify.py` exits 2 only for the rows that are already
waiting on `main`.

**The implementing change** edits `record-clip`'s body. That stales its review
row and the first rows of the cases holding it, all of which are already owed
or never measured. Case 89 starts with no rows.

**What the pull request owes.** `method/` and `skills/` move, so it owes one
label, **`minor`** (a changed judgment), and a `## Changelog` section. A
`.feature` moves, so it owes the Gherkin block. `tests/`, `evals/` and
`.github/scripts/` move, so it owes the run block. The audit surface does not
move, so no `## Ids` section is owed.

## Risks

- **Routing.** Case 89 asks for a pull request body once the picture already
  exists. `record-clip`'s description is about recording, so the route tier may
  find that it does not fire. The description is not widened to make it fire:
  that costs every session. A route row that comes back low is the evidence a
  later change would need.
- **The count reads as a target.** A reviewer or agent could treat a low number
  as "good". The report says the number is counted, not judged, and the method
  says why no gate holds it.
- **The heuristic miscounts.** A body that opens with a table, or with a title
  heading, could be counted differently from how a person would read it. The
  count is advisory and printed beside the body it was taken from, so a miscount
  is visible and costs nothing.
- **Always-promises.** `always-green`: the report gains a section and no way to
  fail, and the control proves it on the degenerate bodies. `context-budget`:
  no description moves. `ids-are-permanent`: three rule ids added, none renamed.
  `never-implements`: prose, a script, a case.

## Acceptance checks

1. Read *And the point, before the evidence* in `repository.md`. It names no
   command, file or threshold, and every item the three subsections above
   require is still required.
2. Run `report.py` over this pull request's own body and see *The opening*
   print a count under a hundred and twenty words.
3. Run it over a body that opens with a fenced block, and see it say nothing
   comes before the evidence.
4. `verify.py` exits 2 with only the measurement board waiting. The tests
   claiming the third rule run, and case 89 is held by `evalsuite.py`.
