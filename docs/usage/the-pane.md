### The pane's lines 🟢

🟢 The waiting line (`waiting on a seat: ...`, above) stands first while
the current task is an approval, word for word, since a multiplexer's
plugin may read it.

🟢 Each item line under another item opens on the **last segment of its
id** (`o7-release`, `approve-tests`), since the lines above give the
rest; a top-level item's line opens on its full id. Everything else keeps
full ids: `taskcontract tree` with or without an id, the waiting line,
every link and `SDLC_NODE`.

🟢 Two optional keys under `tree: pane:` in `.sdlc/config.yaml` choose
what the lines hold. The pane reads them at each render, so a change
shows within two seconds; the config template does not carry them.

```yaml
tree:
  pane:
    parts: [status, marks]
    fold: names
```

- 🟢 **`parts:`** lists what each item line shows after its id and plain
  name, from `status`, `marks`, `evidence`, `links`, `doc` and `summary`.
  The id and the plain name always show, and listing `id` changes
  nothing. The parts print in that fixed order whatever order the list
  gives, and `[]` shows the id and the plain name alone. Unset, each item
  line shows every part it has. The key leaves the waiting line, the
  cursor line and `taskcontract tree` unchanged.
- 🟢 **`fold: names`** makes each closed item's group name the items it
  holds in place of the counts: each item as `<id> [<status>]`, the id as
  its own line would show it, joined by `, ` in the tree's order.
  `fold: counts`, or no `fold:`, keeps the counts by status.

🟢 A bad key never stops the pane. A `parts:` that is not a list, or that
names anything but the seven parts, is ignored as a whole, so each item
line shows every part it has. A `fold:` other than `names` or `counts`
keeps the counts. Either shows one line inside the pane at each render,
as an unreadable source does. `{value}` is the first entry that names no part,
or the whole value when it is not a list, and for `fold:` the value, each
as YAML reads it, so `fold: yes` prints `True`:

```
taskcontract tree: pane parts ignored: {value} - give a list from id, status, marks, evidence, links, doc, summary
taskcontract tree: pane fold ignored: {value} - give names or counts
```

🟢 A `tree:` or `pane:` that is not a mapping reads as unset, as it does
for `notify:`.

### Gates and their conditions 🟢

🟢 Each gate opens into its **conditions**, the named parts its kit page
lists, in the page's order. `taskcontract/data/gates.yaml` lists every
gate's conditions, 57 in all, each an id and a plain name: the page's
heading without its date note and without a last word "check" or "join"
(`G0.1 Definition-of-ready`, `G0.2 Vocabulary coverage`, `G0.3 Unit
confirmation`).

🟢 Each feature shows its gates first: each gate in `active_gates`, then
the first gate after them in the kit's order, marked `inactive`, the gate
its work reaches next. With `active_gates: [G0]`, every contract shows `G0`,
then `G1` marked `inactive`. An inactive gate and its conditions read `to
do`, and never count toward the contract's status, so a closed contract
still reads `done`.

