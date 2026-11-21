#!/usr/bin/env python3
# What the withdrawal makes dead, named in the change spec this sitting wrote:
# the rule, the test that claims it, and the where field the code writes and
# renders. The check reads the spec's removal section, by whatever heading says
# it removes, and the fixture's own traceability check. See specs/changes/0085.
import re
import subprocess
import sys
from pathlib import Path

specs = [f for f in sorted(Path("specs/changes").glob("*.md")) if not f.name.startswith("0006")]
if not specs:
    print("no new change spec in specs/changes/")
    sys.exit(1)

text = "\n".join(f.read_text() for f in specs)
section = re.search(r"^#+[^\n]*(remov|delet|what goes)[^\n]*\n(.*?)(?=^#{1,2} |\Z)", text, re.I | re.M | re.S)
problems = []
if not section:
    problems.append("the change spec has no section saying what it removes")
else:
    body = section.group(2)
    if "place-carries-from-the-last-sighting" not in body:
        problems.append("the removal section does not name the rule place-carries-from-the-last-sighting")
    if not re.search(r"test_the_place|tests/", body):
        problems.append("the removal section does not name the test that claims the rule")
    if not re.search(r"\bwhere\b|store\.js|fieldnote\.js", body):
        problems.append("the removal section does not name the where field the code writes and renders")

proc = subprocess.run([sys.executable, "scripts/trace.py"], capture_output=True, text=True)
if proc.returncode != 0:
    problems.append("the traceability check is red:\n" + proc.stdout[-600:])

for p in problems:
    print("✘", p)
print(f"{len(problems)} problem(s)")
sys.exit(1 if problems else 0)
