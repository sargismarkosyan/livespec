# Spec 0109: the process from its principles

- **Status:** approved — by the maintainer in advance, 2026-11-22 (*"Carry on."*), as the next of the seven moves agreed on 2026-11-19; implemented end to end, reviewed at the pull request
- **Issue:** [#195](https://github.com/sargismarkosyan/livespec/issues/195), the first of several changes under it
- **Sketch:** skipped — approval was given in advance, so there was no decision left for one to support.

## Who this is for

**Ren — [`agent-accelerated-owner`](../personas/agent-accelerated-owner.md).**
Ren is the person in the loop, and Ren's agent is the one reading the method;
every rule it reads is a rule it can misapply. Nothing about who this is for
moves.

**The workflow is [`adopt-the-process`](../workflows/adopt-the-process.feature),**
at every step of it: `process.md` is the page the method's README says to read
first.

## The job behind the request

To hold a method small enough that the agent reading it follows all of it.
[#195](https://github.com/sargismarkosyan/livespec/issues/195): the method is
written incident by incident, and a page patched one paragraph at a time keeps
the shape that made it long — [`claude-md.md`](../../method/claude-md.md#when-it-is-out-of-line)
says so about the context file, and the same holds here.

## Why now

- `method/` is 2,382 lines. `process.md`, the page read first, is 266 of them,
  and two of its rules carry a paragraph saying *the reason this needs a rule
  is…*.
- [0085](0085-less-is-the-default.md) set a ceiling on `method/`; this is the
  first change to lower it.

## The end value

The method states six principles once, and `process.md` is rewritten from them:
each rule sits under the principle it follows from, and a rule that follows from
none has nowhere to go.

**How we would know it worked:** every fact the old page held is in the new one
or named below as dropped, and the page is shorter.

## What changes

1. **[`method/README.md`](../../method/README.md)** gains *Six principles*:
   - the code is the truth;
   - one change, decided before it is built;
   - every promise is checked by something that can fail;
   - one copy of anything;
   - say what you cannot do;
   - delete what stops being true.
2. **[`method/process.md`](../../method/process.md)** is rewritten from them.
   - It is not patched. The harvest below is the check that nothing was lost.
   - The four headings other files link to keep their anchors: *The rules*, *A
     step you cannot take here…*, *A workaround names what would end it* and *A
     technical change that serves no workflow…*.
3. **The `method/` ceiling** in the bindings is lowered to the size this change
   leaves.

No rule, workflow or skill moves. No Gherkin moves.

### The harvest

| Fact the old page held | Where it is now |
|---|---|
| The code is the truth; the spec is context that keeps the reasoning readable | principle 1, and its section |
| The deliverable is a series of pictures; every commit worth looking at | *Who does what* |
| The person uses, reports and approves; the agent writes everything else; artefacts are the only channel | *Who does what* |
| The eight-step loop, with the skills | *The loop* |
| Filing and specifying are separate jobs | under *The loop* |
| The picture is the agent's, from the shot list; the person uses the version | under *The loop* |
| One change spec = one step = one version | principle 2 |
| Spec before code; `refine-spec` first | principle 2 |
| A workflow or persona edit is confirmed on its own, before the spec | principle 2 |
| A reading is played back before anything is written; a diff does not replace it | principle 2 |
| The decision gets its evidence; sketch vs picture; when no sketch; the bindings say which changes owe each | principle 2 |
| Feedback never fixed on the spot; the pipeline fix's lighter path, issue first | principle 2 |
| Every merged change read back for one path or the other | principle 3 |
| Less is the default | principle 4 |
| Whatever only grows has a ceiling | principle 4 |
| Every version runs and is green | principle 3 |
| Specs commit separately from implementations | principle 2 |
| An issue is closed when its job is answered | principle 2 |
| A version is a change spec number; version 0 is the scaffold; `git log` and the pictures are the history | principle 1 |
| What a change makes dead goes in it, named under *What this removes* | principle 6 |
| *When the process gets in the way*: behaviour someone could notice; when unsure, write the spec | its section |
| A technical change that serves no workflow, and what it still owes | its section |
| A step you cannot take is said once; handing over; not a licence to investigate less; *unreachable* boundaries | its section, under principle 5 |
| A workaround names what would end it; the four columns; a decision is not a workaround; never followed silently | its section |
| The row comes out when the workaround does | its section, and principle 6 as *a record comes out when the thing it describes does* |

## What this removes

- **"There are no semver tags and no releases."** It was true of the reference
  repository and is not true of every repository using the method — livespec
  itself releases — and it is a binding if it is anything.
- **"In Claude chat … not in the app, not as a written issue"** in step 1. It
  names one host, and the loop runs under two.
- **The two "the reason this needs a rule is…" paragraphs.** The rules stay. The
  incidents behind them are in the change specs that made them.
- **77 lines of `process.md`;** `method/README.md` grows by 17, for the
  principles.

## What we are not doing

- **The other method files.** Each is its own change under #195, so a regression
  is traceable to one page.
- **Moving gate-enforced prose into failure messages.** That is
  [#194](https://github.com/sargismarkosyan/livespec/issues/194).
- **Changing any rule.** This is a rewrite of how the rules are said, not of
  what they say.

## Data

None.

## Risks

- **A rule loses force in the shortening.** The harvest is the check, and the
  review reads the old page beside the new one. The eval cases that hold the
  skills are unchanged and still claim the same rules.

## Acceptance checks

1. Every row of the harvest can be found in the new `process.md` or the README.
2. The four linked anchors still resolve; `verify.py` is green.
3. `method/` is under its old ceiling, and the ceiling is lowered to match.
