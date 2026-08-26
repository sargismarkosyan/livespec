# The process

## What this is for

**The code is the source of truth. The spec is where the context lives.** Every
change starts as a written spec, gets implemented in one small step, and is
captured as one commit — not so the spec can generate the code, but so the
reasoning that produced the code is still readable in six months, when the diff
has long since stopped explaining itself.

The deliverable is a **series of pictures** — one per version — showing the
product evolving change by change. That is why every commit must leave the app in
a state worth looking at.

## Who does what

**The human uses the app.** They run it, test it, break it, and say what they
found. They approve specs. They do not write code, issues, or specs by hand.

**The AI writes everything else.** Issues, specs, code, tests.

That split is the point. It is also why the written artefacts have to be good:
they are the only channel between the person who knows what is wrong and the
thing that fixes it.

## The loop

1. **Human tests and reports.** In Claude chat, in their own words, with
   screenshots. Not in the app, not as a written issue.
2. **AI files issues** using the [`feedback`](../skills/feedback/SKILL.md) skill. It takes
   the report apart into distinct insights, investigates the code to find what is
   actually happening, and files researched GitHub issues. It does not fix.
3. **AI writes the spec** using the [`refine-spec`](../skills/refine-spec/SKILL.md) skill.
   It digs out the job behind the request, checks it against the persona and
   workflows, and writes Gherkin rules tagged `@planned` plus a numbered change
   spec. It does not implement.
4. **Human approves** the spec, or asks for changes.
5. **AI implements.** Removes the `@planned` tags, writes the tests referencing
   those rules, gets the repository's verification green, commits.
6. **AI records the version** using the [`record-clip`](../skills/record-clip/SKILL.md) skill — one
   picture of the change, on the branch — and opens the pull request with it in
   the body.
7. **Human merges**, and uses the new version.
8. **AI closes the issue**, with a comment saying what was asked, what shipped,
   and why they differ. Back to 1.

Steps 2 and 3 are separate on purpose. Filing and specifying are different jobs
and get done badly when merged — filing wants breadth and evidence, specifying
wants focus and a decision.

