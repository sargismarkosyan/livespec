@feature:refining-a-name-from-the-day @workflow:adopt-the-process
Feature: A change spec is named by the day it is written and its slug

  @rule:a-change-spec-is-named-by-its-day-and-slug @planned
  Rule: A refining skill names a new change spec by the date it is written and its slug, reads nothing in flight to choose it, and leaves the numbered specs before it as they are

    Example: two trees start the same morning
      Given two trees are cut from the same main branch on 2026-11-23
      And one session refines "a quieter log" and the other "one place to report"
      When each writes its change spec
      Then one is specs/changes/2026-11-23-a-quieter-log.md and the other specs/changes/2026-11-23-one-place-to-report.md
      And neither session asked the platform what the other holds

    Example: a repository that numbered its specs before
      Given the main branch ends at spec 0006 and an open pull request adds spec 0007
      When a session writes a new change spec on 2026-11-23
      Then it is named 2026-11-23-<slug>.md, not 0007 or 0008
      And 0001 to 0006 keep their names and every link to them

    Example: the same slug on the same day
      Given two trees each wrote specs/changes/2026-11-23-a-quieter-log.md
      When the second pull request is brought up to date with the main branch
      Then git reports the two files in conflict
      And the one not yet merged takes another slug, its file, its heading and every link to it
