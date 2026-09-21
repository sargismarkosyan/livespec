# Spec 0063: the tool is named where the testing story is decided

- **Status:** approved — built on the maintainer's *merge all unmerged MR's and start actually improving*, 2026-09-21
- **Issue:** [#135](https://github.com/sargismarkosyan/livespec/issues/135) —
  `setup` hand-rolls a case format where the product is prose instead of
  reaching for `claude plugin eval init`. Three of three on the one-turn
  harness; at the floor with a person and a shell (the sitting of 2026-09-20,
  `16-setup-with-no-app-code`), one of three named the tool, one invented a
  layout, a tag schema and a grader script after the tool was refused.
- **Depends on:** [`0058`](0058-a-case-is-a-sitting-not-a-turn.md).

## Who this is for

[`agent-accelerated-owner`](../personas/agent-accelerated-owner.md), in
[`adopt-the-process`](../workflows/adopt-the-process.feature), setting the
process up in a repository whose product is prose — the desk's agent
instructions — where a rule is proved by grading what the instruction does
and there is no function to call. What they were handed on 2026-09-20 was
`evals/cases/*.yaml` with a `rule: rule:<id>` schema of its own and a
`tools/check_gates.py` that parses it, which one repository uses and nobody
documents.

**This lengthens nothing anybody types.** No always-promise moves; the
description does not move.

## The job behind the request

The skill names the tool once, 190 lines after the decision is made, under the
branch for repositories with code; §2's fifth question — what proves a rule
here — says *graded cases* and stops. A session decides the testing story in
§2 and is writing the bindings by §5, and a format it can write is nearer than
a tool it read about later and cannot run. The verdict of 2026-09-20: *every
attempt was blocked … rather than stopping there and naming the tool plus what
it would produce, it went on to invent its own case format from scratch.*

The job: **the tool is named at the moment the answer is graded cases, and
the fallback — the tool's format, run by a platform that already runs graded
suites — is named in the same breath, so that a tool the sitting cannot run
has settled the format rather than opened the question.**

## What changes

1. **[`skills/setup/SKILL.md`](../../skills/setup/SKILL.md) §2**, the fifth
   bullet: where the answer is graded cases, `claude plugin eval init <name>`
   is named there — cases as folders of a prompt and its graders — with the
   fallback in the same sentence, and *a case format of this repository's own
   is never the answer*.
2. **§5**, the graded-cases bullet: the fallback says what the tool's format
   is — a folder per case holding `prompt.md`, `case.yaml` and `graders/*.md`,
   the format this plugin's own `evals/` is in — and names the third thing
   that is never done.

**Rules changed: none.** `setup-scaffolds-the-rule-binding` already says it.
`patch`; the description does not move. Re-stales the setup cases.

## Acceptance checks

`16`'s `uses-the-existing-tool` at the floor, three of three, after this
lands; it read one of three before.
