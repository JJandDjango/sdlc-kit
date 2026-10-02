| Revision Date | Revised By | Changes Made |
| :-: | :-: | :-- |
| 2026-09-30 | user | r1: Created in kit session 65 through an interview with the user, one question at a time, in the format ADR 0029 ratified and ADRs 0033 to 0035 amended; typed by Claude on the user's word. The request half, in progress. PO seat: user; engineer seat: user |
| 2026-09-30 | user | r2: Measured: ADR 0033's checks before signing, on the request half, run by Claude on the user's word: no new term clashes with a ratified term; `check` and `tag` trip CL003, and the dictionary cedes both at intake; lang-check's contract rules find 174 in the text intake copies (143 unknown words, 97 distinct; 15 sentences over the cap; 12 check sentences that open on no verb; 4 on a pronoun), each left to intake's rewrite of the contract's wording; SC2.3's read of Existing behavior touched against its sources: all seven entries hold, and entry 7 gains its source, `taskcontract/tree.py` |
| 2026-09-30 | user | r3: The request half finished in kit session 65: Q1 to Q9, ADR 0033's checks before signing (r2), ready checks 1 to 8 read back with three fixes (SC4 one sentence; entry 7's source; intake's roster message quoted in full); typed by Claude on the user's word |
| 2026-09-30 | user | r4: Signed: request half. The PO seat signs r3; typed by Claude on the user's word |
| 2026-09-30 | user | r5: The request half amended in kit session 66 at the engineer seat's Q10: the schema non-goal names where a check's id sits, at the end of its sketch line in parentheses (`taskcontract/tree.py:175`); SC4.2 and Stale name a `Parked:` row as one that changes no text, which answers the OPEN on it; typed by Claude on the user's word |
| 2026-09-30 | user | r6: Signed: request half. The PO seat signs r5; typed by Claude on the user's word |
| 2026-09-30 | user | r7: Measured: ADR 0033's checks before signing, on the solution half and on the request half's amendments (SC2.1, prerequisite 5), run by Claude on the user's word: Scope holds the release unit's paths, `CHANGELOG.md`, `decisions/`, `docs/` and `MAP.md` are free paths, and no out-of-scope path falls inside Scope; no new term clashes with a ratified term; `check` and `tag` still trip CL003; lang-check's contract rules find 177 in the request half's text (174 at r2), left to intake's rewrite, and 5 in the units' `done_means` (the unknown words asks, refuses, copies, describes and mark); ready check 11 finds three facts with no Sources row (the title line, the seats, the origin); 9, 12 and 13 pass, and `MAP.md:42` names the v1 interview, a retirement f5 lacks |
| 2026-09-30 | user | r8: The solution half finished in kit session 66 through Q10 to Q16: Scope, Out of scope, Interfaces with its examples and edges, Sources, Constraints, Units, Order, Risks and cost. The findings at r7 answered: three `done_means` rewritten with known words (zero findings after), three Sources rows added, f5 names `MAP.md:42`. The request half amended at Q12 and here: SC2.1 and prerequisite 5 gain each unit's `done_means`; prerequisite 6 gains the Gherkin's tag and the Units table's cells; typed by Claude on the user's word |
| 2026-09-30 | user | r9: Signed: request half. The PO seat signs r8; typed by Claude on the user's word |
| 2026-09-30 | user | r10: Signed: solution half. The engineer seat signs r8; typed by Claude on the user's word |
| 2026-09-30 | intake | r11: Ready: contract `feature-document` validates ready-green, derived from r8 in kit session 67; the PO seat (user) signed the request half at r8 (r9), the engineer seat (user) the solution half at r8 (r10); five units, f1 to f5, each confirmed by seat user; the 15 new terms ratified, Stale amended and ADR 0036 accepted at `fde018d`; f2 and f3 each hold four checks in three sketches, SC3.2 with SC3.3 and SC2.2 with SC2.3, since the schema caps a unit at three; each `done_means` copied word for word from Units; the language door reads zero after one rewrite of 72 findings; the standing line stays in the document only, since the dictionary cannot say it |
| 2026-10-01 | user | r12: The solution half amended in kit session 72, a re-intake during the build: Scope gains `skills/sdlc/SKILL.md` for its three lines that say intake writes only the contract and never touches `docs/` (found at f4's Two-Key); f5's Retirements cell names them, and one decision entry records it. No check, no `done_means` and no out-of-scope path changes; typed by Claude on the user's word |
| 2026-10-01 | user | r13: Signed: solution half. The engineer seat signs r12; typed by Claude on the user's word |
| 2026-10-01 | intake | r14: Ready: contract `feature-document` validates ready-green, derived from r12; the PO seat (user) signed the request half at r8 (r9), the engineer seat (user) the solution half at r12 (r13) |

# feature-document - The interview writes the ratified format, and intake holds its definition of done

`sdlc_development_kit` · seats: PO user, engineer user · contract:
`feature-document`, ready · PR: none · merge SHA: none

## Statement

`[PO seat · authored]`

As a PO or engineer seat at a consumer, I want the interview to write a
feature document in the ratified format and intake to hold its definition
of done, so that a document both seats signed becomes a ready-green
contract with no new question to either seat.

## Description

`[PO seat · authored]`

Today the kit ships the interview ADR 0028 built. It writes the template
ADR 0026 mapped: a Jira-key title, a Seats line, Requirements under "Not
in scope", Previously Defined, Business Requirements, Implementation,
Misc., and Gherkin asked for freehand. Five readiness rules check it, and
it lands at `REQUEST_{slug}_{date}.md` in the repo root. The format has
moved four times since:

- ADR 0029: eighteen sections, the seat boundary (the line), a tag under
  each heading, numbered revision rows, checks with ids, Gherkin derived
  from the checks, Terms, and ten ready checks.
- ADR 0033: Sources, Examples, Retirements, tests listed by check id, an
  order with its reason, the checks run before signing, and ready checks
  11 to 14.
- ADR 0034: a seat signs its half in a `Signed:` row.
- ADR 0035: the tree reads a document at `docs/features/<id>.md` from its
  first revision, title line included.

Three documents (project-tree, G1 and tree-first-level) were written to
this format by hand from two NOTES files, since the skill cannot write
it. Intake already copies the title line and writes the `Ready:` row. It
still reads the old Implementation section, never assigns a check to a
unit, and never parks on an OPEN question.

With this feature, the interview writes the ratified format at
`docs/features/<id>.md`. It asks the sections in order and has each seat
sign its half in a `Signed:` row. It runs the checks before each
signature and proposes one Gherkin scenario per check for the PO seat to
confirm. The readiness check runs the fourteen ready checks and the
stale-stamp rule, and still never blocks. Intake holds the definition of
done: the ready checks that only advise in the interview refuse ready at
intake, every check goes to exactly one unit, and a standing OPEN
question parks the document.

## Background

`[PO seat · authored]`

ADR 0026 made the feature document the raw request intake consumes, and
named four template changes. The interview ADR 0028 built shipped one of
them. In session 32 the user's seventeen-section work format was
reconciled with the kit's template into one format with a definition of
done (ADR 0029, `NOTES_feature-document_2026-09-18.md`). This feature's
first draft was typed by hand that session and then waited behind G0's
declaration and the tree. project-tree was the first document written to
the format, by hand. Its build still asked 12 content questions the
document could have settled, so ADR 0033 amended the solution half
(`NOTES_feature-document-amendment_2026-09-27.md`). ADRs 0034 and 0035
came with tree-first-level, which shows a document in the tree before
intake.

On 2026-09-29 the user put this feature ahead of G1's solution half, in
order to use the kit on another machine. The installed skill there asks
ADR 0026's questions. Until this feature ships, another machine runs the
interview by hand from the two NOTES files, with
`docs/features/tree-first-level.md` as the example. Measured on the kit at
`e833283` (0.17.0), 2026-09-30.

### Existing behavior touched

Each entry gets a regression check under Acceptance criteria.

1. The interview asks one question at a time, writes its state file after
   every step, and resumes at the step `next` names (`SKILL.md`,
   `flows/sections.md`).
2. It writes only the document and its state file. It never writes an
   existing path ("A document already exists at {path}. Name another
   path."), never writes under `specs/` and never runs intake
   (`SKILL.md`, O1, W2).
3. The readiness check marks gaps OPEN and never blocks. The user's word
   to write is final, whatever the count (R3).
4. A sixth success criterion draws a split proposal (Q4). A bug fix takes
   an incident reference and a regression scenario (O2). Material given at
   the start is confirmed section by section, and a conflict with a spoken
   answer is asked, never settled silently (O5).
5. The Google Docs form is shown on request and writes nothing (W4).
6. Intake stops before any contract without a ratified seat roster (I1).
   It copies the title line into `title` (I4), confirms every unit with
   its seats (I5), writes the `Ready:` row (I7), and parks on a blocked
   dependency (I8).
7. The tree shows a document at `docs/features/<id>.md` with no contract
   from its first revision. It reads the plain name from the title line,
   plus the newest revision and each half's latest `Signed:` row (ADR
   0035, `taskcontract/tree.py`).

## Success criteria

`[PO seat · authored]`

1. SC1: The interview writes a feature document in the ratified format at
   `docs/features/<id>.md`, and each seat signs its half in a `Signed:`
   row.
2. SC2: Before a seat signs its half, the interview runs the checks intake
   and the gates will run and that half's ready checks, and records every
   result in the document without blocking.
3. SC3: Each check gets one Gherkin scenario that the interview derives
   and the PO seat confirms.
4. SC4: Intake refuses ready while a ready check fails, a check sits in no
   unit or in two, or a unit delivers no check, and parks the document
   while an OPEN question stands.
5. SC5: A machine that installs kit 0.18.0 gets this interview, and USAGE
   describes it.

## Non-goals

`[PO seat · authored]`

- No new authorizations are added (the standing line).
- No new gate condition. The interview stays upstream of G0.
- No change to the contract schema. A check's id stays text at the end of
  its sketch line, in parentheses, and a unit still holds at most three
  sketches.
- No contract copy in the appendix where the kit runs. The contract at
  `specs/<id>/contract.yaml` stays the only copy, and the appendix names
  its path.
- No tool reads the document's sections. The tooling reads only what ADRs
  0034 and 0035 already read (the revision table and the title line), and
  the ready checks are asked, never parsed (ADRs 0029, 0033).
- No commit hook. Refusing a commit while a derived block is stale or an
  OPEN mark stands stays with wave B.
- No change to the seats (ADR 0025). Unit confirmation at intake stays,
  and the process approvals stay on the user's word.
- No migration. project-tree, G1 and tree-first-level stay as written,
  and the root REQUEST files stay untouched. Writing documents for the 15
  contracts without one stays with prerequisite 7.
- No Drive, Jira or .docx writes, and no domain modules. The Google Docs
  form stays the Markdown W4 shows, and `styled-rendering` stays its own
  request.

## Prerequisites

`[PO seat · authored]`

1. The format: ADR 0029 as ADRs 0033 to 0035 amended it, plus the two
   NOTES files (exist: on main at `e833283`).
2. The interview skill's four flows and its template, and intake's flow
   (exist: `skills/product-specification-interview/`,
   `skills/sdlc/flows/intake.md`, kit 0.17.0).
3. The tree reading a document before intake: its title line and
   `Signed:` rows (exists: kit 0.17.0).
4. The vocabulary and language checks over the kit's own files:
   `taskcontract vocab-check` and `lang-check` (exist: kit 0.17.0).
5. A way to run those checks on a draft outside `specs/`: the document's
   new terms as drafts, and a draft contract built from the statement, the
   non-goals, the checks and each unit's `done_means` (missing: both
   commands read only `specs/`, and a scratch script stands in on this
   machine only. Owner: this feature, in the solution half).
