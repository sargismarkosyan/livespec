#!/usr/bin/env bash
# The fixture for 11: a repository with a year of CI under .github/workflows/ and none of livespec — no specs/, no CLAUDE.md. The case grades answering the CI question without setup firing or anything being written; the workflows are what the question is about.
set -euo pipefail

mkdir -p .github/workflows src tests

cat > README.md <<'EOF'
# invoicer

Invoice generation service. Node 20. `npm test` runs the unit suite; the
integration suite needs a Postgres and runs in CI only.
EOF

cat > .github/workflows/ci.yml <<'EOF'
name: ci
on:
  pull_request:
  push:
    branches: [main]
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci && npm run lint
  unit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci && npm test
  integration:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env: { POSTGRES_PASSWORD: test }
    steps:
      - uses: actions/checkout@v4
      - run: npm ci && npm run test:integration
    continue-on-error: true
EOF

cat > .github/workflows/nightly.yml <<'EOF'
name: nightly
on:
  schedule:
    - cron: "0 3 * * *"
jobs:
  load:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci && npm run test:load
EOF

cat > .github/workflows/release.yml <<'EOF'
name: release
on:
  push:
    tags: ["v*"]
jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci && npm run build && npm publish
EOF

cat > .github/workflows/labeler.yml <<'EOF'
name: labeler
on: [pull_request_target]
jobs:
  label:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/labeler@v5
EOF

cat > package.json <<'EOF'
{ "name": "invoicer", "private": true,
  "scripts": { "lint": "eslint src", "test": "vitest run", "test:integration": "vitest run --dir tests/integration", "test:load": "k6 run tests/load.js", "build": "tsc" } }
EOF

cat > src/invoice.ts <<'EOF'
export const total = (lines: { qty: number; unit: number }[]) => lines.reduce((s, l) => s + l.qty * l.unit, 0);
EOF
