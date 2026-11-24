# Spec 2026-11-23: a retired gate leaves nothing behind

- **Status:** approved in advance, by the maintainer, 2026-11-23 ("ok carry on fixing them and merged automatically")
- **Issue:** [#262](https://github.com/sargismarkosyan/livespec/issues/262)
- **Sketch:** not drawn — approval given in advance

## Who this is for

**[`agent-accelerated-owner`](../personas/agent-accelerated-owner.md), in [`adopt-the-process`](../workflows/adopt-the-process.feature)**, at *The changes after*: bringing a repository up to a release that retired a gate.

## The job behind the request

When livespec stops asking for a gate, the repository stops running it and stops describing it.

## Why now

3.15.0 retired `gate:change-number-unique`. Bringing helios/wf-developer-agents up to it, `doctor.py --plan` listed one item, *drop the row*, and the session called the plan complete ([#262](https://github.com/sargismarkosyan/livespec/issues/262)). The repository's own gate (`npm run trace --changes`) still refused a second dated spec in a year, and about ten places still described numbered specs.

## The end value

A retired gate's upgrade item says what to remove there, its command from the row and what replaced it, and the sitting removes them in the commit that drops the row.

**How we would know it worked:** the plan's *retire* item for a row naming a command carries that command and the replacement, and says the fault and the prose go with it.

## What changes

1. **`doctor.py --plan`**: a *retire* item names the command the row ran, what replaced the id, and that the command, its fault and the prose describing it go with the row.
2. **[`setup`](../../skills/setup/SKILL.md)**, *Bring it up to date*: the outcome *retired* is the row dropped with what it named here, in the same commit.

**Rules added or changed**:

| Rule id | Feature file | New or changed |
|---|---|---|
| `the-plan-is-read-from-the-list` | [`wiring/what-changed-since-the-stamp.feature`](../features/wiring/what-changed-since-the-stamp.feature) | changed — what the retire item names |

## What this removes

Nothing.

## What we are not doing

- **Finding the prose for the repository.** Where a retired gate is described is the sitting's reading; the tool names the gate, its command and its replacement.

## Ids

unchanged — the plan's wording for a retired id moves; no id's meaning does, and nothing a repository holds names the plan's wording.
