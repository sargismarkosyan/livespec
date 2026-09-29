# Spec 0073: a second tree as ready as the first

- **Status:** proposed
- **Issue:** [#166](https://github.com/sargismarkosyan/livespec/issues/166)
- **Numbered 0073, not 0068**, because `main` ends at 0067 and the open
  [#165](https://github.com/sargismarkosyan/livespec/pull/165) already holds
  0068–0072. The rule in `refine-spec` would have given this spec 0068, which
  is [#167](https://github.com/sargismarkosyan/livespec/issues/167) happening
  in this repository. The number was chosen by hand, and #167 still owns the
  fix.

## Who this is for

**Ren — [`agent-accelerated-owner`](../personas/agent-accelerated-owner.md) —
with several changes in flight in one repository, one tree each.** This is
their pace, not a new person. The persona already goes through an agent
because there is more to do than there are hours, and an agent makes a second
change as cheap to start as the first. The persona gains one observed line
saying so, confirmed on its own before this spec.

**Whatever harness they drive it through.** The maintainer runs livespec under
Pi as often as under Claude Code, with models from more than one provider
([#155](https://github.com/sargismarkosyan/livespec/issues/155)). Where a
repository's trees live and how they are made is a fact about the
repository. It is not a fact about the harness, so nothing this spec adds
names one.

**The workflow is [`adopt-the-process`](../workflows/adopt-the-process.feature),
at the sitting** — the phase *Putting it in* in
[`trusting-the-spec-again`](../journeys/trusting-the-spec-again.md), steps 5–6.
The sitting grows by one offer and one proof. [The workflows
README](../workflows/README.md#reading-this-as-a-map) says a change that
lengthens adoption has to name which later attempt it shortens. This one
shortens every change started in a new tree after it — *The changes after*,
step 8, *many times a day*. It also shortens the step nobody currently takes
at all: clearing the trees away afterwards.

**The audit half sits in the same workflow**, in the part
[`0021`](0021-asked-not-assumed.md) added: asking months later whether the
process still holds. Tree readiness decays the same way a ledger row does. An
install step gets added, and the command that makes a tree never learns it.

## The job behind the request

To hand the next issue to the next agent in a tree of its own, and to trust
three things. The tree behaves like the first one: the gates run, the app
starts, and nothing collides. Every tree can be found in one place. And
clearing them away afterwards is one command that cannot throw away work.

**What they do today instead** is make each tree by hand, somewhere, and
never clear them.

- **In the repository #166 came from**, two of the trees have their packages
  and a third does not. The install is also what turns the pre-push hook on,
  so **whether the gates run before a push depends on which tree the change
  was made in**. Nothing says so.
- **In this repository**, on the day this spec was written, there were 18
  linked trees, split across two folders (`livespec-issues/` and
  `livespec-worktrees/`), with overlapping names. 17 had nothing to lose:
  clean, and every commit already on `main`. One had two uncommitted files.
  Nothing said which was which. It took a survey by hand to tell them apart,
  and the survey was run because the maintainer asked how to remove them all
  at once. Beside the trees sat a hand-made `.tasks/` folder of per-issue
  briefs and `launch-N.sh` scripts: a parallel setup built by hand, because
  nothing gave one.

## Why now

- **The cost is quiet, and it lands on the gates.** A tree missing its install
  is not a slow start. It is a tree where the local half of verification never
  runs, and the persona reads that as green.
- **Trees pile up, and the one with work in it hides among them.** Eighteen
  trees, one of them holding uncommitted work, with no way to tell it from the
  seventeen that could go. The only safe move is to leave all eighteen, and
  that is how they got to eighteen.
- **Nothing in the method or the skills mentions a second tree.** `rg -i
  "worktree|parallel|\.env"` over `method/` and `skills/` finds nothing
  relevant.
- **Each harness has invented its own answer, and they disagree.** Claude Code
  puts trees under `.claude/worktrees/` and copies ignored files named in
  `.worktreeinclude`. Cursor runs `.cursor/worktrees.json` and puts trees
  where it likes. A repository that adopts one of those has bound its tree
  setup to that harness. Anyone on another harness, or the same person
  switching, gets bare trees.
- **It has already bitten this repository once.** #127 was a hook run from a
  linked worktree that followed `GIT_DIR` onto the real branch.

## The end value

Starting a change in a new tree is one command, and the tree is as ready as
the first. Every tree lives in one place the bindings name. One command lists
them with whether each is safe to remove, and clears every one that is, and
keeps and names the one with work in it. When readiness stops being true, the
next audit says so, before the next agent stalls on it.

**How we would know it worked:**

- In a repository set up after this ships, the bindings name the directory,
  the command, and the date a throwaway tree was last watched going green.
  Making a tree with it and running verification there is green with nothing
  else typed, under any harness or none.
- Listing the trees in this repository after a month of work shows each one's
  state. Cleaning them leaves only the trees with work in them.
- In the repository #166 came from, `doctor` reports the trees row *open*.
  Once `setup` has run, it reports *clear*.

## What changes

1. **The method, [`repository.md`](../../method/repository.md) — a section
   *Several changes at once*** under *Branches and pull requests*. It says
   six things and names no command, path or harness:
   - several changes in flight is the ordinary case: one change, one branch,
     one tree;
   - **every tree of a repository lives in one directory the bindings name**,
     so they can be found, and **one command makes, lists and cleans them**;
   - a fresh tree is **made ready by that command**, because a tree readied by
     hand is readied differently from the last, and the difference that
     matters is the one nobody sees;
   - what two trees would contend for is **worked out per tree** by that
     command and named — ports, data directories, database names, caches that
     are not safe to share;
   - what every tree shares, secrets above all, **has one source outside every
     tree's history**, reaches each tree as an ignored file, and is never
     committed. A file mixing the two kinds, such as a key beside a port, is
     split;
   - **cleaning goes by the repository's own record of its trees, never by
     deleting a directory.** It removes a tree only when it has nothing to
     lose, and it lists every other tree with why it stayed. The record
     finds every tree, including one a harness made somewhere else. A
     deleted directory leaves the record claiming a tree that is gone.

   **A harness's own tree mechanism calls the command. The command never
   calls the harness.** That one sentence keeps a harness from becoming where
   the repository's setup lives.

2. **The bindings template, [`bindings.md`](../../templates/bindings.md) — two
   rows.**
   - **Trees**: the directory they live in, the command and its three verbs,
     and the date a throwaway tree was last watched going green, or
     *unproven* with why.
   - **What trees keep apart**: what each tree has its own of and how the
     command works it out, and what they share and where its one source is.

3. **[`setup`](../../skills/setup/SKILL.md).**
   - Section 1 reads three more things:
     - the untracked files verification and the app need, meaning ignored
       files the first tree has and a fresh one would not;
     - what binds a port or a data directory;
     - where the repository's existing trees already are, from its own
       record of them.
   - Section 4 gains a subsection after the hook offer: *Then make a second
     tree as ready as the first*.
     - It proposes the home. The recommendation is **a `.worktrees/`
       directory at the repository root, ignored**. It is inside the
       repository, so a newcomer sees it and deleting the checkout deletes
       the trees. It sits under no harness's directory.
     - It offers **the command with three verbs, `new`, `list` and
       `clean`**, in the repository's own language, **said and then waited
       on, the way the hook is**. A decline writes the steps into the row, in
       order.
     - Where a harness in use has its own setup hook, the offer includes
       pointing that hook at `new`. This is never a second copy of the steps.
     - It makes a throwaway tree with `new` and runs verification there.
       Where there is an app, it starts the app beside the first tree's. It
       also runs verification in the first tree while the throwaway exists,
       to catch a tool walking into the ignored directory.
     - It cleans the throwaway with `clean`, and writes the row from what
       came back.
   - Section 8's report gains the line. *What this skill refuses* gains
     *committing a secret* and *removing a tree with work in it*.
   - The command is repository tooling, like the hook, and not application
     code. Where only an app change would let two trees run at once, such as
     a port fixed in code, the row names it and the hand-back hands it to the
     person.

4. **[`doctor`](../../skills/doctor/SKILL.md) and
   [`tools/doctor.py`](../../tools/doctor.py) — two checks.**
   - `check:trees-row`, *mechanical, record*: the bindings carry the row.
     Missing is *open*, closed by the sitting.
   - `check:fresh-tree-green`, *judgment, wiring*: the tool pre-fills it with
     the command the row names. The audit runs `new` for a throwaway tree,
     runs verification there, and runs `clean`. Red is *open*, with the first
     failing line. A secret this session cannot reach is *not-read*, with
     why.
   - The audit never edits the command, and never cleans any tree but its own
     throwaway. Clearing the others is the person's call.

5. **[`gates.md`](../../method/gates.md#the-checks-an-audit-makes) — the two
   ids**, `since` reading `next`. The pull request carries `## Ids`: added
   `check:trees-row`, `check:fresh-tree-green`.

6. **This repository's own bindings, command and proof.**
   - **Trees:** `.worktrees/`, ignored, with a standard-library `trees.py`
     (`new`, `list`, `clean`). `new` needs only `git worktree add`. The gates
     take no dependencies, and `core.hooksPath` is shared config pointing at
     a tracked `.githooks`, so a clone that opted in has the hook in every
     tree.
   - **What trees keep apart:** `evals/results/` is per tree already. What the
     command cannot separate is named: the account's session limit, which is
     one across every tree.
   - `trace.py` and `evalsuite.py` read fixed paths from the root. The proof
     confirms that neither walks into `.worktrees/`.

7. **The cases and the test.**
   - Unit tests under `tests/` claim `the-trees-row-is-there` against
     `doctor.py`, and `clean-removes-only-what-is-safe` against this
     repository's `trees.py`. Those are both code, so both are held the
     ordinary way.
   - Eval cases claim the other five rules. The expected cut is three:
     - a `setup` case whose fixture needs an install, a hook and an env file
       holding a key beside a port (`trees-have-one-home-and-one-command`,
       `what-two-trees-fight-over-is-derived`, `a-shared-secret-has-one-source`);
     - a `setup` case whose command leaves the hook off
       (`a-fresh-tree-is-watched-going-green`);
     - a `doctor` case whose command has fallen behind an install step
       (`a-fresh-tree-is-re-proven`).

**Rules added** — all `@planned` until the implementing commit:

| Rule id | Feature file | New or changed |
|---|---|---|
| `trees-have-one-home-and-one-command` | [`features/setup/a-second-tree.feature`](../features/setup/a-second-tree.feature) | new |
| `a-fresh-tree-is-watched-going-green` | same | new |
| `what-two-trees-fight-over-is-derived` | same | new |
| `a-shared-secret-has-one-source` | same | new |
| `clean-removes-only-what-is-safe` | same | new |
| `the-trees-row-is-there` | [`features/wiring/a-second-tree.feature`](../features/wiring/a-second-tree.feature) | new |
| `a-fresh-tree-is-re-proven` | same | new |

**Prose moved with it:** a line in the persona, confirmed on its own, and
**tree** / **fresh tree** in [`spec.md`](../spec.md)'s vocabulary.

## What we are not doing

- **The numbering collision.** That is #167, and it gets its own spec.
- **Adopting any harness's tree convention.**
  - `.claude/worktrees/`, `.worktreeinclude` and `.cursor/worktrees.json` are
    each one harness's answer.
  - Binding a repository's setup to one of them strands everybody on
    another, and the maintainer is often on Pi.
  - Where a repository uses one, it calls the command.
  - A tree a harness makes elsewhere is still listed and cleaned, because
    `list` and `clean` read the repository's own record of its trees rather
    than a directory.
- **How a harness schedules parallel sessions.** Which tool opens the trees,
  how many sessions run at once and how they are named belong to the
  harness.
- **A tree command shipped in the plugin's `tools/`.** Readiness is
  repository-specific: its install, its env, its ports. And a plugin script
  exists only where the plugin is installed. The command is the repository's,
  in its own language, like the gates. This repository gets its own, because
  it is a repository too.
- **A gate in CI.** CI checks out one commit into one tree, so a fresh-tree
  check there passes forever while looking enforced — the reason
  `local:journey-freshness` reads *not applicable* here.
- **A row in the gate wiring ledger.** Tree readiness refuses no change. It is
  a binding, read back by a check, the way the sketch row is.
- **The audit clearing anybody's trees.** It cleans only its own throwaway.
  The others hold somebody's work, or might, and clearing them is the
  person's call.
- **Choosing a mechanism for the shared source, or a port scheme.** The method
  states the invariant, and the repository chooses the mechanism.

## Data

No storage contract moves. A consuming repository's bindings gain two rows.
Bindings written before this ship without them, so the first audit after the
upgrade reports `check:trees-row` *open* and names the sitting, which is how
every row the method has added since 0.21.0 has arrived. Trees that already
exist are left where they are. `list` finds them wherever they live, and
nothing moves one.

## Risks

- **A longer sitting.** One offer and one proof, paid once per repository, is
  the trade the workflows README requires this spec to name, and it is named
  above.
- **`clean` deleting work.** This is the one destructive verb, so the rule is
  written as what it keeps. It removes only a tree with no uncommitted or
  untracked files, with every commit on the main branch or its merged remote
  branch deleted, that is not locked and is not the current tree. It takes
  the local branch with it only when git agrees the branch is merged. Its
  unit test is the one in this change that must break on purpose.
- **Nested trees and the tools that walk them.** A home inside the repository
  is the easy one to find, and it is also one a test runner or watcher can
  wander into. The proof is written to catch that, not to assume it away.
- **`never-implements`.** The command is tooling the sitting writes, on the
  same terms as the hook. Anything that needs the app to change is named and
  handed back.
- **`always-green`.** Nothing here reaches a user's build. The command is not
  in CI, and the proof runs locally.
- **Eval spend.** Editing `setup` and `doctor` stales every board entry that
  holds either skill, and the three new cases start unmeasured. The stale set
  and its price are read off the board at implementation and named in the
  pull request. None of it runs without the maintainer's yes.

## Acceptance checks

1. Read *Several changes at once* in `repository.md` and confirm it names no
   command, path or harness.
2. In this repository, with the implementation on a branch:
   - `trees new` a throwaway tree, run `python3 .github/scripts/verify.py`
     there, and see the same exit as in the main tree;
   - run `trees list` and see it listed;
   - run `trees clean` and see it gone, with any tree holding work still
     listed and its reason given.
3. The same `trees new` from a Pi session and from a Claude Code session
   gives the same tree in the same place.
4. In the repository #166 came from, run the audit and see `check:trees-row`
   open. Run `setup` over it and see the command offered, not written.
