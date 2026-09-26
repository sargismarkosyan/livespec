#!/usr/bin/env bash
# The fixture for 63: fieldnote at spec 0007, where the flat log became outings and every screen moved. The case grades recording the tour through the workflows that carry the value rather than one corner of the change.
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

cat > specs/changes/0007-the-log-becomes-outings.md <<'EOF'
# Spec 0007: the log becomes outings

- **Status:** shipped
- **Issue:** none — from watching him use it

## Who this is for

The patch watcher. A flat list of four hundred sightings stopped being a log
of mornings and became a wall.

## The job behind the request

He thinks in walks, not in entries. "The morning I saw the kingfisher" is how
he finds anything, and the log had no idea a morning was a thing.

## What changes

- Sightings written within one walk group into an **outing**, headed by its
  date and place, and the log shows outings rather than loose lines.
- The empty state says what an outing is before there are any.
- Writing a sighting joins the open outing, or starts one if the last is more
  than three hours old.
- Opening an outing shows its sightings in the order they were written.
- `settling-a-question` searches within and across outings, and a result says
  which outing it came from.

This touches both workflows and every screen the app has.

## Acceptance checks

1. From empty, the message explains outings.
2. Write three sightings: they gather under one outing with its date.
3. Open the outing: the three are in the order written.
4. Search a species: the result names the outing it came from.
EOF

git init -q -b main
git add -A
GIT_AUTHOR_DATE=2026-05-10T09:00:00 GIT_COMMITTER_DATE=2026-05-10T09:00:00 \
  git -c user.email=sam@fieldnote.example -c user.name="Fieldnote" \
  commit -qm "0006: suggesting a species"
git checkout -qb spec-0007 2>/dev/null || true
