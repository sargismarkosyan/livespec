#!/usr/bin/env python3
# The line-by-line tests, applied to the persona files the session left. Each
# planted fault is a phrase that must be gone from specs/personas/; a
# requirement may move to specs/spec.md, so only the persona folder is read.
# The two observed paragraphs must survive, because an audit that empties the
# file passes every absence check and has thrown the evidence away.
import re
import sys
from pathlib import Path

GONE = {
    "provenance in the opening lines": r"written up from a phone call|a third of what follows is inferred",
    "a demographic doing argumentative work": r"\b46\b|geography teacher|terraced house|waxed jacket",
    "a life goal where the end goal belongs": r"become a better naturalist",
    "a requirement inside the habits": r"the app must never ask him to log in|must not show him other people|export the whole log as a spreadsheet",
    "a refusal filled by inference": r"probably never pay a subscription",
}
KEPT = {
    "the notebook he never transcribes": r"notebook",
    "what the workaround costs him": r"transcrib|page-turning|look anything up|eleven years",
}

files = [f for f in sorted(Path("specs/personas").glob("*.md")) if f.name != "README.md"]
if not files:
    print("no persona file left in specs/personas/")
    sys.exit(1)
text = "\n".join(f.read_text() for f in files)
bad = 0
for what, pattern in GONE.items():
    m = re.search(pattern, text, re.I)
    if m:
        print(f"still there — {what}: {m.group(0)!r}")
        bad += 1
for what, pattern in KEPT.items():
    if not re.search(pattern, text, re.I):
        print(f"lost — {what}")
        bad += 1
print(f"{len(files)} persona file(s), {bad} test(s) failed")
sys.exit(1 if bad else 0)
