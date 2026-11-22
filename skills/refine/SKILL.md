---
name: refine
description: Refine the layers above the features — who the product is for (specs/personas/), the bounded attempts it is built out of (specs/workflows/), and the arc over time with the seams between attempts (specs/journeys/). Use when a persona needs adding, amending or retiring, or the human testing the repo is being mistaken for the person it is built for; when the workflow list no longer matches what anyone attempts — one that is really two, one with no end state, one to add, split, retire or re-cut; when a journey has gone stale since the workflows under it moved, or a seam belongs to no workflow; or when the traceability gate reports an orphan in those layers. Runs as an interview — asks about real occasions, plays its reading back, then writes the file and a numbered change spec, confirms the diff on its own, and never implements.
---

# Refine the personas, the workflows and the journeys

Three layers sit above the features, and each is written from what only a person
can tell you:

- **A persona** is *who the product is for*, and nothing else in `specs/` may
  invent one. Every workflow is written for somebody in that folder. It is the
  highest-leverage file in the repository and the one edited most casually.
- **A workflow** is **a bounded attempt to achieve something**: a trigger, some
  steps, and an end state you can stand at and say "done". It is one sitting,
  one objective, one product.
- **A journey** is the one living layer nothing asserts. It carries what no
  bounded attempt can hold: the arc over time, the timescales, and above all the
  **seams** — what happens in the gap between two attempts, where neither one is
  at fault. That is why it rots quietly: the workflows under it move, every gate
  stays green, and nothing reports it.

**Which layer** is what the request is about. A change touching two is two
changes, landed in the order they depend on each other: a persona before the
workflow that names it, a workflow before the journey that describes it.

**Never touch application code, tests, or what a feature promises.** Retagging a
feature with the workflow it serves is this skill's work; changing its contract
is not. Never write Gherkin in a journey.

## What this skill refuses

The tell is always the order of arrival: the wanted thing existed before the
person, the attempt or the arc did. When that is what is happening, say so
plainly and stop.

- **A persona written to make a wanted feature legal** — a change does not fit,
  so the persona grows a sentence, or a second persona appears who wants exactly
  the thing on the table. A new persona is a decision about what product this
  is, argued on its own terms, before anything is built for them.
- **A workflow invented to give an orphan feature a home.** The gate says every
  feature names a workflow, so the cheapest fix is a workflow shaped exactly like
  it — the gate satisfied and the product lied to. Either the feature serves an
  attempt already on the list, or it serves nobody and the change spec says so.
- **A journey where every phase goes well.** That is a future-state map wearing
  the costume of what happens, and the seams are precisely the parts that do not
  go well. A future-state journey announces itself in its first line and stays
  separate from the current-state one; if nobody can tell which they are
  reading, do not write it.

## Before anything else, read

- the layer's own README, and every file in it — `@retired` personas included:
  the tag marks somebody no workflow names *yet*, so a file wearing it is
  mid-transition and its version is not finished;
- the layers beside it: the personas a workflow is for, the workflows a persona
  is for and the README that ranks them, the journeys they sit in;
- `specs/spec.md` — the product boundaries, the other half of "not for";
- `specs/setup/README.md` — the bindings, including the command that runs the
  traceability gate. Run it, warnings included, and `git log` on the personas,
  workflows and journeys folders. **A journey older than the workflows under it
  is assumed wrong until you have read both.**

