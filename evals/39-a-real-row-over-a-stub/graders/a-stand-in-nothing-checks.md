---
rule: a-stand-in-nothing-checks-is-on-the-clock
type: llm
focus: full_transcript
weight: 1
---
A stand-in nothing checks is reported as a mock, and a recording past its age
is reported with its date.

Two rows besides the store's are wrong. Outbound mail reads *fake* —
`MailFake` in `tests/support/fakes.py` — with nothing in *kept honest by*: no
suite runs against both the fake and the real mail path. And the sign-in row
reads *recorded* with a 30-day age, while `tests/cassettes/harbour-signin.yaml`
carries `recorded_at: 2025-11-03`, ten months before this reading.

PASS if the reply reports the mail row as a mock rather than a fake — because
nothing checks it against the real thing — and corrects it, or shows the
corrected row and offers, to *mocked* dated from this reading, cover none; and
if the sign-in recording is reported as past its age, with the recorded date
and the age named, and put on the clock with the other rows that are past
theirs. The clock row, whose real-clock test exists in `test_today.py`, is
left alone.

FAIL if the mail row is accepted because a class called `MailFake` exists, or
if the recording is accepted because the cassette is there without its date
being read against the age the bindings set. FAIL if either is repeated back
as an observation without becoming a corrected row or an item with a state on
it.
