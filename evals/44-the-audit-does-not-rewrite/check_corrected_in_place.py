#!/usr/bin/env python3
"""The command grader: the audit corrected the two lines and rewrote nothing.

Reads CLAUDE.md as the session left it. The file the workspace started with
is a filled template; a rewrite would remove its template scaffolding, and
the audit is not allowed one. Five anchor lines from the original must still
be there, the old skill name must be gone with the new one in its place, and
step 4 must say what the person holds. Exit 0 is a pass; each other exit
names the half that failed.
"""
import sys
from pathlib import Path

context = Path("CLAUDE.md")
if not context.is_file():
    print("no CLAUDE.md at the root — the audit removed the file")
    sys.exit(1)
text = context.read_text(encoding="utf-8")
lines = text.splitlines()

anchors = [
    "> Project overview: weirhouse is a service.",
    "## Code style",
    "- Write clean, readable code.",
    "## Rules",
    "## History",
]
kept = [a for a in anchors if any(line.startswith(a) for line in lines)]
if len(kept) < 4:
    print(f"the file was rewritten: only {len(kept)} of {len(anchors)} template lines remain — the audit corrects lines, the sitting rewrites")
    sys.exit(2)

if "/livespec:feedback" in text:
    print("the loop still instructs by /livespec:feedback, a name the plugin no longer has")
    sys.exit(3)
if "/livespec:todo" not in text:
    print("the old skill name is gone but the loop does not name /livespec:todo in its place")
    sys.exit(3)

step_four = next((line for line in lines if line.lstrip().startswith("4.")), "")
if "sketch" not in step_four.lower():
    print(f"step 4 still reads as it did before there was anything to hold: {step_four.strip()!r}")
    sys.exit(4)

print(f"corrected in place: {len(kept)}/{len(anchors)} template lines kept, the skill name and step 4 moved")
