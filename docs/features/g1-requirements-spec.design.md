| Revision Date | Revised By | Changes Made |
| :-: | :-: | :-- |
| 2026-10-07 | user | r1: Created through /sdlc:product-specification-interview. The design, in progress, against requirements r3. Engineer seat: user |
| 2026-10-07 | user | r2: Measured: the checks before signing, on the solution half: 3 findings (CL003 2, CL014 1); Scope against the release unit's paths: covered; ready checks 11 to 15: 0 OPEN |
| 2026-10-07 | user | r3: The solution half finished: 12 sections written, 0 OPEN |
| 2026-10-07 | user | r4: Signed: solution half. The engineer seat signs r3 |
| 2026-10-08 | user | r5: Confirmed against requirements r6 |
| 2026-10-08 | user | r6: Signed: solution half. The engineer seat signs r5 |
| 2026-10-08 | intake | r7: Ready: contract `g1-requirements-spec` validates ready-green, derived from r5, against requirements r6; the engineer seat (user) signed the solution half at r5 (r6) |
| 2026-10-17 | user | r8: Measured: the checks before signing, on the solution half's amendment: 14 findings (CL014 14), each a copied term ratified since r2 and none in the amended text; Scope against the release unit's paths: covered; ready checks 11 to 15: 0 OPEN |
| 2026-10-17 | user | r9: Amended by hand in kit session 101, after the signature and intake: G1.1's record holds a `runs` list, one run for each `g1.schemas` entry with a schema in scope (Interfaces: the record file and its edges); a tool not installed is recorded for its own run; a contract whose scope cannot be read or holds no entry reads G1.1 `to do` and `lint` refuses it (Interfaces: the edges and How a condition reads); three answers under Decisions; typed by Claude on the user's word |
| 2026-10-17 | user | r10: Signed: solution half. The engineer seat signs r9 |
| 2026-10-17 | intake | r11: Ready: contract `g1-requirements-spec` validates ready-green, derived from r9, against requirements r6; the engineer seat (user) signed the solution half at r9 (r10) |
| 2026-11-12 | user | r12: Amended by hand in kit session 147, against requirements r10, after the engine's finding `g1-unreachable-from-a-plain-request`: `new` refuses a feature G1 gates that has no feature document, and intake's I3 reports any refusal of `new` (Scope, Interfaces: The scaffold, Sources); G1.3 reports RS302 for such a feature, and the venue asks no item there; unit `s7-plain-request` takes SC1.2 and SC4.1 and ships kit 0.22.1 (Units, Order); the usage pages for messages 8 and 9 (Scope); consult cases 2 and 4; constraint 10's count; one risk; five answers under Decisions, one naming the kept readings left for Next 26 (ADR 0041, rule 1); typed by Claude on the user's word |
| 2026-11-12 | user | r13: Measured: the checks before signing, on the solution half's amendment: 14 findings (CL014 14), each a copied term ratified since r2 and none in the amended text; Scope against the release unit's paths: covered; ready checks 11 to 15: 0 OPEN; kept readings since r9 (ADR 0041, rule 1): 39, 1 taken and 38 left, each named under Decisions |
| 2026-11-12 | user | r14: Signed: solution half. The engineer seat signs r12 |
| 2026-11-12 | intake | r15: Ready: contract `g1-requirements-spec` validates ready-green, derived from r12, against requirements r10; the engineer seat (user) signed the solution half at r12 (r14) |
| 2026-11-13 | user | r16: Amended by hand in kit session 151, against requirements r10, after the engineer seat's rulings on G1's 37 open edges (kit session 150, Next 26): 28 fixed in three units, 1 found closed by `s4-tree`, and 8 left, each named (Interfaces: The edges ruled at r16); every reading kept at a PR review since r9 taken, two of them overturned by a ruling (ADR 0041, rule 1); a G1.2 record binds the model's folder (The files); `lint` refuses a call with no `g1.schemas`; G1 does not gate a contract born of an escape or maintenance (The scaffold, Intake's report, Sources); units `s8-honest-reads`, `s9-one-line-refusals` and `s10-words-and-folds` take seven existing checks and ship kit 0.22.2 (Units, Order); Scope; constraint 10's count; six risks; consult cases 2 and 4; nine answers under Decisions; typed by Claude on the user's word |
| 2026-11-13 | user | r17: Measured: the checks before signing, on the solution half's amendment: 14 findings (CL014 14), each a copied term ratified since r2 and none in the amended text; Scope against the release unit's paths: covered; ready checks 11 to 15: 0 OPEN; kept readings since r9 (ADR 0041, rule 1): 45, 31 taken as built, 2 overturned, 3 closed by a fix, 1 left, 7 with no design text and 1 ruled as an edge, each named under Decisions; each edge's source re-read at its line: one found closed by `s4-tree`, one line moved in `docs/usage/g1.md` |
| 2026-11-13 | user | r18: Signed: solution half. The engineer seat signs r16 |
| 2026-11-13 | user | r19: Amended by hand in kit session 152, against requirements r10, after intake found `s8-honest-reads` with four checks and a contract unit holds at most three sketch entries: SC2.1 and SC3.1 share one entry, `SC2.1+SC3.1` (Units); typed by Claude on the user's word |
| 2026-11-13 | user | r20: Measured: the checks before signing, on the solution half's amendment: 14 findings (CL014 14), each a copied term ratified since r2 and none in the amended text; Scope against the release unit's paths: covered; ready checks 11 to 15: 0 OPEN |
| 2026-11-13 | user | r21: Signed: solution half. The engineer seat signs r19 |
| 2026-11-13 | intake | r22: Ready: contract `g1-requirements-spec` validates ready-green, derived from r19, against requirements r10; the engineer seat (user) signed the solution half at r19 (r21) |

# g1-requirements-spec - Failure points found before development starts

`sdlc_development_kit` · seat: engineer user · requirements: `docs/features/g1-requirements-spec.md` · contract: `g1-requirements-spec`, draft · PR: none · merge SHA: none

## Proposed solution

`[Engineer seat · authored]`

### Scope

The package:

- `taskcontract/g1.py` (new): G1's rules, the record's reader and its one writer.
- `taskcontract/__main__.py`: two subcommands, `g1-check` and `g1-record`.
- `taskcontract/data/gates.yaml`: `rules:` on G1.1, G1.2 and G1.3.
- `taskcontract/data/g1-items.yaml` (new): G1.3's 11 items, each a number and a name.
- `taskcontract/data/tasks.yaml`: its header comment.
- `taskcontract/schemas/component-declaration.schema.json` (new, version 1.0.0).
- `taskcontract/tree.py`: a feature's own active gates, G1's reading, G1.3's evidence.
- `taskcontract/tree_view.py`: the pane watches `.sdlc/g1`.
- `taskcontract/progress.py`: the refusal.
- `taskcontract/scaffold.py`: `new` refuses a feature G1 gates that has no feature document (`s7-plain-request`); `new --origin` (`s8-honest-reads`).
- `taskcontract/scope_check.py`: the YAML loader's ValueError reads as a YAML error (`s9-one-line-refusals`).
- `taskcontract/__main__.py`, `g1.py`, `tree.py` and `progress.py` again, for the edges ruled at r16 (`s8-honest-reads` to `s10-words-and-folds`).

The skill:

