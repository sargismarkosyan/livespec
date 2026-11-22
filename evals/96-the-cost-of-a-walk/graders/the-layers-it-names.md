---
rule: each-layer-holds-the-other-side-fixed
type: llm
focus: full_transcript
weight: 1
---
printshop is a browser front end (`src/`) and its own Node server
(`server.js`, `/api/prints` and `/api/orders`). Each layer is measured with
what it does not control held still.

PASS if what was written or proposed:
- measures the front end with the server's answers replayed or stubbed at a
  fixed delay (Playwright's HAR replay or route stubs, or the like), so a
  slower server cannot move the front end's numbers;
- measures the server's two endpoints without a browser;
- measures the whole walk too, as its own end-to-end line;
- names the layers in the bindings, and has each sample carry its `layer`.

FAIL if only the whole walk is measured, if the front end's numbers include
the real server's time with no layer that holds it fixed, or if the three are
folded into one line of the report.
