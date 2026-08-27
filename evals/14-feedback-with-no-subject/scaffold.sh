#!/usr/bin/env bash
# The fixture for 14: a repository that adopted the process, so that the
# question the case grades — this repository's tracker, or the plugin's — has
# two real answers instead of being asked about an empty directory.
#
# What is here: bindings naming its own GitHub tracker, a spec layer with the
# undo rule the app violates, and the violation itself in `src/shelf.js` —
# `render()` clears the undo buffer that `remove()` just filled, so removing
# works and undoing never does. That is the bug the mis-titled issue is really
# about, and spec 0003 is where the clearing came from.
#
# What is deliberately absent: anything saying **who wrote the bad title**. The
# bindings say some issues here are typed by hand and some are written by the
# tooling, and no case grants a shell, so the tracker cannot be read from here
# to settle it. Also absent: the issue itself in any local form — nothing here
# mirrors the tracker.
#
# The word the bindings do NOT use is `feedback`. The first measurement (Δ
# −0.33) named the skill in that row, and the without-plugin arm read it as an
# instruction: it tried to call `Skill(feedback)`, was told the name is a UI
# command, and the one bare run that passed reached the second destination by
# quoting the row back. A fixture is laid down in both arms alike, so anything
# in it that names the plugin's machinery is handed to the baseline too.
set -euo pipefail

mkdir -p specs/setup specs/features/shelf specs/workflows specs/changes docs/feedback src

cat > CLAUDE.md <<'EOF'
# shelf

Things one person meant to read, kept in the browser's local storage. No
accounts, no server, no build step — open `index.html`. `specs/` is the
contract: read `specs/setup/README.md` before assuming any command, and spec
before code. What we find while using it gets filed, not fixed on the spot.
EOF

cat > specs/setup/README.md <<'EOF'
# Bindings

| | |
|---|---|
| **Where the app runs** | open `index.html` in a browser; no build step |
| **Tracker** | GitHub `acme/shelf`, filed with `gh`. Findings get filed rather than fixed — some issues are typed by hand, some are written by the tooling |
| **Stored state** | localStorage key `shelf`; the shape is in `specs/spec.md` |
| **Screenshot home** | `docs/feedback/`, committed and pushed |
| **Tests** | none yet — the suite is a coming infrastructure change |
| **Change specs** | `specs/changes/NNNN-<slug>.md`, numbered one past the highest |
EOF

cat > specs/spec.md <<'EOF'
# shelf

Things one person meant to read, kept where they will see them again. An
**item** is a title and a link, either **unread** or **read**. **Removing** one
takes it off the shelf; a removal can be **undone**, and the shelf holds the
last one removed until something else is removed or the page is reloaded.

Storage: localStorage key `shelf`, a JSON array of
`{ "title": string, "url": string, "state": "unread" | "read" }`.

What it is not: a bookmark manager, a read-it-later service with a backend, or
anything shared. One person, one browser.
EOF

cat > specs/workflows/clearing-the-shelf.feature <<'EOF'
@workflow:clearing-the-shelf @persona:one-person-shelf
Feature: Clearing the shelf

  The weekend attempt: open the shelf, read or remove what is on it, and put
  back anything that came off by mistake. Done when nothing on it is stale.

  Example: something removed by mistake goes back
    Given an item was just removed
    When they undo
    Then it is back on the shelf, where it was
EOF

cat > specs/features/shelf/removing.feature <<'EOF'
@feature:removing @workflow:clearing-the-shelf
Feature: Removing an item, and putting it back

  @rule:remove-takes-it-off-the-shelf
  Rule: removing an item takes it off the shelf and out of storage

    Example: still gone after a reload
      Given "The mess we're in" is on the shelf
      When they remove it
      Then it is off the shelf, and still off after a reload

  @rule:undo-restores-the-last-removal
  Rule: the last removal can be undone until something else is removed

    Example: put back where it was
      Given three items and the middle one is removed
      When they undo
      Then the middle one is back between the other two

    Example: the buffer does not survive a reload
      Given an item was removed
      When the page is reloaded
      Then undo does nothing, because nothing is held any more
EOF

cat > specs/changes/0001-the-shelf-on-one-screen.md <<'EOF'
# Spec 0001: the shelf on one screen

- **Status:** shipped

The first slice of `clearing-the-shelf`: the stored items rendered as a list —
title linking out, unread above read. Local storage only, no build step.
EOF

cat > specs/changes/0002-remove-and-undo.md <<'EOF'
# Spec 0002: remove, and undo the removal

- **Status:** shipped

Removing an item takes it off the shelf and out of storage. Because the button
sits next to the link, a removal is easy to hit by mistake, so the shelf holds
the last one removed and an Undo puts it back where it was.
EOF

cat > specs/changes/0003-the-undo-buffer-does-not-survive-a-reload.md <<'EOF'
# Spec 0003: the undo buffer does not survive a reload

- **Status:** shipped

A held removal from an hour ago is not something anyone means to undo. The
buffer is cleared when the page is loaded, so Undo does nothing on a shelf
nobody has removed anything from this sitting.
EOF

cat > docs/feedback/.gitkeep <<'EOF'
EOF

cat > index.html <<'EOF'
<!doctype html>
<meta charset="utf-8">
<title>shelf</title>
<body>
  <ul id="shelf"></ul>
  <button id="undo">Undo remove</button>
  <script src="src/shelf.js"></script>
</body>
EOF

cat > src/shelf.js <<'EOF'
const KEY = "shelf";

const SEED = [
  { title: "The mess we're in", url: "https://example.com/mess", state: "unread" },
  { title: "A short history of the undo button", url: "https://example.com/undo", state: "unread" },
  { title: "Notes on local storage", url: "https://example.com/storage", state: "read" },
];

const load = () => JSON.parse(localStorage.getItem(KEY) || "null") || SEED;
const save = (items) => localStorage.setItem(KEY, JSON.stringify(items));

let held = null;

function remove(index) {
  const items = load();
  held = { item: items[index], index };
  items.splice(index, 1);
  save(items);
  render();
}

function undo() {
  if (!held) return;
  const items = load();
  items.splice(held.index, 0, held.item);
  save(items);
  held = null;
  render();
}

function render() {
  held = null; // 0003: a held removal must not survive a reload
  const list = document.getElementById("shelf");
  list.innerHTML = "";
  const items = load();
  items.forEach((item, index) => {
    const row = document.createElement("li");
    row.innerHTML = `<a href="${item.url}">${item.title}</a> <span>${item.state}</span> `;
    const button = document.createElement("button");
    button.textContent = "Remove";
    button.onclick = () => remove(index);
    row.append(button);
    list.append(row);
  });
}

document.getElementById("undo").onclick = undo;
render();
EOF

git init -q -b main
git add -A
git -c user.email=nils@example.com -c user.name="Nils Bergström" \
    commit -q -m "the undo buffer does not survive a reload (spec 0003)"
git remote add origin git@github.com:acme/shelf.git
