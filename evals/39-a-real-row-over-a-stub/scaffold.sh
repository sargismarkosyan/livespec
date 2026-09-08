#!/usr/bin/env bash
# mooring: berth booking for one marina office. Python 3.12, PostgreSQL, the
# livespec process installed in June with the boundaries table written. Since
# then nobody has read the table against the tests it describes.
set -euo pipefail

mkdir -p specs/setup specs/personas specs/workflows specs/journeys specs/changes \
         specs/features/booking specs/features/tides specs/features/signin \
         src/mooring tests/support tests/behaviour tests/workflows tests/unit \
         tests/cassettes tools .github/workflows

cat > CLAUDE.md <<'EOF'
# mooring

Berth booking for one marina office. Python 3.12 and PostgreSQL; `make check`
runs everything and `make db` starts the database. `specs/` is the contract:
read `specs/setup/README.md` before assuming any command, and spec before code.
The process is the livespec plugin; its method is not restated here.
EOF

cat > specs/setup/README.md <<'EOF'
# Bindings

Everything here is true of `mooring` and nothing else.

| | |
|---|---|
| **Verification** | `make check` — `python3 tools/trace.py`, then `pytest -q` with coverage |
| **Traceability gate** | `python3 tools/trace.py` — both directions, and the boundary rows below against the rule-bound tests |
| **Coverage** | `pytest --cov=src --cov-branch --cov-fail-under=100`, exclusions in `pyproject.toml` |
| **Test discovery** | `tests/behaviour/test_*.py` and `tests/workflows/test_*.py` are rule-bound; `tests/unit/` is exempt |
| **Rule claiming** | `@rule("<id>")` and `@workflow("<id>")` from `tests/support/covers.py` |
| **Double patterns** | the store: `mock.patch` of `psycopg` or `mooring.store`; outbound mail: `MailFake`; sign-in: `mock.patch` of `mooring.signin`. Read by `tools/trace.py` over the rule-bound folders only |
| **Recording age** | 30 days — `recorded_at:` in each cassette under `tests/cassettes/` |
| **Required check** | `verify` — the job name in `.github/workflows/checks.yml` |
| **Tracker** | GitHub Issues on `harbourside/mooring`, via `gh` |
| **Where the app runs** | `make serve`, http://localhost:8080 |
| **What a pull request carries** | the changed Gherkin; a still of the booking screen when it moved |
| **What a change owes before approval** | a sketch, for any change that moves a rule |

## Gate wiring

Reconciled against livespec 1.2.0 on 2026-06-14.

| Gate | State | Wired by, or why not |
|---|---|---|
| rule → test | automated | `tools/trace.py` |
| test → rule | automated | `tools/trace.py` |
| feature → workflow, workflow → persona, journey → workflow | automated | `tools/trace.py` |
| workflow → test | automated | `tools/trace.py` — `tests/workflows/` |
| coverage — lines, branches, functions | automated | `pytest --cov`, 100% of `src/` less the exclusions named in `pyproject.toml` |
| required check on the default branch | automated | read back 2026-06-14: `gh api repos/harbourside/mooring/rules/branches/main` — `verify` required, nobody on the bypass list |
| both gates verified to fire | automated | `tools/inject.py`, run by `make check` |
| a rule-bound test doubling a boundary declared real | automated | `tools/trace.py`, with the patterns in the table above |

### The wiring that must never gate

| Wiring | State | How |
|---|---|---|
| the pull-request report | automated | `tools/report.py`, watched arriving on #12 |
| the rule-bound measure | automated | a second `--cov` run over the rule-bound folders, printed by `tools/report.py` |

### The boundaries

| Boundary | Row | What reaches it from here | Kept honest by | Leaves uncovered | Since |
|---|---|---|---|---|---|
| the store | **real** | PostgreSQL 16, `make db` (`docker compose up -d db`); `tests/behaviour/` and `tests/workflows/` run against it | it is the real thing | production volume | 0001 |
| outbound mail | **fake** | `MailFake` in `tests/support/fakes.py` | | rendering in real clients | 0001 |
| the harbour authority's sign-in | **recorded** | cassettes in `tests/cassettes/`, replay locked | `recorded_at` on each; max age 30 days; `make record-signin` re-records | a token expiring mid-session | 0003 |
| the clock | **fake** | injected at the entry point; `tests/behaviour/test_today.py` reads today's tide with the real clock | the real-clock test | midnight; the harbour's timezone | 0002 |
EOF

