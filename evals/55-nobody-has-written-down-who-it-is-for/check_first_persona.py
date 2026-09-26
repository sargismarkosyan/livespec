#!/usr/bin/env python3
# The three things this sitting owes the tree: a persona where there was none,
# a green check, and a ledger row that stopped saying no personas exist. The
# rows were honest when setup ran and are wrong the moment this lands, and the
# skill says the row is this change's to move.
import re
import subprocess
import sys
from pathlib import Path

bad = 0
files = [f for f in sorted(Path("specs/personas").glob("*.md")) if f.name != "README.md"]
if not files:
    print("no persona file in specs/personas/")
    bad += 1
else:
    print(f"persona file(s): {[f.name for f in files]}")

proc = subprocess.run([sys.executable, "scripts/trace.py"], capture_output=True, text=True)
if proc.returncode != 0:
    print("the traceability check is red:", " / ".join(proc.stdout.strip().splitlines()[:3]))
    bad += 1

bindings = Path("specs/setup/README.md")
text = bindings.read_text() if bindings.exists() else ""
stale = [line.strip() for line in text.splitlines()
         if "persona" in line.lower() and re.search(r"not applicable", line, re.I)]
if stale:
    for line in stale:
        print("ledger row still reads not applicable:", line[:120])
    bad += 1

print(f"{bad} thing(s) the sitting still owes")
sys.exit(1 if bad else 0)
