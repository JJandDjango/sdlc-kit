# 35. Gates roll up their features, and a feature shows before intake

Status: accepted
Date: 2026-09-30

## Context

Kit 0.16.0 (0032) read each gate item `to do` while each verdict at
`gates/G0` read `done`, and a feature document with no contract was absent
from the tree, so a feature showed only once intake had written its
contract. The request is the feature document
`docs/features/tree-first-level.md`, written through an interview in
0029's format as 0033 amended it; the PO seat signed its request half at
r3 and the engineer seat its solution half at r6, and intake derived the
contract `tree-first-level` from it at r8.

Bound by: the tree computed at print, never stored (0031); the tree reads
one part of one document (0032); no headings read by the tooling (0029);
the signature form (0034); no change to what any gate checks.

## Decision

- **A gate item reads the roll-up of the features' verdicts at its
  gate**, and each of its conditions that condition across the same
  verdicts, by the rule a feature rolls up its children. An `inactive`
  verdict never counts, and a closed feature's verdicts count as they
  read. A gate item or condition that is not `done` names each feature
  holding it back, `<feature> holds <id> at <status>`. A finding counts in
  no roll-up.
- **A feature document with no contract is a feature before intake**, at
  the first level from its first revision. Its G0 verdict reads `to do`
  and counts at `gates/G0`. It shows its document's revision and its two
  halves, each signed in 0034's form or `to do`, and it never reads
  `done`. Once intake writes its contract, it stays one item, read as any
  contract is.
- **The tree reads one heading: a feature before intake's title line**,
  the first `# ` line, for its plain name only (the words after its first
  ` - `), and never checks it. A contract's `title` still comes from the
  contract, never from its document.

This amends 0029's non-goal "no headings read by the tooling" and 0032's
"the tree reads one part of one document": the tree also reads a feature
before intake's title line.

Recorded non-goals: no stored state; no ready check run by the tree; no G1
work; no feature under a gate item.

## Consequences

- `gates/G0` answers whether every feature has passed intake: a document
  before intake holds it at `to do` or `doing`.
- A feature is followed from its first revision, not from intake.
- Harder: a title line without ` - ` reads `(no title)`, and a signature
  typed in words reads unsigned (0034).
- The kit goes to 0.17.0; the contract schema stays at 1.5.0.