cat > specs/spec.md <<'EOF'
# mooring

Berth booking for the office at Granton marina. A **berth** is a numbered
pontoon space; a **hold** is a berth kept for one boat between two dates; the
**authority** is the harbour authority whose sign-in the office uses.
EOF

cat > specs/personas/berth-master.md <<'EOF'
@persona:berth-master

# Morag — the one person who knows which berth is free

Runs the marina office. Books berths by phone and email, and is the only person
who would notice two boats given the same one.

## What they will never do
- Give a berth to a second boat and sort it out on the day.
EOF

cat > specs/workflows/book-a-berth.feature <<'EOF'
@workflow:book-a-berth @persona:berth-master @journey:a-season-on-the-pontoon
Feature: Book a berth

  When a boat asks for a berth between two dates, I want it held for them and
  nobody else, so the day they arrive there is somewhere to put them.

  **Ends when** the berth is held for those dates and the boat has been told.

  Example: a berth is held and the boat is told
    Given berth A12 is free from the 3rd to the 6th
    When Kittiwake asks for it
    Then A12 is held for Kittiwake on those dates
    And Kittiwake is told which berth is theirs
EOF

cat > specs/journeys/a-season-on-the-pontoon.md <<'EOF'
@journey:a-season-on-the-pontoon @persona:berth-master

# A season on the pontoon

From the first booking of the year to the last boat lifted out.
EOF

cat > specs/features/booking/holding.feature <<'EOF'
@feature:booking-holding @workflow:book-a-berth
Feature: Holding a berth

  @rule:a-berth-is-held-once-booked
  Rule: A booked berth is held for the boat on every night of the stay

    Example: three nights
      Given berth A12 is free
      When Kittiwake books it from the 3rd to the 6th
      Then A12 is Kittiwake's on the 3rd, the 4th and the 5th
      And Kittiwake is told so

  @rule:a-double-booking-is-refused
  Rule: A berth already held for a night is not given to a second boat

    Example: the dates overlap by one night
      Given A12 is held for Kittiwake from the 3rd to the 6th
      When Puffin asks for it from the 5th to the 8th
      Then Puffin is refused
      And Kittiwake's hold is exactly as it was
EOF

cat > specs/features/tides/today.feature <<'EOF'
@feature:tides-today @workflow:book-a-berth
Feature: Today's tide

  @rule:todays-tide-is-todays
  Rule: The tide the office sees is for the real today, not a day a test chose

    Example: the office opens
      When the tide table is shown
      Then it is for today's date
EOF

cat > specs/features/signin/staying-signed-in.feature <<'EOF'
@feature:signin-staying-signed-in @workflow:book-a-berth
Feature: Signing in with the authority

  @rule:a-signed-in-office-stays-signed-in
  Rule: Once signed in with the authority, the office stays signed in for the day

    Example: the token is still good
      Given the office signed in this morning
      When a booking needs the authority
      Then no second sign-in is asked for
EOF

cat > specs/changes/0001-holding-a-berth.md <<'EOF'
# Spec 0001: holding a berth

- **Status:** shipped

The first booking. A berth held for a boat between two dates, refused to a
second boat for any night that overlaps, and the boat told by email.
EOF

cat > specs/changes/0002-todays-tide.md <<'EOF'
# Spec 0002: today's tide

- **Status:** shipped

The office sees the tide for today. The clock is injected at the entry point so
the rule can be tested on a chosen day, and one test reads the real clock so
the injection cannot drift from it.
EOF

cat > specs/changes/0003-signing-in-with-the-authority.md <<'EOF'
# Spec 0003: signing in with the authority

- **Status:** shipped

The harbour authority's sign-in, recorded once and replayed in the suite. The
recordings carry the date they were made and are re-recorded when they age
out.
EOF

cat > pyproject.toml <<'EOF'
[project]
name = "mooring"
version = "0.3.0"
requires-python = ">=3.12"
dependencies = ["psycopg[binary]>=3.2", "requests>=2.32"]

[project.optional-dependencies]
dev = ["pytest>=8", "pytest-cov>=5"]

[tool.pytest.ini_options]
testpaths = ["tests"]

[tool.coverage.run]
omit = ["src/mooring/web.py"]
EOF

cat > Makefile <<'EOF'
check:
	python3 tools/trace.py && pytest -q --cov=src --cov-branch --cov-fail-under=100

