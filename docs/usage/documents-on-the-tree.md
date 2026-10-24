### Gates roll up their features 🟢

🟢 A gate item at the first level reads the roll-up of the features'
verdicts at its gate, and each of its conditions reads the roll-up of
that condition across the same verdicts: each feature's own reading of
the condition ("Gates and their conditions", above). A verdict marked
`inactive` never counts. A closed feature's verdicts count as they read:
a close governs only its own feature's roll-up.

🟢 The roll-up takes the first of `failed`, `waiting on a seat`,
`blocked` and `doing` that any verdict reads. Otherwise it reads `done`
when every verdict reads `done`, `to do` when every verdict reads `to
do`, and `doing` when some read `done` and some `to do`. A gate or
condition that no verdict counts in reads `to do`, as it does in a
repository with no feature.

🟢 A gate item or condition that is not `done` names each feature
holding it back: each feature whose counted verdict, or whose reading of
that condition, is not `done`. Each prints as one line under the item,
`- ` then the message, in the tree's order of features, before the
item's conditions and findings:

```
{feature} holds {id} at {status}
```

🟢 `{feature}` is the feature's id, `{id}` the gate's or condition's own
id (`G0`, `G0.1`), and `{status}` what that verdict or condition reads.
The pane folds a closed gate item that names features as it folds a
condition, `(<n> diagnostics)`, and shows a `holds` line whole on the
cursor line.

🟢 A finding still stands once, under the condition or gate its `gate:`
field names, and shows its kind, never a status. It counts in no
roll-up, so a finding never changes what a gate or condition reads.

🟢 With two features, `apply-discount` at `to do` as in "Gates and their
conditions" and `ship-rates` `done` at G0:

```
gates/G0 Planning / Intake [doing]
  - apply-discount holds G0 at to do
  gates/G0/G0.1 Definition-of-ready [done]
  gates/G0/G0.2 Vocabulary coverage [doing]
    - apply-discount holds G0.2 at to do
  gates/G0/G0.3 Unit confirmation [done]
```

### Features before intake 🟢