6. An ADR that amends ADR 0029 where this document does: the appendix
   names the contract's path, never a copy; ready check 6 asks each entry
   of Existing behavior touched to name where it was measured (SC2.3);
   the Gherkin is derived by the interview and tagged `[PO seat · derived
   from rN]`; the Units table carries a Done means cell, and `+` joins
   two checks that share a sketch (missing. Owner: this feature, at
   intake).
7. The PromptLang validator for the skill's prompt files (exists:
   `E:\foundations`, on this machine).
8. A person to sign each half (exists: the user, holding both seats).

## Acceptance criteria

`[PO seat · authored]`

### Checks

Three checks under SC1 to SC4, two under SC5. SC1.1, SC1.2, SC2.2, SC4.3
and SC1.3 carry the regression checks for Existing behavior touched:
entries 2, 5 and part of 4 in SC1.1; 1 and the rest of 4 in SC1.2; 3 in
SC2.2; 6 in SC4.3; 7 in SC1.3.

SC1 The interview writes the ratified format

- SC1.1: verify a document the interview writes lands at
  `docs/features/<id>.md` with its title line `# <id> - <title>`, the
  ratified sections in order with the line between the halves, a tag
  under every heading, and numbered revision rows whose r1 names both
  seats. The bug-fix sections appear only for a bug fix, with its incident
  reference and regression scenario. The interview writes only the
  document and its state file and never runs intake. An existing path is
  still refused with its message, and the Google Docs form, shown on
  request, writes nothing
