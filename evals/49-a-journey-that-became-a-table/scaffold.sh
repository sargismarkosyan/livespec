#!/usr/bin/env bash
# The fixture for 49: sowlog whose journey was written from the workflows folder without asking the keeper and has become a workflows README with a journey id on top — a table of ids, a rules list, phases that reorder freely — and now carries a workflow name that was retired in July. The case grades taking the ids out and naming what the file had become, not refreshing them.
# Read by caselib.py, run by `run.py --scaffold` in both arms alike. See 0054 / #123.
set -euo pipefail

mkdir -p specs/personas specs/workflows specs/features/diary specs/changes specs/journeys specs/setup scripts src

cat > CLAUDE.md <<'EOF'
# sowlog

One gardener's sowing diary, kept in the browser's local storage. No server,
no accounts, no build step. `specs/` is the contract: read
`specs/setup/README.md` before assuming any command, and spec before code — a
change starts life in `specs/changes/`, never in `src/`.
EOF

cat > specs/setup/README.md <<'EOF'
# Bindings

| | |
|---|---|
| **Where the app runs** | open `index.html` in a browser; no build step |
| **Tests** | none yet — the suite is a coming infrastructure change |
| **Traceability check** | `python3 scripts/trace.py` — exits 1 on an error, prints warnings and exits 0 otherwise |
| **Tracker** | none — requests arrive in conversation and become change specs |
| **Change specs** | `specs/changes/NNNN-<slug>.md`, numbered one past the highest |

## Gate wiring ledger

| check | state | since |
|---|---|---|
| a journey naming a workflow that does not exist | wired — error | 0002 |
| a workflow naming no journey | wired — warning | 0002 |
| a feature naming no workflow | wired — error | 0001 |
EOF

cat > scripts/trace.py <<'EOF'
#!/usr/bin/env python3
# The traceability check sowlog's bindings name. Standard library only.
import re
import sys
from pathlib import Path

errors, warnings = [], []
workflows = {}
for f in sorted(Path("specs/workflows").glob("*.feature")):
    head = f.read_text().splitlines()[0] if f.read_text() else ""
    wid = re.search(r"@workflow:([\w-]+)", head)
    if wid:
        workflows[wid.group(1)] = f
        if not re.search(r"@journey:([\w-]+)", head):
            warnings.append(f"{f}: workflow {wid.group(1)} names no journey")
journeys = {}
for f in sorted(Path("specs/journeys").glob("*.md")):
    if f.name == "README.md":
        continue
    text = f.read_text()
    jid = re.search(r"@journey:([\w-]+)", text)
    if jid:
        journeys[jid.group(1)] = f
    named = set(re.findall(r"workflow:([\w-]+)", text))
    named |= {w for w in re.findall(r"`([a-z]+(?:-[a-z]+)+)`", text)}
    for wid in sorted(named):
        if wid not in workflows:
            errors.append(f"{f}: journey names workflow {wid}, which does not exist")
for f in sorted(Path("specs/workflows").glob("*.feature")):
    head = f.read_text().splitlines()[0]
    jid = re.search(r"@journey:([\w-]+)", head)
    if jid and jid.group(1) not in journeys:
        errors.append(f"{f}: names journey {jid.group(1)}, which does not exist")
for f in sorted(Path("specs/features").rglob("*.feature")):
    head = f.read_text().splitlines()[0]
    wid = re.search(r"@workflow:([\w-]+)", head)
    if not wid or wid.group(1) not in workflows:
        errors.append(f"{f}: feature names no existing workflow")
for w in warnings:
    print("warning:", w)
for e in errors:
    print("error:", e)
print(f"{len(errors)} error(s), {len(warnings)} warning(s)")
sys.exit(1 if errors else 0)
EOF

cat > specs/spec.md <<'EOF'
# sowlog

One gardener's sowing diary, on their own phone or laptop. A **batch** is seeds
sown on a day into a place — a tray on the windowsill, a row in a bed. A batch
is **sown**, then **up** once anything shows, then **out** when it is planted
into its final place, or **failed** if nothing came. The **diary** is every
batch, newest first, with its dates.

What it must always be:

- **Theirs alone.** No accounts, no sync, no server. Local storage is the
  whole persistence story.
- **Quicker than the label.** Recording a batch takes less time than writing
  the plant label it goes in with.
- **It never forgets a batch.** Anything sown stays in the diary until the
  gardener removes it; nothing disappears on its own.

What it is not: a planting calendar, a seed shop, a garden planner, a thing
for a team or a market garden. Anything that needs a second person is out.
EOF

