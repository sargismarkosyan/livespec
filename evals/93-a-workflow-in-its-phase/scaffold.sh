#!/usr/bin/env bash
# The fixture for 93: fieldnote with one workflow, placed in its journey's map at "Out on the patch", and a second
# attempt nothing describes — going back through the log to settle an argument about a date. The journey's map has
# a phase "A question comes up" that the new attempt is plainly made in. The case grades the new workflow naming
# it, and the journey left exactly as it was. See specs/changes/0084.
set -euo pipefail

mkdir -p specs/personas specs/journeys specs/workflows specs/features/log specs/changes specs/setup scripts src tests

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
warnings = []


def first_line(f):
    text = f.read_text()
    return text.splitlines()[0] if text.strip() else ""


def phases_of(f):
    """The headings of the journey's map, lower case and hyphenated."""
    in_map = False
    for line in f.read_text().splitlines():
        if re.match(r"^##\s+The map\s*$", line.strip()):
            in_map = True
        elif in_map and line.startswith("## "):
            return []
        elif in_map and line.strip().startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")][1:]
            names = [re.sub(r"[^a-z0-9]+", "-", re.sub(r"[*_`']", "", c).lower()).strip("-") for c in cells]
            return [n for n in names if n]
    return []


personas = {}
for f in sorted(Path("specs/personas").glob("*.md")):
    if f.name == "README.md":
        continue
    pid = re.search(r"@persona:([\w-]+)", first_line(f))
    if pid:
        personas[pid.group(1)] = "@retired" in first_line(f)

journeys = {}
for f in sorted(Path("specs/journeys").glob("*.md")):
    if f.name == "README.md":
        continue
    jid = re.search(r"@journey:([\w-]+)", first_line(f))
    if jid:
        journeys[jid.group(1)] = phases_of(f)

workflows = {}
for f in sorted(Path("specs/workflows").glob("*.feature")):
    head = first_line(f)
    wid = re.search(r"@workflow:([\w-]+)", head)
    if not wid:
        continue
    workflows[wid.group(1)] = {"file": f, "planned": "@planned" in head}
    pid = re.search(r"@persona:([\w-]+)", head)
    if not pid:
        errors.append(f"{f}: workflow names no persona")
    elif pid.group(1) not in personas:
        errors.append(f"{f}: names persona {pid.group(1)}, which does not exist")
    named = re.findall(r"@journey:([\w-]+)", head)
    for jid in named:
        if jid not in journeys:
            errors.append(f"{f}: names journey {jid}, which does not exist")
    if not named:
        warnings.append(f"{f}: names no journey")
    for phase in re.findall(r"@phase:([\w-]+)", head):
        if not any(phase in journeys.get(j, []) for j in named):
            errors.append(f"{f}: names phase {phase}, which no journey it names has")

served = set()
for f in sorted(Path("specs/features").rglob("*.feature")):
    wid = re.search(r"@workflow:([\w-]+)", first_line(f))
    if not wid:
        errors.append(f"{f}: feature names no workflow")
        continue
    served.add(wid.group(1))
    if wid.group(1) not in workflows:
        errors.append(f"{f}: names workflow {wid.group(1)}, which does not exist")

walked = set()
for f in sorted(Path("tests").rglob("*.py")):
    walked.update(re.findall(r"@workflow:([\w-]+)", f.read_text()))

for wid, info in sorted(workflows.items()):
    if info["planned"]:
        continue
    if wid not in served:
        errors.append(f"specs/workflows: workflow {wid} is claimed by no feature")
    if wid not in walked:
        errors.append(f"specs/workflows: workflow {wid} is walked by no end-to-end test")

for pid, retired in sorted(personas.items()):
    if not retired and not any(re.search(rf"@persona:{pid}\b", first_line(w["file"])) for w in workflows.values()):
        errors.append(f"specs/personas: persona {pid} is named by no workflow and is not @retired")

for w in warnings:
    print("warning:", w)
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
- **It never loses a sighting.**

What it is not: an identification guide, a social feed, a survey app for a
club.
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
- Writes species and place standing up, one-handed.
- Argues about dates with whoever is walking with him.
EOF

