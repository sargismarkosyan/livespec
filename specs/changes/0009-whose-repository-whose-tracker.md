# Spec 0009: whose repository, whose tracker

- **Status:** approved
- **Issue:** [#12](https://github.com/sargismarkosyan/livespec/issues/12) and
  [#10](https://github.com/sargismarkosyan/livespec/issues/10), taken together at
  the human's direction. See *Risks* — they split cleanly and were not split.

## Who this is for

[`@persona:agent-accelerated-owner`](../personas/agent-accelerated-owner.md), in
[`adopt-the-process`](../workflows/adopt-the-process.feature) — and this spec
does not have to argue for the placement, because the workflow file already
names both halves of it in *Where it breaks*:

> A skill assuming a tracker this repository does not use. A skill acting on
> "this repository" without resolving which one, so what is filed lands in the
> wrong tracker.

Those two sentences have been sitting in the workflow since
[`0006`](0006-adopt-the-process.md) with nothing implementing them. This is that
change.

The persona is the right one for a harder reason than the tag. Their file lists
four observed misses, and **two of the four are these**: *"a skill that never
resolved which repository it was standing in; a tracker assumed to be GitHub in a
repository whose tracker is a corporate GitLab."* This is not a persona inferred
to fit a change — it is a change written from behaviour that was watched.

The always-promise most at risk is **`context-budget`**
([spec.md](../spec.md#the-promises-that-belong-to-no-single-workflow)).
`feedback`'s description contains the ambiguous phrase and has to move, and a
description is the field every session pays for whether or not the skill fires.
The argument that this is affordable is in *Risks*, and it turns on the edit
**narrowing** rather than widening.

## The job behind the request

Have the report reach the person who can act on it.

That is the whole job, and it is smaller than either issue's title. An issue in
the wrong tracker is not misplaced — it is **invisible**. The consuming
repository's maintainer never sees the bug in their app, and livespec's
maintainer never sees the complaint about the plugin. Nobody is told. There is no
error, no failed command, and no second copy anywhere. It is the only failure
mode in this plugin that produces silence on both sides at once.

## Why now

**Because it has already cost a user.** [#10](https://github.com/sargismarkosyan/livespec/issues/10)
records what happened in the repository whose tracker is a corporate GitLab:
*"kept the repo's own local `feedback` skill for now rather than adopting
`livespec:feedback`, specifically because of this gap."* That is a hand-built
skill winning against the shipped one, in the only repository where the two were
ever compared. Nothing else in this tracker has evidence that strong.

**Because the ambiguity is everywhere and resolved nowhere.** The phrase "this
repository" appears 13 times across six payload files. Nothing in `method/` or
`skills/` says which one it means, and
[`method/repository.md`](../../method/repository.md) says issues are *"GitHub
Issues, via `gh`"* without ever saying whose.

**Because nothing has to be hardcoded for it to go wrong.** #12 establishes that
the plugin's own checkout is a live `gh` target however it was installed —
a directory marketplace points at the working clone, and a GitHub install is a
clone with a GitHub origin. `$CLAUDE_PLUGIN_ROOT` is a directory where
`gh issue create` succeeds and files into livespec.

**And it happened in the session that wrote this spec.** Three issues were filed
today — #30, #31, #32 — into livespec. That was correct, because the session's
working directory *was* livespec. Nothing in the skill checked, and nothing in
what it reported said which repository it had chosen. Being right by coincidence
looks identical to being right on purpose, which is the condition this change
ends.

## The end value

A report lands in the tracker of the repository it is about, and the human can
see which one that is **before** it happens rather than by going to look
afterwards.

And the plugin's `feedback` becomes adoptable in a repository that is not on
GitHub, which today it is not.

**How we would know it worked:** two things, both observable. Every filing reply
names the `owner/repo` it is about to file into, so a wrong target is one word to
correct instead of an issue nobody finds. And the hand-built `feedback` skill in
the GitLab repository can be deleted in favour of this one — the person who kept
it said exactly why they kept it, so that is a check somebody can actually run.

## What changes

1. **One portable sentence in `method/`.** Every repository-scoped action a skill
   takes — filing, listing, reading, committing evidence — targets the repository
   the session is working in. The plugin's own checkout is not a target. It goes
   in the method rather than in `feedback`, because #12's report says *"same for
   all other skills"* and seven copies of a rule go stale separately.

2. **`method/repository.md` stops naming GitHub as the tracker.** *"GitHub
   Issues, via `gh`"* becomes the portable statement — issues go where that
   repository's bindings say — and GitHub becomes an example rather than the
   definition.

3. **The bindings gain a tracker row**: the host, and the command that files
   there. This is the row [#10](https://github.com/sargismarkosyan/livespec/issues/10)
   asks for in as many words — *"so a repo can say 'this repo's tracker is GitLab
   at &lt;host&gt;, via `glab`' and the skill reads that instead of assuming
   GitHub."*

4. **`setup` writes that row.** It already has to find this:
   `setup-finds-where-issues-go` is a **live rule** as of
   [`0008`](0008-the-gate-gets-something-to-hold.md), and
   [`claude-md.md`](../../method/claude-md.md) requirement 10 already demands the
   answer be written down. What is missing is the row in the shape a skill reads,
   and one skill being told to read it. **The hook exists; nothing was plugged
   into it.**

5. **`feedback` names its target before it files** — the `owner/repo`, in the
   reply, before anything is created. This is the half of the change that can be
   graded, and *Risks* explains why that matters more than it looks.

6. **`feedback` gains the plugin exception and the undecided case.** A report the
   human says is about the plugin goes to the plugin's tracker, and the reply
   says so. A report that could be either, with nothing said, is **asked about
   once** rather than guessed — step 1 already batches questions, so it costs no
   new round.

7. **Evidence links follow the host.** `feedback` builds a
   `raw.githubusercontent.com` URL for screenshots; that is GitHub-shaped and
   breaks with the rest of it.

8. **`refine-spec` resolves which tracker `gh issue view <n>` reads.** The same
   ambiguity in reverse: *"pick up issue 7"* can mean two issues that both exist.

9. **The two descriptions carrying the defect lose it.** `feedback`'s said "the
   app in this repository" and named GitHub as the destination; `refine-spec`'s
   said the same phrase and "picking up a GitHub issue". Both are the always-on
   field, so both are the one place the ambiguity is read in every session
   whether or not the skill fires. `refine-spec` was not named in this spec
   before implementation and is added here rather than left: it is the same
   defect in the same field, and fixing one while shipping the other would leave
   a contradiction in the two most expensive characters in the plugin.

   **Both got shorter.** Dropping the tracker claim from `feedback`'s opening
   line — a description should not assert where issues go, since that is a
   binding — took the always-on cost to **3801**, below the 3809 it started at.
   No should-not-fire case is owed, because nothing widened.

**Rules added or changed** — the `@rule:` ids in `specs/features/`:

| Rule id | Feature file | New or changed |
|---|---|---|
| `skills-act-on-the-session-repository` | `features/routing/repository.feature` | new |
| `plugin-reports-reach-the-plugin` | `features/routing/repository.feature` | new |
| `an-unstated-subject-is-asked-about` | `features/routing/repository.feature` | new |
| `the-target-is-named-before-filing` | `features/routing/repository.feature` | new |
| `the-tracker-comes-from-the-bindings` | `features/routing/tracker.feature` | new |
| `evidence-links-follow-the-tracker` | `features/routing/tracker.feature` | new |

All six are `@planned` and **the files are already committed with this spec** —
the first time that has been possible here. `trace.py` accepts them because
[`0008`](0008-the-gate-gets-something-to-hold.md) made `adopt-the-process` live
and walked, so a new feature naming it no longer forces a workflow tag off or
demands a walkthrough. The two earlier specs that had to quote their Gherkin in
prose — [`0002`](0002-setup-finishes-what-it-names.md) and
[`0004`](0004-setup-can-be-offered.md) — were paying a cost that no longer
exists.

**Ledger:** nothing moves. No new gate.

## What we are not doing

- **Not implementing every tracker.** The bindings name the host and the command;
  the skill runs what they name. Shipping a `glab` code path — or a matrix of
  them — would be livespec deciding what somebody else's tracker is, which is the
  mistake in miniature.
- **Not auto-detecting beyond the remote.** Where the bindings say nothing, the
  host is worked out from what the repository already shows and **said out loud
  before it is relied on**. Silent inference is what this whole spec is against;
  replacing one silent guess with a cleverer silent guess would be building the
  defect again.
- **Not letting the plugin's own slug into the payload except once.** The
  exception in item 6 is the one place it may appear, because there it is a fact
  about livespec rather than an assumption about the reader's repository.
- **Not changing `record-clip`'s `docs/screenshots/` path.** It is already
  correct — relative to the working directory — but it was correct *by accident*,
  with no rule behind it. Rule 1 is now that rule; the path does not move.
- **Not the pull-request report** ([#30](https://github.com/sargismarkosyan/livespec/issues/30),
  [#31](https://github.com/sargismarkosyan/livespec/issues/31)), and not the
  tapes ([#32](https://github.com/sargismarkosyan/livespec/issues/32)) — though
  #32's upload-to-embed step lands on item 7 and should not be specced blind to
  it.
- **Not pinning every `gh` call to an explicit `--repo`.** Considered and
  dropped: it removes the model's discretion at the call site, but the resolution
  it forces is the one `gh` already performs from the working directory, so it
  buys less than it appears to — and it pays for that in more imperatives per
  skill body, which is [#15](https://github.com/sargismarkosyan/livespec/issues/15).

## Data

None. There is no storage contract — the plugin ships prose, and what a version
leaves behind is listed in [spec.md](../spec.md#what-a-version-leaves-behind).

## Risks

- **Two issues in one version, and they split cleanly.** #12 is *which
  repository*; #10 is *which tracker tool*; #10 depends on #12, because you
  cannot choose between `gh` and `glab` before resolving what you are talking
  about. They were taken together deliberately, on the grounds that the person
  who hit both hit them as one experience. **One change spec = one step = one
  version** is the rule in [`process.md`](../../method/process.md) this bends, and
  the honest form of the bend is that the second half could be lifted out at any
  point up to implementation.
- **Half of this ships unexercised by its own repository.** livespec is on
  GitHub, so the `glab`-shaped path — items 3 and 7 — is never taken here. That
  is the same property [#32](https://github.com/sargismarkosyan/livespec/issues/32)
  has and the same answer: the reference is the repository that reported it, and
  the check belongs there rather than in a case that cannot fail here.
- **The undecided-case question lands in a daily attempt.** Filing what they
  found is something this persona does *"multiple times a day, across more than
  one repository"*, and the workflows README is explicit that a step added to a
  daily attempt has to name what it shortens. It does not fire on the common
  case — a report about the app you are standing in resolves without asking. It
  fires only where both readings are live, which is precisely where guessing
  produces the silent misroute. **The first time that question fires on an
  unambiguous report, it is a defect, not a tuning problem.**
- **Naming the target is a claim, not a guarantee.** Rule 4 makes the skill say
  which repository it is filing into; it does not make that the right one. What
  it buys is that a wrong answer becomes visible at the moment it is cheap to
  fix. It is also **the only part of this an eval case can grade** — the suite
  grants no `Bash` and *"a case that files a real GitHub issue while being graded
  is not a test"*, so nothing here can check where an issue actually landed. A
  case can read what the reply claimed. That constraint is what chose this shape.
- **`context-budget` moved in the good direction, measured rather than hoped.**
  3809 → **3801** across 7 skills. The saving came from deleting a claim rather
  than from trimming prose: a description asserting the tracker was both wrong
  and expensive, and two skills carried it. Had it grown, the promise required a
  should-not-fire case rather than absorption; it did not, so none is owed.

## Acceptance checks

1. `python3 .github/scripts/verify.py` green, and the always-on cost reported by
   `checks.py` is **not higher** than 3809 across 7 skills. If it is, the
   description grew and `context-budget` says that is paid for, not absorbed.
2. In a clone of a repository that is **not** livespec, with livespec installed,
   report a bug about that app. The reply names that repository's `owner/repo`
   before filing, and what is filed is there.
3. Same session, say the complaint is about a skill. It reaches livespec's
   tracker, and the reply says that is where it went.
4. Same session, report something ambiguous — "the issue it filed had the wrong
   title" — with no indication of which repository. It asks once and files
   nothing until answered.
5. Run `feedback` **inside livespec**. It behaves identically and reads as normal
   prose; nothing in the reply implies the two repositories have to be different
   places.
6. Read the six `Rule:` lines looking only for a tool name — `gh`, `glab`,
   GitHub, GitLab. There should be none: the tool is a binding and the rules are
   the method.
