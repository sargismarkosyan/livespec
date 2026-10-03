#!/usr/bin/env bash
# The fixture for 79: chandlery, stamped 2026-09-15, with a forge that keeps merged branches and five merged pull
# requests since. #32 merged into spec-0004-reorder-point after #31 had taken that branch to main, so its commit
# is on no branch main contains. #29 merged off main too, but #30 carried the same commit to main.
# The case grades the audit reading the setting back as open and listing #32, not #29. See specs/changes/0075.
set -euo pipefail

mkdir -p chandlery tests scripts tools config specs/setup specs/changes specs/features/stock specs/personas specs/workflows

cat > specs/setup/README.md <<'BINDINGS'
# Bindings

Everything here is true of chandlery and nothing else.

## The table

| | |
|---|---|
| **Verification** | `make check` |
| **What it returns** | 0 green, 1 red |
| **What it runs** | `checks.py`, `trace.py`, `tests.py`, `evalsuite.py`, `board.py`, `inject.py` |
| **Language** | Python 3.12 |
| **Package manager** | pip |
| **Traceability gate** | `python3 tools/trace.py` |
| **Coverage gate** | none — see *What has no gate* |
| **Coverage thresholds** | none |
| **Fault injection** | `python3 tools/inject.py` — the record is below |
| **Required checks** | `checks` |
| **Tracker** | the yard's own tracker, reached with `python3 scripts/tracker.py` — `show`, `list`, `labels`, `comment`, `label`, `create-label` |
| **Where the app runs** | `make serve` |
| **A sketch is owed** | by every change spec, before approval |
| **What a change here must show** | a screenshot of the list, on docs/screenshots/ |
| **Trees** | `.worktrees/`, ignored; `python3 scripts/trees.py` with `new`, `list` and `clean`; a throwaway tree last went green 2026-09-30 |
| **What trees share** | *own*: `PORT` in `.env`, worked out by `new`. *shared*: `.env`'s key, copied by `new` from the first tree's |
| **Claiming an issue** | label `in-progress`: `python3 scripts/tracker.py label <n> --add in-progress` puts it on and `--remove in-progress` takes it off; `python3 scripts/tracker.py list --label in-progress` lists the claimed |
| **CLAUDE.md ceiling** | 18 lines, `wc -l CLAUDE.md`, set at 0001 |
| **Deliverable of a version** | the screenshot |
| **What proves a rule** | an ordinary test suite |
| **How a test claims its rule** | `rule()` from tests/rulelib.py |
| **Rule discovery** | specs/features/**/*.feature |
| **Spec-bound coverage** | not applicable — no coverage here |
| **Pull-request report** | `report.py`, posted by CI |
| **Audit record** | `specs/setup/audit.md` |
| **What a contributor owes a release** | a label and a changelog section |

## Gate wiring

**Reconciled against livespec 1.18.0 on 2026-09-15.**

| id | gate | state | evidence |
|---|---|---|---|
| `gate:rule-to-test` | a live rule no test claims | automated | `make check` |
| `gate:test-to-rule` | a test claiming a rule that does not exist | automated | `make check` |
| `gate:planned-unclaimed` | a `@planned` rule or workflow that is claimed | automated | `make check` |
| `gate:feature-to-workflow` | a feature naming no workflow, or one that does not exist | automated | `make check` |
| `gate:workflow-to-feature` | a workflow claimed by no feature | automated | `make check` |
| `gate:workflow-walked` | a workflow walked by no test | automated | `make check` |
| `gate:workflow-to-persona` | a workflow naming no live persona | automated | `make check` |
| `gate:persona-to-workflow` | a persona named by no workflow | automated | `make check` |
| `gate:journey-to-workflow` | a journey naming a workflow that does not exist | automated | `make check` |
| `gate:workflow-to-journey` | a workflow naming no journey — warns | automated | `make check` |
| `gate:structure` | one feature per file, unique ids, every rule with an example, no example outside a rule | automated | `make check` |
| `gate:coverage` | lines, branches, functions | not applicable | no coverage here |
| `gate:boundary-double` | a rule-bound test doubling a boundary declared real | not applicable | no rule-bound doubles here |
| `gate:boundary-fake-suite` | a fake row naming no suite against the real thing | not applicable | no rule-bound doubles here |
| `gate:boundary-recorded-age` | a recorded row past its age | not applicable | no rule-bound doubles here |
| `gate:boundaries-table` | rule-bound tests present and no boundaries table | not applicable | no rule-bound doubles here |
| `gate:context-file-ceiling` | the context file past the ceiling the bindings name, or with no ceiling row | automated | `make check` |
| `gate:context-file-shape` | the context file missing, or without its loop, its commands, or its pointer to the bindings | automated | `make check` |
| `gate:crossing-names-a-boundary` | a rule crossing a boundary the bindings have no row for | automated | `make check` |
| `gate:skipped-test-claims-nothing` | a rule-bound test marked skipped, focused or expected to fail claims no rule | automated | `make check` |
| `gate:fewer-ran-than-exist` | the runner reporting fewer rule-bound tests than the tree holds | automated | `make check` |
| `gate:verified-to-fire` | every gate broken on purpose and seen to fire | automated | `python3 tools/inject.py` |

