| Revision Date | Revised By | Changes Made |
| :-: | :-: | :-- |
| 2026-09-27 | user | r1: Created in kit session 59 through an interview with the user, one question at a time, in the format ADR 0029 ratified and ADR 0033 amended; typed by Claude on the user's word. The request half, in progress. PO seat: user; engineer seat: user |
| 2026-09-28 | user | r2: Measured: ADR 0033's checks before signing, on the request half, run by Claude on the user's word: no new term clashes with a ratified term; `half` and `intake` trip CL003, and the dictionary cedes both at intake; lang-check's contract rules find 90 in the text intake copies (72 unknown words, 10 sentences over the cap, 7 check sentences that open on no verb, 1 on a pronoun), each left to intake's rewrite of the contract's wording |
| 2026-09-28 | user | r3: The request half finished in kit session 59: the terms (Q9), ADR 0033's checks before signing (r2), ready checks 1 to 8 read back with no fix; typed by Claude on the user's word. Signed by the PO seat (user) |
| 2026-09-28 | user | r4: Signed: request half. The PO seat's r3 signature, restated in the form Q10 fixed; typed by Claude on the user's word |
| 2026-09-28 | user | r5: Measured: ADR 0033's checks before signing, on the solution half, run by Claude on the user's word: Scope holds the release unit's paths, `CHANGELOG.md`, `decisions/` and `docs/` are free paths, and no out-of-scope path falls inside Scope; no new term; ready check 11 finds two facts with no Sources row (a feature's place at the first level, a feature's status); 12 and 13 pass |
| 2026-09-28 | user | r6: The solution half finished in kit session 59 through Q10 to Q15: the signature form, Interfaces with its examples and edges, Sources, Scope, Out of scope, Constraints, Units, Order, Risks and cost; ready check 11's two Sources rows added (r5); typed by Claude on the user's word |
| 2026-09-28 | user | r7: Signed: solution half. The engineer seat signs r6 |

# tree-first-level - The tree's first level shows where each gate and feature stands

`sdlc_development_kit` · seats: PO user, engineer user · contract:
`tree-first-level`, draft · PR: none · merge SHA: none

## Statement

`[PO seat · authored]`

As a developer, I want the tree's first level to show where each gate and
each feature stands, so that I can follow every feature in the pane from
its first revision, and read each gate's status as its features' verdicts
give it.

## Description

`[PO seat · authored]`

Today the tree's first level shows less than the work holds, in two
places:

- The top item reads `gates/G0 Planning / Intake [to do]`, and its three
  conditions read `to do`, although all 16 features' own G0 verdicts read
  `done`. project-tree never said where a gate item's status comes from,
  so it always reads `to do`. G1's feature document names this gap and
  leaves it to this feature.
- G1's feature document has been in progress since session 58, with its
  request half signed at r3, and the pane shows none of it. A feature
  enters the tree only with a contract, which intake writes. A feature's
  interview, its checks before signing and its seats' signatures all
  happen before intake, where the pane cannot see them. This document is
  the second such feature.

With this feature, a feature shows in the pane from its first revision,
and each gate reads what its features' verdicts say.

## Background

`[PO seat · authored]`

project-tree, released in kit 0.16.0, defines the tree and the pane
(`docs/features/project-tree.md`, ADR 0031). Measured on the kit at
`6ca8492`, 2026-09-27: the first level holds `gates/G0` and 16 features.
Each feature's G0 verdict reads `done`, and each G1 verdict reads `to do`,
marked inactive. The tree opens a feature's document only for its
revision table, to mark drift, and never opens a document that has no
contract, so `g1-requirements-spec` shows nowhere. The pane already
redraws when a file under `docs/features/` changes
(`taskcontract/tree_view.py:66`). The ratified term Feature reads "a
piece of work with its own feature document and contract; a top-level
item of the tree", so a feature before intake falls outside it. G1's
feature document leaves the `gates/G0` line to this feature in its
non-goals. Its SC5 has the tree show each feature's G1 conditions once G1
is active.

### Existing behavior touched

Each entry gets a regression check under Acceptance criteria.

