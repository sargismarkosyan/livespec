@feature:showing-how-it-is-drawn @workflow:adopt-the-process
Feature: How a sketch shows what changes

  @rule:a-sketch-draws-one-instance-twice
  Rule: A sketch shows the change on one real thing the spec names, drawn as it is now and as it would be in two frames of the same layout, with each count as a sentence under its frame, and draws the evidence in the form it has before reaching for a tile or a bare table

    Example: a change to how something is done
      Given a change spec that replaces the three steps a request goes through with one
      When the sketch is drawn
      Then one request the spec names is shown going through both, now and after, in frames laid out alike
      And the only thing that differs between the two frames is what the change changes

    Example: a count that moved
      Given a change spec in which the files kept in step by hand go from three to one
      When the sketch is drawn
      Then the count is a sentence under each frame, in the reader's own units
      And it is not a number standing alone in a tile

    Example: which thing covers which
      Given a change spec about which checks hold which steps
      When the sketch is drawn
      Then it is a grid of checks against steps, with a legend saying what each mark means

    Example: files or steps added and removed
      Given a change spec that adds one file and retires two
      When the sketch is drawn
      Then the tree is drawn before and after, with what is added marked and what is removed struck through, one note per line

    Example: a line to start from
      Given a sketch about to be drawn
      When it is given a headline
      Then it is one sentence taken from the spec's account of what changes
      And none of the end value, the job or the reasons is restated above the evidence
