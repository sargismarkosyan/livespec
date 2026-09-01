@feature:showing-before-it-is-built @workflow:adopt-the-process
Feature: What the one decision a person holds gets to look at

  @rule:the-decision-gets-what-the-prose-cannot-carry @planned
  Rule: Before approval is asked for, the person deciding is shown the evidence the change spec argues from and cannot carry at reading speed

    # @planned here means *nothing can hold it yet*, not *nobody built it*: the
    # instruction ships in refine-spec's section 7, and a headless session — the
    # only kind a case runs in — has no way to render a page at all, so no arm
    # can watch a sketch being drawn. Softening the Examples until a session
    # with no such tool could pass them would buy the tag with the exact
    # dishonesty evals/README.md warns about. See 0029, *What no case reaches*.

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

    # @planned for the same reason as the rule above — there is no sketch in a
    # session that cannot render one, so there is nothing for a case to read.
    # What *is* watchable is that nothing is put in its place, and that is held
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

    Example: this session has no way to render one
      Given a change spec with a before and an after worth showing
      And a session that cannot render a page at all
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
