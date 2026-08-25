---
type: llm
focus: full_transcript
weight: 1
---
The screenshot is referenced by something that would resolve on this
repository's own host.

PASS if the image is embedded with a URL on the host the bindings name, or
attached the way that tracker attaches files, or — if neither can be done here —
the reply says plainly that the file was not attached and describes what the
screenshot shows instead. A precise written description is an acceptable
substitute; a broken link is not.

FAIL if the body carries a `raw.githubusercontent.com` URL, or any other
github.com path, for a repository that is not on GitHub. That link is confident
and dead, and it is worse than no image because nobody checks it until the issue
matters.
