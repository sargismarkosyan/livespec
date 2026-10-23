# Spec 0081: a closing line that closes

- **Status:** approved — by the maintainer in advance, 2026-10-23: implemented end to end, reviewed at the merge request
- **Issue:** [#179](https://github.com/sargismarkosyan/livespec/issues/179)

No sketch was drawn: approval was given in advance, so there was no decision
for one to be held at.

## Who this is for

**Ren — [`agent-accelerated-owner`](../personas/agent-accelerated-owner.md) —
on a self-hosted GitLab.** The report is from `helios/pi-plugins` on
gitlab.workfront.tech, where agents open every merge request and Ren merges
them. Nothing about who this is for moves.

**The workflow is [`adopt-the-process`](../workflows/adopt-the-process.feature).**
- Its *Where it breaks* already names this failure: *a skill assuming a
  tracker this repository does not use.* The method's one check for a
  closing line is GitHub's command.
- The sitting writes one more bindings row (steps 5–6 of
  [`trusting-the-spec-again`](../journeys/trusting-the-spec-again.md)).
- What it changes is the end of every change after that: the step in the
  loop that opens the pull request.

## The job behind the request

When a change merges, the issue it answered should close, and nobody should
have to go back and check. If it is not going to close, Ren wants to know
while the pull request is still open, not after three merges.

**What they do today instead** is close every issue by hand, after the merge,
once somebody notices it is still open. In `helios/pi-plugins`,
[helios/pi-plugins!42](https://gitlab.workfront.tech/helios/pi-plugins/-/merge_requests/42),
[helios/pi-plugins!41](https://gitlab.workfront.tech/helios/pi-plugins/-/merge_requests/41)
and [helios/pi-plugins!33](https://gitlab.workfront.tech/helios/pi-plugins/-/merge_requests/33)
merged and closed nothing. The repository's own workaround, until the method
covers it, is a line in its `AGENTS.md` loop and a row in its bindings.

## Why now

- **The form the method leaves out is the one a linking convention produces.**
  The repository's instructions say to link every reference and never leave a
  bare `#31`. So the agent wrote the closing line the same way: the keyword,
  then `#31` as a Markdown link to the issue. Tested on
  [helios/pi-plugins!44](https://gitlab.workfront.tech/helios/pi-plugins/-/merge_requests/44)
  by reading GitLab's `closes_issues` back after each edit:

  | Closing line | Registered |
  |---|---|
  | keyword, then a Markdown link to `/-/issues/31` | nothing |
  | keyword, then a Markdown link to `/-/work_items/31` | nothing |
  | keyword, then the bare `/-/issues/31` URL | 31 |
  | keyword, then the bare `/-/work_items/31` URL | 31 |
  | keyword, then a bare `#31` | 31 |

  On GitHub the Markdown-link form is untested.
- **And the opposite failure.** On GitLab, a keyword in front of a real
  reference registers even inside a code span. The draft of !44 quoted test
  lines that way, and the merge request then listed an issue it does not fix.
- **The method's only check is GitHub's command**, written into
  `method/repository.md`. That is a binding in the method, and on GitLab it
  does not run at all.
- **Nothing runs it.** It is prose in a page the loop does not open. The
  step that opens a pull request is the loop in the repository's context
  file, and no requirement on that loop mentions what the pull request will
  close.

## The end value

An issue named by a pull request closes when the pull request merges, on
whichever platform the repository is on. A closing line that the platform
did not register is caught while the pull request is still open.

**How we would know it worked:**
- In a GitLab repository adopting or re-auditing the process, the bindings
  name the GitLab read-back, and the loop's pull-request step runs it.
- The next merge request whose closing line is a Markdown link is fixed
  before the merge, because the read-back came back empty.
- Here, the bindings carry GitHub's read-back, watched listing an issue.

## What changes

1. **The method, [`repository.md`](../../method/repository.md) — *Closing an
   issue*.**
   - The keyword sits straight before a **bare** reference: `#12`, or the
     issue's full URL, which links as well as closes.
   - Two lines that read like a closing line and close nothing are named:
     words between the keyword and the reference (already there), and the
     reference wrapped in a Markdown link (new).
   - The opposite: a keyword in front of a real reference can register inside
     a code span, so a description that discusses closing lines does not put
     the keyword in front of a real reference.
   - **The step that opens the pull request reads back what it will close**,
     before handing it back. An empty list, or a list naming an issue the
     change does not finish, is fixed in the description and read again.
   - The command moves out. The method names none; it is a binding, read from
     the platform the repository is on — the same treatment the protection
     table's read-back gets.
2. **The method, [`process.md`](../../method/process.md) — step 6 of the
   loop.** Opening the pull request includes reading back what it will close.
3. **The method, [`claude-md.md`](../../method/claude-md.md) — requirement
   6.** The loop's step that opens the pull request says it reads back what
   the pull request will close, with the bindings' command. `doctor` already
   reads the loop against this page (`check:loop-per-claude-md`), so a
   repository set up earlier is told at its next audit. No new check id.
4. **The bindings template, [`bindings.md`](../../templates/bindings.md) —
   one row, *What a pull request will close*.** The platform's own read-back
   command and the date it was watched listing an issue. Or *not applicable,
   decided*, where a merge here closes nothing: no tracker, or issues on a
   different host from the pull requests.
5. **[`setup`](../../skills/setup/SKILL.md), section 5.** Writes that row
   beside the tracker row:
   - read from the platform the repository is on. The skill names the GitHub
     and GitLab commands as the two known answers; any other forge's own
     client is asked;
   - run against a pull request that named an issue before the row is
     written, so the row carries a date, or *unobserved* with why;
   - never another platform's command because it is the familiar one.
6. **This repository.**
   - The bindings gain the row: `gh pr view <n> --json closingIssuesReferences`,
     watched on 2026-10-23 listing #164 on
     [#178](https://github.com/sargismarkosyan/livespec/pull/178).
   - `CLAUDE.md`'s loop, step 6, gains the read-back, inside the ceiling.
7. **Two eval cases**, on a fixture forge that is not GitHub, reached with
   its own client:
   - **87**, `setup`: three merged merge requests closed nothing. The sitting
     binds the row with the forge's own read-back, run against a merge
     request first (`the-closing-read-back-is-bound`).
   - **88**, `setup`: an `AGENTS.md` whose loop opens the merge request with
     a Markdown-link closing line and never reads it back. The sitting
     reports the step stale and rewrites it
     (`the-loop-reads-back-what-a-pull-request-closes`).

**Rules added**, live since the implementing commit:

| Rule id | Feature file | New or changed |
|---|---|---|
| `the-closing-read-back-is-bound` | [`features/setup/what-a-pull-request-closes.feature`](../features/setup/what-a-pull-request-closes.feature) | new |
| `the-loop-reads-back-what-a-pull-request-closes` | [`features/setup/what-a-pull-request-closes.feature`](../features/setup/what-a-pull-request-closes.feature) | new |

## What we are not doing

- **A `doctor` check that reads merged pull requests against the issues they
  named.** The issue's third point lists it. The read-back at the step that
  opens the pull request catches the same failure before the merge, and
  `check:loop-per-claude-md` already reaches a loop that lacks it. A check
  reading history is a new id, and can come later if repositories still miss
  it.
- **A gate on the pull request body.** Whether a line registers is the
  platform's answer, and only the platform's read-back gives it. A regex for
  `Closes [` would be a second, weaker copy of that answer.
- **Testing the Markdown-link form on GitHub.** Nothing here needs the
  answer: the read-back is the check on every platform. The method says it
  is untested there.
- **Setup's own pull request at the end of section 8.** It lands the spec
  layer the sitting wrote and rarely names an issue. It follows the loop like
  any other pull request.
- **This repository's move to GitLab.** Its pull requests now open on
  GitLab and its issues stay on GitHub, so no merge here closes an issue,
  and once that is recorded the new row here reads *not applicable,
  decided*. The rest of the bindings still describe GitHub, so the row is
  written to match them, and recording the move is a change of its own.

## Data

No storage contract moves. Bindings written before this ship have no row.
The next audit reaches it through `check:loop-per-claude-md` and the
changelog entry.

## Risks

- **A read-back too early.** A platform may take a few seconds to register a
  description edit; the test on !44 read back after about 6 s. Reading
  straight after the edit can show a stale list. The method says to read it
  again after a fix, which covers this.
- **Eval spend.** Editing `setup` stales its tier rows, and the two new cases
  start unmeasured. Named in the pull request; nothing runs without the
  maintainer's yes.

## Acceptance checks

1. Read *Closing an issue* in `repository.md`. Confirm it names no command,
   and names both forms that close nothing.
2. Read requirement 6 in `claude-md.md` and step 6 of this repository's
   `CLAUDE.md`. Both carry the read-back.
3. Run the row's command here against a pull request that named an issue,
   and see the issue listed.