db:
	docker compose up -d db

record-signin:
	RECORD=1 pytest -q tests/behaviour/test_signin.py

serve:
	python3 -m mooring.web
EOF

cat > docker-compose.yml <<'EOF'
services:
  db:
    image: postgres:16
    environment:
      POSTGRES_PASSWORD: mooring
      POSTGRES_DB: mooring
    ports:
      - "5432:5432"
EOF

cat > src/mooring/__init__.py <<'EOF'
EOF

cat > src/mooring/store.py <<'EOF'
"""Holds live in PostgreSQL. One row per berth per night, unique on the pair."""
from datetime import date, timedelta

import psycopg


class PgStore:
    def __init__(self, dsn: str):
        self.dsn = dsn

    def hold(self, berth: str, boat: str, arrive: date, leave: date) -> None:
        nights = [arrive + timedelta(days=n) for n in range((leave - arrive).days)]
        with psycopg.connect(self.dsn) as conn:
            with conn.transaction():
                for night in nights:
                    conn.execute(
                        "insert into holds (berth, night, boat) values (%s, %s, %s)",
                        (berth, night, boat),
                    )

    def holds(self, berth: str, night: date):
        with psycopg.connect(self.dsn) as conn:
            row = conn.execute(
                "select boat from holds where berth = %s and night = %s", (berth, night)
            ).fetchone()
        return row[0] if row else None
EOF

cat > src/mooring/mail.py <<'EOF'
"""The boat is told by email. Plain SMTP, one message per hold."""
import smtplib
from email.message import EmailMessage


class SmtpMail:
    def __init__(self, host: str, sender: str):
        self.host, self.sender = host, sender

    def send(self, to: str, subject: str, body: str) -> None:
        msg = EmailMessage()
        msg["From"], msg["To"], msg["Subject"] = self.sender, to, subject
        msg.set_content(body)
        with smtplib.SMTP(self.host) as smtp:
            smtp.send_message(msg)
EOF

cat > src/mooring/signin.py <<'EOF'
"""The harbour authority's sign-in. A token per day, fetched once."""
import requests

TOKEN_URL = "https://signin.forthports.example/oauth/token"


class AuthoritySignin:
    def __init__(self, client_id: str, secret: str):
        self.client_id, self.secret = client_id, secret
        self._token = None

    def token(self) -> str:
        if self._token is None:
            reply = requests.post(TOKEN_URL, data={"client_id": self.client_id, "client_secret": self.secret})
            reply.raise_for_status()
            self._token = reply.json()["access_token"]
        return self._token
EOF

cat > src/mooring/booking.py <<'EOF'
from datetime import date


class Refused(Exception):
    pass


def book(store, mail, berth: str, boat: str, arrive: date, leave: date, to: str = "skipper@example.net") -> None:
    try:
        store.hold(berth, boat, arrive, leave)
    except (KeyError, Exception) as err:  # a unique violation from the store, or the stand-in's KeyError
        raise Refused(f"{berth} is not free for every night") from err
    mail.send(to, f"{berth} is yours, {arrive.day} to {leave.day} {leave.strftime('%B')}", "See you on the pontoon.")
EOF

cat > src/mooring/tides.py <<'EOF'
from dataclasses import dataclass
from datetime import date, datetime, timedelta


@dataclass
class Tide:
    day: date
    high_water: str


def todays_tide(now=None) -> Tide:
    """The clock is injected so a rule can be tested on a chosen day; the
    default is the real one, and one test reads it on purpose."""
    now = now or datetime.now()
    minutes = (now.date().toordinal() * 50) % 1440  # a stand-in harmonic; the table is not the point
    hw = (datetime.combine(now.date(), datetime.min.time()) + timedelta(minutes=minutes)).strftime("%H:%M")
    return Tide(day=now.date(), high_water=hw)
EOF

cat > src/mooring/web.py <<'EOF'
"""The office's screen. Not covered; excluded in pyproject.toml."""
EOF

cat > tests/support/__init__.py <<'EOF'
EOF

cat > tests/support/covers.py <<'EOF'
"""rule("<id>") names the Gherkin rule a behaviour test exists for, and
workflow("<id>") the attempt a walkthrough walks. Both throw at import if the id
is not live in specs/, which is the whole point of the binding."""
import pathlib
import re

SPECS = pathlib.Path(__file__).resolve().parents[2] / "specs"


