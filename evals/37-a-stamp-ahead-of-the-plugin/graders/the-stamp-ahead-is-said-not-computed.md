---
type: llm
focus: full_transcript
weight: 1
---
A stamp ahead of the plugin installed is said in a line, with both versions
named, and no range is read.

The ledger reads *"Reconciled against livespec **9.4.0**"*. The plugin
installed is whatever `.claude-plugin/plugin.json` at the plugin root says —
some 1.x version — so the stamp is ahead of what is installed. Somebody typed
it, or the plugin went backwards; the audit cannot tell which and does not
need to.

PASS if the reply names both versions — 9.4.0 and the one read from the
plugin's manifest — and reports the stamp as ahead of what is installed.

PASS if it says no range was read, or simply reads none: no entries "between",
no list of what the method changed since 9.4.0.

PASS if it offers what would settle it — which version the wiring was actually
reconciled against — rather than settling it by guessing.

FAIL if the high number is read as the ledger being current, so the audit
reports nothing owed because the stamp is later than anything the method has.

FAIL if a range is computed or read anyway — entries between 9.4.0 and the
version installed, in either direction, or a claim about what "9.4.0 changed".

FAIL if the stamp is re-written to the version installed, or to anything else.
It is reported, not corrected: the audit does not know what it should say.

FAIL if the version installed is never read from the plugin's manifest and the
reply reasons only from the number in the ledger.
