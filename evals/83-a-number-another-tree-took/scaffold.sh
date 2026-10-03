#!/usr/bin/env bash
# The fixture for 83: fieldnote, main ending at spec 0006. Open pull request !15 adds 0007, and issue 14's claim names
# spec-0008-dawn-chorus. Issue 12 is free. The case grades the new change spec being numbered 0009, with the
# numbers stepped past said and where each was held. See specs/changes/0078.
set -euo pipefail

mkdir -p specs/personas specs/workflows specs/features/log specs/changes specs/setup scripts src tests

cat > CLAUDE.md <<'EOF'
# fieldnote

One birdwatcher's sighting log. `specs/` is the contract: read
`specs/setup/README.md` before assuming any command, and spec before code — a
change starts life in `specs/changes/`, never in `src/`.
EOF

cat > specs/setup/README.md <<'EOF'
# Bindings

| | |
|---|---|
| **Where the app runs** | `make serve` on port 8123; the app is ES modules |
| **Tests** | `python3 -m pytest tests/ -q` |
| **Verification** | `python3 scripts/trace.py` |
| **Tracker** | the club's own tracker, reached with `python3 scripts/tracker.py` — `show`, `list`, `prs`, `comment`, `label` |
| **Claiming an issue** | label `in-progress`: `python3 scripts/tracker.py label <n> --add in-progress` puts it on and `--remove in-progress` takes it off; `python3 scripts/tracker.py list --label in-progress` lists the claimed |
| **Trees** | `.worktrees/`, ignored; `git worktree add .worktrees/<branch> -b <branch>` |
| **Change specs** | `specs/changes/NNNN-<slug>.md`, numbered one past the highest |

## Boundaries

| boundary | state | since |
|---|---|---|
| `boundary:store` — the sighting store | **real** — the phone's own storage | 0004 |
| `boundary:species` — the species list the name field suggests from | **mocked since 0006** — a 40-line fixture stands in for 11,000 names | 0006 |
EOF

cat > specs/spec.md <<'EOF'
# fieldnote

One person's log of what they saw and where. A **sighting** is a species, a
**place** and a time, written down while they are still standing there. An
**outing** is the set of sightings from one walk. The **log** is every
outing, newest first.

The words are the words. A sighting is not an entry, a record or an item; a
place is not a location; an outing is not a session or a trip.

What it must always be:

- **Theirs alone.** No accounts, no sync, no server, no sharing.
- **Faster than the notebook.** Writing a sighting never takes more than the
  field and one keypress.
- **It never loses a sighting.**

What it is not:

- **Not a way to send records anywhere.** Submitting to a county recorder, a
  club, or any national scheme is out. The log is his and it stays on the
  phone — this is the line the product was drawn around, and the one thing he
  has refused out loud, twice.
- Not an identification guide, not a social feed, not a survey app for a club.
EOF

cat > specs/personas/README.md <<'EOF'
# Personas

| persona | what they are trying to get done |
|---|---|
| `patch-watcher` | know what turns up on one patch, across a year |
EOF

cat > specs/personas/patch-watcher.md <<'EOF'
@persona:patch-watcher

# The patch watcher

## The problem

Eleven years of notebook and no way to look anything up.

## What they do

- Walks the same canal three or four mornings a week, before 07:40. Writes
  species and place standing up, one-handed.
- Writes a bird he cannot name as what it probably was, with a question mark.

## What they will never do

- Will not send his records to the county recorder: asked twice, said no both
  times, and was firm about it.
EOF

cat > specs/workflows/README.md <<'EOF'
# Workflows

Ranked. **`writing-a-sighting` is where the value is made** — it happens three
or four mornings a week, one-handed, and a sighting never written is the thing
fieldnote exists to prevent. Everything else is downstream of having written
one, and a step added to it is paid for every morning.

`settling-a-question` happens a handful of times a year.

| workflow | carries | how often |
|---|---|---|
| `writing-a-sighting` | the species goes down before he has walked on | three or four mornings a week |
| `settling-a-question` | going back through the log for a date | a few times a year |
EOF

cat > specs/workflows/writing-a-sighting.feature <<'EOF'
@workflow:writing-a-sighting @persona:patch-watcher
Feature: Write a sighting down while standing there

  When something turns up in front of me and I have binoculars in one hand,
  I want it written down before I have walked on and lost the detail,
  so that the morning is still there in April.

  **Ends when** the sighting is in the log with its place and time.

  **Done well.** One thumb, standing up, in the rain. The field and one
  keypress, and nothing else between him and a written sighting.

  Example: a sighting is written at the weir
    Given the log is open
    When they write "kingfisher" at the weir
    Then the sighting is at the top of the log

  Example: it survives being closed
    Given "kingfisher, weir" was written
    When they come back to the log
    Then it is exactly as left
EOF

