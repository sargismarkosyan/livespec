#!/usr/bin/env bash
# penstock: logs the flow through a hydro scheme's penstock gauges and raises
# an alarm when a gauge disagrees with its neighbour. Occupied — a green suite,
# CI — and a CLAUDE.md of five lines that was enough for a while: a title, what
# it is, the test command, the branch convention. No loop, no fenced block, no
# pointer to any bindings. No specs/: the process has never been set up here.
set -euo pipefail

mkdir -p src/penstock tests .github/workflows

cat > CLAUDE.md <<'EOF'
# penstock

Logs the flow through the penstock gauges and alarms when two neighbours disagree. Python 3.12.
`make check` runs the tests. Branches are `flow/<what>`, squashed on merge.
EOF

cat > README.md <<'EOF'
# penstock

Flow logging for the penstock gauges, with a disagreement alarm. Python 3.12.
`make check` runs the suite.
EOF

cat > CONTRIBUTING.md <<'EOF'
# Contributing

Branches are `flow/<what>`, squashed on merge. Issues are GitHub Issues on
`hillworks/penstock` — `gh issue create --repo hillworks/penstock`.
EOF

cat > pyproject.toml <<'EOF'
[project]
name = "penstock"
version = "0.9.1"
requires-python = ">=3.12"
dependencies = []

[project.optional-dependencies]
dev = ["pytest>=8"]

[tool.pytest.ini_options]
testpaths = ["tests"]
EOF

cat > Makefile <<'EOF'
check:
	pytest -q
EOF

cat > src/penstock/__init__.py <<'EOF'
EOF

cat > src/penstock/flow.py <<'EOF'
"""Readings from the gauges, and the disagreement alarm. Pure."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Reading:
    gauge: str
    litres_per_second: float


def disagreement(a: Reading, b: Reading, tolerance: float = 0.05) -> bool:
    """Two neighbouring gauges should agree within the tolerance, as a fraction of the larger."""
    larger = max(a.litres_per_second, b.litres_per_second)
    if larger == 0:
        return False
    return abs(a.litres_per_second - b.litres_per_second) / larger > tolerance
EOF

cat > src/penstock/log.py <<'EOF'
"""The flow log: append-only, one file per day, under the data directory."""
from datetime import date
from pathlib import Path

from .flow import Reading


def append(data_dir: Path, reading: Reading, day: date | None = None) -> Path:
    day = day or date.today()
    path = data_dir / f"{day.isoformat()}.log"
    with path.open("a", encoding="utf-8") as handle:
        handle.write(f"{reading.gauge}\t{reading.litres_per_second:.2f}\n")
    return path
EOF

cat > tests/test_flow.py <<'EOF'
from penstock.flow import Reading, disagreement


def test_neighbours_within_tolerance_do_not_alarm():
    assert not disagreement(Reading("upper", 100.0), Reading("lower", 103.0))


def test_neighbours_apart_by_more_than_the_tolerance_alarm():
    assert disagreement(Reading("upper", 100.0), Reading("lower", 80.0))
EOF

cat > tests/test_log.py <<'EOF'
from datetime import date

from penstock.flow import Reading
from penstock.log import append


def test_a_reading_is_appended_to_the_days_file(tmp_path):
    path = append(tmp_path, Reading("upper", 100.0), day=date(2026, 3, 1))
    assert path.name == "2026-03-01.log"
    assert path.read_text() == "upper\t100.00\n"
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