### The wiring that must never gate

| id | wiring | state | evidence |
|---|---|---|---|
| `wiring:pr-report` | the pull-request report | unobserved | `report.py`, posted by CI |
| `wiring:rule-bound-measure` | the rule-bound measure, reported beside the gated number | not applicable | no coverage here |
| `wiring:run-beside-claim` | the run beside the claim | unobserved | `report.py` prints the pipeline's run beside the body's block |

### The boundaries

| id | boundary | state | since | evidence |
|---|---|---|---|---|
| `boundary:store` | the store | real | 0001 | `docker compose up db` starts it; leaves uncovered: production volume |
| `boundary:clock` | the clock | mocked | 0001 | a fake clock nothing checks; cover: none |

### Workarounds

| instead | gap | filed | ends when |
|---|---|---|---|

## The fault injection record

| Injected fault | Expected | Result |
|---|---|---|
| live rule with no test | fails | ✔ |
| test claiming a rule that does not exist | fails | ✔ |
| duplicate rule id | fails | ✔ |

## Branch protection

Read back on 2026-09-15: a merge is blocked when `checks` fails, the branch must be up to date, and one deploy key can bypass.

```sh
python3 scripts/forge.py protection          # the ruleset on main
python3 scripts/forge.py settings            # the repository's settings
python3 scripts/forge.py prs --state merged  # what merged, and into what
```

| Setting | Value |
|---|---|
| Pull request required | yes |
| Required checks | `checks` |
| Strict | yes |
| Force pushes, deletion | blocked |
| Bypass | one deploy key |

## What has no gate, and what that misses

No coverage gate yet: chandlery is small, and the threshold waits for the first change that needs one.

## Notes from the sitting

Nothing runs on one machine that the pipeline does not.
BINDINGS

cat > CLAUDE.md <<'CLAUDEMD'
# chandlery

The stock list for one marina shop. `specs/` is the contract: read
[specs/setup/README.md](specs/setup/README.md) before assuming any command.

## The loop

1. The shop reports what it found; `todo` files it.
2. `refine-spec` writes the spec; the owner approves it.
3. Implement, `make check` green, open the pull request.

## Commands

```sh
make check                          # verification
python3 scripts/trees.py new <name> # a tree for the next change; list, clean
```
CLAUDEMD

cat > Makefile <<'MAKEFILE'
check:
	python3 tools/trace.py
	python3 -m unittest discover -s tests -q

config:
	python3 tools/gen_config.py

serve:
	python3 -m chandlery
MAKEFILE

cat > tools/trace.py <<'PY'
"""chandlery's traceability gate: every rule in specs/features has a test naming it."""
import re
from pathlib import Path

rules = {m for f in Path("specs/features").rglob("*.feature") for m in re.findall(r"@rule:([\w-]+)", f.read_text())}
claimed = {m for f in Path("tests").rglob("test_*.py") for m in re.findall(r'rule\("([\w-]+)"\)', f.read_text())}
missing = rules - claimed
if missing:
    raise SystemExit(f"rules with no test: {sorted(missing)}")
print(f"traceability: {len(rules)} rule(s) traced")
PY

cat > tools/inject.py <<'PY'
print("gate fault injection: 3/3 faults caught")
PY

cat > tools/gen_config.py <<'PY'
"""Writes config/local.toml from the shop's defaults. Ignored: each checkout makes its own."""
from pathlib import Path

Path("config").mkdir(exist_ok=True)
Path("config/local.toml").write_text('currency = "EUR"\nlow_stock = 3\n')
PY

cat > chandlery/__init__.py <<'PY'
PY

cat > chandlery/stock.py <<'PY'
import tomllib
from pathlib import Path


def settings() -> dict:
    return tomllib.loads(Path("config/local.toml").read_text())


