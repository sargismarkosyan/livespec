#!/usr/bin/env python3
# The journey layer, read the way its own README says it must be read: at
# least one journey beside the README, no workflow id, rule id or tag name in
# the prose, and no Gherkin. The first line carries the file's own tags and is
# the one place an id belongs. A step is indented or keyworded; a paragraph that
# happens to begin "Then the plot empties" is prose. Exit 1 names the line.
import re
import sys
from pathlib import Path

IDS = r"workflow:|@rule|(?<![\w-])rule:|@persona:|@feature|sowing-a-batch|checking-the-bed|keeping-the-diary"
GHERKIN = r"^(\s{2,}(Given|When|Then|And)\s|\s*(Scenario:|Scenario Outline:|Example:|Feature:|Rule:|Background:)\s)"
files = [f for f in sorted(Path("specs/journeys").glob("*.md")) if f.name != "README.md"]
if not files:
    print("no journey beside specs/journeys/README.md")
    sys.exit(1)
bad = 0
for f in files:
    for n, line in enumerate(f.read_text().splitlines(), 1):
        if n == 1 and line.startswith("@journey:"):
            continue
        if re.search(IDS, line) or re.search(GHERKIN, line):
            print(f"{f}:{n}: {line.strip()[:120]}")
            bad += 1
print(f"{len(files)} journey file(s), {bad} line(s) carrying spec jargon or Gherkin")
sys.exit(1 if bad else 0)
