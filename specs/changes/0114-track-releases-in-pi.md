# Spec 0114: track releases in Pi

- **Status:** approved by the maintainer, 2026-11-22: "Unpinned by default (Recommended)", after "I suspect that it will dynamically check if there is a new version available of the Pi plug-ins and recommend to upgrade it like it does with any other Pi plug-in."
- **Issue:** [#191](https://github.com/sargismarkosyan/livespec/issues/191)
- **Sketch:** not drawn — one line in a settings file, and the prose carries it

## Who this is for

**[`agent-accelerated-owner`](../personas/agent-accelerated-owner.md), in [`adopt-the-process`](../workflows/adopt-the-process.feature)**, at *The changes after*. Pi tells them when any other package has a release. livespec, as `setup` declared it, never did.

## The job behind the request

To learn that livespec has a release the way they learn it for every other Pi package.

## Why now

- The maintainer's repository, wf-developer-agents, sat on livespec 1.16.3 for two months. Pi showed no update, and the [`0108`](0108-a-hint-in-pi.md) hint cannot reach a session loading 1.16.3.
- Pi 1.5.2 checks every git package for updates except a pinned one (`dist/core/package-manager.js:1059–1062`: `if (parsed.type === "local" || parsed.pinned) return undefined;`). `setup` §8 pinned livespec to a release tag.

## The end value

A repository `setup` declares for Pi gets Pi's own *Package updates are available* when livespec releases. The footer hint then says what is pending here. A team that wants one version for everyone can still pin, knowing nothing announces a release.

**How we would know it worked:** `setup` writes `git:github.com/sargismarkosyan/livespec` with no ref, and case 85's grader holds that. The hint says *pi update* where nothing is pinned, and *move the Pi pin* where something is.

## What changes

1. **`setup` §8 and [`method/README.md`](../../method/README.md)** declare livespec for Pi with no ref. Merging is releasing, so the default branch is the latest release. The pin is an option when asked for, with the trade-off said.
2. ***Bring it up to date*** offers a pinned repository the switch once. A kept pin still bounds the ledger ([`0106`](0106-the-pi-tag.md)).
3. **`behind.py`** words its step by whether the repository pins.
4. **`the-sitting-enables-livespec-for-each-host-in-use`**'s example, and case 85's grader (renamed `tracks-releases-for-pi`), expect no ref.

## What we are not doing

- **Reaching a repository already pinned below 3.11.0.** The code it loads cannot change. Dropping its pin once is a one-line edit, made for wf-developer-agents on its own branch.
- **Retiring `check:host-pin-current`.** A kept pin is still checked.

## Ids

unchanged
