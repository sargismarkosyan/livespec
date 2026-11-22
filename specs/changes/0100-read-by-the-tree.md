# Spec 0100: read by the tree

- **Status:** approved in advance, by the maintainer, 2026-11-22 ("Do however you feel right" … "go")
- **Issue:** [#213](https://github.com/sargismarkosyan/livespec/issues/213)
- **Sketch:** not drawn — approval given in advance

## Who this is for

**[`agent-accelerated-owner`](../personas/agent-accelerated-owner.md), in [`adopt-the-process`](../workflows/adopt-the-process.feature)**, at *The changes after*. An audit that passes a reason nobody can check leaves them believing a gap is closed.

## The job behind the request

To have a *not applicable* reason, and a gap named in prose, read against what the repository actually holds.

## Why now

The self-audit of 1.32.1 passed two things it never read ([#213](https://github.com/sargismarkosyan/livespec/issues/213)):
- `gate:coverage` read "no application code to measure" beside ~1,470 shipped lines of `tools/`. `na-vs-tree` understands only layer claims.
- "## Three more attempts, not written yet" in the workflows README. `prose-phrases` looks for four phrases, in the bindings only.

## The end value

A no-code reason beside code in the tree reads open. A reason the tool cannot read is named rather than passed. A gap in a layer's README is put to a mind.

**How we would know it worked:** on this repository, `prose-phrases` asks about `specs/workflows/README.md:L51 'not written yet'`, and `na-vs-tree` names the nine rows whose reasons it cannot read.

## What changes

1. **`check:na-vs-tree`** (revised): an undecided *not applicable* saying *no code*, *no app* or *nothing to measure* is read against the source files the tree tracks, outside specs, tests, docs and dot directories. It is open with how many and where. A reason naming no layer and no code is listed in the evidence as not read against the tree.
2. **`check:prose-phrases`** (revised): it also reads each layer's README, and the phrases gain *not written yet*, *not wired yet* and *uninterviewed*. `setup`'s report names them.
3. Three examples, on [`a-decided-exception-is-reported-once-and-never-relitigated`](../features/audit/the-reply.feature) and [`a-gap-is-a-row-not-a-sentence`](../features/wiring/ledger-claims.feature), claimed by three tests.

## What we are not doing

- **This repository's coverage row.** It already reads *not applicable, decided*, since [`0092`](0092-the-plugin-held-to-itself.md).
- **Making an unread reason open.** The tool cannot say it is wrong, only that it did not read it.

## Ids

revised: `check:na-vs-tree`, `check:prose-phrases`