- `skills/sdlc/flows/g1.md` (new): the venue.
- `skills/sdlc/SKILL.md`: the dispatch line, the flow list, one constraint, one criterion.
- `skills/sdlc/flows/intake.md`: one sentence at I9; one clause at I3, which reports any refusal of `new` (`s7-plain-request`).
- `skills/sdlc/flows/g1.md`: at R5, no item is asked where the feature has no feature document (`s7-plain-request`); R5's ask says what `checked` covers (`s10-words-and-folds`).
- `skills/sdlc/flows/intake.md`: I3 passes `--origin` for an escape or maintenance, and I9 names both origins (`s8-honest-reads`).
- `skills/sdlc/init.py`: `KIT_VERSION`.
- `skills/sdlc/templates/SDLC.md.template` and `skills/sdlc/templates/specs-README.md.template`.

The release and the pages:

- `pyproject.toml`: the version.
- `tests/`: each unit's tests, and the retirements Units names.
- `USAGE.md`, `CHANGELOG.md`, `MAP.md` and `SDLC.md`.
- `docs/usage/intake.md` and `docs/usage/g1.md`: messages 8 and 9 (`s7-plain-request`); the lines and refusals of r16 (`s8-honest-reads` to `s10-words-and-folds`).
- `docs/gates/G1-requirements-spec.md`, `docs/gates.md` and `docs/operators.md`.
- `.github/workflows/sdlc.yml`: the install pin, moved at the self-pin after the tag.

The kit as G1's first consumer:

- `.sdlc/config.yaml`: `G1` under `active_gates`, and the `g1` key.
- `specs/components.yaml` (new): the kit's own component declaration record.
- `.spectral.yaml` (new): the kit's pinned ruleset (prerequisite 8).

### Out of scope

The requirements run left no state file, so no refused place is shown
here. The build leaves these places untouched:

- `taskcontract/checker.py` and the `validate` command: ready-green keeps meaning G0 alone.
- `taskcontract/schemas/task-contract.schema.json`: the contract schema stays at version 1.5.0.
- `skills/product-specification-interview/`: every file.
- `skills/sdlc/flows/intake.md`, steps I1, I2 and I4 to I8.
- `.github/workflows/ci.yml` and `skills/sdlc/templates/workflow.yml.template`: no step runs a linter or a checker.
- `skills/sdlc/templates/config.yaml.template`: a new repository is born with G0 alone.
- `skills/sdlc/templates/hooks-protect-specs.py.template`.
- `skills/sdlc/audit.py`.
- `agents/`: no `sdlc-spec` definition ships, and `sdlc-developer.md` stays as it is.
- `taskcontract/pane.py`.
- `.sdlc/progress/`: no G1 record stands there, and the progress file keeps its form.
- G1.3's 11 items on `docs/gates/G1-requirements-spec.md`, word for word.

### Interfaces

A user sees one flow, two commands, seven messages, three files and the
tree. The drawings use a consumer's feature, `apply-discount`.

**The venue.** `/sdlc g1 {id}` runs after intake and before a unit's
first task, in seven steps:

| Step | What it does |
| :-- | :-- |
| R1 | Reads the contract. It stops when the contract is not ready-green, or when G1 is not active for the feature. |
| R2 | Reads the two declarations. When one is absent it shows the form and stops: a person writes a declaration, never the flow. |
| R3 | Runs `python -m taskcontract g1-record lint {id}` and shows its lines. |
| R4 | Runs `python -m taskcontract g1-record model {id}` and shows its lines. |
| R5 | Asks the person each of G1.3's 11 items, one at a time, in the item's own words. For items 3 and 4 it shows intake's `Ready:` rows as the evidence. For an item left unchecked it asks which section the item concerns. |
| R6 | Asks the signer's name and seat, then runs `python -m taskcontract g1-record review` on the person's word. An agent may draft a reading of an item; it never answers one and never signs. |
| R7 | Runs `python -m taskcontract g1-check {id}`, shows its lines and names the next step. |

R7's report ends on one of two lines:

```
G1 has passed for apply-discount. Next step: the first unit's approve-tests.
G1 has not passed for apply-discount. Fix each line above, then run /sdlc g1 apply-discount again.
```

**`g1-record`, the one writer.** Each call appends one record to
`.sdlc/g1/{id}.yaml`, and the last record of a condition counts.

```
$ python -m taskcontract g1-record lint apply-discount
G1.1: api/openapi.yaml lints clean under spectral
recorded: .sdlc/g1/apply-discount.yaml

$ python -m taskcontract g1-record model apply-discount
G1.2: the model of ledger passes tlc
recorded: .sdlc/g1/apply-discount.yaml

$ python -m taskcontract g1-record review apply-discount --by "Ann Lee" --seat po --checked 1,2,3,4,5,7,8,9,10,11 --unchecked 6=Statement
G1.3: item 6 Consistent is unchecked in Statement
recorded: .sdlc/g1/apply-discount.yaml
```

It exits 0 when the record it wrote reads clean, and 1 when the record
fails its condition, with the failure's message printed. It exits 2 and
writes nothing on a call it cannot use: no contract for the id, G1 not
active for the feature, a review that does not name each of the 11
items once, or a seat that is no value of the ratified `intake-seat`
term. Its edges:

- With `g1.schemas` declared and no boundary schema in scope, `lint` prints `G1.1: no boundary schema in scope`, writes nothing and exits 0. With no `g1.schemas` key, `lint` refuses the call (r16).
- With no hard core in scope, `model` prints `G1.2: no hard core in scope`, writes nothing and exits 0.
- A tool that is not installed is recorded as such for its own run, and the other runs stand, so the condition reads `failed`; the call prints message 1 or 3 and exits 1.
- A contract whose scope cannot be read, or holds no entry, is a call `lint` cannot use: it exits 2 and writes nothing, as `model` and `review` have it.
- A hard core with no model gets message 2 and no record: the rule reads the declaration.

**`g1-check`, the verdict.** It reads the records and the declarations,
runs no tool and writes nothing.

```
$ python -m taskcontract g1-check apply-discount
apply-discount: RS201 G1.2: hard core ledger has no model
apply-discount: G1.1 done, G1.2 failed, G1.3 to do

$ python -m taskcontract g1-check apply-discount
g1-green: apply-discount
```

It exits 0 when G1 reads `done` and 1 when it does not. It exits 2 when
G1 is not active for the feature, printing `apply-discount: G1 is not
active`, when the id has no contract, or on a call it cannot use.
`--root` names the repository, as `tree` has it. `--json` prints a
`note`, which holds the summary line, and a `findings` array:

```json
{"note": "G1.1 done, G1.2 failed, G1.3 to do", "findings": [{"feature": "apply-discount", "condition": "G1.2", "rule": "RS201", "message": "G1.2: hard core ledger has no model"}]}
```

**The messages.** Seven. Messages 1 to 5 are the requirements' words;
6 and 7 are new here, and `{n}` counts errors and warnings alike.

| # | Rule | Message |
| :-: | :-: | :-- |
| 1 | RS101 | `G1.1: {tool} is not installed; install it and pin it in the repository` |
| 6 | RS102 | `G1.1: {file} does not lint clean: {tool} reports {n}` |
| 2 | RS201 | `G1.2: hard core {component} has no model` |
| 3 | RS202 | `G1.2: {tool} is not installed; install it and pin it in the repository` |
| 7 | RS203 | `G1.2: the model of {component} does not pass {tool}` |
| 5 | RS301 | `G1.3: item {n} {item} is unchecked in {section}` |
| 4 | none | `{unit} cannot start: G1 has not passed for {feature}` |