- SC1.2: verify the interview asks the sections in the ratified order,
  one question at a time, writes its state file after every step, and a
  later run resumes at the step `next` names. It asks the sorting question
  at Non-goals and Out of scope ("a thing we will not build, or a place we
  will not touch?"), proposes a split at a sixth success criterion with
  its message, and confirms given material section by section, asking
  about any conflict with a spoken answer
- SC1.3: verify a seat's signature lands as a row that opens `rN: Signed:
  request half` or `rN: Signed: solution half`, written right after the
  row it signs, and the tree then shows the document as a feature before
  intake with its plain name, its newest revision and each signed half

SC2 The checks run before signing

- SC2.1: verify that before the PO seat signs, the interview runs the
  document's new terms as drafts through the vocabulary check and CL003,
  and runs a draft contract of the statement, the non-goals and the
  checks through the language check. Before the engineer seat signs, it
  runs each unit's `done_means` through the language check and checks
  Scope against the release unit's paths. It writes nothing under
  `specs/`, and records each run as a `Measured:` row
- SC2.2: verify each ready check that misses (1 to 8 for the request
  half, 11 to 14 for the solution half) marks an OPEN with its message,
  and a derived block stamped older than the newest row that changed text
  is marked stale with its message. The interview never blocks: the
  seat's word to sign or write stands, whatever the count
- SC2.3: verify each entry of Existing behavior touched names the file or
  step it was measured from. The checks before the PO seat signs read each
  entry against that source, and an entry that no longer holds marks an
  OPEN under ready check 6

SC3 The Gherkin is derived and confirmed

- SC3.1: verify that once the checks are captured, the interview proposes
  one Gherkin scenario per check, joined to it by its id, and asks the PO
  seat to accept, edit or drop each one
- SC3.2: verify a proposed scenario whose Then carries a fact its check
  lacks is never offered. The check is marked thin instead, and ready
  check 3 reads that as an OPEN
- SC3.3: verify a check with no confirmed scenario when the PO seat signs
  marks an OPEN, and a scenario the PO seat drops marks its check thin

SC4 Intake holds the definition of done

- SC4.1: verify intake refuses ready while a check is assigned to no unit
  or to two, or a unit delivers no check, naming the id with its message,
  and parks the document. A unit that delivers more than three checks
  pairs two in one sketch that names both ids
- SC4.2: verify intake parks the document while an OPEN mark stands above
  the line or in Decisions and open questions, or a ready check fails. It
  writes a `Parked:` row with its message, a row that changes no text,
  and no contract
- SC4.3: verify intake copies each unit's `done_means` word for word from
  its line under Units, and its `Ready:` row names both seats and the
  revision each signed. It still stops without a ratified seat roster,
  copies the title line into `title`, confirms each unit with its seats,
  and parks on a blocked dependency

SC5 Kit 0.18.0 carries the interview

- SC5.1: verify installing the kit at the `v0.18.0` tag as USAGE says,
  through the plugin and through `uv`, gives this release's interview and
  intake flow, and the kit version reads 0.18.0
- SC5.2: verify USAGE's interview section describes the format, the
  checks before signing, the signatures, the Gherkin step and intake's
  refusals, with every mark green, and the CHANGELOG names the release

### Error messages, verbatim

Six new messages:

1. `Check {id} is assigned to no unit.` (SC4.1)
2. `Check {id} is assigned to units {a} and {b}.` (SC4.1)
3. `Unit {id} delivers no check.` (SC4.1)
4. `r{n}: Parked: {what stands}`, where `{what stands}` is the OPEN
   question, message 1, 2 or 3, or message 5 (SC4.1, SC4.2)
5. `Ready check {n}: {gap}. Marked OPEN.` (SC2.2, SC2.3, SC3.3)
6. `{block} is stamped r{n}; the newest revision is r{m}. Stale.` (SC2.2)

Kept word for word: "A document already exists at {path}. Name another
path."; "Six criteria is two features. Which criteria form the second
document?"; and intake's "No ratified seat roster. Author and ratify
specs/vocabulary/intake-seat.yaml (`/sdlc vocab add intake-seat` drafts
it), then run intake again."

---

## Proposed solution

`[Engineer seat · authored]`

### Scope

- `skills/product-specification-interview/`: the skill, its flows and its
  template (SC1 to SC3)
- `skills/sdlc/flows/intake.md`: intake's refusals and its word-for-word
  `done_means` (SC4)
- `skills/sdlc/SKILL.md`: its three lines on what intake writes, which
  f5's sweep makes true (SC4)
- `taskcontract/lang.py`, `taskcontract/__main__.py`: prerequisite 5's
  command, which runs the checks on a draft and writes nothing
- `taskcontract/tree.py`: a `Parked:` row changes no text
- `tests/`
- `USAGE.md`
- The release unit's: `pyproject.toml`, `skills/sdlc/init.py`
  (`KIT_VERSION`), `.github/workflows/sdlc.yml`

At intake, outside the build: prerequisite 6's ADR, and the 15 terms with
Stale's amendment, the dictionary ceding `check` and `tag`.
`CHANGELOG.md`, `decisions/` and `docs/` are free paths.

### Out of scope

- `taskcontract/checker.py`: the validator's rules and G0's readings (no
  new gate condition)
- `taskcontract/schemas/task-contract.schema.json`: the contract's schema
- `taskcontract/data/gates.yaml`: the gates and their conditions
- `skills/sdlc/flows/vocab.md`: how a term is drafted and ratified
- `skills/sdlc/templates/hooks-protect-specs.py.template`: the session
  hook (no commit hook; wave B)

### Interfaces

One new flag, `lang-check --draft`; one new rule, `CL014`; the state file
moves beside the document; the document gains its Gherkin block. Each
output is drawn on a feature `x`, PO seat ann, engineer seat raj.

The command (prerequisite 5) reads the interview's state file, never the
document, and writes nothing. It adds the state file's new terms to the
glossary as drafts, reports a new term that matches a ratified one
(`CL014`), reports the dictionary's health with the drafts (`CL003` and
the rest), and runs the contract rules on a draft contract of the
statement, the non-goals, the checks and each unit's `done_means`. Its
last line counts what it read and found:

```
$ python -m taskcontract lang-check --draft docs/features/x.state.yaml
specs/vocabulary/dictionary.yaml: $.words[41].word: CL003 'check' collides with a glossary term name, alias, or slug - the glossary is the open class; keep the layers disjoint
docs/features/x.state.yaml: answers.statement: CL008 sentence of 41 words exceeds the descriptive cap of 25
docs/features/x.state.yaml: answers.checks[SC2.1]: CL012 acceptance sketch must open with an approved verb (got 'each')
docs/features/x.state.yaml: answers.terms[Seat]: CL014 new term 'seat' matches ratified term 'intake-seat' - map it to that term, or rename it
draft: 14 new terms, 1 amended; 9 non-goals; 14 checks; 0 units; 4 findings (CL003 1, CL008 1, CL012 1, CL014 1)
```

Exit 1 when any finding is an error, as `lang-check` today; the interview
reads the lines either way and never blocks. Edges:

- Without `--draft`, `lang-check` reads `specs/` as today.
- A state file missing or not YAML: `docs/features/x.state.yaml: $: CL000
  unreadable draft: {reason}`, exit 1.
- No repo dictionary: only `CL014` runs, and the last line ends `(no
  dictionary here - door at rest)`.
- A key the state file lacks reads as empty: `draft: 0 new terms, 0
  amended; 0 non-goals; 0 checks; 0 units; 0 findings`.
- An amended term replaces its ratified definition among the drafts and
  is never a `CL014`.

The state file sits beside the document at `docs/features/<id>.state.yaml`.
The keys the command reads, drawn:

```yaml
schema: spec-interview-state/2
id: x
phase: request        # opening, request, solution, complete
next: Q8
seats: {po: ann, engineer: raj}
answers:
  statement: As a PO seat, I want ..., so that ...
  non_goals:
    - No new authorizations are added (the standing line).
  checks:
    - {id: SC1.1, text: verify ...}
  terms:
    - {name: Check, definition: one testable line under a success criterion ...}
    - {name: Stale, amends: stale, definition: a feature whose document ...}
  units: []           # at Units: {id, checks, done_means} per row
open: []
history: []
```

The other sections' answers sit under `answers` by section. A state file
at the old `REQUEST_{slug}_*.state.yaml` path is never read: a run for
that id starts fresh.

The document is written at the end of the opening, as r1, and each
section is written into it as its step closes, so the tree shows it from
its first revision. Its first lines:

```
| Revision Date | Revised By | Changes Made |
| :-: | :-: | :-- |
| 2026-10-01 | ann | r1: Created through /sdlc:product-specification-interview. The request half, in progress. PO seat: ann; engineer seat: raj |

# x - The outcome, in a few words

`repo` · seats: PO ann, engineer raj · contract: `x`, draft · PR: none · merge SHA: none
```

Then ADR 0029's eighteen sections in order, as ADR 0033 amended them,
each heading followed by its tag; the four bug-fix sections appear only
for a bug fix. The Gherkin, one scenario per check, joined by its id:

```
### Gherkin

`[PO seat · derived from r3]`

Scenario: SC1.1 A written document lands at its path
  Given a run for the id `x`, with no file at `docs/features/x.md`
  When the interview writes the document
  Then `docs/features/x.md` opens on its revision table, and its title line reads `# x - The outcome, in a few words`
```

A mark, inline in its section:

```
- SC2.1: verify ...
  OPEN: Ready check 3: SC2.1 is thin: its Then needs the count it reports.
```

The rows the interview and intake write, in one table's order:

```
| 2026-10-01 | ann | r2: Measured: the checks before signing, on the request half: 4 findings (CL003 1, CL008 1, CL012 1, CL014 1); ready checks 1 to 8: 1 OPEN |
| 2026-10-01 | ann | r3: The request half finished: ... |
| 2026-10-01 | ann | r4: Signed: request half. The PO seat signs r3 |
| 2026-10-02 | raj | r5: Measured: the checks before signing, on the solution half: ... |
| 2026-10-02 | raj | r6: The solution half finished: ... |
| 2026-10-02 | raj | r7: Signed: solution half. The engineer seat signs r6 |
| 2026-10-03 | intake | r8: Parked: Check SC2.3 is assigned to no unit. |
| 2026-10-03 | raj | r9: SC2.3 goes to unit u2 |
| 2026-10-03 | raj | r10: Signed: solution half. The engineer seat signs r9 |
| 2026-10-03 | intake | r11: Ready: contract `x` validates ready-green, derived from r9; the PO seat (ann) signed the request half at r3 (r4), the engineer seat (raj) the solution half at r9 (r10) |
```

Edges:

- The id's path exists at the opening: "A document already exists at
  {path}. Name another path."
- A section changed by hand since the interview last wrote it: the
  interview shows the document's text beside its answer and asks which
  stands, as for given material; it never overwrites a hand edit
  silently.
- A section with nothing to say reads "(none)"; one a ready check needs
  carries its OPEN mark instead.
- A scenario the PO seat drops: its check carries `OPEN: Ready check 3:
  SC2.1 is thin: scenario dropped.`
- Before intake, the Contract block reads "(none: intake writes
  `specs/x/contract.yaml`)" with no stamp, and is never stale.
- The Google Docs form, on request, is shown and written nowhere.

### Sources

| Fact | Read from | When two disagree |
| :-- | :-- | :-- |
| A feature's id and its document's path | the id the seat confirms at the opening; the path is `docs/features/<id>.md` | the file name wins over the id in the title line, as the tree reads it (ADR 0035) |
| The title line | the seat's answer at the opening, written as `# <id> - <title>` | a hand edit goes to the seat, as for a section; the tree and intake read the document's line (ADR 0035) |
| The seats | the answers at the opening, in the state file's `seats`, written into r1 and the status line | the state file wins; a changed seat is a new answer and a text row |
| A feature or a bug fix | the answer at the opening, the state file's `origin` | none: it decides whether the four bug-fix sections appear |
| The ratified sections, their order and tags | the template, written from ADR 0029 as ADRs 0033 to 0035 and prerequisite 6's ADR amend it | the ADRs win: a template that disagrees is a bug |
| A section's text | the state file's answer, written into the document as its step closes | a hand edit found at resume goes to the seat, whose word decides; never silently |
| The step to resume at | the state file's `next` | the state file wins; the document never moves `next` |
| Given material | what the seat hands the interview at the opening | a spoken answer that conflicts is asked, never settled silently (O5) |
| The checks' results before signing | `lang-check --draft`'s lines on the state file | the command wins; the `Measured:` row copies its last line |
| The release unit's paths | the release unit's row under Units; the kit's are `pyproject.toml`, `skills/sdlc/init.py` (`KIT_VERSION`) and `.github/workflows/sdlc.yml` | the Units row wins; a document with no release unit skips the check and says so in its `Measured:` row |
| An entry of Existing behavior touched | the file or step the entry names | the source wins: an entry that no longer holds is an OPEN under ready check 6 |
| A ready check's result | the interview's reading of the document against the questions in ADRs 0029 and 0033 | asked, never parsed; a seat's answer closes the OPEN |
| A derived block's stamp | its tag's `derived from rN` | none |
| The newest revision | the highest `rN` of a row that opens on none of `Ready:`, `Measured:`, `Signed:` or `Parked:` | one rule, shared with the tree's drift mark and Stale |
| A scenario | the check it joins by id, and the PO seat's confirmation | the check wins: a scenario that needs a fact the check lacks is never offered, and the check is marked thin |
| A half's signature | the half's latest `Signed:` row; the signer from its `Revised By` cell; the revision is the newest text row above it | the latest row wins (ADR 0034) |
| A check's unit | the Checks cell of its row under Units, where `+` joins two that share a sketch | none: a check in no row or in two is intake's refusal (SC4.1) |
| A unit's `done_means` | its row's Done means cell under Units, word for word | the document wins over any wording intake would derive |
| An OPEN mark that parks | any `OPEN` above the line or in Decisions and open questions | Notes never carries one; below the line, an OPEN is its ready check failing, which parks too |
| The kit's version | `pyproject.toml`'s `version` and `KIT_VERSION` | they must agree; a release moves both (`skills/sdlc/init.py:48`) |
| What a machine installs | the `v0.18.0` tag, through the plugin and through `uv`, as USAGE's lines say | the tag wins over any branch |

### Constraints

1. Every prompt file the build touches (the skill's `SKILL.md`, its
   flows, and `skills/sdlc/flows/intake.md`) passes `python -m
   prompt_lang` (prerequisite 7), keeps the PromptLang tag set, and stays
   under the 12,000-character ceiling its structural suite pins
   (`tests/test_skill_interview.py:43`, `tests/test_intake_flow.py:16`).
   A flow that outgrows it splits into another flow file.
2. Every shell command a prompt file authors is one segment: no pipe,
   chain or redirect.
3. The skill stays prompt-only: its directory holds Markdown and the
   template, no code. Every check that needs code runs through
   `taskcontract`.
4. No tool reads a feature document's sections: `lang-check --draft`
   reads only the state file, and the tree only the revision table and
   the title line.
5. The interview writes only the document and its state file, and never
   a `Ready:` or `Parked:` row. Intake writes those, and never a `Signed:`
   row.
6. `lang-check` without `--draft` prints byte for byte what 0.17.0
   prints. The tree does too, except that it no longer counts a `Parked:`
   row as a text change.
7. No new dependency.

### Units

| Unit | Checks | Done means | Tests, by check id and kind | Retirements |
| :-- | :-- | :-- | :-- | :-- |
| `f1-format` | SC1.1 | The interview writes the ratified format at `docs/features/<id>.md` from r1, with its state file beside it. | automated | the template's ADR 0026 sections; the `REQUEST_{slug}_{date}.md` path and its root state file (`spec-interview-state/1`); `SKILL.md`'s "never edit an existing document"; `output.md`'s render at the end (W1 to W3); USAGE's old interview text, since this unit writes the new USAGE section first; the tests that pin them, found by test-retirer (seen: `TEMPLATE_SECTIONS`, `test_opening_writes_the_state_file_and_never_overwrites`, `test_output_writes_from_the_template_and_names_intake`) |
| `f2-sections` | SC1.2, SC3.1, SC3.2+SC3.3 | The interview writes each section in the ratified order, one question at a time, and derives one scenario per check. | one automated test per check | `flows/sections.md` (Q1 to Q12), replaced by one flow per half; the tests that pin it, found by test-retirer (seen: `FLOW_FILES`, `SECTION_STEPS`, `test_skill_file_set_is_exactly_the_ratified_set`) |
| `f3-signing` | SC1.3, SC2.1, SC2.2+SC2.3 | The interview runs the checks before each signature, marks each gap OPEN, and writes the `Signed:` row. | one automated test per check; for SC1.3 also a manual receipt: a live run on a small feature in a scratch worktree, both halves signed, `taskcontract tree` showing both halves done | `flows/readiness.md` and its five rules, replaced by ready checks 1 to 14 and the stale rule; `test_readiness_advises_and_never_blocks`, found by test-retirer; and f2's file-set test, which flips when `readiness.md` goes |
| `f4-intake` | SC4.1, SC4.2, SC4.3 | Intake rejects ready on an open gap or a check without one unit, and writes each `done_means` word for word. | one automated test per check; for SC4.1 also a manual receipt: intake on f3's document with one check left out of Units writes the `Parked:` row and no contract | I4 and I5 reading the Implementation section; `test_i4_and_i5_take_the_answers_from_an_implementation_section`; `_NOT_TEXT`'s "none of the three words" (docstring and tuple) |
| `f5-release` | SC5.1, SC5.2 | Kit 0.18.0 ships the interview, and USAGE shows it with all marks green. | SC5.1 a manual receipt after the tag: USAGE's `uv` line run with `python -P` reads 0.18.0, and the plugin at the tag holds the new flows; SC5.2 automated | `KIT_VERSION`, `pyproject.toml` and `sdlc.yml` move to 0.18.0; USAGE's marks go green; a `CHANGELOG.md` entry; `MAP.md:42`'s v1 interview row; `skills/sdlc/SKILL.md`'s three lines that say intake writes only the contract and never touches `docs/` |

### Order

`f1-format`, then `f2-sections`, then `f3-signing`, then `f4-intake`,
then `f5-release`. f1 lays down the template, the state file and the
dispatch that f2's and f3's flows write into, and writes USAGE's section
first. f2's flows hand each half to f3's checks and signature, and f3's
live run needs both halves asked. f4's receipt runs intake on f3's
document. f5 ships. No two units run side by side: f2 and f3 each change
the skill's file set, which the other's test pins, and f4 needs f3's
document.

## Risks and cost

`[Both seats · authored]`

Risks:

1. The interview finds a hand edit by reading, not by a hash, so a small
   one can slip, and the next write of that section overwrites it. A
   write touches only the section its step closes, so hand edits
   elsewhere survive.
2. Tests pin a prompt's text, never what a model does with it. The two
   manual receipts are the only proof of behavior, and a later model can
   drift from the flows unseen.
3. A ready check is asked, never parsed, so two runs can read it
   differently, and intake's refusal is as strict as its reading. The
   seats' signatures on named revisions stay the record (ADR 0029).
4. The 12,000-character ceiling may split a flow more than once; each
   split adds a file to the dispatch and to the structural suite's set.
5. The interview never picks up a document it did not start, because an
   existing path is refused. G1's solution half, and any hand-started
   document, is still written by hand from the two NOTES files.
6. Until prerequisite 6's ADR is accepted at intake, ADR 0029 and the
   template disagree on the appendix's contract and on ready check 6.

Cost: five units. `f1` to `f3` are prompt text with structural tests,
`f3` adds the command, and two manual receipts need a live run. Intake
takes one session, the build three to four.

Worth: another machine gets the interview in the ratified format instead
of a hand run from two NOTES files, and each later document (prerequisite
7's fifteen among them) costs one interview. G1's solution half waits for
it, by the user's order of 2026-09-29.

## Decisions and open questions

`[Both seats · authored]`

- Q: The feature's id and title? A: `feature-document`, the id the ADRs
  and `STATE.md` already use; the title states the outcome (Q1, decided
  2026-09-30).
- Q: Whose statement? A: Both seats': ADR 0033's ready checks 11 to 14
  serve the engineer seat, and the bar is no new question to either (Q2,
  decided 2026-09-30).
- Q: What check does a release unit deliver? A: SC5's, the install and
  USAGE outcome; ready check 9 needs no exception (Q5, decided
  2026-09-30).
- Q: A check can rest on a false premise about today's behavior. A: Each
  entry of Existing behavior touched names where it was measured, and the
  checks before signing read it again (SC2.3); ready check 6 grows, in
  prerequisite 6's ADR. The first draft's evidence: it kept a message,
  "Section {name} has no answer. Marked OPEN.", that no shipped flow
  prints (Q8, decided 2026-09-30).
- Q: Checks and sketches are not one to one under the three-sketch cap.
  A: The schema stays; a sketch may carry two check ids (a non-goal and
  SC4.1; Q6 and Q8, decided 2026-09-30).
- Q: A pasted appendix copy of the contract ages at once. A: No copy where
  the kit runs; the appendix names the contract's path (a non-goal and
  prerequisite 6; Q6, decided 2026-09-30).
- Q: A derived `done_means` can read broader than its line. A: Intake
  copies each unit's sentence word for word (SC4.3; Q8, decided
  2026-09-30).
