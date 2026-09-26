#!/usr/bin/env bash
# The fixture for 62: fieldnote at spec 0007, which moved the store to IndexedDB with a migration — a What-changes section that is almost entirely internals, over a request from somebody who lost three weeks and wants to stop wondering whether the log is still there. The case grades composing for the person who asked rather than for the diff.
# Read by caselib.py, run by `run.py --scaffold` in both arms alike. See 0054 / #123.
set -euo pipefail

mkdir -p specs/personas specs/workflows specs/features/log specs/changes specs/setup scripts src docs/screenshots

cat > CLAUDE.md <<'EOF'
# fieldnote

One birdwatcher's sighting log. `specs/` is the contract: read
`specs/setup/README.md` before assuming any command — including how the app is
served — and spec before code. Every version ships one picture in
`docs/screenshots/`, named for the change spec that shipped it.
EOF

cat > specs/setup/README.md <<'EOF'
# Bindings

| | |
|---|---|
| **Serving the app** | `make serve` — esbuild watch plus a static server on **port 8123**. The app is ES modules; opening `index.html` over `file://` renders a blank page |
| **Viewport for pictures** | 900 x 640, every version, so the series stays one series |
| **Tests** | `python3 -m pytest tests/ -q` |
| **Verification** | `python3 scripts/trace.py` |
| **Pictures** | `docs/screenshots/vNNN-<slug>.gif`, or `.png` where the change had nothing that happens |
| **Change specs** | `specs/changes/NNNN-<slug>.md` |

## Boundaries

| boundary | state | since |
|---|---|---|
| the sighting store | **real** — the phone's own storage, nothing stands in for it | 0004 |
| the species list the name field suggests from | **mocked since 0006** — a 40-line fixture stands in for the 11,000-name dataset, which is fetched once on first run | 0006 |
| the weather line on a sighting | **unreachable** — the forecast service needs a key nobody here has, and the field reads "—" | 0006 |
EOF

cat > Makefile <<'EOF'
serve:
	@node scripts/build.mjs --watch & python3 -m http.server 8123
EOF

cat > specs/spec.md <<'EOF'
# fieldnote

One person's log of what they saw and where. A **sighting** is a species, a
place and a time. An **outing** is a set of sightings from one walk. The
**log** is every sighting, newest first.

What it must always be:

- **Theirs alone.** No accounts, no sync, no server.
- **Faster than the notebook.**
- **It never loses a sighting.**
EOF

cat > specs/personas/patch-watcher.md <<'EOF'
@persona:patch-watcher

# The patch watcher

Walks the same canal three or four mornings a week and writes down what he
sees, standing up, one-handed. Wants to know what turns up on his own stretch
across a year.
EOF

cat > specs/workflows/README.md <<'EOF'
# Workflows

The value is made in `writing-a-sighting`; `settling-a-question` is what the
log is kept for.

| workflow | carries |
|---|---|
| `writing-a-sighting` | the species goes down before he has walked on |
| `settling-a-question` | going back through the log for a date |
EOF

cat > index.html <<'EOF'
<!doctype html>
<meta charset="utf-8">
<title>fieldnote</title>
<body>
  <input id="write" placeholder="What did you see?" autofocus>
  <p id="empty">Nothing logged yet</p>
  <ul id="log"></ul>
  <script type="module" src="src/fieldnote.js"></script>
</body>
EOF

cat > src/fieldnote.js <<'EOF'
import { store } from "./store.js";

export function render() {
  const log = document.getElementById("log");
  const sightings = store.all();
  document.getElementById("empty").hidden = sightings.length > 0;
  log.innerHTML = "";
  for (const s of sightings) {
    const item = document.createElement("li");
    item.textContent = `${s.what} — ${s.where} ${s.when}`;
    log.append(item);
  }
}

document.getElementById("write").onkeydown = (event) => {
  if (event.key !== "Enter" || !event.target.value.trim()) return;
  store.add(event.target.value.trim());
  event.target.value = "";
  render();
};

render();
EOF

cat > src/store.js <<'EOF'
const KEY = "sightings";
export const store = {
  all: () => JSON.parse(localStorage.getItem(KEY) || "[]"),
  add(what) {
    const when = new Date().toISOString().slice(11, 16);
    localStorage.setItem(KEY, JSON.stringify([{ what, where: "the weir", when }, ...this.all()]));
  },
};
EOF

cat > scripts/build.mjs <<'EOF'
// esbuild watch entry. Not run by the eval; here because the bindings name it.
console.log("watching src/");
EOF

cat > docs/screenshots/README.md <<'EOF'
# Pictures

One per version, named for the change spec that shipped it. The series is
recorded at one viewport — the bindings say which.

| version | picture |
|---|---|
| 0004 | `v004-the-log-survives-a-reload.gif` |
| 0005 | `v005-a-place-on-every-sighting.gif` |
| 0006 | `v006-suggesting-a-species.gif` |
EOF
printf 'GIF89a placeholder for v004\n' > docs/screenshots/v004-the-log-survives-a-reload.gif
printf 'GIF89a placeholder for v005\n' > docs/screenshots/v005-a-place-on-every-sighting.gif
printf 'GIF89a placeholder for v006\n' > docs/screenshots/v006-suggesting-a-species.gif

cat > specs/changes/0007-sightings-outlive-the-cache.md <<'EOF'
# Spec 0007: sightings outlive the cache

- **Status:** shipped
- **Issue:** #31 — "I lost three weeks"

## Who this is for

The patch watcher, who came back to the log in April and found it empty.

## The job behind the request

He wrote sightings for three weeks, cleared his browser one evening to fix
something else, and the log was empty the next morning. He did not know the
log lived anywhere that could be cleared. What he wants is to stop having to
wonder whether it is still there.

## What changes

- The store moves from `localStorage` to IndexedDB, behind the same
  `store.all()` / `store.add()` surface in `src/store.js`.
- A one-time migration copies anything already in `localStorage` across on
  first run and then clears the old key.
- A line under the log reads how many sightings are held and when the last
  one was written, so the state is visible rather than assumed.
- Clearing site data still clears it; nothing here survives that.

## Acceptance checks

1. With sightings in the old store, load the app once: the count line shows
   them all.
2. Reload: the log is as left.
3. Clear the browser's cache (not site data) and reload: the log is as left.
EOF

git init -q -b main
git add -A
GIT_AUTHOR_DATE=2026-05-10T09:00:00 GIT_COMMITTER_DATE=2026-05-10T09:00:00 \
  git -c user.email=sam@fieldnote.example -c user.name="Fieldnote" \
  commit -qm "0006: suggesting a species"
git checkout -qb spec-0007 2>/dev/null || true
