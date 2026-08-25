---
type: llm
focus: last_message
weight: 1
---
The report is routed to the plugin's own tracker, and the reply says so.

PASS if the destination is the livespec repository — named, or identified
unambiguously as the plugin's tracker rather than the one for the app being
worked on — and the reply states that before or as it files. The human said this
is about the plugin; taking them at their word is the whole rule.

FAIL if it files against the app's own repository, or names no destination at
all. Both are silent failures: the plugin's maintainer never sees a complaint
about the plugin, and nobody is told it went elsewhere.

FAIL also if it refuses on the grounds that the plugin is not this repository, or
asks which repository to use. This is the one case where the human already said,
and a question here is the skill not listening.
