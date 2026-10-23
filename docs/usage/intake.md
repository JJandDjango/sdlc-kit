### `/sdlc intake` — the G0 venue
Give it a raw request ("add CSV export"). 🟢 Intake first checks for a
ratified seat term (§8); with none, it stops before authoring and names
the file to author and the command that drafts it (kit 0.14.0). The
agent authors `specs/<task-id>/contract.yaml` — intent, scope,
non-goals, decomposition with a done-meaning and 1–3 acceptance-sketch
criteria per unit, dependencies, entities, provenance — then loops

```bash
python -m taskcontract validate specs/<task-id>/contract.yaml --profile ready
```

until green, and refuses the handoff to spec/implementation while red.
A blocked dependency parks the contract as a valid `draft`; `ready` is
what gates entry into development. 🟢 Intake also takes a human answer
per unit and records it under `confirmed_by` before the contract lands
(kit 0.12.0).

### What `ready` requires — two declarations 🟢

> 🟢 **Shipped** (kit 0.14.0, [ADR 0030](../../decisions/0030-a-doors-input-is-a-declaration.md),
> contract `specs/g0-declaration/`, schema 1.4.0).

🟢 At the `ready` profile, the input a door reads is required, so a green
G0 means every condition checked something. A contract carries
`entities:`, the glossary terms it operates on (§5). An empty list is valid
and is a statement: `entities: []` says the contract operates on no
glossary term. A contract with no field fails `TC017`. `/sdlc intake`
always writes the field, and writes `[]` only on the PO seat's confirmed
answer; `taskcontract new` names the field in a comment and sets no value.

🟢 Inside a specs tree, a ratified `intake-seat` (§8) must exist before any
contract reaches `ready`. With the term absent or at draft, every contract
fails `TC018`, and the diagnostic names the file to author:
`specs/vocabulary/intake-seat.yaml` (`/sdlc vocab add intake-seat` drafts
it; ratifying it is yours). Intake checks this first and stops before
authoring. Greenfield `/sdlc init` asks who holds the seats and seeds the
term ratified; brownfield `/sdlc init` ends its report with a note naming
the same command while the term is not ratified. A repo with one human
ratifies a one-value roster. The `draft` profile is unchanged: a parked
contract may carry neither.

🟢 **Adopting on an existing repo needs no re-intake.** The session hook
protects only a contract that validates `ready`, so a contract the new
doors fail is open to the edits that repair it. After the upgrade, a
`ready` contract with no `entities:` fails `TC017`, and in a repo with no
ratified roster it fails `TC018` too. Add the field. Ratify
`intake-seat`, and each contract fails `TC016` until its units carry
`confirmed_by`; stamp the answers. A contract locks again only when it
passes both doors, so adding `entities:` locks it on its own only where
the roster is already ratified and its units already carry answers.
Install the kit by pinned tag (§7, "Kit → your repo"), so an upgrade is a
choice, never a surprise.
