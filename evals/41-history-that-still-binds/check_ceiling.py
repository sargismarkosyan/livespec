#!/usr/bin/env python3
"""The command grader for the ceiling row: is the number the file's own size?

Run in the session's workspace after it ends. Reads the bindings the session
wrote for a table row whose label names the ceiling, takes the first number in
it, and compares it to CLAUDE.md as it stands at the end — in lines, characters
or bytes, whichever unit the row chose. Exit 0 is a pass; every other exit says
which half was missing.
"""
import re
import sys
from pathlib import Path

bindings = Path("specs/setup/README.md")
context = Path("CLAUDE.md")
if not bindings.exists():
    print("no specs/setup/README.md — the sitting wrote no bindings")
    sys.exit(1)
if not context.exists():
    print("no CLAUDE.md at the root at the end of the sitting")
    sys.exit(1)

rows = [line for line in bindings.read_text(encoding="utf-8").splitlines() if line.startswith("|") and "ceiling" in line.lower()]
if not rows:
    print("the bindings carry no table row naming the ceiling")
    sys.exit(2)
row = rows[0]
numbers = [int(n.replace(",", "")) for n in re.findall(r"\b\d[\d,]*\b", row)]
if not numbers:
    print(f"the ceiling row carries no number: {row}")
    sys.exit(3)

text = context.read_text(encoding="utf-8")
sizes = {"lines": len(text.splitlines()), "characters": len(text), "bytes": len(text.encode("utf-8"))}
written = numbers[0]
if written in sizes.values():
    unit = next(k for k, v in sizes.items() if v == written)
    print(f"ceiling {written} is the file's own size in {unit}")
    sys.exit(0)
print(f"ceiling row says {written}; the file is {sizes['lines']} lines, {sizes['characters']} characters, {sizes['bytes']} bytes")
sys.exit(4)
