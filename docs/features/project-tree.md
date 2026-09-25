| Revision Date | Revised By | Changes Made |
| :-: | :-: | :-- |
| 2026-09-24 | user | r1: Created in kit session 49 through an interview with the user, one question at a time, in the format ADR 0029 ratified (`NOTES_feature-document_2026-09-18.md`); typed by Claude on the user's word. The request half, in progress. PO seat: user; engineer seat: user |
| 2026-09-24 | user | r2: The request half finished in kit session 50: the terms (Q11), the format's checks 1 to 8 read back, six fixes, the section tags; typed by Claude on the user's word. Signed by the PO seat (user). The title question stays open for the engineer seat |
| 2026-09-24 | user | r3: The solution half written in kit session 50 through the interview's eight decisions, after a Textual spike in a herdr pane; the request half gains the missing-extra message (SC4.1), Ctrl-C as existing behavior 10 (SC4.3), prerequisite 9 (titles), a wider SC5.2 and the term Pane extra; typed by Claude on the user's word. Signed by the PO seat (user) for the request half and the engineer seat (user) for the solution half |

# project-tree - The exact state of every feature's work, in one tree

`sdlc_development_kit` · seats: PO user, engineer user · contract:
`project-tree`, draft · PR: none · merge SHA: none

## Statement

`[PO seat · authored]`

As a developer, I want to easily keep track of the exact state of work on
every feature being worked on (which gates and conditions it has passed,
which units and tasks are done, what is in flight, what is blocked or
waiting on me, and what its gates found), so I know at any moment
whether the work still matches its feature document.

## Description

`[PO seat · authored]`

The session plans I get as Archify documents are confusing to follow and
do not hold up well between sessions: they use abbreviations and
references I do not know off the top of my head. I always have to ask the
LLM where things are, and that concerns me: I might be committing code I
do not understand. On 2026-09-23 the tree pane (kit 0.15.0) replaced the
Archify plans, and it is not proving to be a useful source of information
for me right now: with no task in flight it shows `no current task`, then
`16 items: 14 to do, 2 done`.

This feature clears up the ambiguity with a tree I can easily read. At
each step it shows notes (which gates and conditions a feature has
passed, which units and tasks are done, what is in flight, what is
blocked or waiting on me, and what its gates found), its status (done,
doing or to do), and references to its documentation. Where an id
shows, its plain name stands beside it: `G0.2 vocabulary coverage`,
never `G0.2` alone.

## Background

`[PO seat · authored]`

The tree started as the user's sketch in engine session 10 (2026-09-21,
transcript `83087a60`, 15:57Z), verbatim:

> I want a way to follow along easier, potentially in a herdr pane, and
> thought that the entire flow of work throughout my entire project could
> be done via a tree. Each node has a name, a paragraph in brief summary,
> file references if needed, and connections to other nodes.
>
> ```
> spec
> - m0
> -- g0
> --- g0.1
> ---- Status: Completed
> ---- Findings: x, y, z
> --- g0.2
> ---- Status: Incomplete/Failed
> --- g0.3
> --- ...
> -- g1
> -- ...
> - m1
> - ...
> ```
>
> This would all be in either one large file (presumably JSON) that gets
> parsed by a utility script to only access what it needs to prevent
> filling up the context window unnecessarily, or a folder structure that
> contains small files in it as each node. A node like m0 or spec contains
> a reference to their respective documents on system, but smaller ones
> like gates that don't have a file do not. Gates could potentially get a
> file made for them but that may be unnecessary given their structure.

Kit 0.15.0 built the tree from `REQUEST_tree-view_2026-09-21.md`, typed
from this sketch, and the pane from `REQUEST_pane-view_2026-09-23.md`.
Neither was written through an interview. tree-view's r1 mapped each gate
to one verdict per contract and took the tree's depth to units, tasks and
checks; no candidate offered the gate conditions, so no strike kept or
removed them. A first request written from the sketch in session 49
(`REQUEST_gate-outline_2026-09-23.md`, r1, untracked) traced each element
against 0.15.0; this document replaces it. The trace:

