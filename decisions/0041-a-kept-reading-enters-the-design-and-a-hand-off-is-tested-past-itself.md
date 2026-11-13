# 41. A kept reading enters the design, and a hand-off is tested past itself

Status: accepted
Date: 2026-11-12

## Context

Since the user's delegation of 2026-10-11 (`CONTRIBUTING.md`, Delegation),
a build settles each case the signed documents never name from their
purpose, builds on it, and lists it as a reading at the top of its PR. The
user keeps or overturns each one at the review. G1's units settled 39
readings this way (PRs #112, #116 and #119), and each PR said they belong
in the design at its next text row. That row, r9 of
`docs/features/g1-requirements-spec.design.md` (session 101), carried one
ruling and none of the 39.

Reading 3 of PR #112 kept a feature with no feature document from passing
G1. It was judged in session 92, when G1 refused nothing. `s5-start`,
drafted from the design, then added the refusal and I9's G1 line. Its
tests checked I9's words, and its receipt ran a plain request to the G1
line and read the refusal as the expected output. The engine found the
result on 2026-11-12: a contract green at G0 that can never be built. The
kit's own `glossary-alias-disjointness` had shown G1.3 `to do` for 25
days. The post-mortem and its evidence are in
`NOTES_g1-plain-request-post-mortem_2026-11-12.md`.

Alternatives weighed and rejected: overturning reading 3 alone (it fixes
this case and leaves 38 readings where no later unit reads them); folding
the readings at the release unit's row (too late: `s5-start` was built
before `s6-release`); dropping readings and stopping the build on every
case the documents never name (it brings back the per-session approvals
the delegation ended).

## Decision

1. A design's next text row takes every reading kept at a PR review since
   its last text row, or names each one it leaves out and why. Its
   `Measured:` row counts both.
2. A unit that adds a refusal, or turns a gate on, reads its feature's
   kept readings before its test list, and its PR names each reading whose
   cost it raises.
3. A hand-off's tests and receipt take the step it hands to, on each path
   into the hand-off. For intake, the paths are a plain request and a
   pair.
4. A condition that, as things stand, can never read `done` says so, and
   names its way out, apart from `to do`.

## Consequences

A unit's drafters see every kept reading in the design they work from,
and a dead end shows in the tree instead of hiding behind `to do`. Each
design text row now costs a sweep of the PR bodies since the last row,
and each hand-off unit's receipt runs one more step.

The rules bind by practice. No tool counts the readings yet; the signing
flow's `Measured:` row gains no field until a feature builds it. Rule 4 is
built for G1.3 by `s7-plain-request`; other conditions follow as their
edges are taken. Rule 1 binds `g1-requirements-spec`'s next design row,
which takes reading 3 of PR #112 and names the other 38 as left for Next
26's later rows.
