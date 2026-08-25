---
name: refine-personas
description: Refine specs/personas/ — who the app is for, and who it is explicitly not for. Use when a persona needs adding, amending or retiring, when a boundary in a persona file ("not for someone who…") is what a change actually turns on, when a persona is named by no workflow, or when the human testing the repo is being mistaken for the person it is built for. Also when a persona file needs auditing line by line against what a design persona is allowed to contain, or when the traceability gate reports a persona orphan. Runs as an interview — asks, plays its reading back, and only then writes the persona and a numbered change spec, confirms the diff on its own, and never implements.
---

# Refine the personas

A persona is *who the product is for*, and nothing else in `specs/` is allowed to
invent one. Every workflow is written for somebody in this folder; every feature
is downstream of a workflow. **This is the highest-leverage file in the
repository and the one that gets edited most casually.**

**Never touch `src/`, `tests/`, or `specs/features/`.**

Workflows are [`refine-workflows`](../refine-workflows/SKILL.md); journeys are
[`refine-journeys`](../refine-journeys/SKILL.md). Each is its own change.

## The one thing this skill refuses

**A persona written to make a wanted feature legal.** It arrives looking
reasonable — a change does not fit the persona, so the persona grows a sentence, or a
second persona appears who happens to want exactly the thing on the table.

The tell is order of arrival: the feature existed before the person did. When
that is what is happening, say so plainly and stop. A new persona is a decision
about what product this is, argued on its own terms, before anything is built for
them.

## Before anything else, read

- `specs/personas/README.md` — the gate that runs both ways, and *the other
  person in the room*
- every persona file, `@retired` ones included — the tag marks somebody no
  workflow names *yet*, so a file wearing it is mid-transition and its version is
  not finished.
- `specs/workflows/` — which workflows name this persona, since that is what the
  persona is *for*
- `specs/spec.md` — the product boundaries, which are the other half of "not for"
- `specs/setup/README.md` — this repository's bindings, including the command
  that runs the traceability gate. Run it, and `git log --oneline -5 --
  specs/personas/`

## 1. Interview the only person who knows

**Nobody here has met the person the product is for.** Every fact about them
comes from whoever has, and a fact nobody gave you is one you invented — which is
the failure this whole layer exists to prevent. So this skill opens by asking,
not by editing.

- **Ask in rounds of three or four.** Each question carries your recommendation
  and one line on what a different answer would change. A question whose answers
  all produce the same persona is not worth asking: that is a survey, and this is
  a design interview.
- **Ask about behaviour, never about preference.** *"What did you do the last
  time that happened?"* moves the product. *"Would you like a field for that?"*
  is a feature request wearing an interview's clothes, and it will be answered
  yes.
- **A question about mechanism is not a persona question.** Undo, versions,
  fields, side-by-side, a button — those belong to `refine-spec` and the person
  answering will rightly say so. Ask what he *does* when a change turns out to be
  wrong; what the product does about it is somebody else's question.
- **Never put a fact in the question that was not given to you.** A question
  built on an assumed circumstance comes back confirming the *mechanism* and
  carries the assumption in behind it, where it then reads as evidence. Ask the
  premise on its own first. If you catch yourself having skipped it, the finding
  is yours rather than theirs, and it goes in the open questions rather than in
  the file.
- **Follow the collisions first.** One new fact that contradicts the file, a
  workflow, or a boundary in `spec.md` is worth four that confirm it. Say the
  collision out loud when you hit it — the person answering usually does not know
  that the sentence they just said rules a feature in or out.
- **Play your reading back before writing anything.** One short paragraph: here
  is what I think these facts mean for the product. The raw answers are not the
  persona — the persona is what you concluded from them, and the human is the
  only one who can tell you the conclusion is wrong.
- **Ask again when the answer opens something.** One round is a rule of thumb,
  not a limit; three rounds of four beats a guess. Stop when the answers stop
  moving the file.
- **The transcript does not go in the file.** A persona holds conclusions; one
  that reads like an interview log has stopped being a design tool. The answers
  themselves belong in the change spec.

**When nobody has said anything new**, the same skill runs as an audit instead:
what does the file claim, what is actually true from the workflows and the app,
is anybody citing it (grep the recent change specs for its name — a persona they
never turn on has become scenery), and is what you found drift or a decision.
Drift is a description that fell behind the person; a decision moves who the
product is built for.

## 2. Hold every line to a test

These are the operational half of the design-persona literature at the bottom of
this file. Apply them **line by line to the file**, not to the change on the
table — that is what makes this a refinement skill rather than an editing one.

- **Behaviour, not biography.** Every line must be something they do, decide or
  refuse. A detail that changes no decision in the product is decoration, and
  decoration is what gets quoted back three versions later as though it were
  evidence.
- **End goals and experience goals, never life goals.** *"Wants it in front of
  them in three seconds"* is a goal a product can serve. *"Wants to be better at
  this"* belongs to nobody and can be used to argue for anything.
- **No demographic doing argumentative work.** Age, household, job — if a
  sentence's force comes from one of those rather than from what the person does,
  it is a guess wearing a fact's clothes. The colour in a persona is there to
  make them memorable; it never wins an argument, and a spec that leans on it has
  found nothing.
- **Keep provenance out of it.** Who was interviewed, when, how much was
  inferred, whether anyone has met a real user at all: that is the change spec's
  to record. In the persona it takes the opening lines and gets read as part of
  the description. What the file carries instead is the questions nobody has
  answered, at the foot, so the next reader asks rather than extrapolating.
