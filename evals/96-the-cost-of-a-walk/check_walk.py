"""Case 96: what the sitting left on disk. Run in the workspace; exits 0 when every part is there."""
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(os.environ["LIVESPEC_ROOT"]) / "tools"))
import walkcost  # noqa: E402

skip = {".git", "node_modules", ".worktrees"}
files = [p for p in Path(".").rglob("*") if p.is_file() and not skip & set(p.parts)]
problems = []

copies = [p for p in files if p.suffix == ".py" and p.read_text(errors="ignore").startswith("# livespec walkcost")
          and "def judge_time" in p.read_text(errors="ignore")]
if not copies:
    problems.append("no copy of walkcost.py whose first line is '# livespec walkcost <version>'")

policies = []
for p in files:
    if p.suffix == ".json" and p.name != "package.json":
        try:
            if "measures" in json.loads(p.read_text()):
                policies.append(p)
        except ValueError:
            pass
if not policies:
    problems.append("no policy file naming its measures")
for p in policies:
    try:
        walkcost.load_policy(str(p))
    except walkcost.Refused as exc:
        problems.append(f"the comparison refuses {p}: {exc}")

ci = "\n".join(p.read_text() for p in Path(".github/workflows").glob("*.y*ml")) if Path(".github/workflows").is_dir() else ""
name = copies[0].name if copies else "walkcost"
if name not in ci or "--gate" not in ci:
    problems.append(f"no CI step runs {name} with --gate")
if "worktree" not in ci:
    problems.append("no CI step checks the base out into a second worktree")

ledger = Path("specs/setup/README.md").read_text()
for rid in ("wiring:workflow-cost", "gate:workflow-budget"):
    row = next((l for l in ledger.splitlines() if l.startswith(f"| `{rid}`")), None)
    if row is None:
        problems.append(f"no ledger row for {rid}")
    elif not re.search(r"\|\s*\**(automated|unobserved|deferred|not applicable)\**\s*\|", row):
        problems.append(f"{rid}'s row is in none of the four states")

for line in problems:
    print("✘", line)
sys.exit(1 if problems else 0)
