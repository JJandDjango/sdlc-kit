# 6. Encode task-contract enforcement: schema, validator, wiring

Status: accepted
Date: 2026-07-23

## Context
ADR 0005 fixed G0.1's field set but left schema encoding, validator
tooling, and harness wiring open ("enforcement-pass work"). Session 4's
user directive pulled that pass forward; walked through interactively and
ratified stop by stop (2026-07-23).

## Decision
- **Encoding:** JSON Schema Draft 2020-12 over YAML/JSON instances,
  `schemas/task-contract.schema.json`. E1: `acceptance_sketch` nests inside
  each decomposition unit (cross-array correspondence is inexpressible;
  0005's logical field set unchanged). E2: two profiles in one file - root
  = `draft` (admits `status: blocked` + `blocked_by`), `$defs/ready` adds
  all-dependencies-resolved; G0.1 gates on `ready`. E3: provenance is
  `{origin, ref}`, `ref` required for `g8-escape` (ratified delta over
  0005). E4: `additionalProperties: false` throughout. E5: contracts live
  at `specs/<task-id>/contract.yaml` - `specs/**` becomes the single
  protected root feeding G4.6/Q1. Tunable: P1 id `^[a-z][a-z0-9-]{2,63}$`
  (revisit at the REQ-ID ADR), P2 intent 40-1200 chars.
- **Validator:** house package `taskcontract` (foundations pattern), thin
  over installed python-jsonschema: `python -m taskcontract validate
  <files> [--profile ready|draft] [--json]`, stable TC000-TC009 rule ids,
  per-field lines enriched with instance data. check-jsonschema (generic
  diagnostics miss the loopability bar) and ajv-cli (Node toolchain)
  rejected.
- **Wiring:** the gate is the harness intake step (`/intake` loop,
  deferred to the pilot, Q6); pre-commit + CI validate committed
  `specs/**` as backstops only. Kept set: build F1-F3/F7/F9 (schema,
  validator, fixtures + pytest, pyproject, kit CI); document F8/F12
  (consumer snippets); defer F10 (`/intake`), F11 (scaffold).

## Consequences
- G0.1 stays `specified` (venue pending) but drops "(human until schema
  exists)" and gains the near-final check shape in the registry.
- The enforcement layer carries its own regression suite - golden fixtures
  (first: this task's own contract, dogfood) + kit CI - per PL-PIPE.2.
