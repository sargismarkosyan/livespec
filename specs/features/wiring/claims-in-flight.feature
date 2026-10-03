@feature:wiring-claims-in-flight @workflow:adopt-the-process
Feature: What an audit reads back about issues marked as taken

  @rule:the-claim-row-is-there
  Rule: The audit tool reports as open bindings with no row naming the claim marker, and hands the marker to the reading

    Example: bindings written before the row existed
      Given bindings with no row for claiming an issue
      When the audit tool reads them
      Then the claim row line reads open, with the setup sitting as what closes it

    Example: the row is there
      Given bindings whose claim row names a label
      When the audit tool reads them
      Then the claim row line reads clear
      And the claims line after it is printed unanswered, carrying that label

  @rule:a-claim-with-nothing-behind-it-is-listed @crosses:consuming-repository
  Rule: The audit reads every open issue carrying the claim marker and lists each one whose branch, tree and pull request are all gone, with its age and session, and releases none of them

    Example: two claims, one stranded
      Given two open issues carry the claim marker
      And one names a branch a tree still holds, and the other names a branch that exists nowhere
      When the audit reads the claims
      Then the line reads open, listing the second issue with its claim's age and session id
      And both issues keep the marker

    Example: the marker does not exist in the tracker
      Given bindings naming a label the tracker does not have
      When the audit reads the claims
      Then the line reads open, saying the label is missing, rather than clear because no issue carries it

    Example: the tracker cannot be read from here
      Given the tracker does not answer this session
      When the audit reads the claims
      Then the line reads not-read, with why
