---
rule: a-journey-says-where-it-goes-round
type: llm
focus: full_transcript
weight: 1
---
The arc's return is written as a way between two phases, not as a phase.

The map in the fixture runs *Before the log*, *The spring passage*, *Summer on
the patch*, *The quiet months*. The person says nothing ends after the quiet
months: he goes quiet, and then it is March again, and the first thing he
does is open last March.

PASS if the session:
- asks about the last time, and the gap between the seasons, before writing;
- plays the reading back before the file changes;
- writes one line under the map saying that from the quiet months (or
  whatever the last phase is now called) it goes back to the spring (or
  whatever the first recurring phase is now called), naming both;
- leaves *Before the log* out of the loop, since it happened once.

FAIL if:
- the loop becomes a column of the map — *The year turns*, *Next spring*,
  *Repeat* — or a second copy of the spring phase;
- the session asks the person to name the phases or lay out the map;
- the journey goes on reading as one pass that ends.
