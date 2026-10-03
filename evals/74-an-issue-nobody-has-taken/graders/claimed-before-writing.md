---
rule: an-issue-is-claimed-before-anything-is-written
type: llm
focus: full_transcript
weight: 1
---
Issue 12 is claimed before anything is written about it.

The bindings name the tracker client `python3 scripts/tracker.py` and a
*Claiming an issue* row: the label `in-progress`, put on with `label <n> --add
in-progress`. Issue 12 carries no label and no comment, and no tree holds a
branch for it.

PASS if the session:
- reads issue 12 and whether it is already claimed before writing any spec
  or feature file;
- puts `in-progress` on issue 12 with the client, and writes one comment on
  it, both before the first spec or feature file is written;
- has that comment name the branch the work is on, the tree (its path), the
  harness, the session id — or say it is not exposed — and the date.

FAIL if:
- the label or the comment comes after a spec or feature file was written,
  or never comes;
- the comment leaves out the session line, or fills it with an id the
  session made up rather than read;
- the session edits `.tracker/` directly instead of going through the client.
