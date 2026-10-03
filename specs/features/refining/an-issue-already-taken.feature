@feature:refining-an-issue-already-taken @workflow:adopt-the-process
Feature: An issue one session has taken is not taken again by another

  @rule:an-issue-is-claimed-before-anything-is-written @crosses:consuming-repository
  Rule: Before a refining skill writes anything about an issue, it reads whether the issue is already claimed, and if it is not, claims it in the tracker with the marker the bindings name and one comment saying where the work is

    Example: the issue is free
      Given issue 12 carries no claim marker, no open pull request closes it, and no tree holds a branch for it
      When a session is asked to pick up issue 12
      Then the claim marker goes on issue 12 before any spec file is written
      And one comment on it names the branch, the tree, the harness, the session id and the date

    Example: the harness gives no session id this session can read
      Given a session whose harness exposes no id for it
      When it claims an issue
      Then the comment says the session id is not exposed, rather than leaving the line out or making one up

    Example: the tracker refuses the marker
      Given the bindings name a claim label the tracker does not have
      When the session claims the issue
      Then the comment is still written, and the hand-back says the marker was refused and why
      And no label is created by the refining skill

  @rule:a-claimed-issue-is-not-taken-twice @crosses:consuming-repository
  Rule: An issue already claimed is reported with where its work is and how old the claim is, and nothing is written about it until the person says to take it over; nothing releases a claim by age

    Example: another tree is already on it
      Given issue 12 carries the claim marker, and its comment names a branch in another tree on this machine
      When a second session is asked to pick up issue 12
      Then it says issue 12 is in flight, naming the branch, the tree, the harness and the session id the comment gives
      And it writes nothing until the person answers

    Example: the claim looks abandoned
      Given issue 12 was claimed nine days ago, and the branch it names exists nowhere and no pull request closes it
      When a session is asked to pick up issue 12
      Then it reports the claim, its age and that nothing stands behind it, and asks
      And the claim is not removed or replaced while the question is unanswered

    Example: the person says to take it over
      Given the person has said to take over a claimed issue
      When the session claims it
      Then its comment names the claim it replaced, by its session id and date

    Example: asked for the next issue rather than a named one
      Given three open issues, the oldest of them claimed
      When a session is asked to pick up the next issue
      Then it chooses among the two that carry no claim, and says which it skipped and why

    Example: the tracker cannot be read
      Given the tracker does not answer when the claim is read
      When a session is asked to pick up an issue
      Then it says the claim could not be read and asks before writing anything
      And it does not treat an unread claim as no claim

  @rule:a-dropped-claim-is-released-by-whoever-dropped-it
  Rule: A session that stops work on a claimed issue without a pull request takes the marker off and says so in a comment; a pull request that closes the issue is the claim's end, and nothing else releases it

    Example: the spec is turned down
      Given a session claimed issue 12 and its spec was turned down
      When the session stops
      Then the marker is off issue 12, and a comment says the work stopped and why

    Example: the pull request merges
      Given a pull request that closes issue 12 has merged
      When the issue is closed by it
      Then nothing else is owed to release the claim
