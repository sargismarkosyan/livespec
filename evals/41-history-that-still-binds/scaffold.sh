#!/usr/bin/env bash
# sluicegate: schedules lock openings on a canal for the keepers who work them.
# Occupied — a green suite, CI, a deploy — with a CLAUDE.md written by hand over
# a year, in its own shape. Two of its paragraphs are what the case grades: a
# dated account under "Where it runs" that still binds every new route, and a
# finished migration under "How it got here" that binds nothing. No specs/: the
# process has never been set up here.
set -euo pipefail

mkdir -p src/sluicegate tests .github/workflows

cat > README.md <<'EOF'
# sluicegate

Schedules lock openings on the canal for the keepers who work them. FastAPI
over PostgreSQL, Python 3.12. `make check` runs the suite; `make dev` runs the
service against the compose database.
EOF

cat > CONTRIBUTING.md <<'EOF'
# Contributing

Branches are `keeper/<what>`, squashed on merge. Issues are GitHub Issues on
`canalworks/sluicegate` — `gh issue create --repo canalworks/sluicegate`.
EOF

cat > pyproject.toml <<'EOF'
[project]
name = "sluicegate"
version = "1.3.0"
requires-python = ">=3.12"
dependencies = ["fastapi>=0.115", "uvicorn>=0.30", "psycopg[binary]>=3.2", "slowapi>=0.1.9"]

[project.optional-dependencies]
dev = ["pytest>=8", "httpx>=0.27"]

[tool.pytest.ini_options]
testpaths = ["tests"]
EOF

cat > Makefile <<'EOF'
check:
	python3 -m pytest -q

dev:
	uvicorn sluicegate.api:app --reload --port 8000

db:
	docker compose up -d db
EOF

cat > fly.toml <<'EOF'
app = "sluicegate"
primary_region = "lhr"

[build]
  builder = "paketobuildpacks/builder:base"

[http_service]
  internal_port = 8000
  force_https = true
EOF

cat > docker-compose.yml <<'EOF'
services:
  db:
    image: postgres:16
    environment:
      POSTGRES_PASSWORD: sluicegate
      POSTGRES_DB: sluicegate
    ports:
      - "5432:5432"
EOF

cat > CLAUDE.md <<'EOF'
# sluicegate

Schedules lock openings on the canal for the keepers who work them. A keeper
enters the boats waiting at each lock; the service works out an opening order
that keeps water in the summit pound and tells each keeper when to open.
FastAPI over PostgreSQL. Python 3.12.

## Getting a session going

    make check      # pytest, quick
    make dev        # uvicorn on :8000 against the compose database
    make db         # postgres in docker, for poking at by hand

Branches are `keeper/<what>`; squash on merge. `main` deploys.

## Where it runs

**Deployed on Fly.io, and reachable from the public internet.** `fly.toml`
builds it, `src/sluicegate/api.py` reads `FLY_APP_NAME` for its own base URL,
and the secrets live in the Fly dashboard. **This section said *"Not deployed.
Runs on the lock-keeper's laptop"* until 2026-07-30**, and that sentence was
load-bearing: change 0019 argued from it that the gate-override endpoint
needed no authentication — *"the only caller is the keeper on the same
machine"* — and it was caught in review, by a person reading the diff, not by
anything in this repository.

So every route is somebody else's to call. Three things follow for anything
new:

- **Authenticate the overrides.** Anything that opens a gate takes a keeper
  token, the way `POST /locks/{id}/override` does now.
- **Rate-limit what the internet can reach**, as the limiter in `api.py`
  already does for the public schedule.
- **The filesystem is not storage.** Fly replaces it on every deploy. Anything
  that must survive goes to Postgres.

## How it got here

Until March 2025 this was a Flask app with SQLite, under `legacy/`. The move
to FastAPI and PostgreSQL finished in change 0011, the data was migrated by a
one-off script that ran once and was deleted, and `legacy/` itself went in
change 0012. The old blueprints are in git history if anybody is curious; the
`schedule.py` algorithm is the one piece that survived the move unchanged.

