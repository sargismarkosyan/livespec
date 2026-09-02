# Spec 0031: a missing tool is not a missing page

- **Status:** approved
- **Issue:** [#82](https://github.com/sargismarkosyan/livespec/issues/82)
- **Depends on:** [`0029`](0029-drawn-before-it-is-built.md), which introduced
  the sketch and, in the same breath, decided the thing this corrects.

## Who this is for

[`agent-accelerated-owner`](../personas/agent-accelerated-owner.md), in
[`adopt-the-process`](../workflows/adopt-the-process.feature), at step 4 — the
same seat [`0029`](0029-drawn-before-it-is-built.md) was written for, and the
one step of the loop the person holds rather than the agent.

The persona line this turns on is not the one about hours. It is the plainest
fact in the file and the easiest to skip past: *at a terminal, in an agent
session, inside the repository itself.* Somebody sitting there can open a file
on their own machine. That is what makes a written page a real page for this
person rather than a lesser substitute for a published one — and it is why an
agent deciding there is nothing it can do is wrong about their situation, not
merely unlucky in its host.

The second line that bites is *more than one repository at once*. Those sessions
do not all run on the same host, and a promise that holds only where one
particular tool is present is a promise that lands in some of their repositories
and not others, with nothing saying which.

## The job behind the request

Be handed the evidence at the step where the decision is theirs — in whatever
session they happen to be sitting in.

Not *have a sketch published*. Publishing is a mechanism, and the request that
raised this said so twice: first asking for something to review beside the spec,
then, unprompted, correcting the reading — *"Not referring to the tool, by the
way […] If there are no artifact tool, then it should be HTML page."* The job is
the evidence arriving. The mechanism is whatever the session can do.

## Why now

Because the promise [`0029`](0029-drawn-before-it-is-built.md) made stopped
being kept on the first sitting after it shipped, and it stopped being kept
silently.

Running `refine-spec` in `planning-ai-dashboard` on 2026-09-02 — its issue #22,
its spec 0024 — no sketch was produced. There was a real before and after and
there was a session that could write files. What there was not was the one tool
`refine-spec` names.

**This is not a slip in one sentence.** The narrowing is written into three
places at once, which is why it needs a spec rather than an edit:

- [`skills/refine-spec/SKILL.md:211`](../../skills/refine-spec/SKILL.md) offers
  the step *"where the session has a tool that can (in Claude Code, `Artifact`)"*
  — one mechanism, named as though it were the category.
- The escape hatch at [`:243`](../../skills/refine-spec/SKILL.md) reads *"Where
  the session has no way to publish a page"*, which an agent holding the line
  above resolves against `Artifact` and nothing else.
- [`0029`](0029-drawn-before-it-is-built.md) argued it deliberately, under *The
  portability question*: *"A host with no way to publish a page is that rule's
  ordinary case."* It routed the whole condition to
  [`an-unreachable-step-is-said-not-searched-for`](../features/reach/absent-means.feature),
  which is the right rule for a step that cannot be taken and the wrong rule for
  one that can be taken differently.
- [`29-nowhere-to-draw-it`](../../evals/29-nowhere-to-draw-it/prompt.md) then
  **fails** a session for *"writing an HTML file into the repository"*. The case
  written to hold the promise scores the fallback as the failure.

What it costs is the whole of what 0029 bought, in every session whose host
lacks that tool — and worse than nothing, because the person is not told. 0029's
own measurement is the evidence that the *stated* absence works: all three
with-arm sessions named the absent tool in a line. A real sitting, with a real
before and after, produced neither the page nor the line.

**And the ambiguity is doing the work, not the missing sentence.** An agent
reading *"no way to publish a page"* beside a single named tool has been handed
a binary check. It takes the branch that is written down.

## The end value

The evidence arrives at step 4 in any session that can write a file, which is
very nearly all of them — as a page they open, at a path handed over with the
links — and the line saying it could not be drawn means what it says.

**How we would know it worked:** the next `refine-spec` sitting on a host with
no publishing tool ends with a path to open rather than a step nobody mentioned.
That is checkable on the next sitting in `planning-ai-dashboard`, which is where
this was found. The slower signal is 0029's own: nobody writes the page by hand
after the hand-back.

## What changes

- **`refine-spec` names two mechanisms in order.** Publish the page where the
  host has a tool for it; otherwise **write it as an `.html` file the person
  opens**, and hand the path over with the links. The second is ordinary, not a
  workaround, and it is written down so that nothing has to be searched for.
- **The written page is not a record.** It goes somewhere the repository does
  not track, it is not part of the spec commit, and the change spec stays the
  only thing the repository keeps. A revision rewrites that same path — the same
  *replaces, never accumulates* rule the published page already has, with a file
  path as the address.
- **The escape hatch narrows to what it was always meant to mean**: a session
  that can neither publish a page nor write a file. That, and only that, is one
  line and a hand-back.
- **`method/process.md` loses "nowhere in this session to render one"** for *no
  way in this session to produce one in any form*. The portable half, naming no
  tool and no format — the method already had the better sentence and only has
  to stop being readable as a check against one thing.
- **A new case, `33-no-tool-to-publish-with`, claims the new rule.** It inherits
  the session
  [`29-nowhere-to-draw-it`](../../evals/29-nowhere-to-draw-it/prompt.md) was
  written for — a real before and after, `Write` granted, no publishing tool —
  because under this change the behaviour that case currently fails is the
  behaviour that is owed.
- **`29-nowhere-to-draw-it` keeps its name and its rule**, and gets the prompt
  its rule can still be reached by: a change with no before, no ledger and no
  count that moves. **This is not what the spec said before it was built.** It
  said the case would be re-pointed at the new rule and renamed, and that turned
  out to break two things at once — the rename orphans three links in shipped
  [`0029`](0029-drawn-before-it-is-built.md), and re-pointing it makes 0029's
  own table say that case claims a rule it no longer claims. A shipped spec
  quietly stopping being true is the failure this repository exists to prevent,
  and it is not worth a tidier directory name.

**Rules added or changed** — the `@rule:` ids in `specs/features/`:

| Rule id | Feature file | New or changed |
|---|---|---|
| `a-missing-tool-is-not-a-missing-page` | `features/showing/before-it-is-built.feature` | new, `@planned` |
| `an-absent-sketch-is-said-rather-than-filled` | `features/showing/before-it-is-built.feature` | changed — its first example's session is now one that can *neither* publish a page *nor* write a file. Same id, same promise, said so it cannot be read as a check against one tool |

`the-decision-gets-what-the-prose-cannot-carry` and
`what-is-shown-is-not-the-spec-again` keep their text and their `@planned` tags.
Their in-file comments change, because the reason those tags are on changes —
see below.

### What this does to the two rules that could not be reached

0029 shipped them `@planned` on an honest reason: *a headless session — the only
kind a case runs in — has no way to render a page at all, so no arm can watch a
sketch being drawn.* **That reason expires with this change.** A sketch written
to a file is a file, and a file is readable by a grader.

They stay `@planned` anyway, and the comments in the feature file are corrected
to say why: nothing claims them yet. That is a smaller and more ordinary reason
than the one it replaces, and leaving the old wording in place would be exactly
the failure this repository exists to prevent — a spec-layer sentence that
quietly stopped being true.

Writing those cases is its own change. Both are judgments about *what is in* a
sketch — evidence or decoration, drawn or invented — and 0029 was right that no
gate can check that. A case can, because a case is a model reading the page. It
needs graders that read a produced file rather than the last message, which no
case here does yet, and it is worth its own spec rather than riding inside this
one.

## What we are not doing

- **Un-planning the two content rules**, per the section above. Named as newly
  possible, deliberately not taken.
- **Committing the sketch, linking it from the change spec, or putting it in the
  pull request body.** 0029 ruled on all three and nothing here reopens them.
  The repository already has the precedent in its own `.gitignore`, for
  `evals/results/`: *"a measurement of one moment, not a record the repository
  keeps."* A sketch is a page for one decision. Same reasoning, same treatment.
- **Markdown instead of HTML.** The sketch exists because prose in a terminal
  cannot put two states side by side. A markdown file is prose in a file, and
  picking it would deliver the mechanism while dropping the reason.
- **Writing a file even where a publishing tool exists.** A published page has
  an address that survives the session and needs nothing on the reader's disk.
  Where the host has one it stays first.
- **The other three `refine-*` skills.** 0029 ruled `refine-spec` only, on the
  grounds that their evidence *is* prose. That ruling is untouched.
- **A binding for which mechanism a repository uses.** 0029 settled this: the
  condition is a fact about the session, not about the repository, and a binding
  for it would be a claim about somebody else's terminal. The skill asks at the
  moment it needs the answer.
- **Making any of it a gate.** Unchanged and for the unchanged reason: a gate
  that can only check a file exists is satisfied by a decorated summary.
- **Teaching `doctor` to catch a skipped step.** The issue asked. It cannot:
  `doctor` audits wiring recorded in a repository's `specs/setup/README.md`, and
  an instruction skipped inside one session leaves nothing in repository state
  for a later audit to find. That is a fact about what `doctor` is, not a gap in
  it, and the fallback above is what actually closes the reported hole.

## Data

No storage contract moves. `specs/spec.md` needs no new vocabulary — **sketch**
is already defined there as *what the person deciding on a change spec is shown
beside it*, which says nothing about how it is produced, and that definition is
the one this change is enforcing rather than amending.

`evals/board.json` gains no field, and **this spec commit stales nothing**: the
only case claiming a rule in the edited feature file is
[`29-nowhere-to-draw-it`](../../evals/29-nowhere-to-draw-it/prompt.md), which
has never been measured and has no row. `verify.py` is green on this commit.

**The implementing change is where the bill lands.** `measurement_inputs` hashes
a case's own files, the text of the rules it claims, and the bodies of the
skills it holds — all three move:

| What moves | What goes stale | What it costs |
|---|---|---|
| `skills/refine-spec/SKILL.md` | [`01-solution-shaped-request`](../../evals/01-solution-shaped-request/) — 3 runs, Δ +1.00, measured 2026-09-01 at `773ecd0` for $2.51 | ~$2.50 to re-measure |
| `29-nowhere-to-draw-it` — new prompt and grader, same name, same rule | nothing; never measured, no row | ~$1.80 to measure |
| `33-no-tool-to-publish-with`, claiming the new rule | nothing; a new row | ~$1.80 to measure |

**About $6, and it is the maintainer's to approve.** The implementing commit and
its pull request can be finished with a gap where the numbers go: `verify.py`
exits **2**, which is the red that means nothing is broken and a run is owed —
[`repository.md`](../../method/repository.md), *Commits*, says what that commit
then owes.

`method/process.md` is in no column. No case holds it, which is a fact about
what the board measures rather than a claim that it matters less.

## Risks

- **A file nobody opens.** A published page is a link; a path is a path, and a
  person short of hours may not open it. This is the change's real exposure and
  there is no mitigation inside it — the hand-back gives the path with the links
  and the person decides. It is still strictly better than the current state,
  where there is nothing to not-open and no line saying so.
- **The page gets committed.** The likeliest mechanical failure: an agent
  finishing a spec commit sweeps up an untracked `.html` sitting in the tree.
  *the spec is committed* is the example written for it, and the untracked
  location is the first defence rather than the last.
- **The escape hatch is read as gone.** It is not: a session that can do neither
  still says it once and hands back. Narrowing a hatch is how a hatch quietly
  becomes unavailable, so the rule states both halves in one sentence rather
  than leaving the survivor to be inferred.
- **Search creep.** [`process.md`](../../method/process.md) is right that a
  session hunting for a way to perform an unavailable step ends with nothing
  written down. This does not license the hunt — it removes the need for one, by
  naming the second mechanism outright. What the skill must never gain is *look
  for another way*; what it gains is one more way, written down.
- **`context-budget` is untouched.** No description moves; body text costs
  nothing until `refine-spec` fires.
- **`never-implements` is untouched.** An `.html` sketch is not application
  code, and `refine-spec` already writes files — spec files and feature files.
  What is new is the kind of file, not the fact of writing one.
- **`always-green` is untouched.** No build depends on a sketch, here or in any
  consuming repository.
- **`ids-are-permanent` is respected**, and an eval case directory turned out to
  behave like one anyway. No rule id is renamed or reused, and the case
  directory that was going to be renamed is not: three links in a shipped spec
  point at it, and the gate that catches a dangling link is what found this.
  Worth knowing for next time — a case directory is not covered by the promise
  and is still not free to move.

## Acceptance checks

There is no screen here. What a person does by hand:

1. Run `refine-spec` in a repository, on a request with a real before and after,
   in a session with **no** publishing tool and a file-write tool. A page is
   written, its path is handed over with the links, and the step is not
   described as one that could not be taken.
2. Open it. It is the sketch 0029 specified — what it is now beside what it
   would be, what moves and what stays with the reason, a count that changed, a
   link to the change spec — and none of the spec's four headings are in it.
3. `git status` after the spec commit. The page is not in it.
4. Ask for a change to the spec and take the hand-back again. The same path is
   rewritten; there is no second file.
5. Run it in a session with a publishing tool. A published page, as before —
   nothing about this change makes a file the first choice.
6. `python3 .github/scripts/verify.py` — green on this spec commit; exit 2 on
   the implementing commit until the three cases in *Data* are measured, which
   is the maintainer's spend to approve.