| Sketch | Kit 0.15.0 |
| :-- | :-- |
| `spec` at the root | Not built: struck at tree-view r2; waits on `spec-doc-type` (ADR 0031) |
| `m0`, `m1` | Built as contracts, top-level in their own repository's tree; a milestone level was struck at pane-view r2 |
| `g0`, `g1` under each | Active gates only, one verdict each (`<contract>/G0`); G1 to G10 are inactive in the kit and the pilot |
| `g0.1` to `g0.3` | Not built, and never offered |
| `Status:` on a condition | Six statuses on every item but a finding, in brackets on its line; no condition item |
| `Findings:` on a condition | Findings stand once at the repository level under their gate (ADR 0031); one that names a condition files under its gate |
| Name, summary, file references, connections | Built: the id, the source's own text, `file:`, `doc:` and `page:`, typed links |
| One JSON file or a folder of small files | Ruled out: computed at each print, never stored (ADR 0031) |
| A utility that reads only what it needs | Built: `taskcontract tree <id>`, one item in at most seven lines |
| m0 and spec name their documents; gates have none | Built: a contract's `doc:`, a gate's kit page |
| Following along in a herdr pane | Built: `tree --follow` and the herdr hook |
| The whole outline at once | Not built: the pane folds all but the current path (tree-view SC2, kept at r2) |
| Not in the sketch: units, tasks, checks | Built: units and checks from the contract; the seven tasks per the pilot's finding `plan-granularity-one-node-one-task` |

Measured on the kit at `7c79ba3`, 2026-09-23: the whole tree holds 16
items at its first level (`gates/G0` and 15 contracts), 118 at its second
(15 G0 verdicts and 103 units) and 971 at its third (tasks and checks).
13 of the 15 contracts read `to do`: they predate the tree and carry no
progress records (ADR 0031). The kit holds no finding; the pilot's 16
name G0 (9), G0.2 (1), G3 (1), G4.6 (1) and none (4).

### Existing behavior touched

Each entry gets a regression check under Acceptance criteria.

1. `taskcontract tree` prints every item and exits 0; an unreadable
   source prints one line on stderr, and the rest of the tree still
   prints (SC1.3).
2. `taskcontract tree <id>` answers every id the tree prints, in at most
   seven lines (SC1.3).
3. The pane's waiting line, `waiting on a seat: {approval} for {unit}`,
   stays its first line, word for word: the herdr hook reads it (SC4.3).
4. The notify command runs once each time the current task arrives at an
   approval, never on a redraw, with the item's id in `SDLC_NODE`
   (SC3.3).
5. The pane redraws within two seconds of a change to a source file
   (SC4.3).
6. `taskcontract progress` stays the only writer, and every state it
   recorded reads as before (SC3.3).
7. Each contract's G0 verdict reads as the validator says: `done` at
   ready-green, `blocked` when draft-green with `TC003`, `to do` when
   draft-green otherwise, `failed` when draft-red (SC2.3).
8. `tree: pane: parts:` selects the parts an item's line prints after
   its id and plain name (SC1.1).
9. `tree: pane: fold:` sets whether a closed item's line names or counts
   what it holds (SC4.2).
10. Ctrl-C ends the pane and exits 0 (SC4.3).

## Success criteria

`[PO seat · authored]`

1. SC1: Every feature being worked on stands in one tree, and each item
   shows its plain name beside its id and a reference to the document it
   comes from.
2. SC2: Each feature shows its gates and their conditions, each with its
   status and what its rules found.
3. SC3: Each feature shows its units and tasks as done, doing or to do,
   and marks what is blocked or waiting on me.
4. SC4: The pane shows the whole tree as an outline, each feature opened
   down to its units, whether or not a task is in flight; I scroll it,
   move through it and open or close any item with the arrow keys or the
   mouse.
5. SC5: The tree shows when a feature's work no longer matches its
   feature document.

## Non-goals

`[PO seat · authored]`

- No new authorizations are added, and no new gate condition: the tree
  shows the conditions the kit defines and adds none (the standing line).
- No change to what any gate checks: a condition shows what its rules
  already report.
- No stored copy: the tree is computed from the kit's files at every
  print, so the sketch's JSON file stays ruled out.
- No edits through the tree: it only reads.
- No spec doc level, a list of features above the features, before
  `spec-doc-type` is built: the sketch's `spec` root.
- No tree across repositories: the pilot's features, M0 among them, show
  in the pilot's own tree.