**Step 6 belongs to the AI, not the human.** The picture is recorded from the
change spec's own shot list, in whichever form the change earns, and composed so
that somebody holding only the request can tell whether they got it — see
[repository.md](repository.md#every-pull-request-shows-what-it-did). The human
still *uses* the version, which is step 7 and where the next round of feedback
comes from; what they never do is produce the deliverable by hand.

## The rules

- **One change spec = one step = one version.** Unrelated changes do not travel
  together, however small.
- **Spec before code.** No implementation without an approved change spec, and no
  change spec without `refine-spec` first. A request is not a spec.
- **A change to `specs/workflows/` or `specs/personas/` is confirmed on its own.** Those
  two files say what the product is and who it is for, and every other layer in
  `specs/` is downstream of them. **The reason this needs a rule is that such an
  edit never arrives on its own** — it rides inside a spec nominally about a
  button, where a single "approved" silently covers both, and the largest half
  is the half nobody was looking at. So it does not travel with the spec's
  approval: show that diff by itself, say in one line what it changes about who
  this is for or what they do, and get it confirmed *before* asking for approval
  of the spec. **If only one thing is reviewed in a round, it is this one.**
- **Feedback is never fixed on the spot.** It becomes an issue, then a spec, then
  a commit. Fixing something the moment it is mentioned is the fastest way to
  lose the record of why it changed.
- **No silent scope growth.** Found something else broken while working? File it
  as its own issue. Do not fix it inline.
- **Every version must run and be green.** Each commit is a screenshot candidate
  and must pass whatever `specs/setup/README.md` names as verification.
- **Specs commit separately from implementations.** `spec 0004: <title>` lands
  first and is approved; the implementation follows in its own commit.
- **An issue is closed when its job is answered, not when its request is built.**
  The two are often different — a request is one proposed shape for a job, and
  `refine-spec` exists to tell them apart. Comment what was asked, what shipped,
  and why they differ; then close. Anything dropped goes in that comment, and
  gets a fresh issue if it is still wanted. See
  [repository.md](repository.md#closing-an-issue-by-hand).

## Versions

A version number is a change spec number. "Version 3" is the state of the repo
after spec `0003` shipped. Version 0 is the scaffold — process machinery, no app.

There are no semver tags and no releases. `git log` is the version history, and
`docs/screenshots/` is its visual counterpart.

## When the process gets in the way

It sometimes will — a one-word typo fix does not need a persona analysis. The
judgment call is whether the change alters **behaviour someone could notice**. If
it does, it needs a spec, however small it looks. If it does not (a comment, a
stale path in a doc, a broken link), fix it and say so.

### A technical change that serves no workflow is correct, not a gap

Written down because the gates make the absence visible, and an absence nobody
explained reads as an escape hatch being used.

A change can be real, necessary, argued for in a numbered spec — and serve no
workflow, add no feature file, and touch neither the personas nor the workflows.
That is not the process being dodged. It is the honest shape of a change whose
whole requirement is that **nothing a person can see moves**.

**The worked example is a framework migration** — [spec 0016 in the reference
repository](https://github.com/sargismarkosyan/todo-change/blob/main/specs/changes/0016-somebody-elses-frame.md). It was
taken for the organisation that owns the code, not for the person using the app.
Its spec says so in its first paragraph and spends its length arguing the trade
in the open, and every workflow came out the far side with exactly the shape it
went in with — which was the requirement.

What such a change still owes:

- **A numbered change spec.** *Who this is for* says **not the persona**, out loud, and
  argues for whoever it is for instead.
- **An acceptance check proportional to the risk.** A rewrite that changes
  nothing visible is the one kind of change where "it looks fine" and "it is
  fine" are indistinguishable, so it buys a walkthrough of every workflow.
- **Silence in the gates, not an exemption from them.** Verification is green
  the ordinary way. No feature is retagged to make a number look better.

What it does **not** owe is an invented workflow to sit in. Filing a framework
migration under whichever workflow was nearest, because the template asked for
one, is the
failure this paragraph exists to prevent — one bad tag is worse than an honest
blank, because the gate cannot tell them apart and the map is what goes stale.

When unsure, write the spec. The cost of an unnecessary small spec is a few
minutes. The cost of undocumented behaviour change is that the series stops
explaining itself.

### A step you cannot take here is said once, not searched for

The repository in front of you is usually not fully set up. The tool a step needs
is not installed, the file it was told to read was never written, the path in
somebody's report points at nothing. That is the ordinary condition rather than
the exception, and it has a failure mode of its own: the session goes into
looking for the missing thing and ends with the whole budget spent and nothing
written down.

**Say it once, and hand over the rest.** Two halves, and the second is the one
that gets dropped:

- **Name what is not there, in a line, where the person will see it.** Not after
  a search — instead of one. Looking twice for a file nobody ever wrote is not
  diligence; it is the same answer bought twice.
- **Finish everything that did not depend on it.** A step that cannot be taken
  here does not take the work before it down with it. What was investigated is
  still worth writing out, and what could not be run is still worth handing over
  as the exact thing to run. Somebody holding that finishes in a minute.
  Somebody handed an empty session finishes not at all.

**Stopping is not the same as handing over**, and an instruction to stop that
does not say what to hand over will be read as permission to stop with nothing.
Where a step is genuinely impossible — there is nowhere to file it, there is
nothing to record it in — that is a result, not a dead end. Report it with the
work attached.

**This is not a licence to investigate less.** Looking for the *cause* of what
somebody reported is the most valuable thing any of these skills does, and it
ends when it has an answer. What this rules out is looking for a *way to perform
a step that is not available here*, which ends when the session does.

### A workaround names what would end it

The section above is about a step that cannot be taken here at all. This one is
about what usually happens next: the work goes **around** it and carries on. The
gap gets filed where it can be fixed for everyone, and the local way of doing it
stays so that nothing stops. Both halves are right. Together they leave the
repository carrying something whose reason may already be gone.

**Nobody in that arrangement can close it.** The filed gap cannot know which
repositories worked around it — nothing records that. The local way of doing it
cannot know when the fix shipped; it is a file here and the fix is somewhere
else. And the thing that did not fit cannot go looking for its own past
inadequacies. Every party behaves correctly and the join still does not exist,
which makes this structural rather than somebody's oversight — and structural
gaps are closed by writing the join down, not by trying harder.

**Record it where this repository's own facts already live** — the bindings,
beside the other dated tables of what is true here. One row per workaround,
carrying four things:

- **what is done here instead**, in enough detail to recognise a year later;
- **the gap it goes around**;
- **where that gap is filed**, so it can be looked at rather than remembered;
- **what would end it** — the arrival that makes the workaround removable.

A row that cannot name the last of those is describing a **decision** rather than
a workaround. Decisions do not expire, and filing one here is how the table turns
into a list of everything anybody is unhappy about, which is a second thing to
maintain and the opposite of the point.

**A recorded workaround is never followed silently.** A row read only by the
person who wrote it has not closed anything. So a session standing on a
workaround says so, once, and says what would end it — and where it is already at
the place that would answer that, it says whether the answer has arrived. Not a
poll, and not a background job: a check that runs when nobody is in the room
produces an answer nobody reads.

**The row comes out when the workaround does.** A record that outlives what it
describes is the same failure one level up, and worse, because it reads as
current to everybody who was not there.
