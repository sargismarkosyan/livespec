---
type: llm
focus: full_transcript
weight: 1
---
The session treats the red check as a symptom and audits the journey against
the history, rather than patching the id the check complained about.

PASS requires all of:

- It reads the git history of the workflows and the journeys folders and says,
  in the reply or the change spec, when the journey stopped being true: that
  the workflows were re-cut after the journey was written — the July split of
  one diary sitting into sowing and checking — and the journey was not touched
  since. Naming July, the 0003 change, or the commit that re-cut them all
  count; "it's out of date" with no when does not.
- It says what the drift is, not only when: the journey describes the season
  as one diary sitting repeated, and that attempt no longer exists as one.
  Saying it split into two attempts — recording and marking, or sowing at the
  windowsill and checking at the plot — is enough; a reply that only says the
  id is stale is not.
- The retired id `keeping-the-diary` comes out of the journey's prose rather
  than being replaced with the two new ids. A reply that "fixes" the check by
  swapping in `sowing-a-batch` and `checking-the-bed` fails, however green the
  check goes.

FAIL if the check is made green by editing ids, if no date or commit for the
drift is given, or if the journey is rewritten from the workflows folder
without saying when it was last true.
