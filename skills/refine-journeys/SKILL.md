---
name: refine-journeys
description: Refine specs/journeys/ — the prose layer carrying the arc over time and the seams between workflows. Use when a journey has gone stale since the workflows under it moved, when a seam belongs to no workflow and nothing holds it, when a persona has no journey, or when a journey has drifted into being a longer workflows README. Also when the traceability gate reports a dangling journey reference. Runs as an interview — asks for the last time rather than the usual time, plays the arc back, and only then writes the journey and a numbered change spec. Never implements.
---

# Refine the journeys

A journey is the one living layer nothing asserts. It carries what no bounded
attempt can hold: the arc over time, the timescales, and above all the **seams**
— what happens in the gap between two attempts, where neither one is at fault.

That is also why it rots quietly. The workflows under it move, every gate stays
green, and the prose goes on describing something that changed two versions ago.
**Nothing reports this**, which is what this skill is for.

**Never touch `src/`, `tests/`, or the feature specs.** Never write Gherkin here.

## The one thing this skill refuses

**A journey where every phase goes well.** That is a future-state map — the
product as somebody hopes it will be — wearing the costume of what happens. It is
a legitimate artifact and a catastrophic one to confuse with the current state,
because the seams are precisely the parts that do not go well, and a map without
them has nothing to say.

A future-state journey must announce itself in its first line and stay clearly
separate from the current-state one. If nobody can tell you which one they are
reading, do not write it.

## Before anything else, read

- the journeys folder's own README — what this layer is for, and the norms it owns
- every existing journey
- the workflows, and the README that ranks them — this comparison is what the
  whole skill turns on
- the personas: a journey belongs to exactly one of them
- the traceability gate — the command is in `specs/setup/README.md` — warnings
  included, and `git log` on both the workflows and the
  journeys folder. **If the workflows moved after the journey did, assume the
  journey is wrong until you have read both.**

## 1. Interview for the arc, not for the steps

Nobody here has lived the arc. Every fact about it comes from whoever has, and a
phase nobody described is one you invented.

- **Ask retrospectively, never hypothetically.** *"Walk me through the last time
  you did this"* returns memory. *"What would you do if…"* returns a guess
  dressed as a fact, and it will match whatever you were hoping to hear.
- **Ask about the gaps, not the sittings.** The workflows already have the
  sittings. What this layer needs is what happened *between* them, and how long
  between — a journey lives or dies on its timescales.
- **Ask where it nearly ended.** When did they almost stop, or go back to the old
  way? That moment is a seam, and it is worth more than the five phases that went
  fine.
- **Ask about the two ends.** The first time ever, and the most recent time.
  Beginnings and returns are where expectation and reality diverge most.
- **Ask what they expected.** A seam is usually the distance between what they
  thought would happen and what did.
- **Never ask them to name the phases**, or to draw the map. Synthesis is yours;
  handing it over gets you their mental model of your product, which is not the
  same thing as their experience of it.
- **Play the arc back in one paragraph** before writing anything, and let it be
  corrected. Rounds of three or four questions, each carrying a recommendation
  and one line on what a different answer would change.

**When nobody has said anything new**, run as an audit instead: read the journey
against the workflows it names, id by id and in the order they are first reached,
and say when it was last true.

## 2. The anatomy a journey must have

Three parts. A file missing any one of them is not a journey.

- **It points at nothing.** A journey declares its own id and names no workflow.
  The dependency runs the other way — a workflow says which arc it sits in,
  because a bounded attempt knows what it is part of and an arc does not know
  what will be built inside it. A journey listing workflows has started keeping a
  table that some later change will silently falsify.
- **No spec jargon in it, anywhere.** Workflow ids, rule ids, tag names: a
  journey is read by somebody trying to understand a person, and an id in the
  prose makes them stop and go look something up. Say *"everything it offers
  begins with somebody who has already decided to write something down"*, not the
  id of the attempt that does.
- **The lens — one actor, one scenario.** A journey that covers two personas
  covers neither; it is two journeys. Name both in the first lines.
- **The spine — phases, in time order.** If the sections can be reordered without
  breaking anything, it is a category list, not a journey.
- **The heart — what they do, what they think, and how it feels**, phase by
  phase. Actions alone make a flow chart. The emotional line is the reason this
  layer exists in prose: it is the part no assertion can carry.
- **The output — the seams, and what owns each.** Every journey ends in findings,
  not in description: here is the gap, here is which attempt is nearest to it,
  here is whether anything owns it at all. **A seam nobody owns is the most
  valuable sentence in the layer.** A journey that stops at narration is a poster.

