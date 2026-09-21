---
rule: a-dated-account-that-still-binds-is-not-history
type: llm
focus: full_transcript
weight: 1
---
The finished migration is named as history, with the version history and the
change specs as where it goes.

The section *How it got here* says the app was Flask and SQLite until March
2025, that the move finished in change 0011, and that `legacy/` was deleted in
0012. Nothing in it constrains the next change: the script ran once and is
gone, the directory is gone, and the one line about `schedule.py` surviving is
already said under *What is where*. By the method's test — does it still
change what the next change may do? — it is history.

PASS if the reading reports that section as history — or as belonging to
`git log`, the change specs, the version history, in any of those words — and
either removes it, offers its removal, or leaves it out of the rewritten file
with a line saying where the account lives instead.

FAIL if the section is reported as met or kept as a requirement satisfied — it
is not *where it lives*, and it is not *the rules that get broken here*; if it
is never mentioned; or if it is carried into the final file with no account
given, because a paragraph kept for having been there is the failure this case
exists to catch. FAIL also if the *Where it runs* paragraph is the one named as
history: the two have the same shape and only one of them binds.