🟢 Under a contract, each of G0's conditions takes its status from the
rules it owns, read as the `G0` verdict is read: `failed` when one of its
rules fails the draft profile, `done` when none fails the ready profile,
`blocked` when `TC003` fails it, and `to do` otherwise. A feature before
intake's conditions read `to do` ("Features before intake"), and a gate
item's read the roll-up of the features' ("Gates roll up their
features").

| Condition | Its rules |
|---|---|
| G0.1 Definition-of-ready | TC000 to TC009, TC013 to TC015 |
| G0.2 Vocabulary coverage | TC010 to TC012, TC017, W001 |
| G0.3 Unit confirmation | TC016, TC018 |

🟢 Every code the validator emits belongs to exactly one condition. A
warning (`W001`) never changes a status and never shows. The `G0` verdict
still reads from the validator, as above, so it agrees with its
conditions: `failed` when one reads `failed`, else `blocked` when one reads
`blocked`, `done` when all three read `done`, and `to do` otherwise. A
contract the tree cannot read as a mapping, one it names on stderr as an
`unreadable contract`, reads `failed` at G0.1 and `to do` at G0.2 and
G0.3, since their joins read nothing from it. A feature's conditions at G2
to G10 read `to do`: the kit computes none of them yet. G1's conditions
read from its records where G1 is active for the feature ("G1 as an
active gate", below) and `to do` where it is inactive.

🟢 A condition that is not `done` lists what its rules report, one line
under it per diagnostic: `- `, then the validator's message without its
code. A message repeated word for word prints once. A `failed` condition
lists the draft profile's messages, any other the ready profile's. A
contract at draft-green with one draft term, before intake has written
its `Ready:` row:

```
apply-discount Apply one discount code per order [to do] no "Ready:" row doc: docs/features/apply-discount.md | Checkout applies one discount code per order.
  apply-discount/G0 Planning / Intake [to do] via python -m taskcontract validate specs/apply-discount/contract.yaml --profile ready at 1a2b3c4
    apply-discount/G0/G0.1 Definition-of-ready [done]
    apply-discount/G0/G0.2 Vocabulary coverage [to do]
      - entity 'discount-code' is not ratified (status: draft) - draft does not resolve; ratify the term or fork the vocabulary task
    apply-discount/G0/G0.3 Unit confirmation [done]
  apply-discount/G1 Requirements / Spec [to do] inactive
    apply-discount/G1/G1.1 Spec/schema linting [to do]
    apply-discount/G1/G1.2 Model checking [to do]
    apply-discount/G1/G1.3 Criteria completeness + ambiguity review [to do]
```

🟢 At the repository level each gate opens into its conditions too, and a
finding whose `gate:` names a condition stands once under that condition,
never under a feature. A finding that names the gate itself, or a
condition its gate does not list, stands under the gate, after its
conditions.

| Item | Id |
|---|---|
| a condition | `gates/<gate>/<condition>`, `<feature>/<gate>/<condition>` |
| a finding that names a condition | `gates/<gate>/<condition>/<finding>` |

🟢 `taskcontract tree <id>` prints a condition as it prints a gate: its
line, which carries its plain name, and the gate's `page:`. Its
diagnostics print with the whole tree.

### Plain names and titles 🟢

🟢 Each item line opens on its id and its **plain name**, the words that
say what it is, then the parts `tree: pane: parts:` selects: `G0.2
Vocabulary coverage`, never `G0.2` alone. `parts:` never leaves out the
plain name, as it never leaves out the id, so `[]` shows both.

| Item | Its plain name |
|---|---|
| a gate, a verdict | the gate's name in `taskcontract/data/gates.yaml` |
| a condition | its name in `taskcontract/data/gates.yaml` |
| a task | its name in `taskcontract/data/tasks.yaml` |
| a feature with a contract | its contract's `title`, else `(no title)` |
| a feature before intake | its document's title line, after the first ` - `, else `(no title)` |
| a half | `Request half` or `Solution half` |
| a unit | its `done_means` |
| a check | its sketch line |
| a finding | its `statement` |

🟢 A plain name follows the summary rule above: its ends stripped, each
line break read as one space. An item whose source gives no text, such as
`gates/none` or a unit without `done_means`, shows no plain name; only a
feature shows `(no title)` in its place. A unit's, a check's and a
finding's plain name is the text that closed their line in 0.15.0, now
after the id, so the `summary` part holds only a contract's `intent`, and
`taskcontract tree <id>` prints its `summary:` line only for a contract.
An excerpt:

```
apply-discount Apply one discount code per order [doing] doc: docs/features/apply-discount.md | Checkout applies one discount code per order.
  apply-discount/u1-code-field The checkout form validates a discount code before it applies it. [doing]
    apply-discount/u1-code-field/approve-tests Approve the test list [done] by user at 1a2b3c4
    apply-discount/u1-code-field/write-tests Write the tests [doing] current
```

🟢 Once a feature has a contract, its plain name is the contract's
`title`, an optional field of one line that holds more than blanks. The
contract schema moves from 1.4.0 to 1.5.0 for it, and a `title` that is
blank or holds a line break fails the draft profile with `TC002`, under
G0.1. The tree reads the `title` from the contract, never from the
document. Intake copies it from the feature document's title line,
`# <id> - <title>`: the words after `<id> - `, or the whole heading when
it opens on anything else. A contract without a `title`, as every contract
written before 0.16.0 is until one is added, shows `(no title)`.

🟢 The pane's item lines open the same way, on the last segment of the id
and then the plain name. The waiting line keeps the id alone.

🟢 The pane's cursor line and `taskcontract tree <id>` show each item's
plain name and document reference from its source: a feature's title and
its feature document; a half's name and the row of its counting
signature, else the document's line 1 ("Revisions and halves"); a unit's
`done_means` and a check's sketch line, each with its contract file and
line; a gate's, a condition's and a task's name and kit page.

### Drift from the feature document 🟢

🟢 For a feature with a contract, the tree opens its document at
`docs/features/<id>.md` for its revision table only: the first table in
the file. A row counts when its last cell, the changes made, opens on
`r<N>:`; the tree skips every other row. Two revisions come from the rows
that count:

- 🟢 The **document's revision** is the highest `rN` of a row that is
  none of a `Ready:` row (its cell opens `rN: Ready:`), a `Measured:` row
  (`rN: Measured:`), a `Signed:` row (`rN: Signed:`, a signature or
  not) or a `Parked:` row (`rN: Parked:`).
- 🟢 The **contract's revision** is the `rM` that the newest `Ready:` row
  names, the one with the highest `rN` among those whose cell holds
  `derived from rM`. Intake writes the row in that fixed shape, `rN:
  Ready: ... derived from rM ...`. When two such rows share that `rN`,
  the lower one in the table wins, and a row that names more than one
  `rM` gives its first.

🟢 The feature's line names what the tree finds, as a mark after its
status:

- 🟢 `stale: document rN, contract from rM` when the document's revision
  is higher than the contract's.
- 🟢 `no feature document` when there is no file at
  `docs/features/<id>.md`.
- 🟢 `no "Ready:" row` when the file holds no `Ready:` row that names its
  `rM`, or cannot be read as text.

🟢 With none of the three marks, the contract matches its document; a
contract's `rM` above the document's revision matches too. A
document whose table runs `r1`, `r2`, `r3: Ready: ... derived from r2`,
`r4`:

```
apply-discount Apply one discount code per order [doing] stale: document r4, contract from r2 doc: docs/features/apply-discount.md | Checkout applies one discount code per order.
```

🟢 The pane already lists `docs/features/`, so an edit to a document
shows within two seconds. The contract records nothing new for this.

🟢 When the request is a feature document at `docs/features/<id>.md`,
intake adds one row to each document's revision table once the contract
validates ready-green: the date, `intake`, and a changes cell that opens
``rN: Ready: contract `<id>` validates ready-green, derived from rM``,
with `rN` the next revision in that table and `rM` that table's signed
text revision.

### Blocked and waiting, named 🟢

🟢 Each unit and each task shows `done`, `doing` or `to do` from the
progress record, as "Six statuses" reads them. A closed unit reads `done`.
A closed contract reads `done`, whatever its verdicts read; each verdict
still shows the validator's reading on its own line.

🟢 A task blocked by its own record names its reason on its own line,
`because <reason>`, the `--reason` that `taskcontract progress block` took.
Only a task takes a `--reason`, so a unit or contract that reads `blocked`
through one of its tasks names none; the task does.

🟢 The approval that holds the current task reads `waiting on a seat` and
names the seats it waits on, `seat: <seats>`: its unit's `confirmed_by`,
the seats that answered for the unit at intake, joined by `, `. Nothing
else records a seat before the approval's answer. A unit without
`confirmed_by` names none. The waiting line keeps its words.

```
    apply-discount/u1-code-field/approve-commit Approve the commit [waiting on a seat] current seat: user
```

🟢 Both print as the line's evidence, so a `tree: pane: parts:` list
without `evidence` leaves them out.

### The interactive pane 🟢

🟢 With the `pane` extra, `taskcontract tree --follow` runs an interactive
outline of the whole tree. The extra installs Textual (`>=8.2,<9`), a
terminal-UI library; every other command still needs only jsonschema and
PyYAML.

```bash
pip install 'sdlc-taskcontract[pane]'
```

🟢 The pane holds, top to bottom: the waiting line, when the current task
is an approval; the outline; the lines the pane reports (below); and the
cursor line. 0.15.0's where-am-I line, fold lines and `no current task`
line give way to the outline.

🟢 The outline holds every line `taskcontract tree` prints, in its order:
each item, and each diagnostic under its condition or gate item. An
item's line opens as "The pane's lines" gives, a top-level item on its
full id and any other on the last segment of its id, then its plain name
and the parts `tree: pane: parts:` selects. Each line shows its text as
written, so `[to do]` reads as brackets, never as a style.

🟢 The pane opens with each feature open, so a contract shows its units
and a feature before intake its verdicts and halves, and every other item
closed, whether or not a task is in flight. A task in flight
also opens its own unit, so the current task shows. Its line carries
`current` whatever `parts:` selects, the cursor starts on it, and the
window scrolls to it. With no current task the cursor starts on the first
line.

🟢 A closed item's line shows what it holds, in parentheses after its
status: `(<n> items: <counts>)`, the items one level below it counted by
status in the order "Six statuses" gives, zeros left out, then each
finding by its kind, `<n> kind: <kind>`; or under `fold: names` each item
as `<id> [<status>]`, joined by `, `. A closed condition or gate item
counts its diagnostics, `(<n> diagnostics)`.

🟢 A plain name that would push the status, those parentheses and the
current task's `current` past the pane's right edge is cut where they
still fit, ending in `...`; the other parts after them are cut at the
edge. The cursor line shows the name whole.

🟢 This kit's own tree at o7's first approval, in a pane 57 columns wide
with the cursor on the current task; the waiting line wraps at this
width, and `...` rows stand for rows left out here:

```
waiting on a seat: approve-tests for
project-tree/o7-release
...
▼ project-tree (no title) [waiting on a seat] doc: docs/f
├── ▶ G0 Planning / Intake [done] (3 items: 3 done) via p
├── ▶ G1 Requirements / Spec [to do] (3 items: 3 to do) i
...
├── ▶ o6-pane-keys `Up` and... [done] (10 items: 10 done)
└── ▼ o7-release Kit `0.16.0` ship... [waiting on a seat]
    ├── approve-tests Appr... [waiting on a seat] current
USAGE.md | Approve the test list
```

🟢 The **cursor line** shows the item at the cursor: its document
reference, then ` | ` and its plain name, whole, wrapping onto as many
rows as it needs. The reference is the one `taskcontract tree <id>`
prints: a feature's `doc:`, or its `file:` when it has no feature
document; a unit's, a check's, a finding's and a half's `file:`; a
gate's, a verdict's, a condition's and a task's `page:`. An item with no plain name
shows its reference alone, and one with neither shows its id. On a
diagnostic, the cursor line shows the diagnostic whole.

```
specs/project-tree/contract.yaml:134 | With the pane extra, `taskcontract tree --follow` shows all of the tree as an outline, each feature open down to its units. ...
```

🟢 Up and Down move the cursor one line. Right opens the item at the
cursor and Left closes it; on an item that holds nothing, or is already
open or closed, they change nothing. A click opens or closes the item it
lands on and puts the cursor there. The wheel scrolls the window and
leaves the cursor where it is.

🟢 The pane lists its sources as "The three modes" gives and renders
again within two seconds of a change, never while nothing changes. A render
keeps the cursor on the same item and every item open or closed as it
was, each item known by its path from the root, so two items that share
an id never trade places. An item new to the tree opens as at the start.
When the item at the cursor is gone, the cursor moves to its nearest
parent that remains. When a render moves the current task to another
task, the pane opens the items above the new one and scrolls it into
view, as at the start; the cursor stays where it was.

🟢 The waiting line stays the pane's first line, word for word. The
notify command runs as "The notify command" gives, once per arrival at an
approval, never on a render, with the item's id in `SDLC_NODE`. Ctrl-C
ends the pane with exit 0.

🟢 Each problem line (an unreadable source, a bad `tree: pane:` key, a
failed notify command) shows word for word inside the pane, under the
outline, each whole. A render replaces the
lines the one before it reported, and a notify failure stays until the
next render. The pane writes nothing to stderr while it runs.

🟢 Without the extra, `--follow` prints one line on stderr and exits 2;
an id with `--follow` still gets its own line first:

```
taskcontract tree: --follow needs the pane extra - pip install 'sdlc-taskcontract[pane]'
```
