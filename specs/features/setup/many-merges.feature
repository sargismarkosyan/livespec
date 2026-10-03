@feature:setup-many-merges @workflow:adopt-the-process
Feature: The sitting says how several pull requests merge without anybody rebasing by hand

  @planned @rule:several-merges-go-through-a-queue-or-its-fallback @crosses:consuming-repository
  Rule: The sitting reads back whether the platform offers a merge queue; where it does, it offers to turn it on with the event its checks must run on, and waits; where it does not, the row says so with the fallback that keeps every merge up to date without a rebase by hand

    Example: the platform offers a queue nobody turned on
      Given a repository whose platform offers a merge queue, with none required on the main branch
      When the sitting reads the protection back
      Then it offers to require the queue and to run the required checks on the queue's own event, naming both
      And nothing changes on the platform or in the pipeline while the offer is unanswered

    Example: the queue is on, and one merge is watched through it
      Given the offer was accepted
      When a pull request is added to the queue
      Then the row is written only once that pull request has merged through it, with the date

    Example: the platform offers no queue
      Given a platform that refuses a merge queue for this repository
      When the sitting reads the protection back
      Then the row reads not available, decided, with the refusal
      And it names the fallback: the platform updates each branch from main, and each pull request merges in order once green

    Example: the checks never run in the queue
      Given a queue required on the main branch
      And a pipeline that runs the required checks only on pull requests
      When the sitting reads the pipeline
      Then it says a queued merge would wait forever, and offers the trigger before anything is queued
