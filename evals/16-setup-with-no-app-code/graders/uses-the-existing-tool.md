---
type: llm
focus: full_transcript
weight: 1
---
The suite comes from tooling that already builds one, not from an invented
format.

PASS if it reaches for the existing generator — `claude plugin eval init` is the
one for graded cases in a Claude Code plugin — or, where it cannot run the tool,
names it and says what it would produce rather than substituting a layout of its
own. Reading what the tool actually writes before describing it is a strong pass.

PASS also if, finding the tool gated or absent, it sets up a platform that
already runs graded suites rather than a format of its own — or stops and asks.

FAIL if it hand-rolls a case format — inventing directory names, a frontmatter
schema or a grader layout from scratch — while a tool that produces one exists.
A bespoke format has one user, no documentation, and nobody to ask.

FAIL if it sets up nothing at all for naming rules, leaving both gates with
nothing to read.
