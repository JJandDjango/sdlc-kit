# Task contract - schema, validator, wiring (G0 enforcement)

<!-- covers: decisions/0006-task-contract-enforcement.md -->

> **Contract** - one question: *how is G0.1 mechanically checked?*
> Component deep page (MAP row: task-contract schema). Spec baseline:
> [gates/G0-planning-intake.md](gates/G0-planning-intake.md) +
> [0005](../decisions/0005-task-contract-fields.md); encoding, validator and
> wiring ratified 2026-07-23 in
> [0006](../decisions/0006-task-contract-enforcement.md) after an
> interactive three-stop walk-through (session 4).

## G0.1 as mechanical clauses

The 8-field set is fixed by 0005 (field table lives on the G0 page - not
duplicated here); [0017](../decisions/0017-vocabulary-layer.md) V2 amends
it with one optional field, `entities:` - unique term-slug refs; and
[0024](../decisions/0024-unit-dependency-graph.md) amends the unit shape
with a required `id` and an optional `depends_on`. Schema
`version: 1.2.0`. Every pass-condition clause maps to vanilla JSON Schema
Draft 2020-12:

| G0.1 clause | Schema encoding |
|---|---|
| all fields present, non-empty | `required` + `minLength: 1` / `minItems: 1` |
| `scope`, `non_goals` each >=1 entry | `minItems: 1` |
| `decomposition` >=1 unit, each with a done-meaning | object array, `minItems: 1`; unit requires `done_means` |
| 1-3 sketch criteria per unit | `minItems: 1, maxItems: 3` nested in the unit (E1) |
| every unit identified | unit requires `id`, same pattern as the contract id (0024) |
| unit order declared | optional `depends_on`: unique array of unit ids (0024) |
| the order is a graph, not a list | *not schema* - TC013-TC015, Python-side (0024) |
| dependency `resolved` / `blocked-by: <ref>` | item object + `if/then` (E2) |
| all dependencies resolved to pass | `ready` profile: `status: const resolved` (E2) |
| `provenance` origin fixed | enum; `ref` required on escape (E3) |
| no stray fields | `additionalProperties: false` (E4) |

**The boundary:** the schema checks that the *witness exists* - a sketch is
written, a done-meaning is stated - never that it is *good*. Goodness stays
human, concentrated at G1.3. The intent length bounds are a proxy: they
catch the empty and the essay, not the off-topic.

Two rule families live outside the schema, both Python's half of the
two-layer split. The **unit graph** (0024) runs in *both* profiles: ids
must be unique (TC013), every `depends_on` entry must name a unit of the
same contract (TC014), and the graph must be acyclic (TC015). JSON Schema
can express neither reference resolution nor acyclicity, and a cycle is
malformed rather than merely unready, so draft catches it too. Isolated
units are valid - parallel work is the point, so nothing checks
connectivity.

The other is ready-profile only: the **coverage join**
(0017 V3) - when a contract at `specs/<id>/contract.yaml` declares
`entities:`, each ref must resolve to a *ratified* term in the sibling
`specs/vocabulary/`. That is a cross-file join, Python's half of the
two-layer split ([0008](../decisions/0008-two-layer-condition-model.md)):
schema at the door, joins at the ledger. Loose files (fixtures, ad-hoc
paths) never enter the join.

## Ratified decisions (0006)

- **E1** `acceptance_sketch` nests inside each decomposition unit - vanilla
  JSON Schema cannot check correspondence across parallel top-level arrays.
  Unit shape: `{unit, done_means, acceptance_sketch}`, all required.
  **Amended by [0024](../decisions/0024-unit-dependency-graph.md):** the
  shape is now `{id, unit, done_means, acceptance_sketch}` plus optional
  `depends_on`. E1 originally ruled *no per-unit id* because
  [0011](../decisions/0011-criterion-traceability-format.md) needed none -
  criteria carry `REQ-<task>-<nnn>` and cite units by name (G1.3 item 3).
  That held while nothing referenced a unit; `depends_on` is the first
  thing that does, and a reference needs a referent that outlives an edit
  to the prose. 0011's format is unchanged.
