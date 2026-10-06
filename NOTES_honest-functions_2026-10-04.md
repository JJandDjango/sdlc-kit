# Notes - honest and dishonest functions (2026-10-04)

Status: backlog. Material for the interview's materials step (O5) when
this becomes a feature. No contract, no ratified term.

Source: Logan Smith, "How to write the perfect function",
https://youtu.be/2OMRWPOSw9s, 7:29 to 25:56.

## The idea

An honest function reaches the outside world only through its signature.
A dishonest function reads or writes something its signature does not
name: the clock, a random source, the environment, a file, the network,
a process, a mutable global. A caller of a dishonest function is
dishonest too. So honest code sits at the leaves of the call tree, and
the dishonest code is a thin shell at the top.

## What the kit holds today

- G4.4: property tests run under a derived seed, so the merge gate
  repeats exactly.
- G5.2 and G5.3: fresh seeds, and each red ships a replay recipe.
- G4.11: a flaky test goes to an audited quarantine (class E).

All three govern the test run. None reads the code under test for what
it touches, and none reads a test's own body.

## Candidate conditions: checking

1. Shell boundary (G3.2 analyzer battery, or G4.2 architecture tests).
   Outside the declared shell paths, no call to a banned ambient API.
   Tier: tripwire, a fail is bad and a pass proves little. Bindings:
   ruff's banned-api rule (TID251) with per-path ignores; for .NET,
   BannedApiAnalyzers (RS0030, `BannedSymbols.txt`).
2. Hermetic tests (G4.11, the unit partition). A unit test's body calls
   no banned ambient API. The clock, the seed and the temp path arrive
   through the runner's fixtures. This finds a flaky test when it is
   written, before the quarantine.
3. Order agreement (G4.11). The unit partition is green under a shuffled
   order derived from the candidate's seed. The dynamic backstop for
   what condition 1 cannot see: module-level state, and mutation
   through `self`.
4. Thin shell (G4.8 ratchets). Shell paths take a low branching cap:
   they hold wiring, and no logic worth a unit test.

## Candidate conditions: generating

- Honest unit: examples and properties written from the signature alone,
  with no mock. G4.4 and G5.5's mutation floor count it.
- Dishonest unit: no mocked unit test. One wiring test at G5.1, and the
  branching cap stands in for coverage. Exempt from the mutation floor.
- The drafter needs the kind before it writes. The solution half names
  each unit's shell files, and intake copies them.

## Open

- Declared per path, not per function: whether a function is honest is
  not decidable in general (THEORY's non-goals), and a path is the
  proxy. Where does the list live: `.sdlc/config.yaml`, or a field on
  each unit?
- The injection hole: an honest function that takes a callback still
  does whatever the callback does.
- The banned list differs per stack: profile data.
- "honest", "dishonest" and "shell" are terms to ratify, or to replace
  with plainer words.
- A measure first: which of the kit's own modules would fail condition 1
  today.
