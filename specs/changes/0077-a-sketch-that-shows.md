# Spec 0077: a sketch that shows

- **Status:** proposed
- **Issue:** [#168](https://github.com/sargismarkosyan/livespec/issues/168)

## Who this is for

**Ren — [`agent-accelerated-owner`](../personas/agent-accelerated-owner.md).**
They don't read the documentation, but they do read the spec layer, and the
sketch is the one page drawn for the moment they decide on a change spec.
Nothing about who this is for moves.

**The workflow is [`adopt-the-process`](../workflows/adopt-the-process.feature),
at *The changes after***, step 8 of
[`trusting-the-spec-again`](../journeys/trusting-the-spec-again.md): every
approval, many times a day. The step's length doesn't change. What changes is
whether the page shown at that step can be taken in at a glance.

## The job behind the request

To approve or push back on a change spec by looking at one page, and see
what the change does to something they already know, without reading the
spec twice.

**What they do today instead** is read the spec, because the sketch doesn't
carry it. In helios/pi-plugins, a `refine-spec` sketch (spec 0035) followed
§ *And draw the sketch* to the letter: five metric tiles, two unrelated
`<pre>` blocks for before and after, a *what moves* table, and two small
diagrams. The maintainer called it correct and reading like a form. In the
same week, with the same artifact tool and design system, another page
showed one named workflow as it is now and as it would be, in two frames laid
out alike, with the count as a sentence under each frame. They preferred that
one, and asked for livespec's guidance to produce it. The sketches for 0074,
0075 and 0076, drawn in this repository the same day, have the same shape as
the one they called a form: tiles and a table.

## Why now

- **The guidance says what to carry and not how to show it.** The four
  bullets in `skills/refine-spec/SKILL.md` (*What goes in it*) are content
  requirements. With no form named, an agent fills them with the most generic
  layout to hand: a tile per count, a table per list, a code block per state.
- **The difference is the guidance, not the tooling.** Both pages came from
  one session, one artifact tool and one design system.
- **Nothing holds the sketch at all.** Two of the four sketch rules in
  [`before-it-is-built.feature`](../features/showing/before-it-is-built.feature)
  are still `@planned`, because no case has ever graded a drawn sketch. A
  sketch written to a file has been readable by a case since 0031, and
  nobody wrote the case.

## The end value

A sketch shows the change on one real thing the person knows, drawn twice the
same way, so the difference is what the eye lands on. The counts are
sentences under the drawing. The forms used are the ones the evidence has: a
flow, a grid, a tree diff. A person can decide from the sketch whether the
spec is worth opening.

**How we would know it worked:**
- The next sketch this repository draws (0078's) has two frames on one named
  instance and no free-standing tiles.
- A case drawing a sketch to a file passes a grader that reads the page for
  exactly that, and the two sketch rules that sat `@planned` since 0031 come
  off.

## What changes

1. **[`refine-spec`](../../skills/refine-spec/SKILL.md), § *And draw the
   sketch* — a short *How it is shown*,** after *What goes in it*:
   - **One instance, drawn twice.** Pick the one real thing the change
     touches most that the spec names (a request, a workflow, a file, a
     command). Draw it now and after, in two frames with the same layout,
     so only the difference differs.
   - **The count is a sentence under its frame**, in the reader's units
     ("three files kept in step by hand; none checked"), never a number alone
     in a tile.
   - **The form the evidence has:**
     - a **flow** of real artifacts for a process;
     - a **grid with a legend** for which-covers-which;
     - a **tree diff** (added marked, removed struck through, a note per
       line) for files;
     - a **pipeline diff** for steps and gates;
     - a **yes/no table** only for options side by side.
   - **One headline sentence at most**, taken from the spec's *What
     changes*, never from *The end value*. *Evidence, never argument* stands.
   - **The reference page is
     `templates/sketch.html`:** start from
     it, keep its structure, replace its example.

2. **`templates/sketch.html` — new.** One
   self-contained page that carries the vocabulary with a worked example:
   - the headline line;
   - two Now/After frames, each with its count sentence;
   - a flow, a grid with its legend, a tree diff and a pipeline diff;
   - *what moves and what stays*, as rows with the reason against each;
   - the link to the spec.

   Colours are tokens, with light and dark both defined. It uses no external
   script, so it renders as a file as well as when published. It is linked
   from the skill, so it ships as payload and loads only when a sketch is
   drawn.

3. **The rule and the case.**
   - One new rule, `a-sketch-draws-one-instance-twice`, in
     [`features/showing/how-it-is-drawn.feature`](../features/showing/how-it-is-drawn.feature).
   - One `refine-spec` eval case whose request changes something with a
     plain before and after, in a session with no publishing tool, so the
     sketch is written to a file. Its graders read the page for:
     - the new rule;
     - `the-decision-gets-what-the-prose-cannot-carry`: now beside after,
       handed over without being asked for;
     - `what-is-shown-is-not-the-spec-again`: none of the four sections
       restated, and the link present.

     Both of those lose `@planned` in the implementing commit. Their
     comments, which say they wait on a case, are removed with the tags.

**Rules added or changed:**

| Rule id | Feature file | New or changed |
|---|---|---|
| `a-sketch-draws-one-instance-twice` | [`features/showing/how-it-is-drawn.feature`](../features/showing/how-it-is-drawn.feature) | new, `@planned` until the implementing commit |
| `the-decision-gets-what-the-prose-cannot-carry` | [`features/showing/before-it-is-built.feature`](../features/showing/before-it-is-built.feature) | `@planned` comes off; wording unchanged |
| `what-is-shown-is-not-the-spec-again` | same | `@planned` comes off; wording unchanged |

## What we are not doing

- **The artifact tool or a design system.** Both pages came from the same
  ones.
- **A sketch checker in the gates.** Form is judged, so a model grades it,
  in a case. A gate counting `<div class="tile">` would be a gate about
  markup, not about whether a person can see the change.
- **Numbered prose sections** ("1 · Today, 2 · Target") like the preferred
  page's lower half. That page was a proposal, and its prose is argument.
  The sketch keeps the top half, the evidence.
- **Re-drawing the sketches already published** for 0074–0076. They served
  their decision, and they stay as drawn.
- **The other refine skills.** Only `refine-spec` draws a sketch.

## Data

No storage contract moves. A consuming repository's sketches are not stored,
since they are pages for one decision, so nothing already drawn is affected.

## Risks

- **A template becomes the look of every sketch.** The structure is meant to
  repeat. The example must not be left in. The case grades the instance as
  the spec's own, so a page still carrying the template's example fails.
- **Context cost.** The skill body grows by a short section, about 15 lines,
  and no description moves. The template loads only when a sketch is drawn.
- **Eval spend.** Editing `refine-spec` stales `review refine-spec`, which is
  already stale on `main`. The new case starts unmeasured. Named in the pull
  request, and nothing runs without the maintainer's yes.

## Acceptance checks

1. Open `templates/sketch.html` as a file, in light and dark. Every part of
   the vocabulary renders with no network.
2. Read *How it is shown* and confirm it names the template and restates
   none of the four sections.
3. The next sketch drawn here (0078's) follows it.
