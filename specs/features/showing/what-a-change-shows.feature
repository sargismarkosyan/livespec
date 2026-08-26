@feature:showing-what-a-change-shows @workflow:adopt-the-process
Feature: What a version puts in front of somebody deciding whether to merge

  @rule:the-form-follows-what-changed @planned
  Rule: What a version shows is moving when the change is something happening and still when its result is static, and the form is never picked by what is easier to produce

    Example: the change is only legible while it happens
      Given a version whose change is a thing unfolding on screen
      When the version is recorded
      Then what it shows is moving
      And a single frame is not offered in its place

    Example: the whole result of the change is one screen
      Given a version whose change is finished the moment it is on screen
      When the version is recorded
      Then a still of that screen is enough
      And nothing is padded into an animation to satisfy a format

    Example: the change is visible and awkward to get on screen
      Given a version whose change is visible and hard to record
      When the version is recorded
      Then it is shown anyway
      And the difficulty is not read as the exemption

    Example: the change moved nothing anybody sees
      Given a version that changed tooling and no screen
      When the pull request is opened
      Then it says in a line that there is nothing to see
      And nothing is produced to fill the space

  @rule:what-is-shown-answers-the-request @planned
  Rule: What a version shows is picked so that somebody holding only the request and that one artefact can say whether it was delivered

    Example: the person deciding has not read the diff
      Given a version opened as a pull request
      And somebody deciding on it who has read the request and nothing else
      When they look at what the version shows
      Then they can say whether what they asked for arrived
      And they do not have to check the branch out to find out

    Example: the shot list would show how it was built
      Given a change spec whose steps describe how the change was made
      When the version is recorded
      Then what was asked for is what is on screen
      And the parts that only explain the implementation are left out

    Example: what was asked for only reads against what was there before
      Given a request about something behaving differently than it used to
      When the version is recorded
      Then the state it is different from is in shot
      And the difference is what the artefact is of

  @rule:the-bindings-say-what-a-change-here-must-show @planned
  Rule: A consuming repository comes out of the sitting with bindings naming which changes owe something to look at, in what form, and where it goes

    Example: the sitting ends
      Given a consuming repository having the process set up
      When the sitting ends
      Then the bindings say which changes owe something to look at
      And they say what form it takes and where it is kept

    Example: there is no screen in this repository
      Given a consuming repository nobody looks at through a screen
      When the sitting ends
      Then the bindings say so plainly
      And they record the line as the standing case rather than the exception
