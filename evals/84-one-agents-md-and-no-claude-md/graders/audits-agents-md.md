---
rule: the-sitting-names-the-context-file
type: llm
focus: full_transcript
weight: 1
---
The sitting audits the file the repository has, rather than asking for another.

chandlery's one instructions file is `AGENTS.md`. There is no `CLAUDE.md`, and
the bindings say "CLAUDE.md ceiling" and name no context file.

PASS if the session:
- finds that AGENTS.md is the instructions file, and reads it against the
  requirements in method/claude-md.md (requirement by requirement: met,
  missing, stale);
- writes a Context file row naming AGENTS.md, and points the ceiling row at
  AGENTS.md (relabelled or not);
- creates no CLAUDE.md, and does not propose one, not even as a pointer.

FAIL if:
- it writes a CLAUDE.md, or recommends adding one beside AGENTS.md;
- it reports the context file as missing;
- it audits nothing and only renames rows.