- No herdr plugin inside the kit: herdr wraps the pane from outside.
- Not a replacement for STATE.md, which keeps the narrative.

## Prerequisites

`[PO seat · authored]`

1. The tree, its query face and its pane (exist: tree-view and pane-view,
   kit 0.15.0).
2. herdr passes keys and mouse clicks to a pane's program and keeps pane
   scrollback (exists: this session runs in herdr, and its default config
   says pane apps "can still receive mouse when they request it").
3. Each gate's conditions, named on its kit page (exist: `docs/gates/`);
   the rules behind G0's three conditions (exist, in prose on the G0
   page).
4. A structured list of each gate's conditions and the rules each owns
   (missing: the kit's gate list names gates only, and ADR 0029 keeps
   tooling off document headings; owner: this feature).
5. A contract names its feature document (missing: `derived-language`
   SC4 asks for it; until it lands, the tree finds a document by its id at
   `docs/features/<id>.md`; owner: `derived-language`).
6. The revision a contract was derived from (exists in the format: intake
   writes a "Ready:" row naming the signed revision, ADR 0029).
7. The kit's own features have documents where the tree finds them
   (missing: the kit keeps its requests untracked in its root, and this
   document is the first under `docs/features/`; owner: the kit session).
8. Progress records for the 13 contracts older than the tree, so SC3
   reads true for them (missing: one `progress done` each, carried in
   STATE.md; owner: the kit session).
9. A title in each of the 15 existing contracts, so SC1.1 reads true for
   them (missing: one `title` line each; owner: the kit session).

## Acceptance criteria

`[PO seat · authored]`

### Checks

Two or three checks under each success criterion. SC1.3, SC2.3, SC3.3 and
SC4.3 carry the regression checks for Existing behavior touched, and
SC1.1 and SC4.2 those for its entries 8 and 9.

SC1 One tree, plain names, document references

- SC1.1: verify every contract in the repository stands in the tree as a
  feature, and each item line opens on its id and its plain name, before
  the parts `tree: pane: parts:` selects
- SC1.2: verify each item's plain name and document reference come from
  its source (a gate's, a condition's and a task's from the kit's lists;
  a feature's title and its document; a unit's done-means and a check's
  sketch line with their contract file and line), shown for the item
  under the pane's cursor and by `taskcontract tree <id>`
- SC1.3: verify `taskcontract tree` still prints every item and exits 0,
  an unreadable source still costs one line on stderr, and `taskcontract
  tree <id>` still answers every id it prints in at most seven lines

SC2 Gates, conditions, what they found

- SC2.1: verify each feature shows its active gates and then the next
  gate in the kit's order, marked inactive, and each gate opens into its
  conditions in the kit's order, each with its own status from the rules
  that condition owns
- SC2.2: verify a condition that is not done lists what its rules found,
  one line per diagnostic in plain words, and a finding that names a
  condition stands under that condition at the repository level
- SC2.3: verify each contract's G0 verdict still reads as the validator
  says: done at ready-green, blocked when draft-green with TC003, to do
  when draft-green otherwise, failed when draft-red

SC3 Units, tasks, blocked and waiting

- SC3.1: verify each unit and each of its tasks shows done, doing or to
  do from the progress records, and a closed unit or contract reads done
- SC3.2: verify a blocked item names its reason and an approval waiting
  on me names its seat, both on the item's own line
- SC3.3: verify `taskcontract progress` stays the only writer, every
  state it recorded reads as before, and the notify command still runs
  once per arrival at an approval, with the item's id in `SDLC_NODE`,
  never on a redraw

SC4 The interactive outline

- SC4.1: verify the pane opens on the whole tree as an outline, each
  feature opened down to its units, whether or not a task is in flight,
  with the current task marked and in view, and that without the `pane`
  extra `--follow` prints the message under Error messages and exits 2
- SC4.2: verify Up and Down move the cursor, Right opens and Left closes
  the item under it, a click opens or closes the item it lands on, and
  the wheel scrolls; a closed item's line counts what it holds, or names
  what it holds under `fold: names`
- SC4.3: verify the waiting line stays the pane's first line, word for
  word, a redraw within two seconds of a source change keeps the cursor
  and every open and closed item as they were, and Ctrl-C still ends the
  pane with exit 0

