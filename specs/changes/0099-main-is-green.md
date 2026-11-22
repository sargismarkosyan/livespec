# Spec 0099: main is green

- **Status:** approved in advance, by the maintainer, 2026-11-22 ("Do however you feel right" … "go")
- **Issue:** [#209](https://github.com/sargismarkosyan/livespec/issues/209)
- **Sketch:** not drawn — approval given in advance

## Who this is for

**[`agent-accelerated-owner`](../personas/agent-accelerated-owner.md), in [`adopt-the-process`](../workflows/adopt-the-process.feature)**, at *The changes after*. Merging is releasing, so a red main branch reaches every install, and the person finds out when somebody else does.

## The job behind the request

To know at each audit whether what was released was green.

## Why now

- **This repository's main branch was red for a month.** The `checks` job failed on every push from 2026-10-23 to 2026-11-21, through two releases ([#209](https://github.com/sargismarkosyan/livespec/issues/209)).
- **No check asks.** The platform checks read the *settings* (merges blocked, the check's name). None reads whether the pipeline actually passed.

## The end value

The report says whether the main branch is green now, and whether it was red at any point since the last audit, naming the first and the last red run.

**How we would know it worked:** `check:main-green` (judgment, platform severity) reads:
- *open* with no row;
- the row's command plus the last audit's date, for a mind to run and answer;
- *n/a* where nothing runs.

## What changes

1. **A bindings row, *The main branch's runs*.** It names the platform's command that lists the runs, or *not applicable, decided*. It is in the template, `setup`'s sitting writes it, and this repository's bindings carry it.
2. **`check:main-green`** in `tools/doctor.py` and [`requirements.md`](../../method/requirements.md). The report's line in `setup` says what makes it open.
3. **`@rule:main-is-read-green`** in [`many-merges.feature`](../features/wiring/many-merges.feature), claimed by `MainGreen` in `tests/test_doctor.py`.

## What we are not doing

- **Running the command from the tool.** The audit stays offline. The command is handed to the mind answering, like every platform line.
- **The hint.** Showing "main is red" between audits is [#191](https://github.com/sargismarkosyan/livespec/issues/191)'s.

## Ids

added: `check:main-green`
