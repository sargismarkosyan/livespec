---
rule: a-change-spec-is-named-by-its-day-and-slug
type: command
command: 'ls specs/changes/[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]-*.md >/dev/null 2>&1 && ! ls specs/changes/000[7-9]-*.md >/dev/null 2>&1'
weight: 1
---
The new change spec is named `YYYY-MM-DD-<slug>.md`. No number is taken —
not 0007 from the checkout, nor 0009 past what is in flight.