1. The first level lists each active gate and each gate a finding names,
   in the kit's order. Then comes `gates/none` when a finding names no
   gate, then each feature with a contract, in folder order
   (`taskcontract/tree.py:17`).
2. A feature's G0 verdict reads as the validator says: `done` at
   ready-green, `blocked` when draft-green with `TC003`, `to do` when
   draft-green otherwise, `failed` when draft-red. The next gate after the
   active ones shows marked inactive (project-tree SC2.1).
3. A feature rolls up its units and its verdicts, but not the inactive
   one. A closed contract's verdicts never count, so a closed feature
   reads `done` once its units do.
4. A feature's drift mark comes from its document's revision table: `no
   feature document`, `no "Ready:" row`, or `stale: document rD, contract
   from rM`.
5. A finding stands once, under the condition or gate its `gate:` field
   names, and shows its kind, never a status.
6. A feature with a contract takes its plain name from the contract's
   `title`, never from its document.

## Success criteria

`[PO seat · authored]`

1. SC1: Each gate item reads the roll-up of its features' verdicts at
   that gate, and each of its conditions reads the roll-up of that
   condition across the features.
2. SC2: A feature whose document has no contract yet shows at the first
   level from its first revision.
3. SC3: A feature before intake shows its newest revision and which
   halves its seats have signed.
4. SC4: A feature keeps one item from its first revision on. Intake's
   contract joins that item and never adds a second one.

## Non-goals

`[PO seat · authored]`

- No new authorizations are added (the standing line).
- Nothing stored: the tree still computes every status at each print and
  writes no file (ADR 0031).
- No document text beyond SC3: a feature before intake shows its revision
  and its signed halves, never its statement, criteria or checks.
- No ready checks: the tree does not run a document's ready checks 1 to
  14. They stay with `feature-document`'s readiness check.
- Not G1: G1's rules, the status of its conditions, and its activation
  stay with G1's feature document (its SC5). A gate item rolls up
  whatever verdicts its features hold.
- No features under a gate: a gate item does not list its features as
  children, and features stay at the first level.
- Not the pane's layout: its keys, its fold rule and its line layout stay
  as 0.16.0 ships them.
- Not prerequisite 7: the 15 contracts without a document keep their `no
  feature document` mark.

## Prerequisites

`[PO seat · authored]`

1. The tree, the pane, and the rule by which a feature rolls up its units
   (exist: `taskcontract/tree.py`, kit 0.16.0).
2. Each feature's verdict at an active gate, and its conditions' statuses
   (exist for G0, from the validator. Every other gate reads `to do`
   until it is built; G1's are owned by G1's feature document).
3. The feature document's revision table, with its `Ready:` and
   `Measured:` rows (exists: ADR 0029).
