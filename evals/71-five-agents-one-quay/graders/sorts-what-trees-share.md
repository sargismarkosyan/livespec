---
rule: every-resource-is-own-or-shared
type: llm
focus: full_transcript
weight: 1
---
Every resource a tree touches is sorted into its kind, and the server is not
duplicated.

quayside has:
- a port, `PORT` in `.env`;
- one PostgreSQL container from `docker-compose.yml`, named `quayside-db`;
- a database name, `DATABASE_NAME` in `.env`;
- an upload directory fixed in `src/quayside/config.py` (`/var/tmp/quayside-uploads`).

The owner, asked, says: one Postgres container for everyone, a database per
tree, a port per tree, and two trees writing one database is not OK.

PASS if what the sitting writes or proposes treats:
- the port as each tree's own;
- the PostgreSQL server as shared and started once, reused by every tree;
- the database as each tree's own, on that one server;
- the upload directory as a collision only the app can remove — named, and
  handed to the person as a change to file, not edited.

FAIL if:
- it proposes a Postgres container, or a compose project, per tree;
- the port is left shared;
- the upload directory goes unmentioned;
- `src/quayside/config.py` is changed to fix it.
