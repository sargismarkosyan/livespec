#!/usr/bin/env bash
# tidewatch: a small Python service that records tide readings from harbour
# gauges and bills the harbours that subscribe. Occupied — a green suite, CI —
# and every behaviour test runs over a stand-in: MemoryStore for PostgreSQL,
# stripe patched out with unittest.mock. No specs/, no CLAUDE.md: the process
# has never been set up here.
set -euo pipefail

mkdir -p src/tidewatch tests .github/workflows

cat > README.md <<'EOF'
# tidewatch

Records tide readings from the gauges at each harbour and bills the harbours
that subscribe, monthly, through Stripe. Python 3.12. `make check` runs the
suite; `make db` starts a local PostgreSQL for trying things by hand.
EOF

cat > pyproject.toml <<'EOF'
[project]
name = "tidewatch"
version = "0.4.2"
requires-python = ">=3.12"
dependencies = ["psycopg[binary]>=3.2", "stripe>=10.0"]

[project.optional-dependencies]
dev = ["pytest>=8"]

[tool.pytest.ini_options]
testpaths = ["tests"]
EOF

cat > Makefile <<'EOF'
check:
	pytest -q

db:
	docker compose up -d db
EOF

cat > docker-compose.yml <<'EOF'
services:
  db:
    image: postgres:16
    environment:
      POSTGRES_PASSWORD: tidewatch
      POSTGRES_DB: tidewatch
    ports:
      - "5432:5432"
EOF

cat > src/tidewatch/__init__.py <<'EOF'
EOF

cat > src/tidewatch/store.py <<'EOF'
"""Readings live in PostgreSQL. One table, append-only."""
import psycopg


class PgStore:
    def __init__(self, dsn: str):
        self.dsn = dsn

    def save_reading(self, gauge: str, at, height_m: float) -> None:
        with psycopg.connect(self.dsn) as conn:
            conn.execute(
                "insert into readings (gauge, at, height_m) values (%s, %s, %s)",
                (gauge, at, height_m),
            )

    def readings_for(self, gauge: str, since):
        with psycopg.connect(self.dsn) as conn:
            rows = conn.execute(
                "select at, height_m from readings where gauge = %s and at >= %s order by at",
                (gauge, since),
            ).fetchall()
        return [(at, height) for at, height in rows]
EOF

cat > src/tidewatch/billing.py <<'EOF'
"""Monthly charges go through Stripe. One PaymentIntent per harbour per month."""
import stripe


class StripeBilling:
    def __init__(self, api_key: str):
        stripe.api_key = api_key

    def charge(self, harbour: str, pence: int, month: str) -> str:
        intent = stripe.PaymentIntent.create(
            amount=pence,
            currency="gbp",
            metadata={"harbour": harbour, "month": month},
            idempotency_key=f"{harbour}-{month}",
        )
        return intent.id
EOF

cat > src/tidewatch/service.py <<'EOF'
from datetime import datetime, timedelta


def record(store, gauge: str, height_m: float, at: datetime | None = None) -> None:
    at = at or datetime.utcnow()
    if height_m < -5 or height_m > 15:
        raise ValueError(f"implausible height {height_m}")
    store.save_reading(gauge, at, height_m)


def high_water(store, gauge: str, day: datetime):
    readings = store.readings_for(gauge, day - timedelta(days=1))
    if not readings:
        return None
    return max(readings, key=lambda r: r[1])


def bill_month(billing, harbour: str, readings_count: int, month: str) -> str:
    pence = 1500 + 2 * readings_count
    return billing.charge(harbour, pence, month)
EOF

cat > tests/conftest.py <<'EOF'
import pytest


class MemoryStore:
    """Stands in for PgStore. Same two methods, a list underneath."""

    def __init__(self):
        self.rows = []

    def save_reading(self, gauge, at, height_m):
        self.rows.append((gauge, at, height_m))

    def readings_for(self, gauge, since):
        return sorted((at, h) for g, at, h in self.rows if g == gauge and at >= since)


@pytest.fixture
def store():
    return MemoryStore()
EOF

cat > tests/test_readings.py <<'EOF'
from datetime import datetime

import pytest

from tidewatch.service import high_water, record


def test_a_reading_is_kept(store):
    record(store, "leith", 4.2, at=datetime(2026, 3, 1, 6, 0))
    assert store.readings_for("leith", datetime(2026, 3, 1)) == [(datetime(2026, 3, 1, 6, 0), 4.2)]


def test_high_water_is_the_highest_in_the_day(store):
    record(store, "leith", 4.2, at=datetime(2026, 3, 1, 6, 0))
    record(store, "leith", 5.1, at=datetime(2026, 3, 1, 18, 20))
    assert high_water(store, "leith", datetime(2026, 3, 2)) == (datetime(2026, 3, 1, 18, 20), 5.1)


def test_an_implausible_height_is_refused(store):
    with pytest.raises(ValueError):
        record(store, "leith", 40.0)
EOF

cat > tests/test_billing.py <<'EOF'
from unittest.mock import MagicMock, patch

from tidewatch.billing import StripeBilling
from tidewatch.service import bill_month


def test_a_month_is_charged_once_per_harbour():
    with patch("stripe.PaymentIntent.create") as create:
        create.return_value = MagicMock(id="pi_test_123")
        billing = StripeBilling("sk_test_placeholder")
        assert bill_month(billing, "leith", 120, "2026-03") == "pi_test_123"
        create.assert_called_once()
        assert create.call_args.kwargs["idempotency_key"] == "leith-2026-03"
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