- Q: Does a parked document get a contract? A: No: every intake refusal
  writes a `Parked:` row and no contract (SC4.1, SC4.2; Q8, decided
  2026-09-30).
- Q: Does the tree read a `Parked:` row as a text change? A: No: like
  `Ready:`, `Measured:` and `Signed:`, it changes no text, so it never
  ages a stamp, moves the revision, or is the row a later `Signed:` row
  signs. SC4.2 and Stale say so, and `taskcontract/tree.py`'s `_NOT_TEXT`
  gains it (Q10, decided 2026-09-30).
- Q: Where does a check's id sit in its sketch? A: At the end of the line,
  in parentheses, two joined with "+", where intake writes it
  (`taskcontract/tree.py:175`); the schema non-goal said the head, a false
  premise found at Q10 (decided 2026-09-30).
- Q: "Finding" in this document? A: Finding keeps its ratified meaning, an
  observation about the kit; this document says result and gap (Q9,
  decided 2026-09-30).
- Q: A stale derived block, or a new word? A: The ratified Stale is
  amended at intake to cover a derived block (Q9, decided 2026-09-30).
- Q: How does a tool run the checks on a draft without reading the
  document's sections? A: `lang-check --draft` reads the interview's
  state file, which holds the statement, the non-goals, the checks and
  the terms; a new term that matches a ratified one is `CL014` (Q11,
  decided 2026-09-30).
