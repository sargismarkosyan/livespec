# Spec 0020: enough to say yes

- **Status:** proposed
- **Issue:** [#32](https://github.com/sargismarkosyan/livespec/issues/32)

## Who this is for

[`agent-accelerated-owner`](../personas/agent-accelerated-owner.md) — Ren, at the
end of a change rather than the start of one. Several repositories are moving
faster than they can be read, the agent wrote the change, and the one decision
left is whether to merge it. The persona file already says reading is not the
check: *"Checking the result by reading is not available either."* This is that
sentence applied to the last step of the loop.

It sits in [`adopt-the-process`](../workflows/adopt-the-process.feature), at the
end — the sitting writes the binding that decides what a change here has to show,
and the first change after the install is where that binding is spent. **Two of
the three rules will outgrow that tag.** Taking a version through review is one
of the [three attempts not yet interviewed](../workflows/README.md#three-more-attempts-not-written-yet),
and `the-form-follows-what-changed` and `what-is-shown-answers-the-request`
belong to it. A feature may serve two workflows; when that attempt is cut, this
file gains its tag. Tagging it today with a workflow that does not exist is the
alternative, and the gate is right to refuse it.

## The job behind the request

Somebody has to decide whether a change is the one they asked for, and the only
things they will actually open are the request and whatever the pull request puts
in front of them. Not the diff, not the branch, not the app. **The job is to be
able to say yes or no from those two things alone.**

The literal ask was different, and larger: every workflow carries a `.tape` and a
recorded `.gif`, kept in lockstep with the workflow, with a gate failing any
workflow that has no tape. That was reported from a repository where it is being
built concretely, and it is the right thing *there*. It is not what livespec
should carry, for a reason the reporter gave when asked: **the tape is that
project's.** What generalises is not the recorder — it is what the artefact has
to be good enough for.

Two things fall out of that once the tape is set aside:

- **The form is not the point, and the method currently thinks it is.**
  [`repository.md`](../../method/repository.md) says *"One animated GIF per
  version"* and `record-clip` says *"**No PNGs.** A frozen frame is not a
  deliverable here."* For a change whose entire result is one static screen, that
  rule buys nothing and costs a recording session — the reviewer's question is
  answered by the frame.
- **The audience was never written down.** The method says what to record and
  where to put it; it never says who has to be able to read it, or what they are
  holding when they do.

## Why now

Three things are going wrong today, and the third is the expensive one.

**A static change pays for an animation.** Every version, in every repository
that adopted this, whatever the change was. The cost is a recording session and a
GIF in git forever for something a single frame said better.

**Nothing says what the artefact has to be sufficient for.** `record-clip` takes
its shot list from the change spec's *What changes* — the section describing what
was built. So the picture drifts toward showing the implementation, and the
person holding the issue is not who it was composed for. It is the same defect
[`0014`](0014-the-reader-the-method-assumes.md) found in the method's prose,
one layer further on: an artefact produced for a reader nobody named.

**And the check is a habit rather than a binding.** Whether a pull request owes
something to look at is decided per change, by whoever is writing it, with
nothing written down. [`setup`](../../skills/setup/SKILL.md) section 5 already
calls this row *"easy to leave out and expensive to add later"* — it currently
asks for where the recording goes and which paths make the Gherkin owed, and
stops short of the one thing a pipeline could read: which changes owe an artefact
at all.

## The end value

Ren opens a pull request they have not read the diff of, next to the issue they
filed, and can tell whether the thing they asked for arrived — without checking
the branch out, and without a session spent animating a screen that does not
move.

**How we would know it worked:** a change whose result is static ships with a
still and no recording session, and nobody asks for a GIF. And the reverse, which
is the one that matters: a pull request whose artefact does not answer the
request gets sent back for that reason, rather than merged because there was a
picture in the body.

## What changes

- **`method/repository.md` — the section *Every pull request carries a moving
  picture* is rewritten and renamed.** It becomes *Every pull request shows what
  it did*. The unit does not move: **one artefact per version**, on the branch,
  before the pull request is opened, embedded by a permanent URL pinned to the
  commit. What moves is the form and the standard:

  - a change that is something *happening* is recorded moving — a still drops
    exactly the half that carries;
  - a change whose whole result is a static screen is a still, and is not padded
    into an animation to satisfy a format;
  - a change with nothing to see says so in a line. That exemption already
    exists and keeps its wording, including *"it is hard to record"* is not it;
  - and the standard the artefact is held to, which is new: **somebody holding
    the request and this one artefact can say whether it was delivered.** Not
    the diff, not the branch.

- **`record-clip` chooses the form before it records, and composes against the
  request.** Two edits to the skill body: the opening claim (*"Produces one
  looping GIF"*, *"No PNGs"*) becomes the choice, with the animation as the
  default and the still as the case that has to be true rather than convenient;
  and *What to record* names the reader — the shot list still starts at the
  change spec, but what goes on screen is what was asked for, in a state where
  somebody who only read the request can tell.

  **The description is rewritten and must not grow.** It currently asserts the
  artefact is *"the animated GIF"* and offers *"to show a change moving rather
  than frozen"* as a trigger, and both are now false. No trigger word is added —
  *screenshot* and *capture* are already in it — so nothing widens and no
  should-not-fire case is owed. Always-on cost is 3800 of 5000; the replacement
  lands at or under that, and `checks.py` is the arbiter.

- **`skills/setup/SKILL.md` section 5 — the deliverable row gains the two
  missing halves.** It already asks whether there is anything to record and where
  it goes; it now also asks **which changes owe one** and **in what form**, so
  that the answer is a binding a pipeline can read rather than a judgment made
  again every version. A repository with no screen writes that down as the
  standing case, which is what this repository's own bindings already do.

- **`method/process.md` follows.** *"The deliverable is a series of moving
  pictures"* and step 6's *"one animated GIF of the change"* are the same claim
  in the document that describes the loop, and a prose spec contradicting a live
  feature file is worse than one that says nothing.

- **Three anchor links move with the heading** — `skills/setup/SKILL.md`,
  `method/process.md`, `specs/setup/README.md`. `specs/changes/0008` also points
  at the old anchor and is **left alone**: change specs are the record of a
  decision at a time and are not maintained afterwards.

- **This repository's own bindings say why none of it applies here.** *What does
  not apply* already exempts `record-clip` and `docs/screenshots/`; it gains the
  form sentence, so the exemption reads as a decision about a repository with no
  screen rather than as an omission.

**Rules added or changed** — the `@rule:` ids in `specs/features/`:

| Rule id | Feature file | New or changed |
|---|---|---|
| `the-form-follows-what-changed` | `features/showing/what-a-change-shows.feature` | new |
| `what-is-shown-answers-the-request` | `features/showing/what-a-change-shows.feature` | new |
| `the-bindings-say-what-a-change-here-must-show` | `features/showing/what-a-change-shows.feature` | new |

All three are `@planned` and the file is committed with this spec. `showing/` is
a new area and is deliberately not `report/`: that one holds the report the
pipeline posts, which never gates and is generated; this is an artefact a person
composes and a pull request owes.

**Ledger:** nothing moves. No new gate — see *What we are not doing*.

**Two eval cases are owed by the implementation**, one per subject: a recording
case that holds the first two rules, and a sitting case that holds the third.
Neither can be written here, and **neither can be run without the maintainer** —
comparable rows on the board cost $0.16–$0.24 each. The commit and the pull
request can be finished with a gap where the numbers go.

## What we are not doing

- **No `.tape`, and no per-workflow artefact.** Set aside on the reporter's own
  answer — the tape is that project's. There is a second reason worth writing
  down so this is not proposed again from the other direction: a picture kept in
  the tree *claims to be current*, and
  [`gates.md`](../../method/gates.md#the-same-loop-one-layer-up) already refuses
  two checks of exactly that shape, because CI that checks out a single commit
  answers them with silence. A per-version artefact is a record of a moment and
  cannot go stale; a per-workflow one can, and nothing here could catch it.
- **No `e2e:workflows:check` and no new row on the gates page.** The presence
  half of what was asked for already exists one layer up: `workflow → test` fails
  a workflow nothing walks. A second check over the same workflows, satisfied by
  a script with no assertions in it, is the copy that rots first while looking
  authoritative. What a pull request body has to carry is a **binding** in this
  method, not a gate — that is where the Gherkin block is held in this
  repository, and it is where *"enforce the artefact"* lands.
- **Not the embed host.** The method pins a `raw.githubusercontent.com` URL and
  the original report wanted GitLab's `/uploads`. Left out on the reporter's
  answer: *"that depends on repo infra, so this is not this repo's concern."*
  The portable half — permanent, pinned to the commit, not a branch URL — is
  already in the method and does not move. Filed against
  [#32](https://github.com/sargismarkosyan/livespec/issues/32) when it closes, so
  the GitHub-shaped URL is a known gap rather than a forgotten one.
- **Not moving `docs/screenshots/`,** and not renaming it for a directory that
  now also holds stills. The path is in every adopting repository already, and
  renaming it buys a better word for the cost of a migration nobody asked for.
- **Not touching the Gherkin block.** It shipped in 0.10.0 and is the other half
  of what a pull request carries; this change does not renegotiate it.

## Data

No storage contract. What moves is *what a version leaves behind*, which
[`spec.md`](../spec.md) names — and it moves in the method rather than here: this
repository's own answer is unchanged, because there is no app to record and its
deliverable stays the pull request description. Nothing already recorded in any
adopting repository is invalidated; a `docs/screenshots/` full of GIFs stays
correct, and the change is about what the next one may be.

## Risks

**`context-budget`, and it is the one to watch.** `record-clip`'s description is
the always-on field, paid by every session of every user whether or not the skill
fires. This change rewrites it while removing a claim, which should end level or
shorter; if the replacement is longer, it is a widening and owes a should-not-fire
case in `evals/` rather than a hunch. `checks.py` decides, not the author.

**The still becomes the default by drift.** A rule that permits a frame will be
read as permitting one whenever recording is inconvenient, which is the exact
excuse the method already names and refuses. The Gherkin holds the boundary with
its own example rather than trusting the prose, and the phrasing puts the burden
the right way round: the still is what has to be *true*, not what is available.

**`never-implements` is unaffected.** `record-clip` still records and never
changes the app — [`08-fix-it-while-recording`](../../evals/08-fix-it-while-recording/prompt.md)
holds that, and this change must not disturb it. If the edited skill body moves
that case's score, the body is what is wrong.

**And it ships unexercised here.** livespec has no screen, so no version of this
repository will ever produce an artefact under the new rule. That is the first
thing in the method with that property, and it is stated in the bindings rather
than discovered later from a green run.

## Acceptance checks

1. `python3 .github/scripts/verify.py` is green with the three rules live and
   claimed.
2. `python3 .github/scripts/checks.py` reports an always-on cost no higher than
   3800.
3. Read `method/repository.md` and `skills/record-clip/SKILL.md` back to back:
   neither says a still is forbidden, both say what decides the form, and the
   audience sentence appears once rather than in both.
4. Every anchor pointing at the renamed section resolves to it — the three live
   references, not `specs/changes/0008`.
5. Ask a session to record a version whose whole change is one static screen, in
   a repository with an app. It produces a still and does not open a recording
   session.
