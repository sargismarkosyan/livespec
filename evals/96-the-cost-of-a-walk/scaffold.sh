#!/usr/bin/env bash
# printshop: one illustrator's print shop, a static page and a small Node
# server. The process is set up; two Playwright walkthroughs walk its two
# workflows; the ledger predates the cost of a walk, so it has no row for
# wiring:workflow-cost or gate:workflow-budget. See specs/changes/0089.
set -euo pipefail

mkdir -p src tests/workflows specs/personas specs/workflows specs/features/shop specs/changes specs/setup scripts .github/workflows

cat > README.md <<'EOF'
# printshop

One illustrator's print shop: browse the prints, buy one. `node server.js`
serves `src/` on port 4173. `npx playwright test` walks the workflows.
EOF

cat > package.json <<'EOF'
{
  "name": "printshop",
  "private": true,
  "scripts": {
    "start": "node server.js",
    "walk": "playwright test"
  },
  "devDependencies": {
    "@playwright/test": "^1.58.0"
  }
}
EOF

cat > playwright.config.js <<'EOF'
const { defineConfig } = require("@playwright/test");

module.exports = defineConfig({
  testDir: "tests/workflows",
  workers: 1,
  retries: 0,
  use: { baseURL: "http://localhost:4173", headless: true },
  webServer: { command: "node server.js", port: 4173, reuseExistingServer: false },
});
EOF

cat > server.js <<'EOF'
const http = require("http");
const fs = require("fs");
const path = require("path");

const prints = [
  { id: "heron", title: "Heron at dusk", price: 40 },
  { id: "weir", title: "The weir in March", price: 55 },
];

http.createServer((req, res) => {
  if (req.url === "/api/prints") {
    res.setHeader("content-type", "application/json");
    return res.end(JSON.stringify(prints));
  }
  if (req.url === "/api/orders" && req.method === "POST") {
    res.statusCode = 201;
    return res.end(JSON.stringify({ order: Date.now() }));
  }
  const file = path.join(__dirname, "src", req.url === "/" ? "index.html" : req.url);
  fs.readFile(file, (err, body) => {
    res.statusCode = err ? 404 : 200;
    res.end(err ? "not found" : body);
  });
}).listen(4173);
EOF

cat > src/index.html <<'EOF'
<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><title>printshop</title></head>
<body>
  <h1>Prints</h1>
  <ul id="prints"></ul>
  <section id="checkout" hidden>
    <h2>Checkout</h2>
    <p id="chosen"></p>
    <button id="pay">Pay</button>
    <p id="done" hidden>Thank you — your print is on its way.</p>
  </section>
  <script src="app.js"></script>
</body>
</html>
EOF

cat > src/app.js <<'EOF'
async function load() {
  const prints = await (await fetch("/api/prints")).json();
  const list = document.getElementById("prints");
  for (const p of prints) {
    const li = document.createElement("li");
    li.innerHTML = `<button data-id="${p.id}">${p.title} — £${p.price}</button>`;
    li.querySelector("button").onclick = () => choose(p);
    list.appendChild(li);
  }
  performance.mark("printshop:list-shown");
}

function choose(p) {
  document.getElementById("checkout").hidden = false;
  document.getElementById("chosen").textContent = p.title;
  document.getElementById("pay").onclick = async () => {
    await fetch("/api/orders", { method: "POST", body: JSON.stringify({ id: p.id }) });
    document.getElementById("done").hidden = false;
    performance.mark("printshop:paid");
  };
}

load();
EOF

cat > tests/workflows/browse-the-prints.spec.js <<'EOF'
// @workflow:browse-the-prints — walked end to end.
const { test, expect } = require("@playwright/test");

test("browse-the-prints", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("button", { name: /Heron at dusk/ })).toBeVisible();
  await expect(page.getByRole("button", { name: /The weir in March/ })).toBeVisible();
});
EOF

cat > tests/workflows/buy-a-print.spec.js <<'EOF'
// @workflow:buy-a-print — walked end to end.
const { test, expect } = require("@playwright/test");

test("buy-a-print", async ({ page }) => {
  await page.goto("/");
  await page.getByRole("button", { name: /The weir in March/ }).click();
  await page.getByRole("button", { name: "Pay" }).click();
  await expect(page.getByText("your print is on its way")).toBeVisible();
});
EOF

cat > scripts/trace.py <<'EOF'
#!/usr/bin/env python3
"""printshop's traceability gate: every workflow is walked by a file in tests/workflows/. Standard library."""
import re
import sys
from pathlib import Path

