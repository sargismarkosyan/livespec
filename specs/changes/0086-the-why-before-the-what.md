# Spec 0086: the why before the what

- **Status:** approved — by the maintainer, 2026-11-21, after reading the spec and the sketch
- **Issue:** none — direct request, from a session that researched pull
  request descriptions with the maintainer and settled each rule with him
- **Number:** one past the highest in flight. `0085` is held by the tree
  `spec-0085-less-is-the-default`; no open pull request holds a later one.
- **Sketch:** one page, kept outside the repository and handed over with the
  spec.

## Who this is for

**Ren — [`agent-accelerated-owner`](../personas/agent-accelerated-owner.md) —
at the merge**, and whoever Ren asks to review. It is the same situation
[`0082`](0082-the-point-before-the-proof.md) served: the pull request is the
one piece of an agent's prose a person is still expected to read, because
*"checking the result by reading is not available"* for the code itself. Two
readers are new since `0082` and the method does not mention them yet. One is
the reviewer who did not ask for the change, at the consuming repository's own
company. The other is the AI reviewer or QA agent that reads the body as the
author's intent.

**The workflow is [`adopt-the-process`](../workflows/adopt-the-process.feature),
at its end**: *the pull request carries what the version leaves behind*. `0082`
said in what order the body is read. This says what the body says, in which
shape, and at what length.

## The job behind the request

The literal ask: make livespec's guidance on pull request bodies match what
the session found good descriptions do (a guideline it wrote and kept
outside the repository), with these points settled by the maintainer:

- the repository's template wins;
- the opening states the problem before the change;
- about a hundred words;
- a release note only where one is published;
- no section about what is out of scope;
- what is unknown is asked, not guessed;
- the body is checked against the diff;
- every reference carries its title;
- no line about AI use.

The job: **somebody who did not ask for the change can tell, from the first
lines alone, why it exists, and can approve or refuse it without asking the
author anything the author already knew.** Today a body written to the method
does three things wrong:

- it says what changed and hides why;
- it is two to three times the length a reviewer reads;
- where the team has its own template, it is written in a shape that template
  does not have.

## Why now

The evidence comes from three places. They agree on what goes wrong.

- **The method's own pull requests.** [#186](https://github.com/sargismarkosyan/livespec/pull/186)
  opened with 594 words before its first heading, about a change a reviewer
  could take in from three sentences. Every rewrite the session made of it, and
  of six other cases, started from the change and left the reason in a clause:
  *"Board cards can now be moved without a mouse, as the users in #311 asked."*
  Hide what changes, and nothing says what was wrong. The maintainer reviewed
  the rewrites and said the why was not clear in any of them.
- **Reviewers at an adopting company.** Their most common complaint about
  agent-written merge requests is that the agent ignores the repository's
  template and writes its own. Reviewers asked for the template back on several
  merge requests, and teams added instructions to their agents' context files
  to stop it. The second complaint is length: reviewers asked for a short
  summary, called the descriptions too long to follow, and one team capped its
  description at 150 words. An AI reviewer there reads the description as the
  author's intent, and a QA agent builds its test plan from it, so exact flag
  names and error codes matter.
- **Public practice.**
  - Google, the Linux kernel, Monzo and Chromium's own agent skill all put the
    problem first.
  - Corridor measured its descriptions: about 100 words is enough for most
    changes, and checking the text against the diff raised "good explanation"
    from 62% to 89% while cutting median length by 28%.
  - Kubernetes keeps a separate release note because it publishes one; Google,
    React, GitLab's own template and the kernel have none.
  - Chromium's skill stops and asks the author rather than guess the why.

A council of three models scored the guideline and seven example bodies against
these rules for six rounds. Three examples reached ten from all three
reviewers. What held the rest back was what only an author can supply: a
picture, an address, a cost. That is the rule on asking working as intended.

## The end value

A reviewer reads the opening, knows what was wrong, for whom and how anyone
knows, and sees what the change does about it. The body is about a hundred
words in their team's own template. Every number in it opens to its title,
and nothing in it was guessed.

**How we would know it worked:**

- the next pull request here opens with the problem and stays near a hundred
  words before its folded blocks;
- a body written in a consuming repository with a template keeps every heading
  of it;
- a reviewer stops asking what an issue number is, what the rollback is, or
  why the change exists.

## What changes

[`method/repository.md`](../../method/repository.md), *And the point, before
the evidence*, is rewritten around the guideline. It keeps the subsection's
place and its argument, that the body is written for the person deciding, and
it says:

