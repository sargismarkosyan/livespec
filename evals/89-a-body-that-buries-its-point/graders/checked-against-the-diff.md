---
rule: the-body-is-checked-against-the-diff
type: command
command: 'python3 "$LIVESPEC_ROOT/evals/89-a-body-that-buries-its-point/check_body.py" diff'
weight: 1
---
The notes claim that a split also re-sorts the whole log by start time. The
diff does no such thing: `splitAt` only puts the new outing on top. So
`pr-body.md` does not say the log is re-sorted.
