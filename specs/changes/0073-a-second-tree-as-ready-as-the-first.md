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
saying so, confirmed on its own before this spec. The evidence is the one
repository #166 came from: six worktrees open on the day of the report, two of
them opening merge requests five minutes apart, each readied by hand.

**The workflow is [`adopt-the-process`](../workflows/adopt-the-process.feature),
at the sitting** — the phase *Putting it in* in
[`trusting-the-spec-again`](../journeys/trusting-the-spec-again.md), steps 5–6.
The sitting grows by one offer and one proof. [The workflows
README](../workflows/README.md#reading-this-as-a-map) says a change that
lengthens adoption has to name which later attempt it shortens. This one
shortens every change started in a new tree after it — *The changes after*,
step 8, *many times a day*. Each of those currently starts with somebody
readying the tree by hand, or with an agent that hits a missing install or a
missing env file halfway through and stops to ask.

**The audit half sits in the same workflow**, in the part
[`0021`](0021-asked-not-assumed.md) added: asking months later whether the
process still holds. Tree readiness decays the same way a ledger row does. An
install step gets added, and the command that readies a tree never learns it.

## The job behind the request

To hand the next issue to the next agent in a tree of its own and trust that
the tree behaves like the first one. The gates run there, the app starts
there, and nothing in it collides with the trees already open. That has to
hold without anyone setting the tree up, and without the agent stopping to ask
where the secrets are.

**What they do today instead** is ready each tree by hand, and every tree comes
out different. In the repository #166 was filed from, two trees have their
packages and a third does not. The install is also what turns the pre-push hook on,
so **whether the gates run before a push depends on which tree the change was
made in**. Nothing says so. The tree without the install looks exactly like a
tree with a hook that passed.

## Why now

- **The cost is quiet, and it lands on the gates.** A tree missing its install
  is not a slow start. It is a tree where the local half of verification never
  runs, and the persona reads that as green. The method's own promise, *every
  version runs and is green*, gets checked in some trees and not in others.
- **Nothing in the method or the skills mentions a second tree.** `rg -i
  "worktree|parallel|\.env"` over `method/` and `skills/` finds nothing
  relevant.
  [`repository.md`](../../method/repository.md#branches-and-pull-requests) has
  one `git switch -c` on one checkout. `setup` wires the gates for the tree it
  is standing in, and `doctor` re-reads that tree only.
- **It has already bitten this repository once.** #127 was a hook run from a
  linked worktree that followed `GIT_DIR` onto the real branch. Trees are
  already how the maintainer works here. The method is behind the practice.
- **The number collision in #167 is the same pace showing up elsewhere.** It
  gets its own spec. It is named here because two issues filed from the same
  report on the same day are a pace the method was not written for.

## The end value

Starting a change in a new tree is one command. After it, the tree is as ready
as the first: the same gates run before a push, the app comes up beside the
others, and the secrets are reachable without a copy. When that stops being
true, the next audit says so rather than the next agent stalling.

**How we would know it worked:**

- In a repository set up after this ships, the bindings name the command and
  the date a throwaway tree was last watched going green. Running that command
  in a new tree and then verification there is green with nothing else typed.
- In the repository #166 came from, `doctor` reports the fresh-tree row
  *open*. Once `setup` has run, it reports *clear*, and readying a sixth tree
  is one line.

## What changes

1. **The method, [`repository.md`](../../method/repository.md) — a section
   *Several changes at once*** under *Branches and pull requests*. It says five
   things and names no command:
   - several changes in flight is the ordinary case: one change, one branch,
     one tree;
   - a fresh tree is readied by **one command the bindings name**, because a
     tree readied by hand is readied differently from the last, and the
     difference that matters is the one nobody sees (a hook turned on as a side
     effect of an install only one tree had);
   - what two trees would contend for is **worked out per tree** by that
     command and named — ports, data directories, database names, caches that
     are not safe to share;
   - what every tree shares, secrets above all, **comes from one place each
     tree points at**. It is never copied into a tree, and never committed. A
     file mixing the two kinds, such as a key beside a port, is split, because
     a shared port is the collision above and a copied secret is one copy per
     tree to rotate;
   - it is **watched, not assumed**: a throwaway tree readied by the command
     runs verification green, and the app beside the first tree's, before the
     bindings say a fresh tree works.

2. **The bindings template, [`bindings.md`](../../templates/bindings.md) — two
   rows.**
   - **A fresh tree**: the command, or *nothing — a fresh checkout runs as it
     stands*, and the date a throwaway tree was last watched going green, or
     *unproven* with why.
   - **What trees keep apart**: what each tree has its own of and how the
     command works it out, and what they share and where it comes from.

3. **[`setup`](../../skills/setup/SKILL.md).**
   - Section 1 reads two more things. The untracked files verification and the
     app need, meaning ignored files the first tree has and a fresh one would
     not. And what binds a port or a data directory.
   - Section 4 gains a subsection after the hook offer: *Then make a second tree
     as ready as the first*.
     - It works out the steps.
     - Where there is more than one, it offers a script that does them, **said
       and then waited on, the way the hook is**. A decline writes the steps
       into the row, in order.
     - It readies a throwaway worktree outside the repository with the command,
       runs verification there, and — where there is an app — starts it beside
       the first tree's.
     - It removes the tree and writes the row from what came back.
   - Section 8's report gains the line. *What this skill refuses* gains
     *copying a secret into a tree*.
   - The script is repository tooling, like the hook, and not application code.
     Where only an app change would let two trees run at once, such as a port
     fixed in code, the row names it and the hand-back hands it to the person.

4. **[`doctor`](../../skills/doctor/SKILL.md) and
   [`tools/doctor.py`](../../tools/doctor.py) — two checks.**
   - `check:fresh-tree-row`, *mechanical, record*: the bindings carry the
     row. Missing is *open*, closed by the sitting.
   - `check:fresh-tree-green`, *judgment, wiring*: the tool pre-fills it with
     the command the row names. The audit readies a throwaway tree with it,
     runs verification there and removes it. Red is *open*, with the first
     failing line. A secret this session cannot reach is *not-read*, with why.
   - Nothing the audit does edits the command. `check:record-only` stays true
     because the throwaway tree lives outside the working tree and is gone
     before the record is validated.

5. **[`gates.md`](../../method/gates.md#the-checks-an-audit-makes) — the two
   ids**, `since` reading `next`. The pull request carries `## Ids`: added
   `check:fresh-tree-row`, `check:fresh-tree-green`.

6. **This repository's own bindings** gain both rows, proven the same way:
   - **A fresh tree:** `git worktree add`, and nothing after it. The gates are
     standard library, and `core.hooksPath` is shared config pointing at a
     tracked `.githooks`, so a clone that opted in has the hook in every tree.
   - **What trees keep apart:** `evals/results/` is per tree already. What the
     command cannot separate is named: the account's session limit is one
     across every tree, so two trees running the suite spend from the same
     limit.

7. **The cases and the test.**
   - A unit test under `tests/` claims `a-fresh-tree-row-is-there`, against
     `doctor.py`.
   - Eval cases claim the other five rules. The expected cut is three:
     - a `setup` case whose fixture needs an install, a hook and an env file
       holding a key beside a port (`a-fresh-tree-is-one-command`,
       `what-two-trees-fight-over-is-derived`, `a-shared-secret-is-pointed-at`);
     - a `setup` case whose command leaves the hook off
       (`a-fresh-tree-is-watched-going-green`);
     - a `doctor` case whose command has fallen behind an install step
       (`a-fresh-tree-is-re-proven`).

**Rules added** — all `@planned` until the implementing commit:

| Rule id | Feature file | New or changed |
|---|---|---|
| `a-fresh-tree-is-one-command` | [`features/setup/a-second-tree.feature`](../features/setup/a-second-tree.feature) | new |
| `a-fresh-tree-is-watched-going-green` | same | new |
| `what-two-trees-fight-over-is-derived` | same | new |
| `a-shared-secret-is-pointed-at` | same | new |
| `a-fresh-tree-row-is-there` | [`features/wiring/a-second-tree.feature`](../features/wiring/a-second-tree.feature) | new |
| `a-fresh-tree-is-re-proven` | same | new |

**Prose moved with it:** a line in the persona, confirmed on its own, and
**tree** / **fresh tree** in [`spec.md`](../spec.md)'s vocabulary.

## What we are not doing

- **The numbering collision.** That is #167, and it gets its own spec.
- **How an agent harness schedules parallel sessions.** Which tool opens the
  trees, how many sessions run at once and how they are named belong to the
  harness, and differ between harnesses. The method says what a tree must be.
  It does not say who opens one.
- **A tree-making tool shipped in `tools/`.** A plugin script that creates
  worktrees would be a second command beside the repository's own, and a
  consuming repository's CI never has it. The command is the repository's, in
  its own language, like the gates.
- **A gate in CI.** CI checks out one commit into one tree, so a fresh-tree
  check there passes forever while looking enforced — the reason
  `local:journey-freshness` reads *not applicable* here. The proof is local,
  at the sitting and at the audit.
- **A row in the gate wiring ledger.** Tree readiness refuses no change, and a
  courtesy recorded as a refusal is the failure
  [`gates.md`](../../method/gates.md#and-what-is-not-wiring-at-all) describes
  for the hook. It is a binding, not a gate. The audit reads it back through a
  check, the way it reads the sketch row.
- **Choosing a mechanism for shared secrets.** Symlink, a per-user directory,
  a secrets manager, the platform's own store: the method states the
  invariant, and the bindings name the mechanism.
- **Allocating ports.** The method says they are worked out per tree. The
  scheme, whether an offset from a tree index or a free port found at start,
  belongs to the repository.

## Data

No storage contract moves. A consuming repository's bindings gain two rows.
Bindings written before this ship without them, so the first audit after the
upgrade reports `check:fresh-tree-row` *open* and names the sitting, which is
how every row the method has added since 0.21.0 has arrived.

## Risks

- **A longer sitting.** One offer and one proof, paid once per repository, is
  the trade the workflows README requires this spec to name, and it is named
  above.
- **A slow proof.** A repository whose install takes minutes makes the sitting
  wait minutes. That is the same cost as proving the gates fire. The row can
  say *unproven* with why, and it can never say *works* without the run.
- **`never-implements`.** The script is tooling the sitting writes, in the
  same place and on the same terms as the hook. Anything that needs the app to
  change — a port fixed in code, a data path hard-coded — is named and handed
  back, and never edited.
- **`always-green`.** Nothing here reaches a user's build. The command is not
  in CI, the proof runs locally, and a consuming repository's pipeline is
  unchanged.
- **A throwaway tree left behind.** An audit that is interrupted could leave a
  worktree entry. It is created outside the repository, and removal is part of
  the rule, not a courtesy (`a-fresh-tree-is-re-proven`, *the audit is over*).
  #127 is why a tree made from inside a hook is not the path.
- **Eval spend.** Editing `setup` and `doctor` stales every board entry that
  holds either skill, and the three new cases start unmeasured. The stale set
  and its price are read off the board at implementation and named in the
  pull request. None of it runs without the maintainer's yes.

## Acceptance checks

1. Read *Several changes at once* in `repository.md` and confirm it names no
   command, file or language.
2. In this repository, with the implementation on a branch: `git worktree add`
   a throwaway tree outside the checkout, run
   `python3 .github/scripts/verify.py` there, and see it finish with the same
   exit as in the main tree. Remove the tree, and confirm `git worktree list`
   shows only what was there before.
3. In the repository #166 came from, run `/livespec:doctor` and see
   `check:fresh-tree-row` open. Run `/livespec:setup` over it and see the
   script offered, not written. Once it is accepted, see a sixth tree readied
   by one line with its hook on.