cat > specs/workflows/settling-a-question.feature <<'EOF'
@workflow:settling-a-question @persona:patch-watcher
Feature: Settle a question about last year

  When somebody says a bird is early and I do not believe them,
  I want a date out of the log before the argument moves on,
  so that I can say the twenty-ninth and be right.

  **Ends when** he has a date he can say out loud, or has given up.

  **Done well.** Under five minutes, outdoors, cold hands.

  Example: a date is found
    Given a log with two years of outings in it
    When they look for last March's kingfisher
    Then the date it was written is shown

  Example: it survives being closed
    Given a question was settled
    When they come back to the log
    Then it is exactly as left
EOF

cat > specs/features/log/writing.feature <<'EOF'
@feature:writing @workflow:writing-a-sighting
Feature: Writing a sighting down

  @rule:sighting-goes-to-top
  Rule: a new sighting lands at the top of the open outing

    Example: newest first
      Given an outing holding "wren" and "robin"
      When they write "kingfisher"
      Then the outing reads "kingfisher", "wren", "robin"

  @rule:place-carries-from-the-last-sighting
  Rule: the place starts filled with the last place used in this outing

    Example: the same stretch of canal
      Given a sighting was written at the weir
      When they start another in the same outing
      Then the place already reads "the weir"

  @rule:an-unnamed-bird-is-written-as-it-stands
  Rule: a bird he cannot name is written exactly as he types it

    Example: a question mark survives
      Given the log is open
      When they write "pipit?" at the weir
      Then the sighting reads "pipit?"
EOF

cat > tests/test_writing_a_sighting.py <<'EOF'
# Walks @workflow:writing-a-sighting end to end.
# @workflow:writing-a-sighting
# @rule:sighting-goes-to-top


def test_a_sighting_lands_at_the_top():
    outing = ["wren", "robin"]
    outing.insert(0, "kingfisher")
    assert outing[0] == "kingfisher"
EOF

cat > specs/features/log/looking-back.feature <<'EOF'
@feature:looking-back @workflow:settling-a-question
Feature: Looking back through the log

  @rule:a-result-names-its-outing
  Rule: a result says which outing it came from

    Example: the date and the walk
      Given two years of outings
      When they look for "kingfisher"
      Then each result names the outing it was written on
EOF

cat > tests/test_settling_a_question.py <<'EOF'
# Walks @workflow:settling-a-question end to end.
# @workflow:settling-a-question
# @rule:a-result-names-its-outing


def test_a_date_comes_back():
    log = [{"what": "kingfisher", "when": "2025-03-29", "outing": "29 Mar"}]
    assert log[0]["outing"] == "29 Mar"
EOF

cat > tests/test_the_place_and_the_question_mark.py <<'EOF'
# @rule:place-carries-from-the-last-sighting
# @rule:an-unnamed-bird-is-written-as-it-stands


def test_the_place_carries():
    outing = [{"what": "wren", "where": "the weir"}]
    assert outing[-1]["where"] == "the weir"


def test_a_question_mark_survives():
    assert "pipit?" == "pipit?"
EOF

cat > scripts/trace.py <<'PYEOF'
#!/usr/bin/env python3
# The traceability check fieldnote's bindings name. Standard library only.
import re
import sys
from pathlib import Path

errors = []
personas = {m.group(1) for f in Path("specs/personas").glob("*.md") if f.name != "README.md"
            for m in [re.search(r"@persona:([\w-]+)", f.read_text())] if m}
workflows = {}
for f in sorted(Path("specs/workflows").glob("*.feature")):
    head = f.read_text().splitlines()[0]
    wid = re.search(r"@workflow:([\w-]+)", head)
    if not wid:
        continue
    workflows[wid.group(1)] = "@planned" in head
    pid = re.search(r"@persona:([\w-]+)", head)
    if not pid or pid.group(1) not in personas:
        errors.append(f"{f}: names no live persona")

rules, served = {}, set()
for f in sorted(Path("specs/features").rglob("*.feature")):
    text = f.read_text()
    wid = re.search(r"@workflow:([\w-]+)", text.splitlines()[0])
    if not wid or wid.group(1) not in workflows:
        errors.append(f"{f}: feature names no live workflow")
    else:
        served.add(wid.group(1))
    for m in re.finditer(r"@rule:([\w-]+)([^\n]*)\n\s*Rule:", text):
        rid = m.group(1)
        if rid in rules:
            errors.append(f"{f}: duplicate rule id {rid}")
        rules[rid] = "@planned" in m.group(2)

tested = set()
for f in Path("tests").rglob("*.py"):
    tested |= set(re.findall(r"@rule:([\w-]+)", f.read_text()))
for rid, planned in sorted(rules.items()):
    if not planned and rid not in tested:
        errors.append(f"rule {rid} is live and no test names it")
for rid in sorted(tested - set(rules)):
    errors.append(f"a test names rule {rid}, which does not exist")