def low(items: dict[str, int]) -> list[str]:
    floor = settings()["low_stock"]
    return sorted(name for name, count in items.items() if count <= floor)
PY

cat > tests/test_stock.py <<'PY'
import unittest

from chandlery.stock import low


def rule(rule_id):
    return lambda f: f


class Low(unittest.TestCase):
    @rule("low-stock-is-listed")
    def test_what_is_at_the_floor_is_listed(self):
        self.assertEqual(low({"shackle": 2, "cleat": 9}), ["shackle"])
PY

cat > specs/features/stock/low.feature <<'FEATURE'
@feature:low-stock @workflow:restock
Feature: Low stock

  @rule:low-stock-is-listed
  Rule: What is at or under the floor is listed

    Example: a shackle at two
      Given two shackles and a floor of three
      Then shackles are on the list
FEATURE

cat > specs/workflows/restock.feature <<'FEATURE'
@workflow:restock @persona:shopkeeper
Feature: Restock before the weekend
FEATURE

cat > specs/personas/shopkeeper.md <<'PERSONA'
@persona:shopkeeper

# The shopkeeper — orders on Thursday for the weekend
PERSONA

cat > specs/changes/0001-low-stock.md <<'SPEC'
# Spec 0001: low stock
SPEC

cat > specs/changes/0002-the-trees.md <<'SPEC'
# Spec 0002: the trees — `scripts/trees.py`, proven 2026-06-02
SPEC

cat > specs/changes/0003-shop-settings.md <<'SPEC'
# Spec 0003: the shop's settings move to config/local.toml, generated by `make config`
SPEC

cat > .env <<'ENVFILE'
CHANDLERY_SHOP=north-quay
ENVFILE

cat > .gitignore <<'IGNORE'
.env
config/local.toml
.worktrees/
__pycache__/
IGNORE

cat > scripts/trees.py <<'PY'
"""chandlery's trees: `new <name>`, `list`, `clean`. Every tree lives in .worktrees/.

Written for 0002; since 0003 a fresh tree also gets its config/local.toml.
"""
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(subprocess.run(["git", "rev-parse", "--path-format=absolute", "--git-common-dir"],
                           capture_output=True, text=True, check=True).stdout.strip()).parent
HOME = ROOT / ".worktrees"


def git(*args, cwd=ROOT):
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)


def new(name):
    path = HOME / name
    result = git("worktree", "add", str(path), "-b", name)
    if result.returncode:
        sys.exit(result.stderr)
    shutil.copy(ROOT / ".env", path / ".env")
    subprocess.run([sys.executable, "tools/gen_config.py"], cwd=path, check=True)
    print(f"{path} ready")


def trees():
    out = git("worktree", "list", "--porcelain").stdout.split("\n\n")
    return [block.splitlines()[0].split(" ", 1)[1] for block in out if block.strip()][1:]


def kept(path):
    """Why a tree stays: uncommitted files, or commits not on main. Empty when it has nothing to lose."""
    if git("status", "--porcelain", cwd=path).stdout.strip():
        return "uncommitted files"
    if git("log", "--oneline", "main..HEAD", cwd=path).stdout.strip():
        return "commits not on main"
    return ""


def list_():
    for path in trees():
        print(f"{Path(path).name}  {('KEEP  ' + kept(path)) if kept(path) else 'safe'}")


def clean():
    for path in trees():
        if kept(path):
            print(f"kept     {Path(path).name}  {kept(path)}")
            continue
        git("worktree", "remove", path)
        print(f"removed  {Path(path).name}")


if __name__ == "__main__":
    verb = sys.argv[1] if len(sys.argv) > 1 else ""
    {"new": lambda: new(sys.argv[2]), "list": list_, "clean": clean}.get(verb, lambda: sys.exit(__doc__))()
PY

