#!/usr/bin/env bash
# `dovetail`, audited three months after its sitting. Everything a previous
# audit knows to ask is already answered here: every gate row is accurate,
# branch protection was read back from the platform, the second table holds
# both pieces of never-gating wiring, and the sketch row is there. Nothing is
# missing, so nothing announces itself.
#
# What is wrong is a number, and it is not in the ledger. `vitest.config.js`
# demands exactly what the code scores — nine ratchet steps kept as a ladder of
# comments, each one read off a report — so the slack is zero and an audit
# looking for a threshold below the score finds nothing to say. The row above it
# reads *automated*, names the command, and was watched refuse a drop. It was
# correct under the method as it stood on 2026-06-11.
#
# `functions: 100` is the guard against over-firing. It equals the score too,
# and the ladder shows it has never moved: it is the whole of what is in scope,
# reached, which is what the method now recommends and must be left alone.
#
# `src/legacy/` and `src/generated/` are named, honestly and with reasons, in
# the bindings' own prose — and excluded by nothing the coverage tool reads.
set -euo pipefail

mkdir -p specs/setup specs/personas specs/workflows specs/journeys specs/changes \
         specs/features/scheduling src/schedule src/legacy src/generated \
         tests/schedule .github/workflows tools

cat > CLAUDE.md <<'EOF'
# dovetail

Shared scheduling for clinics: a patient picks a slot, the clinic's rules decide
whether it holds. Node, `vitest`, one command. `npm run verify` runs everything.
`specs/` is the contract — read `specs/setup/README.md` before assuming any
command.

## The loop

1. Human uses it and reports what they found.
2. AI files issues (`/livespec:todo`). It does not fix.
3. AI writes the spec (`/livespec:refine-spec`) — Gherkin plus a numbered change spec.
4. Human approves the spec and the sketch, or asks for changes.
5. AI implements, gets `npm run verify` green, commits.
6. AI opens the pull request with the clip and what the change did to the spec layer.
7. Human merges.
8. AI closes the issue.
EOF

cat > specs/setup/README.md <<'EOF'
# Bindings

Everything below is true of this repository and nothing else.

| | |
|---|---|
| **Verification** | `npm run verify` |
| **What it runs** | `node tools/trace.mjs`, `node tools/inject.mjs`, `vitest run --coverage` |
| **Language** | Node 20, ES modules |
| **Traceability gate** | `node tools/trace.mjs` |
| **Fault injection** | `node tools/inject.mjs` — breaks each gate in a fixture and checks it fires. Walked row by row on 2026-06-11 |
| **Coverage** | `vitest run --coverage`, thresholds in `vitest.config.js`, over `src/` |
| **Spec-bound coverage** | `vitest run --coverage --dir tests/rules`, reported beside the gated number, never compared to it |
| **Required check** | `verify` — the `name:` of the job in `.github/workflows/checks.yml` |
| **Tracker** | GitHub Issues on `dovetail-health/dovetail`, via `gh` |
| **Pull-request report** | `node tools/report.mjs`, posted by `.github/workflows/checks.yml`, `continue-on-error: true` |
| **Deliverable of a version** | a clip of the booking screen, in `docs/screenshots/` |
| **Sketch before approval** | every change that moves what a person sees owes one at step 4, drawn from the change spec rather than recorded from the app. A change to `tools/` or to the gates does not |

## Gate wiring

Reconciled against livespec 0.26.0 on 2026-06-11.

| Gate | State | Wired by, or why not |
|---|---|---|
| rule → test | automated | `node tools/trace.mjs` |
| test → rule | automated | `node tools/trace.mjs` |
| feature → workflow | automated | `node tools/trace.mjs` |
| workflow → feature | automated | `node tools/trace.mjs` |
| workflow → test | automated | `node tools/trace.mjs` |
| workflow → persona | automated | `node tools/trace.mjs` |
| persona → workflow | automated | `node tools/trace.mjs` |
| journey → workflow | automated | `node tools/trace.mjs` |
| coverage — statements, branches, functions, lines | automated | `vitest run --coverage`, thresholds in `vitest.config.js`, over the whole of `src/`. Watched refuse a drop on 2026-07-02 |
| both gates verified to fire | automated | `node tools/inject.mjs`, run by `npm run verify` |
| required check on the default branch | automated | branch protection on `dovetail-health/dovetail` requires `verify`. Read back with `gh api repos/dovetail-health/dovetail/rules/branches/main` on 2026-08-14; nobody may bypass |

