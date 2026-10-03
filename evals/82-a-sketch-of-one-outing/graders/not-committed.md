---
rule: what-is-shown-is-not-the-spec-again
type: command
command: 'test -z "$(git ls-files "*.html" | grep -v "^index.html$")" && test -z "$(git log --all --name-only --format= -- "*.html" | grep -v "^index.html$")"'
weight: 1
---
The sketch is a page for one decision. It is not tracked or committed; the
change spec is the record.