walked = {m.group(1) for f in Path("tests/workflows").glob("*.spec.js")
          for m in re.finditer(r"@workflow:([\w-]+)", f.read_text())}
missing = []
for f in sorted(Path("specs/workflows").glob("*.feature")):
    wid = re.search(r"@workflow:([\w-]+)", f.read_text()).group(1)
    if wid not in walked:
        missing.append(wid)
for wid in missing:
    print(f"✘ workflow {wid} is walked by no test")
sys.exit(1 if missing else 0)
EOF

cat > .github/workflows/ci.yml <<'EOF'
name: ci
on: [pull_request]
jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 22 }
      - run: npm ci
      - run: npx playwright install --with-deps chromium
      - run: python3 scripts/trace.py
      - run: npx playwright test
  report:
    needs: verify
    if: ${{ !cancelled() }}
    runs-on: ubuntu-latest
    continue-on-error: true
    permissions: { pull-requests: write }
    steps:
      - uses: actions/checkout@v4
      - run: python3 scripts/trace.py > trace.txt || true
      - run: gh pr comment ${{ github.event.pull_request.number }} --body-file trace.txt --edit-last --create-if-none
        env: { GH_TOKEN: "${{ github.token }}" }
EOF

cat > specs/personas/illustrator.md <<'EOF'
@persona:illustrator

# Ines — sells her own prints, between commissions

She checks the shop on her phone between jobs. A sale that does not go
through is a sale she never hears about.
EOF

cat > specs/workflows/browse-the-prints.feature <<'EOF'
@workflow:browse-the-prints @persona:illustrator
Feature: Browse the prints

  A buyer opens the shop and sees every print with its price.

  Example: the shop opens
    Given the shop has two prints
    When a buyer opens it
    Then both prints are listed with their prices
EOF

cat > specs/workflows/buy-a-print.feature <<'EOF'
@workflow:buy-a-print @persona:illustrator
Feature: Buy a print

  A buyer picks a print and pays for it.

  Example: a print is bought
    Given a buyer has chosen The weir in March
    When they pay
    Then they are told it is on its way
EOF

cat > specs/features/shop/listing.feature <<'EOF'
@feature:listing @workflow:browse-the-prints @workflow:buy-a-print
Feature: The listing

  @rule:every-print-has-its-price
  Rule: Every print is listed with its price

    Example: two prints
      Given the shop has two prints
      When the listing loads
      Then each shows its price
EOF

cat > specs/changes/0003-pay-in-one-tap.md <<'EOF'
# Spec 0003: pay in one tap

- **Status:** shipped
EOF

cat > CLAUDE.md <<'EOF'
# printshop

One illustrator's print shop. `specs/` is the contract: read
[specs/setup/README.md](specs/setup/README.md) before assuming any command.

## The loop

1. Ines reports what she found; `todo` files it.
2. `refine-spec` writes the spec; Ines approves it.
3. Implement, verification green, open the pull request.

## Commands

```sh
python3 scripts/trace.py && npx playwright test   # verification
```
EOF

cat > specs/setup/README.md <<'EOF'
# Bindings

Everything here is true of printshop and nothing else.

## The table

| | |
|---|---|
| **Verification** | `python3 scripts/trace.py && npx playwright test` |
| **Language** | JavaScript (Node 22) for the app; Python 3 standard library for the gates |
| **Walkthroughs** | `tests/workflows/*.spec.js`, one per workflow, Playwright against `node server.js` |
| **CI** | GitHub Actions, `.github/workflows/ci.yml`; `main` protected, `verify` required |
| **Tracker** | GitHub Issues, via `gh issue create` |
| **Deliverable of a version** | a GIF of the workflow it changed |

## What is wired

Reconciled against livespec 1.32.1.

### The gates

| id | gate | state | evidence |
|---|---|---|---|
| `gate:workflow-walked` | a workflow walked by no test | automated | `scripts/trace.py`; watched failing on a workflow with no spec file, 2026-10-02 |
| `gate:coverage` | a module under the thresholds | deferred | since 0002: no unit tests yet |

### The wiring that must never gate

| id | wiring | state | evidence |
|---|---|---|---|
| `wiring:pr-report` | the pull-request report | automated | the `report` job in `ci.yml`, `continue-on-error`; watched arriving on #4 |
EOF

git init -q -b main
git add -A
git -c user.name=ines -c user.email=ines@printshop.example commit -q -m "printshop, with the process"
