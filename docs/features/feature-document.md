| Revision Date | Revised By | Changes Made |
| :-: | :-: | :-- |
| 2026-09-30 | user | r1: Created in kit session 65 through an interview with the user, one question at a time, in the format ADR 0029 ratified and ADRs 0033 to 0035 amended; typed by Claude on the user's word. The request half, in progress. PO seat: user; engineer seat: user |
| 2026-09-30 | user | r2: Measured: ADR 0033's checks before signing, on the request half, run by Claude on the user's word: no new term clashes with a ratified term; `check` and `tag` trip CL003, and the dictionary cedes both at intake; lang-check's contract rules find 174 in the text intake copies (143 unknown words, 97 distinct; 15 sentences over the cap; 12 check sentences that open on no verb; 4 on a pronoun), each left to intake's rewrite of the contract's wording; SC2.3's read of Existing behavior touched against its sources: all seven entries hold, and entry 7 gains its source, `taskcontract/tree.py` |
| 2026-09-30 | user | r3: The request half finished in kit session 65: Q1 to Q9, ADR 0033's checks before signing (r2), ready checks 1 to 8 read back with three fixes (SC4 one sentence; entry 7's source; intake's roster message quoted in full); typed by Claude on the user's word |
| 2026-09-30 | user | r4: Signed: request half. The PO seat signs r3; typed by Claude on the user's word |

# feature-document - The interview writes the ratified format, and intake holds its definition of done

`sdlc_development_kit` · seats: PO user, engineer user · contract:
`feature-document`, draft · PR: none · merge SHA: none

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
- No change to the contract schema. A check's id stays text at the head
  of its sketch line, and a unit still holds at most three sketches.
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
   non-goals and the checks (missing: both commands read only `specs/`,
   and a scratch script stands in on this machine only. Owner: this
   feature, in the solution half).
6. An ADR that amends ADR 0029 where this document does: the appendix
   names the contract's path, never a copy; ready check 6 asks each entry
   of Existing behavior touched to name where it was measured (SC2.3)
   (missing. Owner: this feature, at intake).
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
  checks Scope against the release unit's paths. It writes nothing under
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
  writes a `Parked:` row with its message, and no contract
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
- Q: Does the tree read a `Parked:` row as a text change? A: OPEN, for the
  engineer seat: today it would age the stamp and be the row a later
  `Signed:` row signs.
- Q: "Finding" in this document? A: Finding keeps its ratified meaning, an
  observation about the kit; this document says result and gap (Q9,
  decided 2026-09-30).
- Q: A stale derived block, or a new word? A: The ratified Stale is
  amended at intake to cover a derived block (Q9, decided 2026-09-30).

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
  its document's newest revision. A "Ready:", "Measured:" or "Signed:" row
  never counts.

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
