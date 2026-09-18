---
replies: 3
---
I keep sluicegate. Answer what a session asks from this and nothing else.

- Yes — go on with the list; write the files as you go. Read CLAUDE.md
  properly first; every line in it is there for a reason.
- What we build: the lock-opening scheduler for the keepers on the canal. A
  version's deliverable is the public schedule page, moving — a keeper
  watching a slot open is the picture.
- Who it is for: the lock keepers who work the canal, on their phones at the
  lockside. Not the navigation authority; they get a report, not this.
- Verification: `make check` — pytest — and CI runs the same thing.
  Coverage: the whole of `src/sluicegate/`, all of what is left after
  exclusions; exclude nothing until something needs it.
- What it talks to: Postgres through the compose file, and the public
  internet on Fly. The suite runs over a real Postgres when `make db` is up
  and skips otherwise. Fly is unreachable from here.
- Issues: GitHub Issues on canalworks/sluicegate, as CONTRIBUTING.md says.
- A pre-push hook: yes, the quick half.
- Anything not on this list: your call.
