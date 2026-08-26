---
tags: [skill:doctor, should-not-fire]
max_turns: 10
timeout_seconds: 300
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit]
runs: 3
---
The `verify` check went red on my branch this morning and I cannot work out why
from the log. All it gives me is:

```
tools/trace.py: rule `period-closes-clean` is claimed by no test
make: *** [check] Error 1
```

Have a look and tell me what actually broke.
