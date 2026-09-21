# Spec 0066: a claim is a grader that can fail

- **Status:** approved — built on the maintainer's *you must have full rules coverage in evals and ensure that skills execute them correctly*, 2026-09-21
- **Issue:** none filed; the instruction above is the report.
- **Depends on:** [`0058`](0058-a-case-is-a-sitting-not-a-turn.md), whose
  sittings are what make a grader's verdict about the skill.

## Who this is for

The maintainer at step 4, reading the board and asking what a rule's number
means. Until now *coverage* meant a `rule:` tag on a case: the traceability
gate fails a live rule no case claims, and stops there. A case claiming nine
rules with ten graders said nothing about which grader would fail if one of
the nine were broken — and five fire cases (`01`, `03`, `04`, `05`, `10`)
claimed no rule at all, grading behaviour the spec never promised.

## The job behind the request

Coverage that can be read is a grader that fails when the rule is broken.
So every grader says which rule it tests, the suite gate holds a case's claims
to its graders both ways, and the behaviour five cases have been grading gets
the rules it was missing.

## What changes

1. **[`caselib.py`](../../.github/scripts/caselib.py)** reads `rule: <id>` or
   `rules: [a, b]` from a grader's frontmatter into `grader["rules"]`, and
   marks the plugin-fired indicator, which is in neither arm's score.
2. **[`evalsuite.py`](../../.github/scripts/evalsuite.py)** fails a case that
   claims a rule no grader names, and a grader that names a rule its case does
   not claim. A grader naming none is a guard — `no-source-edits` — and never
   coverage. Two faults in [`inject.py`](../../.github/scripts/inject.py):
   119 becomes 121.
3. **Every grader in the suite names its rule**: 115 annotated, the
   multi-rule cases read grader by grader; `02` gains the claim its
   *files-rather-than-fixes* grader was already testing.
4. **Five rules the suite was grading without a promise**, in
   `specs/features/refining/`: `the-job-is-found-under-the-request` (`01`),
   `a-persona-invented-to-fit-a-feature-is-refused` (`03`),
   `a-workflow-invented-for-an-orphan-feature-is-refused` (`04`),
   `an-arc-with-no-seam-is-refused` (`05`),
   `a-twice-deferred-row-stops-the-workflow` (`10`). Live on arrival: the
   cases exist and their graders now name them. 100 live rules become 105.
5. **Words**: `evals/README.md`'s floor bullet, and the bindings' *Rule
   claiming* row and fault record.

**Rules changed: five added, none moved.** Nothing ships — no label. The
`.feature` files move, so the pull request carries the Gherkin; `evals/` and
`.github/scripts/` move, so it carries the run.

## What we are not doing

- **Not a rule for every guard.** `separates-the-implicit` on `02` grades
  something `todo` does that no rule promises; it stays a guard until a rule
  is written for it, and the list of such graders is one query away.
- **Not re-measuring here.** A `rule:` line is in each case's inputs hash, so
  every row stales; the after-sitting running today measures the skills, not
  the annotations, and its verdicts are read the same.

## Acceptance checks

1. `evalsuite.py` green over the suite; 121 faults; `trace.py` reads 105.
2. Removing `rule:` from any one grader of a single-rule case fails the
   suite gate naming the case and the rule.
