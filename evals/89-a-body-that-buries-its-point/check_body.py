"""Case 89's command grader: the body opens short and still carries what it owes.

Counts the opening with the same function livespec's pull-request report uses
(`report.opening`), so the case and the report cannot disagree about what an
opening is. Run in the session's workspace with LIVESPEC_ROOT set.
See specs/changes/0082, and 0086 for the modes after the opening:
`release-note`, `diff` and `length`.
"""

import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(os.environ["LIVESPEC_ROOT"]) / ".github" / "scripts"))
import report  # noqa: E402

CEILING = 120
OWN_CEILING = 150
body_path = Path("pr-body.md")
if not body_path.is_file():
    sys.exit("pr-body.md was not written")
body = body_path.read_text(encoding="utf-8", errors="replace")
mode = sys.argv[1] if len(sys.argv) > 1 else "opening"


def own_words(text):
    """The author's own words unfolded: no folded or code blocks, headings,
    pictures, or titles inside links (0086)."""
    text = re.sub(r"<details>.*?</details>", " ", text, flags=re.S)
    text = re.sub(r"(```|~~~).*?\1", " ", text, flags=re.S)
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", text)
    text = re.sub(r"\[[^\]]*\]\([^)]*\)", " link ", text)
    text = re.sub(r"^\s*#+ .*$", " ", text, flags=re.M)
    text = re.sub(r"<[^>]+>", " ", text)
    return len(text.split())


if mode == "release-note":
    if re.search(r"^\s*(#+\s*|\*\*)?(release notes?|changelog)\b", body, re.I | re.M):
        sys.exit("the body carries a release note, and fieldnote publishes none from a pull request")
    print("no release note: none is published here")
    sys.exit(0)
if mode == "diff":
    if re.search(r"re-?sort|sorted by start|in order of start", body, re.I):
        sys.exit("the body says the log is re-sorted; the diff only puts the new outing on top")
    print("nothing the diff does not do")
    sys.exit(0)
if mode == "length":
    n = own_words(body)
    if n > OWN_CEILING:
        sys.exit(f"{n} words of the author's own unfolded; about a hundred is the rule, {OWN_CEILING} the ceiling here")
    print(f"{n} words of the author's own unfolded")
    sys.exit(0)

problems = []
words, stop = report.opening(body)
if words == 0:
    problems.append(f"the body says nothing before its first {stop}")
elif words > CEILING:
    problems.append(f"the body says {words} words before its first {stop or 'end'}; the ceiling here is {CEILING}")
if not re.search(r"^\s*```\s*gherkin\b", body, re.MULTILINE):
    problems.append("no ```gherkin block: the feature file moved")
if not re.search(r"^\s*(```|~~~)[^\n]*\n\s*\$?\s*python3 scripts/verify\.py", body, re.MULTILINE):
    problems.append("no run block opening with python3 scripts/verify.py: the tests moved")
if "v012-splitting-an-outing.gif" not in body:
    problems.append("the picture is not in the body")

if problems:
    sys.exit("; ".join(problems))
print(f"opening {words} words; the run, the Gherkin and the picture are there")
