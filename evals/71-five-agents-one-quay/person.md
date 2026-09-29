---
replies: 3
---
I own quayside. Answer what a session asks from this and nothing else.

- Yes — go ahead; I'll stop you if I disagree.
- What we build: quay bookings for one harbour office, with photos of the
  berth uploaded against each booking. A version's deliverable is a still of
  the booking page when it moves; nothing when it does not.
- Who it is for: the harbour office staff. Not the boat owners.
- Verification: `make check`; coverage over `src/quayside/`, all of it.
- What it talks to, if asked: PostgreSQL, started by `make db` in a container
  on my machine. Whether a session here can start it: I don't know.
- Parallel work, if asked: up to five agents at once, one worktree each,
  sometimes under Pi and sometimes under Claude Code. They can all use the one
  Postgres container — I don't want five. Each needs its own database on it:
  two trees writing the same database is not OK. Each needs its own port, so
  two builds can run side by side. The API key is the same for everyone.
- Tracker: GitHub Issues on this repository.
- A pre-push hook: yes, the fast half only.
- Anything not on this list: your call.
