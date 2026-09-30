# 36. The appendix names the contract, and a unit's row holds its done

Status: accepted
Date: 2026-09-30

## Context

ADR 0029 fixed the feature document's format; 0033 to 0035 amended it.
Writing `feature-document`'s own document (both halves signed at r8,
session 66) found four places where 0029's text no longer fits the kit,
its prerequisite 6. A contract copied into the appendix ages whenever the
contract changes, and the kit already holds the one copy at
`specs/<id>/contract.yaml` (Q6). Ready check 6 asks for a regression
check per entry of Existing behavior touched, not whether the entry is
true: the document's first draft kept a message no shipped flow prints
(Q8). 0029 tags the Gherkin as intake's, though each scenario restates a
check the PO seat signs and binds only on that seat's word (Q11). A
`done_means` intake derives can read broader than the line the engineer
seat signed (Q8, Q12), and the schema caps a unit at three sketches, so a
unit with four checks pairs two (Q6, Q8). Bound by the seats (0025), no
headings read by the tooling (0026, 0029), and the contract schema, which
the feature leaves unchanged. Decided at feature-document's Q6, Q8, Q10,
Q11 and Q12 (2026-09-30). Alternatives rejected: a copy re-rendered at
each intake (it still drifts between intakes); lifting the three-sketch
cap (a schema change, a non-goal).

## Decision

- **The appendix names the contract's path, never a copy.** Where the kit
  runs, 18.1 Contract reads `specs/<id>/contract.yaml`, the only copy.
  Before intake it reads "(none: intake writes `specs/<id>/contract.yaml`)"
  with no stamp, and is never stale. Without the kit, 0029 stands: the
  appendix is the contract's only home.
- **Ready check 6 asks where each entry was measured.** Existing behavior
  touched is listed or says "none"; every entry names the file or step it
  was measured from and has a regression check. The checks before the PO
  seat signs read each entry against its source, and an entry that no
  longer holds is an OPEN under ready check 6.
- **The interview derives the Gherkin, and the PO seat confirms it.** Once
  the checks are captured, the interview proposes one scenario per check,
  joined by its id, and the PO seat accepts, edits or drops each. 18.2
  Gherkin is tagged `[PO seat · derived from rN]`. A scenario whose Then
  needs a fact its check lacks is never offered, and the check is marked
  thin; a dropped scenario marks its check thin too. Ready check 3 reads a
  thin check as an OPEN.
- **The Units table carries a Done means cell**: the unit's `done_means`
  in the engineer seat's words, which intake copies word for word. In the
  Checks cell, `+` joins two checks that share one sketch, and that sketch
  ends in both ids. A unit still holds at most three sketches.
- **A `Parked:` row changes no text.** Intake's refusal writes `rN:
  Parked: {what stands}` and no contract. Like `Ready:`, `Measured:` and
  `Signed:`, it never ages a stamp or the drift mark, never moves the
  newest revision, and is never the row a `Signed:` row signs.

This amends 0029: 18.1 shows no copy where the kit runs, ready check 6
gains the entry's source, 18.2's owner moves from intake to the PO seat,
and 13.6 Units gains a cell. It amends 0034: the rows that change no text
are `Ready:`, `Measured:`, `Signed:` and `Parked:`.

Recorded non-goals: no change to the contract schema, so a check's id
stays text at the end of its sketch line; no tool reads a document's
sections, so the ready checks stay asked, never parsed (0029); no change
to the seats (0025).

## Consequences

- `feature-document` carries the change into the template (`f1-format`),
  the interview's flows (`f2-sections`, `f3-signing`) and intake
  (`f4-intake`). Until `f4-intake` ships, intake writes no `Parked:` row
  and the tree reads one as text.
- The documents written by hand (project-tree, G1, tree-first-level) stay
  as written. G1's solution half, still written by hand, follows this ADR.
- Harder: intake no longer rewords a `done_means`, so the engineer seat
  writes each one to pass the language door as it stands; the checks
  before that seat signs run them.
