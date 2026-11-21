@feature:wiring-a-ceiling-on-what-grows @workflow:adopt-the-process
Feature: What the build holds a part that only grows to

  @rule:a-part-past-its-ceiling-fails @planned
  Rule: Verification fails when a part the bindings' Ceilings row names is larger than its ceiling, or when the bindings carry no Ceilings row, naming the part, its size and the ceiling

    Example: every part within its ceiling
      Given the Ceilings row names the skills at 2,700 lines
      And the skills are 2,692 lines
      When verification runs
      Then nothing is reported about it

    Example: a part grew past its ceiling
      Given the Ceilings row names the skills at 2,700 lines
      And a change adds a paragraph that takes the skills to 2,712 lines
      When verification runs
      Then it fails, naming the skills, 2,712 lines and the ceiling of 2,700
      And the fix it names is a cut, or the ceiling raised in this change with the reason beside it

    Example: no ceiling was ever written
      Given the bindings carry no Ceilings row
      When verification runs
      Then it fails, because a number nobody wrote is not a pass
