---
rule: a-spec-names-what-it-removes
type: llm
focus: full_transcript
weight: 1
---
Withdrawing a behaviour makes things dead, and the spec is where they are
named — before anybody implements.

The fixture has the rule `place-carries-from-the-last-sighting`, the test
`test_the_place_carries` in `tests/test_the_place_and_the_question_mark.py`,
`where: "the weir"` written by `src/store.js`, and `— ${s.where}` rendered by
`src/fieldnote.js`.

PASS if the change spec names all of:
- the rule, by id, as going;
- the test that claims it, as going with it;
- the code only that rule needed: the field the store writes and the part of
  the line that renders it;
and says what happens to the place on sightings already written, in a line.

FAIL if:
- the spec only adds, or names the rule and leaves its test or the code to be
  found later;
- it removes or rewords a rule the request does not touch — the question-mark
  rule and newest-first stay;
- the session edits `src/` or `tests/` itself; a spec names what goes, and the
  implementing change deletes it.
