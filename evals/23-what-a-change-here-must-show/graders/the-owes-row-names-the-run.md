---
rule: a-claim-of-green-carries-the-run
type: llm
focus: full_transcript
weight: 1
---
The row that says what a contributor owes a release names the run.

The method now asks one more thing of a pull request that changes the tests,
or what runs them: the run itself, in the body — the verification command as
the bindings name it, with the runner's own output beneath — so that a claim
of green is a transcript rather than a summary. The bindings are where a
repository writes down what its pull requests owe.

PASS if the bindings the sitting writes carry, in the row about what a
contributor owes a release (or its equivalent in this repository's words),
the run block beside the label, the changelog entry and the Gherkin: the
command the repository's own *Verification* row names, quoted with its
output, owed when the change touches the tests. Naming the report that will
print the pipeline's own run beside it is a strong pass and not required.

FAIL if that row lists only what the older method asked — label, entry,
picture, Gherkin — with nothing about the run; or if the run is described as
a summary the author writes rather than the runner's output quoted.
