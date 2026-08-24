---
name: feedback
description: Turn a human testing session into well-researched GitHub issues. Use whenever the user reports something about the app in this repository from having actually used it — a bug, something confusing, something missing, an "I wish it did X", or a screenshot with a complaint attached. Triggers on "feedback", "report this", "log an issue", "this is broken", "found a bug", or a pasted screenshot of the app. Investigates the code before filing, and does not fix anything.
---

# Feedback → GitHub issue

The human is the only person who actually *uses* this app. This skill exists so
that nothing they noticed gets lost between their chat message and the issue
tracker.

Your job is to **listen, investigate, and file**. Not to fix. Resist every urge
to open an editor — a fix without a spec breaks the process in `CLAUDE.md`.

## 1. Take the feedback apart

One message from a human is almost never one issue. Read it and pull out every
distinct thing worth tracking.

Capture the **implicit** alongside the literal:

- The stated complaint ("delete doesn't work").
- The expectation behind it ("I assumed it would ask me first") — an unstated
  expectation is a real finding even when the app behaves as specced.
- Friction they mention in passing ("I had to scroll to find it"). Passing
  remarks are the easiest thing to drop and often the most useful.
- Emotional signal — annoyance, hesitation, surprise. "That's weird" means the
  app violated a mental model. Record what the model seems to be.
- What they were *trying to accomplish*, which is often bigger than what they
  asked for.
- Anything the screenshot shows that they did not mention.

Then split into separate issues. **One issue = one change someone could spec.**
Two bugs in one sentence are two issues. A bug plus a wish is two issues.

If something is ambiguous and the answer changes what gets filed, ask before
filing — but batch your questions and ask once.

## 2. Handle screenshots

A screenshot is evidence; get it into the issue if you can.

- **If the user gives a file path** (or drags a file in and you can see a path):
  copy it into the repo as
  `docs/feedback/<issue-slug>-<n>.png`, then commit and push it. In the issue
  body, embed it with the raw URL:
  `![description](https://raw.githubusercontent.com/<owner>/<repo>/main/docs/feedback/<file>)`
  — `gh repo view --json nameWithOwner` if you are not sure of the slug.
  The file is temporary: it gets `git rm`'d when the issue closes, which is why
  the written description below is the part that has to survive.
- **If the image was pasted straight into chat**, you can see it but you cannot
  write it to disk. Ask for a path if the image is load-bearing; otherwise
  describe it precisely in the issue and note that no file was attached.

Either way, **write down what the screenshot shows**. Exact wording of visible
text, what is misaligned and by roughly how much, what state the contents is in,
anything visibly wrong that the user did not call out.

## 3. Investigate before filing

This is what makes these issues worth reading. Do not file a restatement of the
complaint — go find out what is actually happening.

- Find the responsible code. Name the file and line — `src/<file>:42` — so it
  is one click for whoever picks it up.
- Find the spec that introduced the behaviour (`specs/`) and check whether the
  app is violating its spec or faithfully implementing a bad one. Say which —
  they lead to very different fixes.
- Form a concrete hypothesis about the cause, and say how confident you are.
  A wrong guess stated as a guess is useful; a wrong guess stated as fact is not.
- **Reproduce it.** Not "if convenient" — this is the step that decides whether
  the issue is worth anything, and it has its own section below.
- Read whatever the app has persisted and paste it into the issue. The storage
  contract is in `specs/spec.md` and the way to read it is in
  `specs/setup/README.md`; a malformed or surprising stored value is very often
  the answer.
- Check whether it is really about persistence rather than about the screen:
  does it survive a reload, does it break with two of the app open at once, does
  it break when the stored value is missing or corrupt.
- Note anything nearby that is broken for the same reason. File those as their
  own issues rather than folding them in.

If investigation shows the report is not reproducible, still file it — with what
you tried and what you would need from the user to get further.

### Reproduce it, and put the reproduction in the issue

**A reproduction someone can run beats a description of one every time.** It is
what turns "the AI proposes things in a funny order" into a defect with a known
cause, and it is the difference between an issue that gets fixed and an issue
that gets argued about.