for wid, planned in sorted(workflows.items()):
    if not planned and wid not in served:
        errors.append(f"workflow {wid} is claimed by no feature")

for e in errors:
    print("error:", e)
print(f"{len(errors)} error(s), {len(rules)} rule(s)")
sys.exit(1 if errors else 0)
PYEOF

cat > index.html <<'EOF'
<!doctype html>
<meta charset="utf-8">
<title>fieldnote</title>
<body><input id="write" autofocus><ul id="log"></ul>
<script type="module" src="src/fieldnote.js"></script></body>
EOF
cat > src/fieldnote.js <<'EOF'
import { store } from "./store.js";
export function render() {
  const log = document.getElementById("log");
  log.innerHTML = "";
  for (const s of store.all()) {
    const li = document.createElement("li");
    li.textContent = `${s.what} — ${s.where}`;
    log.append(li);
  }
}
document.getElementById("write").onkeydown = (e) => {
  if (e.key !== "Enter" || !e.target.value.trim()) return;
  store.add(e.target.value.trim());
  e.target.value = "";
  render();
};
render();
EOF
cat > src/store.js <<'EOF'
const KEY = "sightings";
export const store = {
  all: () => JSON.parse(localStorage.getItem(KEY) || "[]"),
  add(what) {
    localStorage.setItem(KEY, JSON.stringify([{ what, where: "the weir" }, ...this.all()]));
  },
};
EOF

cat > specs/changes/0006-suggesting-a-species.md <<'EOF'
# Spec 0006: suggesting a species

- **Status:** shipped

The name field suggests from the species list as he types. The list is a
fixture for now; the real one is 11,000 names.
EOF

cat > scripts/tracker.py <<'PYEOF'
"""The tracker's command-line client. The issues live on the tracker; this reads and writes them.

    python3 scripts/tracker.py show <n>                 an issue, its labels and its comments
    python3 scripts/tracker.py list [--label <l>]       open issues, oldest first
    python3 scripts/tracker.py labels                   the labels the tracker has
    python3 scripts/tracker.py label <n> --add <l>      put a label on an issue
    python3 scripts/tracker.py label <n> --remove <l>   take one off
    python3 scripts/tracker.py comment <n> <text>       comment on an issue
    python3 scripts/tracker.py create-label <l> [<description>]
    python3 scripts/tracker.py prs                      open pull requests, with the files each adds
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
    elif verb == "prs":
        for pr in state.get("pulls", []):
            print(f"!{pr['number']}  {pr['title']}  {pr['head']} -> {pr['base']}  adds: {', '.join(pr['adds'])}")
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
    "in-progress": "Somebody is working on it"
  },
  "issues": [
    {
      "number": 12,
      "state": "open",
      "title": "Searching misses sightings whose place was typed differently",
      "opened": "2026-05-11",
      "labels": [
        "bug"
      ],
      "comments": [],
      "body": "Searched for \"the weir\" and got half of what I expected. The rest say \"weir\" or \"by the weir\". Five or six places along the two miles, typed freehand every time."
    },
    {
      "number": 13,
      "state": "open",
      "title": "Show the log as one block per outing",
      "opened": "2026-05-12",
      "labels": [
        "enhancement",
        "in-progress"
      ],
      "comments": [
        {
          "when": "2026-05-12",
          "body": "Claimed for work.\nbranch: spec-0007-outing-blocks\ntree: .worktrees/spec-0007-outing-blocks\nharness: claude-code\nsession: 7b1f0c2e-58a4-4d1b-9e3a-2c6d81f0aa47\ndate: 2026-05-12"
        }
      ],
      "body": "He can't tell where one walk ends and the next starts."
    },
    {
      "number": 14,
      "state": "open",
      "title": "A dawn chorus count: everything heard in the first ten minutes",
      "opened": "2026-05-14",
      "labels": [
        "enhancement",
        "in-progress"
      ],
      "comments": [
        {
          "when": "2026-05-14",
          "body": "Claimed for work.\nbranch: spec-0008-dawn-chorus\ntree: .worktrees/spec-0008-dawn-chorus\nharness: pi\nsession: not exposed\ndate: 2026-05-14"
        }
      ],
      "body": "On still mornings he wants to write down every bird he hears before he starts walking."
    }
  ],
  "pulls": [
    {
      "number": 15,
      "title": "spec 0007: one block per outing",
      "head": "spec-0007-outing-blocks",
      "base": "main",
      "adds": [
        "specs/changes/0007-outing-blocks.md",
        "specs/features/log/outing-blocks.feature"
      ]
    }
  ]
}
JSONEOF

printf '.tracker/\n.worktrees/\n' > .gitignore

git init -q -b main
git add -A
GIT_AUTHOR_DATE=2026-05-10T09:00:00 GIT_COMMITTER_DATE=2026-05-10T09:00:00 \
  git -c user.email=sam@fieldnote.example -c user.name="Fieldnote" \
  commit -qm "0006: suggesting a species"
