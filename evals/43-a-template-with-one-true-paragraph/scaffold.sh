#!/usr/bin/env bash
# millrace: meters the water each mill draws from the race and bills the
# miller monthly. Occupied — a green suite, CI, a deploy — with a CLAUDE.md
# assembled from a template last spring: placeholder overview, generic style
# rules, the plugin's loop and rules copied in, a history paragraph, and one
# paragraph only this file knows. No specs/: the process has never been set
# up here.
set -euo pipefail

mkdir -p src/millrace tests .github/workflows

cat > CLAUDE.md <<'EOF'
# millrace

> Project overview: millrace is a service. Describe what it does and who uses it here.

Millrace meters the water each mill draws from the race and bills the miller
monthly. FastAPI over PostgreSQL. Python 3.12.

## Code style

- Write clean, readable code.
- Follow best practices for the language.
- Add comments where they help.
- Keep functions small.

## The loop

1. Human tests and reports.
2. AI files issues.
3. AI writes the spec.
4. Human approves.
5. AI implements.
6. AI records the version.
7. Human merges.
8. AI closes the issue.

## Rules

- Spec before code.
- One change spec = one step = one version.
- Feedback is never fixed on the spot.
- No silent scope growth.
- Every version must run and be green.
- Rule ids are permanent.
- Always write tests.
- Never break the build.

## Commands

```sh
make check
make dev
```

## Where it runs

**Deployed on Fly.io, and reachable from the public internet.** `fly.toml`
builds it and the secrets live in the Fly dashboard. **This section said
*"Not deployed. Runs on the clerk's laptop"* until 2026-06-02**, and that
sentence was load-bearing: change 0007 argued from it that the meter-reset
endpoint needed no authentication — *"only the clerk can reach it"* — and it
was caught in review, by a person reading the diff, not by anything in this
repository. So every route is somebody else's to call: anything that changes a
reading takes a clerk token, and what the internet can reach is rate-limited.

## History

Started as a spreadsheet in 2023, moved to Flask in 2024, and to FastAPI and
PostgreSQL in change 0003. The Flask code was deleted in change 0004.
EOF

cat > README.md <<'EOF'
# millrace

Meters the water each mill draws from the race and bills the miller monthly.
Python 3.12. `make check` runs the suite; `make dev` runs the service.
EOF

cat > CONTRIBUTING.md <<'EOF'
# Contributing

Branches are `race/<what>`, squashed on merge. Issues are GitHub Issues on
`leatworks/millrace` — `gh issue create --repo leatworks/millrace`.
EOF

cat > pyproject.toml <<'EOF'
[project]
name = "millrace"
version = "2.1.0"
requires-python = ">=3.12"
dependencies = ["fastapi>=0.115", "uvicorn>=0.30", "psycopg[binary]>=3.2"]

[project.optional-dependencies]
dev = ["pytest>=8", "httpx>=0.27"]

[tool.pytest.ini_options]
testpaths = ["tests"]
EOF

cat > Makefile <<'EOF'
check:
	pytest -q

dev:
	uvicorn millrace.api:app --reload --port 8000
EOF

cat > fly.toml <<'EOF'
app = "millrace"
primary_region = "lhr"

[http_service]
  internal_port = 8000
  force_https = true
EOF

cat > src/millrace/__init__.py <<'EOF'
EOF

cat > src/millrace/meter.py <<'EOF'
"""Readings and the monthly bill. Pure."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Reading:
    mill: str
    cubic_metres: float


def bill_pence(readings: list[Reading], pence_per_cubic_metre: int = 12) -> int:
    return round(sum(r.cubic_metres for r in readings) * pence_per_cubic_metre)
EOF

cat > src/millrace/api.py <<'EOF'
import os

from fastapi import Depends, FastAPI, Header, HTTPException

from .meter import Reading, bill_pence

app = FastAPI(title="millrace")


def clerk(x_clerk_token: str = Header(default="")):
    if x_clerk_token != os.environ.get("CLERK_TOKEN", ""):
        raise HTTPException(401, "a clerk token is required")


@app.get("/mills/{mill}/bill")
def bill(mill: str):
    return {"mill": mill, "pence": bill_pence([Reading(mill, 120.0)])}


@app.post("/mills/{mill}/reset", dependencies=[Depends(clerk)])
def reset(mill: str):
    return {"mill": mill, "reset": True}
EOF

cat > tests/test_meter.py <<'EOF'
from millrace.meter import Reading, bill_pence


def test_the_bill_is_the_volume_at_the_rate():
    assert bill_pence([Reading("upper", 100.0), Reading("upper", 50.0)]) == 1800
EOF

cat > .github/workflows/ci.yml <<'EOF'
name: checks
on: [push, pull_request]
jobs:
  check:
    name: check
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -e .[dev]
      - run: make check
EOF
