---
name: record-clip
description: Record the animated GIF a version ships with — the app being used in a real browser — and save it to docs/screenshots/. Use when asked to record, film, screenshot or capture a version, a clip, a GIF or a video of the app, or to show a change moving rather than frozen. Every pull request that changes what the app looks like needs one. Ships with the plugin — it records the app and never changes it.
---

# Record the version

Produces **one looping GIF** in `docs/screenshots/`: the app being *used*, not a
still. It is the only picture a version gets, and the pull request carries it —
see [`repository.md`](../../method/repository.md). **Keep it
short**: a handful of seconds, a dozen or so frames. Nobody watches a long one,
and it lives in git forever.

**No PNGs.** A frozen frame is not a deliverable here. Half of what an app does
is something *happening* — a thing unfolding, a line landing where it was
dropped, a suggestion being taken — and that is exactly the half a still drops.

## What to record

**The change this version made, in the shortest sequence that shows it.** Read
the change spec first: its *What changes* section is the shot list, and its
*Acceptance checks* are usually already in order.

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

## Rules

- **Never commit the frames.** Only the finished GIF. `.frames/` is ignored.
- **One GIF per version**, named for the change spec that shipped it —
  `v001-<the spec's slug>.gif`.
- **Recorded on the branch, before the pull request is opened**, and embedded in
  the body by a raw URL pinned to the commit. A branch URL rots when the branch
  is deleted on merge.
- **Never touch `src/` or `specs/`.** If the recording shows something broken,
  that is a finding: file it with the `feedback` skill. Do not fix it here, and
  do not re-record around it.
- Check the file size before committing. Over ~1 MB means too many frames or too
  large a viewport.
