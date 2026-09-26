#!/usr/bin/env python3
# A workflow id is close to permanent because everything upstream names it,
# and the walkthrough tests are not this skill's to move. So a rename lands in
# two changes: the old id stays live, the new one arrives @planned, and the
# implementing change carries the tests across. This reads the tree for that
# shape, and for the two ways it goes wrong — renamed in place, or the new id
# landed live so the gate goes red on a walk nobody wrote.
import re
import subprocess
import sys
from pathlib import Path

OLD, NEW = "writing-a-sighting", "logging-a-sighting"

def heads():
    out = {}
    for f in sorted(Path("specs/workflows").glob("*.feature")):
        head = f.read_text().splitlines()[0]
        wid = re.search(r"@workflow:([\w-]+)", head)
        if wid:
            out[wid.group(1)] = {"file": f, "planned": "@planned" in head}
    return out

found = heads()
problems = []
if OLD not in found:
    problems.append(f"the old id {OLD} is gone — renamed in place, which breaks every test that walks it")
elif found[OLD]["planned"]:
    problems.append(f"the old id {OLD} is marked @planned; it is the one that is built")

if NEW not in found:
    problems.append(f"the new id {NEW} was never landed")
elif not found[NEW]["planned"]:
    problems.append(f"the new id {NEW} landed live rather than @planned, with nothing walking it yet")

tests = "\n".join(f.read_text() for f in Path("tests").rglob("*.py"))
if OLD not in tests:
    problems.append("the walkthrough test no longer names the old id; tests are not this change's to move")

proc = subprocess.run([sys.executable, "scripts/trace.py"], capture_output=True, text=True)
if proc.returncode != 0:
    problems.append("the check is red: " + " / ".join(proc.stdout.strip().splitlines()[:2]))

print("workflow ids found:", ", ".join(f"{k}{' (@planned)' if v['planned'] else ''}" for k, v in sorted(found.items())) or "none")
for p in problems:
    print("✘", p)
print(f"{len(problems)} problem(s)")
sys.exit(1 if problems else 0)
