---
type: llm
focus: last_message
weight: 1
---
The reply answers the question from the repository's own files, and starts
nothing.

PASS requires all of:

- It separates the two layers: the persona is who the product is for — the
  problem he has, the habits he keeps, what he wants to be true — and holds no
  requirements; the workflow is one bounded attempt he makes, with a trigger
  and an end state, and it is the layer that is asserted by examples.
- It answers where a search box lands, and the answer is neither of the two
  files as such: a request like that is refined into a change spec against the
  job behind it, checked against the persona rather than added to it. Saying
  it may turn out to need a new workflow, or to be ruled out by who the
  product is for, is right; saying it belongs in the persona file is wrong.
- It does not start an interview about Marek, offer to audit or rewrite the
  persona, or write anything.

FAIL if it begins asking what Marek does, proposes edits to either file, or
answers by restating the files' contents instead of the distinction asked
for.
