---
replies: 3
---
I'm Priya, the tech lead on ledger-api. Answer what a session asks from this
and nothing else.

- Yes — go ahead with the list as you have it. Write the files; I'll read
  them after.
- What we build: the double-entry ledger service behind the finance
  dashboard. A version's deliverable here is a green `make test` and a line
  in the merge request saying what moved — there is no screen and nothing to
  film.
- Who it is for: the finance-platform engineers who post to it and read
  balances from it. Not the finance team; they see the dashboard, never this.
- Verification: `make test`, the unit suite, no database. `make test-db`
  needs `DATABASE_URL` and does not run here or in CI today. Coverage:
  measure `src/ledger/`; the whole of what is left after exclusions, and
  there is nothing to exclude yet.
- What it talks to: Postgres, and only Postgres. The unit suite fakes it;
  nothing here can start the real one. Write that down as it is.
- Tracker: our self-hosted GitLab at gitlab.internal.example — issues and
  merge requests both. Nothing on GitHub.
- A pre-push hook: yes, the fast half only.
- Anything not on this list: your call.
