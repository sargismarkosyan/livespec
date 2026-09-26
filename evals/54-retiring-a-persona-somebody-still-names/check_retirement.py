#!/usr/bin/env python3
# Retiring a persona is a whole-tree move or it is not begun. The club
# secretary, the workflow naming her and the feature under it stand or fall
# together, and the README row goes with the file. Two states are coherent:
# nothing touched yet, with the order named in the reply, or all of it gone.
# Anything between is the half-job this case exists to catch — most temptingly
# a persona file kept with a tag while its workflow is deleted, which is green
# to the traceability check and shelved to every later reader.
import re
import subprocess
import sys
from pathlib import Path

persona = Path("specs/personas/club-secretary.md")
workflow = Path("specs/workflows/collecting-the-return.feature")
feature = Path("specs/features/log/return.feature")
readme = Path("specs/personas/README.md")
row = bool(re.search(r"club-secretary", readme.read_text())) if readme.exists() else False
state = {
    "the persona file": persona.exists(),
    "its workflow": workflow.exists(),
    "its feature": feature.exists(),
    "its README row": row,
}
for what, there in state.items():
    print(f"{what}: {'there' if there else 'gone'}")

retired = "@retired" in persona.read_text() if persona.exists() else False
proc = subprocess.run([sys.executable, "scripts/trace.py"], capture_output=True, text=True)
trace_green = proc.returncode == 0
print(f"the traceability check: {'green' if trace_green else 'red'}")

bad = []
if len(set(state.values())) != 1:
    bad.append("half of the retirement landed: " + ", ".join(
        f"{what} is {'there' if there else 'gone'}" for what, there in state.items()))
elif all(state.values()) and retired:
    bad.append("the file is still here wearing @retired, with its workflow and feature intact — "
               "a tag is a marker for one version mid-transition, not an end state")
if not trace_green:
    bad.append("the check is red: " + " / ".join(proc.stdout.strip().splitlines()[:2]))
for line in bad:
    print("✘", line)
print(f"{len(bad)} problem(s)")
sys.exit(1 if bad else 0)
