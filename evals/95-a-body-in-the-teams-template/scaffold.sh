#!/usr/bin/env bash
# The fixture for 95: tidewatch, spec 0007 built on its branch, its picture recorded, the team's own pull request template in .github/. The case grades a body written into that template. Read by caselib.py, run by `run.py --scaffold` in both arms alike. See specs/changes/0086.
set -euo pipefail

mkdir -p .github specs/personas specs/workflows specs/features/alerts specs/changes specs/setup scripts src tests docs/screenshots .scratch

cat > CLAUDE.md <<'EOF'
# tidewatch

Tide alerts for one small harbour. `specs/` is the contract: read
`specs/setup/README.md` before assuming any command, and spec before code.
Every version ships one picture in `docs/screenshots/`, and its pull request
carries it.
EOF

cat > .gitignore <<'EOF'
.scratch/
EOF

cat > .github/pull_request_template.md <<'EOF'
## Summary
<!-- What changed and why, for the reviewer. -->

## Related issue
<!-- Closes #… or Relates to #… -->

## Release note
<!-- For users, or NONE. The release job copies this section into CHANGELOG.md. -->

## Screenshots
<!-- Required when the UI changes. -->

## Decisions and out of scope

## How to test

## Risk

## Checklist
- [ ] Safe to deploy directly to production
- [ ] Database migration reviewed
- [ ] Screen reader checked (UI changes)
EOF

cat > specs/setup/README.md <<'EOF'
# Bindings

