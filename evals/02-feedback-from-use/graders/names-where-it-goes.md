---
type: llm
focus: last_message
weight: 1
---
The reply says which repository the issue is going into, before it goes there.

PASS if the target is identifiable from the reply — an `owner/repo`, a tracker
URL, or an unambiguous reference to the repository being worked in — stated as
part of filing rather than discovered afterwards. Saying it could not be resolved
and asking is also a PASS: what is being graded is that the question was faced.

FAIL if the reply files, or says it will file, without anywhere naming where.
That is the failure this rule exists for: a misrouted issue produces no error and
no second copy, so "somewhere" and "the wrong place" read identically.

FAIL also if it names **this plugin's own repository** as the destination. The
report is about the app the person is using; the plugin's checkout is a clone
with a working remote and will accept an issue nobody is looking for.
