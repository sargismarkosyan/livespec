@feature:refining-a-number-nobody-else-holds @workflow:adopt-the-process
Feature: A change spec takes a number no other change in flight holds

  @rule:a-change-number-is-taken-past-everything-in-flight @crosses:consuming-repository
  Rule: A refining skill numbers its change spec one past the highest it can see on the main branch, in the open pull requests and in the branches the open claims name, and says which it read

    Example: another tree already holds the next number
      Given the main branch ends at spec 0006
      And an open pull request adds spec 0007
      And a claimed issue's comment names the branch spec-0008-dawn-chorus
      When a session writes a new change spec
      Then it is numbered 0009
      And the hand-back says the numbers it stepped past and where each was held

    Example: a number a closed pull request left behind
      Given the main branch goes from 0023 to 0025, because the pull request holding 0024 was closed
      When a session writes a new change spec
      Then it is numbered 0026, and 0024 is left as a gap rather than reused

    Example: the open pull requests cannot be read
      Given the platform does not answer when the open pull requests are asked for
      When a session is about to number a change spec
      Then it says the number may collide, naming what it could not read
      And it does not present the number as checked
