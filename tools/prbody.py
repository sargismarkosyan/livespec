#!/usr/bin/env python3
"""Hold a pull request's description to the repository's template and to linked references. Standard library only.

    python3 prbody.py --body-file body.md [--template .gitlab/merge_request_templates/Default.md]
                      [--allow "## Changelog" ...]

Copied into a consuming repository by livespec's setup, which writes the
version it copied on the first line, and run on every pull request event,
an edited description included. It fails what a script can decide of
livespec's description guideline (method/repository.md, *And the point,
before the evidence*):

- with a template, a heading or checkbox of it missing, renamed or out of
  order, or a heading added beside it that `--allow` does not name;
- an issue, pull request or incident named by a bare number (`#12`, `!12`)
  or a bare address, rather than a link carrying its title.

A closing line (`Closes #12`), fenced code, inline code, folded `<details>`
blocks and HTML comments are not read for references. The length is
reported and never failed. Exit 0, or 1 with each failure and what it
means. See livespec's method/gates.md, *The description a pull request carries*.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

CLOSING = re.compile(r"^\W*(close[sd]?|fix(e[sd])?|resolve[sd]?|implement(s|ed)?)\b", re.IGNORECASE)
HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
CHECKBOX = re.compile(r"^\s*[-*+]\s+\[[ xX]\]\s+(.+?)\s*$")
LINK = re.compile(r"!?\[[^\]]*\]\([^)]*\)")
BARE_NUMBER = re.compile(r"(?<![\w&/#!\]])[#!]\d+\b")
BARE_ADDRESS = re.compile(r"<?https?://[^\s>)]+>?")

MEANS = {
    "template": "The template is the repository's shape for every description: fill it, every heading and checkbox in its order, and put what it has no field for above its first heading as plain lines.",
    "added": "A heading beside the template's is a second shape for the reviewer to read. Put the text under the template's own field, or above its first heading as a plain line.",
    "reference": "A bare number or address makes the reader open it to learn what it is. Write it as a link with its title, or its id and title in words where it has no address.",
}


def folded_out(text: str) -> str:
    """The description as it is read unfolded: no comments, no folded blocks, no fenced code."""
    text = re.sub(r"<!--[\s\S]*?(-->|$)", " ", text)
    text = re.sub(r"<details\b[\s\S]*?(</details>|$)", " ", text, flags=re.IGNORECASE)
    return re.sub(r"^\s*(```|~~~)[\s\S]*?^\s*\1\s*$", " ", text, flags=re.MULTILINE)


def fields(text: str) -> list[tuple[str, str]]:
    """The headings and checkboxes, in order: ("heading", "## Summary") or ("checkbox", "text")."""
    found: list[tuple[str, str]] = []
    for line in folded_out(text).splitlines():
        heading = HEADING.match(line)
        box = CHECKBOX.match(line)
        if heading:
            found.append(("heading", f"{heading.group(1)} {heading.group(2)}"))
        elif box:
            found.append(("checkbox", box.group(1)))
    return found


def template_failures(body: str, template: str, allowed: list[str]) -> list[str]:
    wanted = fields(template)
    got = [f for f in fields(body) if not (f[0] == "heading" and f[1] in allowed)]
    failures: list[str] = []
    position = 0
    for kind, name in wanted:
        match = next((i for i in range(position, len(got)) if got[i][0] == kind
                      and (got[i][1] == name if kind == "heading" else got[i][1].startswith(name))), None)
        if match is None:
            failures.append(f"template: the {kind} \u201c{name}\u201d is missing, renamed or out of order")
        else:
            position = match + 1
    for kind, name in got:
        if kind == "heading" and not any(w == ("heading", name) for w in wanted):
            failures.append(f"added: the heading \u201c{name}\u201d is not the template's")
    return failures


def reference_failures(body: str) -> list[str]:
    failures: list[str] = []
    for line in folded_out(body).splitlines():
        if CLOSING.match(line):
            continue
        prose = LINK.sub(" ", re.sub(r"`[^`]*`", " ", line))
        for found in BARE_NUMBER.findall(prose) + BARE_ADDRESS.findall(prose):
            failures.append(f"reference: \u201c{found.strip('<>')}\u201d is bare")
    return failures


def own_words(body: str, template: str) -> int:
    """The author's words, unfolded: no template field, no link or its title, no code."""
    lines = [line for line in folded_out(body).splitlines()
             if not HEADING.match(line) and not CHECKBOX.match(line) and line.strip() not in template]
    text = LINK.sub(" ", "\n".join(lines))
    text = re.sub(r"`[^`]*`|https?://\S+", " ", text)
    return len([w for w in text.split() if re.search(r"\w", w)])


def check(body: str, template: str = "", allowed: list[str] | None = None) -> tuple[list[str], int]:
    """The failures, each with what it means, and the author's word count."""
    failures = (template_failures(body, template, allowed or []) if template.strip() else []) + reference_failures(body)
    return failures, own_words(body, template)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--body-file", required=True, help="the description; - reads stdin")
    parser.add_argument("--template", help="the template the platform fills a new pull request with")
    parser.add_argument("--allow", action="append", default=[], help="a heading the repository's rules add, e.g. '## Changelog'")
    args = parser.parse_args(argv)
    body = sys.stdin.read() if args.body_file == "-" else Path(args.body_file).read_text(encoding="utf-8")
    template = Path(args.template).read_text(encoding="utf-8") if args.template else ""
    failures, words = check(body, template, args.allow)
    for failure in failures:
        print(f"\u2718 {failure}\n  {MEANS[failure.split(':', 1)[0]]}")
    print(f"{'✘' if failures else '✔'} pull request description: {len(failures)} failure(s); "
          f"{words} words of the author's own, unfolded — about a hundred is the aim, and it is never failed")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