## What is where

    src/sluicegate/api.py        the routes, the limiter, the keeper-token check
    src/sluicegate/schedule.py   the opening-order algorithm, pure
    src/sluicegate/store.py      Postgres, one module, all the SQL
    tests/                       pytest; a MemoryStore stands in for Postgres
    fly.toml                     the deploy

## Things a session keeps getting wrong

- `schedule.py` is pure. It takes lists and returns lists; it does not open a
  connection, and a change that makes it do so is wrong however convenient.
- Times are UTC in the database and local at the lock. Convert at the edge,
  in `api.py`, and nowhere else.
- The summit pound is the constraint everything else bends to. An opening
  order that drains it is wrong even if every boat gets through faster.
EOF

cat > src/sluicegate/__init__.py <<'EOF'
EOF

cat > src/sluicegate/schedule.py <<'EOF'
"""The opening order. Pure: lists in, lists out, no connection anywhere."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Waiting:
    lock: str
    boat: str
    direction: str  # "up" or "down"
    since_minutes: int


def opening_order(waiting: list[Waiting], summit_level_cm: int, floor_cm: int = 120) -> list[Waiting]:
    """Longest wait first, but never an uphill opening that would drain the summit."""
    ordered = sorted(waiting, key=lambda w: -w.since_minutes)
    if summit_level_cm <= floor_cm:
        ordered = [w for w in ordered if w.direction == "down"]
    return ordered
EOF

cat > src/sluicegate/store.py <<'EOF'
"""Postgres. One module, all the SQL."""
import psycopg


class PgStore:
    def __init__(self, dsn: str):
        self.dsn = dsn

    def waiting_at(self, lock: str):
        with psycopg.connect(self.dsn) as conn:
            return conn.execute(
                "select boat, direction, since_minutes from waiting where lock = %s", (lock,)
            ).fetchall()

    def summit_level(self) -> int:
        with psycopg.connect(self.dsn) as conn:
            return conn.execute("select level_cm from summit order by at desc limit 1").fetchone()[0]
EOF

cat > src/sluicegate/api.py <<'EOF'
import os

from fastapi import Depends, FastAPI, Header, HTTPException, Request
from slowapi import Limiter
from slowapi.util import get_remote_address

from .schedule import Waiting, opening_order

app = FastAPI(title="sluicegate")
limiter = Limiter(key_func=get_remote_address)
BASE_URL = f"https://{os.environ.get('FLY_APP_NAME', 'localhost')}.fly.dev"


def keeper(x_keeper_token: str = Header(default="")):
    if x_keeper_token != os.environ.get("KEEPER_TOKEN", ""):
        raise HTTPException(401, "a keeper token is required")


@app.get("/locks/{lock}/schedule")
@limiter.limit("60/minute")
def schedule(lock: str, request: Request):
    store = request.app.state.store
    waiting = [Waiting(lock, b, d, m) for b, d, m in store.waiting_at(lock)]
    return [w.boat for w in opening_order(waiting, store.summit_level())]


@app.post("/locks/{lock}/override", dependencies=[Depends(keeper)])
def override(lock: str, request: Request):
    return {"lock": lock, "opened": True}
EOF

cat > tests/conftest.py <<'EOF'
import pytest


class MemoryStore:
    """Stands in for PgStore: the same two methods over a dict."""

    def __init__(self, waiting=None, level=200):
        self.waiting = waiting or {}
        self.level = level

    def waiting_at(self, lock):
        return self.waiting.get(lock, [])

    def summit_level(self):
        return self.level


@pytest.fixture
def store():
    return MemoryStore()
EOF

cat > tests/test_schedule.py <<'EOF'
from sluicegate.schedule import Waiting, opening_order


def test_longest_wait_opens_first():
    w = [Waiting("lock-3", "Heron", "up", 10), Waiting("lock-3", "Kestrel", "down", 45)]
    assert [x.boat for x in opening_order(w, 200)] == ["Kestrel", "Heron"]


def test_a_low_summit_refuses_uphill_openings():
    w = [Waiting("lock-3", "Heron", "up", 90), Waiting("lock-3", "Kestrel", "down", 5)]
    assert [x.boat for x in opening_order(w, 110)] == ["Kestrel"]
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
