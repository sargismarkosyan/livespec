---
replies: 3
---
I'm on the on-call rota for beacon and I own it. Answer what a session asks
from this and nothing else.

- Yes — go ahead and write files.
- What we build: a daemon that tails log files and ships them to the sink. A
  version's deliverable is a green `make verify` and the changelog line —
  there is no screen and there never will be.
- Who it is for: the on-call engineer who needs the logs to have arrived. Not
  the people whose services write them.
- Verification: `make verify` — the traceability gate, then pytest with
  coverage. Coverage over the whole of the daemon; nothing excluded.
- What it talks to: the log sink, over HTTP, and the files it tails. Nothing
  here starts a real sink; write that down as it is.
- Tracker: GitHub Issues on this repository.
- A pre-push hook: yes, the fast half only.
- Anything not on this list: your call.
