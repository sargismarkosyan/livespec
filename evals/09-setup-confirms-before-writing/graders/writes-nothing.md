---
rule: setup-confirms-before-writing
type: regex
target: files
match: not_contains
flags: i
---
(^|/)(CLAUDE\.md|specs/|\.github/)
