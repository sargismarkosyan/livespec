# Spec 0102: the whole context file

- **Status:** approved in advance, by the maintainer, 2026-11-22 ("Do however you feel right" … "go")
- **Issue:** [#215](https://github.com/sargismarkosyan/livespec/issues/215)
- **Sketch:** not drawn — approval given in advance

## Who this is for

**[`agent-accelerated-owner`](../personas/agent-accelerated-owner.md), in [`adopt-the-process`](../workflows/adopt-the-process.feature)**, at *The changes after*. Their agents read the context file first. A rules list missing the rule this repository keeps breaking is the list they are working from.

## The job behind the request

To have the audit read the whole context file, not only its loop, and to have it ask about the rules this repository has actually broken.

## Why now

- **The audit re-reads only item 6** of *What must be there* (the loop). The other nine items are never read again after `setup` ([#215](https://github.com/sargismarkosyan/livespec/issues/215)).
- **[`0098`](0098-the-loop-read-back.md) made broken rules readable.** `check:loop-followed` names a change merged with no spec, or with its code committed first.

## The end value

The context file's judgment line asks after every item the method lists, by count. It also names each rule the history shows broken since the last audit, and asks whether the rules list carries it.

**How we would know it worked:** `check:loop-per-claude-md` asks after "all N items". After a change merged with no spec, it asks whether the rules list carries *spec before code*.

## What changes

1. **`check:loop-per-claude-md`** (revised) counts the items under *What must be there* in [`claude-md.md`](../../method/claude-md.md). It asks after each, and names the rules `check:loop-followed` found broken: *spec before code*, and the sketch's line. A line that is record is corrected; a rewrite stays the sitting's.
2. **`setup`'s report** says it the same way.
3. **`@rule:the-audit-reads-the-whole-context-file`** in [`context-file.feature`](../features/wiring/context-file.feature), claimed by `TheWholeContextFile`.

## What we are not doing

- **One line per item.** A single judgment line asks after all of them, so the record does not grow by nine lines.
- **This repository's `CLAUDE.md`.** It has carried *Spec before code* since [`0092`](0092-the-plugin-held-to-itself.md).

## Ids

revised: `check:loop-per-claude-md`
