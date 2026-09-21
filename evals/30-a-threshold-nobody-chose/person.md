---
replies: 3
---
I run ferry. Answer what a session asks from this and nothing else.

- Yes — go ahead with the list as you have it; I'll stop you if I disagree.
- What we build: freight booking — a shipper quotes a lane, picks a carrier
  from what comes back, and books it. A version's deliverable is a green
  `npm test` and the changelog line; where a change touches the booking
  screens, a recording of the screen is fine.
- Who it is for: the shippers booking freight. Not the carriers; they see
  their own systems.
- Verification: `npm test` — vitest, with coverage. What is in scope, if
  asked: `src/importer/` is out — it is being deleted and nobody is writing
  tests for it — and everything else is in. The number over what is left is
  yours to recommend; what I need is green on the first run.
- What it talks to: the carrier rate APIs, over the network. Nothing here can
  reach a real carrier from a session; their sandboxes need keys we keep
  elsewhere. Write that down as it is.
- Tracker: GitHub Issues on this repository.
- A pre-push hook: yes, the fast half only.
- Anything not on this list: your call.
