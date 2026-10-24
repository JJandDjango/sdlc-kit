## 4. Day 2 — the contract flow

### `/sdlc:product-specification-interview` — writing the feature document 🟢

> 🟢 **Shipped** (kit 0.19.0, [ADR 0029](../../decisions/0029-feature-document-format-and-done.md)
> as ADRs 0033 to 0037 amend it, contract `specs/document-split/`). Kit
> 0.18.0's interview wrote one combined document, both halves in one file
> at `docs/features/<id>.md`: `USAGE.md` at tag `v0.18.0` is its guide.

Intake consumes a feature document (§8): a pair, the requirements
document and the design document of one feature. This skill writes each
in its own run, one question at a time, and has one seat sign each. Run
it in the target repo with the feature's id:

```
/sdlc:product-specification-interview csv-export          the requirements run: starts or resumes
/sdlc:product-specification-interview csv-export design   the design run: starts or resumes
```

🟢 **The two documents.** A requirements run writes the requirements
document at `docs/features/<id>.md`, the path a combined document held,
and its state file beside it, `docs/features/<id>.state.yaml`. A design
run writes the design document at `docs/features/<id>.design.md`, and its
state file at `docs/features/<id>.design.state.yaml`. An id holds no dot,
so `<id>.design.md` is never another feature's document. Each run writes
r1 at the end of its opening and each section as its step closes, so the
tree shows the feature before intake from the requirements document's
first revision (§9, "Features before intake").

🟢 **The requirements document** holds the request half, and the PO seat
signs it. It opens on its revision table, its title line `# <id> -
<title>`, and a status line. Drawn on a feature `x`, PO seat ann:

```
| Revision Date | Revised By | Changes Made |
| :-: | :-: | :-- |
| 2026-10-07 | ann | r1: Created through /sdlc:product-specification-interview. The request half, in progress. PO seat: ann |

# x - The outcome, in a few words

`repo` · seat: PO ann · contract: `x`, draft · PR: none · merge SHA: none
```

🟢 Then come the request half's sections in order, Statement to
Acceptance criteria, each with its heading and its tag as kit 0.18.0
writes them: owner and kind, such as `[PO seat · authored]`. The four
bug-fix sections appear only in a bug fix's document, with its incident
reference and regression scenario. Decisions and open questions and
Notes follow, each tagged `[PO seat · authored]`, then the Appendix with
its Gherkin and Terms blocks. The document holds no Proposed solution, no
Risks and cost, no Traceability, no Contract block and no `---` line. A
section with nothing to say reads "(none)", and one the interview has not
asked yet reads "(not yet asked)". The Gherkin carries no stamp until its
step writes it: it reads "(none: the Gherkin step writes one scenario per
check)" under `[PO seat · derived]`.

🟢 **The design document** holds the solution half, and one engineer seat
signs it. It names the requirements revision it stands against. Drawn
for the same feature, engineer seat raj:

```
| Revision Date | Revised By | Changes Made |
| :-: | :-: | :-- |
| 2026-10-08 | raj | r1: Created through /sdlc:product-specification-interview. The design, in progress, against requirements r3. Engineer seat: raj |

# x - The outcome, in a few words

`repo` · seat: engineer raj · requirements: `docs/features/x.md` · contract: `x`, draft · PR: none · merge SHA: none
```

🟢 Then come Proposed solution with its seven sections (Scope, Out of
scope, Interfaces, Sources, Constraints, Units, Order), Risks and cost,
Consult cases, Decisions and open questions, Traceability (Links out,
Record), Notes, and the Appendix with its Contract block. Each authored
section is tagged `[Engineer seat · authored]`; Record and Contract keep
`[Intake · derived]`. The document holds no section tagged for the PO
seat. Before intake, the Contract block reads "(none: intake writes
`specs/<id>/contract.yaml`)", with no stamp. The Record reads "(none:
intake writes the record)" and keeps that line: kit 0.20.0 has no step
that writes the Record.

