# Spec 2026-11-25: a release is not a change

- **Status:** approved in advance, by the maintainer, 2026-11-25 ("Open an MR in livespec too", after the two findings were put to them)
- **Issue:** [#273 The audit reads a release as a change](https://github.com/sargismarkosyan/livespec/issues/273)
- **Sketch:** not drawn — approval given in advance

## Who this is for

**[`agent-accelerated-owner`](../personas/agent-accelerated-owner.md), in [`adopt-the-process`](../workflows/adopt-the-process.feature)**, at the audit and the upgrade after it: reading which lines are open, and bringing the ledger level.

## The job behind the request

An open line in the audit means something here needs doing.

## Why now

Auditing helios/project-metrics-mfe on 3.18.3, two lines stayed open over nothing to do. `check:loop-followed` reported five commits as following neither the loop nor the light path. They were its release bot's `v0.0.10` … `v0.0.14`, and each changes only `"version"` in `package.json`. Bringing the ledger from 3.18.2 to 3.18.3 opened a transaction with no items, because 3.18.3 asked nothing of the ledger, and finalizing it raised no row. So the stamp stayed at 3.18.2 and `check:stamp-range` stays open until a later release happens to ask something.

## The end value

An audit whose open lines are all real: a release commit is not read for a loop, and an upgrade that found nothing to do leaves the ledger level.

**How we would know it worked:** the same repository audited again reads `check:loop-followed` clear over its release commits, and an upgrade of 0 items finalizes with the stamp at the plugin installed.

## What changes

1. **`doctor.py`, `check:loop-followed`**: a commit on the main line whose every changed line is a manifest's version (`"version": "…"`, `version = "…"`, `<version>…</version>`) is passed over. A commit changing anything else is read as before.
2. **`doctor.py`, `--finalize`**: every row no item in the transaction names, for an id the list still carries, is raised to the release with the answered rows. The plan already found that the range asked nothing of it. Rows are never lowered, and the Pi tag still caps the raise.

**Rules added or changed**:

| Rule id | Feature file | New or changed |
|---|---|---|
| `the-loop-is-read-from-the-history` | [`wiring/what-an-audit-reads.feature`](../features/wiring/what-an-audit-reads.feature) | changed — an Example: a release commit is not a change |
| `finalize-raises-what-was-answered` | [`wiring/what-changed-since-the-stamp.feature`](../features/wiring/what-changed-since-the-stamp.feature) | changed — reworded to raise each row no item names, and an Example: a release that asked nothing |

## What this removes

Nothing.

## What we are not doing

- **Naming the release bot.** The commit's diff, not its author, says that it is a release.
- **Moving the stamp from the audit.** `a-reading-leaves-the-stamp-where-it-was` stands: only the sitting's `--finalize` raises rows.

## Ids

unchanged — `check:loop-followed` and `--finalize` read the same history and the same ledger. What they ask of a repository does not move.
