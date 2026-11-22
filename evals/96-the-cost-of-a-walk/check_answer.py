"""Case 96: the walk's answer is wired. Run in the workspace; exits 0 when every part is there."""
import re
import sys
from pathlib import Path

ci = "\n".join(p.read_text() for p in Path(".github/workflows").glob("*.y*ml")) if Path(".github/workflows").is_dir() else ""
context = "\n".join(Path(n).read_text() for n in ("CLAUDE.md", "AGENTS.md") if Path(n).exists())
problems = []
if "walkcost" not in ci or not re.search(r"--body(?![-\w])", ci):
    problems.append("no CI step passes the pull request's body to the comparison with --body")
if not re.search(r"\bedited\b", ci):
    problems.append("the job does not run again when the pull request's body is edited")
if "## Performance" not in context:
    problems.append("the context file does not name the ## Performance heading a slowdown is answered under")
for line in problems:
    print("✘", line)
sys.exit(1 if problems else 0)
