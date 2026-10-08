| Revision Date | Revised By | Changes Made |
| :-: | :-: | :-- |
| 2026-10-07 | user | r1: Created through /sdlc:product-specification-interview. The design, in progress, against requirements r3. Engineer seat: user |
| 2026-10-07 | user | r2: Measured: the checks before signing, on the solution half: 3 findings (CL003 2, CL014 1); Scope against the release unit's paths: covered; ready checks 11 to 15: 0 OPEN |
| 2026-10-07 | user | r3: The solution half finished: 12 sections written, 0 OPEN |
| 2026-10-07 | user | r4: Signed: solution half. The engineer seat signs r3 |
| 2026-10-08 | user | r5: Confirmed against requirements r6 |
| 2026-10-08 | user | r6: Signed: solution half. The engineer seat signs r5 |

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

The skill:

- `skills/sdlc/flows/g1.md` (new): the venue.
- `skills/sdlc/SKILL.md`: the dispatch line, the flow list, one constraint, one criterion.
- `skills/sdlc/flows/intake.md`: one sentence at I9.
- `skills/sdlc/init.py`: `KIT_VERSION`.
- `skills/sdlc/templates/SDLC.md.template` and `skills/sdlc/templates/specs-README.md.template`.

The release and the pages:

- `pyproject.toml`: the version.
- `tests/`: each unit's tests, and the retirements Units names.
- `USAGE.md`, `CHANGELOG.md`, `MAP.md` and `SDLC.md`.
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
- `skills/sdlc/flows/intake.md`, steps I1 to I8.
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

- With no boundary schema in scope, `lint` prints `G1.1: no boundary schema in scope`, writes nothing and exits 0.
- With no hard core in scope, `model` prints `G1.2: no hard core in scope`, writes nothing and exits 0.
- A tool that is not installed is recorded as such, so the condition reads `failed`; the call prints message 1 or 3 and exits 1.
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
| G1.1 | `g1.schemas` is absent; or a schema in scope has no lint record that matches its hash and the pin's | no schema is in scope; or every schema in scope is recorded clean |
| G1.2 | `specs/components.yaml` is absent; or a hard core in scope has a model with no record that matches its hash and its configuration's | no hard core is in scope; or every one is recorded as passing |
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
    tool: spectral
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
- A G1.2 record holds one entry per hard core: the component, the tool, the model's and the configuration's hashes, and `pass` or `fail`.
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
done with G1 not passed. An exempt feature is never refused.

**Intake's report.** I9 gains one sentence. For a ready-green contract
whose feature needs G1, the report ends:

```
Next step: G1. Run /sdlc g1 apply-discount.
```

With `G1` absent from `active_gates`, or the feature exempt, the report
ends as today.

### Sources

| Fact | Read from | When two disagree |
| :-- | :-- | :-- |
| Whether G1 is active for a feature, and which features are already done | `.sdlc/config.yaml`: `G1` under `active_gates`, and the `g1.exempt` list | The exempt list wins for a feature it names, and it wins over a contract's close record, which is local and uncommitted. |
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
10. Each prompt file the build touches passes `python -m prompt_lang`, keeps the PromptLang tag set and stays under 12,000 characters. `intake.md` has 495 characters free.
11. Intake keeps I1 to I9 and their order, and I9's sentence names no fifth `python -m taskcontract` command.
12. The 13 question sentences of ready checks 1 to 8 and 11 to 15 stand in no G1 file.
13. G1.3's 11 items stay as ratified, and no agent signs a review: the flow runs the writer only on the person's word.
14. Every authored command is one segment: no pipe, no chain, no redirect.
15. In USAGE a red sentence stands under its own red subsection, and a new drawing in section 9 follows the pinned ones.

### Units

