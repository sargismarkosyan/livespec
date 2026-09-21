---
replies: 3
---
I own millrace. Answer what a session asks from this and nothing else.

- Yes — go ahead and write files. Except the CLAUDE.md: I wrote that one by
  hand, so show me the whole new file you propose and leave the one on disk as
  it is; I'll read it and say.
- What we build: it meters the water each mill draws from the race and bills
  the miller monthly. A version's deliverable is a green `make check` and the
  changelog line; `make dev` runs the service, but there is no screen worth
  recording.
- Who it is for: the mill owners who read their bills. Not the water board.
- Verification: `make check` — `pytest -q`; coverage over `src/millrace/`, all
  of it.
- What it talks to: the flow meters, over the network, and the Postgres it
  bills from. Neither is reachable from a session here; write that down as it is.
- Tracker: GitHub Issues on `leatworks/millrace`.
- A pre-push hook: yes, the fast half only.
- Anything not on this list: your call.
