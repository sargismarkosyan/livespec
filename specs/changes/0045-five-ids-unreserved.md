# Spec 0045: five ids, unreserved

- **Status:** proposed
- **Issue:** [#107](https://github.com/sargismarkosyan/livespec/issues/107)
- **Depends on:** nothing to build. It stands behind
  [`0003`](0003-main-releases-itself.md), whose reservation it withdraws, and
  beside [`0042`](0042-the-release-writes-the-list.md) and
  [`0044`](0044-the-release-stamps-its-own-ledger.md), which practised the
  answer this spec writes down.

## Who this is for

**Nobody the product is for, and the spec says so.** It changes one sentence
of the method and withdraws a reservation in this repository's own record — a
contribution matter,
[workflows/README.md](../workflows/README.md) keeps such things out of the
persona's attempts, and it is the documented case in
[`process.md`](../../method/process.md#a-technical-change-that-serves-no-workflow-is-correct-not-a-gap).
What [`agent-accelerated-owner`](../personas/agent-accelerated-owner.md)
gets is what they get from every sentence that stops the method having two
answers: a gate that means one thing in every repository that has it.

## The job behind the request

The literal ask, from [#107](https://github.com/sargismarkosyan/livespec/issues/107):
*"Five rule ids reserved by 0003 have pointed at nothing for 34 releases:
the gate has no way to say a feature serves no workflow on purpose."*

The job: **the method should have one answer to what a feature that serves no
workflow is, and this repository's record should agree with it.** Today it
has two. `process.md` says a technical change *"serves no workflow, adds no
feature file"*. `0003` says five ids for such a feature are *"reserved by this
spec and permanent from here"* and that *"the file that carries them lands
with that decision."* Both sit in the tree. The decision they both waited on
was asked in #20 and answered by practice — the fault table is the pipeline's
contract — three times over since, in `0042`, `0043` and `0044`, none of which
wrote a feature file. The ids went on pointing at nothing.

What happens today instead: a reader of `0003` is told five permanent ids
exist; a reader of `specs/features/` finds none; and every change to the
release step spends a paragraph explaining which of the two to believe.

## Why now

Because the maintainer decided it, on 2026-09-16, asked with the three
answers side by side: **unreserve**. And because the alternative — a tag the
gate accepts in place of `@workflow:` — is a method change that would give
every consuming repository a way to file a feature no attempt traces to,
which is precisely the thing the feature → workflow direction exists to
refuse. A hole opened for five ids here would be open everywhere.

## The end value

One answer, written where the gate's meaning is written: a repository's own
pipeline — its gates, its release — is held by its fault table and reserves
no rule ids; a feature naming no workflow is refused and nothing is owed to
it. `0003`'s five ids are unreserved, never having been used, so nothing is
renamed and nothing is orphaned — `ids-are-permanent` is about ids that
exist, and these never did.

**How we would know it worked:** #107 closes with the sentence; the next
change to the release step spends no paragraph on which answer to believe;
and `grep -rn release-bumps-on-merge specs/` finds only the two dated
accounts, `0003` and this.

## What changes

1. **One sentence in [`gates.md`](../../method/gates.md)**, under *The same
   loop, one layer up*, after the failure table: a repository's own pipeline
   — the gates on this page, the step that releases — is not an attempt
   anybody makes with the product; it is held by the fault table this page
   ends with, and it reserves no rule ids. A feature naming no workflow is
   refused, and the answer is never a second kind of tag.
2. **The five ids are unreserved.** `0003` is left as written — a dated
   account is a record — and this spec is where the withdrawal is recorded:
   `release-bumps-on-merge`, `release-takes-its-number-from-the-label`,
   `release-takes-its-entry-from-the-body`,
   `release-refuses-without-its-inputs`, `release-does-not-release-itself`
   were reserved on 2026-08-25 and are not reserved from this change on.
   Nothing may still use them, because nothing ever did.
3. **#107 closes** with what was asked, what shipped, and why they differ.

**Rules added or changed:** none. That is the point.

## What we are not doing

- **Not editing `0003`.** A record edited to agree with the present is not a
  record; this spec is the later entry that supersedes it.
- **Not adding a tag** — `@workflow:none`, `@contract`, or any other — to the
  gate, here or in the method. Above.
- **Not writing the release contract as rules anywhere else.** The fault
  table is where it is stated, and the bindings' fault injection record is
  where it is read.

## Data

No storage; two files move — `method/gates.md` by a sentence, `specs/changes/`
by this file. `method/` moves, so the change ships: `patch`, a `## Changelog`
section, and — `gates.md` being on the audit surface — an `## Ids` section
reading *unchanged*. No `.feature` moves. `verify.py` exits **2** for the rows
already owed and no other reason.

## Risks

- **Somebody reads `0003` and not this.** The changelog entry names the
  withdrawal, and `0003` is the only place the ids appear besides here.
- **A future pipeline change wants a rule after all.** Then it argues for the
  tag this spec declines, in the open, as its own change — with this spec's
  reasoning to answer.

## Acceptance checks

1. `grep -rn "release-bumps-on-merge" specs/` → `0003` and `0045` only.
2. `method/gates.md` carries the sentence; `verify.py` exits 2 for the rows
   already owed.
3. #107 is closed with the three-part comment.
