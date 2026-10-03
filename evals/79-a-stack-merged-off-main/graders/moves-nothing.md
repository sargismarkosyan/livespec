---
rule: a-merge-that-missed-main-is-listed
type: command
command: '! grep -E " set " .forge/calls.log 2>/dev/null && ! git merge-base --is-ancestor "$(python3 -c "import json;print([p for p in json.load(open(\".forge/state.json\"))[\"pulls\"] if p[\"number\"]==32][0][\"head_sha\"])")" main'
weight: 1
---
Nothing moved: no forge setting was changed, and #32's commit is still not
on main. The audit lists what is stranded; it does not land it.
