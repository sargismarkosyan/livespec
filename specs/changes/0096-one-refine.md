# Spec 0096: one refine

- **Status:** approved in advance, by the maintainer, 2026-11-22 ("Do however you feel right" … "go")
- **Issue:** [#198](https://github.com/sargismarkosyan/livespec/issues/198), its second half. The first was [`0095`](0095-setup-reports-and-brings-it-up-to-date.md).
- **Sketch:** skipped, because approval was given in advance.

## Who this is for

**[`agent-accelerated-owner`](../personas/agent-accelerated-owner.md), in [`adopt-the-process`](../workflows/adopt-the-process.feature)**: at *Putting it in*, where `setup` hands on to three interviews in order, and at *The changes after*, whenever a request turns out to be about who the product is for, what they attempt, or the arc between attempts. Today that is three skills to tell apart, and three descriptions paid for in every session.

## The job behind the request

To refine the layers above the features through one interview, whichever layer the request is about.

## Why now

- **The three skills are one discipline.** Their claim block is identical word for word. Their interview, play-back and hand-back differ only in which layer they name. What differs is each layer's rules: a persona's line tests, a workflow's definition, a journey's anatomy.
- **Every skill costs its description in every session.** Three become one: 4,084 → 3,097 characters always on.
- **[#198](https://github.com/sargismarkosyan/livespec/issues/198)** asked for six skills to become three. With `doctor` folded into `setup`, this is the rest of that.

## The end value

One skill refines personas, workflows and journeys. It says the shared interview once, and keeps every rule each layer had.

**How we would know it worked:**
- `refine` fires on every case the three skills held, and on none of the three should-not-fire cases.
- `refine-personas`, `refine-workflows` and `refine-journeys` no longer exist. An instruction naming one is reported with its new name.

## What changes

1. **`skills/refine/SKILL.md` replaces the three** (331 lines, from 765):
   - which layer is what the request is about; a change touching two is two changes, persona before workflow before journey;
   - the three refusals, under one tell: the order of arrival;
   - the reading, the claim block, the interview (shared rules, then what each layer asks for), the play-back — once;
   - *Personas: hold every line to a test*, the tester, delete-not-shelve; *Workflows: hold it against the definition*, the job story, declarative examples, the phase, shrink; *Journeys: the anatomy*, the title, its own layer;
   - one gate table, its eight rows read against the ledger, with what bites each layer;
   - one hand-back, each layer's diff shown alone first;
   - the sources, grouped by layer.
2. **The three become former skill names** mapping to `refine`, so `check:skill-names` reports an instruction still using one.
3. **Eval cases.** The twenty-one that held a `refine-*` skill hold `refine`. Tags and `skill-fired` graders move. The three should-not-fire cases (51, 56, 61) still hold: each is an explanatory question, not a request to refine.
4. **The record.**
   - `setup`, `refine-spec`, the README table, `specs/README.md` and `evals/README.md` name `refine`.
   - "seven skills" becomes "five".
   - Old change specs pin the deleted files at their last commit.
   - The `skills/` ceiling is lowered to the measured 2,329.

## What we are not doing

- **Rewriting dated accounts.** An eval run that measured `refine-personas` still says so.
- **Merging `refine-spec` in.** It refines a feature request into a change, against the features. These three refine the layers that request is judged against.
- **New rules.** Every rule the three skills carried is kept, reworded only where saying it once needed that.

## Ids

unchanged
