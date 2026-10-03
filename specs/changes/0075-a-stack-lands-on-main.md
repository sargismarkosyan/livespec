# Spec 0075: a stack lands on main

- **Status:** proposed
- **Issue:** [#170](https://github.com/sargismarkosyan/livespec/issues/170)

## Who this is for

**Ren — [`agent-accelerated-owner`](../personas/agent-accelerated-owner.md) —
with several changes in flight in one repository, one tree each**, where
some of those changes depend on others. That persona line was added by
[`0073`](0073-a-second-tree-as-ready-as-the-first.md). Nothing about who this
is for moves.

**The workflow is [`adopt-the-process`](../workflows/adopt-the-process.feature).**
- The sitting gains one read-back and one offer, at steps 5–6 of
  [`trusting-the-spec-again`](../journeys/trusting-the-spec-again.md).
- The audit gains two lines.
- What it shortens is *The changes after* (step 8): a merge that reads
  *Merged* is then on `main`, with nobody checking.

## The job behind the request

To merge a change that depends on another one, and to trust that **Merged**
means it reached `main`, and therefore the next release.

**What they do today instead** is trust the word. On 2026-09-26, #160–#163 were
a stack, each pull request based on the one before it:
- #157 merged to `main` first;
- the other four then merged into their parents' branches, which were already
  merged, so they never reached `main`;
- every one of them reads **Merged**;
- none of the work (cases 52–70, specs 0068–0071) reached a release until #165
  carried it, a week later, as a side note in a pull request about something
  else.

## Why now

- **It happened here, and it was silent.** Every required check passed,
  because each ran against its own base. Nothing asks where a merge landed.
- **The cause is one platform setting, and it was never read back.** This
  repository keeps a pull request's branch after merging it
  (`delete_branch_on_merge: false`, read 2026-10-03). GitHub retargets a
  stacked pull request to `main` only when the branch beneath it is deleted.
  With deletion off, the stacked pull request goes on pointing at a dead
  branch.
- **0073 made parallel trees ordinary, and parallel changes are sometimes
  dependent.** A stack is the natural shape for those, and the method says
  nothing about one: *Branches and pull requests* shows one branch from
  `main` and one `gh pr create`.

## The end value

A pull request stacked on another one ends up on `main`, or the next audit
says it didn't, naming the pull request and the commit `main` lacks.

**How we would know it worked:**
- In this repository, a two-deep stack merged in order leaves both changes on
  `main`, and the second pull request's base reads `main` when it merges.
- `doctor` run on this repository, with the stamp before 2026-09-26, lists
  #160–#163 as having merged off `main`, and then finds their commits on
  `main` through #165, so it doesn't call them stranded. With a fixture
  where nothing carried them, it lists them.
- In a repository set up after this ships, the protection table carries a
  read-back of the delete-on-merge setting.

## What changes

1. **The method, [`repository.md`](../../method/repository.md) —
   *Branches and pull requests*.**
   - **A paragraph: *A pull request may be based on another's branch*.**
     - A stack is allowed, and it merges only into the main branch.
     - When its base merges, it is retargeted to the main branch before it
       merges itself.
     - The platform does that retargeting when it deletes a merged pull
       request's branch. So deletion is a protection setting, read back like
       the others, rather than a habit somebody keeps.
     - **Merged is not the same as on the main branch.** What arrived is read
       from the main branch.
   - **The protection table gains a row**, *Merged branches deleted*: a pull
     request stacked on one is retargeted to the main branch rather than
     merged into a branch nobody will merge again.
   - It names no platform and no command.

2. **[`setup`](../../skills/setup/SKILL.md).** Where it reads branch
   protection back, it also reads the delete-on-merge setting.
   - Off: it says what that does to a stack, offers to turn it on with the
     command, and waits. A protection change is outward-facing, the same as
     the hook.
   - A refusal goes into the protection section as *unobserved*, with who can
     read it.

3. **[`doctor`](../../skills/doctor/SKILL.md) and
   [`tools/doctor.py`](../../tools/doctor.py) — two checks**, both judgment,
   both pre-filled from the read-back commands the bindings' protection
   section already names:
   - `check:merged-branch-deleted`, *platform*: the setting, read back. Off
     is *open*, and a refusal is *not-read*.
   - `check:merged-off-main`, *wiring*: every pull request merged since the
     stamp's date into a base that isn't the main branch, each checked for
     whether its head commit is on the main branch. Each one missing is
     listed with its base and the commit, and the line is *open*. The audit
     changes nothing: it doesn't retarget, cherry-pick or reopen.

4. **[`gates.md`](../../method/gates.md#the-checks-an-audit-makes) — the two
   ids**, with `since` reading `next`. The pull request carries `## Ids`.

5. **This repository.**
   - `delete_branch_on_merge` is turned on at implementation, with
     `gh api -X PATCH repos/sargismarkosyan/livespec -F delete_branch_on_merge=true`.
   - The protection section of the bindings records it, with the read-back
     command and the date.
   - `trees.py clean` is unaffected: it goes by git's own record, and
     `git branch -d` still agrees that a merged branch is merged.

6. **The cases and tests.**
   - Unit tests under `tests/` hold the tool's pre-fill for both checks.
   - Two eval cases:
     - a `setup` case whose platform keeps merged branches: the offer, the
       wait, then the row (`merged-branches-are-deleted-so-stacks-retarget`);
     - a `doctor` case with the setting off and one stranded stack:
       `the-delete-on-merge-setting-is-read-back` and
       `a-merge-that-missed-main-is-listed`.
   - The platform in both cases is the fixture's own client script, which
     the bindings name, the same way 0074 stood in for the tracker. A real
     `gh` lent to a session could change a live repository's settings.

**Rules added**, all `@planned` until the implementing commit:

| Rule id | Feature file | New or changed |
|---|---|---|
| `merged-branches-are-deleted-so-stacks-retarget` | [`features/setup/a-stack-lands-on-main.feature`](../features/setup/a-stack-lands-on-main.feature) | new |
| `the-delete-on-merge-setting-is-read-back` | [`features/wiring/a-stack-lands-on-main.feature`](../features/wiring/a-stack-lands-on-main.feature) | new |
| `a-merge-that-missed-main-is-listed` | same | new |

## What we are not doing

- **Forbidding stacks.** A dependent change would then sit idle until its
  parent lands. With several trees in flight, that is the wait trees exist to
  remove.
- **A required check that fails a pull request whose base isn't `main`.** The
  protection on `main` doesn't govern a merge into another branch. That is
  exactly how #160–#163 got past it, so such a check would be red on a pull
  request nothing stops from merging.
- **Moving stranded work.** The audit lists it. Cherry-picking, reopening or
  re-basing it is a change of its own, and the person's call.
- **The merge queue (#169), claiming (#171), numbering (#167).**
- **Teaching a skill to merge.** No skill merges. The method states the rule,
  and the platform setting enforces it.

## Data

No storage contract moves. Bindings written before this ship have no
read-back of the setting. The first audit after the upgrade reports
`check:merged-branch-deleted` *unanswered* with the protection section's
commands, and `open` if the setting is off. Pull requests already stranded
are listed once, by `check:merged-off-main`, from the stamp's date forward.

## Risks

- **A deleted branch is not a deleted tree.** The platform deletes the remote
  branch. The local branch and its tree stay until `trees.py clean`, which
  already removes only what has nothing to lose.
- **Look-back cost.** Reading merged pull requests since the stamp is one
  platform call, plus one ancestry check per merge whose base wasn't `main`,
  which is usually none.
- **`always-green`.** Nothing reaches a user's build. Both checks are the
  audit's.
- **Eval spend.** Editing `setup` and `doctor` stales their tier rows, and
  the two new cases start unmeasured. They are named in the pull request,
  and nothing runs without the maintainer's yes.

## Acceptance checks

1. Read the stack paragraph in `repository.md` and confirm it names no
   platform or command.
2. In this repository, after implementation, `gh api
   repos/sargismarkosyan/livespec --jq .delete_branch_on_merge` reads
   `true`, and the bindings record it with that command and the date.
3. Make a two-deep throwaway stack and merge the parent. See the child's
   base become `main`.
4. Run the audit's pre-fill here and see both lines carry a command.
