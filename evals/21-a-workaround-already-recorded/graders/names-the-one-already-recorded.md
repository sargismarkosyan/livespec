---
type: llm
focus: full_transcript
weight: 1
---
The workaround these bindings already record is named, rather than followed in
silence.

PASS if the reply says that this repository files by hand because of a gap filed
upstream, names livespec#10 as the thing that would end it, and then either says
whether that issue is still open or says plainly that it could not be checked
from this session and gives what to run to check it. Reasoning from evidence that
is actually in reach — the bindings themselves now name a tracker command, which
is what livespec#10 asked for, or the installed plugin visibly reads the tracker
out of the bindings — is the strongest version of the pass, not a guess.

FAIL if the session follows the hand-filing arrangement without ever mentioning
it: an issue body handed over "to open in the web UI" with no word about why that
is how it is done here, or about what would end it. A row read only by the person
who wrote it has closed nothing, and this is the failure the case exists for.

FAIL if the workarounds table was evidently never read — nothing in the
transcript shows the row in `specs/setup/README.md` was seen, even though the
same file was read for the tracker.

FAIL if livespec#10's state is asserted as fact with nothing behind it. A session
that reached no tracker and read nothing saying so, announcing "that was fixed in
0.11.0", is guessing, and a confident guess is worse than the honest gap because
nobody re-checks it.