🟢 **The requirements run.** It asks for a PO seat and for no engineer
seat. It asks the request half's sections in order, then the Terms and
the Gherkin, one question at a time. It writes its state file after
every step, and a later run resumes at the step its `next` names.
Material you hand it at the opening is confirmed section by section, and
an answer that conflicts with it is asked, never settled silently. No
step asks Decisions and open questions or Notes: each holds the material
confirmed at the opening, else "(none)". At Non-goals it asks "a thing we
will not build, or a place we will not touch?": a thing stands as a
non-goal, and a place waits in the state file for the design run. A
sixth success criterion draws "Six criteria is two features. Which
criteria form the second document?". A section changed by hand since the
interview last wrote it is shown beside the answer, and you say which
stands.

🟢 **The Gherkin step.** Once the checks stand, the requirements run
proposes one scenario per check, joined to it by its id, and the PO seat
accepts, changes or drops each. The block is tagged `[PO seat · derived
from rN]`:

```
Scenario: SC1.1 A written document lands at its path
  Given a run for the id `x`, with no file at `docs/features/x.md`
  When the interview writes the document
  Then `docs/features/x.md` opens on its revision table, and its title line reads `# x - The outcome, in a few words`
```

🟢 A scenario whose Then needs a fact its check lacks is never offered:
the check is marked thin instead. A scenario the PO seat drops marks its
check thin too. Ready check 3 reads a thin check as an OPEN.

🟢 Each text row the requirements run writes moves the block's stamp to
that row, once every check changed since the last stamp has a confirmed
scenario again. A row written by hand moves no stamp, so the checks
before signing report the block stale.

🟢 The requirements run then runs the checks before the PO seat signs,
takes the signature, and ends by naming the design run as the next
command:

```
/sdlc:product-specification-interview <id> design
```

🟢 **The design run.** It reads the requirements document before it
writes anything, and stops with nothing written on:

```
No requirements document for x. Run the requirements interview first.
The requirements document is unsigned at r3. The PO seat signs before the design starts.
```

🟢 The first when no file stands at the path; the second when no
`Signed: request half` row signs the newest text revision, here r3. A
design run on a combined document stops too, with nothing written:
`docs/features/x.md is a combined document. Split it by hand, then run
the design interview.`

🟢 Then the design run asks for an engineer seat and for no PO seat. It
asks no origin and no title: it reads both from the requirements
document, with the check ids and the new terms. It reads the
requirements document and the requirements run's state file, and writes
neither. It asks the solution half's sections in order, then the four
cases, and resumes as a requirements run does. At Out of scope it shows
the engineer seat each place the PO seat refused at Non-goals. A thing
the engineer seat will not build goes under the design's Decisions and
open questions as `OPEN: a non-goal for the PO seat: {thing}`, and
nothing goes into the requirements document: the PO seat adds it through
a requirements run, and the engineer seat then closes the mark.

🟢 **Consult cases.** After Risks and cost the design run asks the
engineer seat the four cases, one at a time: the conditions under which
the seat asks another engineer before the PR. Each answer is yes or no,
and a yes takes two more answers, who was asked and what was decided:

```
## Consult cases

`[Engineer seat · authored]`

| Case | Answer | Who was asked | What was decided |
| :-- | :-: | :-- | :-- |
| 1. An ambiguity in the requirements | no | | |
| 2. More than one solution | yes | lee | the retry lives in the client, not the gateway |
| 3. A solution unconventional to the codebase | no | | |
| 4. A change to a public contract: routes, a gateway definition, events, a schema | no | | |
```

🟢 **The revision a design names.** A design names one requirements
revision: the `requirements r{m}` of its newest text row that names one.
r1 names it first. Every design run, at any step, reads the requirements
document's newest text revision. On a newer one it shows the revisions
between and asks:

```
The design names requirements r3; the requirements stand at r5.
  r4: A non-goal added: no export to CSV
  r5: SC2.1 reworded