## The wiring that must never gate

| Wiring | State | Notes |
|---|---|---|
| pull-request report | automated | `tools/report.mjs`, `continue-on-error: true`. Watched arrive on 2026-06-12 |
| rule-bound measure | automated | the second coverage pass over `tests/rules/` alone, printed in the report, never compared to the gated number |

## What coverage does not cover

Two directories under `src/` are not covered, and it is worth writing down why
rather than leaving somebody to wonder:

- **`src/legacy/`** — the ICS import path. Two clinics still send us calendars
  this way and it goes the week the second one is migrated. Nobody is writing
  tests for code with a delete date on it.
- **`src/generated/`** — the timezone tables, rewritten by `npm run zones` from
  the IANA database. Testing generated output tests the generator, which has its
  own tests.

## Notes from the sitting

Branch protection was read back from the platform rather than from the workflow
file, and re-read on 2026-08-14 after the organisation moved to rulesets. The
coverage gate was watched refuse a pull request on 2026-07-02.
EOF

cat > specs/personas/clinic-scheduler.md <<'EOF'
@persona:clinic-scheduler

# Rae — keeping a clinic's day from falling apart

Runs the front desk at a two-site clinic. Books, moves and cancels appointments
all day, mostly while somebody is standing in front of them.

## What they do
- Moves an appointment rather than cancelling it, whenever the rules allow.
- Trusts a slot they can see the rule behind.

## What they will never do
- Take a booking the system merely failed to refuse.
EOF

cat > specs/workflows/book-a-slot.feature <<'EOF'
@workflow:book-a-slot @persona:clinic-scheduler @journey:filling-a-day
Feature: Book a patient into a slot

  When a patient needs an appointment, I want the slot held under the clinic's
  own rules, so the day I hand over at five is one that actually happened.

  **Ends when** the slot is held and the patient has the confirmation.

  Example: the slot is inside the clinic's notice period
    Given a slot less than two hours away
    When it is booked
    Then it is refused with the notice period named
EOF

cat > specs/journeys/filling-a-day.md <<'EOF'
@journey:filling-a-day @persona:clinic-scheduler

# Filling a day

## The lens

| | |
|---|---|
| **Actor** | Rae, working the desk with somebody waiting. |
| **Goal** | To end the day with a schedule that matches what happened. |

## Opportunities

- **A refused booking does not say which rule refused it.**
EOF

cat > specs/features/scheduling/holding-a-slot.feature <<'EOF'
@feature:scheduling-holding-a-slot @workflow:book-a-slot
Feature: A slot is held under the clinic's rules

  @rule:a-slot-inside-the-notice-period-is-refused
  Rule: A booking for a slot inside the clinic's notice period is refused, and the refusal names the period

    Example: two hours' notice, ninety minutes away
      Given a clinic with a two hour notice period
      When a slot ninety minutes away is booked
      Then the booking is refused with the notice period named

  @rule:a-move-keeps-the-original-hold
  Rule: Moving an appointment keeps the original hold until the new slot is confirmed

    Example: the new slot is taken mid-move
      Given an appointment being moved to a slot somebody else takes first
      When the move fails
      Then the original slot is still held
EOF

cat > package.json <<'EOF'
{
  "name": "dovetail",
  "private": true,
  "type": "module",
  "scripts": {
    "verify": "node tools/trace.mjs && node tools/inject.mjs && vitest run --coverage",
    "test": "vitest run",
    "zones": "node tools/zones.mjs"
  },
  "devDependencies": {
    "@vitest/coverage-v8": "^2.1.0",
    "vitest": "^2.1.0"
  }
}
EOF

