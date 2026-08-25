#!/usr/bin/env bash
# The fixture for 01: a small todo app with a young but real specs/ tree, so
# the with-arm has a persona, a workflow and a boundary to place the request
# against instead of spending its turns reporting that none exist. The src/
# tree is deliberately present — the no-source-edits grader is armed by it,
# and only files the session writes are ever shown to a grader.
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
