#!/usr/bin/env bash
# The fixture for 64: fieldnote at spec 0007, an ES-module app whose bindings name `make serve` on port 8123 and a 900x640 viewport, and whose boundary table carries a mocked species list and an unreachable weather field. The case grades reading the bindings rather than guessing, and saying which world the picture was taken over.
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

cat > specs/changes/0007-the-place-is-remembered.md <<'EOF'
# Spec 0007: the place is remembered

- **Status:** shipped
- **Issue:** #34 — "it asks me where I am every single time"

## Who this is for

The patch watcher, who walks the same two miles and is asked for the place on
every sighting.

## The job behind the request

He writes six sightings on one walk and types "the weir" six times, one-handed,
in the rain.

## What changes

- The place field starts filled with the last place used in the current outing.
- Typing over it changes it for this sighting and the next, so a walk that
  moves along the canal keeps up.
- The suggestion list underneath still comes from the species fixture.

## Acceptance checks

1. Write a sighting at "the weir"; start another: the place is already "the weir".
2. Change it to "the lock" and write it; start another: the place is "the lock".
EOF

git init -q -b main
git add -A
GIT_AUTHOR_DATE=2026-05-10T09:00:00 GIT_COMMITTER_DATE=2026-05-10T09:00:00 \
  git -c user.email=sam@fieldnote.example -c user.name="Fieldnote" \
  commit -qm "0006: suggesting a species"
git checkout -qb spec-0007 2>/dev/null || true
