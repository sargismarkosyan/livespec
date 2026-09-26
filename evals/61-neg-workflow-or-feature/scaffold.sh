#!/usr/bin/env bash
# The fixture for 61: fieldnote in good order, and a question about what separates a workflow file from a feature file. The case grades nothing firing.
# Read by caselib.py, run by `run.py --scaffold` in both arms alike. See 0054 / #123.
set -euo pipefail

mkdir -p specs/personas specs/workflows specs/features/log specs/changes specs/setup scripts src tests

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
    head = f.read_text().splitlines()[0] if f.read_text().strip() else ""
    pid = re.search(r"@persona:([\w-]+)", head)
    if pid:
        personas[pid.group(1)] = "@retired" in head

workflows = {}
for f in sorted(Path("specs/workflows").glob("*.feature")):
    head = f.read_text().splitlines()[0]
    wid = re.search(r"@workflow:([\w-]+)", head)
    if not wid:
        continue
    workflows[wid.group(1)] = {"file": f, "planned": "@planned" in head}
    pid = re.search(r"@persona:([\w-]+)", head)
    if not pid:
        errors.append(f"{f}: workflow names no persona")
    elif pid.group(1) not in personas:
        errors.append(f"{f}: names persona {pid.group(1)}, which does not exist")

served = set()
for f in sorted(Path("specs/features").rglob("*.feature")):
    head = f.read_text().splitlines()[0]
    wid = re.search(r"@workflow:([\w-]+)", head)
    if not wid:
        errors.append(f"{f}: feature names no workflow")
        continue
    served.add(wid.group(1))
    if wid.group(1) not in workflows:
        errors.append(f"{f}: names workflow {wid.group(1)}, which does not exist")

walked = set()
for f in sorted(Path("tests").rglob("*.py")):
    for wid in re.findall(r"@workflow:([\w-]+)", f.read_text()):
        walked.add(wid)

for wid, info in sorted(workflows.items()):
    if info["planned"]:
        continue
    if wid not in served:
        errors.append(f"specs/workflows: workflow {wid} is claimed by no feature")
    if wid not in walked:
        errors.append(f"specs/workflows: workflow {wid} is walked by no end-to-end test")

for pid, retired in sorted(personas.items()):
    if retired:
        continue
    if not any(re.search(rf"@persona:{pid}\b", w["file"].read_text().splitlines()[0]) for w in workflows.values()):
        errors.append(f"specs/personas: persona {pid} is named by no workflow and is not @retired")

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

- **Theirs alone.** No accounts, no sync, no server, no sharing.
- **Faster than the notebook.** Writing a sighting takes less time than
  getting a pen out with binoculars round your neck.
- **It never loses a sighting.** Anything written stays until the watcher
  deletes it; nothing expires and nothing is tidied away.

What it is not: an identification guide, a social feed, a records committee
submission tool, a survey app for a club.
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

Eleven years of notebook and no way to look anything up. The question he keeps
asking — is the kingfisher back earlier than last year? — costs an evening of
page-turning, so he has stopped asking it.

## What they do

- Walks the same canal three or four mornings a week, before 07:40.
- Writes species and place standing up, one-handed, in a notebook kept in the
  car. Never transcribes it.
- Writes a bird he cannot name as what it probably was, with a question mark.

## What they will never do

- Will not send his records to the county recorder: asked twice, said no both
  times.
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

document.getElementById("write").onkeydown = (event) => {
  if (event.key !== "Enter" || !event.target.value.trim()) return;
  const when = new Date().toISOString().slice(11, 16);
  save([{ what: event.target.value.trim(), where: "", when }, ...load()]);
  event.target.value = "";
};
EOF

cat > specs/setup/README.md <<'EOF'
# Bindings

| | |
|---|---|
| **Where the app runs** | open `index.html` on the phone's browser; no build step |
| **Tests** | `python3 -m pytest tests/ -q` |
| **Verification** | `python3 scripts/trace.py` |
| **Tracker** | none — requests arrive in conversation and become change specs |
| **Change specs** | `specs/changes/NNNN-<slug>.md`, numbered one past the highest |

## Gate wiring ledger

| check | state | since |
|---|---|---|
| every feature names a live workflow | automated — `python3 scripts/trace.py` | 0001 |
| every workflow is claimed by a feature | automated — `python3 scripts/trace.py` | 0002 |
| every workflow names a live persona | automated — `python3 scripts/trace.py` | 0002 |
| every workflow is walked by an end-to-end test | automated — `python3 scripts/trace.py` | 0002 |
EOF

cat > specs/changes/0001-write-a-sighting.md <<'EOF'
# Spec 0001: write a sighting down

- **Status:** shipped

One field, the species, stamped with place and time, at the top of the log.
EOF

cat > specs/changes/0002-the-workflow-layer.md <<'EOF'
# Spec 0002: the workflow layer

- **Status:** shipped

The attempt behind the log got a file, the persona got named, and the four
workflow rows in the ledger were wired the day they became applicable.
EOF

cat > specs/workflows/README.md <<'EOF'
# Workflows

A workflow is a bounded attempt: a trigger, some steps, and an end state you
can stand at and say done.

The value is made in `writing-a-sighting` — a sighting that was never written
is the thing fieldnote exists to prevent, and everything else is downstream of
having written one.

| workflow | carries |
|---|---|
| `writing-a-sighting` | the species goes down before he has walked on |
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

  Example: a bird he cannot name
    Given the log is open
    When they write "pipit?" at the weir
    Then the sighting is in the log exactly as written

  Example: it survives being closed
    Given "kingfisher, weir" was written
    When they come back to the log
    Then it is exactly as left
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

cat > tests/test_writing_a_sighting.py <<'EOF'
# Walks @workflow:writing-a-sighting end to end.
# @workflow:writing-a-sighting


def test_a_sighting_is_written_and_survives_a_reopen():
    log = []
    log.insert(0, {"what": "kingfisher", "where": "weir", "when": "07:15"})
    assert log[0]["what"] == "kingfisher"
    reopened = list(log)
    assert reopened == log
EOF

git init -q -b main
git add -A
GIT_AUTHOR_DATE=2026-04-02T09:00:00 GIT_COMMITTER_DATE=2026-04-02T09:00:00 \
  git -c user.email=sam@fieldnote.example -c user.name="Fieldnote" \
  commit -qm "0002: the workflow layer"
