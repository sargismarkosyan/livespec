#!/usr/bin/env python3
# The loop, read off the journey this sitting left: a paragraph under the map
# naming two of its phase headings and saying the arc goes back from one to the
# other, no column standing in for the loop, and the check still green.
# See specs/changes/0084.
import re
import subprocess
import sys
from pathlib import Path

LOOP_COLUMN = re.compile(r"repeat|loop|again|cycle|round|next (year|spring)|starts? over|new year|turns", re.I)
GOES_BACK = re.compile(r"go(es)? (back|round)|back to|comes? (back )?round|returns?|starts? (over|again)|loops?|round to|round again", re.I)

journeys = [f for f in sorted(Path("specs/journeys").glob("*.md")) if f.name != "README.md"]
target = [f for f in journeys if "@journey:a-year-on-the-patch" in f.read_text()]
if not target:
    print("the journey a-year-on-the-patch is gone")
    sys.exit(1)
text = target[0].read_text()
lines = text.splitlines()

problems = []
start = next((i for i, line in enumerate(lines) if re.match(r"^##\s+The map\s*$", line.strip())), None)
if start is None:
    print("no ## The map section")
    sys.exit(1)
section = []
for line in lines[start + 1 :]:
    if line.startswith("## "):
        break
    section.append(line)
table = [l for l in section if l.strip().startswith("|")]
if not table:
    print("no map table")
    sys.exit(1)
headings = [re.sub(r"[*_`]", "", c).strip() for c in table[0].strip().strip("|").split("|")[1:]]
headings = [h for h in headings if h]
print("phases:", headings)
for h in headings:
    if LOOP_COLUMN.search(h):
        problems.append(f"a column of the map stands in for the loop: {h!r}")
if len(set(h.lower() for h in headings)) < len(headings):
    problems.append("a phase appears twice in the map")

paragraphs, current = [], []
for line in section:
    if line.strip().startswith("|") or not line.strip():
        if current:
            paragraphs.append(" ".join(current))
        current = []
    else:
        current.append(line.strip())
if current:
    paragraphs.append(" ".join(current))

found = False
for p in paragraphs:
    plain = re.sub(r"[*_`]", "", p).lower()
    named = [h for h in headings if h.lower() in plain]
    if len(set(named)) >= 2 and GOES_BACK.search(plain):
        print("the loop:", p)
        found = True
        break
if not found:
    problems.append("no paragraph under the map names two of its phases and says the arc goes back from one to the other")

proc = subprocess.run([sys.executable, "scripts/trace.py"], capture_output=True, text=True)
if proc.returncode != 0:
    problems.append("the check is red: " + " / ".join(proc.stdout.strip().splitlines()[:2]))

for p in problems:
    print("✘", p)
print(f"{len(problems)} problem(s)")
sys.exit(1 if problems else 0)