- **No requirements, anywhere in it.** A persona holds three things: the
  **problem**, the **habits**, the **desires** — what he struggles with, what he
  actually does, what he wants to be true afterwards. The moment a line says what
  the *product* must or must not do, it is a requirement wearing a persona's
  voice. *"He asks somebody else to do the arithmetic"* is a habit and belongs
  here. *"The app does the arithmetic"* is a requirement and belongs in
  `spec.md`. The
  second kind is what makes a persona unfalsifiable: nobody can go back to a
  person and check it.
- **The persona is not the job.** Who they are, and what they will not tolerate,
  lives here. What they are attempting lives in `specs/workflows/`. The job
  behind a particular request is `refine-spec`'s. A persona file that starts
  listing tasks has begun duplicating the workflows, and the two will drift
  apart with no gate to notice.
- **A simulated persona is a different artifact.** Big Five scores, routines,
  relationships, a photograph — that schema exists to make a model answer *as*
  somebody. This file exists to settle design arguments between people. Never
  import one into the other.

## 3. The tester is not the persona

The human testing this repo has no file here **on purpose**: a `@persona:` tag
would let a workflow be written for them. They paste odd input, open devtools and
corrupt storage by hand; the person the product is for does none of that.

What the tester *finds* is real — a crash is a crash. What the tester *wants*
gets checked against the persona before it becomes a spec. If a request would be
served by giving the tester a file here, that is this skill's refusal above,
wearing a different hat.

## 4. The gate runs both ways

| | |
|---|---|
| every workflow names a live persona | error |
| every persona is named by a workflow, or is `@retired` | error |

**Both rows are claims about this repository, not about the method.** Check them
against the gate wiring ledger in `specs/setup/README.md` before repeating them:
`setup` wires what applies the day it runs, and on that day there were no
personas — so the row over them may still read *not applicable* while you are
about to make it applicable.

- If it does, **the row is yours to move**, in this change: to *automated* if the
  check lands with the persona, or to *deferred* with the change number and one
  line on why not.
- If it reads *not applicable — no personas exist* and persona files already do,
  the ledger contradicts the tree. Say so, and do not restate the table above as
  fact.
- If it has read *deferred* since two changes ago, **stop and ask**: wire it, or
  write it off as deliberately not automated, with the reason in the row. A third
  change flagging the same gap is how a repository carries an unbuilt gate for a
  year — the norm is in [`gates.md`](../../method/gates.md#what-is-wired-and-what-is-not).

So the two edits this skill makes both land in the sibling skill's folder:

- **Adding a persona** needs a workflow naming them, or `trace` goes red. That
  workflow is `refine-workflows` and a separate change. Land the persona
  `@retired`-free only when a workflow is ready to name them, or land the
  workflow first.
- **Retiring a persona** orphans every workflow naming them. Those workflows go
  or get rehomed first, in their own change; this one follows.

A spec commit that leaves `trace` red is not a spec commit.

## 5. Delete, do not shelve

A persona the product has stopped being for is **deleted**, file and README row
together. Git holds what was dropped and the change spec holds why, so a file
left in the tree to be ignored is read as current by everyone who was not there
when it was shelved.

`@retired` stays in the tagging for the one honest use of it — a persona no
workflow names *yet*, mid-transition, for a version. If the tag is still on when
the change lands, the change is not finished.

## 6. Write it, check, hand back

The persona file, from [`templates/persona.md`](../../templates/persona.md),
and `personas/README.md`, then a numbered change spec at
`specs/changes/NNNN-<slug>.md` from
[`templates/change.md`](../../templates/change.md), one past the highest. *Who
this is for* in that spec is, for once, literally the subject.

Then run the traceability gate — the command is in `specs/setup/README.md`.

Green. Commit the spec on its own — `spec NNNN: <title>`.

**Show the persona diff by itself, first** — the diff, one line on what it
changes about who this is for, and what that newly allows in the product or newly
rules out. Ask for that alone in one plain line: never a multiple choice, never
merged with the spec's own approval. Of everything in this repo, this is the
diff that most needs reading before it is approved.

Then clickable `path:line`, the change spec first, and above it only what the
file cannot say: what changed about the reader's understanding of this person,
drift or decision, what you left for later. Then one plain line asking for
approval, and **stop**.

## Where these rules come from

Read these before arguing with the section above; every rule in it is somebody
else's hard-won one, compressed.

- Kim Goodwin, [*Perfecting Your Personas*](https://articles.centercentre.com/perfecting_personas/)
  — behaviour patterns over job titles, the right goals, one persona set per product.
- NN/g, [*Personas vs. Archetypes*](https://www.nngroup.com/articles/personas-archetypes/)
  and [*3 Persona Types*](https://www.nngroup.com/articles/persona-types/) — what the
  name and the invented detail are for, and how to declare which kind you wrote.
- NN/g, [*Why Personas Fail*](https://www.nngroup.com/articles/why-personas-fail/) — the
  uncited persona, and why a failed one poisons the next attempt.
- Indi Young, [*Describing Personas*](https://medium.com/inclusive-software/describing-personas-af992e3fc527)
  — invented demographics as bias, thinking styles as the replacement.
- NN/g, [*Personas vs. Jobs-to-Be-Done*](https://www.nngroup.com/articles/personas-jobs-be-done/)
  — the division of labour between this skill and `refine-spec`.
