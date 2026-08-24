---
name: refine-workflows
description: Refine the workflow specs — the bounded attempts the product is built out of. Use when the workflow list no longer matches what anyone actually attempts: one that is really two, one with no end state, one nothing implements or nothing walks, one to add, split, retire or re-cut. Also when the traceability gate reports a workflow orphan. Runs as an interview — asks what set the attempt off and how they knew they were done — then writes the workflow and a numbered change spec. Never implements.
---

# Refine the workflows

A workflow is **a bounded attempt to achieve something**: a trigger, some steps,
and an end state you can stand at and say "done". That is the whole definition,
and every file in the folder is held against it.

It is narrower than a journey on purpose. A journey spans months and the gaps
between attempts; a workflow is one sitting, one objective, one product.

**Never touch application code or tests.** Never rewrite what a feature promises
— retagging a feature with the workflow it serves is this skill's work, changing
its contract is not.

Personas and journeys are the sibling skills. The gates bind all three, so expect
to hand work across; each hand-off is its own change.

## The one thing this skill refuses

**A workflow invented to give an orphan feature a home.** The gate says every
feature must name a workflow, so when a feature serves nothing the cheapest fix
is a new workflow shaped exactly like it. That is the gate being satisfied and
the product being lied to.

The tell is order of arrival: the feature existed before the attempt did. When
that is what is happening, say so and stop. Either the feature serves an attempt
already on the list, or it serves nobody and the honest move is to say that in
the change spec.

## Before anything else, read

- the folder's README — the definition, and the paragraph that ranks the
  workflows by where the value is
- every workflow file, not just the one in question
- the personas: a workflow with nobody attempting it is not a workflow
- the journeys: they say where each attempt sits in the arc, and they are usually
  where the evidence for a re-cut turns up first
- the traceability gate's output, warnings included
- `git log` on the workflows, personas and journeys folders. A journey newer than
  the workflows under it is where the disagreement will be.

## 1. Interview for the attempt

Ask about one occasion, not about the usual case.

- **"What set it off?"** The trigger is a situation, never a decision to use the
  product. *"When I wanted to use the app"* is circular and means the trigger has
  not been found.
- **"How did you know you were finished?"** If they cannot answer, there is no
  end state, and without one there is nothing to walk and nothing to assert.
- **"What did you do when it went wrong?"** The failure modes are worth more than
  the happy path — they are what stop the examples being a demo.
- **"How long did that take, and when would you have given up?"** A workflow with
  a cost ceiling is specifiable; one without will grow a step every version.
- **Watch rather than ask, where you can.** People describe the task they think
  they perform. What they actually do has more steps and fewer decisions.
- **Never ask what steps they would like.** That is design, and the answer will be
  your own product described back to you.

Play the attempt back in one paragraph before writing — trigger, steps, end state
— and let it be corrected.

## 2. Hold it against the definition

- **No trigger and no end state → it is not a workflow.** It is something that
  must always be true: prose in the product spec, asserted inside ordinary
  features and inside every walkthrough, never a file of its own.
- **Two triggers or two end states → it is two workflows.** A file saying "this
  half-finishes" is telling you so out loud.
- **A category is not an attempt.** "Tidy", "manage", "settings" collect
  everything nobody could file elsewhere.
- **Count the features under each.** Eleven is not a busy workflow, it is two
  sharing an id. One is often not a workflow at all.
- **One path, not a branch.** Several entry points converging on one end state is
  one workflow; two end states is two. If the examples need an "or else" the
  attempt has not been cut finely enough.

Update the folder README's ranking paragraph in the same pass — which attempts
carry the value, and which trade is a bad one. That paragraph is evaluative on
purpose and the journeys are descriptive; do not let them collapse together.

## 3. Write the narrative as a job story

**When `<situation>`, I want `<motivation>`, so `<outcome>`.**