cat > specs/personas/README.md <<'EOF'
# Personas

One. A persona here is a design persona: who this is for, what they are trying
to do, and who it is explicitly not for. It is not the maintainer.
EOF

cat > specs/personas/allotment-keeper.md <<'EOF'
@persona:allotment-keeper

# The allotment keeper

Grows vegetables on one rented plot, ten minutes' walk from home. Sows in
batches from February to June — trays on the windowsill first, then rows in the
beds — and gets to the plot two or three times a week when the weather lets
them. Wants to know what went in where and when, because by May the trays all
look the same.

Not a market gardener and not a club: nobody else needs to read the diary, and
a feature that assumes an audience, a rota or a schedule is for somebody else.
They will not read documentation; the diary has to behave the way it looks,
one-handed, with soil on the other one.
EOF

cat > specs/workflows/README.md <<'EOF'
# Workflows

Two bounded attempts, ranked. The first is where the value is made: a batch
that was never recorded is the thing this exists to prevent. The second is what
keeps the diary from lying.

| workflow | carries |
|---|---|
| `sowing-a-batch` | seeds go in, the batch goes in the diary before the label is written |
| `checking-the-bed` | a walk round the plot, and the diary made to match what is up, out or gone |
EOF

cat > specs/features/diary/batches.feature <<'EOF'
@feature:batches @workflow:sowing-a-batch
Feature: Recording batches

  @rule:batch-goes-to-top
  Rule: a new batch lands at the top of the diary

    Example: newest first
      Given batches "leeks, tray 2" and "broad beans, bed 1"
      When they record "tomatoes, windowsill"
      Then the diary reads "tomatoes, windowsill", "leeks, tray 2", "broad beans, bed 1"

  @rule:batch-carries-its-date
  Rule: a batch is dated the day it is recorded

    Example: sown today
      Given today is 14 March
      When they record "leeks, tray 2"
      Then the batch shows "sown 14 Mar"
EOF

cat > specs/features/diary/states.feature <<'EOF'
@feature:states @workflow:checking-the-bed
Feature: Moving a batch on

  @rule:state-moves-forward
  Rule: a batch moves from sown to up to out, and can fail from either

    Example: something shows
      Given "leeks, tray 2" is sown
      When they mark it up
      Then it shows "up" with today's date

  @rule:failed-stays-in-the-diary
  Rule: a failed batch stays in the diary, marked failed

    Example: nothing came
      Given "parsnips, bed 3" is sown
      When they mark it failed
      Then it shows "failed" and is still in the diary
EOF

cat > specs/changes/0001-record-a-batch.md <<'EOF'
# Spec 0001: record a batch

- **Status:** shipped
- **Issue:** none — direct request

## Who this is for

The allotment keeper, at the moment the seeds are in and the label is not yet
written. Sits at the start of `sowing-a-batch`.

## What changes

One field, enter to record, the batch at the top of the diary with today's
date. Local storage only, per the always-list in `specs/spec.md`.
EOF

cat > specs/changes/0002-mark-a-batch-on.md <<'EOF'
# Spec 0002: mark a batch on

- **Status:** shipped
- **Issue:** none — direct request

## Who this is for

The allotment keeper, walking the plot with the phone. Sits in
`checking-the-bed`.

## What changes

Each batch has one button that moves it to the next state — up, then out — and
a second that marks it failed. Failed batches stay in the diary. The
traceability check gains two rows for the journey layer, both wired.
EOF

cat > index.html <<'EOF'
<!doctype html>
<meta charset="utf-8">
<title>sowlog</title>
<body>
  <input id="record" placeholder="What went in, and where…" autofocus>
  <ul id="diary"></ul>
  <script src="src/sowlog.js"></script>
</body>
EOF

cat > src/sowlog.js <<'EOF'
const load = () => JSON.parse(localStorage.getItem("batches") || "[]");
const save = (batches) => localStorage.setItem("batches", JSON.stringify(batches));
const today = () => new Date().toISOString().slice(0, 10);
const NEXT = { sown: "up", up: "out" };

function render() {
  const batches = load();
  const list = document.getElementById("diary");
  list.innerHTML = "";
  for (const batch of batches) {
    const item = document.createElement("li");
    item.textContent = `${batch.text} — ${batch.state} ${batch.dates[batch.state]}`;
    if (NEXT[batch.state]) {
      const on = document.createElement("button");
      on.textContent = NEXT[batch.state];
      on.onclick = () => { batch.state = NEXT[batch.state]; batch.dates[batch.state] = today(); save(batches); render(); };
      const failed = document.createElement("button");
      failed.textContent = "failed";
      failed.onclick = () => { batch.state = "failed"; batch.dates.failed = today(); save(batches); render(); };
      item.append(" ", on, " ", failed);
    }
    list.append(item);
  }
}

