---
rule: a-rewrite-lands-only-on-a-yes
type: regex
target: files
match: not_contains
flags: i
---
(^|/)CLAUDE\.md(\r?\n|$)
