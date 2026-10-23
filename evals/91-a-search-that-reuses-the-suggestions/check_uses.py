#!/usr/bin/env python3
# A feature that builds on a rule another feature owns names that feature with
# @uses on its Feature line. The shared feature does not list who uses it, and
# its rules are not copied under new ids. See specs/changes/0083.
import re
import subprocess
import sys
from pathlib import Path

SHARED = Path("specs/features/log/species-suggestions.feature")
SHARED_RULES = ("suggestions-come-from-the-species-list", "a-suggestion-is-never-forced")


def header(text: str) -> str:
    """The tag lines above the Feature: line."""
    lines = []
    for line in text.splitlines():
        if line.strip().startswith("Feature:"):
            break
        lines.append(line)
    return "\n".join(lines)


problems = []
features = {f: f.read_text() for f in Path("specs/features").rglob("*.feature")}
using = [f for f, text in features.items() if f != SHARED and "@uses:species-suggestions" in header(text)]
if not using:
    problems.append("no feature carries @uses:species-suggestions on its Feature line")
elif not any("@planned" in text for f, text in features.items() if f in using):
    problems.append(f"{', '.join(map(str, using))} carries the tag but holds no new @planned rule")

for f, text in features.items():
    for line in text.splitlines():
        if "@rule:" in line and "@uses:" in line:
            problems.append(f"{f}: @uses on a rule: {line.strip()}")

shared = features.get(SHARED, "")
if "@uses:" in shared:
    problems.append(f"{SHARED} carries @uses; the shared feature does not list who uses it")
everything = "\n".join(features.values())
for rid in SHARED_RULES:
    count = len(re.findall(rf"@rule:{rid}\b", everything))
    if count != 1:
        problems.append(f"@rule:{rid} is declared {count} times; it is owned once, by {SHARED}")

proc = subprocess.run([sys.executable, "scripts/trace.py"], capture_output=True, text=True)
if proc.returncode != 0:
    problems.append("the check is red: " + " / ".join(proc.stdout.strip().splitlines()[:2]))

for p in problems:
    print("✘", p)
print(f"{len(problems)} problem(s)")
sys.exit(1 if problems else 0)
