---
name: record-clip
description: Record the picture a version ships with — the app being used in a real browser — and save it to docs/screenshots/. Use when asked to record, film, screenshot or capture a version, a clip, a GIF or a video of the app, or to show what a change did. Every pull request that changes what the app looks like needs one. Ships with the plugin — it records the app and never changes it.
---

# Record the version

Produces **one picture** in `docs/screenshots/`: the app being *used*, not
described. It is the only picture a version gets, and the pull request carries
it — see [`repository.md`](../../method/repository.md#every-pull-request-shows-what-it-did).
**Keep it short**: a handful of seconds, a dozen or so frames. Nobody watches a
long one, and it lives in git forever.

## Decide the form before you record

**A looping GIF, unless the change has nothing that happens.** Half of what an
app does is something *happening* — a thing unfolding, a line landing where it
was dropped, a suggestion being taken — and that is exactly the half a still
drops. Padding those into an animation is not the risk; delivering a frozen frame
of them is.

**A PNG only when the whole result of the change is a screen sitting there** — a
label reworded, a column added, an empty state that now says something else.
Nothing unfolds, so a recording of it is a dozen identical frames, and the still
answers the reviewer's question better than the loop does.

The form is a fact about the change, not about what is convenient. Being offered
a still, being short of time, or the recording being awkward to set up are none
of them the reason — the exemption in the method is *nothing to see*, and "it is
hard to record" is explicitly not it. When the two answers come apart, record.

## What to record

**The change this version made, in the shortest sequence that shows it.** Read
the change spec first: its *What changes* section is the shot list, and its
*Acceptance checks* are usually already in order.

**Compose it for somebody holding the request and nothing else.** The change spec
is the shot list; the *request* is the standard — the issue it came from, or the
spec's own *The job behind the request*. They have not read the diff and will not
check the branch out, so the question a shot has to answer is whether the person
who asked can tell that they got what they asked for. A sequence that shows how
the change was built answers a question nobody was asking.

Get on screen the thing that is new, plus just enough of what was there before to
make it read. Search shows a result from somewhere the user was not looking.
Reordering shows the line *arriving*, which is two frames minimum. A change that
only makes sense against the old state needs the old state in shot.

When the version changed the core of the app rather than one corner, record the
tour instead — the shortest walk through the workflows that carry the value
(`specs/workflows/README.md`), which is usually:

1. The empty state, its message showing.
2. Three things created, one at a time — a frame after each.
3. One of them opened. Whatever unfolds is the moment worth holding.
4. One of them filled in, so it happens on screen.

Use the repo's own vocabulary for what goes on screen, not lorem ipsum. Content
that reads like somebody's real data.

## How

1. Serve the app in the background — the command is in
   `specs/setup/README.md`. Do not guess it, and do not reach for `file://`:
   an app of ES modules does nothing there.
2. Drive it with the Playwright browser tools at the viewport
   `specs/setup/README.md` names. Every version is recorded at one size, or the
   series stops being one series.
3. After every step, screenshot to `docs/screenshots/.frames/NN.png` —
   zero-padded so they sort.
4. Hold on a moment by writing the same frame twice. Worth holding: the state
   the change is *about*, and the last frame, so a loop does not snap.
5. Stitch, then clean up:
   ```sh
   python3 "$CLAUDE_PLUGIN_ROOT/tools/clip.py" docs/screenshots/.frames docs/screenshots/vNNN-<slug>.gif
   rm -rf docs/screenshots/.frames
   ```

   The stitcher ships with this plugin. If `$CLAUDE_PLUGIN_ROOT` is not set,
   it is `tools/clip.py` two levels up from this skill file.
6. Stop the background server.

**A still is steps 1, 2 and one screenshot**, written straight to
`docs/screenshots/vNNN-<slug>.png`. No `.frames/`, no stitcher. The viewport is
the same one — a series that changes size stops being a series whichever format
it is in.

## Rules

- **Never commit the frames.** Only the finished picture. `.frames/` is ignored.
- **One picture per version**, named for the change spec that shipped it —
  `v001-<the spec's slug>.gif`, or `.png` where the change had nothing that
  happens.
- **Recorded on the branch, before the pull request is opened**, and embedded in
  the body by a raw URL pinned to the commit. A branch URL rots when the branch
  is deleted on merge.
- **Never touch `src/` or `specs/`.** If the recording shows something broken,
  that is a finding: file it with the `feedback` skill. Do not fix it here, and
  do not re-record around it.
- Check the file size before committing. Over ~1 MB means too many frames or too
  large a viewport.
- **The form is reported, not slipped in.** Say which one this version got and
  why, in the same breath as handing the file over. A still that arrives without
  its reason is indistinguishable from a recording somebody gave up on.