SC5 Drift from the feature document

- SC5.1: verify a feature whose document holds a revision newer than the
  one its contract was derived from, other than intake's "Ready:" row or
  a "Measured:" row, reads stale, naming both revisions
- SC5.2: verify a feature whose document the tree cannot find, or whose
  document names no revision its contract was derived from, says so,
  rather than reading as matching

### Error messages, verbatim

One new message, from `taskcontract tree --follow` without the `pane`
extra, on stderr with exit 2 (SC4.1):

`taskcontract tree: --follow needs the pane extra - pip install 'sdlc-taskcontract[pane]'`

Every message the kit prints today stays word for word.

---

## Proposed solution

`[Engineer seat · authored]`

The print, the query face and the pane read one tree, so each change
below shows in all three. Four changes carry the success criteria.

1. The pane becomes an interactive outline (SC4). `taskcontract tree
   --follow` runs a Textual app (a Python terminal-UI library) whose Tree
   widget opens and closes items with the arrow keys and the mouse and
   scrolls with the wheel. A line under the tree shows the item under
   the cursor: its plain name and document reference (SC1.2). Textual
   ships as the optional `pane` extra, `pip install
   'sdlc-taskcontract[pane]'`, so the validator's own dependencies stay
   jsonschema and PyYAML and a consumer's CI installs nothing new.
   Without the extra, `--follow` prints one line naming the install
   command. The waiting line stays the pane's first line, the notify
   command runs as today, and a redraw keeps the cursor and every open
   and closed item (SC4.3). A spike on 2026-09-24 ran a Textual Tree in a
   herdr pane on Windows: the arrow keys, clicks and the wheel all
   arrived, and the waiting line held the first row.
2. Each feature shows its title (SC1). The contract gains an optional
   one-line `title` field, which intake copies from the document's title
   line; the tree reads the title from the contract, never from the
   document's heading (ADR 0029). A contract without one shows its id and
   `(no title)`.
3. Gates open into their conditions (SC2). `taskcontract/data/gates.yaml`
   lists each gate's conditions in page order, 57 in all, each an id and
   a plain name taken from its page's heading without "check" or "join".
   G0's conditions list the rules each owns: G0.1 TC000 to TC009 and
   TC013 to TC015, G0.2 TC010 to TC012 and TC017, G0.3 TC016 and TC018. A
   condition's status comes from its own rules, read as G0's verdict is
   read today, so the verdict is the roll-up of its conditions (existing
   behavior 7). A condition that is not done lists the validator's
   messages, one line each, without their codes; warnings stay out, as
   today. A test holds every code the validator emits to exactly one
   condition.
4. The tree reads each feature's revision table (SC5). The document at
   `docs/features/<id>.md` is opened for its revision table only. Its
   newest revision is the highest rN other than intake's "Ready:" row
   and "Measured:" rows; the revision its contract was derived from is
   the rM that the newest "Ready:" row names, in the shape `rN: Ready:
   ... derived from rM ...`. A newer revision reads stale, naming both; a
   missing document or a missing "Ready:" row says so. The contract
   records nothing new for this.

### Scope

- `taskcontract/tree.py`: conditions, rules, titles and the stale
  reading
- `taskcontract/tree_view.py`: the print and query lines, and the
  `--follow` entry with its missing-extra line
- `taskcontract/pane.py` (new): the Textual app, imported only when
  `--follow` runs
- `taskcontract/data/gates.yaml`: the 57 conditions and G0's rules
- `taskcontract/schemas/task-contract.schema.json`: the optional `title`
  field
- `pyproject.toml`: the `pane` extra; Textual joins the `test` extra
  too, so CI's install line stays as it is
- `skills/sdlc/flows/intake.md`: intake copies `title` and writes the
  "Ready:" row in its fixed shape
- `tests/` and `USAGE.md`

Free paths need no entry: the G0 page's field table, a new ADR and the
changelog sit under `docs/`, `decisions/` and `CHANGELOG.md`.

### Out of scope

- `taskcontract/checker.py` and `taskcontract/graph.py`: the rules
  themselves (no change to what any gate checks)
- `taskcontract/vocabulary.py`: the G0.2 and G0.3 joins
- `taskcontract/progress.py`: the only writer (existing behavior 6)
- `specs/`: no contract changes; the title and progress backfills
  (prerequisites 8 and 9) are the kit session's own work

