"""Case 89's command grader: the body opens short and still carries what it owes.

Counts the opening with the same function livespec's pull-request report uses
(`report.opening`), so the case and the report cannot disagree about what an
opening is. Run in the session's workspace with LIVESPEC_ROOT set.
See specs/changes/0082.
"""

import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(os.environ["LIVESPEC_ROOT"]) / ".github" / "scripts"))
import report  # noqa: E402

CEILING = 120
body_path = Path("pr-body.md")
if not body_path.is_file():
    sys.exit("pr-body.md was not written")
body = body_path.read_text(encoding="utf-8", errors="replace")

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
