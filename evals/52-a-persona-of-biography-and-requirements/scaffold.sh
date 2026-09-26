#!/usr/bin/env bash
# The fixture for 52: fieldnote, a birdwatcher's sighting log, whose one persona carries every fault the skill's line-by-line tests name — provenance in the opening lines, a demographic doing argumentative work, a life goal where the end goal belongs, three requirements inside the habits, and a refusals list filled by inference — beside observed paragraphs that must survive. Its ledger also reads 'no personas exist' while one does. The case grades the audit.
# Read by caselib.py, run by `run.py --scaffold` in both arms alike. See 0054 / #123.
set -euo pipefail

mkdir -p specs/personas specs/workflows specs/features/log specs/changes specs/setup scripts src

cat > CLAUDE.md <<'EOF'
# fieldnote

One birdwatcher's sighting log, kept on their own phone. No server, no
accounts, no build step. `specs/` is the contract: read
`specs/setup/README.md` before assuming any command, and spec before code — a
change starts life in `specs/changes/`, never in `src/`.
EOF

cat > scripts/trace.py <<'PYEOF'
#!/usr/bin/env python3
# The traceability check fieldnote's bindings name. Standard library only.
import re
import sys
from pathlib import Path

errors = []
personas = {}
for f in sorted(Path("specs/personas").glob("*.md")):
    if f.name == "README.md":
        continue
    text = f.read_text()
    head = text.splitlines()[0] if text.strip() else ""
    pid = re.search(r"@persona:([\w-]+)", head)
    if pid:
        personas[pid.group(1)] = "@retired" in head
named = set()
for f in sorted(Path("specs/workflows").glob("*.feature")):
    head = f.read_text().splitlines()[0]
    pid = re.search(r"@persona:([\w-]+)", head)
    if not pid:
        errors.append(f"{f}: workflow names no persona")
        continue
    named.add(pid.group(1))
    if pid.group(1) not in personas:
        errors.append(f"{f}: names persona {pid.group(1)}, which does not exist")
    elif personas[pid.group(1)]:
        errors.append(f"{f}: names persona {pid.group(1)}, which is @retired")
for pid, retired in sorted(personas.items()):
    if pid not in named and not retired:
        errors.append(f"specs/personas: persona {pid} is named by no workflow and is not @retired")
for f in sorted(Path("specs/features").rglob("*.feature")):
    head = f.read_text().splitlines()[0]
    if not re.search(r"@workflow:([\w-]+)", head):
        errors.append(f"{f}: feature names no workflow")
for e in errors:
    print("error:", e)
print(f"{len(errors)} error(s)")
sys.exit(1 if errors else 0)
PYEOF

cat > specs/spec.md <<'EOF'
# fieldnote

One person's log of what they saw and where. A **sighting** is a species, a
place and a time, written down while they are still standing there. The
**log** is every sighting, newest first. Everything lives on the phone.

What it must always be:

- **Theirs alone.** No accounts, no sync, no server, no sharing. The log is
  private and stays that way.
- **Faster than the notebook.** Writing a sighting takes less time than
  getting a pen out with binoculars round your neck.
- **It never loses a sighting.** Anything written stays until the watcher
  deletes it; nothing expires and nothing is tidied away.

What it is not: a bird identification guide, a social feed, a records
committee submission tool, a survey app for a club. Anything that needs a
second person is out.
EOF

cat > specs/features/log/writing.feature <<'EOF'
@feature:writing @workflow:writing-a-sighting
Feature: Writing a sighting down

  @rule:sighting-goes-to-top
  Rule: a new sighting lands at the top of the log

    Example: newest first
      Given sightings "wren, hedge" and "robin, feeder"
      When they write "kingfisher, weir"
      Then the log reads "kingfisher, weir", "wren, hedge", "robin, feeder"

  @rule:sighting-carries-place-and-time
  Rule: a sighting is stamped with where and when it was written

    Example: stamped where it happened
      Given they are at the weir at 07:15
      When they write "kingfisher"
      Then the sighting shows the weir and 07:15
EOF

cat > index.html <<'EOF'
<!doctype html>
<meta charset="utf-8">
<title>fieldnote</title>
<body>
  <input id="write" placeholder="What did you see?" autofocus>
  <ul id="log"></ul>
  <script src="src/fieldnote.js"></script>
</body>
EOF

cat > src/fieldnote.js <<'EOF'
const load = () => JSON.parse(localStorage.getItem("sightings") || "[]");
const save = (s) => localStorage.setItem("sightings", JSON.stringify(s));

function render() {
  const list = document.getElementById("log");
  list.innerHTML = "";
  for (const s of load()) {
    const item = document.createElement("li");
    item.textContent = `${s.what} — ${s.where || "unknown"} ${s.when}`;
    list.append(item);
  }
}

document.getElementById("write").onkeydown = (event) => {
  if (event.key !== "Enter" || !event.target.value.trim()) return;
  const when = new Date().toISOString().slice(11, 16);
  save([{ what: event.target.value.trim(), where: "", when }, ...load()]);
  event.target.value = "";
  render();
};

