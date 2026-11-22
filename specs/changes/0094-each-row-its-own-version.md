# Spec 0094: each row its own version

- **Status:** approved in advance, by the maintainer, 2026-11-22
- **Issue:** [#189](https://github.com/sargismarkosyan/livespec/issues/189)
- **Sketch:** skipped, because approval was given in advance.
- **Design:** the upgrade plan both reviewers scored 10/10, §5 ([gist](https://gist.github.com/sargismarkosyan/dd1db9368600aafc359584ea9a85b6f8)). This spec is the part that stands without [#190](https://github.com/sargismarkosyan/livespec/issues/190).

## Who this is for

**[`agent-accelerated-owner`](../personas/agent-accelerated-owner.md), in [`adopt-the-process`](../workflows/adopt-the-process.feature) at *The changes after*.** Their ledger stops claiming one version for every row when the rows were reconciled at different times.

## The job behind the request

To say honestly how far a repository's wiring is up to date when some rows have caught up with a release and others have not. One stamp for the whole ledger cannot say that: it is either stale for the rows that moved or a lie for the rows that did not.

## Why now

- **A partial upgrade has no correct stamp** ([#189](https://github.com/sargismarkosyan/livespec/issues/189)). Wire two of three new gates and the line is wrong either way, so in practice it never moves.
- [#190](https://github.com/sargismarkosyan/livespec/issues/190) plans and applies upgrades per row, and needs a per-row version to read and write.
- [`0093`](0093-a-meaning-that-moved.md) gave the list a `revised` column. This gives the ledger the column it is compared against.

## The end value

Each gate and wiring row in a ledger says the release it was last reconciled at. The stamp line reads the oldest of them, and the audit checks the line against the rows.

**How we would know it worked:**
- `doctor` reads a ledger with the column and opens `check:stamp-derived` when the line is not the oldest row.
- It opens `check:ledger-shape` on a ledger without the column, with every other check still reading.
- livespec's own release writes every row and the line.

## What changes

1. **The column.** The gate and wiring tables gain a last column, `reconciled`, holding a release. A `local:` row reads `—`; the boundaries table gets no column.
   - [`templates/bindings.md`](../../templates/bindings.md) carries it, and says who writes it.
   - This repository's ledger carries it at 1.36.0.
2. **The audit reads it** ([`tools/doctor.py`](../../tools/doctor.py)):
   - `ledger_rows` reads the column by header and leaves it out of the evidence;
   - **`check:ledger-shape` is revised**: a ledger in the template's shape but without the column reads `open`, while every check that reads the tables still runs, each row reading as the stamp;
   - **new `check:stamp-derived`** (mechanical, record): the stamp line reads the oldest version among the gate and wiring rows; a row with no version, or a line that is not the oldest, reads `open`;
   - `--reshape` prints the column, filled with the stamp.
3. **Setup writes it**: `doctor.py --adopt [bindings] [ids…]` writes the reconciled cell of every row (or the ids given) at the plugin installed, then writes the stamp line as the oldest, dated today.
   - [`setup`](../../skills/setup/SKILL.md) runs it once the rows are written, and moves a row's version only when its wiring moved.
   - The audit never runs it: reading still never moves a version.
4. **The release writes it**: `releaselib.stamp_ledger` writes every gate and wiring row's cell to the release, beside the line, so livespec's own ledger agrees by construction.
5. **Table cells may hold a literal pipe.** `cells_of` splits only on an unescaped `|`. This repository's `wiring:pr-report` evidence had an unescaped one in a code span, which already broke its rendering, and is escaped.
6. **Faults and a control** (`inject.py`):
   - faults: *a ledger with no reconciled column* (`ledger-shape` opens) and *a stamp line that is not its oldest row* (`stamp-derived` opens);
   - the control: the release reconciles every row and leaves a `local:` row alone;
   - the fixture is reconciled at its own version.
7. **The id list**: `check:stamp-derived` added (`since: next`); `check:ledger-shape` revised (`revised: next`), the first use of [`0093`](0093-a-meaning-that-moved.md)'s column.
8. **Ceilings** rise by what remained after trimming, with the reason beside them.

**Rules added or changed:** none. The new check is held by `every-mechanical-check-is-proven-to-fire`, and `a-reading-leaves-the-stamp-where-it-was` stays true word for word: the audit still never writes a version.

## What we are not doing

- **Planning and applying from the cells**: [#190](https://github.com/sargismarkosyan/livespec/issues/190).
- **Holding the cells to HEAD** (refusing a cell an audit changed): it needs the third git command, which [#190](https://github.com/sargismarkosyan/livespec/issues/190)'s hardening adds.
- **The tag cap and Answers**: also #190.
- **Retiring `a-reading-leaves-the-stamp-where-it-was`**: it stays true until #190 changes who raises a cell.

## Data

A consuming repository's ledger grows a column the next time `setup` reshapes it. Until then, every row reads as the stamp and `ledger-shape` says so, as a drift finding only.

## Risks

- **An older doctor reading a new ledger** reads the extra column as part of the evidence. That is harmless: no older check parses the evidence's last word.
- **A hand-edited cell** is not detected yet; that waits for the HEAD check in #190.

## Acceptance checks

1. `python3 .github/scripts/verify.py` is green.
2. `python3 tools/doctor.py specs/setup/README.md` reads `check:ledger-shape` and `check:stamp-derived` clear.
3. `stamp_ledger` on this repository's ledger changes the 32 reconciled cells and the stamp line, and nothing else.