document.getElementById("record").onkeydown = (event) => {
  if (event.key !== "Enter" || !event.target.value.trim()) return;
  save([{ text: event.target.value.trim(), state: "sown", dates: { sown: today() } }, ...load()]);
  event.target.value = "";
  render();
};

render();
EOF

cat > specs/journeys/README.md <<'EOF'
# Journeys

The one layer nothing asserts. A journey is the arc one persona lives over
time — the seasons, not the sittings — and above all the **seams**: what
happens in the gap between two attempts, where neither one is at fault. A
seam is not a defect. If the gap is somebody's fault it is an issue and a
spec; a seam is a moment in their life the product does not reach.

A journey declares its own id and names no workflow. The workflow files say
which arc they sit in. No workflow ids, rule ids or tag names in the prose:
this is read by somebody trying to understand a person.

Norms this folder owns: a warning from the traceability check that survives
two versions either becomes an error or gets deleted; current state unless
the title says otherwise.
EOF

cat > specs/workflows/sowing-a-batch.feature <<'EOF'
@workflow:sowing-a-batch @persona:allotment-keeper @journey:growing-a-season
Feature: Sow a batch and get it into the diary

  When the seeds are in the compost and the label is still blank,
  I want the batch in the diary with today's date before I forget which tray,
  so that in May I can tell twelve identical trays apart.

  **Ends when** the batch is at the top of the diary, dated today.

  **Done well.** One hand, soil on the other. Less time than the label takes.

  **Where it breaks.** The phone is indoors and the seeds are outdoors; the
  batch gets recorded that evening, or never.

  Example: a batch is recorded at the windowsill
    Given the diary is open
    When they record "leeks, tray 2"
    Then "leeks, tray 2" is at the top of the diary, sown today

  Example: it survives being closed
    Given "leeks, tray 2" was recorded
    When they come back to the diary
    Then "leeks, tray 2" is exactly as left
EOF

cat > specs/workflows/checking-the-bed.feature <<'EOF'
@workflow:checking-the-bed @persona:allotment-keeper @journey:growing-a-season
Feature: Walk the plot and make the diary match it

  When I am at the plot and can see what has come up and what has not,
  I want each batch marked up, out or failed while I am looking at it,
  so that the diary tells the truth about the plot, not about my hopes.

  **Ends when** every batch in the diary matches what is in front of them.

  **Done well.** On the phone, at the bed, one tap per batch.

  **Where it breaks.** A batch nobody recorded cannot be marked. A tray
  that failed quietly stays "sown" for weeks.

  Example: something is up
    Given "leeks, tray 2" is sown
    When they mark it up
    Then it shows up, dated today

  Example: nothing came
    Given "parsnips, bed 3" is sown
    When they mark it failed
    Then it shows failed and stays in the diary
EOF

cat > specs/journeys/growing-a-season.md <<'EOF'
@journey:growing-a-season @persona:allotment-keeper

# Growing a season

The arc for the allotment keeper. It is made of the workflows below, in the
order they are usually reached.

## Workflows in this journey

| workflow | phase | what it carries |
|---|---|---|
| `keeping-the-diary` | February to June | the diary sitting: what went in, what came up |
| `keeping-the-diary` | June to September | the same sitting, with planting out |

## Rules touched

- `@rule:batch-goes-to-top` — the diary is newest first
- `@rule:batch-carries-its-date` — every batch is dated
- `@rule:state-moves-forward` — sown, up, out
- `@rule:failed-stays-in-the-diary`

## Phases

- **Sowing** — trays on the windowsill, then rows in the beds. Covered by
  `keeping-the-diary`.
- **Checking** — walking the plot. Covered by `keeping-the-diary`.
- **Clearing** — no workflow yet.

## Notes

Written from the workflows folder by Priya, 2026-05-02, without asking the
keeper. Update the ids here when the workflows are renamed.
EOF

git init -q -b main
git -c user.email=rowan@sowlog.example -c user.name="Rowan" add -A
GIT_AUTHOR_DATE=2026-07-03T21:40:00 GIT_COMMITTER_DATE=2026-07-03T21:40:00 \
  git -c user.email=rowan@sowlog.example -c user.name="Rowan" commit -qm "0002: mark a batch on"