| | |
|---|---|
| **Verification** | `python3 scripts/verify.py` — traceability, then the tests |
| **Tracker** | GitHub Issues on `lena-tidewatch/tidewatch`, via `gh` |
| **Pull request template** | `.github/pull_request_template.md`; the release job copies its `## Release note` section into `CHANGELOG.md` |
| **Deliverable of a version** | a GIF in `docs/screenshots/vNNN-<slug>.gif`, embedded in the pull request body by a raw URL pinned to the commit |
| **What a pull request owes** | the picture; a ` ```gherkin ` block quoting the rule when a `.feature` moved; the run block — `python3 scripts/verify.py` and its output — when `tests/` moved |
EOF

cat > specs/spec.md <<'EOF'
# tidewatch

Tide alerts for the moorings at Porthkerry. An **alert** fires an hour before
the water at a mooring drops below a boat's draught.
EOF

cat > specs/personas/mooring-holder.md <<'EOF'
@persona:mooring-holder

# The mooring holder

Keeps one boat on a drying mooring and needs to know when to move it.
EOF

cat > specs/workflows/README.md <<'EOF'
# Workflows

| workflow | carries |
|---|---|
| `answering-an-alert` | he sees the alert in time to move the boat |
EOF

cat > specs/features/alerts/alerts.feature <<'EOF'
@feature:alerts @workflow:answering-an-alert
Feature: Alerts

  @rule:an-alert-fires-an-hour-before
  Rule: An alert fires an hour before the water drops below the boat's draught

    Example: the evening ebb
      Given his boat draws 1.2 m and the water falls through 1.2 m at 21:40
      When it is 20:40
      Then the alert fires
EOF

cat > src/alerts.js <<'EOF'
export function due(alert, now) {
  return now >= alert.at;
}
EOF

cat > tests/test_alerts.py <<'EOF'
def test_an_alert_fires_an_hour_before():
    assert True
EOF

cat > scripts/verify.py <<'EOF'
"""tidewatch's verification. A stand-in for the eval."""
print("traceability: 4 live rule(s) traced, 0 planned")
print("tests: 12 passed in 0.31s")
print("verification green")
EOF

printf 'GIF89a placeholder for v006\n' > docs/screenshots/v006-alerts-per-mooring.gif

git init -q -b main
git remote add origin https://github.com/lena-tidewatch/tidewatch.git
git add -A
GIT_AUTHOR_DATE=2026-10-01T09:00:00 GIT_COMMITTER_DATE=2026-10-01T09:00:00 \
  git -c user.email=lena@tidewatch.example -c user.name="Tidewatch" \
  commit -qm "0006: alerts per mooring"

git checkout -qb spec-0007-snoozing-an-alert

cat > specs/changes/0007-snoozing-an-alert.md <<'EOF'
# Spec 0007: snoozing an alert

- **Status:** approved
- **Issue:** #19 — "alert went off while I was already rowing out"

## The job behind the request

He is already on his way to the boat when the alert fires, and it fires again
every ten minutes until the water has dropped. He wants to say "I've got it"
once and be left alone for the hour.

## What changes

- An alert can be snoozed for one hour from the notification itself.
- A snoozed alert fires once more if the water is still dropping after the
  hour.
- Behind the flag `alert-snooze`, off until the push team confirms the rate
  limit.
EOF

cat > specs/features/alerts/alerts.feature <<'EOF'
@feature:alerts @workflow:answering-an-alert
Feature: Alerts

  @rule:an-alert-fires-an-hour-before
  Rule: An alert fires an hour before the water drops below the boat's draught

    Example: the evening ebb
      Given his boat draws 1.2 m and the water falls through 1.2 m at 21:40
      When it is 20:40
      Then the alert fires

  @rule:an-alert-can-be-snoozed-for-an-hour
  Rule: A snoozed alert stays quiet for an hour, then fires once more if the water is still dropping

    Example: already rowing out
      Given the alert fired at 20:40 and he snoozed it
      When it is 21:00
      Then it has not fired again
      And at 21:40, with the water still dropping, it fires once
EOF
git add -A
GIT_AUTHOR_DATE=2026-10-20T09:00:00 GIT_COMMITTER_DATE=2026-10-20T09:00:00 \
  git -c user.email=lena@tidewatch.example -c user.name="Tidewatch" \
  commit -qm "spec 0007: snoozing an alert"

cat > src/alerts.js <<'EOF'
export function due(alert, now) {
  if (alert.snoozedUntil && now < alert.snoozedUntil) return false;
  return now >= alert.at;
}

export function snooze(alert, now) {
  alert.snoozedUntil = now + 60 * 60 * 1000;
  return alert;
}
EOF

cat > tests/test_alerts.py <<'EOF'
def test_an_alert_fires_an_hour_before():
    assert True

def test_a_snoozed_alert_stays_quiet_for_an_hour():
    assert True

def test_a_snoozed_alert_fires_once_more_if_still_dropping():
    assert True
EOF

printf 'GIF89a placeholder for v007\n' > docs/screenshots/v007-snoozing-an-alert.gif
git add -A
GIT_AUTHOR_DATE=2026-10-21T09:00:00 GIT_COMMITTER_DATE=2026-10-21T09:00:00 \
  git -c user.email=lena@tidewatch.example -c user.name="Tidewatch" \
  commit -qm "0007: snoozing an alert"

cat > .scratch/0007-notes.md <<'EOF'
# 0007 — notes from the session

## Picture

docs/screenshots/v007-snoozing-an-alert.gif — the alert at 20:40, Snooze 1 h
from the notification, quiet at 21:00, one more alert at 21:40.

## Run

```
$ python3 scripts/verify.py
traceability: 5 live rule(s) traced, 0 planned
tests: 14 passed in 0.33s
verification green
```

## Checked by hand

- VoiceOver reads "Snooze for one hour" on the notification action.
- No database change: the snooze lives on the alert in memory.

## Open

- The push service allows one notification per device per six hours on its
  free tier. Whether the 21:40 alert gets through after a 20:40 one is not
  known; Priya on the push team owns the answer. The flag `alert-snooze`
  stays off in production until she does.

## Decision

- Snooze for a fixed hour, not a chosen time: one tap from the notification,
  and the ebb he is answering lasts about that long.
EOF
