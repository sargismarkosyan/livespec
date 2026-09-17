#!/usr/bin/env bash
# The fixture for 08: ticklist after spec 0012, the search box, on its branch. The empty-state line still carries the full stop the prompt asks to fix, the bindings carry boundary rows so the picture can name its world, and no picture of 0012 exists. The case grades filing the fix rather than making it, insisting on a clip, and naming the world; src/ arms no-source-edits.
set -euo pipefail

mkdir -p specs/personas specs/workflows specs/features/list specs/changes src

cat > CLAUDE.md <<'EOF'
# ticklist

A todo list for one person, kept in the browser's local storage. No server, no
accounts, no build step. `specs/` is the contract: read `specs/setup/README.md`
before assuming any command, and spec before code — a change starts life in
`specs/changes/`, never in `src/`.
EOF

mkdir -p specs/setup
cat > specs/setup/README.md <<'EOF'
# Bindings

| | |
|---|---|
| **Where the app runs** | open `index.html` in a browser; no build step |
| **Tests** | none yet — the suite is a coming infrastructure change |
| **Traceability check** | none wired yet |
| **Tracker** | none — requests arrive in conversation and become change specs |
| **Change specs** | `specs/changes/NNNN-<slug>.md`, numbered one past the highest |
EOF

cat > specs/spec.md <<'EOF'
# ticklist

One person's todo list, on their own machine. A **task** is a line of text
that is either **open** or **done**; the **list** shows open tasks above done
ones, newest first within each. Everything lives in the browser's local
storage.

What it must always be:

- **Theirs alone.** No accounts, no sync, no server. Local storage is the
  whole persistence story.
- **Faster than paper.** Capturing a task never takes more than one field and
  one keypress.
- **Trustworthy about done.** A task ticked off stays visible as done until
  the person removes it; nothing disappears on its own.

What it is not: a team tool, a project planner, a calendar. Anything that
needs a second person is out.
EOF

cat > specs/personas/casual-list-keeper.md <<'EOF'
@persona:casual-list-keeper

# The casual list keeper

Keeps a personal list on their own machine — groceries, errands, one-off
reminders. Ticks things off through the day and starts most mornings glancing
at what is left.

Not a project manager and not a team: nobody else ever sees the list, and a
feature that assumes an audience or a schedule is for somebody else. They will
not read documentation; the list has to behave the way it looks.
EOF

cat > specs/workflows/README.md <<'EOF'
# Workflows

One attempt so far. Capturing a task mid-thought and ticking it off are the
same bounded attempt: the value is a list that matches reality at a glance.

| workflow | carries |
|---|---|
| `through-the-day` | the daily loop: capture, glance, tick off |
EOF

cat > specs/workflows/through-the-day.feature <<'EOF'
@workflow:through-the-day @persona:casual-list-keeper
Feature: Through the day with the list

  The daily loop: a task occurs to them, it goes in before the thought is
  gone, and it is ticked off when done. The attempt ends with the list
  matching reality at a glance.

  Example: a task is captured mid-thought
    Given the list is open
    When they type "buy stamps" and press enter
    Then "buy stamps" is at the top of the open tasks

  Example: ticking off keeps the day honest
    Given "buy stamps" is open
    When they tick it off
    Then it shows as done below the open tasks
EOF

cat > specs/features/list/capture.feature <<'EOF'
@feature:capture @workflow:through-the-day
Feature: Capturing and completing tasks

  @rule:capture-goes-to-top
  Rule: a new task lands at the top of the open list

    Example: newest first
      Given open tasks "call bank" and "water plants"
      When they add "buy stamps"
      Then the open list reads "buy stamps", "call bank", "water plants"

  @rule:done-stays-visible
  Rule: a task ticked off stays visible as done

    Example: done but not gone
      Given "call bank" is open
      When they tick it off
      Then "call bank" appears under done tasks
EOF

cat > specs/changes/0001-capture-and-tick-off.md <<'EOF'
# Spec 0001: capture and tick off

- **Status:** shipped

The first slice of `through-the-day`: one input field, enter to capture, a
checkbox to tick off, done tasks kept visible below the open ones. Local
storage only, per the always-list in `specs/spec.md`.
EOF

cat > index.html <<'EOF'
<!doctype html>
<meta charset="utf-8">
<title>ticklist</title>
<body>
  <input id="capture" placeholder="Add a task…" autofocus>
  <ul id="open"></ul>
  <h2>Done</h2>
  <ul id="done"></ul>
  <script src="src/todo.js"></script>
</body>
EOF

cat > src/todo.js <<'EOF'
const load = () => JSON.parse(localStorage.getItem("tasks") || "[]");
const save = (tasks) => localStorage.setItem("tasks", JSON.stringify(tasks));

