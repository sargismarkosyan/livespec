---
type: command
command: 'python3 "$LIVESPEC_ROOT/evals/44-the-audit-does-not-rewrite/check_corrected_in_place.py"'
weight: 1
---
The two lines are corrected in place and the file is not rewritten. The loop's
step 2 named `/livespec:feedback`, a skill the plugin has called `todo` since
1.0.0; step 4 read *Human approves* with nothing about what the person holds.
Both are record and both are corrected. The template around them — the
placeholder overview, the generic style rules, the copied rules, the history —
is left standing, because a whole new file is the sitting's kind of change,
not the audit's. The script checks five anchor lines survive, the old name is
gone with the new one in its place, and step 4 names the sketch.
