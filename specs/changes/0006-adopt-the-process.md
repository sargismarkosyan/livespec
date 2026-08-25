# Spec 0006: adopt the process

- **Status:** approved
- **Issue:** [#14](https://github.com/sargismarkosyan/livespec/issues/14)

## Who this is for

[`@persona:agent-accelerated-owner`](../personas/agent-accelerated-owner.md), in
the situation that opens the file: a repository that has grown past what anybody
can re-explain to a fresh session, with regressions arriving out of changes whose
reasons nobody remembers.

This spec **is** the workflow, so it sits in
[`adopt-the-process`](../workflows/adopt-the-process.feature) by being it. It is
also the attempt [`0004`](0004-setup-can-be-offered.md) already named without
being able to cite —  *"adopting the process into a repository is an attempt made
with the plugin, in the adopter's own repository"* — and the point where
[journeys/](../journeys/README.md) says the arc starts.

**Provenance.** One interview, 2026-08-25, immediately after
[`0005`](0005-the-first-persona.md) and from the same `setup` chain: one occasion,
four questions, plus the reference implementation in `../todo-change` that the
same person pointed at. Same n = 1 caveat as 0005, and the same mitigation —
most of what is written down was observed in repositories that are not this one.

## The job behind the request

Every session begins by being told what the repository is and why it is the way
it is. That cost does not fall as the repository grows; it rises with it, because
there is more to re-explain and less chance of remembering all of it. Meanwhile
changes land against reasons nobody has written down, and the regressions that
follow are the bill for that.

## Why now

Two things, one of them on a clock.

[#14](https://github.com/sargismarkosyan/livespec/issues/14) again: the layer has
been empty for a version and everything downstream reads it first.

The clock is [`0005`](0005-the-first-persona.md). The persona landed `@retired`,
because `trace.py` fails a live persona no workflow names, and that tag is only
honest **mid-transition, for a version**. This is the change that finishes the
transition: the workflow names the persona and the tag comes off in the same
commit. A version later it would have stopped being a transition and started
being a shelf, which is what
[`refine-personas`](../../skills/refine-personas/SKILL.md) §5 exists to prevent.

## The end value

The layer stops being empty, so a change spec can say which attempt it serves and
be checked on it. And the **Gherkin debt becomes payable for the first time**:
[`0002`](0002-setup-finishes-what-it-names.md) reserved three rule ids —
`setup-continues-into-the-layers`, `setup-finds-where-issues-go`,
`setup-audits-an-existing-claude-md` — that could not be written because a feature
naming no live workflow fails the gate and there were no workflows. Now there is
one, and it is the one those three serve.

**How we would know it worked:** the next change that writes a feature file tags
it `@workflow:adopt-the-process`, drops `@planned` from the workflow in the same
commit, and the gate goes from mapping one workflow to nothing, to mapping one
workflow to a feature and a case.

## What changes

- `specs/workflows/adopt-the-process.feature` — new, `@planned`. Job story,
  one end state, three prose sections, four examples of which two are failures
  and the last is the return.
- `specs/personas/agent-accelerated-owner.md` — **`@retired` comes off.** Nothing
  else in the file moves.
- `specs/workflows/README.md` — the layer stops saying *Empty*, gains the row,
  the evaluative map paragraph the journeys must not duplicate, and a note naming
  the three attempts that are real but uninterviewed.
- `specs/personas/README.md` — the row goes from `@retired` to live, and records
  which change took the tag off.

**Rules added or changed:** none, and not owed. This moves what somebody is
attempting, not what the product does. The three reserved ids stay reserved —
attaching them is a feature change with eval cases behind it, and it is the
change that drops `@planned`.

**Ledger:** nothing to move. All six rows in
[`refine-workflows`](../../skills/refine-workflows/SKILL.md) §5 already read
*automated* in [setup/README.md](../setup/README.md#gate-wiring), each proven by
a fault in `inject.py`. The skill warns those rows are often unwired where the
layer arrived after `setup`; here they were wired first and the layer arrived
second.

## What we are not doing

- **Not writing the other three workflows.** Filing what they found, getting a
  request specced, taking a version through review — all three are real and all
  three have happened repeatedly in `todo-change`. None has had its occasion
  interviewed, and this skill's whole refusal is about workflows that arrive to
  fill a shape rather than to describe an attempt. Each gets its own change.
- **Not attaching the three reserved rule ids**, and not writing
  `specs/features/`. That is `refine-spec`'s work, needs an eval case per live
  rule, and drops `@planned` when it lands.
- **Not writing the journey.** Next skill, its own approval. Until then the
  workflow names no `@journey:` and the gate warns — deliberately, and it is the
  only warning in the run.
- **Not fixing [#21](https://github.com/sargismarkosyan/livespec/issues/21)**,
  which the end state leans on. See *Risks*.

## Data

`@workflow:adopt-the-process` is **permanent from the moment this lands** —
`ids-are-permanent` in [spec.md](../spec.md#the-promises-that-belong-to-no-single-workflow),
and workflow ids are worse than most because everything upstream names them: a
feature tag, a journey reference, an eval case's `workflow:` claim, in every
consuming repository at once. It is named for the attempt rather than for the
skill that serves it, so that `setup` could be renamed, split or replaced without
orphaning it.

## Risks

- **No cost ceiling, and this is the real risk in the file.** The interview could
  not produce one — *"I don't know how to answer this one"* — and
  `refine-workflows` §1 is blunt about what that means: an attempt without a
  ceiling grows a step every version. The mitigation is written into the map
  paragraph rather than left as a hope: a change that lengthens adoption has to
  name which later attempt it shortens. The first time that argument is waved
  through is the version this workflow starts rotting.
- **The end state names something that does not exist yet.** *The pull request
  carries what the version leaves behind* is
  [#21](https://github.com/sargismarkosyan/livespec/issues/21), still open. The
  workflow is `@planned`, so describing an attempt that cannot yet complete is
  legitimate — but it means the tag cannot come off until #21 does, and that is a
  dependency nobody would find by reading the file alone.
- **It could be misread as an attempt made *on* livespec.** The layer README's
  own test — *"when a workflow could be read either way, it is the wrong
  workflow"* — passes here, but narrowly: the attempt is the adopter's, in the
  adopter's repository. What makes it look otherwise is that the features serving
  it will describe what `setup` does, which is livespec's own behaviour. That is
  correct and is what "a feature serves a workflow" means; it is written here
  because the next person to read it will have the same doubt.
- **`ids-are-permanent`** is spent again, on a second id from the same n = 1.

## Acceptance checks

1. `python3 .github/scripts/verify.py` is green, and **the only warning is the
   missing `@journey:`**. Any second warning means something else moved.
2. The map printed by the gate shows `adopt-the-process` for
   `agent-accelerated-owner`, with `(nothing yet)` under it.
3. `specs/personas/agent-accelerated-owner.md` line 1 has no `@retired`.
4. Read the four examples once looking only for interface detail — a control, a
   click, a screen. If a line would need rewording when the implementation
   changed, it is imperative and it will rot.
5. Read **Where it breaks** and check every failure named there is one that has
   actually happened, not one that could.