cat > vitest.config.js <<'EOF'
import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    include: ["tests/**/*.test.js"],
    coverage: {
      provider: "v8",
      reporter: ["text", "lcov"],
      include: ["src/**/*.js"],
      // Thresholds are the current baseline. Ratcheted to the measured actuals
      // each time a change moves them, floored to 2dp, so a regression cannot
      // slip back under. Previous rungs kept for the record:
      //
      // 2026-08-27, spec 0021: 94.1176 / 87.3417 / 100 / 95.0617
      // 2026-08-19, spec 0019: 93.8461 / 86.9565 / 100 / 94.8717
      // 2026-08-06, spec 0017: 93.5064 / 86.4864 / 100 / 94.5945
      // 2026-07-28, spec 0015: 93.1034 / 85.7142 / 100 / 94.2028
      // 2026-07-15, spec 0012: 92.7536 / 85.1063 / 100 / 93.8461
      // 2026-07-02, spec 0010: 92.1052 / 84.4444 / 100 / 93.3333
      // 2026-06-24, spec 0008: 91.7808 / 84.0909 / 100 / 92.9577
      // 2026-06-18, spec 0006: 91.4285 / 83.7209 / 100 / 92.5373
      // 2026-06-11, setup:     91.0891 / 83.3333 / 100 / 92.1052
      thresholds: {
        statements: 94.12,
        branches: 87.34,
        functions: 100,
        lines: 95.06,
      },
    },
  },
});
EOF

cat > CONTRIBUTING.md <<'EOF'
# Contributing

`npm run verify` runs the gates and the suite. CI runs the same command.

Coverage on `main`, 2026-08-27:

```
 % Coverage report
 ------------------------|---------|----------|---------|---------|
 File                    | % Stmts | % Branch | % Funcs | % Lines |
 ------------------------|---------|----------|---------|---------|
 All files               |   94.12 |    87.34 |  100.00 |   95.06 |
  schedule/slots.js      |  100.00 |   100.00 |  100.00 |  100.00 |
  schedule/book.js       |  100.00 |    96.15 |  100.00 |  100.00 |
  schedule/move.js       |   98.41 |    92.30 |  100.00 |   98.36 |
  legacy/ics.js          |   61.53 |    38.46 |  100.00 |   63.15 |
  generated/timezones.js |   88.23 |    71.42 |  100.00 |   90.00 |
 ------------------------|---------|----------|---------|---------|
```

The thresholds in `vitest.config.js` are at those numbers. Move them up when a
change moves the report up; never down.
EOF

cat > src/schedule/slots.js <<'EOF'
export function openSlots(day, taken) {
  const held = new Set(taken);
  return day.filter((slot) => !held.has(slot.id));
}

export function withinNotice(slot, now, noticeMinutes) {
  return (slot.startsAt - now) / 60000 < noticeMinutes;
}
EOF

cat > src/schedule/book.js <<'EOF'
import { withinNotice } from "./slots.js";

export function book(slot, patient, clinic, now) {
  if (!slot) return { booked: false, reason: "no slot chosen" };
  if (withinNotice(slot, now, clinic.noticeMinutes)) {
    return { booked: false, reason: `inside the ${clinic.noticeMinutes} minute notice period` };
  }
  if (slot.takenBy) return { booked: false, reason: "already taken" };
  return { booked: true, slot: slot.id, patient: patient.id };
}
EOF

cat > src/schedule/move.js <<'EOF'
export function move(appointment, target, hold) {
  if (!target) return { moved: false, holding: appointment.slot };
  if (target.takenBy) {
    return { moved: false, holding: appointment.slot, reason: "taken while moving" };
  }
  const released = hold.release(appointment.slot, { onlyAfter: target.id });
  if (!released) return { moved: false, holding: appointment.slot };
  return { moved: true, slot: target.id, holding: target.id };
}
EOF

