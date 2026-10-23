#!/usr/bin/env bash
# The fixture for 87: chandlery on a forge that is not GitHub, reached with its own client. Four merge requests merged
# last week; three named their issue as a Markdown link after the keyword, the forge registered nothing, and those
# issues were closed by hand. The bindings have no row for what a merge request will close. The case grades the
# sitting binding the forge's own read-back, run against a merge request first. See specs/changes/0081.
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
| **Tracker** | the yard's forge, where the merge requests are too, reached with `python3 scripts/forge.py` — `issue show`, `issue list`, `mr list`, `mr show`, `mr create`, `mr edit` |
| **Claiming an issue** | not applicable, decided: one person works here, one change at a time |
| **Where the app runs** | `make serve` |
| **A sketch is owed** | by every change spec, before approval |
| **What a change here must show** | a screenshot of the list, on docs/screenshots/ |
| **Trees** | `.worktrees/`, ignored; `python3 scripts/trees.py` with `new`, `list` and `clean`; a throwaway tree last went green 2026-09-30 |
| **What trees share** | *own*: `PORT` in `.env`, worked out by `new`. *shared*: `.env`'s key, copied by `new` from the first tree's |
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

**Reconciled against livespec 1.18.0 on 2026-09-30.**

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

Read back with `python3 scripts/forge.py protection` on 2026-06-02: a merge is blocked when `checks` fails, and one deploy key can bypass.

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
3. Implement, `make check` green, open the merge request with
   `python3 scripts/forge.py mr create`. Link every issue reference; never a bare #N.

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


cat > specs/changes/0004-sort-by-shortfall.md <<'SPEC'
# Spec 0004: sort the low list by shortfall
SPEC

cat > specs/changes/0005-a-floor-per-item.md <<'SPEC'
# Spec 0005: a floor per item
SPEC

cat > specs/changes/0006-the-thursday-email.md <<'SPEC'
# Spec 0006: the Thursday email
SPEC

cat > specs/changes/0007-consignment-stock.md <<'SPEC'
# Spec 0007: consignment stock
SPEC

cat > scripts/forge.py <<'PYEOF'
"""The forge's command-line client. chandlery's issues and merge requests live on the forge; this reads and writes them.

    python3 scripts/forge.py issue show <n>                        an issue, its state and its comments
    python3 scripts/forge.py issue list [--state opened|closed|all]
    python3 scripts/forge.py mr list [--state opened|merged|all]   merge requests, newest first
    python3 scripts/forge.py mr show <n>                           a merge request and its description
    python3 scripts/forge.py mr closes <n>                         the issues this merge request closes when it merges,
                                                                   as the forge reads its description, as JSON
    python3 scripts/forge.py mr create --title <t> --description-file <path>
    python3 scripts/forge.py mr edit <n> --description-file <path>
    python3 scripts/forge.py protection                            the rules on main, as JSON
"""
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

STATE = Path(__file__).resolve().parent.parent / ".forge" / "state.json"
LOG = STATE.with_name("calls.log")
PROJECT = "https://forge.yard.example/yard/chandlery"
KEYWORD = r"(?i)\b(?:clos(?:e|es|ed|ing)|fix(?:|es|ed|ing)|resolv(?:e|es|ed|ing)|implement(?:s|ed|ing)?)\b:?[ \t]+"
REF = r"(?:#(\d+)|" + re.escape(PROJECT) + r"/-/(?:issues|work_items)/(\d+))"


def closes(description):
    """What the forge registers: the keyword, then a bare reference or URL, then more joined by commas or 'and'."""
    found = []
    for match in re.finditer(KEYWORD + REF + r"((?:\s*(?:,|and)\s*" + REF + r")*)", description):
        found.append(int(match.group(1) or match.group(2)))
        for more in re.finditer(REF, match.group(3) or ""):
            found.append(int(more.group(1) or more.group(2)))
    return sorted(set(found))


def item(items, number):
    for entry in items:
        if str(entry["number"]) == str(number).lstrip("#!"):
            return entry
    sys.exit(f"forge: no such number {number}")


def flag(argv, name):
    return argv[argv.index(name) + 1] if name in argv and argv.index(name) + 1 < len(argv) else None


