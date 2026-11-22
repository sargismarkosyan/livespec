@feature:wiring-many-merges @workflow:adopt-the-process
Feature: What an audit reads back about how several pull requests merge

  @rule:the-queue-is-read-back @crosses:consuming-repository
  Rule: The audit reads the merge queue row back from the platform and the pipeline, and reports it open when the queue, its trigger or the named fallback is not what the platform has

    Example: no row at all
      Given bindings with no row saying how several pull requests merge
      When the audit tool reads them
      Then the line reads open, with the setup sitting as what closes it

    Example: the queue row says on, and the pipeline lost the trigger
      Given a row saying the queue is required on the main branch
      And a pipeline whose required checks no longer run on the queue's event
      When the audit reads both back
      Then the line reads open, naming the workflow that lost the trigger

    Example: the fallback row, with the update setting turned off
      Given a row saying no queue is available and the platform updates each branch instead
      And a platform whose setting for updating a branch is off
      When the audit reads the setting back
      Then the line reads open, naming the setting

  @rule:main-is-read-green @crosses:consuming-repository
  Rule: The audit asks the platform whether the main branch's pipeline is green now and was green on every run since the last audit, through the command the bindings name, and reports a red run open

    Example: no row names the command
      Given bindings with no row saying how the main branch's runs are read
      When the wiring is audited
      Then the line is open and names the setup sitting

    Example: the row names the command
      Given bindings naming the command that lists the main branch's runs
      When the wiring is audited
      Then that command is handed to the mind answering, with the date of the last audit
      And a red run is to be reported open, naming the first and the last

    Example: nothing runs on the main branch
      Given bindings saying the main branch's runs are not applicable, with why
      When the wiring is audited
      Then the line is not applicable, quoting the row