Message 4 is a refusal of `progress` and no rule's. `{item}` is the
item's name in `g1-items.yaml`. `{section}` is a section name of the
feature's requirements document or design document, as the person names
it. `{unit}` is the unit's own id, or the feature's id on a contract's
close.

**How a condition reads.** Each of the six rules reports `failed`. With
none reported, a condition reads `done` when everything it needs is
present and current, else `to do`, and a `to do` lists nothing.

| Condition | Reads `to do` | Reads `done` |
| :-- | :-- | :-- |
| G1.1 | `g1.schemas` is absent; or the contract's scope cannot be read or holds no entry; or a schema in scope has no lint record that matches its hash and the pin's | no schema is in scope; or every schema in scope is recorded clean |
| G1.2 | `specs/components.yaml` is absent; or a hard core in scope has a model with no record that matches its folder's hash and its configuration's | no hard core is in scope; or every one is recorded as passing |
| G1.3 | no review is recorded; or the last review passed on revisions the contract was not derived from | the last review checks all 11 items on the revisions the contract was derived from |

A schema is in scope when its path matches a `g1.schemas` pattern and
the contract's `scope`. A hard core is in scope when one of its paths
and a `scope` entry overlap. A review that leaves an item unchecked
reads `failed` until a later review passes, whatever revision follows.
The G1 verdict is the roll-up of its three conditions. A record or a
declaration that cannot be read counts as absent, and the tree prints
its problem line.

**The files.** `.sdlc/config.yaml`, written by a person:

```yaml
active_gates:
  - G0
  - G1
g1:
  exempt:
    - controlled-language
  schemas:
    - paths: [api/*.yaml]
      linter: spectral
      pin: .spectral.yaml
```

`specs/components.yaml`, written by a person:

```yaml
version: 1
components:
  - id: ledger
    paths: [src/ledger/]
    hard_core: true
    oracle: concurrency
    model: specs/models/ledger.tla
    model_config: specs/models/ledger.cfg
    checker: tlc
  - id: api
    paths: [src/api/]
    hard_core: false
    oracle: none
    oracle_reason: read-only pass-through, covered by its acceptance tests
```

`.sdlc/g1/apply-discount.yaml`, written by `g1-record` alone and
committed:

```yaml
records:
  - condition: G1.1
    at: 2026-10-07T14:02:11Z
    head: 8635064
    runs:
      - tool: spectral
        tool_version: 6.11.0
        installed: true
        pin: {path: .spectral.yaml, sha256: 9f2c}
        files:
          - {path: api/openapi.yaml, sha256: 41d0, reported: 0}
  - condition: G1.3
    at: 2026-10-07T14:20:40Z
    head: 8635064
    by: Ann Lee
    seat: po
    requirements: r5
    design: r4
    items:
      - {n: 1, name: Testable, checked: true}
      - {n: 6, name: Consistent, checked: false, section: Statement}
```

The drawing cuts each hash to four characters and the items to two.
The edges of the three files:

- `exempt` absent means no feature is exempt. An `exempt` id that names no feature prints a problem line in the tree.
- `schemas: []` and `components: []` each say none.
- `linter` is `spectral` or `buf`; `checker` is `tlc` or `p`.
- `oracle` is one of `differential`, `fuzz`, `property-only`, `concurrency`, `soak` and `none`, and `none` needs an `oracle_reason`.
- A G1.1 record holds one run for each `g1.schemas` entry with a schema in scope, in the entry's order: the tool, its version, whether it is installed, the pin, and each file's hash with the count the tool reported. An entry with no schema in scope has no run. A record that holds `tool`, `pin` and `files` on the record itself counts as absent.
- A G1.2 record holds one entry per hard core: the component, the tool, the hash of the model's folder, the configuration's hash, and `pass` or `fail` (r16). The folder's hash covers each file under the folder that holds `model` whose extension is the checker's, by path: `.tla` and `.cfg` for TLC, `.p` and `.pproj` for P. A trace module TLC writes beside the model during a run is left out. An entry of the two-file form counts as absent.
- A feature whose contract was derived from one document holds no `design` revision in its review.

**The tree.** A feature that needs G1 shows it active, with G2 as the
inactive next gate:

```
  apply-discount/G1 Requirements / Spec [failed]
    apply-discount/G1/G1.1 Spec/schema linting [done]
    apply-discount/G1/G1.2 Model checking [failed]
      - G1.2: hard core ledger has no model
    apply-discount/G1/G1.3 Criteria completeness + ambiguity review [done] by po at r5, design r4
  apply-discount/G2 Design / Architecture [to do] inactive
```

The repository's line names each feature that holds G1:

```
gates/G1 Requirements / Spec [failed]
  - apply-discount holds G1 at failed
```

An exempt feature prints as today, byte for byte: G0, then G1 `[to do]
inactive`. A feature before intake that is not exempt shows G1 active
and `to do`. A diagnostic prints its message whole, its `G1.2:` opening
included. A review on a feature with one document reads `by po at r5`.

**The refusal.** `progress start` on a task, and `progress done` on a
task, a unit or a contract, refuse while the feature's G1 is active and
not `done`. The line goes to stderr, and the call exits 2 and writes
nothing:

```
$ python -m taskcontract progress start apply-discount/u1-rate/approve-tests
u1-rate cannot start: G1 has not passed for apply-discount

$ python -m taskcontract progress done apply-discount
apply-discount cannot start: G1 has not passed for apply-discount
```

`block` and `run` stay open. A contract's close is refused with the
feature's id in the unit's place: a close would else mark every task
done with G1 not passed. An exempt feature is never refused, in either
build of the tree, nor a contract born of an escape or maintenance (r16).

**Intake's report.** I9 gains one sentence. For a ready-green contract
whose feature needs G1, the report ends:

```
Next step: G1. Run /sdlc g1 apply-discount.
```

With `G1` absent from `active_gates`, the feature exempt, or the
contract's origin `g8-escape` or `g9-maintenance` (r16), the report
ends as today.

**The scaffold** (`s7-plain-request`). `new {id}` keeps its two
refusals, a bad id and a contract that exists, in that order. Then,
where G1 is active for {id} and `docs/features/{id}.md` is no file, it
writes nothing, prints message 8 on stderr and exits 1, as its other
refusals do. It reads G1 through `g1.read_config` and `g1.is_active`.
`new {id} --origin {origin}` (r16) writes the origin into the
scaffold's `provenance`, `human-request` when the flag is absent; with
`g8-escape` or `g9-maintenance` G1 does not gate the contract, and `new`
skips message 8. I3 passes the flag for a request that comes from an
escape or from maintenance. I3 gains one clause: on any other failure of `new`, REPORT its line
verbatim, write nothing, and return to the conversation. The clause names
no G1 word, no config file and no command, so I9's tests stand.

```
$ python -m taskcontract new apply-discount
taskcontract new: no feature document for apply-discount, and G1 is active for it; write docs/features/apply-discount.md, or add apply-discount to g1.exempt
```

