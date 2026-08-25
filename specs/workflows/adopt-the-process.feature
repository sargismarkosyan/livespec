@workflow:adopt-the-process @persona:agent-accelerated-owner @journey:trusting-the-spec-again @planned
Feature: Adopt the process

  When a repository has grown to where regressions arrive out of changes whose
  reasons nobody remembers, and every fresh session starts by being told
  everything again,
  I want the repository to carry that context itself and to say so out loud when
  it stops being true,
  so the next change costs what the change costs, rather than an explanation
  first.

  **Ends when** the next change opened in that repository proves it: the pull
  request carries what the version leaves behind, and the pipeline refuses the
  change until the specs move with it.

  **Done well.** One sitting, and the layers are filled in it rather than
  scheduled — a persona, the attempts, the arc. The gates are wired in the
  language already in the repository and add no dependency to run. Nothing that
  already shipped is specced retroactively: the layer starts at the next change,
  not at the history.

  **The process goes on top of what is there, never in place of it.** Where the
  plugin does not fit the repository — the tracker is somewhere else, a local
  skill already does the job better — the repository wins, and the mismatch is
  filed against livespec rather than absorbed quietly. A repository that had to
  be rearranged to accept the process has been handed a second thing to maintain,
  which is the problem it adopted the process to stop having.

  **Where it breaks.** A skill assuming a tracker this repository does not use.
  A skill acting on "this repository" without resolving which one, so what is
  filed lands in the wrong tracker. Bindings asserting a behaviour nobody has
  run. A sitting that names the next step instead of taking it, and leaves the
  layers empty behind a promise. A pull request with nothing in it to look at.

  Example: the gates arrive in the language already in the repository
    Given a consuming repository with its own verification command
    When the process is set up in it
    Then its bindings name that command rather than a new one
    And nothing has been installed that the gates need in order to run

  Example: the repository's own tooling wins where the plugin does not fit
    Given a consuming repository whose tracker is not the one a skill assumes
    When that skill does not fit the repository
    Then what the repository already had is kept
    And the mismatch is filed against livespec rather than worked around in silence

  Example: a layer that was named is not a layer that was filled
    Given the process has been set up and the persona layer is empty
    When the sitting ends
    Then the hand-back says which layers are still empty
    And naming the next command does not count as having run it

  Example: a later session starts from what is written
    Given the process has been set up in a repository
    And I come back to it after weeks away
    When a change is started
    Then what the repository is for is readable from its specs
    And nothing has to be explained again before the change can begin