Situation first. The role-first form — *"As a `<role>`, I want…"* — starts from
who somebody is and quietly assumes that explains why they are doing this; it
also invites a solution into the middle clause. The job form starts at the moment
that caused the attempt, which is the only part a product can actually serve.

Then **one line naming the end state**, and two or three short prose sections.
Each must be a decision somebody could otherwise relitigate: what a good attempt
looks like and what it must not cost, the distinction this workflow must not
cross, and **where it breaks**. Write the failure section first if you are stuck
— it is the one that makes the rest honest.

## 4. Write the examples declaratively

- **Say what happens, not which control does it.** No clicks, no drags by pixel,
  no element names. Ask of every line: would this need rewording if the interface
  were rebuilt? If yes, it is imperative and it will rot.
- **One behaviour per example**, and name it for what it proves rather than for
  the mechanics.
- **Use the product's own vocabulary** and no other words for the same things.
  A workflow that invents a synonym has started a second vocabulary.
- **Cover a failure, not only the ordinary case.** The examples exist to be
  walked; a walk that only ever succeeds proves nothing about the attempt.
- **End with the return.** The last example comes back to the product and finds
  it exactly as left — that is the durability promise asserted where it is
  cheapest, once per workflow.

The template in the workflows folder carries this shape with the rules inline.

## 5. Walk the gates by hand, then run them

| | |
|---|---|
| every feature names a live workflow | error |
| every workflow is claimed by a feature | error |
| every workflow names a live persona | error |
| every workflow is walked by an end-to-end test | error |
| a journey naming a workflow that does not exist | error |
| a workflow naming no journey | warning |

Three bite this skill in particular:

- **A new workflow has no test yet** — tag it `@planned` and let the implementing
  change drop the tag.
- **A renamed or retired id breaks the walkthrough tests**, and tests are not
  yours to move. Do not rename in place: leave the old id live, land the new one
  `@planned`, and let the implementing change carry the rename across. A spec
  commit that leaves the gate red is not a spec commit.
- **Deleting a workflow can orphan a journey reference or a persona.** That is
  the sibling skill's file and a separate change; land theirs first.

## 6. Shrink it

- Re-cutting the list and retiring one attempt are two changes. Write the first.
- **Deleting beats shelving.** A dropped workflow leaves the tree; the change spec
  that dropped it is where somebody reads what it was and why it went.
- Workflow ids are close to permanent — everything upstream names them.

## 7. Write it, check, hand back

The workflow files, then a numbered change spec from the template. Feature
*retagging* needed to keep the gate green belongs in the same commit; nothing
else in the feature specs moves.

Run the gate. Green, warnings read rather than skimmed. Commit the spec on its
own.

**Show the workflow diff by itself, first** — the diff, one line on what it
changes about what they attempt, and what that newly allows or newly rules out.
Ask for that alone in one plain line: never a multiple choice, never merged with
the spec's own approval.

Then clickable `path:line`, the change spec first, and above it only what the
files cannot say: the drift found, whether it was drift or a decision, what you
assumed, what you left for later. Then one plain line asking for approval, and
**stop**.

## Where these rules come from

- Cucumber, [*Writing better Gherkin*](https://cucumber.io/docs/bdd/better-gherkin/)
  — declarative over imperative, no interface details, and the wording test: would
  this need changing if the implementation did?
- The cardinal rule of BDD — **one scenario, one behaviour**. A scenario is a
  requirement and an acceptance criterion, not a script; two behaviours in one
  make it impossible to say which broke.
- Alan Klement, [*Replacing the user story with the job story*](https://medium.com/the-job-to-be-done/replacing-the-user-story-with-the-job-story-af7cdee10c27)
  and [Intercom on job stories](https://www.intercom.com/blog/using-job-stories-design-features-ui-ux/)
  — situation first, and why the role-first form smuggles in assumptions.
- NN/g, [*User Journeys vs. User Flows*](https://www.nngroup.com/articles/user-journeys-vs-user-flows/)
  — a flow is one objective inside one product, and that is what keeps this layer
  narrower than the journeys.