**A contract with no feature document** (`s7-plain-request`). G1.3
reads it first: where `docs/features/{id}.md` is no file, G1.3 reads
`failed` with one finding, `RS302`, message 9, whatever its records
hold. The tree and `g1-check` show it as they show `RS301`. At R5 the
venue asks no item there and goes to R7, whose `g1-check` line names the
way out. `g1-record review` keeps its refusal.

**The edges ruled at r16.** The engineer seat ruled G1's open edges on
2026-11-13 (kit session 150). This row also takes each reading kept at a
PR review since r9 (ADR 0041, rule 1), named by PR and number. Each
group names the unit that builds it.

G1 reads only what it checked (`s8-honest-reads`):

- A `.sdlc/config.yaml` that stands and cannot be read is never read as G1 off. It cannot be read when it is not UTF-8, is no YAML mapping, or holds an `active_gates` that is no list of text, a `g1` that is no mapping, or a `g1.exempt` that is no list of text. `new` then exits 1 with `taskcontract new: .sdlc/config.yaml cannot be read: {reason}`; `progress start` and `progress done` exit 2 with `{unit} cannot start: .sdlc/config.yaml cannot be read: {reason}`; `g1-check` and `g1-record` exit 2 with `{id}: .sdlc/config.yaml cannot be read: {reason}`. The tree keeps its print and its problem lines. An absent file still means no gate is active. This closes PR #119's readings 6 and 9.
- Intake reaches I9 only past I3's `new`, which reads the config with the kit's reader and refuses one it cannot read. I9 then reads the keys the kit reads (PR #119, reading 7).
- The tree's second build reads `g1.exempt`: an exempt feature prints as today and is never refused, and each other feature holds G1 active with each condition `to do`. This overturns PR #116's reading 12 and PR #119's reading 5.
- G1 does not gate a contract whose `provenance.origin` is `g8-escape` or `g9-maintenance`: it fixes or keeps behavior that a gated feature already specified. Its G1 reads `inactive`, as an exempt feature's does (The scaffold; PR #162, reading 7).
- `lint` with no `g1.schemas` key refuses the call with `{id}: no g1.schemas in .sdlc/config.yaml`. `schemas: []` says none.
- A `g1.schemas` pattern loses a leading `./`. A pattern that is absolute, holds `..`, or matches no file makes the declaration unreadable, with the pattern in the reason: G1.1 reads `to do` with the tree's problem line, and `lint` refuses. A pattern whose folder differs from the disk in case alone, or whose folder the system refuses, matches no file (PR #116, reading 9). The walk skips `.git`.
- A G1.2 record binds the model's folder (The files).
- A P configuration that names no test case (`-tc`) is refused: `{id}: the configuration of {component} names no test case: {path}`. P's live run stays open (risk 2).
- A linter or a checker that resolves to a file inside the repository is refused: `{id}: {tool} resolves inside the repository: {path}`. A committed file could report any pass.
- Two components with one `id`, or a `model` or `model_config` path outside the repository, make `specs/components.yaml` unreadable, with the component in the reason.

No hand-written file ends a command on a traceback (`s9-one-line-refusals`):

- With G0 active, a contract that is not UTF-8, or whose scope holds a number past 4300 digits, prints as an unreadable contract, and the print goes on. `validate` keeps every byte of its output.
- `tree._load`, `scope_check.contract_scope` and `g1._seat` read the YAML loader's ValueError (a date no calendar holds, with no quotes) as a YAML error, as `g1.py`'s other readers do. A test feeds each one such a file.
- `g1-check` holds each reader's failure to one line with exit 2, in the tree's words: `{id}: unreadable G1 reading: {condition} ({class}: {message})`.
- Each writer exits 2 with one line where it ended on a traceback, and writes nothing: `taskcontract g1-record: the record cannot be written: {path} ({reason})`; `taskcontract g1-record: the kit's schema cannot be read: {name} ({reason})`. A NUL in a declared path or in a P configuration makes that file unreadable. A contract that is not UTF-8 is a scope that cannot be read (PR #116, reading 10).
- Each command writes a character its output cannot hold as its backslash escape, as the print does since `s4-tree` (PR #116, reading 15). No byte of a line that prints today changes.
- With RS302 the tree shows no review's evidence beside the line.

The words, and the folds (`s10-words-and-folds`):

- The writer's refusal lines stand here word for word, each on stderr with exit 2, and tests hold each one: `{id}: no contract at specs/{id}/contract.yaml`; `{id}: G1 is not active`; `{id}: the contract's scope cannot be read at specs/{id}/contract.yaml`; `taskcontract g1-record: unreadable record: {path} ({reason})`; `{id}: g1.schemas cannot be read: {reason}`; `{id}: g1.schemas names a linter the kit does not know: {value}`; `{id}: specs/components.yaml cannot be read: {reason}`; `{id}: no component declaration at specs/components.yaml`; `{id}: no working folder for the model of {component}: {reason}`; `{id}: the configuration of {component} cannot be read: {path}`; and the lines of `s8-honest-reads` and `s9-one-line-refusals` above. `review`'s other refusals stand as built: one line each, holding the id and the value it refuses (PR #112, reading 10).
- The two green lines: `g1-green: {id}` and `G1.3: the review checks all 11 items` (PR #112, reading 10).
- `review` takes `--unchecked {n}={section}` once for each item left unchecked, cut at its first `=`, and `--checked` as one list with commas (PR #112, reading 1). An item is one of the texts 1 to 11 and is named once, so `01` and a range are refused; `--by`, `--seat` and `--checked` each count once (reading 4). A name and a section each stand on one line and hold a letter or a digit; outer blanks are cut and the rest is kept (reading 2). The seat equals a value of `intake-seat` at the call, and `g1-check` does not read the roster (reading 5). A scope that cannot be read is refused (reading 7).
- G1.3 counts the last G1.3 record alone. A record changed by hand counts as absent unless it holds a signer, a seat and each of the 11 items once. Revisions compare as text with the `Ready:` rows on disk, and a record of one document does not count for a pair, nor the reverse (PR #112, reading 6).
- The venue: a declaration is absent when its file is absent, or when `.sdlc/config.yaml` holds no `schemas:` list under `g1:`. An answer other than `checked` or `unchecked` is no answer. A person who declines to sign gets no record, and the verdict reads not passed (PR #112, reading 9). R5 holds the 11 items word for word, and a test holds them equal to G1's page (reading 8). R6 passes a section that holds a quote or a dollar sign whole. R5's ask says that `checked` covers an item that does not apply to the feature.
- One reader reads a `Ready:` row for `g1.py` and for `tree.drift` (PR #112, reading 11).
- `build`'s docstring says what the second build prints. `docs/usage/g1.md` holds no line past its limit. `tree.py`'s docstrings that called `rules:` G0's alone were mended by `s4-tree` (`6350bec`).

The tree and the refusal, taken as built:

- G1.3's evidence shows at `done` and at `failed`, and a review that does not count shows none. The evidence is the record's seat, its ends cut, then each revision of the form `r` and digits: `by po at r5, design r4` (PR #116, readings 1 and 2).
- A feature before intake reads each condition `to do`, lists nothing, and its record file is not read (reading 3).
- Five problem lines: `unreadable g1.schemas: ...`, `unreadable component declaration: ...`, `unreadable record: ...`, `g1.exempt names no feature: {id}` and `unreadable g1.exempt: .sdlc/config.yaml (it is no list)`. A declaration's line prints once a print; a record file's prints only for a contract G1 is active for (reading 4). A sixth: a reader that ends on an error reads its condition `to do`, the other two keep theirs, and the line is `unreadable G1 reading: {id}/G1/{condition} ({class}: {message})` (reading 11). In the second build the one line is `unreadable G1 reading: G1 ({class}: {message})`, the print's last, with the class name alone where no message can be made; when the second build also fails, the error stands (reading 13).
- With G1 off the tree reads no G1 source and prints none of those lines (reading 5). An exempt feature keeps its G1 line, `inactive`, under a list that holds a later gate (reading 6).
- `tree {id}/G1/G1.3` prints the line with its evidence and its page, with no diagnostic. The pane watches G1's files under `specs`, `docs/features`, `.sdlc/findings`, `.sdlc/progress` and `.sdlc/g1`; a schema, a pin or a model elsewhere shows as last read until a watched file changes (reading 7).
- A line break prints as one space in a diagnostic and in an exempt id (reading 8).
- The refusal takes G1 from the tree's own build and reads no G1 file (PR #119, reading 1). It stands after the unknown-id and wrong-kind lines and before the checks of `--by` and of a progress file (reading 2). `{unit}` is the unit's own id, and a close prints the feature's (reading 3); a refused `done` also prints `cannot start` (reading 4).
- A contract closed before G1 became active for its feature is refused on a later `start` or `done` (reading 8). Where a contract cannot be read, `start` prints the unknown-id line and `done` on the contract prints the G1 line (reading 10).
- USAGE names the refusal as fact (reading 11), and I9's condition, ways out and line stay one sentence (reading 12).

Left, and said so:

- An error of another cause before the second build prints under G1's name for that one print. It claims nothing done.
- A text that makes a reading run long raises nothing: a `g1.exempt` entry nested deep through YAML aliases, or one that is no text, prints whole in its problem line (PR #116, reading 14).
- `buf` has had no live run: its exit code on a violation, its JSON report and its version line are read from its reference page. The first consumer with a protobuf schema measures it.
- A second name for one folder (a link, an absolute path with no drive, two Unicode forms of one name, a Windows short name) is not seen as an overlap, as USAGE says.
- An item that does not apply is answered `checked`; R5's ask says so. A third answer would add a state to every record.
- A shortened flag (`--check`) is taken; a name, a section, a seat or an exempt id may hold a terminal escape, which prints raw; on Windows an id in capitals reaches the same contract; an unknown exempt id listed twice prints twice.
- A path `docs/features/{id}.design.md` that is a folder counts as no design document.
- `progress._target` keeps its one caller.
- PR #112's reading 12 and PR #162's readings 1 to 6 record how a build ran and hold no design text.

### Sources

| Fact | Read from | When two disagree |
| :-- | :-- | :-- |
| Whether G1 is active for a feature, and which features are already done | `.sdlc/config.yaml`: `G1` under `active_gates`, and the `g1.exempt` list; the contract's `provenance.origin` (r16) | The exempt list wins for a feature it names, and it wins over a contract's close record, which is local and uncommitted. An origin of `g8-escape` or `g9-maintenance` is never gated. A config that stands and cannot be read is refused, never read as G1 off. |
| A feature's scope | `scope` in `specs/{id}/contract.yaml` | One source. |
| Which files are boundary schemas, and each one's linter and pin | the `g1.schemas` entries in `.sdlc/config.yaml`, matched against the files on disk | The declared patterns win over what a file looks like; review item 10 is the guard. |
| A lint result or a model-check result | the last G1.1 or G1.2 record in `.sdlc/g1/{id}.yaml` | The files on disk win: a record whose hashes no longer match counts as absent. |
| Whether a tool is installed | the record, as `g1-record` found it on its run | The record wins over the reader's PATH until the next run. |
| The components, the hard cores, each model and each oracle designation | `specs/components.yaml` | The record wins for the rule. ADR 0007's criteria are how a person decides, and review item 11 is the guard. |
| G1.3's 11 items, each a number and a name | `taskcontract/data/g1-items.yaml` | G1's page wins, and a test holds the list equal to the page's. |
| A review: its signer, seat, revisions and each item's answer | the last G1.3 record in `.sdlc/g1/{id}.yaml` | One source. |
| The revisions a contract was derived from | the `Ready:` row of each document's revision table | The tables win over the review record: a review that names other revisions does not count. |
| The seats a signer may name | the ratified `intake-seat` term, `specs/vocabulary/intake-seat.yaml` | One source. |
| Whether G1 has passed, for the refusal, with the unit's and the feature's ids | the feature's G1 verdict in the tree that `progress` builds on that call | One source: the refusal and the tree give the same reading. |
| G0's verdict | the validator at the draft and ready profiles, as today | One source: no G1 rule reports there. |
| Which rule belongs to which condition | `rules:` in `taskcontract/data/gates.yaml` | One source. |
| Where ready checks 1 to 15 are asked | the interview's signing flow and intake's I2, as today | One source: G1's flow holds none of their question sentences. |
| The parts of intake's report | I9 of `skills/sdlc/flows/intake.md`, as today, with the feature's id | One source. |
| Whether a feature G1 gates has a feature document | `docs/features/{id}.md` is a file, read by `new` and by G1.3 | One source: a design document alone is no feature document. |

### Constraints

1. Every message the kit prints today stays word for word, and `validate` keeps every byte of its output.
2. No G1 rule reports through `checker.validate_path`: ready-green means G0 alone for the tree, the write guard, the audit, CI and pre-commit.
3. The contract schema stays at version 1.5.0. A new schema is born at 1.0.0 with its own `$id`.
4. No new dependency: the package keeps `jsonschema` and `PyYAML`. The kit ships and installs no linter and no checker.
5. The whole suite passes on a machine with no linter and no checker installed, through a stand-in tool or a written record.
6. `g1-record` captures a tool's output as UTF-8 with replacement, opens no window, and tells a tool that did not start from one that ran and failed. It sets no time limit.
7. The tree stays derived at every print: G1's reading stores nothing and runs no tool.
8. `.sdlc/progress/` holds no G1 record, and no gate reads a progress file (ADRs 0024 and 0031).
9. An exempt feature's tree lines keep every byte, and the `gates/G0` line keeps its reading.
10. Each prompt file the build touches passes `python -m prompt_lang`, keeps the PromptLang tag set and stays under 12,000 characters. `intake.md` has 113 characters free (kit session 151), and the two origins at I3 and I9 take about 85 (r16).
11. Intake keeps I1 to I9 and their order, and I9's sentence names no fifth `python -m taskcontract` command.
12. The 13 question sentences of ready checks 1 to 8 and 11 to 15 stand in no G1 file.
13. G1.3's 11 items stay as ratified, and no agent signs a review: the flow runs the writer only on the person's word.
14. Every authored command is one segment: no pipe, no chain, no redirect.
15. In USAGE a red sentence stands under its own red subsection, and a new drawing in section 9 follows the pinned ones.

### Units

| Unit | Checks | Done means | Tests by check id and kind | Retirements |
| :-- | :-- | :-- | :-- | :-- |
| s1-lint | SC2.2, SC2.3 | With a boundary schema in a feature's scope, G1.1 reads done only when the pinned linter's record shows it clean. | SC2.1: automated, with a stand-in linter, and a manual receipt, a live Spectral run on one clean file and one unclean file. SC2.2: automated. SC2.3: automated. | USAGE's red-legend test, at pass zero (`tests/test_document_split_release.py:517-527`). The two tests that hold `rules:` to G0's conditions (`tests/test_tree_conditions.py:313-327` and `432-442`), each replaced by one that holds G1's too. |
| s2-model | SC3.2 | With a hard core in a feature's scope, G1.2 reads done only when the record shows its model passes the checker. | SC3.1: automated, with a stand-in checker, and a manual receipt, a live TLC run on one passing model and one failing model. SC3.2: automated. SC3.3: automated. | none |
| s3-review | SC1.3 | A seat reads G1.3's 11 items at the venue, and G1.3 reads done only from a review with a signature. | SC1.1: automated, and a manual receipt, a live run of `/sdlc g1` on an invented feature with a seat answering the 11 items. SC1.2: automated. SC1.3: automated, a text test on G1's flow, the interview and intake. | none |
| s4-tree | SC5.3 | The tree shows G1 as an active gate where a feature needs it, with each condition's status, diagnostics and review. | SC5.1: automated. SC5.2: automated. SC5.3: automated. | The sha256 pin on `tree.py`'s code (`tests/test_document_split_release.py:483-490`); the docstring's sentence order, pinned at line 487, stays. |
| s5-start | SC4.2 | Intake's report names G1 as the next step, and no unit's task reads done before its feature's G1 passes. | SC4.1: automated, a text test on I9, and a manual receipt, a live intake run whose report ends on the G1 line. SC4.2: automated. | Two sentences that say no task is enforced, each reworded: `tasks.yaml`'s header comment and USAGE's "shown and never enforced". No test pins either. |
| s6-release | SC4.3 | Kit 0.20.0 ships G1 with its documentation, and the kit's own tree shows G1 as an active gate with G0 unchanged. | SC4.3: automated, on a fixture and on the kit's own tree. Two manual receipts: the install from the tag reads 0.20.0, and Spectral lints the kit's four schemas under `.spectral.yaml`. | Section 9's banner test (`tests/test_document_split_release.py:530-545`), replaced. USAGE's drawing of this feature before intake (`USAGE.md:1640-1655`), redrawn on an invented feature. |
| s7-plain-request | SC1.2 | `new` refuses a feature with no feature document where G1 is an active gate, and G1.3 names the missing feature document. Kit 0.22.1 ships the fix. | SC1.2: automated, the no-document case beside `s3-review`'s. SC4.1: automated, `new` on both paths into intake, a plain request and a pair, each taken on to `g1-record review`; and a manual receipt, a live intake run on a plain request with G1 active, taken to the `/sdlc g1` step (ADR 0041, rule 3). | Any test that scaffolds through `new` where G1 is active with no feature document, found by the test-retirer. |
| s8-honest-reads | SC2.1+SC3.1, SC4.1, SC5.2 | G1 reads done only for what a tool or a review checked. Only the config and the contract's origin name where G1 is an active gate. | SC2.1: automated, with a stand-in linter: a pattern that matches no file, a pattern with `./` and a tool inside the repository. SC3.1: automated, with a stand-in checker: the model's folder bound, and a P configuration with no test case; and a manual receipt, a live TLC run on one passing model, which records what TLC writes beside it. SC4.1: automated, `new --origin` and a config `new` cannot read, on a plain request and a pair; and a manual receipt, a live intake run on a request from an escape with G1 active, taken to its report's end (ADR 0041, rule 3). SC5.2: automated, an exempt feature in the second build. | Any test that pins G1.1 `done` for a pattern that matches no file, `lint`'s exit 0 with no `g1.schemas` key, a G1.2 record of the two-file form, or a config read as empty, found by the test-retirer. |
| s9-one-line-refusals | SC3.3, SC5.1 | A file that cannot be read stops no command. `g1-check` and `g1-record` each exit 2 with one line, and the tree goes on. | SC3.3: automated, each writer's three failures, a date with no quotes in each reader, and a character outside the code page through a pipe. SC5.1: automated, a contract that is not UTF-8 and a scope number past 4300 digits with G0 active, and the RS302 line with no evidence. | none |
| s10-words-and-folds | SC1.1 | Each line that `g1-record` shows stands in the design word for word, and one reader reads a `Ready:` row. Kit 0.22.2 ships the three units. | SC1.1: automated, each refusal line and both green lines word for word, several unchecked items, a declined signature, and a text test on R5's ask. A manual receipt: the install from the tag reads 0.22.2. | The test that holds `g1.py`'s `Ready:` reader equal to the tree's, replaced by the one reader's tests. |

Every check stands in one unit; SC1.2 and SC4.1 moved to `s7-plain-request` at r12, and `s3-review`'s and `s5-start`'s tests for them stand. At r16 SC2.1, SC3.1, SC4.1 and SC5.2 move to `s8-honest-reads`, SC3.3 and SC5.1 to `s9-one-line-refusals`, and SC1.1 to `s10-words-and-folds`; each built unit keeps a check, and its tests for a moved check stand. At r19 `s8-honest-reads` joins SC2.1 and SC3.1 with `+`: a unit holds at most three sketch entries, and the two share one, since each holds G1 to what a tool checked. `s6-release` is the release unit of 0.20.0, `s7-plain-request` ships 0.22.1, and `s10-words-and-folds` ships 0.22.2.

### Order

The units are built in a line: `s1-lint`, `s2-model`, `s3-review`,
`s4-tree`, `s5-start`, `s6-release`.

- `s1-lint` is first. It opens with pass zero, USAGE's guide to G1 written under red marks, and it lays the base the rest stand on: `g1.py`, the record file, the declarations' readers and both commands.
- `s2-model` adds the component declaration record and G1.2 on that base.
- `s3-review` follows both, since its flow runs their two commands at R3 and R4.
- `s4-tree` follows the three rules: the tree prints what they read.
- `s5-start` follows the tree: the refusal reads the tree's G1 verdict.
- `s6-release` is last. It turns the red marks green, moves the versions and turns G1 on at the kit.
- `s7-plain-request` follows on main at kit 0.22.0 (r12): it changes `new`, G1.3's reader and two flows, and ships 0.22.1.
- `s8-honest-reads`, `s9-one-line-refusals` and `s10-words-and-folds` follow on main at kit 0.22.1 (r16), in a line. `s8-honest-reads` changes what the readers return and adds their refusals; `s9-one-line-refusals` then holds each reader's failure to one line; `s10-words-and-folds` is last, since it fixes the words of the lines both print, and it ships 0.22.2.

## Risks and cost

`[Engineer seat · authored]`

What can go wrong:

1. Spectral may not lint a plain JSON Schema file without a ruleset the kit writes, and prerequisite 8 depends on it. `s1-lint`'s live run settles it before that unit's test list is approved.
2. P gets no live run, and TLC's needs Java and `tla2tools.jar` on the build machine. A wrong reading of P's exit code would first show at a consumer.
3. Nothing but the flow's rule stops an agent from running `g1-record review`. The non-goal "no agent attests G1.3" holds as a rule of the flow, since no code can tell a person from an agent.
4. `s4-tree` changes `tree.py`, the kit's most pinned file: 20 tests pin its print or its code today, by the explorers' count. A fixture with G0 and G1 active and no declaration must keep reading `to do`.
5. `intake.md` has 495 characters free, and I9's sentence takes about 150. A second edit to intake in this feature would crowd the cap.
6. Four calls go past requirements r3: messages 6 and 7, I9's condition, the refusal on `done` and on a contract's close, and a review that names two revisions. The pair parks at intake until the PO seat's amendment carries them.
7. The requirements document holds no Gherkin block, so intake parks the pair until the PO seat adds one scenario for each of the 15 checks.
8. Turning G1 on at the kit refuses this feature's own last tasks unless its id joins the exempt list in the same commit.
9. The tree reads the two declarations and one record file a feature at every print, and the pane keeps no G1 reading. `s4-tree` measures the print on the kit's 20 features.
10. `{section}` in message 5 is text a person names, and nothing checks that the section exists.
11. `s7-plain-request` makes the kit's own tree show G1.3 `failed` for `glossary-alias-disjointness`, and a test that reads the kit's own tree may pin its line.
12. A G1.2 record of the two-file form counts as absent after 0.22.2, so a consumer's G1.2 reads `to do` until `g1-record model` runs again. CHANGELOG names it.
13. A consumer's G1.1 that read `done` on a pattern that matches no file, or with no `g1.schemas` key, reads `to do` after 0.22.2, and that feature's next `progress` call is refused. CHANGELOG names it.
14. A contract born of an escape skips G1, so an escape fix that adds behavior skips the review. The seat at intake's I5 sees the origin.
15. A config that cannot be read refuses every `progress` call, a repository with G0 alone included, until the file is mended.
16. TLC's trace module and the files P writes are read from their reference pages. `s8-honest-reads`'s live TLC run measures TLC's; P's stays open (risk 2).
17. The origins take about 85 of `intake.md`'s 113 free characters.

What it costs: six units over about six sessions, after two to three
sessions for the PO seat's amendment and intake. The agents cost 3.7
million tokens at document-split's recorded pace (3,648K over its six
units, each passing Two-Key in round 1), 4 to 5 million likely, and
about 300K more for each lost Two-Key round. The live runs need
Spectral, and Java with `tla2tools.jar`, on the build machine.

At r16: three units, about 2 to 3 million agent tokens at one round each
(`docs/session-metrics.md`: rs4 took 634K, rs1 to rs3 about 1.0 million
each), and 100K to 200K more for each lost round.

## Consult cases

`[Engineer seat · authored]`

| Case | Answer | Who was asked | What was decided |
| :-- | :-: | :-- | :-- |
| 1. An ambiguity in the requirements | yes | the PO seat, user, on 2026-10-07 | Five points, which the PO seat's amendment carries before intake: the counts of features done and of ready checks stand at 18 and 15; messages 6 and 7 join the five; I9 names G1 only where G1 is active for the feature; the refusal covers `done` and a contract's close beside `start`; a review names both revisions of a pair. |
| 2. More than one solution | yes | no second engineer; the engineer seat decided on options four read-only explorers laid out with their costs | The 13 shape calls of 2026-10-07, each recorded under Decisions and open questions. At r12 (2026-11-12), the refusal stands in `new` and not at I2, recorded there too. At r16 (2026-11-13), the seat ruled 37 edges, each on Claude's call, fix or leave. |
| 3. A solution unconventional to the codebase | yes | no second engineer; the engineer seat decided on options four read-only explorers laid out with their costs | The refusal makes the task list enforced, and a gate is active by feature. ADR 0038, written at intake, amends ADR 0031 for both. |
| 4. A change to a public contract: routes, a gateway definition, events, a schema | yes | no second engineer; the engineer seat decided on options four read-only explorers laid out with their costs | One new schema, two new commands and new config keys, each additive. No schema, command or message that stands today changes. At r12 (2026-11-12), `new` gains one refusal, message 8 with exit 1, for a feature G1 gates with no feature document, and G1.3 gains RS302; every other call reads as before. At r16 (2026-11-13): `lint` refuses a call with no `g1.schemas` (exit 2, where it exited 0); a G1.2 record's entry binds the model's folder; `new` gains `--origin`; the commands gain the refusals under The edges ruled at r16. No message changes its words. |

## Decisions and open questions

`[Engineer seat · authored]`

The engineer seat decided each answer on 2026-10-07, in kit session 84.
A shape call's number is its place among that session's 13.

- Q: Where do G1's rules run? A: In a new subcommand, `g1-check`, never inside `validate`: ready-green keeps meaning G0 alone (shape call 1).
- Q: What are G1's rule codes? A: A new prefix, `RS`, numbered by condition: six codes, each with one message, and a `to do` carries no code (shape call 2).
- Q: How does a condition take its status? A: `failed` when one of its rules reports; else `done` when everything it needs is present and current; else `to do`, listing nothing (shape call 3).
- Q: What gives the G1 verdict its status? A: The ratified roll-up of its three conditions, so a feature with no schema and no hard core reads G1 `doing` until its review is signed (shape call 4).
- Q: Where do a lint result, a model-check result and a review live? A: In one committed file a feature, `.sdlc/g1/{id}.yaml`, written by `g1-record` alone and bound to its inputs by their hashes (shape call 5).
- Q: How is a tool's result read? A: By its exit code: 0 passes. `{n}` counts what the linter reports at warning severity or above.
- Q: How does a person sign a review? A: The record carries the signer's name, seat, date and both revisions, with no new form of `Signed:` row. "No agent signs" is a rule of the flow (shape call 6).
- Q: Where do the declarations live? A: The component declaration record at `specs/components.yaml`, with a new schema at 1.0.0; the schema patterns and the pins in `.sdlc/config.yaml`. A person writes each, and each is required once G1 is active (shape call 7, ADR 0030).
- Q: What is the venue? A: A new flow, `/sdlc g1 {id}`, in its own file; intake's I9 names it where G1 is active for the feature (shape call 8).
- Q: How do the features already done read G1 inactive? A: Through the `g1.exempt` list; a feature not on it needs G1. The kit lists the features closed at the release and this feature; `glossary-alias-disjointness`, parked and not started, stays off it (shape call 9).
- Q: What does the refusal cover? A: `progress start` on a task, and `progress done` on a task, a unit or a contract. `block` and `run` stay open (shape call 10).
- Q: Does CI change? A: No: no tool runs in the scaffolded workflow, and the refusal is the enforcement (shape call 11).
- Q: How many units, and which release? A: Six, as kit 0.20.0. SC4.3 stands in the release unit, since intake refuses a unit that delivers no check (shape call 12).
- Q: Does a feature before intake show G1? A: Yes: active and `to do` once G1 is on, as it shows G0 today.
- Q: Does the `sdlc-spec` agent definition ship? A: No: a conversation flow that a person signs is no authoring surface for an agent. The venue row for G1 in `docs/operators.md` moves to bound.
- Q: Does the kit review this feature under G1? A: No: it passed intake before G1 stood, and the requirements refuse a retroactive review.
- Q: Do the checks before signing read green? A: No, and each finding is answered: `component` and `venue` trip CL003, and the dictionary cedes both at intake, as requirements r2 says; `ready check` matches the ratified term `ready-check` (CL014), ratified after r3, and the PO seat maps it in the amendment.
- Q: What of the three stale facts in requirements r3? A: The design builds on today's: 18 features done, 15 ready checks, and the `gates/G0` line as kit 0.17.0 computes it. The PO seat amends the words.
- Q: Which ratified terms does this design change? A: Four, each amended at intake: Rule and Condition, for rules that read records; Active gate, for a feature's exemption; Review, for a pair's two revisions.
- Q: Which ADR carries this design? A: ADR 0038, written at intake: it amends ADR 0031's "shown and never enforced" for the refusal, and fixes the homes of the records and the declarations, which closes the deferrals of ADR 0007 and of G1's page.
- Q: What of the tests that pin this feature's own pair? A: Three tests of `tests/test_document_split_g1_pair.py` retire at this design's signature (shape call 13). The fourth, which holds the requirements document's hash, retires with the PO seat's amendment.
- Q: How does one G1.1 record hold the results of several linters? A: A call lints every `g1.schemas` entry with a schema in scope and appends one record whose `runs` list holds one run for each entry. The reader holds each schema to the run of its own entry. The engineer seat ruled it on 2026-10-09 (kit session 90) and the text row of 2026-10-17 (kit session 101) carries it.
- Q: What does G1.1 read for a contract whose scope cannot be read? A: `to do`, as G1.2 does, and `lint` refuses the call with exit 2. Kit session 88's `s1-lint` read `done` there: an escaped defect, fixed by the same text row.
- Q: Do the checks before signing read green for the text row of 2026-10-17? A: No, and each finding is answered: 14 CL014 findings, one for each term the state file copies from the requirements document. The user ratified all 14 word for word in kit session 86 (`8f9e9ed`), so each maps to its ratified term, and none stands in the amended text.
- Q: Where does the refusal of a feature with no feature document stand? A: In `new`, which intake's I3 already runs, and not in a new sentence at I2. The id is known there, the refusal is code a test can run, and `intake.md` keeps room under its cap. The engine's finding proposed I2; the engineer seat ruled `new` on 2026-11-12.
- Q: Why does G1.3 read `failed` and not `to do` with no document? A: `to do` reads as "not yet". The kit's own `glossary-alias-disjointness` read `to do` for 25 days with no way to `done` (ADR 0041, rule 4).
- Q: Which kit ships the fix? A: 0.22.1, a patch, as 0.21.1 shipped the team's fixes; `s7-plain-request` carries its release files.
- Q: Which kept readings does this row take (ADR 0041, rule 1)? A: Reading 3 of PR #112 alone. Left for Next 26's later rows, each with that reason: PR #112's readings 1, 2 and 4 to 12, PR #116's 1 to 15, and PR #119's 1 to 12.
- Q: Do the checks before signing read green for the text row of 2026-11-12? A: No, and each finding is answered: the same 14 CL014 findings as the text row of 2026-10-17, one for each copied term, each ratified in kit session 86. `s7-plain-request`'s Done means reads zero, reworded from five findings before its row was measured.
- Q: How were G1's open edges ruled? A: The engineer seat ruled 37 on 2026-11-13 (kit session 150), each on Claude's call. Fix where G1 can read `done`, or not active, for something it never checked, where a hand-written file ends a command on a traceback, or where shipped words stand in no source. Leave, and say so, where only an outside tool's live run would settle it, or the cost is a cosmetic print. 28 are fixed, 8 left, and 1 was found closed by `s4-tree` at the re-read before signing.
- Q: Which kept readings does r16 take (ADR 0041, rule 1)? A: Each of the 38 r12 left, and PR #162's seven. Two are overturned: PR #116's reading 12 and PR #119's reading 5, since the second build reads `g1.exempt`. A fix closes three: PR #119's readings 6, 7 and 9. One is an edge left: PR #116's reading 14. Seven record how a build ran and hold no design text: PR #112's reading 12 and PR #162's readings 1 to 6. PR #162's reading 7 is the ruling on an escape. The other 31 stand as built under The edges ruled at r16.
- Q: Why do the new units take existing checks? A: G1 holds five success criteria, the interview's limit, so a new check would make a second feature. `s7-plain-request` took two at r12 the same way.
- Q: Why is a pattern that matches no file a declaration that cannot be read, and not a `to do` of its own? A: A `to do` lists nothing, and the tree's problem line names the pattern and the way out. A repository with no schema yet declares `schemas: []`.
- Q: How does G1 skip a contract born of an escape or maintenance? A: Through the contract's `provenance.origin`, which I4 already chooses. `new` runs at I3, before I4, so `--origin` carries the origin to `new`'s refusal and into the scaffold.
- Q: How does I9 agree with the kit's reader with no fifth command (constraint 11)? A: `new` reads the config at I3 with the kit's reader and refuses one it cannot read, so I9 reads only a config the kit reads.
- Q: Why the backslash escape, and not UTF-8, for each command's output? A: It keeps every byte of a line that prints today (constraint 1), as the print has since `s4-tree`.
- Q: Which kit ships the fixes? A: 0.22.2, a patch, as 0.22.1 shipped `s7-plain-request`'s; `s10-words-and-folds` carries the release files.
- Q: Do the checks before signing read green for the text row of 2026-11-13? A: No, and each finding is answered: the same 14 CL014 findings as the text row of 2026-10-17, one for each copied term, each ratified in kit session 86. The three new Done means read zero, reworded from nine findings before the row was measured.

## Traceability

### Links out

`[Engineer seat · authored]`

- `docs/features/g1-requirements-spec.md`: the requirements, at r3.
- `docs/gates/G1-requirements-spec.md`: G1's page, with its three conditions and the 11 items.
- ADR 0007: the hard-core criteria.
- ADRs 0020 and 0021: a check is a `taskcontract` subcommand that speaks the verdict contract.
- ADR 0030: a door's input is a declaration.
- ADR 0031: the tree and the progress record. ADR 0032: conditions and their rules.
- ADRs 0029, 0033, 0034, 0036 and 0037: this document's format and its signature.
- `docs/operators.md`: the venue map and the conformance table.
- The pilot's finding `intake-exit-names-no-successor-venue`, in the engine's `PILOT-NOTES.md`.
- ADR 0038, to be written at intake.

### Record

`[Intake · derived]`

(none: intake writes the record)

## Notes

`[Engineer seat · authored]`

Written in kit session 84 (2026-10-07) through
`/sdlc:product-specification-interview g1-requirements-spec design` on
kit 0.19.0's flows. The engineer seat answered in five batches of
proposed text, and Claude typed each on the user's word. Four read-only
explorers mapped the kit first; their four files stand untracked in the
kit's root, under `RECEIPT_g1-requirements-spec-design_2026-10-07/`.

Before intake the PO seat amends the requirements document: the three
stale facts, the five points of consult case 1, the Review and Ready
check terms, and one Gherkin scenario for each of the 15 checks. The
engineer seat then confirms this design against the new revision and
signs again.

The run's state file held its copy of the terms as a mapping until this
session, a shape the draft check reads as no term. It holds the list
now.

## Appendix

### Contract

`[Intake · derived]`

(none: intake writes `specs/g1-requirements-spec/contract.yaml`)
