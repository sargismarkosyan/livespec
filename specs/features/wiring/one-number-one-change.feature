@feature:wiring-one-number-one-change @workflow:adopt-the-process
Feature: Two change specs never share a number

  @planned @rule:two-change-specs-never-share-a-number
  Rule: Verification fails when two change specs carry the same number, naming both files, whatever their slugs

    Example: two trees took the same number
      Given specs/changes holds 0033-one-place-to-report.md and 0033-a-quieter-log.md
      When verification runs
      Then it fails, naming both files
      And the fix it names is renumbering the one that has not merged yet

    Example: a gap is not a fault
      Given specs/changes goes from 0023 to 0025
      When verification runs
      Then it passes, and says nothing about 0024