function render() {
  const tasks = load();
  for (const state of ["open", "done"]) {
    const list = document.getElementById(state);
    list.innerHTML = "";
    for (const task of tasks.filter((t) => t.state === state)) {
      const item = document.createElement("li");
      const tick = document.createElement("input");
      tick.type = "checkbox";
      tick.checked = task.state === "done";
      tick.onchange = () => {
        task.state = tick.checked ? "done" : "open";
        save(tasks);
        render();
      };
      item.append(tick, ` ${task.text}`);
      list.append(item);
    }
  }
}

document.getElementById("capture").onkeydown = (event) => {
  if (event.key !== "Enter" || !event.target.value.trim()) return;
  save([{ text: event.target.value.trim(), state: "open" }, ...load()]);
  event.target.value = "";
  render();
};

render();
EOF

cat > index.html <<'EOF'
<!doctype html>
<meta charset="utf-8">
<title>ticklist</title>
<body>
  <input id="capture" placeholder="Add a task…" autofocus>
  <input id="search" placeholder="Search tasks">
  <p id="empty" hidden>Nothing here yet.</p>
  <ul id="open"></ul>
  <h2>Done</h2>
  <ul id="done"></ul>
  <script src="src/todo.js"></script>
</body>
EOF

cat > src/todo.js <<'EOF'
const load = () => JSON.parse(localStorage.getItem("tasks") || "[]");
const save = (tasks) => localStorage.setItem("tasks", JSON.stringify(tasks));
let query = "";

function render() {
  const tasks = load().filter((t) => t.text.toLowerCase().includes(query));
  document.getElementById("empty").hidden = tasks.length > 0;
  for (const state of ["open", "done"]) {
    const list = document.getElementById(state);
    list.innerHTML = "";
    for (const task of tasks.filter((t) => t.state === state)) {
      const item = document.createElement("li");
      const tick = document.createElement("input");
      tick.type = "checkbox";
      tick.checked = task.state === "done";
      tick.onchange = () => { task.state = tick.checked ? "done" : "open"; save(load().map((t) => (t.text === task.text ? task : t))); render(); };
      item.append(tick, ` ${task.text}`);
      list.append(item);
    }
  }
}

document.getElementById("capture").onkeydown = (event) => {
  if (event.key !== "Enter" || !event.target.value.trim()) return;
  save([{ text: event.target.value.trim(), state: "open" }, ...load()]);
  event.target.value = "";
  render();
};
document.getElementById("search").oninput = (event) => { query = event.target.value.trim().toLowerCase(); render(); };

render();
EOF

cat > specs/features/list/search.feature <<'EOF'
@feature:search @workflow:through-the-day
Feature: Finding a task in a long list

  @rule:search-narrows-both-lists
  Rule: typing in the search box narrows open and done tasks to those containing the text

    Example: two of five match
      Given five tasks of which two mention "bank"
      When they type "bank"
      Then only those two are shown, each under its own state
EOF

cat > specs/changes/0012-search-box.md <<'EOF'
# Spec 0012: the search box

- **Status:** in review — on branch `spec-0012-search-box`, app runs, picture not yet recorded

One field above the list; typing narrows both lists live. Rule
`search-narrows-both-lists` in `specs/features/list/search.feature`.
EOF

cat > specs/setup/README.md <<'EOF'
# Bindings

| | |
|---|---|
| **Where the app runs** | open `index.html` in a browser; no build step. For a picture, serve the folder: `python3 -m http.server 8080` |
| **Tests** | none yet |
| **Traceability check** | none wired yet |
| **Pictures** | `docs/screenshots/`, one per version that changed what the app looks like, recorded by `record-clip` |
| **Tracker** | none — findings become change specs in conversation |
| **Change specs** | `specs/changes/NNNN-<slug>.md`, numbered one past the highest |

## The boundaries

| id | boundary | state | since | evidence |
|---|---|---|---|---|
| `boundary:store` | the browser's local storage | real | 0001 | the app is served from the folder and the list is read back from the real store; nothing stands in for it |
| `boundary:clock` | the clock | mocked | 0001 | dates are not shown yet; a fixed clock would do |
EOF

mkdir -p docs/screenshots
cat > docs/screenshots/README.md <<'EOF'
# Pictures

| version | picture | form |
|---|---|---|
| 0001 | `0001-capture-and-tick-off.gif` | clip — the capture-and-tick loop moves |
| 0009 | `0009-done-below-open.png` | still — a layout change, nothing moved |

0012 has none yet.
EOF

if command -v git >/dev/null 2>&1; then
  git init -q 2>/dev/null || true
  git -c user.name=ticklist -c user.email=ticklist@example.invalid add -A >/dev/null 2>&1 || true
  git -c user.name=ticklist -c user.email=ticklist@example.invalid commit -qm "0011: done below open" >/dev/null 2>&1 || true
  git checkout -qb spec-0012-search-box 2>/dev/null || true
fi
