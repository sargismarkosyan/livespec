# How a pull request description is written here

Every agent and person opening a pull request in this repository follows this
file, whether or not they load livespec. `setup` wrote it from livespec's
template, for this repository's template, platform and tracker. The audit reads
it against the plugin's guideline after every update, so a change there comes
back here as something to bring level. Linked from <the context file>'s step
that opens a pull request.

## The template

<the template the platform fills a new pull request with, by its path — or
*none*. Each heading and checkbox in its order, with what fills it here.>

The body starts from the template's file: the platform fills a new pull
request with it only in its own form, never one opened from <the command line
or API used here>. It fills it: every heading and checkbox, in its order,
nothing renamed, replaced or added beside it. <Where what it has no field for goes: above its
first heading as plain lines — the point, the links line, a line each for a
decision, a risk or an open question — and the folded evidence after its last
field. With no template: the point, the links line, the sections below, then
decisions, testing and risk when there is something to say, then the folded
evidence.>

**A checkbox is a claim**: ticked only when true now. One that waits on an open
question or an approval says what it waits on; one that does not apply reads
`N/A` with the fact that makes it so.

## The point

The problem first: who is affected, what goes wrong, and how it is known —
<where a problem is known from here: the tracker, an incident, a report, the
request>. Then one sentence on what changes. Hide that sentence, and the reader
still knows why the change exists.

## The closing line and every reference

- **The closing line:** <exactly what this platform registers, e.g.
  `Closes #<n>` on its own line>, read back after opening with <the command that
  lists what a pull request will close>.
- **Every other reference is a link with its title**, never a bare number or
  address: <how each kind is written here — an issue, a pull request, an
  incident, an item in another tracker>. An item with no address is its id with
  its title in words.

## What else a body carries here

<each section this repository's rules or pipeline require, and where it goes:
the picture the bindings' *Deliverable of a version* names, the Gherkin a moved
`.feature` owes, the run under the verification command, a link a pipeline job
checks for, and the release note in the section the release publishes — or that
none is published.>

## Length

About a hundred words of the author's own, unfolded; a risky change adds one
line per decision, open question or rollout step. The template's headings, its
checklist and the titles inside links are not counted. Words are cut, never a
name or fact a reviewer or tester needs.

## Left out

What the change does not do, an account of the tools that wrote it, and
anything every body here would repeat.

## Before it is published

1. **Ask, don't guess.** A reason, cost, rollout, rollback, address, title or
   picture the author can give is asked for. What nobody can answer yet is an
   open question naming who can.
2. **Check it against the final diff** — <the command that shows it> — cutting a
   claim the diff does not bear out and adding a behaviour change it shows.
3. **Read it back** once published — <the command that shows the body as the
   platform has it> — and count the words.
