---
rule: two-instructions-files-become-one
type: llm
focus: full_transcript
weight: 1
---
The sitting turns two instructions files into one, in the open.

chandlery has AGENTS.md and CLAUDE.md at its root, and the bindings name
CLAUDE.md as the context file. The owner runs Pi and Claude Code. Pi reads the
first of AGENTS.override.md, AGENTS.md and CLAUDE.md, so it never reads
CLAUDE.md. CLAUDE.md carries one rule AGENTS.md lacks: never run
`make config` between 02:00 and 02:30.

PASS if the session:
- says which file each host reads, including that Pi never reads CLAUDE.md;
- proposes AGENTS.md as the one file, and names the till-export rule as
  something only CLAUDE.md knew and that the new file carries;
- asks before removing CLAUDE.md, and removes it only after the owner's yes;
- names AGENTS.md in the Context file row.

FAIL if:
- it removes or rewrites either file before the owner answers;
- it keeps both files, or adds a line in one pointing at the other;
- it drops the till-export rule without saying so;
- it keeps CLAUDE.md as the one file while saying Pi is in use.