### Interfaces

| Interface | Shape |
| :-- | :-- |
| `title` in the contract | Optional string, one line, not blank; schema 1.4.0 becomes 1.5.0 |
| `taskcontract/data/gates.yaml` | Each gate gains `conditions:`, a list of `id`, `name` and `rules`; `rules` is a list of codes, only on G0's three conditions |
| The "Ready:" row | Its changes cell reads `rN: Ready: ... derived from rM ...` |
| The `pane` extra | `pip install 'sdlc-taskcontract[pane]'`, Textual `>=8.2,<9` (the spike ran 8.2.8) |
| `--follow` without the extra | On stderr `taskcontract tree: --follow needs the pane extra - pip install 'sdlc-taskcontract[pane]'`, exit 2 |
| The pane's keys | Up and Down move, Right opens, Left closes, a click opens or closes, the wheel scrolls; Ctrl-C ends the pane with exit 0 |
| New marks on a feature's line | `stale: document rN, contract from rM`; `no feature document`; `no "Ready:" row` |
| A condition's diagnostics | The validator's messages, one line each, under the condition |
| A feature with no title | Its id and `(no title)` |

### Constraints

- Only `taskcontract/pane.py` imports Textual, and only when `--follow`
  runs; every other command needs jsonschema and PyYAML alone.