## 3. Name it for the scenario

The title is the lens in three words, and journeys get named badly more often
than personas do.

- **Name the scenario, not the product or a feature.** The map is *actor +
  scenario*; the title carries the scenario. A title with a feature in it
  re-centres the map on what was built.
- **Use the person's words.** If it contains a term only the team says, it is an
  internal name and it will quietly turn the map into a company document.
- **Gerund or verb-first.** It is a process over time. A noun phrase reads as a
  document; a gerund reads as an arc.
- **It must not sound completable in one sitting.** This is the sharpest test:
  workflow names are bounded attempts, journey names span the gaps between them.
  If the title could be a workflow, it is the wrong title.
- **Never name it after the persona.** *"X's journey"* is metadata, not a name —
  it says nothing about what happens and ages badly the moment the persona is
  edited.
- **Say in the title if it is future-state or assumed.** A predicted arc that
  does not announce itself gets cited as evidence within two versions.

## 4. Keep it in its own layer

Four things it is not, and the test for each:

- **Not a workflow.** A workflow is a bounded attempt with a trigger and an end
  state, and it is asserted. If a sentence here is checkable, it belongs there.
- **Not the ranking.** A judgment about which part matters most is evaluative and
  belongs in the workflows README. This layer is descriptive: what happens, in
  what order, over what timescale.
- **Not an experience map.** That describes generic human behaviour independent
  of any product. A journey is this person, with this product.
- **Not a service blueprint.** Backstage processes and who does what internally
  are a different diagram and a different conversation.

**A seam is not a defect.** If the gap is somebody's fault, it is an issue and a
spec. Seams are where *neither* attempt is at fault — that is the whole reason
this layer earns its place.

## 5. Keep provenance out of it

Whether the arc was observed or predicted, who was asked and when, how much was
inferred: **all of it goes in the change spec.** None of it belongs in the
journey, where it takes the opening lines and gets read as part of the arc.

What the file does carry is the questions nobody has answered, at the foot, so
the next reader asks rather than extrapolating.

## 6. The gates, and the one deliberately missing

| | |
|---|---|
| a journey naming a workflow that does not exist | error |
| a workflow naming no journey | warning |

That is all of it, on purpose. **Never invent a gate for prose** — nothing here
is asserted, and a check on a judgment call reports something everybody already
knew.

What is *not* gated is the actual risk: whether a journey has been looked at
since the workflows under it changed. That is a git question rather than a file
question, and until it is a check it is this skill's job, done by hand.

The warning-hygiene norm this folder owns applies everywhere: **a warning that
survives two versions either becomes an error or gets deleted.**

## 7. Write it, check, hand back

One journey per change. Re-cutting the workflows a journey describes is the
workflows skill's job and a different version — those land first, because this
file is downstream of them.

The journey file, from [`templates/journey.md`](../../templates/journey.md),
then a numbered change spec at `specs/changes/NNNN-<slug>.md` from
[`templates/change.md`](../../templates/change.md), one past the highest. Run
the traceability gate; it must be green. Commit the spec on its own.

**Show the journey diff by itself, first** — the arc as it now reads, one line on
what it changes about how the attempts connect, and what that newly explains or
newly stops excusing. Ask for that alone, in one plain line: never a multiple
choice, never merged with the spec's own approval.

Then clickable `path:line`, the change spec first, and above it only what the
file cannot say: the drift found, when the journey was last true, what you left
for later. Then one plain line asking for approval, and **stop**.

## Where these rules come from

- NN/g, [*Journey Mapping 101*](https://www.nngroup.com/articles/journey-mapping-101/)
  — the three zones this skill's anatomy is taken from: the lens, the heart, the
  output.
- NN/g, [*Customer Journey Maps: When and How to Create Them*](https://www.nngroup.com/articles/customer-journey-mapping/)
  — one actor and one scenario, and why current-state comes before future-state.
- NN/g, [*UX Mapping Methods Compared*](https://www.nngroup.com/articles/ux-mapping-cheat-sheet/)
  — the boundaries against experience maps and service blueprints.
- NN/g, [*Journey Mapping: 9 FAQs*](https://www.nngroup.com/articles/journey-mapping-faq/)
  — scope, staleness, and how many maps is too many.
- Jim Kalbach, *Mapping Experiences* — the long form: a map is an alignment
  device, and it is worthless without a stated point of view and time span.
