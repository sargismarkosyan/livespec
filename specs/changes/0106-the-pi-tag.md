# Spec 0106: the Pi tag

- **Status:** approved in advance, by the maintainer, 2026-11-22 ("Do however you feel right" … "go"; then "continue with the remaining open items")
- **Issue:** [#190](https://github.com/sargismarkosyan/livespec/issues/190), the Pi pin model (plan v28 §2 A)
- **Sketch:** not drawn — approval given in advance

## Who this is for

**[`agent-accelerated-owner`](../personas/agent-accelerated-owner.md), in [`adopt-the-process`](../workflows/adopt-the-process.feature)**, at *The changes after*, with collaborators under both hosts. Pi never moves a pinned tag on update. A ledger raised past the pin claims wiring a Pi collaborator's plugin does not know about.

## The job behind the request

To keep what the ledger says it was reconciled with no newer than what the repository makes Pi load.

## Why now

[`0105`](0105-the-upgrade-on-file.md) made the upgrade a transaction. Without a cap, a Claude Code sitting raises rows above the project's Pi tag, and nothing says so.

## The end value

The Pi pin bounds the ledger. A raise stops at the pin. A sitting ahead of the pin plans the pin's move. A pin below the ceiling, or on a branch nobody chose, reads open.

**How we would know it worked:**
- `check:host-pin-current` reads open below the ceiling, open on an unkept branch, n/a on a kept one, and clear at or above the ceiling.
- A finalize above the pin raises only as far as the pin, holds the gate, and keeps the transaction open.
- The tag's own item never keeps a transaction open.

## What changes

1. **`check:host-pin-current`** (mechanical, wiring) in `tools/doctor.py` and [`requirements.md`](../../method/requirements.md). It reads the `livespec` git entry in `.pi/settings.json`:
   - a `livespec--v` tag below the ledger's ceiling is open;
   - another ref is open unless the bindings say `decided: non-release pin kept <ref>`;
   - no ref, or a local checkout, is n/a.
2. **The cap.** `--finalize` raises to the lower of the transaction's release and the pin. An answered item above the pin is finalized *held*: it is pending for closure, and raised by a later finalize once the pin moves. `--adopt` seeds rows at the lower of the plugin installed and the pin. A cell is never lowered.
3. **The tag's item.** `--plan --write` adds `host:tag@<installed>@sitting#N` when the pin is behind the plugin installed. It is never counted toward closure. `setup` moves the pin only after `git ls-remote` shows the exact tag, in its own commit, with a yes. The same verified edit, touching no row, moves Pi ahead without an upgrade.
4. **`@rule:the-pi-tag-bounds-the-ledger`** in [`the-host.feature`](../features/wiring/the-host.feature), claimed by `ThePiTag`. One fault: *a Pi pin on a branch*.

## What we are not doing

- **`check:host-pin-binding` and a Host pin row** (plan v28). Pi reads only `<root>/.pi/settings.json`, so a row naming that path is a second copy of a fact the tool already knows. The kept-ref marker is read anywhere in the bindings.
- **`--verified-tag` and `--settings-writable` flags.** The skill verifies before it edits; the tool never writes the pin.
- **The session's own pin state**, which is personal settings and trust. That belongs to the hint ([#191](https://github.com/sargismarkosyan/livespec/issues/191)).

## Ids

added: `check:host-pin-current`
