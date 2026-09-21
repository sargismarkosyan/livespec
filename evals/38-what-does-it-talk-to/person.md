---
replies: 3
---
I own tidewatch. Answer what a session asks from this and nothing else.

- Yes — go ahead; I'll stop you if I disagree.
- What we build: tide predictions and alerts for one coast, a small Python
  service. A version's deliverable is a green `make check` and the changelog
  line; nothing on a screen here.
- Who it is for: the harbour staff who read the alerts. Not the public.
- Verification: `make check`; coverage over `src/tidewatch/`, all of it.
- What it talks to, if asked: PostgreSQL for the readings, and Stripe for the
  subscription charges. Whether a test can reach the real thing from here:
  Postgres — `make db` starts it in a container on my machine, and I do not
  know whether a session here can; Stripe — the sandbox needs a key we keep
  out of this repository, so nothing here can reach it.
- Tracker: GitHub Issues on this repository.
- A pre-push hook: yes, the fast half only.
- Anything not on this list: your call.