render();
EOF

cat > specs/setup/README.md <<'EOF'
# Bindings

| | |
|---|---|
| **Where the app runs** | open `index.html` on the phone's browser; no build step |
| **Tests** | none yet — the suite is a coming infrastructure change |
| **Verification** | `python3 scripts/trace.py` |
| **Tracker** | none — requests arrive in conversation and become change specs |
| **Change specs** | `specs/changes/NNNN-<slug>.md`, numbered one past the highest |

## Gate wiring ledger

| check | state | since |
|---|---|---|
| a feature naming no workflow | automated — `python3 scripts/trace.py` | 0001 |
| every workflow names a live persona | not applicable — no personas exist | 0001 |
| every persona is named by a workflow, or is `@retired` | not applicable — no personas exist | 0001 |
EOF

cat > specs/personas/README.md <<'EOF'
# Personas

Who fieldnote is for, and who it is explicitly not for. Every workflow is
written for somebody in this folder; a workflow naming nobody, and a persona no
workflow names, are both errors the check catches.

A persona holds three things — the problem, the habits, the desires. Not
requirements, not biography doing argumentative work, and not who was
interviewed: that last belongs in the change spec.

| persona | what they are trying to get done |
|---|---|
| `patch-watcher` | know what turns up on one patch, across a year |
EOF

cat > specs/personas/patch-watcher.md <<'EOF'
@persona:patch-watcher

# Marek — the patch watcher

*Written up from a phone call with Marek on 12 March 2026, plus two evenings
watching him use the notebook. Roughly a third of what follows is inferred
rather than observed, and the weekend sections are a guess we should check.*

Marek is 46, a secondary-school geography teacher, and lives in a terraced
house in Shrewsbury with his wife and two teenage children. He has worn the
same waxed jacket for eleven years.

## The problem

He walks the same two miles of canal three or four mornings a week before
school, and he cannot tell you what he saw there last April. The notebook in
his car has eleven years of sightings in it and no way to look anything up, so
the question he most wants answered — *is the kingfisher back earlier than last
year?* — takes an evening of page-turning, and he has stopped asking it.

What he wants is to become a better naturalist, and to feel the mornings add up
to something.

## What they do

- Walks the canal three or four mornings a week, always the same route, always
  before 07:40 because he has to be at school.
- Writes sightings in a paper notebook kept in the car, standing up, one-handed,
  with binoculars round his neck. Species and place, nothing else.
- Copies nothing up at home. The notebook is the only record and he has never
  transcribed one.
- Asks his wife to remember dates for him, because she is better at it.
- Uses a phone from 2019 with a cracked screen, in the rain, in gloves.
- Being a teacher, he is comfortable with software but has no patience for it
  before 07:00.

The app must never ask him to log in, and it must work with one thumb. It
should also let him export the whole log as a spreadsheet at the end of a year,
and it must not show him other people's sightings.

## What they will never do

- He would never share his patch list publicly, or submit records to the county
  recorder.
- He would probably never pay a subscription, being a teacher.
- He would not want a social feed.

## Open questions

- Nothing yet.
EOF

cat > specs/workflows/writing-a-sighting.feature <<'EOF'
@workflow:writing-a-sighting @persona:patch-watcher
Feature: Write a sighting down while standing there

  When something turns up in front of me and I have binoculars in one hand,
  I want it written down before I have walked on and lost the detail,
  so that the morning is still there in April when I want to compare it.

  **Ends when** the sighting is in the log with its place and time.

  **Done well.** One thumb, standing up, in the rain. Faster than the notebook.

  **Where it breaks.** Gloves. A phone gone to sleep. A bird he cannot name
  yet, which the notebook lets him fudge and a form may not.

  Example: a sighting is written at the weir
    Given the log is open
    When they write "kingfisher" at the weir
    Then the sighting is at the top of the log, stamped with the weir and the time

  Example: it survives being closed
    Given "kingfisher, weir" was written
    When they come back to the log
    Then it is exactly as left
EOF

cat > specs/changes/0001-write-a-sighting.md <<'EOF'
# Spec 0001: write a sighting down

- **Status:** shipped
- **Issue:** none — direct request

## Who this is for

The patch watcher, standing on the towpath with binoculars in one hand.

## What changes

One field, the species, stamped with place and time, at the top of the log.
Phone storage only, per the always-list in `specs/spec.md`.
EOF

cat > specs/changes/0002-where-and-when.md <<'EOF'
# Spec 0002: where and when

- **Status:** shipped
- **Issue:** none — direct request

## Who this is for

The patch watcher. The sighting he writes at the weir has to still say the
weir in April.

## What changes

Every sighting is stamped with its place and time as it is written.
EOF

git init -q -b main
git add -A
GIT_AUTHOR_DATE=2026-03-14T08:00:00 GIT_COMMITTER_DATE=2026-03-14T08:00:00 \
  git -c user.email=sam@fieldnote.example -c user.name="Fieldnote" \
  commit -qm "0002: where and when"
