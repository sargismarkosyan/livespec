# Spec 0103: a read-back ages

- **Status:** approved in advance, by the maintainer, 2026-11-22 ("Do however you feel right" … "go")
- **Issue:** [#212](https://github.com/sargismarkosyan/livespec/issues/212)
- **Sketch:** not drawn — approval given in advance

## Who this is for

**[`agent-accelerated-owner`](../personas/agent-accelerated-owner.md), in [`adopt-the-process`](../workflows/adopt-the-process.feature)**, at *The changes after*. A read-back dated months ago reads as true today, and it is the only thing they have about the platform.

## The job behind the request

To know which claims about the outside no recent audit has read again.

## Why now

This repository's bindings read "Last read back on 2026-08-29" for three months, through ten releases, and every audit accepted it ([#212](https://github.com/sargismarkosyan/livespec/issues/212)). `check:read-back-or-not` asks *whether* a line was read back, never *when*.

## The end value

A read-back dated before the last audit reads open, naming its line and its date.

**How we would know it worked:** `check:read-back-age` reads open for a read-back older than the last audit record. It reads clear when the last audit moved every date, and *n/a* before any audit.

## What changes

1. **`check:read-back-age`** (mechanical, record) in `tools/doctor.py` and [`requirements.md`](../../method/requirements.md). It finds every *read back … YYYY-MM-DD* in the bindings and compares each with the last audit record's date.
2. **The template's *Branch protection*** says the date is written as *read back on YYYY-MM-DD*, and every audit moves it once it has read it again.
3. **`@rule:a-read-back-ages-from-the-last-audit`** in [`ledger-claims.feature`](../features/wiring/ledger-claims.feature), claimed by `ReadBackAge`. One fault: *a read-back older than the last audit*.

## What we are not doing

- **The previous release as the clock**, which the session first chose. A release of the plugin says nothing about a consumer's platform. Here it comes several times a day, and many consumers never release. The last audit is the event that should have read it again. A date it left behind is the finding.
- **A number of days in the bindings.** Nothing asks for one yet.

## Ids

added: `check:read-back-age`
