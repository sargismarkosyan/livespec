# Spec 0037: a name that already belonged to something else

- **Status:** proposed
- **Issue:** [#83](https://github.com/sargismarkosyan/livespec/issues/83)
- **Depends on:** nothing. It stands beside
  [`0032`](0032-the-repository-does-not-know-it-is-owed.md) and
  [`0036`](0036-a-row-that-was-right-once.md), which cut the same seam twice —
  between having adopted the process and the process moving on underneath. This
  is the third thing found sitting in it, and the first one that this repository
  itself causes.

## Who this is for

[`agent-accelerated-owner`](../personas/agent-accelerated-owner.md), and it
arrives in two of their situations rather than one.

**The first is an attempt that is real and deliberately unwritten.** *Filing what
they found* is one of the three the [workflows README](../workflows/README.md)
names as *"real and all three have happened many times over in `todo-change` —
but none of them has had its own occasion interviewed."* The rename serves that
attempt, and this spec does not cut it: a workflow cut from a guess has to be cut
twice, and that is [`refine-workflows`](../../skills/refine-workflows/SKILL.md)'
own change to make. **Said out loud rather than filed under a workflow to fill
the box**, per [`process.md`](../../method/process.md).

**The second is [`adopt-the-process`](../workflows/adopt-the-process.feature)**,
at the seam after the sitting is over — which is where the second half of this
change lives, and which is a live workflow that the new rule tags.

Two persona lines decide the shape:

- **"When the tool does not fit the repository, the hand-built local version
  stays."** The persona file records this as already having happened: *"In the
  repository whose tracker is GitLab, their own `feedback` skill was kept rather
  than replaced with the plugin's."* That is not a preference — it is a **name
  collision that has already cost this plugin an install**, written down in our
  own persona file and never read as the defect it describes.
  [`method/README.md`](../../method/README.md) states the mechanism in the next
  breath: *"A bare `refine-spec` with no prefix means a local copy in
  `.claude/skills/` is shadowing the plugin."*
- **"more than one repository at once."** So the record left pointing at the old
  name is not one file. It is one per repository, and none of them will hear
  about this.

**This does not lengthen adoption.** The workflows README requires a change that
adds a step to the sitting to name the later attempt it shortens; the audit half
runs after the sitting is over, and the rename adds no step to anything.

## The job behind the request

For the word somebody says to land what they found in the place it belongs —
without their first having to work out which of the two things in the session
owns that word.

## Why now

Because the word has three owners in one session, and this plugin is the only one
of the three that can move.

- **Claude Code's own feedback path.** A session carries a built-in
  `SendFeedback` tool, whose whole subject is drafting feedback **about Claude
  Code** for Anthropic. It is present in the roster of the session writing this
  spec.
- **The plugin's `feedback` skill**, whose subject is a finding **about the app
  being built**, filed into that repository's tracker.
- **The persona's own hand-built `feedback` skill**, in the GitLab repository,
  which shadows ours outright.

The two destinations could hardly be further apart — one leaves the repository
entirely — and the single word "feedback" is the only thing the session has to
tell them apart with. A misfire does not produce a wrong-looking answer; it
produces a confident one, filed somewhere nobody working on the app will look.

The current description makes this worse on purpose: it lists **`"feedback"`** as
the first trigger word, which is precisely the token the built-in tool owns.

## The end value

Saying what they found gets it filed against the app; saying they want to report
something about Claude Code reaches Anthropic; and neither has to be disambiguated
by hand. In a repository that already adopted the process, the audit says so when
its own record is still pointing at the name that moved.

**How we would know it worked:** the record in a consuming repository stops being
able to name a skill that does not exist — today `doctor` reads
[`CLAUDE.md`](../../method/claude-md.md) and cannot tell. Concretely, both
`evals/32-*` and `evals/34-*` lay down a fixture `CLAUDE.md` whose loop reads
``2. AI files issues (`/livespec:feedback`)``, and an audit of either reports
nothing about it.

## What changes

- **`skills/feedback/` becomes `skills/todo/`.** The name the human types is
  `/livespec:todo`, and the frontmatter `name` moves with the directory —
  `checks.py` fails a mismatch between the two.
- **The description stops claiming the collided word.** The trigger list's bare
  `"feedback"` becomes `"feedback about the app"`. That is a **narrowing** — it
  matches strictly fewer utterances than the bare word — so no should-not-fire
  case is owed for it. `context-budget` moves from **4315** to about **4325** of
  5000: the name loses four characters and the trigger phrase gains fourteen.
- **`todo` does not become a trigger word.** It is the name, and the name is
  already in always-on context; putting it in the trigger list would widen the
  description straight into the collision the new name has of its own —
  `todo-change` is a repository where *todo* is an app object, and "add a todo"
  there is an instruction to build. That case already has a should-not-fire
  guard in [`19-neg-instruction-is-not-filed`](../../evals/19-neg-instruction-is-not-filed/),
  which this change re-measures rather than adds to.
- **`doctor` gains a check that the record names skills that exist.** A name in a
  consuming repository's own account of the loop is read against the skills this
  plugin now has; one that reaches no skill is reported with what it is now, and
  offered as it will read. It corrects the **record**, which is what `doctor` is
  already for.
- **The prose that names the skill moves; the prose that names the loop does
  not.** `README.md`, `CONTRIBUTING.md`, `CLAUDE.md`, `method/process.md`,
  `method/README.md`, `method/claude-md.md`, `method/repository.md`,
  `specs/spec.md`, and the three sibling skills that name it. Where the word is
  the loop's ordinary noun — *"turn feedback into researched issues"* in
  `plugin.json` — it stays, because it is not a reference to a skill.

**Rules added or changed** — the `@rule:` ids in `specs/features/`:

| Rule id | Feature file | New or changed |
|---|---|---|
| `a-skill-the-record-names-is-one-that-exists` | `features/wiring/what-an-audit-reads.feature` | new, `@planned` |

Added to that file rather than a new one: it is **what an audit reads**, and a
third rule leaves it at 3 of its 6 rules and 75 of its 120 lines.

**No rule for the rename itself.** A decision taken deliberately: the rename is
mechanical and a rule pinning *why the name is not "feedback"* would be prose
with a tag on it. What holds the decision is this spec and the collision, which
has not gone anywhere.

**No description change on `doctor`, so no should-not-fire case is owed there.**
Its description already carries *"to say whether the process still holds here"*,
which a record naming a skill that does not exist plainly is.

## What this costs, in a number

Renaming the skill and editing `doctor` both move a `SKILL.md`, and
`measurement_inputs` hashes the body of every skill a case holds. **13 cases go
stale** — the 8 that claim the renamed skill, and the 5 that hold `doctor`.

**Twelve of those thirteen are already stale, unmeasured, or below the three-run
floor today.** The board carries 2 measurements against 12 stale and 6 never
measured. So the marginal cost of this change is **one measurement**:

| | |
|---|---|
| Cases touched | 13 |
| Already owed before this change | 12 |
| **Live measurements this change destroys** | **1** — [`14-feedback-with-no-subject`](../../evals/14-feedback-with-no-subject/), 3 runs, $2.25 |
| New case owed when `@planned` drops | 1 |

Re-measuring the whole touched set at the floor is roughly **$27**, at the
board's own mean of $0.66 a run. That is the price of the backlog, not of this
change, and it is the maintainer's to spend or defer — the commit and the pull
request can be finished with a gap where the numbers go, and `verify.py` exits 2
until they are filled.

**Editing a description would have cost exactly the same 13 cases.** The hash
covers the skill body, so sharpening the wording in place was never the cheaper
option it looks like. Cost is not an argument against the rename here.

## What we are not doing

- **Not keeping `feedback` as an alias.** A second skill pointing at the first
  costs its description in every session, against `context-budget`, and
  re-creates the exact collision it exists to remove. The old name goes.
- **Not teaching `doctor` to read `CHANGELOG.md`.** Working out everything the
  method changed between a ledger's stamp and the installed version is the
  general mechanism this rule is one special case of, and it is a bigger change
  with an open boundary question in front of it — whether an audit may *apply*
  what it found, when `doctor`'s first refusal is *"Wiring anything"*. Filed as
  [#92](https://github.com/sargismarkosyan/livespec/issues/92) with the three
  options and a recommendation, rather than folded in here.
- **Not renaming the eval case directories.** `02-feedback-from-use`,
  `13-feedback-about-the-plugin` and `14-feedback-with-no-subject` keep their
  names. The board is keyed by directory name, so renaming one orphans its row
  outright rather than staling it — and as English they still describe their own
  scenario exactly.
- **Not rewriting history.** The seven change specs that name the skill
  ([`0001`](0001-the-gate-wiring-ledger.md), [`0002`](0002-setup-finishes-what-it-names.md),
  [`0005`](0005-the-first-persona.md), [`0009`](0009-whose-repository-whose-tracker.md),
  [`0016`](0016-captured-or-built.md), [`0018`](0018-said-once-not-searched-for.md),
  [`0019`](0019-what-would-end-it.md)) and every `CHANGELOG.md` entry keep it. They
  record what was true when they were written, and a record edited to agree with
  the present is not a record.
- **Not renaming `docs/feedback/`.** It holds images attached to open issues —
  a different sense of the word, named in
  [`method/repository.md`](../../method/repository.md), and untouched by any of
  this.
- **Not touching the persona file.** Its line about *their own `feedback` skill*
  stays word for word: it describes **their** skill, which is still called that,
  and after the rename the sentence reads more clearly rather than less. Editing
  it would trigger a separate confirmation for no change in meaning.
- **Not cutting the *filing what they found* workflow.** Named in *Who this is
  for* as the attempt this serves, and left to `refine-workflows`.

## Data

No storage contract here, and none in a consuming repository is touched. What
this writes in a consuming repository is the **record** — its `CLAUDE.md`, and
the bindings where they name a skill — which is what `doctor` already corrects.
No wiring, no gate, no threshold.

Data already stored in the old shape is the interesting case and it is the
`CLAUDE.md` in every repository that has already adopted: those keep saying
`/livespec:feedback` until somebody audits them, and the new rule is how that
audit stops being silent. Nothing migrates on its own, and this spec does not
pretend otherwise.

## Risks

- **`ids-are-permanent` is the promise that looks at risk and is not.** It
  covers a rule, workflow or persona id. A skill name is none of the three, and
  no eval case, gate or consuming test points at a skill by an id that must
  survive. What *does* point at it is the `skill:` tag in 8 case prompts, all of
  which move in the same commit and are checked by `evalsuite.py`, which fails a
  tag naming a skill that is not in `skills/`.
- **The new name carries a collision of its own.** `todo` is an app domain object
  in `todo-change`, the one repository this plugin is dogfooded against, and TODO
  is a comment convention everywhere. The guard is that *todo* stays out of the
  trigger list and the existing should-not-fire case is re-measured; the honest
  statement is that this trades a collision with a built-in tool for a weaker
  collision with a domain word, on the maintainer's explicit decision.
- **Muscle memory breaks with no error message worth reading.** Somebody typing
  `/livespec:feedback` after this ships gets nothing useful. Accepted: an alias
  costs context in every session forever to soften one week.
- **The audit half only reaches a repository somebody audits.** Named rather
  than hidden — the same limit [`0036`](0036-a-row-that-was-right-once.md)
  recorded. No skill here fires without being asked.
- **`always-green` is not at risk.** Nothing here runs in anybody's build.

## Acceptance checks

There is no app; this repository's deliverable is the pull request description.
What is checked by hand:

1. `python3 .github/scripts/verify.py` is green apart from exit 2, and the 2 is
   the 13 stale board rows and nothing else.
2. `claude plugin validate ./skills --strict` passes with the renamed directory,
   and `checks.py` still reports **eight** skills — the count in `CLAUDE.md`,
   `README.md` and `plugin.json` is unchanged by a rename, and `checks.py` fails
   a repository that says otherwise.
3. `grep -rn 'feedback' --include='*.md' .` returns only: `specs/changes/` and
   `CHANGELOG.md` history, `docs/feedback/` the directory, the loop's ordinary
   noun, the persona's line about their own skill, and the eval directory names.
   Nothing that reads as a reference to a skill in this plugin.
4. Start a session with the plugin installed and confirm the skill lists as
   `livespec:todo`, and that `/livespec:todo` invokes it.
5. Run `doctor` against a fixture whose `CLAUDE.md` names `/livespec:feedback` —
   `evals/32-*` and `evals/34-*` both already build one. It reports the name as
   reaching no skill and offers the row as it will read.
6. Run `doctor` against this repository, whose own `CLAUDE.md` names no skill by
   `/livespec:` prefix. It reports nothing about names.
7. `a-skill-the-record-names-is-one-that-exists` drops `@planned` in the
   implementing change, claimed by a case tagged with it. Expected to be a new
   case: `32`'s and `34`'s scaffolds each hold the right fixture but their
   graders are pointed at other faults, and pointing a second rule at them would
   make both cases ambiguous about what they proved.
