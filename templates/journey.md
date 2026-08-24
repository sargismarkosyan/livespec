@journey:<id> @persona:<id>

# <Gerund phrase naming the scenario>

<!--
Structure follows the NN/g journey map: a lens, a map, and an output.
https://www.nngroup.com/articles/journey-mapping-101/

- No provenance in this file. Whether the arc was observed or predicted, who was
  asked and when, all of it goes in the change spec.
- It points at nothing. A journey declares its own id and names no workflow; the
  workflow files say which arc they sit in.
- No spec jargon anywhere — no workflow ids, rule ids or tag names. This is read
  by somebody trying to understand a person.
- Prose and tables, never Gherkin. Nothing here is asserted; a checkable
  sentence belongs in a workflow.
- Current state unless the title says otherwise. An arc where every phase goes
  well is a wish.
- Name the scenario in their words, gerund-first. If the title sounds like
  something completable in one sitting, it is a workflow, not a journey.
-->

## The lens

| | |
|---|---|
| **Actor** | One person. Never a composite, never two personas. |
| **Scenario** | What they are trying to get done, and what set it off. One or two sentences. |
| **Goal** | What "done" looks like from their side of the screen. |
| **Span** | How long the arc runs, and what it is made of. |

**Expectations** — what they think is going to happen, before it does. Every gap
below is measured against these, so vague ones make the whole output vague.

- ...
- ...
- ...

## The map

Phases across, in time order. Number the actions continuously so the sequence
survives being read one column at a time. Include the phases before the product
exists for them, and the ones where it goes badly — those are the only phases
that decide anything.

| | **<Phase 1>** | **<Phase 2>** | **<Phase 3>** | **<Phase 4>** |
|---|---|---|---|---|
| **Doing** | 1. …<br>2. … | 3. …<br>4. … | 5. … | 6. …<br>7. … |
| **Thinking** | *"…"* | *"…"* | *"…"* | *"…"* |
| **Feeling** | ▅ | ▂ | ▁ | ▆ |

**Doing** is behaviour, not screens. **Thinking** is quoted where anything was
actually said and paraphrased where it was not — never invented. **Feeling** is a
curve: `▁▂▃▄▅▆▇`, and it has to move. If every phase carries the same block,
either the arc is wrong or nobody has been asked yet.

**The curve.** One paragraph: where it peaks, where it bottoms out, and what
happens at the bottom. The trough is the phase the product is judged on.

## Opportunities

What could be different, each traced to the gap it comes from. A gap here is one
where **neither side is at fault** — if somebody is at fault it is a defect and
belongs in an issue, not on a map.

- **<the gap, in plain words>** — what would close it.
- ...

## Ownership and metrics

| Opportunity | What answers it today | How we would know it worked |
|---|---|---|
| ... | the part of the product that covers this moment, or **nothing yet** | the observable thing that changes |

*"Nothing yet"* in the middle column is the most valuable row on the page: it is
a moment in their life the product does not reach.