4. A signature the tree can read in the revision table: which seat signed
   which half at which revision (missing: today a signature is free words
   at a row's end. Owner: this feature, through a new ADR that amends ADR
   0029's format).
5. The documents before intake rewritten to that signature form:
   `g1-requirements-spec` at r3, and this document (missing. Owner: this
   feature, one revision row each).
6. The ratified term Feature covering a feature before intake (missing:
   its definition names a contract. Owner: this feature, at intake).
7. A person to sign each half (exists: the user, holding both seats).

## Acceptance criteria

`[PO seat · authored]`

### Checks

Three checks under each success criterion. SC2.3, SC2.2, SC4.3, SC3.3,
SC1.3 and SC4.2 carry the regression checks for Existing behavior touched,
entries 1 to 6 in that order.

SC1 Gate status

- SC1.1: verify a gate item reads the roll-up of its features' verdicts at
  that gate, by the rule a feature rolls up its units. A closed feature's
  verdicts count as they read, every verdict marked inactive is left out,
  and the gate reads `to do` when no verdict counts
- SC1.2: verify each condition under a gate item reads the roll-up of that
  condition across the same verdicts. A gate or condition that is not
  done names, as a diagnostic, each feature whose verdict or condition is
  not done, with its message under Error messages
- SC1.3: verify a finding still stands once under the condition or gate
  its `gate:` field names, shows its kind and never a status, and counts
  in no gate's roll-up

SC2 Features before intake

- SC2.1: verify a document at `docs/features/<id>.md` with no contract at
  `specs/<id>/contract.yaml` shows as a feature at the first level from a
  table holding only its r1 row. Its plain name comes from the document's
  title line, the words intake copies into the contract's `title`
- SC2.2: verify a feature before intake reads its G0 verdict `to do`,
  with its next gate marked inactive, and that verdict counts in
  `gates/G0`'s roll-up. A feature with a contract still reads its G0
  verdict as the validator says: `done` at ready-green, `blocked` when
  draft-green with `TC003`, `to do` when draft-green otherwise, `failed`
  when draft-red
- SC2.3: verify the first level still lists each active gate and each
  gate a finding names, in the kit's order, then `gates/none` when a
  finding names no gate, then the features. Features with a contract keep
  their folder order, and a feature before intake sits among them by its
  id

SC3 Revision and signatures

- SC3.1: verify a feature before intake shows its document's newest
  revision and, for each half, the seat and revision that signed it, or
  that no seat has signed it. The feature reads `to do` until a seat
  signs a half, then `doing`
- SC3.2: verify a document whose revision table holds no counted row
  shows the feature with its message under Error messages. A signature
  row in any form other than the one the new ADR fixes counts as no
  signature
- SC3.3: verify a feature with a contract still carries its drift mark
  from its document's revision table: `no feature document`, `no "Ready:"
  row`, or `stale: document rD, contract from rM`

SC4 One item

- SC4.1: verify that once `specs/<id>/contract.yaml` exists, the feature
  shows once, with its contract's verdicts, units and drift mark, and none
  of SC3's revision or signatures
- SC4.2: verify a feature with a contract still takes its plain name from
  the contract's `title`, never from its document
- SC4.3: verify a feature still rolls up its units and its verdicts, but
  not the inactive one, and a closed feature reads `done` once its units
  do, its verdicts never counting

### Error messages, verbatim

Two new messages:

1. `{feature} holds {id} at {status}` (SC1.2), such as
   `g1-requirements-spec holds G0 at to do`
2. `no revision table` (SC3.2)

Every message the tree prints today stays word for word.

---

## Proposed solution

`[Engineer seat · authored]`

### Scope

- `taskcontract/tree.py`
- `taskcontract/tree_view.py`
- `taskcontract/pane.py`
- `tests/`
- `USAGE.md`
- The release unit's: `pyproject.toml`, `skills/sdlc/init.py`
  (`KIT_VERSION`), `.github/workflows/sdlc.yml`

At intake, outside the build: ADR 0034 for the signature form (Q10), the
terms with the dictionary ceding `half` and `intake`, and
`g1-requirements-spec`'s backfill `Signed:` row (prerequisites 4 to 6).
This document's own backfill row is r4, written before its solution
half's rows so that it signs r3.

### Out of scope

- `taskcontract/checker.py`: the validator's rules and its G0 readings
- `taskcontract/data/gates.yaml`: the gates, their conditions and G0's
  rules
- `taskcontract/progress.py`: progress records
- `skills/sdlc/flows/intake.md`: intake's steps
- `skills/product-specification-interview/`: the template and the
  interview, `feature-document`'s

### Interfaces

No new command, flag or file. The tree's printed lines gain three shapes;
a line keeps 0.16.0's layout: id, plain name, status, marks, evidence,
links, `doc:`, summary.

A feature before intake, drawn from `g1-requirements-spec` once its
backfill adds `r4: Signed: request half`. Its halves are two items after
its verdicts, so the roll-up gives SC3.1's `to do` and `doing`:

```
g1-requirements-spec Failure points found before development starts [doing] no contract: document r3 doc: docs/features/g1-requirements-spec.md
  g1-requirements-spec/G0 Planning / Intake [to do]
    g1-requirements-spec/G0/G0.1 Definition-of-ready [to do]
    g1-requirements-spec/G0/G0.2 Vocabulary coverage [to do]
    g1-requirements-spec/G0/G0.3 Unit confirmation [to do]
  g1-requirements-spec/G1 Requirements / Spec [to do] inactive
    g1-requirements-spec/G1/G1.1 Spec/schema linting [to do]
    g1-requirements-spec/G1/G1.2 Model checking [to do]
    g1-requirements-spec/G1/G1.3 Criteria completeness + ambiguity review [to do]
  g1-requirements-spec/request Request half [done] by user at r3
  g1-requirements-spec/solution Solution half [to do]
```

The gate item, with that feature and this one before intake:

```
gates/G0 Planning / Intake [doing]
  - g1-requirements-spec holds G0 at to do
  - tree-first-level holds G0 at to do
  gates/G0/G0.1 Definition-of-ready [doing]
    - g1-requirements-spec holds G0.1 at to do
    - tree-first-level holds G0.1 at to do
  gates/G0/G0.2 Vocabulary coverage [doing]
    - g1-requirements-spec holds G0.2 at to do
    - tree-first-level holds G0.2 at to do
  gates/G0/G0.3 Unit confirmation [doing]
    - g1-requirements-spec holds G0.3 at to do
    - tree-first-level holds G0.3 at to do
```

In the pane, the closed gate reads `gates/G0 Planning / Intake [doing]
(2 diagnostics)`, the pane's rule for a closed item holding diagnostics.

The signature row, in a feature document's revision table (Q10):

```
| 2026-09-28 | user | r4: Signed: request half. The PO seat signs r3 |
```

The query, `taskcontract tree <id>`, on a feature before intake and on a
half. A half's `file:` is the line of its latest `Signed:` row, or line 1
when unsigned:

```
g1-requirements-spec Failure points found before development starts [doing] no contract: document r3
doc: docs/features/g1-requirements-spec.md:1
```

```
g1-requirements-spec/request Request half [done] by user at r3
file: docs/features/g1-requirements-spec.md:6
```

Edges:

- No feature at all: `gates/G0 Planning / Intake [to do]`, no diagnostic.
- Every feature done at G0: `gates/G0 Planning / Intake [done]`, no
  diagnostic.
- A document with no counted revision row: `x Some title [to do] no
  revision table doc: docs/features/x.md`, both halves `to do`.
- A document with no title line, or one that cannot be read as text: the
  plain name reads `(no title)`, as a contract's does without a title; an
  unreadable one also reads `no revision table`.
- A `Signed:` row that names neither half counts as no signature.
- A feature with a contract shows no halves (SC4.1), and its `Signed:`
  rows never age its drift mark.
- The narrowest pane: lines cut as 0.16.0 cuts them.

### Sources

| Fact | Read from | When two disagree |
| :-- | :-- | :-- |
| A feature before intake | each `*.md` file directly under `docs/features/` that has no `specs/<id>/contract.yaml` | the contract wins: once it exists, the feature shows as one with a contract (SC4.1) |
| Its id | the file's name without `.md` | the file name wins; the id in the title line is never read |
| Its place at the first level | its id, among the features' ids in folder order | none: ids are unique |
| A feature's status | the roll-up of its children, leaving out the inactive verdict: its verdicts, its units, and before intake its halves | a closed contract's verdicts never count toward its own feature |
| Its plain name | the title line's words after its first ` - ` | the contract's `title` wins once a contract exists (SC4.2) |
| Its revision (`document rN`) | the highest N of a counted row that opens on none of `Ready:`, `Measured:` or `Signed:` | one rule, shared with the drift mark |
| A half's signature | that half's latest `Signed:` row; the signer from its `Revised By` cell; the revision is the newest text row above it | the latest row wins; a row naming neither half is no signature |
| Its G0 verdict | always `to do`, since the validator has no contract to read | none |
| A gate item's status | the roll-up of each feature's verdict at that gate, with inactive verdicts left out | a verdict wins over findings, which never count; a closed feature's verdicts count as they read, since its close governs only its own roll-up |
| A gate's condition | the roll-up of that condition across the same verdicts | none |
| A `holds` diagnostic | each feature whose verdict or condition is not done, in the tree's feature order | none |

### Constraints

1. The tree is computed at each print and writes no file (ADR 0031).
2. Every line printed today for a feature with a contract, its verdicts,
   units, tasks and checks, and every finding stays byte for byte; only a
   gate item and its conditions change.
3. The validator runs only for a feature with a contract; the pane's
   verdict cache stays keyed by contract id.
4. A feature document is read once per print, and only its first table
   and its first `# ` line.
5. No new dependency; the pane extra stays optional.

### Units

| Unit | Checks | Tests, by check id and kind | Retirements |
| :-- | :-- | :-- | :-- |
| `t1-gate-rollup` | SC1.1, SC1.2, SC1.3 | one automated test per check | the rule that a gate item and its conditions always read `to do`: `taskcontract/tree.py`'s module docstring and `derive` docstring, `USAGE.md:891`; the assertions that pin it over done verdicts, found by test-retirer (seen at `test_tree_status.py:402`, `test_tree_conditions.py:547`, `test_tree_titles.py:274`, `test_tree_query.py:293`, `test_pane.py:502`, `test_pane_keys.py:631`) |
| `t2-before-intake` | SC2.1, SC2.2, SC2.3, SC4.1 | one automated test per check | the module docstring's "opens each contract's docs/features/<id>.md for its revision table only"; any fixture assertion that a document without a contract shows nothing, found by test-retirer |
| `t3-halves` | SC3.1, SC3.2, SC3.3, SC4.3 | one automated test per check; for SC3.1 also a manual receipt, a live pane on the kit showing `g1-requirements-spec`'s halves and `gates/G0 [doing]` | the drift rule's "every row but `Ready:` and `Measured:`", which now also leaves out `Signed:` rows (docstring and `drift`) |
| `t4-release` | SC4.2 | automated | `KIT_VERSION` moves to `0.17.0`; `USAGE.md`'s marks go green; a `CHANGELOG.md` entry |

### Order

`t1-gate-rollup`, then `t2-before-intake`, then `t3-halves`, then
`t4-release`. SC2.2 tests that a feature before intake counts in
`gates/G0`'s roll-up, which is `t1`'s; `t3` hangs the halves on the item
`t2` creates; `t4` ships. None runs beside another: each changes lines the
next one's tests pin.

## Risks and cost

`[Both seats · authored]`

Risks:

1. A parked or abandoned document holds `gates/G0` at `doing` as long as
   it stands before intake; the `holds` diagnostic names it. A parked
   state for a document is later work, outside this feature.
2. Every `.md` file under `docs/features/` counts as a feature (Q12); the
   kit holds none that is not one.
3. A signature typed in words reads unsigned. Until `feature-document`
   lands, the interview runs by hand and must write `Signed:` rows; ADR
   0034 and `STATE.md`'s standing practice carry the form.
4. One feature's broken contract makes its whole gate read `failed`: true
   but loud, and the `holds` diagnostic names the feature.
5. Once G1 is active, `gates/G1` lists every feature not through it; the
   pane folds the list as `(k diagnostics)`.

Cost: four units, each about the size of a project-tree unit; two to
three sessions after intake.

Worth: built before G1's solution half resumes, so the pane follows all of
G1's remaining work, from its solution half through its build; G1 slips
by about three sessions.

## Decisions and open questions

`[Both seats · authored]`

- Q: One feature or two? A: One: both gaps answer what the first level
  says about the work in flight, and only the second shows G1's work
  before its intake (scope, decided 2026-09-27).
- Q: A revision of project-tree's document, or a new one? A: A new one:
  project-tree is released, and G1's document leaves the `gates/G0` line
  to this feature (scope, decided 2026-09-27).
- Q: The feature's id? A: `tree-first-level`: both gaps change the tree's
  first level, project-tree's word for its top items (Q1, decided
  2026-09-27).