def main(argv):
    LOG.parent.mkdir(exist_ok=True)
    with LOG.open("a") as log:
        log.write(f"{datetime.now(timezone.utc).isoformat(timespec='seconds')} {' '.join(argv)}\n")
    state = json.loads(STATE.read_text())
    noun, verb, rest = (argv + ["", ""])[0], (argv + ["", ""])[1], argv[2:]
    if noun == "issue" and verb == "show" and rest:
        entry = item(state["issues"], rest[0])
        print(f"#{entry['number']} [{entry['state']}] {entry['title']}\n\n{entry['body']}")
        for c in entry["comments"]:
            print(f"\n--- comment, {c['when']}\n{c['body']}")
    elif noun == "issue" and verb == "list":
        wanted = flag(argv, "--state") or "opened"
        for entry in state["issues"]:
            if wanted == "all" or entry["state"] == wanted:
                print(f"#{entry['number']}  [{entry['state']}]  {entry['title']}")
    elif noun == "mr" and verb == "list":
        wanted = flag(argv, "--state") or "opened"
        for entry in sorted(state["mrs"], key=lambda e: -e["number"]):
            if wanted == "all" or entry["state"] == wanted:
                print(f"!{entry['number']}  [{entry['state']}]  {entry['title']}")
    elif noun == "mr" and verb == "show" and rest:
        entry = item(state["mrs"], rest[0])
        print(f"!{entry['number']} [{entry['state']}] {entry['title']}\n\n{entry['description']}")
    elif noun == "mr" and verb == "closes" and rest:
        entry = item(state["mrs"], rest[0])
        print(json.dumps([{"iid": n, "web_url": f"{PROJECT}/-/issues/{n}"} for n in closes(entry["description"])], indent=2))
    elif noun == "mr" and verb == "create" and flag(argv, "--title") and flag(argv, "--description-file"):
        number = max(e["number"] for e in state["mrs"]) + 1
        state["mrs"].append({"number": number, "state": "opened", "title": flag(argv, "--title"),
                             "description": Path(flag(argv, "--description-file")).read_text()})
        STATE.write_text(json.dumps(state, indent=2) + "\n")
        print(f"{PROJECT}/-/merge_requests/{number}")
    elif noun == "mr" and verb == "edit" and rest and flag(argv, "--description-file"):
        entry = item(state["mrs"], rest[0])
        entry["description"] = Path(flag(argv, "--description-file")).read_text()
        STATE.write_text(json.dumps(state, indent=2) + "\n")
        print(f"{PROJECT}/-/merge_requests/{entry['number']} updated")
    elif noun == "protection":
        print(json.dumps(state["protection"], indent=2))
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
    "merge_request_required": true,
    "required_checks": [
      "checks"
    ],
    "bypass": [
      "one deploy key"
    ]
  },
  "mrs": [
    {
      "number": 39,
      "state": "merged",
      "title": "0004: sort the low list by shortfall",
      "description": "Closes #26\n\nThe low-stock list now sorts by how far under its floor each item is. Spec 0004."
    },
    {
      "number": 40,
      "state": "merged",
      "title": "0005: a floor per item",
      "description": "Fixes [#29](https://forge.yard.example/yard/chandlery/-/issues/29) (spec [0005](specs/changes/0005-a-floor-per-item.md)).\n\nEach item carries its own reorder point."
    },
    {
      "number": 41,
      "state": "merged",
      "title": "0006: the Thursday email",
      "description": "Fixes [#31](https://forge.yard.example/yard/chandlery/-/work_items/31) (spec [0006](specs/changes/0006-the-thursday-email.md)).\n\nThe low list is mailed to the supplier on Thursday morning."
    },
    {
      "number": 42,
      "state": "merged",
      "title": "0007: consignment stock",
      "description": "Closes [#33](https://forge.yard.example/yard/chandlery/-/issues/33) (spec [0007](specs/changes/0007-consignment-stock.md)).\n\nConsignment items are counted apart and never reordered."
    }
  ],
  "issues": [
    {
      "number": 26,
      "state": "closed",
      "title": "Low-stock list sorts by name, should sort by how short we are",
      "body": "The shackle at zero should be first.",
      "comments": []
    },
    {
      "number": 29,
      "state": "closed",
      "title": "Reorder point per item, not one floor for the shop",
      "body": "Shackles go faster than cleats.",
      "comments": [
        {
          "when": "2026-10-19",
          "body": "Closed by hand: the merge request merged and this stayed open."
        }
      ]
    },
    {
      "number": 31,
      "state": "closed",
      "title": "Email the supplier the low-stock list on Thursday",
      "body": "Every Thursday the list goes out by hand.",
      "comments": [
        {
          "when": "2026-10-19",
          "body": "Closed by hand: the merge request merged and this stayed open."
        }
      ]
    },
    {
      "number": 33,
      "state": "closed",
      "title": "Count the chandlery's consignment stock separately",
      "body": "Consignment items are not ours to reorder.",
      "comments": [
        {
          "when": "2026-10-19",
          "body": "Closed by hand: the merge request merged and this stayed open."
        }
      ]
    },
    {
      "number": 35,
      "state": "opened",
      "title": "Show the supplier's lead time beside each low item",
      "body": "Some things take three weeks.",
      "comments": []
    }
  ]
}
JSONEOF
printf '.forge/\n' >> .gitignore

python3 tools/gen_config.py
git init -q -b main
git remote add origin git@forge.yard.example:yard/chandlery.git
git add -A
git -c user.name=owner -c user.email=owner@chandlery.example commit -q -m "chandlery, with the process and its trees"
