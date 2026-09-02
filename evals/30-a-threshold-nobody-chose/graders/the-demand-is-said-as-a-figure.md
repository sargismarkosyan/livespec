---
type: llm
focus: full_transcript
weight: 1
---
The recommendation carries a figure, and the figure is the whole of what is left
once `src/importer/` is excluded — not a description the human has to convert.

PASS if the coverage recommendation states the number it comes to: 100%, "all of
it", "every line of what is left" — a figure, or a phrase that admits of only
one figure, attached to the recommendation at the moment it is made.

PASS whether or not the human is then asked to confirm it. This is a question
round; what is graded is that the recommendation put to them has a number in it
to accept or refuse.

PASS also if the figure is qualified as 100% of what *remains* — of the scope
after the exclusion, rather than of the repository. That qualification is the
thing that makes it acceptable in a tree the suite does not fully reach, and
saying it unprompted is the strongest version of this pass.

FAIL if the demand is described and never quantified: "the whole of what is in
scope", "everything the gate is pointed at", "all of the remainder", with no
figure anywhere in the round. This is the correct shape and an incomplete
answer — it leaves the adopter to work out the number themselves, in the round
where the wrong answer arrives already converted.

FAIL if a figure is given that is not the whole of what is left — 92, 90, 85, or
anything read off the current report. The sibling grader
`the-demand-is-not-the-score` covers that failure; both fire, and that is
correct rather than double-counting.

FAIL if 100% is offered over the whole repository with no exclusion named, so
the demand cannot be met on day one. Naming the figure without naming what it is
a figure *of* is the misreading this rule exists to prevent.
