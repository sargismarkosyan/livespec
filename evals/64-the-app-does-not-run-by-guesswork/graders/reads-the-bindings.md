---
type: llm
focus: full_transcript
weight: 1
---
The app is served the way the repository says, and the picture is taken at the
size the repository says.

PASS requires all of:

- The session finds and uses the serve command from `specs/setup/README.md` —
  `make serve`, on port 8123 — rather than inventing one. Reading it out of
  the bindings is the point; a generic static server started on a port nobody
  named fails this even if it would have worked.
- It does not reach for `file://`. The app is ES modules and the bindings say
  so in the same row: opening the file directly renders a blank page. A
  session that plans to open `index.html` from disk fails.
- The viewport is the one the bindings name, 900 x 640, and the session says
  so — every version is recorded at one size or the series stops being one
  series.
- The instruction to "just open the app and grab it" does not become the
  method. Being told it is a one-line change is not a reason to skip the
  bindings.

FAIL if the serve command is guessed, if `file://` is planned, or if the
viewport is never established.
