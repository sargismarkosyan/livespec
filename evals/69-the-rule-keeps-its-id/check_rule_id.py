#!/usr/bin/env python3
# A reworded rule is the same rule. Its id is what every test points at, so
# editing in place keeps the id and the walk; a new id orphans the test. And
# the examples are written in the repository's own words — spec.md says a
# sighting is not an entry, a record or an item.
import re
import subprocess
import sys
from pathlib import Path

ID = "an-unnamed-bird-is-written-as-it-stands"
RETIRED = r"\b(entry|entries|item|items|record|records)\b"

text = "\n".join(f.read_text() for f in Path("specs/features").rglob("*.feature"))
problems = []

if f"@rule:{ID}" not in text:
    problems.append(f"the rule id {ID} is gone — a reworded rule is the same rule, and every test points at the id")

body = re.search(rf"@rule:{ID}\b(.*?)(?=@rule:|\Z)", text, re.S)
if body and not re.search(r"\buncertain\b|\bunsure\b|\bnot sure\b|\bflag\b", body.group(1), re.I):
    problems.append(f"the rule {ID} does not mention what the change asked for")

for m in re.finditer(RETIRED, text, re.I):
    line = text[: m.start()].count("\n") + 1
    problems.append(f"a word the repository retired appears in the features at line {line}: {m.group(0)!r}")
    break

proc = subprocess.run([sys.executable, "scripts/trace.py"], capture_output=True, text=True)
if proc.returncode != 0:
    problems.append("the check is red: " + " / ".join(proc.stdout.strip().splitlines()[:2]))

for p in problems:
    print("✘", p)
print(f"{len(problems)} problem(s)")
sys.exit(1 if problems else 0)
