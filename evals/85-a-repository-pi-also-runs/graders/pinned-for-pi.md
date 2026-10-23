---
rule: the-sitting-enables-livespec-for-each-host-in-use
type: command
command: 'python3 -c "import json,re,sys; pi=json.load(open(\".pi/settings.json\")); cc=json.load(open(\".claude/settings.json\")); src=[p if isinstance(p,str) else p.get(\"source\",\"\") for p in pi.get(\"packages\",[])]; sys.exit(0 if \"npm:@harbourside/pi-tide-tables@1.2.0\" in src and any(re.fullmatch(r\"git:(https://)?github\.com/sargismarkosyan/livespec@livespec--v\d+\.\d+\.\d+\",s) for s in src) and cc.get(\"enabledPlugins\",{}).get(\"livespec@livespec\") is True else 1)"'
weight: 1
---
`.pi/settings.json` declares livespec as a git package pinned to a release
tag, beside the package it already declared, and `.claude/settings.json`
still enables the plugin.
