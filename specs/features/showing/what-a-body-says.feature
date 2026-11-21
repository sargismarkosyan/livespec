@feature:showing-what-a-body-says @workflow:adopt-the-process
Feature: What a pull request body says, in the repository's own shape and no longer than it needs

  @rule:the-repository-template-is-filled-not-replaced
  Rule: Where the repository has a pull request template, the body fills it — every heading and checkbox, in its order, none renamed and none added beside it — and a checkbox is ticked only when its claim is true now

    Example: an agent that writes its own shape
      Given a repository whose template asks for a summary, decisions, how to test, risk and a checklist
      When an agent writes the body
      Then those headings are there, in that order, and nothing else is added beside them

    Example: a box that depends on an open question
      Given a checkbox "Safe to deploy directly to production" and an open question about the deploy window
      When the body is written
      Then the box is left unticked and says which question it waits on

    Example: a box that does not apply
      Given a checkbox about database approval and a change with no migration
      When the body is written
      Then it reads "N/A: no migration", and N/A is never written without a fact behind it

  @rule:a-reference-carries-its-title
  Rule: An issue, pull request, incident or spec named in a body is a link carrying its title in plain words, never a bare number; a later mention of the same item may be the short link, and an item with no address is its id with its title in words

    Example: an issue the reviewer has not seen
      Given a body that closes issue 311, "Can't move cards on the board without a mouse"
      When the body is written
      Then it reads "Closes [#311 Can't move cards on the board without a mouse](…)", never "Closes #311"

    Example: an incident with no address
      Given an incident INC-2291 whose record gives no address
      When the body names it
      Then it reads "INC-2291 (SEV-2: duplicate invoices on webhook retries)", and no address is made up

  @rule:a-release-note-only-where-one-is-published
  Rule: A body carries a release note only where the repository publishes one from it; there it is written for users — what is different for them, no reasons and nothing internal, or NONE — and it reads true on its own in the changelog

    Example: a repository that publishes no changelog from its pull requests
      Given a repository whose template and rules name no changelog section
      When the body is written
      Then it has no release note

    Example: a change users cannot see
      Given a repository whose release copies a changelog section from the body
      And a change that moves internal code only
      When the body is written
      Then that section reads NONE

  @rule:what-the-author-knows-is-asked-not-guessed
  Rule: A reason, cost, rollout, rollback, address, title or picture the reviewer needs and the writer does not have is asked of the author before the body is published; it is never invented and never left as a placeholder, and what nobody can answer yet is an open question naming who can

    Example: a rollback nobody recorded
      Given a change whose rollback the writer was never told
      When the body is written
      Then the author is asked, and the body does not say "Rollback: revert" on a guess

    Example: a question nobody can answer yet
      Given a deploy window the database team has not confirmed
      When the body is written
      Then it carries "Open: does the index build fit the 20 min deploy window? @dba.oncall"

  @rule:the-body-is-checked-against-the-diff
  Rule: Before a body is published, what it says the change does is checked against the final diff — a claim the diff does not bear out is cut, and a behaviour change the diff shows and the text misses is added — and the tests added are told apart from the tests run

    Example: a claim the diff does not make
      Given a body that says the change also logs each failed save
      And a final diff with no such logging
      When the body is checked
      Then the sentence is cut

    Example: a behaviour change the text missed
      Given a refactor whose diff also changes how billing emails round half cents
      When the body is checked
      Then the rounding change is in the point, not only in the diff

  @rule:about-a-hundred-words-of-the-authors-own
  Rule: The unfolded body holds about a hundred words of the author's own; a risky change adds one line for each decision, open question or rollout step it carries, and the template's headings, its checklist and the titles inside links are not counted; words are cut, never a name or fact a reviewer or tester needs

    Example: a routine change written long
      Given a two-file change whose body runs to three hundred words before its folded blocks
      When the body is checked
      Then it is cut toward a hundred, and the folded evidence is untouched

    Example: a risky change
      Given a migration with four decisions, one open question and two rollout steps
      When the body is written
      Then it carries about a hundred words plus one line for each of those seven
