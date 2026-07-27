# specs/ - the protected root

Task contracts live at `specs/<task-id>/contract.yaml` - one per task,
authored at intake (G0), **immutable to implementers** once ready: the
write-surface rule permits implementation diffs to touch everything
*except* `specs/**` (SDLC kit ADR 0010, allowlist form).

- Scaffold: `python -m taskcontract new <task-id>`
- The gate: `python -m taskcontract validate specs/<task-id>/contract.yaml --profile ready`
- A blocked dependency parks a contract as a legal `draft`; `ready` is
  what admits the task into development.

Later spec artifacts - G1 acceptance criteria, locked API baselines,
`.approved.*` files - join this same protected root.
