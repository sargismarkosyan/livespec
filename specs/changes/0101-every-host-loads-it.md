# Spec 0101: every host loads it

- **Status:** approved in advance, by the maintainer, 2026-11-22 ("Do however you feel right" … "go")
- **Issue:** [#211](https://github.com/sargismarkosyan/livespec/issues/211)
- **Sketch:** not drawn — approval given in advance

## Who this is for

**[`agent-accelerated-owner`](../personas/agent-accelerated-owner.md), in [`adopt-the-process`](../workflows/adopt-the-process.feature)**, at *Putting it in* and *The changes after*. Their agents run under more than one host. A host that never loads the plugin runs the repository with no skill, and the session looks ordinary.

## The job behind the request

To know every host in use here loads livespec from what the repository commits.

## Why now

- **This repository ran its own self-audit under Pi with no livespec skill loaded** ([#211](https://github.com/sargismarkosyan/livespec/issues/211)). [`0092`](0092-the-plugin-held-to-itself.md) fixed the declaration, and nothing would notice it going missing again.
- **`setup` §8 knew one shape**: a remote package pinned to a tag. The plugin's own repository loads its checkout instead.

## The end value

The report names each host in use and where it is declared. A host in use with no declaration reads open.

**How we would know it worked:** `check:host-enabled` reads open for a Pi settings file that loads no livespec, and for an audit run from Pi in a repository declaring only Claude Code. On this repository it reads clear, naming `livespec@livespec` and `".."`.

## What changes

1. **`check:host-enabled`** (mechanical, wiring) in `tools/doctor.py` and [`requirements.md`](../../method/requirements.md).
   - Hosts in use: the one running the audit, Claude Code where the tree has `.claude/` or `CLAUDE.md`, and Pi where it has `.pi/` or `AGENTS.md`.
   - Claude Code is declared by an enabled `livespec@…` in `.claude/settings.json`.
   - Pi is declared by a `packages` entry naming livespec, or a local path to a livespec checkout.
2. **`setup` §8** gains the self-hosting paragraph: Pi's relative path, and Claude Code's copy registered per machine.
3. **`@rule:every-host-in-use-loads-it`** in [`the-host.feature`](../features/wiring/the-host.feature), claimed by `EveryHost`. One fault: *a host in use that loads no livespec*. The fixtures declare both hosts.

## What we are not doing

- **Checking the pin's version.** That is [#190](https://github.com/sargismarkosyan/livespec/issues/190)'s tag model.
- **Proving the host loaded it.** Trust, and what a session actually loaded, are outside the tree. The declaration is what a fresh clone gets.

## Ids

added: `check:host-enabled`
