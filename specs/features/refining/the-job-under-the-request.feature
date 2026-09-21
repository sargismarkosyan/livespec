@feature:refining-the-job-under-the-request @workflow:adopt-the-process
Feature: A request is refined to the job under it, not built as asked

  @rule:the-job-is-found-under-the-request
  Rule: A request shaped like a solution is refined to the job the person was doing, and the spec argues from the job

    Example: a button is asked for
      Given a request naming the thing to add — a button, a flag, a field
      When it is refined
      Then the job the person was trying to do is named apart from the thing asked for
      And the spec argues from the job rather than from where to put the button

    Example: the job cannot be told from the request
      Given a request whose job is not readable from what it asks for
      When it is refined
      Then the person is asked what they were trying to do
      And nothing is written until they have answered