cat > src/legacy/ics.js <<'EOF'
// The ICS import path. Two clinics still send calendars this way; it goes the
// week the second one is migrated. Nothing new is built on it.
export function parseCalendar(text) {
  const lines = text.split(/\r?\n/).filter(Boolean);
  const events = [];
  let current = null;
  for (const line of lines) {
    if (line === "BEGIN:VEVENT") current = {};
    else if (line === "END:VEVENT" && current) {
      events.push(current);
      current = null;
    } else if (current) {
      const [key, ...rest] = line.split(":");
      if (!key) continue;
      const value = rest.join(":");
      if (key.startsWith("DTSTART")) current.startsAt = value;
      else if (key.startsWith("DTEND")) current.endsAt = value;
      else if (key === "SUMMARY") current.summary = value;
      else if (key === "UID") current.uid = value;
    }
  }
  return events;
}

export function mergeCalendars(calendars) {
  const seen = new Map();
  for (const calendar of calendars) {
    for (const event of calendar) {
      if (!event.uid) continue;
      const existing = seen.get(event.uid);
      if (!existing || (event.startsAt && existing.startsAt && event.startsAt > existing.startsAt)) {
        seen.set(event.uid, event);
      }
    }
  }
  return [...seen.values()];
}
EOF

cat > src/generated/timezones.js <<'EOF'
// Generated by `npm run zones` from the IANA database. Do not edit by hand.
const ZONES = {
  "Europe/London": { offset: 0, dst: true },
  "Europe/Dublin": { offset: 0, dst: true },
  "Europe/Lisbon": { offset: 0, dst: true },
};

export function offsetFor(zone, inSummer) {
  const entry = ZONES[zone];
  if (!entry) return null;
  if (!entry.dst) return entry.offset;
  return inSummer ? entry.offset + 60 : entry.offset;
}

export function known() {
  return Object.keys(ZONES);
}
EOF

mkdir -p tests/rules
cat > tests/rules/booking.test.js <<'EOF'
import { describe, expect, it, rule } from "../helpers.js";
import { book } from "../../src/schedule/book.js";

rule("a-slot-inside-the-notice-period-is-refused", () => {
  it("refuses a slot ninety minutes away under a two hour notice period", () => {
    const now = Date.parse("2026-08-27T09:00:00Z");
    const slot = { id: "s1", startsAt: now + 90 * 60000 };
    const result = book(slot, { id: "p1" }, { noticeMinutes: 120 }, now);
    expect(result.booked).toBe(false);
    expect(result.reason).toContain("120");
  });
});
EOF

cat > tests/rules/moving.test.js <<'EOF'
import { describe, expect, it, rule } from "../helpers.js";
import { move } from "../../src/schedule/move.js";

rule("a-move-keeps-the-original-hold", () => {
  it("keeps the original slot when the target is taken mid-move", () => {
    const hold = { release: () => false };
    const result = move({ slot: "s1" }, { id: "s2", takenBy: "p9" }, hold);
    expect(result.moved).toBe(false);
    expect(result.holding).toBe("s1");
  });
});
EOF

cat > tests/schedule/slots.test.js <<'EOF'
import { describe, expect, it } from "vitest";
import { openSlots } from "../../src/schedule/slots.js";

describe("openSlots", () => {
  it("leaves out what is already taken", () => {
    const day = [{ id: "s1" }, { id: "s2" }];
    expect(openSlots(day, ["s1"]).map((s) => s.id)).toEqual(["s2"]);
  });
});
EOF

cat > .github/workflows/checks.yml <<'EOF'
name: checks
on: [pull_request]
jobs:
  verify:
    name: verify
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm ci
      - run: npm run verify
      - run: node tools/report.mjs
        continue-on-error: true
EOF

printf '// Traceability gate. Reads specs/features and tests/.\n' > tools/trace.mjs
printf '// Breaks each gate in a fixture in turn and checks it fires.\n' > tools/inject.mjs
printf '// Posts what the change did to the spec layer, and both coverage passes.\n' > tools/report.mjs
printf '// Rewrites src/generated/timezones.js from the IANA database.\n' > tools/zones.mjs
printf 'export { describe, expect, it } from "vitest";\nexport const rule = (id, body) => describe(`rule:${id}`, body);\n' > tests/helpers.js

git init -q -b main
git add -A
git -c user.email=rae@dovetail.example -c user.name="Dovetail" \
    commit -q -m "dovetail: booking, moving, and the ICS path we are getting rid of"
git remote add origin git@github.com:dovetail-health/dovetail.git
