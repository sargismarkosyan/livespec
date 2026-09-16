#!/usr/bin/env python3
"""The command grader: does the CLAUDE.md the sitting left pass the gate it wired?

Run in the session's workspace after it ends. Applies the five checks the
method's gate reads — at the root, within the ceiling the bindings name, a
numbered loop of one to eight steps, a fenced block, a link to the bindings
that resolves — to what is on disk, independently of whatever script the
session wrote. Exit 0 is a pass; otherwise it prints each check that failed.
"""
import re
import sys
from pathlib import Path

context = Path("CLAUDE.md")
bindings = Path("specs/setup/README.md")
problems: list[str] = []

if not context.is_file():
    print("no CLAUDE.md at the root")
    sys.exit(1)
lines = context.read_text(encoding="utf-8").splitlines()

ceiling = None
if bindings.is_file():
    for line in bindings.read_text(encoding="utf-8").splitlines():
        if line.startswith("|") and "ceiling" in line.lower():
            match = re.search(r"\d[\d,]*", line.split("|", 2)[2] if line.count("|") >= 3 else line)
            if match:
                ceiling = int(match.group(0).replace(",", ""))
                break
if ceiling is None:
    problems.append("the bindings name no ceiling for CLAUDE.md")
elif len(lines) > ceiling:
    problems.append(f"CLAUDE.md is {len(lines)} lines against a ceiling of {ceiling}")

longest = run = expected = 0
fenced = False
for raw in lines:
    if re.match(r"^\s*(```|~~~)", raw):
        fenced = not fenced
        continue
    if fenced:
        continue
    match = re.match(r"^\s*(\d+)\.\s", raw)
    if match and int(match.group(1)) == 1:
        run, expected = 1, 2
    elif match and int(match.group(1)) == expected:
        run, expected = run + 1, expected + 1
    elif match or (raw.strip() and not raw.startswith((" ", "\t"))):
        run, expected = 0, 0
    longest = max(longest, run)
if longest == 0:
    problems.append("no numbered list — the loop is missing")
elif longest > 8:
    problems.append(f"a numbered list of {longest} steps — the loop is at most eight")

if sum(1 for raw in lines if re.match(r"^\s*(```|~~~)", raw)) < 2:
    problems.append("no fenced block — the commands are missing")

targets = re.findall(r"\]\((?!https?:|#|mailto:)([^)\s]+)\)", "\n".join(lines))
if not any((context.parent / t.split("#", 1)[0]).resolve() == bindings.resolve() for t in targets):
    problems.append("no link to specs/setup/README.md, the bindings")

if problems:
    print("\n".join(problems))
    sys.exit(2)
print(f"CLAUDE.md passes: {len(lines)} lines within {ceiling}, a loop of {longest}, a fenced block, a link to the bindings")
