# The process

Every rule on this page follows from one of the six principles in
[README.md](README.md#six-principles). Each section names the principle it
comes from. A rule that follows from none of them does not belong here.

## Who does what

**The person uses the product and decides.** They run it, break it, say what
they found, and approve specs. They do not write code, issues or specs.

**The agent writes everything else**: issues, specs, code, tests. Because the
written artefacts are the only channel between the person who knows what is
wrong and the agent that fixes it, they have to be good.

The deliverable of a version is a **picture** of the product being used — one
per version, so the series shows the product changing step by step. Every
commit must therefore leave the product in a state worth looking at.

## The loop

1. **The person uses the product and reports** what they found, in their own
   words, with screenshots.
2. **The agent files issues** with [`todo`](../skills/todo/SKILL.md): it takes the
   report apart into distinct findings, investigates the code, and files each
   one with its evidence. It does not fix.
3. **The agent writes the spec** with [`refine-spec`](../skills/refine-spec/SKILL.md):
   the job behind the request, checked against the persona and the workflows,
   as Gherkin rules tagged `@planned` and a dated change spec. It does not
   implement.
4. **The person approves** the spec, holding the spec and the sketch drawn
   from it, or asks for changes.
5. **The agent implements** the smallest change that makes the rules true:
   removes the `@planned` tags, writes the tests that claim them, deletes what
   the change made dead, gets verification green, commits.
6. **The agent records the version** with [`record-clip`](../skills/record-clip/SKILL.md)
   and opens the pull request with the picture in it, reading back what it will
   close ([repository.md](repository.md#closing-an-issue)).
7. **The person merges** and uses the new version.
8. **The agent closes the issue**: what was asked, what shipped, and why they
   differ. Back to 1.

Filing (2) and specifying (3) are separate steps because they are different
jobs: filing wants breadth and evidence, specifying wants focus and a decision.
The picture (6) is the agent's, recorded from the spec's shot list so that
somebody holding only the request can tell whether they got it; the person
*uses* the version, at 7, which is where the next round of feedback comes from.

## The rules

### The code is the truth; the spec carries what the code cannot say

- **A spec is context, not a generator.** It records who the change is for, the
  job behind it, and what was dropped, so the reasoning is still readable when
  the diff no longer explains itself. The code says what is true.
- **A version is a change spec.** "Version 3" is the product after spec `0003`
  shipped; version 0 is the scaffold. `git log` is the history and the pictures
  are its visual counterpart.

### One change, decided before it is built

- **One change spec = one step = one version.** Unrelated changes do not travel
  together, however small.
- **Spec before code.** No implementation without an approved change spec, and
  no change spec without `refine-spec`. A request is not a spec.
- **Specs commit before their implementation.** `spec 2026-03-14-<slug>: <title>` lands
  first; the implementation follows in its own commit.
- **A change to who the product is for, or what they do, is confirmed on its
  own.** An edit to the personas or the workflows rides inside a spec about
  something else, and one "approved" then covers both. Show that diff by
  itself, say in one line what it changes, and get it confirmed before the spec
  is approved. If only one thing is reviewed in a round, it is this one.
- **A reading is played back before anything is written.** A skill that
  interviews somebody draws a conclusion from their answers; it says that
  conclusion back as a paragraph and waits until it is confirmed or corrected.
  The diff shown at the end does not replace it: a diff is a decision already
  taken, and a reading can still be argued with.
- **The decision gets the evidence it rests on.** Approval is the one step where
  somebody decides on something that does not exist yet. The spec carries the
  argument; a **sketch** drawn from it carries what the argument is about — what
  is there now beside what would be, what moves and what stays. It is evidence,
  never a second copy of the spec's argument. Where prose already carries all
  of it, where no sketch can be produced in this session, or where approval came
  before the spec, the spec's header says so in a line. The sketch (step 4) is
  drawn from the spec; the picture (step 6) is recorded from the product. The
  bindings say which changes owe each — a repository with nothing on a screen
  owes no picture and still owes sketches.
- **Feedback is never fixed on the spot.** It becomes an issue, then a spec,
  then a commit. A fix to the pipeline that changes no promise and ships nothing
  takes a lighter path — the issue, and a line in its pull request saying why no
  spec was owed — never a shorter one: the issue still comes first.
- **An issue is closed when its job is answered,** not when its request is
  built. The closing comment says what was asked, what shipped and why they
  differ; anything dropped gets a fresh issue if it is still wanted
  ([repository.md](repository.md#closing-an-issue-by-hand)).

### Every promise is checked by something that can fail

- **Every version runs and is green** — whatever the bindings name as
  verification.
- **Every merged change is read back** for the path it took: a spec, or the
  pipeline fix's line saying why none was owed.

### One copy of anything

- **Less is the default.** Reuse what is there before writing anything, and add
  nothing no rule asks for — no option, no layer, no second copy.
- **Whatever only grows has a ceiling.** The code, the rules, what every session
  loads: the bindings name a size for each, written from what it is when the
  ceiling is set. It is lowered when the part shrinks and raised only in the
  change that needs the room, with the reason beside the number, so growth is a
  line in a diff. The context file's ceiling ([claude-md.md](claude-md.md#length))
  is the first of them.

### Delete what stops being true

- **What a change makes dead goes in that change** — code, tests, rules, files —
  and its spec names each under *What this removes*. Anything else found broken
  or dead on the way is filed as its own issue. A change whose whole value is
  less is a change like any other.
- **A record comes out when the thing it describes does.** A row, a rule or a
  paragraph that outlives its subject reads as current to everybody who was not
  there.

## When the process gets in the way

A one-word typo needs no persona analysis. The test is whether the change alters
**behaviour someone could notice**: if it does, it needs a spec however small;
if it does not — a comment, a stale path, a broken link — fix it and say so.
When unsure, write the spec: an unnecessary small spec costs minutes, an
unrecorded behaviour change costs the series its explanation.

### A technical change that serves no workflow is correct, not a gap

A change can be real, necessary and specced, and still serve no workflow, add
no feature and touch no persona — a framework migration taken for the
organisation that owns the code, not for the person using it
([spec 0016 in the reference repository](https://github.com/sargismarkosyan/todo-change/blob/main/specs/changes/0016-somebody-elses-frame.md)).
Its whole requirement is that **nothing a person can see moves**. It still owes:

- **a change spec** whose *Who this is for* says *not the persona*, out
  loud, and argues for whoever it is for;
- **an acceptance check proportional to the risk** — here, a walkthrough of
  every workflow, because "it looks fine" and "it is fine" look the same;
- **green gates the ordinary way**, with no feature retagged to improve a
  number.

It does **not** owe an invented workflow. A tag picked because the template
asked for one is worse than an honest blank: the gate cannot tell them apart,
and the map goes stale.

### A step you cannot take here is said once, not searched for

*From: say what you cannot do; do not search for it.*

A repository is usually not fully set up: a tool is not installed, a file was
never written, a path points at nothing. The failure is a session that spends
its whole budget looking for the missing thing and hands over nothing.

- **Name what is not there, in one line, where the person will see it** —
  instead of a search, not after one.
- **Finish everything that did not depend on it**, and hand over what could not
  run as the exact thing to run. Stopping is not handing over; where a step is
  impossible, that is a result, reported with the work attached.

This is not a licence to investigate less: looking for the *cause* of what
somebody reported ends when it has an answer. What it rules out is looking for
a *way to perform a step that is not available here*.

A boundary no test can reach is the same case one layer down: its row in the
bindings reads *unreachable*, with why, and a change touching it says so where
it is decided — never a stand-in written to get past it.

### A workaround names what would end it

When a step cannot be taken, the work often goes around it: the gap is filed
where it can be fixed for everyone, and a local way of doing it keeps the work
moving. Nobody in that arrangement can later tell when the workaround stopped
being needed, so the join is written down.

**One row in the bindings per workaround**, with four things: what is done here
instead; the gap it goes around; where that gap is filed; and what would end it.
A row that cannot name the last is a **decision**, not a workaround, and does not
belong in that table.

**A workaround is never followed silently.** A session standing on one says so
once, with what would end it, and — where it is already at the place that would
answer that — whether the answer has arrived. Not a poll, and not a background
job. **The row comes out when the workaround does.**