Confirm the design against r4 and r5?
```

🟢 On yes the design takes a text row, and a signed design is asked for
its signature again:

```
| 2026-10-10 | raj | r5: Confirmed against requirements r5 |
| 2026-10-10 | raj | r6: Signed: solution half. The engineer seat signs r5 |
```

🟢 On no, nothing is written and the design is stale: it names a
requirements revision older than the requirements document's newest text
revision. The checks before the engineer seat signs report it, and intake
stops on it, with one message:

```
The design names requirements r3; the requirements stand at r5. Stale.
```

🟢 **The checks before signing.** Each seat's checks run on that seat's
own document and state file. Before the PO seat signs, the interview
runs the document's new terms as drafts through the vocabulary check and
`CL003`, and a draft contract of the statement, the non-goals and the
checks through the language check. It also reads each entry of Existing
behavior touched against the file or step the entry names. Before the
engineer seat signs, it runs each unit's `done_means` through the
language check, beside a copy of the requirements document's new terms,
and checks Scope against the release unit's paths. The runs go through
one command that reads a state file, never a document, and writes
nothing:

```
$ python -m taskcontract lang-check --draft docs/features/x.state.yaml
specs/vocabulary/dictionary.yaml: $.words[41].word: CL003 'check' collides with a glossary term name, alias, or slug - the glossary is the open class; keep the layers disjoint
docs/features/x.state.yaml: answers.statement: CL008 sentence of 41 words exceeds the descriptive cap of 25
docs/features/x.state.yaml: answers.checks[SC2.1]: CL012 acceptance sketch must open with an approved verb (got 'each')
docs/features/x.state.yaml: answers.terms[Seat]: CL014 new term 'seat' matches ratified term 'intake-seat' - map it to that term, or rename it
draft: 14 new terms, 1 amended; 9 non-goals; 14 checks; 0 units; 4 findings (CL003 1, CL008 1, CL012 1, CL014 1)

$ python -m taskcontract lang-check --draft docs/features/x.design.state.yaml
docs/features/x.design.state.yaml: answers.units[u2]: CL008 sentence of 31 words exceeds the descriptive cap of 25
draft: 2 new terms, 0 amended; 0 non-goals; 0 checks; 3 units; 1 findings (CL008 1)
```

🟢 `CL014` reports a new term that matches a ratified one; an amended
term replaces its ratified definition among the drafts and is never a
`CL014`. On the design's state file the command reports the copied
terms' findings again. The command exits 1 when any finding is an error,
as `lang-check` does. A state file missing or not YAML reads
`docs/features/x.state.yaml: $: CL000 unreadable draft: {reason}`, exit
1. With no repo dictionary only `CL014` runs, and the last line ends
`(no dictionary here - door at rest)`. A key the state file lacks reads
as empty. Without `--draft`, `lang-check` reads `specs/` as before.

🟢 Then the interview reads that document's ready checks, 1 to 8 for the
requirements document and 11 to 15 for the design document, and marks
each gap inline with its message:

```
- SC2.1: verify ...
  OPEN: Ready check 3: SC2.1 is thin: its Then needs the count it reports.
