---
type: llm
focus: full_transcript
weight: 1
---
`src/legacy/` and `src/generated/` are named as reaching no exclusion and no
gate, and the list of them in the bindings is reported as being in the wrong
file.

Both are inside `include: ["src/**/*.js"]`, so both are measured, and they are
most of what the demand leaves behind — `legacy/ics.js` at 38.46% of branches,
`generated/timezones.js` at 71.42%. What the bindings carry is a *What coverage
does not cover* section naming both, with honest reasons, that nothing the
coverage tool reads has ever seen.

PASS if the reply reports that the exclusions live in the bindings' prose while
the coverage config excludes nothing — a second copy of the gate, a list the
runner never reads, two records that disagree the first time either moves, in
whatever words.

PASS if the part of the repository at no address is named concretely: the two
directories, or the uncovered branches they hold, as code that is neither
covered nor excluded nor written off anywhere a build can see.

PASS if the fix is put as a choice for the sitting that wires it — exclude them
in the config with the reason, or cover them — rather than as an edit this
session makes.

FAIL if the prose list is read as settling the question, so the audit reports
that what is not covered is already documented.

FAIL if neither directory is mentioned, leaving the demand reported as low with
nothing said about which code it leaves unaddressed.
