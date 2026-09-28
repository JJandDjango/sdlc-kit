# 34. A seat signs its half in a revision row

Status: accepted
Date: 2026-09-28

## Context

ADR 0029 made a named seat's signature on a named revision the record
that a half is understood, and left the signature's form free. Until now
a seat signed in words at a row's end: "Signed by the PO seat (user)".
tree-first-level shows a feature in the pane from its first revision,
with which halves its seats have signed (its SC3), so the tree must read
a signature, and it cannot read free words. 0029 says the tooling reads a
row's number and never its words; 0.16.0 already reads a row's opening
word, `Ready:` or `Measured:`, for the drift mark. Bound by the seats
(0025) and no headings read by the tooling (0026, 0029), so the signature
lives in the revision table, which the tooling already reads. Decided at
tree-first-level's Q10 (2026-09-28).

## Decision

- **A signature is a revision row** whose changes cell opens `rN:
  Signed: request half` or `rN: Signed: solution half`; free words may
  follow. The signer is the row's `Revised By` cell. The half names its
  seat: the PO seat signs the request half, the engineer seat the
  solution half.
- **It signs the newest row above it** that opens on none of `Ready:`,
  `Measured:` or `Signed:`. It changes no text.
- **It never ages a stamp or the drift mark**, as a `Measured:` row does
  not.
- **A half's latest `Signed:` row counts.** A row in any other form, or
  one that names neither half, is no signature.
- **The documents signed in words gain a `Signed:` row** that restates
  the signature: tree-first-level at r4 and `g1-requirements-spec` at
  r4, each signing r3.

This amends 0029: a `Measured:` row is no longer the one row that does
not age a stamp, and the tooling reads a row's opening words, `Ready:`,
`Measured:` and `Signed:`, besides its number.

Recorded non-goals: no change to the seats (0025); no check on
understanding (0029), since a signature still records a named seat on a
named revision.

## Consequences

- The tree can show which halves a feature before intake has signed
  (tree-first-level, unit t3), and the drift rule leaves out `Signed:`
  rows.
- `feature-document` writes `Signed:` rows in the interview and checks
  their form in the readiness check. Until it lands, the interview writes
  them by hand.
- Harder: a signature typed in words reads unsigned, and the tree shows
  that half `to do`. A document in Google Docs needs the fixed words
  typed exactly.
- project-tree's document predates this ADR and stays as written: it has
  a contract, so the tree never reads its halves.
