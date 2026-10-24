## 9. Following the work 🟢

> 🟢 **Shipped** (kit 0.15.0, [ADR 0031](../../decisions/0031-the-work-is-one-derived-tree.md),
> contracts `specs/tree-view/` and `specs/pane-view/`; kit 0.16.0,
> [ADR 0032](../../decisions/0032-plain-names-conditions-drift-and-an-outline.md),
> contract `specs/project-tree/`, "Gates and their conditions" to "The
> interactive pane"; kit 0.17.0,
> [ADR 0034](../../decisions/0034-a-seat-signs-its-half-in-a-revision-row.md) and
> [ADR 0035](../../decisions/0035-gates-roll-up-and-a-feature-shows-before-intake.md),
> contract `specs/tree-first-level/`, "Gates roll up their features" to
> "Revisions and halves"; kit 0.18.0,
> [ADR 0036](../../decisions/0036-the-appendix-names-the-contract-and-a-unit-row-holds-done.md),
> contract `specs/feature-document/`, "A parked document"; kit 0.19.0,
> [ADR 0037](../../decisions/0037-a-feature-document-is-a-pair-and-each-document-has-one-seat.md),
> contract `specs/document-split/`, "A pair of documents").

🟢 `taskcontract tree` prints the repo's work as one tree, computed from
the kit's files at every run and never stored. It reads the contracts,
`.sdlc/config.yaml`, the findings, the progress files, git, and two name
lists the kit ships (`taskcontract/data/gates.yaml` and
`taskcontract/data/tasks.yaml`). Of the documents, it reads only each
feature document's revision table ("Drift from the feature document",
below), and the title line of one with no contract ("Features before
intake"): nothing else under `docs/`, and no REQUEST, STATE or plan. It
writes no file; `taskcontract progress` is the only writer, and only under
`.sdlc/progress/`.

### What the tree holds 🟢

🟢 The gates come first, at the repository level: each gate in
`active_gates`, and any other gate a finding names, marked `inactive`.
Each finding under `.sdlc/findings/` prints once, under the gate its
`gate:` field names, or under that gate's condition when the field names
one ("Gates and their conditions", below); `gate: none` prints under a
`none` item, and the form's `TEMPLATE.yaml` prints nothing. A finding is
read only from a `.yaml` file, so a `.yml` file there never shows. Then
each feature: a contract, with its verdict at every gate in
`active_gates` and at the next gate, marked `inactive`, its units, each
unit's seven tasks, and its checks, one per `acceptance_sketch` line; or a
feature before intake, with its verdicts and its two halves ("Features
before intake", below).

🟢 Every item has an id, a path you pass to the commands below:

| Item | Id |
|---|---|
| a gate, a finding, the no-gate item | `gates/G0`, `gates/G0/<finding>`, `gates/none` |
| a feature, its verdict at a gate | `<feature>`, `<feature>/G0` |
| a half | `<feature>/request`, `<feature>/solution` |
| a unit | `<contract>/<unit>` |
| a task | `<contract>/<unit>/<task>`, with the keys in "The seven tasks" |
| a check | `<contract>/<unit>/<check>`: the ids in the sketch's trailing parentheses, joined with `+` (`SC5.1+SC5.2`), else `sketch-<n>`, counted from 1 |

🟢 An item's summary and its plain name ("Plain names and titles",
below) are its source's own text, with their ends stripped and each line
break read as one space. Only a contract has a summary, its `intent`. The
plain names are a contract's `title`, the words of a feature before
intake's title line after its first ` - `, a half's `Request half` or
`Solution half`, a unit's `done_means`, a check's sketch line, a finding's
`statement`, and a gate's, a condition's or a task's name from the kit's
lists. Links come only from source fields: a unit's `depends_on`, each
entry once in the order it first appears, and a finding's `gate`. A
feature document shows as a file reference, found by the feature's id at
`docs/features/<id>.md`.

🟢 Each item prints on one line, indented two spaces per level: its full
id, its plain name, then its status in brackets (a finding shows `[kind:
<kind>]` in its place), its marks (`inactive` on a gate that is not
active, `current` on the current task, a contract's drift mark, a feature
before intake's revision mark), its evidence, its links (`depends_on:
<contract>/<unit>`, `gate: <value>`), a feature's
`doc: docs/features/<id>.md`, and last ` | ` and its summary.
The plain name and each part after the status print only when the item
has them, and a line break inside a part, such as in a multi-line
`--reason`, reads as one space, so an item keeps one line.

### Six statuses 🟢

🟢 Every item but a finding shows one of six statuses: `to do`, `doing`,
`done`, `failed`, `blocked`, `waiting on a seat`. A finding records no
status, so it shows its `kind`.

- 🟢 A task reads the state `taskcontract progress` recorded for it; an
  approval that holds the current task reads `waiting on a seat`.
- 🟢 A check reads its last run, judged by what that run expected: never
  run, `to do`; red under `--expect red`, `doing`; green under the
  default, `--expect green`, `done`; a run that missed its expectation,
  `failed`. A test that passes before its code exists shows `failed`.
- 🟢 A contract's `G0` verdict comes from the validator: `done` at
  ready-green, `blocked` when draft-green with `TC003`, `to do` when
  draft-green otherwise, `failed` when draft-red.
- 🟢 A unit or a feature takes the first of `failed`, `waiting on a
  seat`, `blocked` and `doing` that any child has. It reads `done` only
  when every child reads `done`, and `to do` when nothing under it has
  started. Two children never count: a feature's inactive gate ("Gates
  and their conditions") and, once a contract is closed, its verdicts
  ("Blocked and waiting, named"). A feature before intake never reads
  `done` ("Revisions and halves"). A gate item and its conditions read the
  roll-up of the features' verdicts instead ("Gates roll up their
  features").

🟢 An item names its evidence on its line. A done check names the run
that proved it, `via <command> at <commit>`. A done task names the commit
its own done record was written at, `at <commit>`, and a done approval
names its seat too, `by <seat> at <commit>`. A unit or contract that
reads `done` after a close with `progress done` names that close, `at
<commit>`; one that a later record changed, such as a task started again
or a check's red run, reads as that record says and names none. A
blocked task names its reason, `because <reason>`. A contract's `G0`
verdict, whatever it reads, names the validator run behind it:
`via python -m taskcontract validate specs/<contract>/contract.yaml
--profile ready at <commit>`; a feature before intake's names none, since
no validator runs ("Features before intake"). A signed half names its
signature, `by <signer> at rN` ("Revisions and halves").

🟢 Evidence ends in `dirty` in two cases. A run, a task's record or a
close reads `dirty` when a tracked file differed from `HEAD` as it was
recorded; untracked files do not count, so the untracked REQUESTs in a
repo's root never mark it. A contract's `G0` verdict reads `dirty` when
its own contract file differs from `HEAD`: changed, staged or not, or not
yet committed. Outside a git repository the commit reads `no commit`, and
nothing reads `dirty`.

### The three modes 🟢

- 🟢 **`taskcontract tree`** prints the whole tree and exits 0. Each
  source it cannot read prints one line on stderr, and the rest of the
  tree still prints.
- 🟢 **`taskcontract tree <id>`** prints one item, for an agent that needs
  one fact without reading a document: its line as the whole tree prints
  it, cut after the evidence, then one labeled line per field it has:
  `summary:` whole, on a contract only, one line per link kind with its
  targets joined by `, `, `doc:`, `file:` and `page:`. A file reference
  is a repo path with the line the item starts at: line 1 for a contract,
  its verdicts and a finding, the line its entry starts for a unit or a
  check, and for a half the line of its counting signature, else line 1;
  a feature's document shows on its `doc:` line at line 1. A gate, a
  verdict, a condition and a task name the kit page that defines the gate
  or the task, a path in the kit's repository. So an item never takes
  more than seven lines, whatever its fields hold. Every id the tree
  prints works here, matched whole. An id that names two items (a check whose sketch names a
  task key, such as `(commit)`, or a unit named like an active gate)
  prints both, in the tree's order, with an empty line between them. An
  unknown id exits 2 with `no node '{id}' - print the tree to list every
  node id`, and an id with `--follow` exits 2 with `taskcontract tree:
  --follow takes no id - give the id or --follow, not both`.
- 🟢 **`taskcontract tree --follow`**, with the `pane` extra, runs the
  interactive pane ("The interactive pane", below): the whole tree as an
  outline, moved through with the keys and the mouse. It renders again
  within two seconds of a change to a source file (a vocabulary change
  can take longer, below), and never while nothing changes. Ctrl-C exits
  0. It runs on Windows.

🟢 One check of this kit's own tree: its sketch line is its plain name,
and its evidence names the commit of its last green run:

```
$ taskcontract tree tree-view/t6-query-face/SC6.1
tree-view/t6-query-face/SC6.1 verify an item id prints its source field, status, links and each file reference in at most 20 lines (SC6.1) [done] via python -m pytest tests/test_tree_query.py -q --tb=no -p no:cacheprovider -k sc6_1 at 7945f13
file: specs/tree-view/contract.yaml:186
```

🟢 The pane lists its sources once a second: every file under `specs/`,
`.sdlc/findings/`, `.sdlc/progress/` and `docs/features/`, plus
`.sdlc/config.yaml` and the kit's two lists. It renders again only when a
file was added, removed or changed; a terminal resize cuts each line
again to the new width without a render. It keeps each contract's `G0` reading in memory until that contract's file
changes. A change under `specs/vocabulary/` drops every reading, so that
render runs the validator on every contract and can take longer than two
seconds on a repo with many contracts.

🟢 The current task is derived, never stored: the task marked `doing`
most recently; with none `doing`, the first `to do` task in the contract
that changed most recently; with no progress at all, none, and the pane's
cursor starts on its first line. Marking the current task done moves it on.

### The seven tasks 🟢

🟢 Every unit follows one task list, shown and not enforced, but for one
refusal: while G1 is an active gate for the feature and has not passed,
`progress` refuses a task's start and a done ("G1 as an active gate",
at this section's end). Nothing else stops a unit that skips a task.
Writing the tests and proving red belong
to the spec channel (G2.5), green to the developer (G3), and each
approval is a seat's answer. With `U` for the unit's id
(`<contract>/<unit>`), one command records each task:

| # | Task | Key | Record it with |
|---|---|---|---|
| 1 | Approve the test list | `approve-tests` | `taskcontract progress done U/approve-tests --by <seat>` |
| 2 | Write the tests | `write-tests` | `taskcontract progress done U/write-tests` |
| 3 | Prove red | `prove-red` | `taskcontract progress done U/prove-red` |
| 4 | Green | `green` | `taskcontract progress done U/green` |
| 5 | Approve the commit | `approve-commit` | `taskcontract progress done U/approve-commit --by <seat>` |
| 6 | Commit | `commit` | `taskcontract progress done U/commit` |
| 7 | Two-Key PASS | `two-key` | `taskcontract progress done U/two-key` |

🟢 The checks carry their own runs. During prove red, run each check's
test through the kit with the red it expects:

```bash
taskcontract progress run U/<check> --expect red -- <test command>
```

🟢 During green, run the same without `--expect`, which means `--expect
green`, so a check reads `done` only on a green that was meant to be
green.

### Recording progress 🟢

🟢 `taskcontract progress` writes `.sdlc/progress/<contract>.yaml`, one
local file per contract. The folder holds a `.gitignore` of `*`, so none
of it is committed; the file is disposable, and no gate, check, audit or
hook reads it. Every record carries its time and the `HEAD` commit, and
inside a git repository a `dirty` mark.

| Command | What it records |
|---|---|
| `taskcontract progress start <id>` | the task `doing` |
| `taskcontract progress done <id>` | the task `done`; on a unit or a contract, a close. An approval (`approve-tests` or `approve-commit`) needs `--by <seat>`, and no other item takes it |
| `taskcontract progress block <id> --reason <text>` | the task `blocked`, with its reason, which it needs |
| `taskcontract progress run <check> [--expect red\|green] -- <command>` | runs the command, then records red or green, the expectation (`green` unless given), the command, the commit, a `dirty` mark and the time; exits 0 when the result met the expectation, 1 when it missed |

🟢 A call the kit refuses writes nothing, exits 2 and prints one line on
stderr, and `run` refuses before it starts the command. `{action}` is
`start` or `block`:

```
no node '{id}' - print the tree to list every node id
taskcontract progress: '{id}' is a {kind}, not a check - run takes a check id
taskcontract progress: '{id}' is a {kind}, not a task - {action} takes a task id
taskcontract progress: '{id}' is a {kind}, not a task, unit or contract - done takes a task, unit or contract id
{unit} cannot start: G1 has not passed for {feature}
taskcontract progress: '{id}' is an approval - done needs --by <seat>
taskcontract progress: '{id}' is not an approval - only approve-tests and approve-commit take --by
taskcontract progress: block needs --reason <text> - say why '{id}' is blocked
taskcontract progress: unreadable progress: {path} ({reason})
taskcontract progress: cannot start {command} ({reason})
```

🟢 The G1 line stands for `start` on a task and `done` on a task, a unit or a
contract, while G1 is an active gate for the feature and does not read `done`
(§9, "G1 as an active gate"). On a contract's close `{unit}` is the feature's id.

🟢 A malformed progress file prints one line naming it, and its contract
reads as having no progress. No writer touches it: a call on that
contract that passes its other checks is refused with the `unreadable
progress` line above, so fix or remove the file first.

🟢 **History, backfilled.** `taskcontract progress done` on a unit or a
contract closes every task and check under it; a close never covers a
verdict, which the validator reads. A closed unit reads `done`. A closed
contract reads `done` whatever its verdicts read, and each verdict keeps
the validator's reading on its own line. A record written after a close
still counts, so a task started again or a check's red run changes what
the closed item reads. A contract
finished before the tree existed reads `to do` until it is closed, so one
command per contract backfills its history; a fresh clone, which starts
with no progress file, rebuilds it the same way.

### The notify command 🟢

🟢 When the current task is `approve-tests` or `approve-commit`, the
pane's first line reads `waiting on a seat: {approval} for {unit}`, and
the command set in `.sdlc/config.yaml` runs:

```yaml
tree:
  notify: <command>
```

🟢 It runs through the shell at the repo root, once each time the current
task arrives at an approval, never on a render, with the item's id in
`SDLC_NODE` and its own output discarded. A pane that starts on an
approval has arrived there, so it runs the command at once. The pane
never waits on the command. One that ends nonzero shows `notify failed,
exit {code}: {command}` inside the pane, whole, under the outline, until
the next render; when the shell itself cannot start, the same line reads
code 127. The pane keeps running either way, and with no `notify` set it
runs the same. Ctrl-C ends the pane and leaves the commands it started
running. The key is optional, and
the config template does not carry it. The command is the kit's edge: a
terminal multiplexer's plugin (herdr's, for one) wraps it outside the
kit.