- Labels reach Textual as plain text, never markup, so a status like
  `[to do]` is not read as a style tag (the spike's finding).
- Each line the pane sends to stderr today (an unreadable source, a bad
  `tree: pane:` key, a failed notify command) shows word for word inside
  the pane, under the tree, since Textual owns the screen.
- The pane holds open and closed items in memory only and writes
  nothing.
- CI runs on Linux only, so each unit's local receipts run on Windows.

### Units

- `o1-conditions` delivers SC2.1, SC2.2 and SC2.3; files
  `taskcontract/data/gates.yaml`, `taskcontract/tree.py`, `USAGE.md`;
  tests in `tests/test_tree_conditions.py`. Done means: USAGE's
  project-tree page stands first, with every feature marked red; every
  gate lists its conditions in page order; each of G0's conditions takes
  its status and its diagnostics from its own rules; and a test holds
  every validator code to exactly one condition.
- `o2-titles` delivers SC1.1; files the contract schema,
  `taskcontract/tree.py`, `taskcontract/tree_view.py`,
  `skills/sdlc/flows/intake.md`; tests in `tests/test_tree_titles.py`.
  Done means: the contract takes an optional one-line `title`, intake
  copies it from the document's title line, and every item line opens on
  its id and its plain name, a feature without a title showing `(no
  title)`.
- `o3-stale` delivers SC5.1 and SC5.2; files `taskcontract/tree.py`,
  `skills/sdlc/flows/intake.md`; tests in `tests/test_tree_stale.py`.
  Done means: the tree reads each feature document's revision table,
  marks a feature stale when a revision is newer than the one its
  contract was derived from, naming both, says so when the document or
  its "Ready:" row is missing, and intake writes the "Ready:" row in its
  fixed shape.
- `o4-statuses` delivers SC3.1 and SC3.2; files `taskcontract/tree.py`,
  `taskcontract/tree_view.py`; tests amend the tree's existing tests.
  Done means: each unit and task shows done, doing or to do from the
  progress records, a closed unit or contract reads done, and a blocked
  item names its reason and an approval waiting on a seat names that
  seat, each on the item's own line.
- `o5-pane-outline` delivers SC4.1 and SC1.2; files
  `taskcontract/pane.py` (new), `taskcontract/tree_view.py`,
  `pyproject.toml`; tests in `tests/test_pane.py`, driven by Textual's
  headless test driver. Done means: with the `pane` extra, `taskcontract
  tree --follow` opens an outline of the whole tree, each feature opened
  down to its units and the current task marked and in view, with a line
  under the tree showing the plain name and document reference of the
  item under the cursor; without the extra it prints the install line
  and exits 2.
- `o6-pane-keys` delivers SC4.2, SC4.3 and SC3.3; files
  `taskcontract/pane.py`; tests in `tests/test_pane.py`. Done means: Up
  and Down move the cursor, Right opens and Left closes, a click opens or
  closes, the wheel scrolls, a redraw keeps the cursor and every open and
  closed item, the waiting line stays the first row, the notify command
  runs once per arrival at an approval, and Ctrl-C ends the pane with
  exit 0.
- `o7-release` delivers SC1.3; files `pyproject.toml`, `USAGE.md`,
  `CHANGELOG.md`, ADR 0032; tests amend `tests/test_tree_view.py`. Done
  means: kit 0.16.0 ships with USAGE's marks all green, its changelog
  entry and ADR 0032, and `taskcontract tree` still prints every item and
  exits 0, its query answering every id in at most seven lines.

### Sequencing

- `o1-conditions` first.
- `o2-titles`, `o3-stale` and `o4-statuses` after o1, in any order.
- `o5-pane-outline` after o2, o3 and o4.
- `o6-pane-keys` after o5.
- `o7-release` after o6.

## Risks and cost

`[Both seats · authored]`

Risks:

- Textual inside a herdr pane on Windows: retired by the 2026-09-24
  spike; the keys, clicks and the wheel arrived, and the waiting line
  held the first row.
- Textual's releases: it moves fast and has broken its API across major
  versions; the extra pins `>=8.2,<9`, so a major bump is a deliberate
  change.
- The redraw keeps state by item, and the tree has one known id
  collision (tree-view t1's carried advisory); o6 keys state by each
  item's path from the root, so a collision cannot merge two items.
- Hand-written revision tables: a row the tree cannot read is skipped,
  and a document with no readable "Ready:" row says so (SC5.2) rather
  than reading as matching.
- Partial truth until the backfills: the 15 existing features read `(no
  title)`, `no feature document` and `to do` until prerequisites 7 to 9
  land; the feature shows its worth first on project-tree itself.

Cost:

- Seven units: about three build sessions at sessions 45 to 47's pace,
  plus the intake session.
- About 3M subagent tokens (session 47, per unit: a drafter about 165K,
  a developer 50K to 105K, a Two-Key round 190K to 240K).
- About 22 new terms to ratify at intake (G0.2).
- Nine more packages, in the `pane` extra only.
- The 57 conditions in `gates.yaml` follow the gate pages by hand.

Worth: G1 and the pilot's M0 wait for a pane that follows their
conditions, so the gate program resumes only once this ships; the build
is worth its cost (decided 2026-09-24).

## Decisions and open questions

`[Both seats · authored]`

- Q: The feature's id? A: `project-tree`. `pane-view` is the closed
  0.15.0 contract, and reusing its id would re-derive that contract
  (decided 2026-09-24).
- Q: Where does the document live? A: `docs/features/project-tree.md`,
  tracked: the tree finds a feature document there, git keeps every
  revision, and `docs/` is a free path (decided 2026-09-24).
- Q: What are "notes" and "status updates"? A: The notes are the state
  facts at each step, as listed in the statement; a status update is
  knowing which parts are done, doing or to do (decided 2026-09-24).
- Q: Do ids show? A: Each id is paired with its plain name (decided
  2026-09-24).
- Q: How much of the tree does the pane show? A: All of it: each feature
  opened down to its units, scrolled and navigated with the arrow keys
  and the mouse, whose items open and close (SC4, decided 2026-09-24).
- Q: Which gates does a feature show? A: Its active gates, then the next
  one in the kit's order: the sketch's `-- g1` (SC2.1, decided
  2026-09-24).
- Q: Which keys? A: Up and Down move, Right opens, Left closes, a click
  toggles, the wheel scrolls (SC4.2, decided 2026-09-24).
- Q: Do `tree: pane: parts:` and `fold:` keep working? A: Yes (SC1.1,
  SC4.2, decided 2026-09-24).
- Q: What does "check" mean? A: An acceptance check only, a line such as
  SC1.1. What a condition runs is a rule, and what a rule reports is a
  diagnostic; the statement, the description, SC2, SC2.2 and a non-goal
  say so (Q11, decided 2026-09-24).
- Q: Which status words? A: The six the tree prints: to do, doing,
  done, failed, blocked, waiting on a seat. "In flight" stays the plain
  phrase for a task at doing; "not started" gives way to "to do", since
  a draft-green contract has started G0 without passing it (SC3, Q11,
  decided 2026-09-24).
- Q: Is a verdict its own line? A: No: it shows as its gate's status,
  and the gate under a feature opens into its conditions (SC2.1, Q11,
  decided 2026-09-24).
- Q: How does the pane read keys and the mouse? A: Textual's Tree
  widget, shipped as the optional `pane` extra; a spike in a herdr pane on
  Windows passed the keys, clicks and the wheel (solution, decided
  2026-09-24).
- Q: Where does a feature's title come from? A: An optional one-line
  `title` field in the contract, which intake copies from the document's
  title line; the tree reads the contract, never the heading (solution,
  decided 2026-09-24).
- Q: Where do the conditions and their rules live? A: In
  `taskcontract/data/gates.yaml`: every gate's conditions, and G0's rules
  per condition (solution, decided 2026-09-24).
- Q: Where do the stale revisions come from? A: The document's revision
  table: its newest revision, and the rM that its newest "Ready:" row
  names (solution, decided 2026-09-24).

## Appendix

### Terms

`[PO seat · authored]`

Decided at the interview's Q11 (2026-09-24): session 49's 19 drafts,
reworked in four decisions, and seven added; Pane extra joined at r3,
from the solution half. Five map to the kit's
ratified terms: Gate (`gate`), Verdict (`verdict`), Unit
(`decomposition-unit`), Check (`acceptance-sketch`) and Seat
(`intake-seat`, by its alias). The rest become terms to ratify at
intake. The ratified `verdict` calls the coded records a rule reports
"findings"; this document calls them diagnostics, so ratifying
Diagnostic aligns that sentence.

- Feature: a piece of work with its own feature document and contract; a
  top-level item of the tree.
- Feature document: the document a feature's contract is derived from,
  at `docs/features/<id>.md`.
- Tree: the repository's work as one outline, computed from the kit's
  files at every print.
- Pane: the terminal pane that shows the tree (`taskcontract tree
  --follow`), in herdr or any terminal.
- Pane extra: the optional install the interactive pane needs, `pip
  install 'sdlc-taskcontract[pane]'`.
- Outline: the tree drawn one item per line, each item indented under its
  parent.
- Item: one line of the tree with its own id: a feature, gate, condition,
  finding, unit, task or check.
- Gate: a pass/fail checkpoint between phases of the work, defined by the
  kit (G0 planning and intake, G1 requirements and spec, and on).
- Active gate: a gate the repository has turned on in
  `.sdlc/config.yaml`. The tree marks the next gate after the active ones
  as inactive (SC2.1).
- Condition: one named part of a gate, whose status comes from the rules
  it owns (G0.1 definition of ready, G0.2 vocabulary coverage, G0.3 unit
  confirmation).
- Rule: one test the kit's validator applies to a contract, with a code
  such as `TC003`. Each rule belongs to one condition.
- Diagnostic: one thing a rule reported, shown in plain words under its
  condition.
- Verdict: a feature's result at one gate, as the kit's validator reports
  it, shown as that gate's status: done, blocked, to do or failed
  (existing behavior 7).
- Finding: a recorded observation about the kit, filed under the gate or
  condition it names.
- Unit: one separately verified slice of a feature's work, from its
  contract.
- Task: one of the seven steps every unit follows, from approving its
  test list to its Two-Key pass.
- Approval: a task that waits on a seat's answer, such as approving a
  unit's test list or its commit.
- Check: one testable line under a success criterion, with an id such as
  SC1.1.
- Status: to do, doing or done, or failed, blocked or waiting on a seat.
  These are the six words the tree prints. A task at doing is in flight.
- Progress record: what `taskcontract progress` writes as a task starts,
  finishes or is blocked; unit and task statuses come from it.
- Plain name: the words beside an id that say what it is, without the id
  scheme.
- Document reference: the file an item comes from, and the line where it
  has one.
- Cursor: the item the arrow keys and the mouse act on.
- Stale: a feature whose document holds a revision newer than the one its
  contract was derived from, other than intake's "Ready:" row or a
  "Measured:" row.
- Seat: the human position a step waits on for an answer: PO or engineer.
- Waiting line: the pane's first line while a task waits on a seat; the
  herdr hook reads it.
- Notify command: the command the pane runs once each time the current
  task reaches an approval.
