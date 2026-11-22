# Spec 0104: the key table, held

- **Status:** approved in advance, by the maintainer, 2026-11-22 ("Do however you feel right" … "go")
- **Issue:** [#214](https://github.com/sargismarkosyan/livespec/issues/214)
- **Sketch:** not drawn — approval given in advance

## Who this is for

**[`agent-accelerated-owner`](../personas/agent-accelerated-owner.md), in [`adopt-the-process`](../workflows/adopt-the-process.feature)**, at *The changes after*. A row their bindings lack is a question every later session answers by guessing.

## The job behind the request

To know the bindings answer everything the template asks.

## Why now

This repository's bindings lacked five rows of the template's key table. Three were renamed for graded cases, and two were simply missing. `check:ledger-shape` reads only the ledger tables, so nothing noticed ([#214](https://github.com/sargismarkosyan/livespec/issues/214)).

## The end value

A key row the template carries and the bindings lack reads open by name. A graded-case repository's own names for its rows count.

**How we would know it worked:** `check:key-table-shape` reads open with a row removed, and clear with *How a case names its rule* and *Case discovery* in place of the test-shaped rows. On this repository it reads clear, all 33 rows.

## What changes

1. **`check:key-table-shape`** (mechanical, record) in `tools/doctor.py` and [`requirements.md`](../../method/requirements.md). It compares the template's key table with the bindings', by name or by alias. The aliases are *How a case names its rule*, *Case discovery* and *Deliverable of a version*.
2. **[The template](../../templates/bindings.md)** names each graded-case form beside its row, so a repository fills it in rather than renaming it.
3. **This repository's bindings** gain *Coverage gate* and *What coverage does not reach*, both answered by `gate:coverage`'s decided *not applicable*.
4. **`@rule:the-key-table-is-held-to-the-template`** in [`ledger-claims.feature`](../features/wiring/ledger-claims.feature), claimed by `KeyTable`. One fault. The gate fixture gains its four missing rows and a two-row template.

## What we are not doing

- **Fewer rows.** [#193](https://github.com/sargismarkosyan/livespec/issues/193) is where rows go away.
- **Rows the template lacks.** The extra rows a repository keeps are its own.

## Ids

added: `check:key-table-shape`