cat > specs/journeys/README.md <<'EOF'
# Journeys

One file per journey, `@journey:<id>` on the first line, prose and tables. A
journey names no workflow: each workflow says which arc it sits in, and which
of its phases, by the headings of the map.
EOF

cat > specs/journeys/a-year-on-the-patch.md <<'EOF'
@journey:a-year-on-the-patch @persona:patch-watcher

# Keeping a year on the patch

## The lens

| | |
|---|---|
| **Actor** | Marek, who walks the same stretch of canal most mornings. |
| **Scenario** | A year of walks, and the questions about it that come up on them. |
| **Goal** | To know what turned up, and when, without an evening of page-turning. |
| **Span** | A year, made of short walks and the odd argument. |

## The map

| | **Before the log** | **Out on the patch** | **A question comes up** | **The quiet months** |
|---|---|---|---|---|
| **Doing** | 1. Writes in a notebook kept in the car.<br>2. Never looks anything up. | 3. Writes what he sees, standing up.<br>4. Walks on. | 5. Somebody asks whether a bird is early or late.<br>6. He tries to remember. | 7. Walks less.<br>8. Writes little. |
| **Thinking** | *"it's all in there somewhere"* | *"got it, keep moving"* | *(paraphrase) I know I saw one earlier last year* | *(paraphrase) nothing much to write* |
| **Feeling** | ▂ | ▆ | ▃ | ▄ |

**The curve.** It dips where a question comes up: the answer is written down
and he still cannot reach it while the person asking is standing there.
EOF

cat > specs/workflows/README.md <<'EOF'
# Workflows

A workflow is a bounded attempt: a trigger, some steps, and an end state you
can stand at and say done. Its first line names the persona, the journey and
the journey's phases it is made in.

| workflow | carries |
|---|---|
| `writing-a-sighting` | the species goes down before he has walked on |
EOF

cat > specs/workflows/writing-a-sighting.feature <<'EOF'
@workflow:writing-a-sighting @persona:patch-watcher @journey:a-year-on-the-patch @phase:out-on-the-patch
Feature: Write a sighting down while standing there

  When something turns up in front of me and I have binoculars in one hand,
  I want it written down before I have walked on and lost the detail,
  so that the morning is still there in April when I want to compare it.

  **Ends when** the sighting is in the log with its place and time.

  **Where it breaks.** Gloves. A phone gone to sleep. A bird he cannot name.

  Example: a sighting is written at the weir
    Given the log is open
    When they write "kingfisher" at the weir
    Then the sighting is at the top of the log, stamped with the weir and the time

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
EOF

cat > tests/test_writing_a_sighting.py <<'EOF'
# Walks @workflow:writing-a-sighting end to end.


def test_a_sighting_is_written_and_survives_a_reopen():
    log = []
    log.insert(0, {"what": "kingfisher", "where": "weir", "when": "07:15"})
    assert log[0]["what"] == "kingfisher"
    assert list(log) == log
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
| a journey naming a workflow that does not exist | automated — `python3 scripts/trace.py` | 0003 |
| a workflow naming no journey | automated, warns — `python3 scripts/trace.py` | 0003 |
| a workflow naming a phase its journey does not have | automated — `python3 scripts/trace.py` | 0003 |
EOF

cat > specs/changes/0001-write-a-sighting.md <<'EOF'
# Spec 0001: write a sighting down

- **Status:** shipped

One field, the species, stamped with place and time, at the top of the log.
EOF

cat > specs/changes/0002-the-workflow-layer.md <<'EOF'
# Spec 0002: the workflow layer

- **Status:** shipped

The attempt behind the log got a file, and the persona got named.
EOF

cat > specs/changes/0003-a-year-on-the-patch.md <<'EOF'
# Spec 0003: a year on the patch

- **Status:** shipped

The journey, from one conversation with Marek, and the phase the one workflow
is made in.
EOF

git init -q -b main
git add -A
GIT_AUTHOR_DATE=2026-04-02T09:00:00 GIT_COMMITTER_DATE=2026-04-02T09:00:00 \
  git -c user.email=sam@fieldnote.example -c user.name="Fieldnote" \
  commit -qm "0003: a year on the patch"
