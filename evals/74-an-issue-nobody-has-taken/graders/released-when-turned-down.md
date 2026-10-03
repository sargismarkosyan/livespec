---
rule: a-dropped-claim-is-released-by-whoever-dropped-it
type: command
command: 'python3 -c "import json,sys; i=[x for x in json.load(open(\".tracker/state.json\"))[\"issues\"] if x[\"number\"]==12][0]; sys.exit(0 if \"in-progress\" not in i[\"labels\"] and len(i[\"comments\"])>=2 else 1)"'
weight: 1
---
The person turned the spec down. The session that claimed issue 12 takes
`in-progress` off it and says so in a second comment — the claim, then the
release. A label left on is a claim nobody holds.