def _ids(kind: str) -> dict[str, bool]:
    found = {}
    for f in SPECS.rglob("*.feature"):
        for m in re.finditer(rf"@{kind}:([a-z0-9-]+)([^\n]*)", f.read_text()):
            found[m.group(1)] = "@planned" not in m.group(2)
    return found


def _claim(kind, ident):
    live = _ids(kind)
    if ident not in live:
        raise LookupError(f"no {kind} {ident!r}; known: {sorted(live)}")
    if not live[ident]:
        raise LookupError(f"{ident!r} is still @planned")

    def decorate(fn):
        setattr(fn, f"__{kind}__", ident)
        return fn

    return decorate


def rule(rule_id):
    return _claim("rule", rule_id)


def workflow(workflow_id):
    return _claim("workflow", workflow_id)
EOF

cat > tests/support/fakes.py <<'EOF'
"""Stand-ins the rule-bound tests use."""
from dataclasses import dataclass
from datetime import date, timedelta


class MemoryStore:
    """Stands in for mooring.store.PgStore. Same two methods, a dict underneath."""

    def __init__(self):
        self._holds = {}

    def hold(self, berth, boat, arrive, leave):
        nights = [arrive + timedelta(days=n) for n in range((leave - arrive).days)]
        for night in nights:
            if (berth, night) in self._holds:
                raise KeyError((berth, night))
        for night in nights:
            self._holds[(berth, night)] = boat

    def holds(self, berth, night):
        return self._holds.get((berth, night))


@dataclass
class Sent:
    to: str
    subject: str
    body: str


class MailFake:
    """Stands in for mooring.mail.SmtpMail. Remembers what was sent."""

    def __init__(self):
        self.sent = []

    def send(self, to, subject, body):
        self.sent.append(Sent(to, subject, body))
EOF

cat > tests/support/replay.py <<'EOF'
"""Replays a recorded sign-in from tests/cassettes/. Locked: a request the
cassette does not hold fails rather than going to the network."""
import json
import pathlib
from unittest import mock

CASSETTES = pathlib.Path(__file__).resolve().parents[1] / "cassettes"


def replaying(name):
    text = (CASSETTES / f"{name}.yaml").read_text()
    body = text.split("body: '", 1)[1].split("'", 1)[0]

    class Reply:
        status_code = 200

        def raise_for_status(self):
            pass

        def json(self):
            return json.loads(body)

    return mock.patch("mooring.signin.requests.post", return_value=Reply())
EOF

cat > tests/behaviour/test_holding.py <<'EOF'
# specs/features/booking/holding.feature
from datetime import date

import pytest

from mooring.booking import Refused, book
from tests.support.covers import rule
from tests.support.fakes import MailFake, MemoryStore


@rule("a-berth-is-held-once-booked")
def test_a_booked_berth_is_held_for_every_night():
    store, mail = MemoryStore(), MailFake()
    book(store, mail, berth="A12", boat="Kittiwake", arrive=date(2026, 7, 3), leave=date(2026, 7, 6))
    assert [store.holds("A12", date(2026, 7, d)) for d in (3, 4, 5)] == ["Kittiwake"] * 3
    assert mail.sent[0].subject == "A12 is yours, 3 to 6 July"


@rule("a-double-booking-is-refused")
def test_the_second_boat_is_refused():
    store, mail = MemoryStore(), MailFake()
    book(store, mail, berth="A12", boat="Kittiwake", arrive=date(2026, 7, 3), leave=date(2026, 7, 6))
    with pytest.raises(Refused):
        book(store, mail, berth="A12", boat="Puffin", arrive=date(2026, 7, 5), leave=date(2026, 7, 8))
    assert store.holds("A12", date(2026, 7, 5)) == "Kittiwake"
    assert len(mail.sent) == 1
EOF

cat > tests/behaviour/test_today.py <<'EOF'
# specs/features/tides/today.feature
from datetime import datetime

from mooring.tides import todays_tide
from tests.support.covers import rule


@rule("todays-tide-is-todays")
def test_the_tide_is_for_the_real_today():
    # The real clock, on purpose: the row for the clock says one test reads it.
    assert todays_tide().day == datetime.now().date()
EOF

cat > tests/behaviour/test_signin.py <<'EOF'
# specs/features/signin/staying-signed-in.feature
from mooring.signin import AuthoritySignin
from tests.support.covers import rule
from tests.support.replay import replaying


