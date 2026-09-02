@feature:showing-before-it-is-built @workflow:adopt-the-process
Feature: What the one decision a person holds gets to look at

  @rule:the-decision-gets-what-the-prose-cannot-carry @planned
  Rule: Before approval is asked for, the person deciding is shown the evidence the change spec argues from and cannot carry at reading speed

    # @planned here means *nothing holds it yet*, not *nobody built it*: the
    # instruction ships in refine-spec's section 7. Until 0031 no case could
    # reach it at all — a headless session had no way to render a page, so no
    # arm could watch a sketch being drawn. A sketch written to a file is
    # readable, so what keeps the tag on is only that no case claims this yet.
    # It comes off when one does. See 0031, *What we are not doing*.

    Example: the change alters something that has a before and an after
      Given a change spec proposing a different state for something a person already uses
      When the spec is handed back
      Then what it would become is shown beside what it is now
      And the difference between the two is what the sketch is of

    Example: the change moves nothing anybody looks at
      Given a change spec whose whole result is which things are counted and which are not
      When the spec is handed back
      Then what moves and what stays is shown with the reason against each
      And having no screen has not been read as having nothing to show

    Example: nobody thought to ask for it
      Given a change spec finished and ready to be decided on
      When the spec is handed back
      Then the sketch is there with it
      And it did not have to be asked for after the decision was already due

  @rule:what-is-shown-is-not-the-spec-again @planned
  Rule: The sketch carries the evidence and sends the reader to the spec for the reasoning, so nobody is left holding two versions of the same argument

    # @planned alongside the rule above and now for the same reason: a written
    # sketch is readable by a case, and no case claims either of them yet.
    # What *is* watched today is that nothing is put in a sketch's place, held
    # by the rule below rather than softened into this one.

    Example: the spec already argues its case under its own headings
      Given a change spec saying who this is for, the job behind the request, why now and the end value
      When the sketch is drawn
      Then none of those four are restated in it
      And it points at the spec for every one of them

    Example: the reader wants to know why
      Given somebody who has looked at the sketch and wants the reasoning
      When they go looking for it
      Then the sketch sends them to the change spec
      And what they approve is the spec rather than the sketch

    Example: the spec is corrected after the sketch was shown
      Given a change spec that has been revised since the person last looked
      When they are asked to decide again
      Then what they were shown is corrected where it already stands
      And a second version has not appeared beside the first

  @rule:an-absent-sketch-is-said-rather-than-filled
  Rule: Where there is nothing to draw, or nowhere to draw it, that is one line, and nothing is put in its place

    # Its first example is the one shape no case here can take: a session able
    # to write the spec files is able to write a page, so the harness cannot
    # produce one that can do neither. The rule is claimed on its others.

    Example: this session has no way to render one
      Given a change spec with a before and an after worth showing
      And a session that can neither publish a page nor write a file
      When the spec is handed back
      Then it says in a line that the sketch could not be drawn here
      And what it hands back is the spec, with nothing written out in the sketch's place
      And the rest of the session is not spent looking for another way to draw it

    Example: the spec's prose already carries the whole of it
      Given a change spec with no before, no ledger and no count that moves
      When the spec is handed back
      Then it says in a line that there is nothing the prose cannot carry
      And nothing is produced to fill the space

    Example: what would be drawn was never settled
      Given a change spec that does not establish the state the change starts from
      When the sketch is drawn
      Then only what the spec establishes is in it
      And nothing is invented to make it look complete

    Example: the evidence is real and awkward to lay out
      Given a change whose before and after are tedious to draw side by side
      When the spec is handed back
      Then it is drawn anyway
      And the difficulty is not read as the exemption

  @rule:a-missing-tool-is-not-a-missing-page @planned
  Rule: A sketch takes whichever form the session can produce — a published page where the host has one, a written file where it does not — and only a session that can produce neither says so instead

    Example: the host has no tool that publishes a page
      Given a change spec with a before and an after worth showing
      And a session that cannot publish a page but can write a file
      When the spec is handed back
      Then the sketch is written as a page the person can open
      And its path is handed over beside the change spec
      And one absent tool has not been read as having nowhere to draw it

    Example: the spec is revised after the page was written
      Given a sketch already written as a file the person has opened
      When the spec is revised and handed back again
      Then that same page is rewritten where it already stands
      And a second file has not appeared beside the first

    Example: the spec is committed
      Given a sketch written as a file for one decision
      When the spec is committed
      Then the page is not part of that commit
      And the change spec is still the only record the repository keeps