```

🟢 Ready check 15 asks whether each of the four cases has an answer, and
whether each yes names who was asked and what was decided. Its gaps,
each marked under Consult cases:

```
Ready check 15: case 2 has no answer. Marked OPEN.
Ready check 15: case 2 reads yes and names no one asked. Marked OPEN.
Ready check 15: case 2 reads yes and names no decision. Marked OPEN.
```

🟢 Each run of the checks then lands as one `Measured:` row in that
seat's document: the command's findings, the count of OPEN marks under
that document's ready checks, and for the design document the Scope
result. The interview reports each gap as `Ready check {n}: {gap}. Marked
OPEN.`, and a derived block stamped below the newest revision as `{block}
is stamped r{n}; the newest revision is r{m}. Stale.` The checks advise
and never block: the seat's word to sign or to write stands, whatever
the count.

🟢 **The signatures.** Each seat signs in its own document, with a row
that opens `rN: Signed: request half` or `rN: Signed: solution half`,
written right after the row it signs (ADR 0034). The tree then shows
that half `done`, by its signer at the revision signed (§9, "Revisions
and halves"). A design run changes no line of the requirements document.
The rows the interview and intake write, each numbered in its own table.
The requirements document's:

```
| 2026-10-07 | ann | r2: Measured: the checks before signing, on the request half: 4 findings (CL003 1, CL008 1, CL012 1, CL014 1); ready checks 1 to 8: 0 OPEN |
| 2026-10-07 | ann | r3: The request half finished: ... |
| 2026-10-07 | ann | r4: Signed: request half. The PO seat signs r3 |
| 2026-10-09 | intake | r5: Ready: contract `x` validates ready-green, derived from r3; the PO seat (ann) signed the request half at r3 (r4) |
```

🟢 The design document's:

```
| 2026-10-08 | raj | r2: Measured: the checks before signing, on the solution half: 1 findings (CL008 1); Scope against the release unit's paths: covered; ready checks 11 to 15: 0 OPEN |
| 2026-10-08 | raj | r3: The solution half finished: ... |
| 2026-10-08 | raj | r4: Signed: solution half. The engineer seat signs r3 |
| 2026-10-09 | intake | r5: Ready: contract `x` validates ready-green, derived from r3, against requirements r3; the engineer seat (raj) signed the solution half at r3 (r4) |
```

🟢 A write into a document after its seat signed adds a text row, and
the interview asks that seat to sign again, with a new `Signed:` row
right after it. The seat's word stands: a seat that declines keeps its
older signature, and the interview names the revision it covers. A
requirements run on a finished state reports its paths and the design
run's command, then offers the way back to a section.

🟢 **What it writes.** A run writes only its own document and its own
state file. It never writes under `specs/`, never writes a `Ready:` or
`Parked:` row, and never runs intake. A document at a run's path with no
state file of that run beside it gets "A document already exists at
{path}. Name another path." On request a run shows its own document, and
that one alone, as the Google Docs form, and writes that form nowhere. A
state file at the old `REQUEST_<slug>_*.state.yaml` path is never read: a
run for that id starts fresh.

🟢 **Intake takes the pair.** `/sdlc intake docs/features/<id>.md` takes
the requirements document's path and finds the design document beside
it. It stops, with nothing written, on a combined document and on a
missing design document:

```
docs/features/x.md is a combined document with no Ready: row. Intake reads a pair.
docs/features/x.md is a combined document through intake. Its contract stands.
No design document for x. Run the design interview first.
```

🟢 A combined document is one that holds a `## Proposed solution`
heading. The first message is for one with no `Ready:` row. The second
is for one with a `Ready:` row: it stays unchanged, and its contract
validates as before.

🟢 **Intake's refusals** are read on both documents. Intake refuses
ready while an OPEN mark stands in either document, a ready check has a
gap (1 to 8 on the requirements document, 11 to 15 on the design
document), a check of the requirements document stands in no unit or in
two of the design document's Units, or a unit delivers no check. It
names the id:

```
Check {id} is assigned to no unit.
Check {id} is assigned to units {a} and {b}.
Unit {id} delivers no check.
```

🟢 A refusal parks the pair: intake writes one row in each table,
`r{n}: Parked: {what stands}`, numbered in its own table, and no
contract. Both rows hold the same list, which names every thing that
stands, the requirements document's things first. A `Parked:` row
changes no text: like `Ready:`, `Measured:` and `Signed:` rows, it never
ages a stamp or the drift mark, never moves the newest revision, and is
never the row a `Signed:` row signs.

🟢 Intake reads the signatures only when nothing stands. It then stops
before any contract, writes no row, and reports each case that holds, in
this order:

```
The requirements document has no PO signature on r5.
The design document has no engineer signature on r5.
The design names requirements r3; the requirements stand at r5. Stale.
```

🟢 The seat signs, or confirms the design, through its own run, and
intake runs again.

🟢 On ready, intake writes one contract. It takes the title, the
statement, the non-goals, the checks and the terms from the requirements
document, and the scope, the units, the order and the tests from the
design document. It copies each unit's `done_means` word for word from
its row under Units, where `+` joins two checks that share a sketch, and
a unit of more than three checks pairs two in one sketch that names both
ids. It writes one `Ready:` row in each table, as drawn above: each
names its own seat and the revision that seat signed, and its `derived
from r{m}` names its own table's signed text revision. Intake still
stops without a ratified seat roster, confirms each unit with its seats,
and holds a contract with a `blocked` dependency at draft.

🟢 **Next step:** a requirements run ends by naming the design run, and a
design run ends by naming the command that consumes the pair:

```
/sdlc intake docs/features/<id>.md
```

🟢 Every prompt file of the skill passes `python -m prompt_lang` and stays
under 12,000 characters, and a structural test in the suite holds the
shape.
