# Spec 0105: the upgrade, on file

- **Status:** approved in advance, by the maintainer, 2026-11-22 ("Do however you feel right" … "go"; then "continue with the remaining open items")
- **Issue:** [#190](https://github.com/sargismarkosyan/livespec/issues/190), its transaction (plan v28 §3, §4 and §7's `--finalize`). The Pi project tag and the tool's hardening follow as their own specs.
- **Sketch:** not drawn — approval given in advance

## Who this is for

**[`agent-accelerated-owner`](../personas/agent-accelerated-owner.md), in [`adopt-the-process`](../workflows/adopt-the-process.feature)**, at *The changes after*. An upgrade spans sittings, sessions and sometimes hosts, and their agents forget everything between them.

## The job behind the request

To pick an upgrade up where it stopped, and to have each row raised only for what was actually answered.

## Why now

- [`0095`](0095-setup-reports-and-brings-it-up-to-date.md) shipped *Bring it up to date* as five steps held only by the session. An interrupted sitting leaves nothing to resume from.
- A row was raised by `--adopt <ids>`, which the session had to list correctly. Nothing checked it against the report that followed.
- A check was owed an answer when it was newer than *the last audit*. An audit that read it `open` still counted as answering it.

## The end value

The upgrade's state is a committed file. A sitting resumes from it. A row moves only for an answer the after-report does not contradict, and a check counts as answered only once it reads clear.

**How we would know it worked:** `--plan --write` opens a transaction and refuses a second. `--finalize`:
- raises a wired row;
- vetoes a row a row-level line still finds;
- answers a check that reads clear;
- closes the transaction only when nothing is pending.

## What changes

1. **The upgrade ledger** (`specs/setup/upgrade.md`, or where the bindings' new *Upgrade ledger* row says). It holds:
   - *Answers*: each check and the release it was last answered at, under an *Answers baseline*;
   - *Sittings*: append-only;
   - *Transaction*: open or closed, from and to, each item keyed `<id>@<since|revised|retired>:<version>` with its kind, outcome, finalized flag and evidence, and a snapshot of every row's cell.
2. **`--plan`** reads a check's last answer from Answers, else the baseline, else the stamp, instead of the last audit record (plan v28 §4). **`--plan --write`** opens the transaction, refuses a second one to the same release, and extends an open one to a newer plugin.
3. **`--finalize`**:
   - refuses an outcome off the vocabulary, an answer with no evidence, a transaction to another release, or a record of another commit;
   - sends back to pending an answered row named on an `open` or `not-read` row-level line;
   - raises the rest, and never lowers a cell;
   - records a check as answered where it reads clear or n/a;
   - appends the sitting, and closes the transaction when nothing is pending.
4. **`--adopt`** creates the ledger on first adoption, its baseline at the plugin installed.
5. **`setup`'s *Bring it up to date*** resumes an open transaction, writes each item's outcome and evidence in the item's own commit, and finalizes against the second report.
6. **Rules:** `@rule:the-upgrade-is-a-transaction-on-file` and `@rule:finalize-raises-what-was-answered` in [`what-changed-since-the-stamp.feature`](../features/wiring/what-changed-since-the-stamp.feature), claimed by `TheTransaction`. `the-plan-is-read-from-the-list` now says *since it was last answered*.

## What we are not doing

These are deliberately left for later, against plan v28:
- **Drift items and host items.** The report's open wiring lines are still worked through by the same steps, but not keyed in the ledger.
- **The Pi project tag and its cap.** That is the next spec.
- **The `[ids: …]` prefix.** A row's id is matched in the row-level line's evidence as written.
- **Rewriting the after-record inside `--finalize`.** The skill reports once more instead.
- **The tool's hardening**, and the retired rules plan v28 §7 lists. That is the spec after.
- **New eval cases.** The sitting's behaviour is held by `tests/`; routing cases are re-measured when the maintainer asks.

## Ids

unchanged
