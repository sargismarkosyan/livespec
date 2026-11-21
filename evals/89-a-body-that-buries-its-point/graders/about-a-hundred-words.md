---
rule: about-a-hundred-words-of-the-authors-own
type: command
command: 'python3 "$LIVESPEC_ROOT/evals/89-a-body-that-buries-its-point/check_body.py" length'
weight: 1
---
`pr-body.md` holds about a hundred words of the author's own, unfolded. The
count leaves out folded blocks, code blocks, headings, the picture and the
titles inside links. This change carries a decision or two, so the ceiling is
a hundred and fifty.
