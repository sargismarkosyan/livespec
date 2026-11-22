---
rule: a-front-end-is-weighed-in-bytes-load-and-features
type: llm
focus: full_transcript
weight: 1
---
The front end is weighed three ways: the bytes it ships, how long the page
takes to load, and when each workflow's feature is ready.

PASS if the measures chosen include:
- the bytes the page ships, as a count (the request-count budget Ines takes
  may stand beside it);
- the page's load time, as a time;
- a ready time per workflow read from a mark the app sets itself — `src/app.js`
  already sets `printshop:list-shown` and `printshop:paid` with
  `performance.mark` — rather than from the test runner waiting for an element.

FAIL if feature times are taken from the runner's own waits when the app's
marks are there, or if any of the three is missing without a reason.
