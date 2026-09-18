# Spec 0055: a rider is filed, not served

- **Status:** approved
- **Issue:** [#125](https://github.com/sargismarkosyan/livespec/issues/125) —
  a recording request with a fix-first rider loses the recording. Found by
  the third part of the sitting of 2026-09-17, the first run of case 08 in
  the world its prompt describes.
- **Depends on:** [`0054`](0054-a-case-names-the-world-it-runs-in.md), which
  gave case 08 the fixture that made this visible — yesterday the same
  sessions never got past the directory listing; and
  [`0013`](0013-the-board-of-latest-measurements.md), whose rule about the form
  of the picture this sits beside.

## Who this is for

[`agent-accelerated-owner`](../personas/agent-accelerated-owner.md), in
[`adopt-the-process`](../workflows/adopt-the-process.feature), at the pull
request — the step where the picture is how they check, because *"checking
the result by reading is not available."* They asked for the picture of
version 0012 and mentioned, while they were at it, a full stop that has
bothered them for months. What they got back was a change spec for the full
stop and no picture. Three sessions of three took that path; two of them
ended there.

**This lengthens nothing anybody types.** It changes what a session does with
the second half of a message: one line, filed, instead of a spec that eats the
session. What it shortens is the wait for the thing that was asked for.

One always-promise is touched: **`never-implements`** is untouched in
substance — the rider is filed, not fixed, which is what the sessions already
did — but the routing that put the recording second is what this corrects.
`context-budget` moves: the description grows by a clause, paid for below.

## The job behind the request

The literal ask is #125's: make `record-clip` fire on the recording even when
the message also asks for a change, and say what to do with the change.
Behind it is a shape that will recur in every skill that produces something:
**a request with a rider, where the rider is written as a precondition —
"sort that out first" — and the session serves the precondition and never
returns.** The rider here was a change; a change in a livespec repository
starts as a spec; so the session opened `refine-spec`, wrote spec 0013 and a
feature file for one character of copy, argued about the always-list, and
ran out of room. It did everything right about the change and nothing about
the request.

The job: **the picture is of the version as it is, and nothing the person
asks for alongside changes that.** A picture of an unbuilt fix cannot be
taken; the fix goes where a report goes, in one line; and the hand-back says
what the shot does not show and why. The rule the skill already carries —
*files what it noticed instead of fixing it* — covers what the *recording*
turns up. This extends it to what the *message* carried, and puts the order
in writing: record first, file the rider, never defer the one behind the
other.

The routing decision is made with only the descriptions in context, before
any skill body loads. So the fix has two halves in two places: the
description, so the recording fires; the body, so the rider is handled. The
description is the expensive field, and widening it is paid for with a
should-not-fire case.

## Why now

Because the fixture just landed and the first honest measurement of case 08
came back flat — `record-clip` fired one time in three — and because the
next paid sitting should measure the skill, not this gap in it.

## The end value

A request to record that also asks for a change records the version as it
is, files the change in a line, and says the change is not in the shot
because it is not built. `record-clip` fires on such a request. A message
that uses the recording vocabulary to ask a question fires nothing.

**How we would know it worked:** case 08's plugin arm fires `record-clip` in
every run and its hand-back names the filed rider beside the clip; the new
should-not-fire case stays at 1.00 in both arms; the plugin arm's transcripts
no longer contain a `specs/changes/0013-…` written for a full stop.

## What changes

1. **[`record-clip`](../../skills/record-clip/SKILL.md)'s description** gains
   one clause: *Fires on the recording even when the same message also asks
   for a fix alongside — the fix is filed, and the picture is of the version
   as it is.* The budget goes from 4321 to about 4460 of 5000.
2. **Its body** gains a rule beside *Never touch `src/` or `specs/`*: **a
   rider is filed, not served.** A request to record that also asks for a
   change — fix this first, tweak that while you are in there — records the
   version as it is and files the change with `todo` or in one line of the
   hand-back. The recording is never deferred behind it: a picture of an
   unbuilt change cannot be taken, and the hand-back says which of the
   person's asks the shot does not show and why. *"First"* in the request
   changes the order of nothing; it is the person telling you what they
   noticed.
3. **One rule**, `@planned`, in
   [`what-a-change-shows.feature`](../features/showing/what-a-change-shows.feature):
   `a-rider-is-filed-not-served`, with the recording taken and the rider
   filed, the recording not deferred, and the hand-back naming what the shot
   does not show.
4. **Case 08** gains a grader claiming it — the recording is attempted and
   the rider is filed, not written as a change spec in the session — and its
   tag. Its measurement from today, flat at 0.42, goes stale by design; the
   skill body it held has moved.
5. **A should-not-fire case**, numbered next: a question in the recording
   vocabulary — which of a GIF or a short recording reviewers prefer on a
   pull request, and what size people aim for — where nothing fires and the
   question is answered. The price of item 1.
6. **[`evals/README.md`](../../evals/README.md)**: the two rows.

**Rules added or changed** — the `@rule:` ids in `specs/features/`:

| Rule id | Feature file | New or changed |
|---|---|---|
| `a-rider-is-filed-not-served` | `features/showing/what-a-change-shows.feature` | new, `@planned` — case 08 |

**One description changes, so one should-not-fire case is owed**, item 5.

## What we are not doing

- **Not making `record-clip` file the rider itself as an issue.** It says
  *file it with `todo`* — the routing the plugin already has — or names it in
  the hand-back. A skill that files issues is `todo`; two skills that file
  issues is two places for a finding to go.
- **Not raising case 08's turn limit.** The two sessions that never recorded
  did not run out of turns by accident; they spent them on the wrong half.
  More turns would measure a longer detour.
- **Not touching `refine-spec`.** It did its job on the change it was handed.
  The defect is that it was handed the change first.
- **Not generalising the rule to every skill in this change.** The shape
  recurs — a rider on any request — but the evidence is one skill's, and a
  rule for all eight on one case's evidence is the wallpaper the method warns
  against. The spec names the shape so the next instance is recognised.

## Data

No storage. Files that move: `skills/record-clip/SKILL.md`,
`specs/features/showing/what-a-change-shows.feature`,
`evals/08-fix-it-while-recording/` (a grader, a tag), one new case directory,
`evals/README.md`, `specs/setup/README.md` (the budget number), and this spec.

**This spec commit stales nothing.** One rule, `@planned`, claimed by nobody.
`verify.py` exits **2** for the rows already owed and no other reason.

**The implementing change stales one fresh row and one old one, by design.**
Case 08, measured today at 0.42 in both arms, holds the skill body that
moves; its number was the detour's, and re-measuring it is the point. Case
22, which also holds `record-clip`, was already stale. It adds one case,
never measured until a run is approved.

**What the pull request owes.** A skill moves — **`minor`** — a
`## Changelog` section, a Gherkin block for the rule, and the run block,
because it touches `evals/`. The audit surface does not move.

## Risks

- **The clause makes `record-clip` fire on change requests that mention a
  picture.** The should-not-fire case holds the line at questions; a change
  request that mentions the README's screenshot is `refine-spec`'s and stays
  so, because the clause says *also asks for a fix alongside* a recording,
  not *mentions one*. If a run shows over-firing, the clause narrows and the
  case stays.
- **The rider is important and one line loses it.** One line in the hand-back
  plus an issue is exactly the record a finding gets everywhere else in the
  method; a spec written in a recording session is the record nobody asked
  for.
- **Always-promises.** `never-implements`: unchanged. `context-budget`:
  within the limit, the number updated in the bindings.

## Acceptance checks

1. `python3 .github/scripts/checks.py`: the budget under 5000, the bindings'
   number matching.
2. Case 08's plugin-arm transcripts, next run: `record-clip` fires 3 of 3,
   no `specs/changes/` file written for the full stop, the hand-back names
   the filed rider.
3. The new should-not-fire case: 1.00 in both arms; no skill fires.
4. `verify.py` exits 2 naming case 08 and the new case; the pull request
   carries `minor`, `## Changelog`, the Gherkin block and the run block.