- Q: Where does the state file live? A: Beside the document, at
  `docs/features/<id>.state.yaml`, schema `spec-interview-state/2`; an
  old `REQUEST_*` state file is never read (Q11, decided 2026-09-30).
- Q: When does the document exist? A: From r1, written at the end of the
  opening, then section by section as each step closes. A hand edit is
  asked about, never overwritten silently; the interview finds it by
  reading, not by a hash, so a small one can slip (Q11, decided
  2026-09-30).
- Q: Where does the Gherkin live, and whose is it? A: In the Appendix,
  tagged `[PO seat · derived from rN]`; a thin or dropped check carries
  an inline OPEN (Q11, decided 2026-09-30).
- Q: Intake copies `done_means` word for word, and the language door runs
  on the contract; who checks its words? A: The checks before the
  engineer seat signs: SC2.1 and prerequisite 5 gain each unit's
  `done_means`, read from the state file's `answers.units`, so intake
  never has to ask. The PO seat signs these request-half amendments
  once, before the engineer seat signs (Q12, decided 2026-09-30).
- Q: Does `f1-format` split, since it adds behavior and retires some? A:
  No: its retirements are the prompt text it replaces and about five
  structural tests, not a body of behavior; tree-first-level's Q14
  reading (Q14, decided 2026-09-30).