- Q: Where does a gate item's status come from? A: The roll-up of its
  features' verdicts at that gate; a verdict marked inactive is left out,
  and a closed feature's verdicts count as they read (SC1, decided
  2026-09-27).
- Q: Does a gate item list its features? A: No: a gate or condition that
  is not done names each feature holding it back as a diagnostic (SC1.2,
  Q6, decided 2026-09-27).
- Q: A feature before intake's name and status? A: Its title line, the
  words intake copies into the contract; `to do` until a seat signs a
  half, then `doing`; its G0 verdict reads `to do` and counts in
  `gates/G0` (SC2.1, SC2.2, SC3.1, Q8, decided 2026-09-27).
- Q: How does the tree read a signature? A: In a form a new ADR fixes,
  amending ADR 0029's; until then this document and G1's carry their
  signatures in words (prerequisites 4 and 5, Q7, decided 2026-09-27).
- Q: The signature's form? A: A row whose changes cell opens `rN:
  Signed: request half` or `rN: Signed: solution half`, free words after;
  the signer is the row's `Revised By` cell, and the half names its seat.
  It changes no text and signs the newest row above it that is neither
  `Ready:`, `Measured:` nor `Signed:`; it never ages the drift mark; a
  half's latest `Signed:` row counts (Q10, decided 2026-09-28).
- Q: How does a feature before intake draw? A: Its halves are two items
  after its verdicts, `<id>/request` and `<id>/solution`, `done` with
  `by <signer> at rN` once signed; its line carries `no contract:
  document rN`; so the ratified term Item gains "half" at intake (Q11,
  decided 2026-09-28).
- Q: Does `t1-gate-rollup` split, since it adds behavior and retires
  some? A: No: its retirement is about ten assertions that flip to the
  new value on existing fixtures, not a body of old behavior like o6's
  150 cases, and a retiring half would deliver no check (ready check 9).
  ADR 0033's split rule is read as bounding a drafter's load (Q14,
  decided 2026-09-28).
- Q: Build this before G1's solution half? A: Yes: the pane then follows
  all of G1's remaining work; G1 slips by about three sessions (Q15,
  decided 2026-09-28).
- Q: Do the solution half's checks before signing read green? A: Yes,
  once ready check 11's two missing Sources rows were added: a feature's
  place at the first level and a feature's status (r5, r6, decided
  2026-09-28).
- Q: When is this document's own signature backfilled? A: Now, as r4,
  before its solution half's rows, so that it signs r3; at intake it
  would sign r6 (decided 2026-09-28).
- Q: Does Feature keep its ratified definition? A: No: it names a
  contract, so intake amends it to cover a feature before intake (Q9,
  decided 2026-09-28).
- Q: Do the checks before signing read green? A: No, and each finding is
  answered: `half` and `intake` are ceded by the dictionary at intake;
  the 90 language findings in the statement, the non-goals and the checks
  are answered by intake's rewrite of the contract's wording, and this
  document keeps the PO seat's words (r2, decided 2026-09-28).

## Appendix

### Terms

`[PO seat · authored]`

Decided at the interview's Q9 (2026-09-28). Seventeen map to the kit's
ratified terms: Tree, Pane, Item, Feature, Feature document, Gate, Active
gate, Condition, Verdict, Status, Finding, Diagnostic, Plain name, Stale,
Seat (`intake-seat`, by its alias), Unit (`decomposition-unit`) and Check
(`acceptance-sketch`). Feature takes a new definition at intake
(prerequisite 6):

- Feature: a piece of work with its own feature document, and a contract
  once intake writes it; a top-level item of the tree.

The rest become terms to ratify at intake.

- First level: the tree's top items: each gate item, `gates/none`, and
  each feature.
- Gate item: a gate's item at the first level, `gates/<gate>`, holding
  its conditions and the findings that name it. A verdict is one
  feature's result at a gate; a gate item reads all of them.
- Roll-up: an item's status from the statuses of the items it counts: the
  first of failed, waiting on a seat, blocked and doing that any of them
  reads; else done when all read done; else doing when any reads done;
  else to do.
- Intake: the G0 step that derives a feature's contract from its
  document (`/sdlc intake`).
- Feature before intake: a feature whose document is at
  `docs/features/<id>.md` and whose contract is not yet at
  `specs/<id>/contract.yaml`.
- Closed feature: a feature whose contract is closed by `taskcontract
  progress done`.
- Revision: one numbered row of a feature document's revision table, the
  first table in the document: r1, r2 and on.
- Half: the request half of a feature document, which the PO seat signs,
  or its solution half, which the engineer seat signs.
- Signature: a revision row, in the form the new ADR fixes, by which a
  seat signs one half at one revision.
- Title line: a feature document's `# <id> - <title>` heading. Intake
  copies its title into the contract's `title`.
- Drift mark: the one mark a feature with a contract carries from its
  document's revision table: `no feature document`, `no "Ready:" row` or
  `stale: document rD, contract from rM`.
