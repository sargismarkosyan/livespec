---
rule: the-loop-reads-back-what-a-pull-request-closes
type: llm
focus: full_transcript
weight: 1
---
The loop's step that opens a merge request is read against claude-md.md and
rewritten so that what it opens closes what it names.

chandlery's AGENTS.md tells a session to open each merge request with
`Fixes [#N](<the issue's URL>)` and never a bare `#N`. The forge registers
nothing from a keyword followed by a Markdown link; it does register the
keyword followed by a bare `#N` or by the issue's full URL. The bindings name
the read-back: `python3 scripts/forge.py mr closes <n>`.

PASS if the session:
- reports the step stale (or behind) against claude-md.md's requirement for
  the loop, naming both halves: the Markdown-link form closes nothing here,
  and the step never reads back what the merge request will close;
- rewrites the step so the keyword sits straight before a bare reference or
  the issue's full URL — the full URL keeps the person's wish that a reader
  can click through;
- has the step read back with the bindings' command after opening, and fix an
  empty list (or a list naming the wrong issue) in the description and read
  again before the merge request is handed back.

FAIL if:
- the step still puts the keyword in front of a Markdown link;
- the read-back is missing, or names `gh` or `glab` rather than the bindings'
  command;
- the session drops linking altogether without saying the full URL both links
  and closes;
- a CLAUDE.md is written or proposed beside AGENTS.md.
