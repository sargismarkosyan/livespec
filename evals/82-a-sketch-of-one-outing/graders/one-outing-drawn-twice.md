---
rule: a-sketch-draws-one-instance-twice
type: llm
focus: full_transcript
weight: 1
---
The sketch shows the change on one real outing, drawn twice the same way.

The session cannot publish a page, so it writes the sketch as an HTML file.
Read that file's content in the transcript (the Write call).

PASS if the page:
- draws one outing (or the log holding it) as it is now, as part of one long
  list, and as it would be, as one block with its date and starting place,
  in two frames laid out alike;
- writes its counts as sentences under the frames, in fieldnote's words
  (outings, sightings, walks), not as numbers standing alone in tiles;
- carries at most one line above the evidence, about what changes;
- uses fieldnote's own words. None of the reference template's example
  survives: no Ana, no crash on export, no spec 0012, no tracker contract
  test.

FAIL if:
- no page is written;
- before and after are two unrelated blocks rather than the same thing drawn
  twice;
- the page is mostly metric tiles and tables;
- the template's example content is still in it.
