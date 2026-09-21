---
replies: 3
---
I own penstock. Answer what a session asks from this and nothing else.

- Yes — everything on your list, CLAUDE.md included; write the files.
- What we build: flow logging for the penstock gauges, with an alarm when two
  gauges disagree. A version's deliverable is a green `make check` and the
  changelog line; nothing on a screen.
- Who it is for: the plant operators who read the alarm. Not the gauge vendors.
- Verification: `make check` — `pytest -q`; coverage over `src/penstock/`, all
  of it.
- What it talks to: the gauges, over serial, through a small reader. Nothing
  here can reach one; the tests use recorded readings. Write that down as it is.
- Tracker: GitHub Issues on `hillworks/penstock`.
- A pre-push hook: yes, the fast half only.
- Anything not on this list: your call.
