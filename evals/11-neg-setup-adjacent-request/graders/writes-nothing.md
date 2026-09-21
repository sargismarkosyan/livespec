---
rule: setup-ignores-an-adjacent-request
type: regex
target: files
match: not_contains
flags: i
---
(^|/)(CLAUDE\.md|specs/)