- **E2** one schema file, two profiles: root = `draft` (a parked contract
  with a blocked dependency is representable, per 0005's own grammar);
  `$defs/ready` = draft + every `status: resolved`. The gate checks `ready`.
  Dependency item `{ref, status: resolved|blocked, blocked_by}` -
  `blocked_by` required iff blocked, forbidden iff resolved.
  `dependencies: []` is legal and vacuously ready.
- **E3** provenance `{origin: human-request|g8-escape|g9-maintenance, ref}` -
  `ref` required when origin is `g8-escape`: the convergence loop is
  auditable only if an escape-born task names its incident.
- **E4** `additionalProperties: false` - an unknown key in an immutable spec
  artifact is a typo or scope smuggling; both fail loudly.
- **E5** contracts live at `specs/<task-id>/contract.yaml`. One protected
  root - `specs/**` - later covers every spec artifact (G1 criteria,
  baselines, `.approved.*`), collapsing G4.6's protected-path enumeration to
  a single rule - the shape Q1 then ratified
  ([0010](../decisions/0010-write-surface-immutability.md), allowlist
  form).
- **P1** id pattern `^[a-z][a-z0-9-]{2,63}$`; **P2** intent 40-1200 chars.
  Tunable defaults - nothing downstream hardens on them yet.

## Survey record - why these tools

- **In-house:** the foundations repo (`E:\foundations`) supplies the house
  validator pattern - small package, `python -m <tool>` entry, packaged
  defaults with per-repo override, pip-installable consumer model, and the
  enforcement ramp *ships advisory, tightens to gating* (`theory`
  commit-msg hook; `codestandard` CI gate). Cairn's `audit.py` is the
  report-only-exit-1 audit shape. This repo had no enforcement code before
  this pass.
- **Off-the-shelf:** python-jsonschema 4.26.0 + PyYAML 6.0.3 were already
  installed - zero new dependencies. `check-jsonschema` works as a zero-code
  interim but was rejected as terminal state: generic messages miss G0.1's
  loopability bar, no draft/ready semantics, nowhere to grow intake wiring.
  `ajv-cli` rejected: a Node toolchain for speed this workload never needs.

## The validator

`python -m taskcontract validate <file...> [--profile ready|draft] [--json]
[--schema PATH]` - exit 0 clean / 1 violations / 2 usage. One line per
violation:

```
specs/add-csv-export/contract.yaml: $.dependencies[1].status: TC003 dependency 'schema-migration' unresolved (blocked-by: auth-rework)
```

The wrapper is thin: the schema file is the single source of truth for every
rule; the package only reshapes raw jsonschema errors and enriches them with
instance data (*which* dependency, *which* unit). `--json` emits the same
violations as an array - the agent loop substrate.

| Rule | Meaning |
|---|---|
| TC000 | unreadable file / YAML parse error |
| TC001 | missing required field |
| TC002 | empty or malformed field |
| TC003 | dependency unresolved (names ref + blocker) |
| TC004 | acceptance_sketch count out of 1-3 |
| TC005 | unknown field |
| TC006 | id pattern mismatch |
| TC007 | intent length out of bounds |
| TC008 | malformed dependency entry |
| TC009 | provenance origin invalid / escape missing ref |
| TC010 | entities ref names no vocabulary term (fork the vocab task) |
| TC011 | entities ref not ratified - draft does not resolve |
| TC012 | entities ref deprecated past its sunset |
| TC013 | duplicate unit id (names the first occurrence) |
| TC014 | `depends_on` names no unit in this contract |
| TC015 | dependency cycle (names the ring, spelled "depends on") |
| W001 | entities ref deprecated inside its sunset window (warning - never gates) |

Regression suite: golden fixtures `tests/fixtures/{valid,invalid}/*.yaml` -
every invalid fixture is named for the rule it must trigger; the first valid
fixture is this enforcement task's own contract (dogfood). The enforcement
layer carries its own regression suite (THEORY; PL-PIPE.2 in spirit), run by
kit CI on every push.

## The graph command

`python -m taskcontract graph <file>` renders one contract's unit graph as
Mermaid on stdout - exit 0 clean / 1 unreadable file. Nodes are declared
before edges, so a unit with no links still draws; edges run
**dependency --> dependent**, which is execution order, so the arrow
points the way the work flows rather than the way `depends_on` is written.

Rendering never gates: graph violations go to *stderr* and the exit code
stays 0, because seeing a cycle drawn is how an author fixes it.
`validate` remains the door. The render is computed on demand and never
committed ([0024](../decisions/0024-unit-dependency-graph.md), following
0017 V5's stored-index refusal): the graph is a function of the contract,
so a committed copy would be a second truth needing its own drift check.
Output is byte-identical across runs - no ordering depends on set or dict
iteration - which is what lets a non-interactive caller diff it.

## Wiring - venue precision

1. **Intake loop - the G0 venue.** `/sdlc intake`
   ([0016](../decisions/0016-distribution-before-activation.md),
   `skills/sdlc/SKILL.md`): the agent authors the contract from the raw
   request onto a `taskcontract new` scaffold, loops `validate --profile
   ready` to green, writes `specs/<id>/contract.yaml`, refuses the
   spec-stage handoff while red. *This venue running live in a repo is
   what flips G0.1 to `enforced` there* - the first such repo is the Q6
   pilot.
2. **Repo backstop - pre-commit (consumer snippet, F8):**

   ```yaml
   - repo: local
     hooks:
       - id: taskcontract
         name: task-contract ready check
         entry: python -m taskcontract validate
         language: system
         files: ^specs/.*/contract\.yaml$
   ```

3. **CI backstop (consumer snippet):** after `pip install -e
   <path-to-this-kit>`, add a step `python -m taskcontract validate
   specs/*/contract.yaml` (once a `specs/` tree exists). Backstops are
   conformance checks on committed artifacts - they are not G0 itself.

**Editor freebie (F12):** VS Code `settings.json` -

```json
"yaml.schemas": {
  "./taskcontract/schemas/task-contract.schema.json": "specs/*/contract.yaml"
}
```

External tools can validate the *draft* profile directly
(`check-jsonschema --schemafile taskcontract/schemas/task-contract.schema.json ...`);
the `ready` profile needs the house CLI, which composes root +
`$defs/ready_delta`.

## Lifecycle

G0.1 stays `specified` kit-side: `enforced` means live and blocking in its
venue, and the venue is per-target - it flips in a repo when `/sdlc intake`
is how tasks enter development there (first such repo = the Q6 pilot, per
[0016](../decisions/0016-distribution-before-activation.md)). F10 ships as
`/sdlc intake`, F11 as `python -m taskcontract new <id>` (a deliberately
red skeleton - TC007 trips until a real intent is authored); both ride the
`/sdlc` distribution skill.
