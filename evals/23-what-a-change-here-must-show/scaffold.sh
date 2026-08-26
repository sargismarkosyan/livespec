#!/usr/bin/env bash
# The fixture for 23: relay, gate wired, bindings never written.
#
# The history is the part that matters. Recent versions are a mix on purpose —
# something that unfolds, something whose whole result is a screen sitting there,
# and two nobody can see at all — so the deliverable row cannot be written as a
# blanket rule without being wrong about most of them.
set -euo pipefail

mkdir -p src/ui src/jobs specs/features/schedules specs/workflows tools tests/behaviour

cat > CLAUDE.md <<'EOF'
# relay

An operations dashboard for scheduled jobs — what ran, what failed, what is
queued behind what. `npm run dev` serves it; `npm test` runs the suite.

`specs/` is the contract. Spec before code.
EOF

cat > package.json <<'EOF'
{
  "name": "relay",
  "private": true,
  "scripts": {
    "dev": "vite",
    "test": "vitest run",
    "verify": "node tools/trace.js && vitest run --coverage"
  }
}
EOF

cat > tools/trace.js <<'EOF'
// Traceability, both directions. Reads @rule: ids out of specs/features/**.feature
// and rule() calls out of tests/behaviour/**, and fails on either half missing.
// Also checks the layer above: features name workflows, workflows name personas.
import { readdirSync, readFileSync, statSync } from "node:fs";
import { join } from "node:path";

const walk = (dir) =>
  readdirSync(dir).flatMap((entry) => {
    const path = join(dir, entry);
    return statSync(path).isDirectory() ? walk(path) : [path];
  });

const rules = new Map();
for (const path of walk("specs/features").filter((p) => p.endsWith(".feature"))) {
  const text = readFileSync(path, "utf8");
  for (const [, id] of text.matchAll(/@rule:([\w-]+)/g)) {
    rules.set(id, { path, planned: text.includes(`@rule:${id} @planned`) });
  }
}

const claimed = new Set();
for (const path of walk("tests/behaviour")) {
  for (const [, id] of readFileSync(path, "utf8").matchAll(/rule\(["']([\w-]+)["']/g)) {
    if (!rules.has(id)) {
      console.error(`${path}: claims rule ${id}, which does not exist`);
      process.exitCode = 1;
    }
    claimed.add(id);
  }
}

for (const [id, rule] of rules) {
  if (!rule.planned && !claimed.has(id)) {
    console.error(`${rule.path}: rule ${id} is live and no test claims it`);
    process.exitCode = 1;
  }
}

if (!process.exitCode) console.log(`traceability: ${rules.size} rule(s) traced`);
EOF

cat > specs/spec.md <<'EOF'
# relay

A **job** has a **schedule** and produces **runs**. A run is queued, running,
succeeded or failed; a failed run may be **retried**, and the retries of one run
are its **attempts**. A **board** is the view of every job and its latest run.

What it is not: a scheduler. Relay watches and reports; something else decides
when a job goes.
EOF

cat > specs/workflows/find-out-what-broke.feature <<'EOF'
@workflow:find-out-what-broke @persona:on-call
Feature: Finding out what broke overnight

  Scenario: the board is red and nobody knows why yet
    Given a board with a failed job on it
    When the run is opened
    Then its attempts are there with the error from each
EOF

cat > specs/features/schedules/board.feature <<'EOF'
@feature:schedules-board @workflow:find-out-what-broke
Feature: The board

  @rule:latest-run-decides-the-colour
  Rule: A job shows the state of its most recent run and no other

    Example: an old failure under a fresh success
      Given a job whose last run succeeded and whose previous run failed
      When the board is drawn
      Then the job reads as succeeded
EOF

cat > tests/behaviour/board.test.js <<'EOF'
import { describe, it, expect } from "vitest";
import { colourFor } from "../../src/ui/board.js";
import { rule } from "../rule.js";

rule("latest-run-decides-the-colour", () => {
  it("takes the most recent run and ignores the rest", () => {
    expect(colourFor([{ at: 2, state: "succeeded" }, { at: 1, state: "failed" }]))
      .toBe("green");
  });
});
EOF

cat > tests/rule.js <<'EOF'
import { describe } from "vitest";
import { readFileSync, readdirSync } from "node:fs";

// Looks the id up in specs/features/ and throws where the test is written.
export function rule(id, body) {
  const found = readdirSync("specs/features", { recursive: true })
    .filter((p) => String(p).endsWith(".feature"))
    .some((p) => readFileSync(`specs/features/${p}`, "utf8").includes(`@rule:${id}`));
  if (!found) throw new Error(`no such rule in specs/features/: ${id}`);
  describe(`rule:${id}`, body);
}
EOF

cat > src/ui/board.js <<'EOF'
export function colourFor(runs) {
  const latest = [...runs].sort((a, b) => b.at - a.at)[0];
  if (!latest) return "grey";
  return { succeeded: "green", failed: "red", running: "blue", queued: "grey" }[latest.state];
}
EOF

cat > src/jobs/backoff.js <<'EOF'
const CEILING_MS = 15 * 60 * 1000;

export function nextAttemptAfter(attempt) {
  return Math.min(CEILING_MS, 2 ** attempt * 1000);
}
EOF

git init -q -b main
git add -A
GIT_AUTHOR_NAME="Tomas Ek" GIT_AUTHOR_EMAIL=tomas@example.com \
GIT_COMMITTER_NAME="Tomas Ek" GIT_COMMITTER_EMAIL=tomas@example.com \
  git commit -q -m "relay: the board, and the gate that holds it"

# A history that mixes the three kinds on purpose.
for entry in \
  "0009: the attempt list unfolds under a failed run when it is opened" \
  "0010: the board carries a region column" \
  "0011: retry backoff tops out at fifteen minutes" \
  "0012: the schedule parser accepts a day-of-week field" \
  "0013: a queued job slides into place as the one ahead of it finishes"
do
  echo "$entry" >> CHANGELOG.md
  GIT_AUTHOR_NAME="Tomas Ek" GIT_AUTHOR_EMAIL=tomas@example.com \
  GIT_COMMITTER_NAME="Tomas Ek" GIT_COMMITTER_EMAIL=tomas@example.com \
    git commit -q -am "$entry"
done

git remote add origin git@github.com:tomasek/relay.git
