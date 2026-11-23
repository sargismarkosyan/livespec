@feature:wiring-the-description-gate @workflow:adopt-the-process
Feature: A pull request's description is held to the template and to linked references

  @rule:a-description-out-of-its-template-fails
  Rule: With a template, a description missing one of its headings or checkboxes, renaming one, putting one out of order, or adding a heading the repository's rules do not allow fails, saying what that means

    Example: three headings added beside a checklist
      Given a template holding one heading and one checkbox
      And a description that adds "What changes", "Open questions" and "Testing" beside them
      When the description is checked
      Then it fails, naming each added heading

    Example: a checkbox with its note after it
      Given the checkbox "This change is safe to deploy to production"
      And a description ticking it with "— nothing that ships changes" after its text
      When the description is checked
      Then the checkbox is read as there

    Example: a section the repository's rules add
      Given rules that require a "## Changelog" section
      When a description carrying it is checked against a template without it
      Then the section is allowed

  @rule:a-bare-reference-fails
  Rule: An issue, pull request or incident named by a bare number or a bare address fails; a closing line, code, folded blocks and comments are not read for references

    Example: a tracker item named by its address
      Given a description reading "Hub: https://experience.example/issue/6b00cf69"
      When the description is checked
      Then it fails, naming the address

    Example: the line the platform closes an issue from
      Given a description whose own line reads "Closes #12"
      When the description is checked
      Then that line passes, and "#12" anywhere else in the prose fails

  @rule:the-length-is-reported-never-failed
  Rule: The author's own words, unfolded, are counted and reported beside the aim of about a hundred; the count never fails a description

    Example: a long description
      Given a description of three hundred words of the author's own, in its template
      When the description is checked
      Then it passes, and the report reads three hundred against about a hundred
