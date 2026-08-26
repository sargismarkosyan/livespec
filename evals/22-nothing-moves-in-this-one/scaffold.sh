#!/usr/bin/env bash
# The fixture for 22: perch, four versions in, with a static change on the branch.
#
# Everything record-clip needs to read is real — where the app runs, the viewport,
# where pictures go — so nothing forces a stall. What is deliberately shaped is
# the change spec: its *What changes* section describes the mechanism, and the
# issue it quotes describes the complaint. The two point at different shots.
set -euo pipefail

mkdir -p src specs/changes specs/setup docs/screenshots

cat > CLAUDE.md <<'EOF'
# perch

A browser app for keeping links in lists. `npm run dev` serves it.
`specs/` is the contract — spec before code, and `specs/setup/README.md` holds
anything true of *this* repository.
EOF

cat > package.json <<'EOF'
{
  "name": "perch",
  "private": true,
  "scripts": {
    "dev": "vite",
    "test": "vitest run"
  }
}
EOF

cat > specs/spec.md <<'EOF'
# perch

A **list** holds **links**. A link has a title, a url and a list it belongs to.
A link can be **archived**, which takes it out of the list without deleting it;
archived links stay reachable under *Archive* and keep the list they came from.

What it is not: a bookmarking service, a reader, or anything that fetches the
page behind a link.
EOF

cat > specs/setup/README.md <<'EOF'
# The bindings

Everything here is true of **this repository** and nothing else. Every skill
reads this file before it assumes a command.

## The table

| | |
|---|---|
| **Verification** | `npm test` |
| **Language** | JavaScript, Vite + Vitest |
| **Tracker** | GitHub Issues on `annike/perch`, via `gh` |
| **Where the app runs** | `npm run dev` — http://localhost:5173 |
| **Viewport for recordings** | 1280×800. Every version is recorded at that size |
| **Deliverable of a version** | one picture per version in `docs/screenshots/`, named for the change spec, embedded in the pull request body by a raw URL pinned to the commit |
EOF

cat > specs/changes/0031-how-long-has-it-been-archived.md <<'EOF'
# Spec 0031: how long has it been archived

- **Status:** approved
- **Issue:** [#84](https://github.com/annike/perch/issues/84)

## Who this is for

Somebody who archives constantly and comes back to the archive to dig something
out, weeks or months later.

## The job behind the request

From the issue, in their words:

> The archive is where things go to become identical. Everything in there has
> the same grey dot on it, so I cannot tell what I put away last Tuesday from
> what I put away in February. When I go looking for something I archived
> recently I end up opening things at random.

They are not asking to see a timestamp. They are asking to be able to tell
recent from old at a glance, in the list, without opening anything.

## What changes

- `ArchiveBadge` reads `link.archivedAt` instead of branching on
  `link.archived`, and formats it through the shared `formatDate` helper rather
  than carrying its own.
- The grey-dot branch is deleted, along with the `archived` boolean it read;
  `archivedAt` being set is now the only thing that means archived.
- The badge keeps its position and its size, so nothing in the card reflows.

## Acceptance checks

1. Archive a link and look at it in *Archive* — the badge carries a date.
2. An archive with links put away at different times reads as different at a
   glance, without opening any of them.
EOF

cat > src/ArchiveBadge.js <<'EOF'
import { formatDate } from "./formatDate.js";

export function ArchiveBadge({ archivedAt }) {
  const badge = document.createElement("span");
  badge.className = "badge badge--archived";
  badge.textContent = formatDate(archivedAt);
  badge.title = `Archived ${formatDate(archivedAt)}`;
  return badge;
}
EOF

cat > src/formatDate.js <<'EOF'
const MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

export function formatDate(iso) {
  const d = new Date(iso);
  return `${d.getDate()} ${MONTHS[d.getMonth()]}`;
}
EOF

cat > src/archive.js <<'EOF'
import { ArchiveBadge } from "./ArchiveBadge.js";

export function renderArchive(root, links) {
  root.replaceChildren();
  for (const link of links.filter((l) => l.archivedAt)) {
    const card = document.createElement("article");
    card.className = "card";

    const title = document.createElement("h3");
    title.textContent = link.title;
    card.append(title, ArchiveBadge(link));

    root.append(card);
  }
}
EOF

# The series so far. Two versions, two pictures, both moving — because both
# changes were things happening.
printf 'GIF89a' > docs/screenshots/v029-drag-a-link-between-lists.gif
printf 'GIF89a' > docs/screenshots/v030-undo-an-archive.gif

cat > docs/screenshots/README.md <<'EOF'
One picture per version, named for the change spec that shipped it. Nothing here
is ever deleted.
EOF

git init -q -b main
git add -A
git -c user.email=annike@example.com -c user.name="Annike Sepp" \
    commit -q -m "0031: an archived link carries the date it was archived"
git remote add origin git@github.com:annike/perch.git