Prefer, in this order:

1. **A runnable reproduction against the module.** Where the bug is in `src/`
   rather than on screen, a few lines calling the function directly — with its
   real output pasted underneath — is the strongest evidence there is. Paste it
   as a fenced block, with the actual output, not the expected output.

   ```js
   theFunction(theInputThatBrokeIt, theRestOfTheState)
   // what it actually returned, pasted — not what it should have returned
   ```

   Whoever picks the issue up runs that first and knows in ten seconds whether
   it still bites. **Re-run it before writing a spec**, because the code has
   usually moved since the issue was filed.

2. **Steps through the app**, when the bug is what the screen does. Serve it —
   the command is in `specs/setup/README.md` — and drive it with Playwright.
   Number the steps from cleared storage so they start somewhere known, and say
   what is on screen at the end, not just what is wrong with it.

**Say which build you reproduced on**, and reproduce on `HEAD` rather than on
the build in the screenshot. Those differ more often than not — a user reports
from the version they have, and the fix may already be in. An issue that says
*"still reproduces at `<sha>`"* is worth several that say *"reproducible: yes"*.

### When you cannot reproduce it here

Some things cannot be settled from this machine — anything needing a real
on-device model is the standing example, because a fake one returns whatever the
test told it to and proves nothing about what a model does.

Say so plainly, and then **do the work that makes the check cheap for whoever
can run it**:

- name the exact thing to run, and where;
- say what result closes the issue and what result escalates it;
- where a page or a script would answer it in one go, write that and link it.

What is not acceptable is filing *"somebody should check this"* with no owner
and no method. That is how a one-minute check goes unrun for a dozen versions.
Set **Reproducible:** to `unverified at HEAD — <what would settle it>` so the
gap is legible in the issue list rather than buried in the body.

## 4. Check for duplicates

`gh issue list --state all --limit 100` before creating anything. If it already
exists, add a comment with the new evidence instead of filing again, and tell
the user that is what you did.

## 5. File it

```sh
gh issue create --title "<title>" --label "<labels>" --body-file <path>
```

Write the body to a scratch file and pass `--body-file` — bodies have newlines
and backticks and will not survive being inlined.

**Titles** describe the symptom from the user's side, specifically enough to be
recognised in a list: "Deleting the last one leaves the empty state hidden",
not "delete bug".

**Labels:** `from-feedback` always. Then `bug`, `enhancement`, `ux`,
`accessibility`, or `question`. Add `needs-spec` once it is clearly something to
build.

**Body template:**

```markdown
## Reported

> <the user's own words, verbatim — do not clean them up>

**App version:** <spec number at HEAD, e.g. 0001>
**Reproducible:** yes / no / partly / unverified at HEAD — <what would settle it>
**Reproduced on:** <sha or spec number you actually ran it against>

## Screenshot

![<what it shows>](<raw URL>)

<precise description of what is visible, including anything the user did not mention>

## Everything the feedback contains

- <one bullet per insight, including implicit expectations and passing remarks>
- <note which of these are filed as separate issues, with #numbers>

## Steps to reproduce

1. ...

**Expected:** ...
**Actual:** ...

<a runnable reproduction where one is possible — the call, and its real output
pasted underneath. See *Reproduce it* above.>

## Technical findings

- **Where:** `src/<file>:42` — `<function>`
- **Introduced by:** spec 0001
- **Spec conformance:** violates spec / matches spec (the spec is wrong) / unspecced
- **Stored state:** `<storage key>` = `<value at time of report>`
- **Suspected cause:** <hypothesis, with confidence>

## What a fix would need to cover

<scope notes for whoever writes the spec — and what should stay out of it>
```

Leave out any section you genuinely have nothing for. An empty heading is worse
than no heading.

## 6. Report back

Give the user the issue URLs, one line each, and say plainly what you found
while investigating — especially if the cause turned out to be different from
what they assumed. If you deliberately did not file something they said, say so
and why.

Then stop. Picking the issue up and writing a spec is a separate, later step.
