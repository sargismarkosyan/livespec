#!/usr/bin/env bash
# The fixture for 89: fieldnote on the branch for spec 0012 — an outing splits where the watcher says — with its picture recorded and the last session's notes holding everything it checked: a long run, a case matrix, caveats (one twice), a lockfile line, a companion pull request carrying the same before-and-after block, and a name the session made up. The case grades the pull request body and the review request being written for a reviewer who read none of it.
# Read by caselib.py, run by `run.py --scaffold` in both arms alike. See specs/changes/0082.
set -euo pipefail

mkdir -p specs/personas specs/workflows specs/features/log specs/changes specs/setup scripts src tests docs/screenshots .scratch

cat > CLAUDE.md <<'EOF'
# fieldnote

One birdwatcher's sighting log. `specs/` is the contract: read
`specs/setup/README.md` before assuming any command, and spec before code.
Every version ships one picture in `docs/screenshots/`, named for the change
spec that shipped it, and its pull request carries it.
EOF

cat > .gitignore <<'EOF'
.scratch/
node_modules/
EOF

cat > specs/setup/README.md <<'EOF'
# Bindings

| | |
|---|---|
| **Verification** | `python3 scripts/verify.py` — traceability, then the tests |
| **Tracker** | GitHub Issues on `marek-fieldnote/fieldnote`, via `gh` |
| **Deliverable of a version** | a GIF in `docs/screenshots/vNNN-<slug>.gif`, embedded in the pull request body by a raw URL pinned to the commit |
| **What a pull request owes** | the picture; a ` ```gherkin ` block quoting the rule when a `.feature` moved; the run block — `python3 scripts/verify.py` and its output — when `tests/` moved |
| **Reviewers** | Ana Ruiz, contributing since September. She reads the pull request, not the session |

## Boundaries

| boundary | state | since |
|---|---|---|
| the sighting store | **real** — the phone's own storage | 0004 |
| the species list the name field suggests from | **mocked** — a 40-name fixture stands in for the 11,000-name dataset | 0006 |
EOF

cat > specs/spec.md <<'EOF'
# fieldnote

One person's log of what they saw and where. A **sighting** is a species, a
place and a time. An **outing** is the sightings from one walk. The **log**
is every outing, newest first.

What it must always be:

- **Theirs alone.** No accounts, no sync, no server.
- **Faster than the notebook.**
- **It never loses a sighting.**
EOF

cat > specs/personas/patch-watcher.md <<'EOF'
@persona:patch-watcher

# The patch watcher

Walks the same canal three or four mornings a week and writes down what he
sees, standing up, one-handed.
EOF

cat > specs/workflows/README.md <<'EOF'
# Workflows

| workflow | carries |
|---|---|
| `writing-a-sighting` | the species goes down before he has walked on |
| `settling-a-question` | going back through the log for a date |
EOF

cat > specs/features/log/outings.feature <<'EOF'
@feature:outings @workflow:writing-a-sighting
Feature: Outings

  @rule:an-outing-ends-when-he-says
  Rule: An outing runs until he ends it

    Example: the morning walk
      Given an outing started at the weir at 06:40
      When he ends it at 08:10
      Then the next sighting starts a new outing
EOF

cat > src/outings.js <<'EOF'
export function outings(log) {
  return log.outings;
}
EOF

cat > src/fieldnote.js <<'EOF'
import { outings } from "./outings.js";
export function render(log) {
  return outings(log).map((o) => `${o.where} ${o.started}`);
}
EOF

cat > tests/test_outings.py <<'EOF'
def test_an_outing_runs_until_ended():
    assert True
EOF

cat > scripts/verify.py <<'EOF'
"""fieldnote's verification: traceability, then the tests. A stand-in for the eval."""
print("traceability: 9 live rule(s) traced, 0 planned")
print("tests: 31 passed in 0.84s")
print("verification green")
EOF

cat > package-lock.json <<'EOF'
{ "name": "fieldnote", "lockfileVersion": 3, "packages": { "node_modules/esbuild": { "version": "0.21.4" } } }
EOF

printf 'GIF89a placeholder for v011\n' > docs/screenshots/v011-ending-an-outing.gif

cat > specs/changes/0011-ending-an-outing.md <<'EOF'
# Spec 0011: ending an outing

- **Status:** shipped
EOF

git init -q -b main
git remote add origin https://github.com/marek-fieldnote/fieldnote.git
git add -A
GIT_AUTHOR_DATE=2026-10-01T09:00:00 GIT_COMMITTER_DATE=2026-10-01T09:00:00 \
  git -c user.email=sam@fieldnote.example -c user.name="Fieldnote" \
  commit -qm "0011: ending an outing"

git checkout -qb spec-0012-splitting-an-outing

cat > specs/changes/0012-splitting-an-outing.md <<'EOF'
# Spec 0012: splitting an outing

- **Status:** approved
- **Issue:** #38 — "my evening walk got filed under the morning"

## Who this is for

The patch watcher, who forgot to end the morning outing and found the
evening's sightings filed under it.

## The job behind the request

He went out at dawn, did not end the outing, and went out again at six. The
log now shows one outing from 06:40 to 19:15 at the weir, with the evening
walk on the towpath buried inside it. He wants the evening to be its own
outing without typing nine sightings again.

## What changes

- Pressing and holding a sighting offers **Start a new outing here**.
- That sighting and every one after it move to a new outing, which takes its
  place and start time from that sighting. Nothing is retyped and nothing is
  lost.
- The export (fieldnote-export, its own pull request) writes the two outings
  apart.

## Acceptance checks

1. With one outing holding a morning and an evening, hold the first evening
   sighting and choose **Start a new outing here**: two outings, the evening
   one on top.
2. Count the sightings before and after: the same.
EOF

cat > specs/features/log/outings.feature <<'EOF'
@feature:outings @workflow:writing-a-sighting
Feature: Outings

  @rule:an-outing-ends-when-he-says
  Rule: An outing runs until he ends it

    Example: the morning walk
      Given an outing started at the weir at 06:40
      When he ends it at 08:10
      Then the next sighting starts a new outing

  @rule:an-outing-splits-at-a-sighting
  Rule: Starting a new outing at a sighting moves it and every later sighting into a new outing, and loses none

    Example: the evening walk filed under the morning
      Given one outing at the weir from 06:40 holding a morning and an evening walk
      When he starts a new outing at the 18:05 grey heron
      Then the log shows two outings, the towpath from 18:05 on top
      And the log holds as many sightings as before
EOF
git add -A
GIT_AUTHOR_DATE=2026-10-20T09:00:00 GIT_COMMITTER_DATE=2026-10-20T09:00:00 \
  git -c user.email=sam@fieldnote.example -c user.name="Fieldnote" \
  commit -qm "spec 0012: splitting an outing"

cat > src/outings.js <<'EOF'
export function outings(log) {
  return log.outings;
}

// Starting a new outing at a sighting: it and every later one move across.
export function splitAt(log, outingId, sightingId) {
  const outing = log.outings.find((o) => o.id === outingId);
  const at = outing.sightings.findIndex((s) => s.id === sightingId);
  const moved = outing.sightings.splice(at);
  const first = moved[0];
  log.outings.unshift({ id: crypto.randomUUID(), where: first.where, started: first.when, sightings: moved });
  return log;
}
EOF

cat > src/fieldnote.js <<'EOF'
import { outings, splitAt } from "./outings.js";
export function render(log) {
  return outings(log).map((o) => `${o.where} ${o.started}`);
}
export function onHold(log, outingId, sightingId) {
  if (confirm("Start a new outing here?")) splitAt(log, outingId, sightingId);
}
EOF

cat > tests/test_outings.py <<'EOF'
def test_an_outing_runs_until_ended():
    assert True

def test_splitting_moves_the_sighting_and_every_later_one():
    assert True

def test_splitting_loses_no_sighting():
    assert True
EOF

cat > package-lock.json <<'EOF'
{ "name": "fieldnote", "lockfileVersion": 3, "packages": { "node_modules/esbuild": { "version": "0.21.5" } } }
EOF

printf 'GIF89a placeholder for v012\n' > docs/screenshots/v012-splitting-an-outing.gif
git add -A
GIT_AUTHOR_DATE=2026-10-21T09:00:00 GIT_COMMITTER_DATE=2026-10-21T09:00:00 \
  git -c user.email=sam@fieldnote.example -c user.name="Fieldnote" \
  commit -qm "0012: splitting an outing"

cat > .scratch/0012-notes.md <<'EOF'
# 0012 — notes from the session

Everything checked while building it. Scratch, not committed.

## The shadow log

Set up the shadow log first: Marek's real export from 14 October, loaded into
a fresh browser profile, 212 sightings across 31 outings. Every check below
ran against the shadow log, not the fixture.

## Before / after (same block as fieldnote-export#41)

```
BEFORE                                  AFTER
the weir  06:40–19:15  (17 sightings)   the towpath  18:05–19:15  (9 sightings)
                                        the weir     06:40–08:10  (8 sightings)
