@persona:agent-accelerated-owner @retired

# Ren — keeping several repositories moving faster than they can be read

## The problem

There is more to do than there are hours, across more than one repository at
once, so the work goes through an agent instead of through typing. The
acceleration keeps stalling in the same place: the agent does not work out what
the repository already implies — which repo the session is standing in, what
that repo's tracker is, what tooling is already sitting there — so the session
goes on being handed context that was there to be read. That happens several
times a day, in every repository, and it is the difference between a fast loop
and a fast day.

Checking the result by reading is not available either. The prose in these
repositories — READMEs, docs, comments — is written for the agent and never
opened. What does get read is the spec layer: the workflows, the journeys, the
personas. So when one of those quietly stops being true, nothing stands between
that and finding out months later, with contributors arriving.

What they want is dull: to stop supplying what the repository already says, and
to find the handful of files they do read still true when they come back.

## What they do

- **A miss becomes a filed issue, not a fix.** When the agent fails to work
  something out, it gets written up and tracked rather than patched in the
  moment. Four in a row: a skill that never resolved which repository it was
  standing in; a tracker assumed to be GitHub in a repository whose tracker is a
  corporate GitLab; a framework rebuilt where one already shipped; a claim
  written into a bindings file that nobody had ever run.
- **When the tool does not fit the repository, the hand-built local version
  stays.** In the repository whose tracker is GitLab, their own `feedback` skill
  was kept rather than replaced with the plugin's.
- **A failing pipeline gets fixed. It does not get bypassed.**
- **They read the spec layer and not the documentation.** Workflows, journeys and
  personas above all. READMEs, docs and comments are for the agent.
- **Investing in the pipeline is what they do when they are short of time**, not
  what they do when they have spare time.
- **A setup they did not agree to gets stopped and questioned** rather than
  inherited.
- Working alone today. Contributors are expected and have not arrived.

Four things stated outright, because each one silently decides designs:

- **How often** — multiple times a day, across more than one repository.
- **On what** — at a terminal, in an agent session, inside the repository itself.
- **By choice or by obligation** — by choice. Nobody requires any of it; it is
  done because there is too much else to do.
- **How skilled** — high, at the domain and at software both. They write their
  own skills, migrate their own branch protection, and read what a gate prints.
  Nothing here needs explaining to them. What needs *repeating* to the agent is
  the complaint.

## What they will never do

- Bypass a failing gate to get a change through.
- Adopt a tool that does not fit the repository just because it is the official
  one.

## In their words

> I have not read it. It only for AI.

— on the documentation in their own repositories.

> I mostly read spec files, most important is workflow and journeys and persona.

> Fix the pipeline error, not bypass.

## What this file does not know

- Whether anybody else behaves this way. Nothing here has been observed twice,
  or in a repository belonging to somebody else.
- Whether what a gate prints gets read the way a spec file does, or whether only
  the exit code lands.
- What happens when the contributors actually arrive. Every line above about the
  team is anticipation; none of it is observed behaviour.
- Whether "the agent did not work it out" has a floor — which of the four misses
  they would still expect derived, once told what deriving it costs.
- Whether the loop survives a deadline. The frequency is known; whether it is
  the first thing dropped when something is due is not.
