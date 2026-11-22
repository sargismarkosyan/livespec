@feature:walk-layers @workflow:adopt-the-process @uses:workflow-cost
Feature: Each walk is measured where the change can move it

  @rule:each-layer-holds-the-other-side-fixed @planned
  Rule: The sitting names the layers a walk is measured in — the front end with the service's answers replayed at a fixed delay, the back end with no browser, and the whole walk end to end — and the report keeps each layer apart

    Example: a shop with a browser front end and its own service
      Given a consuming repository whose walkthroughs drive a browser against its own server
      When the sitting wires the cost of a walk
      Then the front-end walk replays the server's recorded answers, so a slower server cannot move it
      And the back-end walk calls the server with no browser
      And the whole walk is measured too, and reported as end to end

    Example: a library with no service behind it
      Given a consuming repository that ships a component library and calls nothing
      When the sitting wires the cost of a walk
      Then the bindings name the front-end layer alone, and say why the other two do not apply

  @rule:the-report-names-the-layer @planned
  Rule: A sample names the layer it was taken in, and the report reads one measure in two layers as two lines, never as one

    Example: the same time, front end and end to end
      Given samples of the checkout walk's load time from the front end and from end to end
      When the comparison runs
      Then the report shows a line for each, naming its layer

  @rule:a-front-end-is-weighed-in-bytes-load-and-features @planned
  Rule: A front end is measured in the bytes it ships, the time its pages take to load, and the time each workflow's feature takes to be ready, read from a mark the app sets when it has painted

    Example: a page with a list to show
      Given a front end whose buy-a-print walk opens the shop and waits for the list of prints
      When the sitting chooses the front end's measures
      Then the bytes shipped are a count, and may carry a budget
      And the page's load time and the list's ready mark are times, and are reported
      And the app sets the ready mark itself, so the runner's own round trips are not counted

  @rule:setup-proposes-a-kit-for-the-stack @planned
  Rule: The sitting measures with what the repository already runs, proposes a tool for each layer nothing there can measure, says what installing it adds, and installs nothing the person has not agreed to

    Example: a bundle nothing weighs
      Given a consuming repository whose front end is bundled and nothing measures the bundle's size
      When the sitting wires the cost of a walk
      Then it proposes a tool that weighs the bundle and says what installing it adds
      And nothing is installed until the person agrees

    Example: the browser runner is already there
      Given a consuming repository whose walkthroughs already run in a headless browser
      When the sitting chooses how to time the front end
      Then it reads the times from that runner, and proposes no second browser tool
