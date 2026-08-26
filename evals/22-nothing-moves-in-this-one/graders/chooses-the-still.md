---
type: llm
focus: last_message
weight: 1
---
The reply delivers a still for this version, and refuses the GIF the human asked
for on the grounds that nothing in the change happens.

PASS requires both:
- what it produces, or says it will produce, is a single image —
  `docs/screenshots/v031-*.png` or an equivalent frame — not an animation;
- the reason is about *this change*: the badge is a card sitting there, the whole
  result is on screen at once, a loop of it would be a dozen identical frames.

The human's reason for wanting a GIF is that the series should look consistent.
A reply that names that as the wrong reason — the form follows what changed, not
what the other files in the directory are — is a strong PASS.

FAIL if it records a GIF anyway to keep the series consistent, or agrees that a
directory of GIFs obliges this version to be one.

FAIL if it manufactures motion to justify the format: archiving a link on camera,
scrolling the archive, hovering the badge for its tooltip. The change is the
badge's contents, and staging an action around it is padding.

Offering the human a choice and stopping is a FAIL — it is the skill's judgment
that is being asked for. Naming the still as the answer and saying it can be a
GIF if they insist is a PASS.
