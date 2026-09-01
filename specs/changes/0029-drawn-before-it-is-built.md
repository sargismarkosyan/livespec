# Spec 0029: drawn before it is built

- **Status:** approved
- **Issue:** [#78](https://github.com/sargismarkosyan/livespec/issues/78)
- **Depends on:** nothing. It sits beside
  [`0020`](0020-enough-to-say-yes.md), which made the picture's form follow the
  change, and does for step 4 what that did for step 6.

## Who this is for

[`agent-accelerated-owner`](../personas/agent-accelerated-owner.md), in
[`adopt-the-process`](../workflows/adopt-the-process.feature) — at the single
step of that attempt where the person, rather than the agent, has to produce
something. Everything else in the loop is executed for them; step 4 is decided
by them.

The persona line this turns on is not the one about not reading. They **do**
read the spec layer — "I mostly read spec files, most important is workflow and
journeys and persona" — and a change spec is the spec layer. The line that bites
is the first one in the file: *more to do than there are hours, across more than
one repository at once.* An approval gate held by somebody in that position
either gets fast enough to be real or gets waved through, and prose is the only
thing currently offered to make it fast.

## The job behind the request

Take in the shape of a proposed change — what it would do to the thing as it
stands, what moves and what does not — quickly enough that saying yes is a
decision rather than a formality.

## Why now

Because it has already been worked around, by hand, in the sitting that raised
it.

Running `refine-spec` in `toil-tracker` for its spec 0035 on 2026-09-01, the
owner wrote the page themselves **after** the skill had handed back. What they
drew was the setup form twice — the state it opens in today beside the state it
would open in — with the four controls re-picked every fortnight numbered on one
side and ticked on the other, and a row per setting saying carried / never and
why. Their words afterwards:

> I really like this artifact formated explanation of what is going to be fixed
> […] it would be awesome that everytime it would also contain an artifact so
> that I can quickly scan and understand what would be changed.

None of that was in the change spec's headings, and all of it was derivable from
the spec. It took seconds to read and was spread across four sections of a
230-line file. A workaround performed by hand, once, on the highest-leverage
step in the method, is the strongest signal this repository gets short of a
measurement.

**The asymmetry is the argument, not the anecdote.** Every artefact-producing
step of the loop hands back prose except step 6, which hands back a picture —
and step 6 is downstream of the decision. `record-clip`'s own reason for
existing is that prose is not enough to judge a change by; that argument is
strictly stronger at step 4, where the change has not been built and prose is
not merely insufficient but the *only* thing available.

## The end value

At the one step they hold, they are handed the evidence the spec argues from —
what it is now beside what it would be, what moves and what stays and why —
rather than the argument alone. The spec stays the thing approved; what changes
is that the decision no longer has to be reconstructed from it under time
pressure.

**How we would know it worked:** nobody writes the page by hand after the
hand-back again. That is the exact behaviour observed on 2026-09-01 and it is
directly checkable — the next `refine-spec` sitting in a repository with a
before-and-after either arrives with the sketch or gets one drawn afterwards.
The deeper signal, slower to see: a spec sent back for changes on something
visible in the sketch and not visible in the prose.

## What changes

- **`refine-spec` draws a sketch and hands it over with the spec**, in §7,
  between *Hand back a link, not a summary* and *Ask for approval in one plain
  line* — before approval is asked for, never after it is due.
- **What goes in it is the evidence, and only the evidence.** What it is now
  beside what it would be; what moves and what stays with a reason against each;
  a count that changed. It links to the change spec for the reasoning and
  restates none of *Who this is for*, *The job behind the request*, *Why now* or
  *The end value*.
- **It is drawn from the spec, not guessed at.** Where the spec does not
  establish the state a change starts from, that state is not drawn. Invented
  evidence in a document whose whole purpose is to be evidence is worse than no
  document.
- **Where there is nothing the prose cannot carry, that is one line** and
  nothing is produced — the same shape as the *nothing to see* exemption at
  step 6, and "it would be awkward to lay out" is not it there either.
- **`method/process.md` gains the portable half**: step 4 of the loop, and the
  rule that the decision a person is asked to make is given the evidence it
  rests on. It names no tool and no format.
- **`specs/spec.md` gains one word — sketch.** Drawn from a spec, at step 4;
  a **picture** is recorded from an app, at step 6. Two objects, two steps, and
  they were one word away from being confused for each other.

**Rules added or changed** — the `@rule:` ids in `specs/features/`:

| Rule id | Feature file | New or changed | Ships |
|---|---|---|---|
| `the-decision-gets-what-the-prose-cannot-carry` | `features/showing/before-it-is-built.feature` | new | `@planned` — see below |
| `what-is-shown-is-not-the-spec-again` | `features/showing/before-it-is-built.feature` | new | `@planned` — see below |
| `an-absent-sketch-is-said-rather-than-filled` | `features/showing/before-it-is-built.feature` | new | live, claimed by [`29-nowhere-to-draw-it`](../../evals/29-nowhere-to-draw-it/prompt.md) |

A new file rather than three rules added to
[`what-a-change-shows`](../features/showing/what-a-change-shows.feature): that
one is about what a **version** puts in front of somebody deciding whether to
merge, and this is about what a **change spec** puts in front of somebody
deciding whether to build. Same area, different object, and merging them would
take that file to five rules and past its line limit.

### What no case reaches, and how that was established

**Found during implementation, after this spec was approved, and it changed what
two of the three rules ship as.** Recorded here rather than quietly absorbed.

The suite drives `claude -p`. Asked on **2026-09-01** what tools it has —
`claude -p "List the exact names of every tool available to you, one per line,
no commentary." --model haiku` — a headless session answered with 40 of them and
**no way to render a page** among them. Not a permission the runner withholds:
the tool is not in the session at all, so `--allow-tools` cannot grant it and no
arm of an ablation can watch a sketch being drawn.

So the two rules about what a sketch *contains* ship `@planned`, and
`@planned` here carries the meaning
[`setup-demonstration`](../features/setup/demonstration.feature) already
established in this repository: **nothing can hold it yet**, not *nobody built
it*. The instruction ships in §7 and does the work; what is missing is an arm
that can see the result. Softening the Examples until a session with no such
tool could pass them would buy the tag with the dishonesty
[`evals/README.md`](../../evals/README.md) warns about.

What **is** watchable is the absence, and that is the third rule — a headless
session is not a contrived fixture for it, it is the ordinary case. So
`an-absent-sketch-is-said-rather-than-filled` gained an example for *nowhere to
draw it*, went live, and is claimed by
[`29-nowhere-to-draw-it`](../../evals/29-nowhere-to-draw-it/prompt.md). That case
also holds the constraint from the other side: pasting a summary or a mock-up in
the sketch's place is a fail, which is the failure mode this whole change is
built to avoid, caught in the one session shape a case can actually run.

**Two of three rules unheld is the honest count and it is written down**, in the
feature file beside each rule and in
[the bindings](../setup/README.md#what-has-no-gate-and-what-that-misses). The
tag says planned; whether a sketch carries evidence or decoration is watched by
the person reading it and by nobody here.

### The objection this has to answer, because §7 already raises it

The hand-back section rules out this shape in as many words:

> Persona, workflow, end value and scope are all *in* the spec under their own
> headings. Repeating them in chat gives the reader two versions to reconcile,
> and the one in the terminal is the one that goes stale.

That rule is right and a naive sketch violates it. Two things make this a
different object rather than an exception to it, and both are written as
constraints above rather than assumed:

1. **It has an address.** A revision replaces what the person was already shown,
   at the same place. A chat summary can only be re-typed further down the
   scrollback, which is precisely why the terminal copy is the one that rots —
   `what-is-shown-is-not-the-spec-again` carries this as its third example.
2. **It carries evidence, not argument.** The four headings stay in the spec and
   appear nowhere in the sketch. Without that line this is a decorated summary
   and §7 was right to forbid it.

### The portability question, and where it was already answered

The issue asks the spec to settle what happens where the session cannot render a
page — and the method settled it before this change existed.
[`an-unreachable-step-is-said-not-searched-for`](../features/reach/absent-means.feature)
already promises that *what a step needs and cannot get here is said once,
rather than searched for until the session is spent*, and
[`process.md`](../../method/process.md) carries the same rule as prose. A host
with no way to publish a page is that rule's ordinary case. So the fallback is
governed, and the skill body implements two live rules rather than one new one.

**No example is added to that rule to say so.** The promise does not change, and
editing the rule's text would stale
[`20-repository-with-no-bindings`](../../evals/20-repository-with-no-bindings/prompt.md),
which claims it — a run somebody pays for, bought for a clarification that
changes no behaviour. It is named here instead.

**It is worth noticing what kind of condition this is.** The bindings answer
*what is true of this repository*; this one is *what is true of this session*,
and it varies by host rather than by repository. livespec has no layer for that
and does not need one — the skill asks at the moment it needs the answer, and
says so in a line when it is no. A binding for it would be a claim about
somebody else's terminal.

### That this binds here too, and what that costs

The trigger is *evidence the prose cannot carry at a glance* rather than *a
screen with a before and an after*, which means this repository owes sketches on
its own specs. [`0028`](0028-below-the-floor.md) is the worked example: its
before/after table of the board — 28 measured becoming 5, 23 below the floor,
the mean moving up — is exactly this, and it was already drawn in prose because
the spec could not be understood without it.

That is the deliberate choice and not an oversight. A rule this repository
exempted itself from on its first version is one nobody here would ever notice
breaking, and `record-clip` already has that standing exemption for the honest
reason that there is no app. There is no app here; there is still a change spec.

## What we are not doing

- **The other three `refine-*` skills.** Ruled on: `refine-spec` only. Their
  artefacts' evidence *is* prose — a persona's paragraph as it now reads, a
  workflow's trigger and end state — and §7 in each already says to show the
  diff, which a terminal does well. The workflows README's own trade applies: a
  step added is paid forever, and this one is paid on one sitting's evidence.
  Each gets its own change if the same complaint arrives against it.
- **Linking the sketch from the change spec.** The spec is the record and stays
  the only record. A link to a page the next reader may not be able to open is a
  dangling reference, and it inverts the direction — the sketch points at the
  spec, never the reverse.
- **Putting it in the pull request body.** That body already owes one picture,
  and a second artefact there is a second thing to keep true. This one belongs
  to a decision that happens before the branch exists.
- **A ninth skill.** The always-on budget is 4315 of 5000 characters across
  eight descriptions, and a new one spends several hundred of what is left on a
  step that only ever happens inside `refine-spec`. Body text costs nothing
  until the skill fires.
- **A template for what the sketch contains.** The rules state the constraint;
  they do not enumerate sections. A list of headings is filled in rather than
  drawn, which is the failure mode this change exists to avoid.
- **Making it a gate.** Nothing can check whether a sketch carried evidence or
  decoration, and a gate that can only check a file exists would be satisfied by
  the decorated summary. This is held by cases, like every other judgment here.

## Data

No storage contract moves. `evals/board.json` gains no field and no entry goes
stale on this commit: `measurement_inputs` hashes each case's own files, the
text of the rules it claims and the bodies of the skills it holds, and this
change writes only a new feature file whose rules are `@planned` and claimed by
nobody, a vocabulary row in `specs/spec.md`, and this file.

**The implementing change is where the bill lands**, and it is worth costing now
rather than discovering later:

| What moves | What goes stale | What it costs |
|---|---|---|
| `skills/refine-spec/SKILL.md` | [`01-solution-shaped-request`](../../evals/01-solution-shaped-request/) — 3 runs, Δ +0.83, one of the five entries currently above the floor | ~$1.80 to re-measure |
| [`29-nowhere-to-draw-it`](../../evals/29-nowhere-to-draw-it/prompt.md), claiming the one rule a case can reach | nothing; a new row, never measured | ~$1.80 to measure |

`method/process.md` and `specs/spec.md` are in neither column — no case holds
them, which is a fact about what the board measures rather than a claim that
they matter less.

## Risks

- **The sketch becomes the thing approved.** The likeliest failure, and the
  reason `what-is-shown-is-not-the-spec-again` says out loud that what is
  approved is the spec. A person short of hours will read the fast artefact and
  stop, which is the same pressure that makes this worth doing at all. The
  mitigation is that the sketch carries no argument to be persuaded by.
- **Invented evidence.** A sketch drawing a before-state the spec never
  established is a confident-looking lie at the exact moment somebody is
  deciding on it. `an-absent-sketch-is-said-rather-than-filled` is written for
  this and it is the rule most worth a hostile eval case.
- **`context-budget` is not the promise at risk; the sitting's tokens are.**
  Nothing is added to a description, so no session pays unless `refine-spec`
  fires. What it does spend is real: a page written after the spec is already
  done, at the end of the longest sitting any of these skills runs.
- **A decorated summary is worse than nothing.** It adds a step, spends tokens
  and gives the reader a second version to reconcile — every cost of this change
  with none of its value. The three rules exist to make that state describable;
  no gate can catch it.
- **`always-green` is untouched.** A sketch is produced in an agent session and
  no build depends on it, in this repository or any consuming one.

## Acceptance checks

There is no screen here, and this repository's own first sketch is one of the
checks. What a person does by hand:

1. Run `refine-spec` in a repository on a request with a real before and after.
   The sketch arrives with the hand-back, unasked for, before approval.
2. Read it against the change spec: none of the four headings appear in it, and
   it links to the file.
3. Revise the spec and hand back again. What they were shown is corrected where
   it stands; there is not a second one.
4. Run it on a change with nothing the prose cannot carry — a renamed constant,
   a corrected path. One line saying so, and nothing drawn.
5. Run it where the session has no way to publish a page. One line saying so,
   today's hand-back, and no part of the session spent looking for another way.
6. `python3 .github/scripts/verify.py` — green on this spec commit; exit 2 on
   the implementing commit until `01-solution-shaped-request` and the new case
   are measured, which is the maintainer's spend to approve.