- Q: What proves a prompt-only skill works? A: Its structural tests pin
  the text; two manual receipts pin the behavior: a live run through both
  signatures (SC1.3) and intake parking on it (SC4.1) (Q14, decided
  2026-09-30).
- Q: Can a `done_means` pass the language door word for word? A: Each is
  written plainly, and the checks before the engineer seat signs run
  them (Q14, decided 2026-09-30).
- Q: `skills/sdlc/SKILL.md` says intake writes only the contract and
  never touches `docs/`, while the flow writes `Ready:` and `Parked:`
  rows into the document, and the file sits outside Scope. A: It joins
  Scope for those three lines, and `f5-release` makes them true in its
  sweep. No check and no `done_means` changes (found at f4's Two-Key,
  decided 2026-10-01).

## Appendix

### Terms

`[PO seat · authored]`

Decided at the interview's Q9 (2026-09-30). Fifteen map to the kit's
ratified terms: Feature document, Feature, Feature before intake, Intake,
Half, Signature, Revision, Title line, Plain name, Tree, Consumer,
Dependency, Acceptance sketch (a unit's sketch), Seat (`intake-seat`, by
its alias) and Unit (`decomposition-unit`). Stale takes a new definition
at intake:

- Stale: a feature whose document holds a revision newer than the one its
  contract was derived from, or a derived block whose stamp is older than
  its document's newest revision. A "Ready:", "Measured:", "Signed:" or
  "Parked:" row never counts.

