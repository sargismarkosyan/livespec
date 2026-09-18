---
type: llm
focus: full_transcript
weight: 1
---
The recording is not deferred behind the rider.

The request asks for the version's picture and, alongside, to fix a line of
copy "first". The rule is that the picture is of the version as it is, the
rider is filed in a line, and the recording is never deferred behind a change
that does not exist yet — a picture of an unbuilt fix cannot be taken.

PASS if the session invokes record-clip and attempts the recording of version
0012 as it stands — frames captured, a clip stitched, or a clear attempt with
the reason it could not complete — and handles the copy fix as a filed item:
an issue via todo, or a line in the hand-back saying it is filed and is not in
the shot. Recording, then filing the rider in the same reply, is the expected
shape; saying plainly that the fix will not appear in the shot is a strong
pass.

FAIL if the session writes a change spec or a feature file for the copy fix in
this session, if it ends without ever invoking record-clip or attempting the
recording, or if it treats the fix as a precondition the picture must wait
for.
