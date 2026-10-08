# 38. A gate refuses a task, and G1's records and declarations have homes

Status: accepted
Date: 2026-10-08

## Context

G1's page holds three conditions: spec and schema linting (G1.1), model
checking (G1.2) and a person's review against 11 items (G1.3), the list
ratified on 2026-07-23. It left their enforcement open. ADR 0007
deferred where a hard core's designation is recorded, and the page
deferred the review's form, its storage and its sign-off record. Kit
0.16.0 listed the three conditions in `taskcontract/data/gates.yaml`
with no rule under them, so no G1 condition takes a status. The pilot's
finding
`intake-exit-names-no-successor-venue` says no venue is bound between
intake and a unit's first test list.

The request is the pair `docs/features/g1-requirements-spec.md` and
`docs/features/g1-requirements-spec.design.md`. The PO seat signed the
requirements at r6, and the engineer seat confirmed the design against
r6 and signed it, both on 2026-10-08. The design's consult case 3 and
its Decisions name this ADR and what it carries.

Bound by: the progress file is local and never a gate input (0024,
0031); no committed plan (0027); a door's input is a declaration (0030);
the tree computed at print (0031); every code belongs to one condition
(0032); a gate item reads the roll-up of its features' verdicts (0035);
the seats (0025); the hard-core criteria (0007); and the contract
schema, which the feature leaves at 1.5.0.

Alternatives rejected: G1's rules inside `validate` (ready-green would
stop meaning G0 alone for the tree, the write guard, the audit, CI and
pre-commit); a tool run in CI (the kit ships and installs no linter and
no checker, so the refusal is the enforcement); a G1 record under
`.sdlc/progress/` (that file is local, and no gate reads it); a new form
of `Signed:` row for a review (the record holds the signer, the seat,
the date and the revisions); a designation in the contract (the schema
stays at 1.5.0); a review of the features already done (the
requirements refuse it); an agent's signature on a review.

## Decision

- **A gate may refuse a task.** `progress start` on a task, and
  `progress done` on a task, a unit or a contract, refuse while the
  feature's G1 is active and not `done`. The line goes to stderr, and
  the call exits 2 and writes nothing: `{unit} cannot start: G1 has not
  passed for {feature}`, with the feature's id in the unit's place on a
  contract's close. `block` and `run` stay open. The refusal reads the
  feature's G1 verdict in the tree that `progress` builds on that call,
  so the refusal and the tree give one reading. It is a refusal of
  `progress` and no rule's.
- **A gate is active by feature.** G1 is active for a feature when
  `.sdlc/config.yaml` lists `G1` under `active_gates` and its
  `g1.exempt` list does not name the feature. The exempt list wins for a
  feature it names, and it wins over a contract's close record. `exempt`
  absent means no feature is exempt. An exempt feature's lines keep
  every byte: G0, then G1 `[to do] inactive`, and it is never refused. A
  feature that needs G1 shows it active, with G2 as the inactive next
  gate, and a feature before intake that is not exempt shows G1 active
  and `to do`. A new repository is born with G0 alone.
- **G1's rules read records, in their own command.** `g1-check` runs six
  rules with the prefix `RS`, numbered by condition and listed under
  `rules:` in `gates.yaml`. It runs no tool and writes nothing. No G1
  rule reports through `validate`: ready-green keeps meaning G0 alone. A
  condition reads `failed` when one of its rules reports; else `done`
  when everything it needs is present and current; else `to do`, listing
  nothing. G1's verdict is the roll-up of its three conditions, as the
  ratified Roll-up term reads.
- **G1's records stand in one committed file a feature**,
  `.sdlc/g1/{id}.yaml`, written by `g1-record` alone. Each call appends
  one record, and the last record of a condition counts. A lint record
  or a model-check record is bound to its inputs by their hashes: each
  file's, and the pin's or the model configuration's. A record whose
  hashes no longer match counts as absent. A review record holds the
  signer's name, the seat, the date and one revision for each document
  the contract was derived from, and it counts while those revisions
  match the `Ready:` rows. A person signs a review. An agent may draft a
  reading of an item; it never answers one and never signs.
- **A person writes the declarations, in two homes.** The component
  declaration record is `specs/components.yaml`, under a new schema at
  version 1.0.0: each component's paths, whether it is a hard core, its
  oracle designation, and a hard core's model and checker. The boundary
  schema patterns, each with its linter and pin, stand under the `g1`
  key of `.sdlc/config.yaml`, beside the exempt list. Each is required
  once G1 is active: absent reads `to do`, and an empty list says none.
  No flow writes a declaration.

This amends 0031: "every unit follows one task list, shown and never
enforced" holds but for the refusal, which stands before a task's start
and before a done. The tree reads more sources: the records under
`.sdlc/g1/`, `specs/components.yaml`, and the files those records hash.
It stores nothing and runs no tool. The
progress file stays local, and no gate reads it (0024): the refusal is
`progress` reading the tree. It amends 0031 and 0032: "its verdict at
every active gate" and "each feature shows its active gates" are read
by feature. 0032's rule holds for the six `RS` codes: each belongs to
one condition. It closes two deferrals: 0007's, on where a designation
is recorded, and those of G1's page, on the recording venue of the
per-component set and on the review's form, storage and sign-off
record.

Recorded non-goals: no change to `validate`, to its output or to what
ready-green means; no change to CI or to the scaffolded workflow; no
linter and no checker shipped or installed by the kit; no change to the
contract schema; no G1 record under `.sdlc/progress/`; no review of a
feature already done; no change to G1.3's 11 items; no `sdlc-spec`
agent definition.

## Consequences

- `g1-requirements-spec` carries the change in six units, `s1-lint` to
  `s6-release`, as kit 0.20.0. Until its units ship, G1 reads as today
  and no task is refused.
- G1 gains a venue: a new flow, `/sdlc g1 {id}`, runs after intake and
  before a unit's first task, and intake's report names it where G1 is
  active for the feature. This answers the pilot's finding.
- The kit turns G1 on for itself in the release unit. Its exempt list
  names the features closed at that release and this feature, which
  passed intake before G1 stood.
- The pilot pins the release that carries G1 and writes its own two
  declarations.
- Harder: a person writes two declarations before G1 can read `done`;
  the record file changes in git with each run of `g1-record`; a
  re-intake at a later revision needs a new review; and a session that
  skips the venue stops at its first `progress start`.
