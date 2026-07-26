# 14. Enforcement-layer change control: two lanes, one ledger, human ground

Status: accepted
Date: 2026-07-26

## Context

Q7: the workflow behind PL-PIPE.1 - who approves class-E deltas, how
routing is decided, how approval is recorded. Already fixed: the
mechanical arm (0010 - G4.6 diff audit, born-protected manifest,
channel provenance) and four direction-conditional instances on
record (0010/G4.8 channel weight, 0012 clock moves, G9.3 allowlist
exceptions, 0013 sunset-date moves). Forced at the S12 walk, stop 5.

## Decision

- **Two lanes, routed mechanically.** A committed direction
  classifier (per-artifact-class field-wise rules) routes every
  class-E delta: tightening auto-approves; loosening takes the full
  lane. **Undecidable direction = loosening** (G10.3's polarity
  transposed) - artifacts with no field-wise direction (CI
  workflows, rulesets-as-code, agent prompts) always take the full
  lane.
- **The full lane's approver is the human principal** - the sixth
  census seat. Every agent is inside the gated class, so no agent
  approves enforcement loosenings; decorrelation does not help
  here. Separation invariant: no single context both authors a
  class-E delta and mints its approval - harness-enforced (0010
  trust root), audit-verified.
- **One append-only approval ledger, hash-bound, total across
  lanes:** {delta path set + content hash, direction verdict + rule
  ref, lane, approver (full lane), rationale, date}. Hash binding
  kills approve-then-swap; auto-lane records are minted by the
  classifier; G4.6 joins diff <-> record at merge, missing or
  incomplete = red. Records supersede, never mutate.
- **The meta-layer always takes the full lane:** the classifier
  config, the write-surface manifest, the ledger schema, the clocks
  artifact's structure, and this workflow itself never auto-approve,
  even tightening. Auto-approval can never widen auto-approval.
- **Revert-to-approved rides the auto lane:** restoring a class-E
  artifact to a state whose hash the ledger already approved is
  backward motion to known ground, hash-decidable. No forward
  break-glass lane exists - stop-the-line is the philosophy (0012).
- **Scope is the manifest** (born-protected polarity), seeded with
  the consolidated census: gate/CI definitions, analyzer rulesets +
  severity configs, agent prompts, the registry, environment
  definition, monitoring/alert/derivation configs, rollout policy,
  chaos plan, clocks.yaml, the allowlist/suppression/quarantine
  set, trimmer root configs, flag schema, tightening-job config,
  doc-set config, sample-relaxation ruleset, dating config.

## Consequences

- PL-PIPE.1 `specified`; Q7 closes; the open-parameter index is
  Q4-only.
- Prompts structurally cannot ride the auto lane; PL-PIPE.3 adds
  the eval gate on the same subjects.
- Golden fixtures and eval scenarios become tamper-evident: edits
  toward green are loosenings and take the full lane.
- Build items riding Q6: the direction classifier + the approval
  ledger (the write-surface audit job gains the join).