| Unit | Checks | Done means | Tests by check id and kind | Retirements |
| :-- | :-- | :-- | :-- | :-- |
| s1-lint | SC2.1, SC2.2, SC2.3 | With a boundary schema in a feature's scope, G1.1 reads done only when the pinned linter's record shows it clean. | SC2.1: automated, with a stand-in linter, and a manual receipt, a live Spectral run on one clean file and one unclean file. SC2.2: automated. SC2.3: automated. | USAGE's red-legend test, at pass zero (`tests/test_document_split_release.py:517-527`). The two tests that hold `rules:` to G0's conditions (`tests/test_tree_conditions.py:313-327` and `432-442`), each replaced by one that holds G1's too. |
| s2-model | SC3.1, SC3.2, SC3.3 | With a hard core in a feature's scope, G1.2 reads done only when the record shows its model passes the checker. | SC3.1: automated, with a stand-in checker, and a manual receipt, a live TLC run on one passing model and one failing model. SC3.2: automated. SC3.3: automated. | none |
| s3-review | SC1.1, SC1.2, SC1.3 | A seat reads G1.3's 11 items at the venue, and G1.3 reads done only from a review with a signature. | SC1.1: automated, and a manual receipt, a live run of `/sdlc g1` on an invented feature with a seat answering the 11 items. SC1.2: automated. SC1.3: automated, a text test on G1's flow, the interview and intake. | none |
| s4-tree | SC5.1, SC5.2, SC5.3 | The tree shows G1 as an active gate where a feature needs it, with each condition's status, diagnostics and review. | SC5.1: automated. SC5.2: automated. SC5.3: automated. | The sha256 pin on `tree.py`'s code (`tests/test_document_split_release.py:483-490`); the docstring's sentence order, pinned at line 487, stays. |
| s5-start | SC4.1, SC4.2 | Intake's report names G1 as the next step, and no unit's task reads done before its feature's G1 passes. | SC4.1: automated, a text test on I9, and a manual receipt, a live intake run whose report ends on the G1 line. SC4.2: automated. | Two sentences that say no task is enforced, each reworded: `tasks.yaml`'s header comment and USAGE's "shown and never enforced". No test pins either. |
| s6-release | SC4.3 | Kit 0.20.0 ships G1 with its documentation, and the kit's own tree shows G1 as an active gate with G0 unchanged. | SC4.3: automated, on a fixture and on the kit's own tree. Two manual receipts: the install from the tag reads 0.20.0, and Spectral lints the kit's four schemas under `.spectral.yaml`. | Section 9's banner test (`tests/test_document_split_release.py:530-545`), replaced. USAGE's drawing of this feature before intake (`USAGE.md:1640-1655`), redrawn on an invented feature. |

Every check stands in one unit. `s6-release` is the release unit.

### Order

The units are built in a line: `s1-lint`, `s2-model`, `s3-review`,
`s4-tree`, `s5-start`, `s6-release`.

- `s1-lint` is first. It opens with pass zero, USAGE's guide to G1 written under red marks, and it lays the base the rest stand on: `g1.py`, the record file, the declarations' readers and both commands.
- `s2-model` adds the component declaration record and G1.2 on that base.
- `s3-review` follows both, since its flow runs their two commands at R3 and R4.
- `s4-tree` follows the three rules: the tree prints what they read.
- `s5-start` follows the tree: the refusal reads the tree's G1 verdict.
- `s6-release` is last. It turns the red marks green, moves the versions and turns G1 on at the kit.

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

What it costs: six units over about six sessions, after two to three
sessions for the PO seat's amendment and intake. The agents cost 3.7
million tokens at document-split's recorded pace (3,648K over its six
units, each passing Two-Key in round 1), 4 to 5 million likely, and
about 300K more for each lost Two-Key round. The live runs need
Spectral, and Java with `tla2tools.jar`, on the build machine.

## Consult cases

`[Engineer seat · authored]`

| Case | Answer | Who was asked | What was decided |
| :-- | :-: | :-- | :-- |
| 1. An ambiguity in the requirements | yes | the PO seat, user, on 2026-10-07 | Five points, which the PO seat's amendment carries before intake: the counts of features done and of ready checks stand at 18 and 15; messages 6 and 7 join the five; I9 names G1 only where G1 is active for the feature; the refusal covers `done` and a contract's close beside `start`; a review names both revisions of a pair. |
| 2. More than one solution | yes | no second engineer; the engineer seat decided on options four read-only explorers laid out with their costs | The 13 shape calls of 2026-10-07, each recorded under Decisions and open questions. |
| 3. A solution unconventional to the codebase | yes | no second engineer; the engineer seat decided on options four read-only explorers laid out with their costs | The refusal makes the task list enforced, and a gate is active by feature. ADR 0038, written at intake, amends ADR 0031 for both. |
| 4. A change to a public contract: routes, a gateway definition, events, a schema | yes | no second engineer; the engineer seat decided on options four read-only explorers laid out with their costs | One new schema, two new commands and new config keys, each additive. No schema, command or message that stands today changes. |

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
