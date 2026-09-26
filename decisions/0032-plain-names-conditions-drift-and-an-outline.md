# 32. The tree names what it shows, and the pane is an outline

Status: accepted
Date: 2026-09-26

## Context

Kit 0.15.0 (0031) printed one verdict per gate and ids with no plain name
beside them, and its pane showed only the path to the current task. In
session 49 the user found it drifted from their sketch: with no task in
flight the pane read `no current task` and one line of counts. The request
is the feature document `docs/features/project-tree.md`, written through an
interview in 0029's format and signed by both seats at r3; intake derived
the contract `project-tree` from it at r4.

Bound by: the tree computed at print, never stored, and no edits through it
(0031); no tooling reads a document's headings (0029); the contract's field
set (0005, amended as 0024 and 0030 did); no change to what any gate checks.

Alternatives weighed and rejected: Textual as a base dependency, which a
consumer's CI would install for nothing; the feature's title read from the
document's heading, which 0029 rules out; the contract's source revision
recorded in the contract, when intake's `Ready:` row already holds it;
reusing the `pane-view` id, which would re-derive a closed contract.

## Decision

- **Each item line opens on its id and its plain name**, taken from one
  source field: a gate's, a condition's or a task's name in the kit's
  lists, a unit's `done_means`, a check's sketch line, a finding's
  `statement`, a feature's `title`. The contract schema moves to 1.5.0 with
  an optional one-line `title`, which intake copies from the feature
  document's title line; the tree reads it from the contract. Only a
  feature keeps a summary, its `intent`.
- **Each gate opens into its conditions.** `taskcontract/data/gates.yaml`
  lists every gate's conditions, 57 in all. Each of G0's three reads the
  validator rules it owns, every code belongs to exactly one condition, and
  a condition that is not done lists its diagnostics. Each feature shows
  its active gates, then the next gate marked `inactive`, which never
  counts toward its status.
- **The tree reads one part of one document.** It opens each feature's
  `docs/features/<id>.md` for its revision table only and marks the feature
  `stale: document rN, contract from rM`, `no feature document` or `no
  "Ready:" row`. Intake writes the `Ready:` row in the shape the tree
  reads. This amends 0031, whose tree read no document.
- **Waiting and blocked items name why.** A blocked task names its
  `--reason`; the approval that holds the current task names its unit's
  `confirmed_by` seats. A closed contract reads done whatever its verdicts
  read.
- **The pane is an outline of the whole tree.** With the optional `pane`
  extra (Textual `>=8.2,<9`), `taskcontract tree --follow` shows every
  item, each feature open down to its units, moved through with the keys,
  clicks and the wheel, with a cursor line that holds the item's reference
  and whole plain name. A render keeps the cursor and each item's open state
  by its path from the root. The waiting line, the notify command and
  Ctrl-C's exit 0 carry over; the lines 0.15.0 wrote to stderr show inside
  the pane. 0.15.0's loop retires.

## Consequences

- The pane answers where each feature stands without a question to the
  agent. A live run in a herdr pane on Windows (session 55) passed the keys,
  clicks, the wheel, a render and Ctrl-C.
- Partial truth until the backfills: the kit's 16 contracts read `(no
  title)`, and the 15 besides `project-tree` read `no feature document`,
  until each gains a title and a document.
- Textual's major versions have broken its API; the pin makes a bump
  deliberate. The extra adds nine packages, and nothing else needs them.
- The 57 conditions in `gates.yaml` follow the gate pages by hand, and only
  G0's are computed; every other gate's read `to do` until its enforcement
  ships.
- The schema goes to 1.5.0, additively; the kit goes to 0.16.0.
