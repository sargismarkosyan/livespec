# Spec 0098: the loop, read back

- **Status:** approved in advance, by the maintainer, 2026-11-22 ("Do however you feel right" … "go")
- **Issue:** [#210](https://github.com/sargismarkosyan/livespec/issues/210)
- **Sketch:** not drawn — approval given in advance

## Who this is for

**[`agent-accelerated-owner`](../personas/agent-accelerated-owner.md), in [`adopt-the-process`](../workflows/adopt-the-process.feature)**, at *The changes after*. Their agents merge changes they do not read one by one, so whether the loop was followed is only known if something reads it back.

## The job behind the request

To know, at each audit, whether every change merged since the last one followed the loop or took the agreed light path.

## Why now

- The self-audit of 1.32.1 passed 47 of 49 checks while [#203](https://github.com/sargismarkosyan/livespec/pull/203) had merged a CI fix with no issue and no spec. Specs had also skipped their sketches with no line saying so. No check reads the history ([#210](https://github.com/sargismarkosyan/livespec/issues/210)).
- The session decided two rules:
  - a small pipeline fix takes a light path;
  - approval given in advance is a legitimate reason to skip a sketch.

  The method says neither yet.
- [`0097`](0097-a-sketch-field.md) put a `Sketch:` line in the template, so it can be read.

## The end value

The report says which merged changes followed neither the loop nor the light path. It never fails a build on it.

**How we would know it worked:** `check:loop-followed` reads open on a change merged with no spec and no issue, and on code committed before its spec. It reads clear on the light path, on spec first, and on a squash it cannot order. On this repository it names 0090 and 0091, whose specs carry no `Sketch:` line.

## What changes

1. **[`process.md`](../../method/process.md)**:
   - *Feedback is never fixed on the spot* gains the light path: an issue first, and a line in the pull request saying why no spec was owed.
   - The sketch's exemptions gain approval given before the spec existed. The spec's header keeps which reason applied.
2. **`check:loop-followed`** (mechanical, record) in `tools/doctor.py`. It reads each first-parent change from the last audit record's `HEAD` to now:
   - with no added change spec, it needs an issue named in the branch's commits (merge-commit and squash `(#N)` titles are pull requests, not issues);
   - with one, each added spec needs a `Sketch:` line;
   - on a merged branch, it needs a `spec NNNN:` commit before any commit touching files outside `specs/`.

   With no previous audit it is *n/a*.
3. **`@rule:the-loop-is-read-from-the-history`** in [`what-an-audit-reads.feature`](../features/wiring/what-an-audit-reads.feature), claimed by `TheLoop` in `tests/test_doctor.py`. One fault, *a change merged with no spec and no issue*.

## What we are not doing

- **Reading pull request bodies.** The light path's line lives on the platform. The audit reads git only and stays offline: an issue named is the evidence.
- **Ordering squash merges.** One commit cannot show which came first.
- **Fixing 0090 and 0091.** Their record is the report's to show.

## Ids

added: `check:loop-followed`
