#!/usr/bin/env python3
# The phase the new workflow names, read off the file this sitting wrote: it
# names a-question-comes-up, every phase it names is one the journey's map
# has, and the journey is as the fixture left it. See specs/changes/0084.
import re
import subprocess
import sys
from pathlib import Path

PHASES = {"before-the-log", "out-on-the-patch", "a-question-comes-up", "the-quiet-months"}
known = {"writing-a-sighting"}
new = []
for f in sorted(Path("specs/workflows").glob("*.feature")):
    head = f.read_text().splitlines()[0] if f.read_text().strip() else ""
    wid = re.search(r"@workflow:([\w-]+)", head)
    if wid and wid.group(1) not in known:
        new.append((f, head))
if not new:
    print("no new workflow file in specs/workflows/")
    sys.exit(1)

problems = []
for f, head in new:
    named = re.findall(r"@phase:([\w-]+)", head)
    print(f"{f.name}: phases named {named or 'none'}")
    if "a-question-comes-up" not in named:
        problems.append(f"{f.name}: does not name @phase:a-question-comes-up")
    for phase in named:
        if phase not in PHASES:
            problems.append(f"{f.name}: names @phase:{phase}, which the journey's map does not have")

first = subprocess.run(["git", "rev-list", "--max-parents=0", "HEAD"], capture_output=True, text=True).stdout.split()
moved = subprocess.run(["git", "diff", "--quiet", first[-1] if first else "HEAD", "--", "specs/journeys"], capture_output=True)
if moved.returncode != 0:
    problems.append("the journey was changed; a phase is the journey's own, and its change is a separate one")

for p in problems:
    print("✘", p)
print(f"{len(problems)} problem(s)")
sys.exit(1 if problems else 0)
