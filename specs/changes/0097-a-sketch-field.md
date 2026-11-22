# Spec 0097: a sketch field

- **Status:** approved in advance, by the maintainer, 2026-11-22 ("Do however you feel right" … "go")
- **Issue:** [#216](https://github.com/sargismarkosyan/livespec/issues/216)
- **Sketch:** not drawn — one header line and the sentence that fills it; the prose carries all of it.

## Who this is for

**[`agent-accelerated-owner`](../personas/agent-accelerated-owner.md), in [`adopt-the-process`](../workflows/adopt-the-process.feature)**, at *The changes after*. Reading a change spec later, they cannot tell whether a sketch was drawn, skipped, or forgotten.

## The job behind the request

To know from the spec alone what became of its sketch.

## Why now

- The self-audit of 1.32.1 found the template has no `Sketch:` field ([#216](https://github.com/sargismarkosyan/livespec/issues/216)). Specs say it ad hoc, or not at all ([0081](0081-a-closing-line-that-closes.md)).
- The history check in [#210](https://github.com/sargismarkosyan/livespec/issues/210) will read this field, and a field nobody fills cannot be read.

## The end value

Every change spec says in its header whether a sketch was drawn and where, or why not.

**How we would know it worked:** a spec written from the template carries a `Sketch:` line, and case 29's spec says *not drawn* with its reason.

## What changes

1. **[`templates/change.md`](../../templates/change.md)** gains `**Sketch:** drawn — <where> | not drawn — <the one line why>`. The three reasons are named: nothing the prose cannot carry, no way to render one here, and approval given in advance.
2. **`refine-spec`** says the spec's `Sketch:` line keeps the answer, drawn or not.
3. **`an-absent-sketch-is-said-rather-than-filled`** gains *the spec keeps what became of the sketch*, claimed by a new grader on case 29: the spec it writes says *not drawn*, and why.

## What we are not doing

- **Backfilling old specs.** They are dated accounts.
- **Checking the field.** That is [#210](https://github.com/sargismarkosyan/livespec/issues/210)'s history check.

## Ids

unchanged
