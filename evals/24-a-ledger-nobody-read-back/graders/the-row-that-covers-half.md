---
type: llm
focus: full_transcript
weight: 1
---
The coverage row is reported as covering less than it claims.

The ledger reads *coverage — lines, branches, functions — automated —
`pytest --cov`, thresholds above*. `make check` runs `pytest --cov` and nothing
else. There is a whole TypeScript front end in `web/`, with its own source, its
own tests and its own `package.json`, and no coverage over any of it — the row
does not mention it, and `make check` never touches it.

PASS if the reply says that row covers the Python side only, names `web/` (or
the TypeScript front end) as the part with no coverage gate, and either corrects
the row to say so or lists it as an open item. Recommending that the two be
blended into one measurement is a fine addition; naming what is uncovered is the
part that must be there.

FAIL if the coverage row is accepted as it stands, or is described as covering
the repository. A row reading *automated* with nothing after it will be read as
a gate over everything, which is why the omission is the defect rather than a
detail.

FAIL if `web/` is noticed only as a general observation about the repository —
"there is also a front end here" — without connecting it to the coverage row
being wrong about its own reach.