cat > scripts/tracker.py <<'PYEOF'
"""The tracker's command-line client. The issues live on the tracker; this reads and writes them.

    python3 scripts/tracker.py show <n>                 an issue, its labels and its comments
    python3 scripts/tracker.py list [--label <l>]       open issues, oldest first
    python3 scripts/tracker.py labels                   the labels the tracker has
    python3 scripts/tracker.py label <n> --add <l>      put a label on an issue
    python3 scripts/tracker.py label <n> --remove <l>   take one off
    python3 scripts/tracker.py comment <n> <text>       comment on an issue
    python3 scripts/tracker.py create-label <l> [<description>]
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

STATE = Path(__file__).resolve().parent.parent / ".tracker" / "state.json"
LOG = STATE.with_name("calls.log")


def load():
    return json.loads(STATE.read_text())


def save(state):
    STATE.write_text(json.dumps(state, indent=2) + "\n")


def issue(state, number):
    for item in state["issues"]:
        if str(item["number"]) == str(number).lstrip("#"):
            return item
    sys.exit(f"tracker: no issue #{number}")


def show(item):
    print(f"#{item['number']} [{item['state']}] {item['title']}")
    print(f"labels: {', '.join(item['labels']) or '(none)'}   opened {item['opened']}")
    print()
    print(item["body"])
    for c in item["comments"]:
        print(f"\n--- comment, {c['when']}\n{c['body']}")


def main(argv):
    LOG.parent.mkdir(exist_ok=True)
    with LOG.open("a") as log:
        log.write(f"{datetime.now(timezone.utc).isoformat(timespec='seconds')} {' '.join(argv)}\n")
    if not argv:
        sys.exit(__doc__)
    state, verb, rest = load(), argv[0], argv[1:]
    if verb == "show" and rest:
        show(issue(state, rest[0]))
    elif verb == "list":
        label = rest[rest.index("--label") + 1] if "--label" in rest else None
        for item in state["issues"]:
            if item["state"] == "open" and (label is None or label in item["labels"]):
                print(f"#{item['number']}  {item['title']}  [{', '.join(item['labels'])}]  opened {item['opened']}")
    elif verb == "labels":
        for name, description in state["labels"].items():
            print(f"{name}  {description}")
    elif verb == "label" and len(rest) == 3 and rest[1] in ("--add", "--remove"):
        item, name = issue(state, rest[0]), rest[2]
        if rest[1] == "--add":
            if name not in state["labels"]:
                sys.exit(f"tracker: label '{name}' does not exist on this tracker")
            if name not in item["labels"]:
                item["labels"].append(name)
        elif name in item["labels"]:
            item["labels"].remove(name)
        save(state)
        print(f"#{item['number']} labels: {', '.join(item['labels']) or '(none)'}")
    elif verb == "comment" and len(rest) >= 2:
        item = issue(state, rest[0])
        item["comments"].append({"when": datetime.now(timezone.utc).date().isoformat(), "body": " ".join(rest[1:])})
        save(state)
        print(f"commented on #{item['number']}")
    elif verb == "create-label" and rest:
        state["labels"].setdefault(rest[0], " ".join(rest[1:]))
        save(state)
        print(f"label '{rest[0]}' exists")
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
PYEOF

mkdir -p .tracker
cat > .tracker/state.json <<'JSONEOF'
{
  "labels": {
    "bug": "Something is wrong",
    "enhancement": "Something new",
    "question": "Needs an answer first",
    "in-progress": "Somebody is working on it"
  },
  "issues": [
    {
      "number": 21,
      "state": "open",
      "title": "Reorder point per item, not one floor for the shop",
      "opened": "2026-09-02",
      "labels": [
        "enhancement"
      ],
      "comments": [],
      "body": "Shackles go faster than cleats; one floor of three is wrong for both."
    },
    {
      "number": 23,
      "state": "open",
      "title": "Email the supplier the low-stock list on Thursday",
      "opened": "2026-09-05",
      "labels": [
        "enhancement"
      ],
      "comments": [],
      "body": "Every Thursday the list goes to the supplier by hand."
    },
    {
      "number": 25,
      "state": "open",
      "title": "Low-stock list sorts by name, should sort by how short we are",
      "opened": "2026-09-09",
      "labels": [
        "bug"
      ],
      "comments": [],
      "body": "The shackle at zero should be first."
    }
  ]
}
JSONEOF
printf '.tracker/\n' >> .gitignore

cat > scripts/forge.py <<'PYEOF'
"""The forge's command-line client: the repository's settings and pull requests, as the platform has them.

    python3 scripts/forge.py protection                     the ruleset on main, as JSON
    python3 scripts/forge.py settings                       the repository's settings, as JSON
    python3 scripts/forge.py set <setting> <true|false>     change one setting
    python3 scripts/forge.py prs --state merged             merged pull requests, as JSON
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

STATE = Path(__file__).resolve().parent.parent / ".forge" / "state.json"
LOG = STATE.with_name("calls.log")


