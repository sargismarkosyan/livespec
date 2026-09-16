@feature:audit-the-record @workflow:adopt-the-process
Feature: The audit record — one line per check, or the audit does not end

  @rule:one-line-per-check-or-it-does-not-end
  Rule: An audit accounts for every check the method names, one line each in a state from the vocabulary, or it is refused and cannot hand back

    Example: one line short
      Given a record with thirty-eight of the thirty-nine lines
      When it is validated
      Then it is refused, naming the missing id
      And the audit does not hand back

    Example: a judgment nobody made
      Given a record with a line still reading unanswered
      When it is validated
      Then it is refused, naming the line

    Example: a state of somebody's own
      Given a record with a line in a state the vocabulary does not have
      When it is validated
      Then it is refused, naming the state

  @rule:a-finding-carries-what-closes-it-and-a-skip-carries-why
  Rule: A line that is open names what closes it, a line not read names why, and a judgment answered carries the command that answered it

    Example: open with nothing after it
      Given a record whose open line names nothing that would close it
      When it is validated
      Then it is refused

    Example: not read, with a reason
      Given a session that cannot reach the platform
      When the line for branch protection is written as not read, with why
      Then the record validates
      And the reply says the claim was not read back rather than that it holds

    Example: clear with no receipt
      Given a judgment line marked clear with no command beside it
      When it is validated
      Then it is refused

  @rule:the-record-is-kept-where-the-bindings-say
  Rule: The record is committed at the path the bindings name, replaced on every run, and every line carries the date it last changed state, read from the previous record

    Example: a line that did not change
      Given a previous record with a line open since a date
      When the next audit finds the same line open
      Then the line keeps that date
      And the reply names it as the oldest open, with how many audits it has survived

    Example: a line that closed
      Given a previous record with a line open
      When the next audit finds it clear
      Then the reply names it as closed
      And the next record carries the new date

  @rule:corrections-touch-only-the-record @refusal
  Rule: What an audit changes in a consuming repository is the bindings, the loop's own account of itself and the audit record, and nothing else

    Example: a fix that strayed
      Given an audit whose corrections touched a source file
      When the record is validated
      Then it is refused, naming the file
      And the reply says that wiring is the sitting's