**If the work came from an issue, claim it before writing anything.** The
marker and its commands are the bindings' *Claiming an issue* row; the rule
is [`repository.md`](../../method/repository.md#several-changes-at-once)'s.
Where the bindings carry no such row, the comment alone is the claim, and the
hand-back names the row as missing.

- **Read the claim first** — the marker, its comment, an open pull request
  that closes the issue. A tracker that does not answer is said, and the
  person decides: an unread claim is not an absent one.
- **Claimed:** report where the work is — branch, tree, harness, session id —
  and how old the claim is, then stop until the person answers. A claim with
  nothing behind it is reported the same way; nothing releases one by age.
  Told to take it over, the new comment names the claim it replaces.
- **Free:** put the marker on, then one comment — the branch you will work
  on, the tree, the harness, your session id as your harness gives it (or
  *not exposed*, never one made up), and the date. A marker the tracker
  refuses is said in the hand-back and the comment written anyway; the label
  is never created here.
- **Asked for the next issue**, choose among the unclaimed and say which you
  skipped.
- **Turned down, or stopped,** take the marker off, with a comment saying
  why. A pull request that closes the issue ends the claim on its own.

## 1. Interview the only person who knows

**Nobody here has met the person, made the attempt, or lived the arc.** Every
fact comes from whoever has, and a fact nobody gave you is one you invented —
the failure these layers exist to prevent. So this skill opens by asking, not
by editing.

- **Ask in rounds of three or four.** Each question carries your recommendation
  and one line on what a different answer would change. A question whose answers
  all produce the same file is a survey, not a design interview. Ask again when
  an answer opens something; stop when the answers stop moving the file.
- **Ask about one real occasion — the last time — never the usual case or a
  hypothetical.** *"Walk me through the last time"* returns memory; *"what would
  you do if…"* returns a guess dressed as a fact.
- **Ask about behaviour, never preference.** *"What did you do?"* moves the
  product. *"Would you like a field for that?"* is a feature request wearing an
  interview's clothes, and it will be answered yes. A question about mechanism —
  undo, a button, a field — is `refine-spec`'s.
- **Never put a fact in the question that was not given to you.** A question
  built on an assumed circumstance comes back confirming it. Ask the premise on
  its own first; a premise you skipped is your finding, and it goes in the open
  questions rather than in the file.
- **Follow the collisions first.** One fact that contradicts the file, another
  layer, or a boundary in `spec.md` is worth four that confirm it. Say it out
  loud: the person answering rarely knows a sentence just ruled a feature in or
  out.
- **Never ask them to design.** Not the steps they would like, not the phases,
  not the map. Synthesis is yours; handing it over gets you their model of your
  product, not their experience of it.
- **The transcript does not go in the file.** The file holds conclusions; the
  answers belong in the change spec.

What each layer asks for:

- **Personas:** what they do, decide and refuse, and what they will not
  tolerate.
- **Workflows:** *what set it off?* — a situation, never a decision to use the
  product; *how did you know you were finished?* — no answer, no end state, and
  nothing to walk; *what did you do when it went wrong?*; *how long did that
  take, and when would you have given up?* Watch rather than ask where you can:
  what people do has more steps and fewer decisions than what they describe.
- **Journeys:** what happened *between* the sittings, and how long between — a
  journey lives or dies on its timescales; where it nearly ended, or went back to
  the old way; the first time ever and the most recent time; what they expected,
  since a seam is usually the distance between that and what happened.

**When nobody has said anything new**, the same skill runs as an audit: what
the file claims against what the other layers and the app now say — for a
persona, whether recent change specs still cite it (one they never turn on has
become scenery); for a journey, read against the workflows it describes, in the
order they are first reached — and whether what you found is drift, a
description that fell behind, or a decision.

## 2. Play the reading back, before the file exists

**One short paragraph, in your words, before anything is written** — what these
facts mean for the product; the trigger, the steps and the end state of the
attempt; the arc, where it starts and where it dips. Not the answers repeated:
the conclusion you drew from them, which the person is the only one able to
correct. Then stop and let it be corrected.

Played back now it costs a paragraph. Played back after the file is on disk it
is a summary of a decision already taken, and the thing they were here for did
not happen. **This is not the diff**, which comes at the hand-back and does not
stand in for this.

## 3. Personas: hold every line to a test

Apply these **line by line to the file**, not to the change on the table.

- **Behaviour, not biography.** Every line is something they do, decide or
  refuse. A detail that changes no decision is decoration, later quoted back as
  evidence.
- **End goals and experience goals, never life goals.** *"Wants it in front of
  them in three seconds"* can be served; *"wants to be better at this"* can argue
  for anything.
- **No demographic doing argumentative work.** Colour makes a persona
  memorable; it never wins an argument.
- **No requirements, anywhere in it.** A persona holds the **problem**, the
  **habits** and the **desires**. *"He asks somebody else to do the arithmetic"*
  is a habit; *"the app does the arithmetic"* is a requirement, and belongs in
  `spec.md`. The second kind makes a persona unfalsifiable.
- **The persona is not the job.** What they attempt lives in the workflows; the
  job behind a request is `refine-spec`'s.
- **A simulated persona is a different artifact.** Big Five scores, routines, a
  photograph — that schema makes a model answer *as* somebody; this file settles
  design arguments between people.
- **The tester is not the persona.** The human testing this repo has no file
  here **on purpose**: what they *find* is real, what they *want* is checked
  against the persona before it becomes a spec. A request served by giving the
  tester a file is the refusal above, wearing a different hat.
- **Delete, do not shelve.** A persona the product has stopped being for is
  deleted, file and README row together. `@retired` is for one honest use — a
  persona no workflow names *yet*, for a version.

## 4. Workflows: hold it against the definition

- **No trigger and no end state → it is not a workflow.** It is something that
  must always be true: prose in the product spec, asserted inside features and
  every walkthrough, never a file of its own.
- **Two triggers or two end states → it is two workflows.** **A category is not
  an attempt** — "tidy", "manage", "settings". **Count the features under each:**
  eleven is two sharing an id; one is often not a workflow at all. **One path,
  not a branch:** if the examples need an "or else", the attempt is cut too
  coarsely.
- **The narrative is a job story:** *When `<situation>`, I want `<motivation>`,
  so `<outcome>`* — situation first, never role first, which assumes the why and
  invites a solution. Then one line naming the end state, and two or three short
  sections, each a decision somebody could relitigate: what a good attempt must
  not cost, the distinction it must not cross, and **where it breaks** — write
  that one first if you are stuck.
- **The examples are declarative.** No clicks, no element names: would this line
  need rewording if the interface were rebuilt? One behaviour per example, named
  for what it proves; the product's own vocabulary; a failure as well as the
  ordinary case; and the last example comes back and finds it exactly as left.
- **Name the phase it is made in.** Beside `@journey:`, `@phase:` — the heading
  from the journey's map, lower case with hyphens — where one plainly fits.
  Where none does, leave it off and say so; never add or rename a phase to make
  one fit.
- **Update the README's ranking paragraph** in the same pass — evaluative on
  purpose, where the journeys are descriptive.
- **Shrink it.** Re-cutting the list and retiring one attempt are two changes.
  Deleting beats shelving. Ids are close to permanent — everything upstream names
  them.

## 5. Journeys: the anatomy a journey must have

- **It points at nothing.** It declares its own id and names no workflow; the
  workflow says which arc it sits in. **No spec jargon in it**: no ids, no tags —
  it is read by somebody trying to understand a person.
- **The lens — one actor, one scenario.** Two personas is two journeys.
- **The spine — phases, in time order.** Sections that can be reordered are a
  category list. Where the arc goes back to an earlier phase, one line under the
  map names both by their headings — never a column of its own. Headings are
  names a workflow's `@phase:` uses, so renaming one retags that workflow in the
  same change.
- **The heart — what they do, think and feel,** phase by phase. The emotional
  line is the part no assertion can carry.
- **The output — the seams, and what owns each.** Every journey ends in
  findings. **A seam nobody owns is the most valuable sentence in the layer.** A
  seam is not a defect: if the gap is somebody's fault, it is an issue and a spec.
- **The title is the scenario in three words**, in the person's words, verb-first
  or a gerund, never after the persona or a feature — and it must not sound
  completable in one sitting, or it is a workflow's name. A future-state or
  assumed arc says so in the title.
- **Keep it in its own layer.** A checkable sentence belongs in a workflow; a
  judgment of what matters most belongs in the workflows README; generic human
  behaviour is an experience map; backstage process is a service blueprint.

**Keep provenance out of personas and journeys alike.** Who was asked and when,
what was observed and what predicted, belongs in the change spec. The file
carries, at its foot, the questions nobody has answered yet.

## 6. The gates, read against the ledger

| | |
|---|---|
| every workflow names a live persona | error |
| every persona is named by a workflow, or is `@retired` | error |
| every feature names a live workflow | error |
| every workflow is claimed by a feature | error |
| every workflow is walked by an end-to-end test | error |
| a journey naming a workflow that does not exist | error |
| a workflow naming no journey | warning |
| a workflow naming a phase its journey does not have | error |

**These are claims about the method, not about this repository.** The gate
wiring ledger in `specs/setup/README.md` says which are wired — a layer that
arrived after `setup` did may have no check over it at all. Read it before
repeating the table as fact, move the rows this change makes applicable, and
report a row reading *not applicable* while the layer plainly exists as a
contradiction. A row *deferred* since two changes ago stops you: wire it, or
write it off with the reason in the row — **and the reply ends on that choice**,
put to the person as those two halves, before the file is written. The norm and
the states are in [`gates.md`](../../method/gates.md#what-is-wired-and-what-is-not).

What bites, layer by layer:

- **Adding a persona** needs a workflow naming them, or the gate goes red: land
  the workflow first, or the persona `@retired` until one names them. **Retiring
  one** orphans the workflows naming them; those go or are rehomed first.
- **A new workflow has no test yet**: tag it `@planned`. **A renamed or retired
  id** breaks the walkthrough tests, which are not yours: leave the old id live,
  land the new one `@planned`, and let the implementing change carry it across.
  Deleting a workflow can orphan a journey or a persona — land theirs first.
- **Never invent a gate for prose.** What is not gated in the journeys is the
  real risk — whether one has been looked at since the workflows changed — and
  until it is a check, it is this skill's job, done by hand. A warning that
  survives two versions becomes an error or gets deleted.

A spec commit that leaves the gate red is not a spec commit.

## 7. Write it, check, hand back

The file from its template — [`persona.md`](../../templates/persona.md),
[`workflow.feature`](../../templates/workflow.feature) or
[`journey.md`](../../templates/journey.md) — and the layer's README; feature
retagging the gate needs lands in the same commit, nothing else in the feature
specs moves. One journey per change. Then a numbered change spec at
`specs/changes/NNNN-<slug>.md` from [`templates/change.md`](../../templates/change.md),
one past the highest in flight, per
[`repository.md`](../../method/repository.md#several-changes-at-once) — say the
numbers stepped past and where each was held, and say so when the open pull
requests could not be read. For a persona, *Who this is for* is, for once,
literally the subject.

Run the traceability gate — green, warnings read rather than skimmed — and
commit the spec on its own: `spec NNNN: <title>`.

**The reading came first, and this does not replace it.** If it has not been
played back in a paragraph and corrected, step 2 has not happened and the
sitting is not ready to show anything.

**Show the layer's diff by itself, first** — the diff, one line on what it
changes about who this is for, what they attempt, or how the attempts connect,
and what that newly allows, explains or rules out. Ask for that alone in one
plain line: never a multiple choice, never merged with the spec's own approval.
The persona diff, of everything in this repository, most needs reading before it
is approved.

Then clickable `path:line`, the change spec first, and above it only what the
file cannot say: drift or decision, when it was last true, what you assumed,
what you left for later. Then one plain line asking for approval, and **stop**.

## Where these rules come from

Read these before arguing with the sections above; every rule in them is
somebody else's hard-won one, compressed.

- **Personas** — Kim Goodwin, [*Perfecting Your Personas*](https://articles.centercentre.com/perfecting_personas/);
  NN/g, [*Personas vs. Archetypes*](https://www.nngroup.com/articles/personas-archetypes/),
  [*3 Persona Types*](https://www.nngroup.com/articles/persona-types/) and
  [*Why Personas Fail*](https://www.nngroup.com/articles/why-personas-fail/);
  Indi Young, [*Describing Personas*](https://medium.com/inclusive-software/describing-personas-af992e3fc527);
  NN/g, [*Personas vs. Jobs-to-Be-Done*](https://www.nngroup.com/articles/personas-jobs-be-done/).
- **Workflows** — Cucumber, [*Writing better Gherkin*](https://cucumber.io/docs/bdd/better-gherkin/);
  the cardinal rule of BDD, one scenario, one behaviour; Alan Klement,
  [*Replacing the user story with the job story*](https://medium.com/the-job-to-be-done/replacing-the-user-story-with-the-job-story-af7cdee10c27)
  and [Intercom on job stories](https://www.intercom.com/blog/using-job-stories-design-features-ui-ux/);
  NN/g, [*User Journeys vs. User Flows*](https://www.nngroup.com/articles/user-journeys-vs-user-flows/).
- **Journeys** — NN/g, [*Journey Mapping 101*](https://www.nngroup.com/articles/journey-mapping-101/),
  [*Customer Journey Maps*](https://www.nngroup.com/articles/customer-journey-mapping/),
  [*UX Mapping Methods Compared*](https://www.nngroup.com/articles/ux-mapping-cheat-sheet/)
  and [*Journey Mapping: 9 FAQs*](https://www.nngroup.com/articles/journey-mapping-faq/);
  Jim Kalbach, *Mapping Experiences*.