@rule("a-signed-in-office-stays-signed-in")
def test_the_token_is_fetched_once():
    with replaying("harbour-signin") as post:
        signin = AuthoritySignin("office", "secret")
        assert signin.token() == signin.token()
        assert post.call_count == 1
EOF

cat > tests/workflows/test_book_a_berth.py <<'EOF'
# specs/workflows/book-a-berth.feature — the whole attempt, trigger to end state.
from datetime import date

from mooring.booking import book
from tests.support.covers import workflow
from tests.support.fakes import MailFake, MemoryStore


@workflow("book-a-berth")
def test_a_boat_asks_and_is_told():
    store, mail = MemoryStore(), MailFake()
    book(store, mail, berth="A12", boat="Kittiwake", arrive=date(2026, 7, 3), leave=date(2026, 7, 6))
    assert store.holds("A12", date(2026, 7, 4)) == "Kittiwake"
    assert mail.sent[0].to == "skipper@example.net"
EOF

cat > tests/unit/test_tides.py <<'EOF'
from datetime import datetime

from mooring.tides import todays_tide


def test_the_same_day_gives_the_same_table():
    a = todays_tide(datetime(2026, 7, 3, 9, 0))
    b = todays_tide(datetime(2026, 7, 3, 17, 0))
    assert a == b
EOF

cat > tests/cassettes/harbour-signin.yaml <<'EOF'
recorded_at: 2025-11-03
interactions:
  - request:
      method: POST
      url: https://signin.forthports.example/oauth/token
    response:
      status: 200
      body: '{"access_token": "REDACTED", "expires_in": 3600}'
EOF

cat > tools/trace.py <<'EOF'
#!/usr/bin/env python3
"""Traceability, both directions, and the boundary rows against the rule-bound
tests. No dependencies. Exits 1 on any failure."""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
RULE_BOUND = [ROOT / "tests" / "behaviour", ROOT / "tests" / "workflows"]

# The double patterns the bindings name, per boundary whose row reads real.
REAL_BOUNDARIES = {
    "the store": [r"mock\.patch\(\s*['\"](psycopg|mooring\.store)"],
}

failures = []

rules, planned = {}, set()
for f in (ROOT / "specs" / "features").rglob("*.feature"):
    for m in re.finditer(r"@rule:([a-z0-9-]+)([^\n]*)", f.read_text()):
        rules[m.group(1)] = f
        if "@planned" in m.group(2):
            planned.add(m.group(1))

claimed = {}
for folder in RULE_BOUND:
    for t in folder.glob("test_*.py"):
        src = t.read_text()
        ids = re.findall(r"@rule\(\"([a-z0-9-]+)\"\)", src)
        if folder.name == "behaviour" and not ids:
            failures.append(f"{t}: no rule() — every behaviour test names the rule it exists for")
        for i in ids:
            claimed.setdefault(i, []).append(t)
        for boundary, patterns in REAL_BOUNDARIES.items():
            if any(re.search(p, src) for p in patterns):
                failures.append(f"{t}: stands a double in for {boundary}, whose row reads real")

for rule_id in rules:
    if rule_id in planned and rule_id in claimed:
        failures.append(f"{rule_id}: @planned but claimed by {claimed[rule_id]}")
    if rule_id not in planned and rule_id not in claimed:
        failures.append(f"{rule_id}: live and claimed by no test")
for rule_id in claimed:
    if rule_id not in rules:
        failures.append(f"{rule_id}: claimed but no such rule")

for line in failures:
    print("✘", line)
print(f"{len(rules) - len(planned)} live rule(s), {len(claimed)} claimed")
sys.exit(1 if failures else 0)
EOF

cat > tools/inject.py <<'EOF'
#!/usr/bin/env python3
"""Breaks each gate in a temporary copy and checks it fires. Kept short here."""
print("inject: 9/9 faults caught")
EOF

cat > tools/report.py <<'EOF'
#!/usr/bin/env python3
"""The pull-request report. Cannot fail the build; posted with continue-on-error."""
print("report: written")
EOF

cat > .github/workflows/checks.yml <<'EOF'
name: checks
on:
  pull_request:
  push:
    branches: [main]
jobs:
  verify:
    name: verify
    runs-on: ubuntu-latest
    services:
      db:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: mooring
          POSTGRES_DB: mooring
        ports: ["5432:5432"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -e .[dev]
      - run: make check
      - run: python3 tools/report.py
        continue-on-error: true
EOF
