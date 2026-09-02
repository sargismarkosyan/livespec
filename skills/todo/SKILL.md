---
name: todo
description: Capture what somebody found or wants about the app they are building, as well-researched issues in that repository's tracker — a bug, something confusing, something missing, an "I wish it did X" or "can it also…", or a screenshot with a complaint. Triggers on "feedback about the app", "report this", "log an issue", "track this", "found a bug". Reporting or wishing lands here; an instruction to build now is refine-spec. Investigates the code before filing; never fixes or specs.
---

# What somebody found → a tracked issue

The human is the only person who actually *uses* this app, and the only one who
knows what it still needs. This skill exists so that nothing they found or
wanted gets lost between their chat message and the issue tracker — a wish for
something that does not exist yet counts, and has nothing to reproduce.

Your job is to **listen, investigate, and file**. Not to fix. Resist every urge
to open an editor — a fix without a spec breaks the process in `CLAUDE.md`.

## 0. Settle where this is going, before anything else

Two questions, both answered before you investigate and **both stated in your
reply before you file**. They take one line each and they are the difference
between an issue somebody reads and an issue nobody ever sees.

**Which repository.** The one the session is working in — never this plugin's own
checkout, which is a clone with a working remote and will happily accept an issue
nobody is looking for. Resolve it rather than assume it, and say what you
resolved.

**The exception, and the only place this plugin names itself:** when the human
says the complaint is about a *skill* — the plugin misbehaved, an interview asked
the wrong thing — it goes to the plugin's own tracker instead, and your reply
says that is where it went.

**When you cannot tell, ask.** A report that could be about either, with nothing
said either way, is the one case worth a question: batch it with the questions in
step 1 and file nothing until it is answered. Everywhere else, infer and state
what you inferred. This is not a licence to ask on every report — a complaint
about the app somebody is standing in resolves without a question, and asking
there is a defect in this skill rather than caution.

**Which tracker.** Read it from `specs/setup/README.md` — the host and the
command that files there. **Do not assume it is GitHub.** Where the bindings say
nothing, work it out from what the repository already shows — `git remote get-url
origin` names the host — and **say what you worked out** before you rely on it.
Where there is no tracker at all, say so — and still hand over the issue body you
wrote, so the finding survives having nowhere to go.

Every command in the steps below is written in the common case, GitHub through
`gh`. **They are examples of the shape, not the tool.** Substitute what the
bindings name.

**When a step will not go through here, say it once and hand over the rest.** The
bindings may name a tool this session cannot run, or the repository may record no
bindings at all. Either is ordinary. Name what is missing in a line, then finish
everything that did not depend on it — the investigation, the issue body, and the
exact command for somebody who can run it. Do not spend the session looking for
another way through; the rule and its reasoning are in
[`process.md`](../../method/process.md#a-step-you-cannot-take-here-is-said-once-not-searched-for).
This narrows nothing in step 3: looking for the **cause** is the job, looking for
a **way to run an unavailable step** is not.

**The bindings may also record a workaround** — something this repository does
its own way because of a gap filed somewhere else. Where one bears on the step in
front of you, say once that you are following it and what would end it; where you
are already at the tracker that gap was filed in, say whether it is still open.
Never follow one silently, and never go looking for a tracker you had no other
reason to reach. The rule is in
[`process.md`](../../method/process.md#a-workaround-names-what-would-end-it).

If the repository the session is in *is* this plugin's repository, all of the
above still applies and gives the same answer. Nothing here requires the two to
be different places.

## 1. Take what they said apart

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
  body, embed it with a raw URL **on the host this repository actually lives on**
  — the one step 0 resolved. On GitHub that is
  `![description](https://raw.githubusercontent.com/<owner>/<repo>/main/docs/feedback/<file>)`;
  elsewhere it is that host's equivalent, and a `raw.githubusercontent.com` link
  in an issue on another host is a broken image with a confident URL.
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

List what the tracker already holds before creating anything — on GitHub,
`gh issue list --state all --limit 100`. If it already exists, add a comment with
the new evidence instead of filing again, and tell the user that is what you did.

## 5. File it

```sh
gh issue create --title "<title>" --label "<labels>" --body-file <path>
```

**Name the repository you are filing into, in your reply, before you run this.**
Not afterwards in the confirmation — before, while a wrong answer still costs one
word to fix. Right by coincidence and right on purpose look identical once the
issue exists.

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

**If this repository is going to carry on around what you just filed, record
that.** Filing the gap where it can be fixed for everyone and keeping the local
way of doing it are both right, and between them they leave a workaround that
nothing ever ends. Write one row into the bindings: what is done here instead,
the gap it goes around, where it is filed, and what would end it. **Say the row
in your reply before you write it**, the way you named the repository before
filing — a wrong row costs one word now and outlives everybody later. You are
recording a decision somebody else made, not making one, and not touching the
workaround itself; the row comes out when the workaround does.

**Where the filing could not go through from here, the row still goes in now**,
naming the report you handed over rather than an issue number nobody in this
session can create. The workaround is in force today, and a row that waits for a
number will only ever be written by sessions that did not have the problem.

Then stop. Picking the issue up and writing a spec is a separate, later step.