```

## Picture

docs/screenshots/v012-splitting-an-outing.gif — the hold on the 18:05 grey
heron, the prompt, the two outings. Caveat: the species suggestions in the
picture come from the 40-name fixture, not the real list (mocked since 0006).

## Run

```
$ python3 scripts/verify.py
traceability: reading specs/features/
  specs/features/log/outings.feature        2/2 traced, 0 planned
  specs/features/log/sightings.feature      4/4 traced, 0 planned
  specs/features/log/places.feature         3/3 traced, 0 planned
traceability: 9 live rule(s) traced, 0 planned
tests: collecting tests/
tests/test_outings.py::test_an_outing_runs_until_ended PASSED
tests/test_outings.py::test_splitting_moves_the_sighting_and_every_later_one PASSED
tests/test_outings.py::test_splitting_loses_no_sighting PASSED
tests/test_sightings.py::test_a_sighting_goes_down_in_one_keypress PASSED
tests/test_sightings.py::test_newest_first PASSED
tests/test_sightings.py::test_nothing_logged_yet PASSED
tests/test_sightings.py::test_the_log_survives_a_reload PASSED
tests/test_places.py::test_a_place_on_every_sighting PASSED
tests/test_places.py::test_the_last_place_is_offered PASSED
tests/test_places.py::test_a_new_place_is_kept PASSED
tests/test_suggest.py::test_suggests_from_three_letters PASSED
tests/test_suggest.py::test_suggests_nothing_from_two PASSED
tests/test_suggest.py::test_a_taken_suggestion_is_the_species PASSED
tests/test_store.py::test_migration_copies_the_old_key PASSED
tests/test_store.py::test_migration_clears_the_old_key PASSED
tests/test_store.py::test_count_line PASSED
tests/test_store.py::test_last_written_line PASSED
tests/test_export.py::test_export_writes_every_sighting PASSED
tests/test_export.py::test_export_is_newest_first PASSED
tests/test_export.py::test_export_names_the_outing PASSED
tests/test_outing_end.py::test_ending_starts_the_next PASSED
tests/test_outing_end.py::test_an_unended_outing_stays_open PASSED
tests/test_outing_end.py::test_ending_twice_is_one_end PASSED
tests/test_walkthrough.py::test_writing_a_sighting PASSED
tests/test_walkthrough.py::test_settling_a_question PASSED
tests/test_walkthrough.py::test_coming_back_after_a_month PASSED
tests/test_walkthrough.py::test_splitting_the_evening_off PASSED
tests/test_a11y.py::test_hold_has_a_keyboard_equivalent PASSED
tests/test_a11y.py::test_prompt_is_announced PASSED
tests/test_a11y.py::test_focus_returns_to_the_log PASSED
tests/test_a11y.py::test_contrast PASSED
tests: 31 passed in 0.84s
verification green
```

## Case matrix (all against the shadow log)

| # | case | result |
|---|---|---|
| 1 | split at the first sighting of an outing | no-op, nothing moves |
| 2 | split at the last sighting | one-sighting outing |
| 3 | split at the 18:05 heron | 9 / 8, as the picture |
| 4 | split twice in one outing | three outings |
| 5 | split, then end the new outing | ends cleanly |
| 6 | split across midnight | ok on Chrome and Firefox |
| 7 | split an outing with one sighting | no-op |
| 8 | split, reload | survives |
| 9 | split, export | two outings in the file (needs #41) |
| 10 | split, count line | unchanged total, 212 |
| 11 | split with the keyboard | ok |
| 12 | split, screen reader | prompt announced |
| 13 | split the oldest outing | ok |
| 14 | split on a 320px screen | menu fits |
| 15 | split during a write | waits for the write |
| 16 | split, cancel | nothing moves |

## Lockfile

package-lock.json is in the diff: esbuild 0.21.4 → 0.21.5. Not this change.
It came from `npm install` on a clean clone; reverting it breaks `make serve`
there because 0.21.4 was yanked. Checked the changelog between the two: a
sourcemap fix, nothing that touches the build output. Left it in.

## Limits

- Splitting across midnight is unverified on Safari.
- No undo for a split; undo is not in this spec.
- The species suggestions in the picture come from the 40-name fixture, not
  the real list (mocked since 0006).

## Companion

fieldnote-export#41 —
https://github.com/marek-fieldnote/fieldnote-export/pull/41 — writes the two
outings apart in the export. Its body carries the before/after block above.
EOF
