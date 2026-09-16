# Spec 0044: the release stamps its own ledger

- **Status:** proposed
- **Issue:** none — the finding of three consecutive audits of this
  repository on 2026-09-16 (audits 2, 5 and 6), each run after a release,
  each finding the stamp one release behind and nothing else, each moving it
  by hand. The maintainer asked, after the third, to *"carry on with the next
  work item"*; this is it.
- **Depends on:** [`0042`](0042-the-release-writes-the-list.md), which made
  the release write the id table — the same step, one more file.

## Who this is for

**Nobody the product is for, and the spec says so.** This changes the
release step of *this* repository, a contribution step
[workflows/README.md](../workflows/README.md) keeps out of the persona's
attempts on purpose. It is the documented case in
[`process.md`](../../method/process.md#a-technical-change-that-serves-no-workflow-is-correct-not-a-gap),
and it has the shape [`0042`](0042-the-release-writes-the-list.md) already
has: a change spec, no feature file, a fault that holds it. What
[`agent-accelerated-owner`](../personas/agent-accelerated-owner.md) gets is
indirect and real — the audit this plugin runs on itself stops reporting a
finding that its own release step created, so the one repository every
consuming repository's audit is measured against reads level.

## The job behind the request

The literal ask is the pattern, not a sentence: three audits, three
re-stampings, three pull requests carrying nothing but the stamp.

The job: **in the plugin's own repository, the ledger's stamp should mean
what it means everywhere else — the version the wiring is level with — and
here that is always the version just released.** The bindings say why in
their own words: *"a release that moves the method moves the gates here in
the same merge, so the ledger is level with the plugin by construction."*
What is not level is the line, because the release commit bumps the version
*after* the audit ran. So every release leaves a stamp that is one behind and
true nowhere, and the next audit's first finding is the release step's own
side effect.

What happens today instead: a person runs the audit, moves the stamp, opens
a pull request for the record, and the release that merges it does not touch
the stamp — so the next one starts the cycle again.

## Why now

Because it has happened three times in one day and the record says so: the
bindings' stamp paragraph was rewritten in audit 6 to state the standing
fact once, and it ends *"the next change to the release step is where it
ends."* This is that change. And because `0042` already made the release
write a third file; a fourth, in the same step, for the same reason — a
version number nobody types — is the smallest possible change with a
finding-per-release to its name.

## The end value

After a release here, the ledger's stamp reads the version just released,
written by the release in the same commit as `plugin.json`, `CHANGELOG.md`
and `gates.md`. The audit after a release finds what moved, not the release.

**How we would know it worked:** the first audit after the first release to
carry this reads `check:stamp-range` clear with *nothing between*, without
anybody having touched the stamp; and one injected fault proves the release
refuses a ledger whose stamp it cannot find.

## What changes

1. **`releaselib.stamp_ledger(text, version, date)`**, pure: the first
   `Reconciled against livespec <version> on <date>` line becomes the version
   and date given — bold and a parenthetical tolerated the way the audit tool
   tolerates them since [`0043`](0043-held-to-bindings-somebody-else-typed.md)
   — and nothing else in the file moves. A text with no stamp line is refused
   with `ReleaseInputError`: a ledger without a stamp is not one the release
   should touch, and here it is not one that exists.
2. **`release.py` calls it** after `stamp_ids`, for `specs/setup/README.md`,
   and only where that file exists beside the manifest — which is this
   repository, the only place `release.py` runs. **`release.yml` commits the
   fourth file.**
3. **A fault and a control** in `inject.py`: *a ledger whose stamp the
   release cannot find* is refused; the control stamps a ledger with a bold
   stamp and a parenthetical and asserts the rest is byte-identical.
4. **The bindings**: the *Release* row names the fourth file; the stamp
   paragraph says the release writes it, from this change on.

**Rules added or changed:** none. No feature file, for the reason in *Who
this is for*; the fault and the control are the contract.

## What we are not doing

- **Not stamping anything in a consuming repository.** `release.py` runs
  here and nowhere else; a consuming repository's stamp follows its wiring,
  which `setup` moves, as before. Nothing in the method changes.
- **Not moving the audit record.** `specs/setup/audit.md` is the audit's;
  the next audit writes it and will find the stamp level.
- **Not stamping on a release that ships nothing.** A merge that moves no
  payload produces no release and no stamp — as now.

## Data

One more file the release writes, here. Nothing already in it moves but the
stamp line. This change ships nothing under `skills/`, `method/`,
`templates/`, `tools/` or `.claude-plugin/`, so it produces no release of its
own — the first release after it is the first to carry it. `verify.py` exits
**2** for the rows already owed and no other reason; no case or skill moves.

**What the pull request owes:** nothing the gate asks for — nothing ships,
no `.feature` moves, the audit surface is untouched. The `## Changelog`
section is written anyway, so the release that first carries this has an
entry to name it by.

## Risks

- **The stamp line is missing here one day.** The release refuses, loudly,
  and `main` is left as the merge left it — the worst case `release.py`
  already promises: a version that is late rather than one that is wrong.
- **The stamp moves for a release that moved no wiring here.** By the
  bindings' own argument that cannot happen: the plugin's wiring *is* this
  repository's, so a release is level with it by construction. Where that
  argument stops being true — a gate here that lags the method it ships — is
  the day this repository is no longer the plugin, and that is a bigger
  change than a stamp.

## Acceptance checks

1. `python3 .github/scripts/inject.py` — the new fault caught, the control
   green.
2. Merge, then merge the next change that ships: the release commit moves
   `plugin.json`, `CHANGELOG.md`, `method/gates.md` and
   `specs/setup/README.md` together, and the stamp reads the new version.
3. `python3 tools/doctor.py specs/setup/README.md` on `main` afterwards:
   `check:stamp-range` clear, *nothing between*, with no hand on the stamp.