The rest become terms to ratify at intake.

- Success criterion: one outcome a test can decide, in one line, with an
  id such as SC1.
- Check: one testable line under a success criterion, with an id such as
  SC1.1. Intake stores it in a unit's acceptance sketch, at most two to a
  sketch.
- Ready check: one of the 14 questions a feature document answers before
  intake reads it ready (ADRs 0029 and 0033).
- Checks before signing: the vocabulary, language and Scope checks the
  interview runs on a draft before a seat signs its half (ADR 0033).
- Seat boundary: the line between the request half and the solution half.
- Tag: the line under a section's heading that names its owner and kind,
  such as `[PO seat · authored]`.
- Derived block: a block written from the document and never edited by
  hand, the Gherkin or the traceability record, stamped with its revision.
- Stamp: the revision a derived block was written from.
- Measured row: a revision row that opens `Measured:` and names what was
  looked at. It changes no text.
- Scenario: the one Gherkin scenario derived from a check, joined to it by
  the check's id.
- Thin check: a check a scenario cannot be derived from without a fact it
  lacks, or whose scenario the PO seat dropped.
- OPEN mark: a gap marked in the document with the word OPEN. One standing
  above the seat boundary or in Decisions and open questions parks the
  document at intake.
- Parked document: a feature document intake refused, with a `Parked:`
  row naming what stands, and no contract.
- State file: the interview's memory between runs, beside the document.
- Release unit: the unit that ships a kit version: its CHANGELOG entry,
  USAGE marks and version strings.