🟢 Each `.md` file directly under `docs/features/` that has no
`specs/<id>/contract.yaml` shows as a feature at the first level: a
**feature before intake**, from its first revision on. A design
document, `<id>.design.md`, is the one exception ("A pair of
documents"). A document whose table holds no revision shows too. Its id
is the file's name without `.md`. The features with a contract keep the
order of `specs/`, and a feature before intake stands among them by its
id.

🟢 Its plain name is the words of its document's title line, the first
`# ` line, after the first ` - `. For a title line in the template's
form, `# <id> - <title>`, those are the words intake copies into the
contract's `title`. A document with no title line, a title line with no
words after a ` - `, or a document that cannot be read as text reads `(no
title)`. The tree reads such a document once per print, its first table
and its title line, and prints none of its other words.

🟢 It shows its verdicts as a feature with a contract does: its G0
verdict, then its next gate marked `inactive`, each opening into its
conditions. Its G0 verdict and those conditions read `to do` and name no
validator run, since there is no contract to validate. That verdict
counts in `gates/G0`'s roll-up, and `gates/G0` names the feature: `<id>
holds G0 at to do`.

🟢 `taskcontract tree <id>` prints a feature before intake's line, then
`doc: docs/features/<id>.md:1`; the cursor line shows the same
reference. Its verdicts name their `page:` and no `file:`, since no file
decides them.

🟢 Once intake writes `specs/<id>/contract.yaml`, the feature stays one
item: it shows its contract's verdicts, units and drift mark, and none of
the revision and halves below. Its plain name comes from the contract's
`title` from then on, never from its document.

### Revisions and halves 🟢

🟢 A feature before intake names its document's revision as a mark, `no
contract: document rN`. `rN` is the highest revision of a **text row**: a
row that counts and opens on none of `Ready:`, `Measured:`, `Signed:` or
`Parked:`. A document with no text row, or that cannot be read as text,
shows `no revision table` in its place.

🟢 After its verdicts come its two **halves**, one item each:

| Item | Id | Plain name |
|---|---|---|
| the request half | `<feature>/request` | Request half |
| the solution half | `<feature>/solution` | Solution half |

🟢 A seat signs its half with a revision row whose changes cell opens
`rN: Signed: request half` or `rN: Signed: solution half`, free words
after (ADR 0034). After `rN:` those words are fixed: case as shown, one
space between them, the half's name ending at a word's end. The row
changes no text: it signs the text row above it with the highest
revision, a tie going to the lower row. A signed half reads `done` and
names its signature as evidence, `by <signer> at rN`: the signer is the
row's `Revised By` cell, `rN` the row it signs. The half names its seat:
the PO seat signs the request half, the engineer seat the solution half.
When a half has more than one signature, the row with the highest
revision counts, a tie going to the lower row. A half with none reads `to
do`. A row is no signature when it takes any other form, names neither
half, has no text row above it, or has a blank `Revised By` cell, the
cell before the last, so a row of fewer than three cells signs nothing.

```
| 2026-09-28 | user | r4: Signed: request half. The PO seat signs r3 |
```

🟢 A feature before intake rolls up its verdicts, but not the inactive
one, and its halves: it reads `to do` until a seat signs a half, then
`doing`. A feature before intake with its request half signed and its
design document at r1 ("A pair of documents"):

```
apply-discount Apply one discount code per order [doing] no contract: document r3 design r1 doc: docs/features/apply-discount.md
  apply-discount/G0 Planning / Intake [to do]
    apply-discount/G0/G0.1 Definition-of-ready [to do]
    apply-discount/G0/G0.2 Vocabulary coverage [to do]
    apply-discount/G0/G0.3 Unit confirmation [to do]
  apply-discount/G1 Requirements / Spec [to do] inactive
    apply-discount/G1/G1.1 Spec/schema linting [to do]
    apply-discount/G1/G1.2 Model checking [to do]
    apply-discount/G1/G1.3 Criteria completeness + ambiguity review [to do]
  apply-discount/request Request half [done] by user at r3
  apply-discount/solution Solution half [to do]
```

🟢 `taskcontract tree <id>` prints a half's line, then its `file:`: the
line of the row whose signature counts, or line 1 when it has none. The
cursor line shows the same reference.

```
apply-discount/request Request half [done] by user at r3
file: docs/features/apply-discount.md:6
```

🟢 A `Signed:` row never ages a contract: the document's revision in
"Drift from the feature document" leaves out every row that opens
`Signed:`, a signature or not.

### A parked document 🟢

🟢 A `Parked:` row is no text row either: intake writes one in each
table when it parks a pair, and it never moves `rN`.

### A pair of documents 🟢

🟢 The tree shows a pair before intake as one feature.
`docs/features/<id>.design.md` is never a feature of its own, and a
design document with no requirements document beside it prints nothing.
The feature's line gains a second mark, the design document's newest
text revision, and the solution half reads its signature from the design
document. The feature's line and its two halves, with the verdicts
between them left out:

```
x The outcome, in a few words [doing] no contract: document r3 design r3 doc: docs/features/x.md
  x/request Request half [done] by ann at r3
  x/solution Solution half [done] by raj at r3

$ python -m taskcontract tree x/solution
x/solution Solution half [done] by raj at r3
file: docs/features/x.design.md:6
```

🟢 With no design document, a feature prints as kit 0.18.0 prints it:
one mark, and the solution half from the document's own `Signed:
solution half` row, else `[to do]`. Once a design document stands, its
table alone gives the solution half. A design document with no text row
shows the mark `design: no revision table`.

🟢 For a pair through intake, the drift mark reads each table against
that table's `Ready:` row. The design's mark reads `stale: design r5,
contract from r3`, after the requirements document's mark. A combined
document through intake prints byte for byte as before. Before intake
the tree shows no mark for a stale design: the interview and intake
report it.

### G1 as an active gate 🟢

> 🟢 **Shipped** (kit 0.20.0, contract `specs/g1-requirements-spec/`,
> [ADR 0038](../../decisions/0038-a-gate-refuses-a-task-and-g1-records-and-declarations-have-homes.md)).
> A repository that does not list `G1` under `active_gates` reads the
> subsections above as they read.

🟢 G1 is active for a feature when `active_gates` lists `G1` and the
`g1.exempt` list does not name the feature. Such a feature shows G1
active, with G2 as the inactive next gate. Each of G1's conditions takes
its status from its own rules (§4, "`/sdlc g1`: the G1 venue"), and the
G1 verdict is their roll-up:

```
  apply-discount/G1 Requirements / Spec [failed]
    apply-discount/G1/G1.1 Spec/schema linting [done]
    apply-discount/G1/G1.2 Model checking [failed]
      - G1.2: hard core ledger has no model
    apply-discount/G1/G1.3 Criteria completeness + ambiguity review [done] by po at r5, design r4
  apply-discount/G2 Design / Architecture [to do] inactive
```

🟢 A condition that is not `done` lists each diagnostic, and a diagnostic
prints its message whole, its `G1.2:` opening included. A signed review
shows its seat and each revision it names; on a feature with one
document it reads `by po at r5`. The repository's line names each
feature that holds G1:

```
gates/G1 Requirements / Spec [failed]
  - apply-discount holds G1 at failed
```

🟢 An exempt feature prints as today, byte for byte: G0, then G1 `[to do]
inactive`. A feature before intake that is not exempt shows G1 active
and `to do`. The tree stays derived at every print: G1's reading stores
nothing and runs no tool. The pane watches `.sdlc/g1`.

🟢 G1.3 shows its review when it reads `done` or `failed`: the seat, then
each revision the record names that reads as `r` and digits. A review
that does not count shows nothing, as an absent one does. A feature
before intake reads each G1 condition `to do`, whatever stands under
`.sdlc/g1/`. An exempt feature's G1 line keeps its `inactive` mark under
a list that holds a later gate.

🟢 While `active_gates` lists `G1`, the tree prints one problem line for
each G1 source it cannot read. Such a source counts as absent, as
`g1-check` reads it, and a declaration's line prints once a print. The
six forms, of which one print holds the first or the second and never
both:

```
taskcontract tree: unreadable g1.exempt: .sdlc/config.yaml (it is no list)
taskcontract tree: g1.exempt names no feature: old-feature
taskcontract tree: unreadable g1.schemas: .sdlc/config.yaml (entry 1 names no pin)
taskcontract tree: unreadable component declaration: specs/components.yaml (YAML error at line 3)
taskcontract tree: unreadable record: .sdlc/g1/apply-discount.yaml (not a mapping)
taskcontract tree: unreadable G1 reading: apply-discount/G1/G1.2 (TypeError: unhashable type: 'list')
```

🟢 The last form stands for a condition whose reading ended on an error
of the kit's own. The print goes on, and that condition reads `to do`:
nothing is proven, so nothing reads `done`.

🟢 An error outside one condition's reading leaves no G1 reading to
trust, so the gate stands where the condition's id stands:

```
taskcontract tree: unreadable G1 reading: G1 (RecursionError: maximum recursion depth exceeded)
```

🟢 The print still goes on, as with no G1 source read: no feature is
exempt, each G1 condition of each feature reads `to do`, and this line
is the print's last problem line and its only one for G1. An error whose
message cannot be made prints its class name alone.

🟢 A character the output's encoding cannot hold prints as its backslash
escape, in the whole print and in a query, as Python writes it to
standard error. Through a pipe on Windows a diagnostic that names the
section `価格` reads `\u4fa1\u683c`, and the print goes on.

🟢 With `G1` absent from `active_gates` the tree reads no G1 source and
prints none of these lines. The pane watches a schema, a pin, a model or
a model's configuration file only where it stands under a folder it
watches: `specs`, `docs/features`, `.sdlc/findings`, `.sdlc/progress` or
`.sdlc/g1`. After a change to one that stands elsewhere it shows G1.1 or
G1.2 as last read, until a file it watches changes.

🟢 **The refusal.** `progress start` on a task, and `progress done` on a
task, a unit or a contract, refuse while the feature's G1 is active and
not `done`. The line goes to stderr, and the call exits 2 and writes
nothing:

```
$ python -m taskcontract progress start apply-discount/u1-rate/approve-tests
u1-rate cannot start: G1 has not passed for apply-discount

$ python -m taskcontract progress done apply-discount
apply-discount cannot start: G1 has not passed for apply-discount
```

🟢 `block` and `run` stay open. A contract's close is refused with the
feature's id in the unit's place: a close would else mark every task
done with G1 not passed. An exempt feature is never refused.
