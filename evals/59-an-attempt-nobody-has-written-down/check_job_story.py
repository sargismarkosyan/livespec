#!/usr/bin/env python3
# The shape §3 and §4 ask of a workflow file, read off the one this sitting
# wrote: a job story that starts at the situation, an end state somebody can
# stand at, a failure section, a last example that returns, and examples that
# say what happens rather than which control does it.
import re
import subprocess
import sys
from pathlib import Path

known = {"writing-a-sighting"}
new = []
for f in sorted(Path("specs/workflows").glob("*.feature")):
    head = f.read_text().splitlines()[0]
    wid = re.search(r"@workflow:([\w-]+)", head)
    if wid and wid.group(1) not in known:
        new.append(f)
if not new:
    print("no new workflow file in specs/workflows/")
    sys.exit(1)

problems = []
for f in new:
    text = f.read_text()
    if not re.search(r"\bWhen\b[^\n]*\n\s*I want\b", text) and not re.search(r"\bWhen\b[^.\n]*,\s*I want\b", text):
        problems.append(f"{f.name}: no job story — the narrative should read When <situation>, I want <motivation>, so <outcome>")
    if re.search(r"^\s*As an?\s", text, re.M):
        problems.append(f"{f.name}: the narrative is role-first (As a …), which starts from who somebody is rather than the situation")
    if not re.search(r"ends? when", text, re.I):
        problems.append(f"{f.name}: no end state — nothing saying when the attempt is done")
    if not re.search(r"where it breaks|goes wrong|fails?\b", text, re.I):
        problems.append(f"{f.name}: no failure section; the examples are a demo without one")
    examples = re.findall(r"^\s*Example:.*(?:\n(?!\s*Example:).*)*", text, re.M)
    if len(examples) < 2:
        problems.append(f"{f.name}: fewer than two examples")
    elif not re.search(r"come back|comes back|as left|exactly as|reopen", examples[-1], re.I):
        problems.append(f"{f.name}: the last example does not come back to the product and find it as left")
    imperative = re.findall(r"\b(click|clicks|button|buttons|tap|taps|drag|checkbox|dropdown|menu|toolbar|scrolls?)\b", text, re.I)
    if imperative:
        problems.append(f"{f.name}: imperative interface words in the examples: {sorted(set(w.lower() for w in imperative))}")

proc = subprocess.run([sys.executable, "scripts/trace.py"], capture_output=True, text=True)
if proc.returncode != 0:
    problems.append("the check is red: " + " / ".join(proc.stdout.strip().splitlines()[:2]))

print("new workflow file(s):", ", ".join(f.name for f in new))
for p in problems:
    print("✘", p)
print(f"{len(problems)} problem(s)")
sys.exit(1 if problems else 0)