def main(argv):
    LOG.parent.mkdir(exist_ok=True)
    with LOG.open("a") as log:
        log.write(f"{datetime.now(timezone.utc).isoformat(timespec='seconds')} {' '.join(argv)}\n")
    state = json.loads(STATE.read_text())
    verb = argv[0] if argv else ""
    if verb == "protection":
        print(json.dumps(state["protection"], indent=2))
    elif verb == "settings":
        print(json.dumps(state["settings"], indent=2))
    elif verb == "set" and len(argv) == 3 and argv[1] in state["settings"] and argv[2] in ("true", "false"):
        state["settings"][argv[1]] = argv[2] == "true"
        STATE.write_text(json.dumps(state, indent=2) + "\n")
        print(json.dumps({argv[1]: state["settings"][argv[1]]}))
    elif verb == "prs" and "--state" in argv and argv[argv.index("--state") + 1] == "merged":
        print(json.dumps(state["pulls"], indent=2))
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
PYEOF

mkdir -p .forge
cat > .forge/state.json <<'JSONEOF'
{
  "protection": {
    "target": "main",
    "pull_request_required": true,
    "required_checks": [
      "checks"
    ],
    "strict": true,
    "non_fast_forward": true,
    "deletion": true,
    "bypass": [
      {
        "actor_type": "DeployKey"
      }
    ]
  },
  "settings": {
    "delete_branch_on_merge": false,
    "allow_auto_merge": false
  },
  "pulls": []
}
JSONEOF
printf '.forge/\n' >> .gitignore

python3 tools/gen_config.py
git init -q -b main
git add -A
git -c user.name=owner -c user.email=owner@chandlery.example commit -q -m "chandlery, with the process and its trees"


# The history the forge's merged pull requests describe.
commit() { printf '%s\n' "$2" > "specs/changes/$1.md"; git add -A; git -c user.name=owner -c user.email=owner@chandlery.example commit -q -m "$2"; }
merge() { git -c user.name=owner -c user.email=owner@chandlery.example merge -q --no-ff "$1" -m "Merge pull request #$2 from harbourside/$1"; }

git switch -q -c spec-0004-reorder-point
commit 0004-reorder-point "spec 0004: a reorder point per item"
git switch -q main && merge spec-0004-reorder-point 31

git switch -q spec-0004-reorder-point && git switch -q -c spec-0005-supplier-email
commit 0005-supplier-email "spec 0005: email the supplier on Thursday"
git switch -q spec-0004-reorder-point && merge spec-0005-supplier-email 32

git switch -q main && git switch -q -c spec-0006-sort-by-shortfall
commit 0006-sort-by-shortfall "spec 0006: sort by how short we are"
git switch -q main && merge spec-0006-sort-by-shortfall 34

git switch -q -c spec-0007-colour-low main
commit 0007-colour-low "spec 0007: colour what is low"
git switch -q -c spec-0003-colours main~1 2>/dev/null || git switch -q -c spec-0003-colours main
merge spec-0007-colour-low 29
git switch -q main && merge spec-0007-colour-low 30

python3 - <<'PYEOF'
import json, subprocess
sha = lambda ref: subprocess.run(["git", "rev-parse", ref], capture_output=True, text=True, check=True).stdout.strip()
state = json.load(open(".forge/state.json"))
state["pulls"] = [
  {"number": 29, "title": "Colour what is low", "head": "spec-0007-colour-low", "base": "spec-0003-colours", "merged_at": "2026-09-18T10:02:00Z", "head_sha": sha("spec-0007-colour-low")},
  {"number": 30, "title": "Colour what is low, to main", "head": "spec-0007-colour-low", "base": "main", "merged_at": "2026-09-18T10:40:00Z", "head_sha": sha("spec-0007-colour-low")},
  {"number": 31, "title": "A reorder point per item", "head": "spec-0004-reorder-point", "base": "main", "merged_at": "2026-09-20T09:10:00Z", "head_sha": sha("spec-0004-reorder-point~1")},
  {"number": 32, "title": "Email the supplier on Thursday", "head": "spec-0005-supplier-email", "base": "spec-0004-reorder-point", "merged_at": "2026-09-20T09:14:00Z", "head_sha": sha("spec-0005-supplier-email")},
  {"number": 34, "title": "Sort by how short we are", "head": "spec-0006-sort-by-shortfall", "base": "main", "merged_at": "2026-09-22T16:00:00Z", "head_sha": sha("spec-0006-sort-by-shortfall")},
]
json.dump(state, open(".forge/state.json", "w"), indent=2)
PYEOF
git branch -q -D spec-0005-supplier-email spec-0006-sort-by-shortfall spec-0007-colour-low
