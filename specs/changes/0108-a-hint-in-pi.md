# Spec 0108: a hint, in Pi

- **Status:** approved in advance, by the maintainer, 2026-11-22 ("Do however you feel right" … "go"; then "continue with the remaining open items")
- **Issue:** [#191](https://github.com/sargismarkosyan/livespec/issues/191), its Pi half. The Claude Code half waits on plan v28 §8's proxy verification, which bills the maintainer's account.
- **Sketch:** not drawn — approval given in advance

## Who this is for

**[`agent-accelerated-owner`](../personas/agent-accelerated-owner.md), in [`adopt-the-process`](../workflows/adopt-the-process.feature)**, at *The changes after*. Nothing tells them an upgrade is waiting until somebody happens to run the audit.

## The job behind the request

To see, on opening a session, that this repository has livespec work waiting, without the model being told.

## Why now

[`0105`](0105-the-upgrade-on-file.md) made what is pending computable (`planned()`), and [`0106`](0106-the-pi-tag.md) the ceiling. Both are what a hint needs to say. The maintainer's first fixed decision (plan v28 §0) is that the hint never enters the model's conversation. Pi's footer status does not.

## The end value

Under Pi, a footer line, first match wins:
- this session's plugin is older than the ledger;
- *N pending · /skill:setup brings it up to date*;
- a newer release exists.

It is silent with no bindings, with `LIVESPEC_NO_HINT`, or on any failure.

**How we would know it worked:**
- `tests/test_behind.py` holds the three lines and the silences;
- the gate fails an extension that imports outside Pi and `node:` or calls anything that reaches the model;
- here, where every row is level, the line is empty.

## What changes

1. **[`tools/behind.py`](../../tools/behind.py)** (payload). It reads files only, through `doctor.context(…, git_reads=False)`. `--fetch-latest` runs `git ls-remote --tags` from the cache directory, never the repository, with a 3 s timeout and no prompt, and caches the newest release for a day.
2. **`extensions/livespec-hint.ts`** (component, Pi only, found by Pi's conventional directory with no manifest):
   - on `session_start`, with a UI only, it runs `behind.py` and sets the footer status;
   - it fetches unawaited, then refreshes, and refreshes again on `agent_settled` while shown;
   - it clears on shutdown.
3. **`checks.py`** holds every extension to imports from Pi and `node:` only, and to no call that reaches the model. One fault proves it.
4. **The component definition** in [`spec.md`](../spec.md), `setup`'s sitting naming the hint, and `extensions/` gets a ceiling of its own.
5. **`@rule:the-hint-is-the-persons-alone`**, claimed by `tests/test_behind.py`.

## What we are not doing

- **The Claude Code hook.** It ships only if a logging proxy shows `systemMessage` never reaches a request (plan v28 §8). That run drives `claude` and bills the maintainer, and has not been approved.
- **Plan v28 §2 B's personal-pin table.** That covers trust, a personal pin and an `autoload: false` delta. The line says *move the Pi pin, or pi update*.
- **A runtime test of the shim.** It is verified by hand, as plan v28 accepted.

## Ids

unchanged