- **The template wins.** Fill it: every heading and checkbox, in order, nothing
  added beside it. With no template, the order is the point (no heading), the
  links line, the sections the repository's rules require, then decisions,
  testing and risk, each only when it has something to say. A checkbox is a
  claim, ticked only when it is true now.
- **The opening states the problem first**: who is affected, what goes wrong,
  how it is known. Then one sentence on what changes. The test: hide that last
  sentence, and the reason for the change should still be clear.
- **What goes in**, one line each:
  - every reference is a link carrying its title;
  - a release note only where one is published;
  - before and after when an existing screen changed;
  - decisions as the choice, the alternative rejected and the cost;
  - testing as what was checked, the tests added, the names a tester needs,
    and the gaps;
  - risk and rollout;
  - the evidence folded, word for word.
- **Before publishing**: ask for what the author knows, check the text against
  the diff, and cut to about a hundred words of the author's own.
- **Rules**: each fact once; nothing about what the change does not do; no
  standing noise; plain words; the author owns it, and there is no line about
  AI use.

[`skills/record-clip/SKILL.md`](../../skills/record-clip/SKILL.md) keeps its one
bullet, reworded to point at the subsection; no skill's `description` changes.

**Rules added or changed:**

| Rule id | Feature file | New or changed |
|---|---|---|
| `the-point-comes-before-the-evidence` | `features/showing/the-point-before-the-evidence.feature` | changed: the opening states the problem before the change |
| `each-fact-once-in-words-the-reviewer-has` | `features/showing/the-point-before-the-evidence.feature` | changed: nothing about what the change does not do |
| `the-repository-template-is-filled-not-replaced` | `features/showing/what-a-body-says.feature` | new |
| `a-reference-carries-its-title` | `features/showing/what-a-body-says.feature` | new |
| `a-release-note-only-where-one-is-published` | `features/showing/what-a-body-says.feature` | new |
| `what-the-author-knows-is-asked-not-guessed` | `features/showing/what-a-body-says.feature` | new |
| `the-body-is-checked-against-the-diff` | `features/showing/what-a-body-says.feature` | new |
| `about-a-hundred-words-of-the-authors-own` | `features/showing/what-a-body-says.feature` | new |

Each new rule is claimed by an eval case when it is built, so the measurement
board owes route and first rows for those cases. Their cost is printed by
`tiers.py --changed` at that point, and only the maintainer approves the run.

## What we are not doing

- **No gate on length.** A hundred words is the reader's number, not a
  repository's. It is written in the method and checked at review. The
  report's count of words before the evidence stays as it is: printed, and
  failing nothing. A gate on length is met by cutting words, not by putting
  the problem first; `0082` says why.
- **The report is not taught templates.** In a repository whose template opens
  with `## Summary`, the report's count reads zero. That is the report not
  knowing the template, not the body failing, and the report never fails a
  build. Teaching it a template is a change of its own.
- **No AI-usage line.** Kubernetes, Rust and Ghostty ask for one. The maintainer
  decided this method does not.
- **No release note everywhere.** It came from one source, Kubernetes, which
  publishes notes to its users. Elsewhere it repeated the opening.
- **No labelled `Problem:` / `Change:` fields.** No source uses them, and they
  make a body read like a form. A template with its own *Why* field gets the
  problem there.
- **No new skill and no `description` change.** The guidance is read when a
  pull request is opened, not on every session.
- **The seven example bodies do not ship.** They were the session's test
  material, and they stay outside the repository.

## Data

None. No stored shape changes.

## Risks

- **The method grows.** The subsection goes from about 400 words to about 1,100.
  It is read when a pull request is opened, not in every session, so it adds
  no always-on cost. The rewrite is held to the guideline's own length, not
  padded around it.
- **Two rules can pull against each other.** "About a hundred words" and
  "every name a tester needs" meet on risky changes. The rule settles it: words
  are cut, never a name or fact a reviewer or tester needs, and a risky change
  adds a line for each decision, open question or rollout step.
- **Asking blocks publishing.** A body that waits on the author for a picture or
  an address is not done until the author answers. That is intended, and it
  makes the next step the author's.

## Acceptance checks

1. Read the rewritten subsection beside the guideline the session wrote.
   Every rule in the guideline is in the subsection, and the subsection adds
   no rule the guideline lacks.
2. Open the next pull request in this repository by the rewritten subsection:
   the problem first, near a hundred words before the folded blocks, every
   issue number a link with its title.
3. In a consuming repository with a template, have an agent open a merge
   request and check that every heading of the template is there, in order.
