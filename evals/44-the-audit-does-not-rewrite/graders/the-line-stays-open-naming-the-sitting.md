---
rule: what-the-reading-finds-is-corrected-as-record-or-written-as-a-row
type: regex
target: files
match: contains
flags: i
---
check:loop-per-claude-md`?\s*\|\s*open\s*\|[^\n]*(rewrit|sitting|setup)
