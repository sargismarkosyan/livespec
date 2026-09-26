---
type: llm
focus: full_transcript
weight: 1
---
The shot is composed for the person who asked, not for the person who wrote
the diff.

PASS requires all of:

- The sequence shows the log surviving something that used to lose it, and
  the count line saying what is held and when it was last written. Those are
  the two things the person who lost three weeks can read as "it is still
  there".
- It does not try to show the migration, IndexedDB, the storage layer or the
  `store.js` surface as such. Those are how the change was built, and the
  person holding the request would not know what they were looking at. Naming
  the migration in the hand-back as context is fine; building the shot around
  it is not.
- It reads the change spec for the shot list and the request for the standard:
  the issue is "I lost three weeks" and the job is to stop having to wonder.
- Enough of the before state is on screen for the after to read — sightings
  present, then the thing that used to empty them, then the sightings still
  there.

FAIL if the sequence is a walk through the internals, if it shows only that
the app still works with no reference to what was lost, or if the change spec
is never opened.
