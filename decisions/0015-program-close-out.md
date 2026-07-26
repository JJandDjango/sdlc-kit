# 15. Program close-out: specification complete, the reds ledger, named residues

Status: accepted
Date: 2026-07-26

## Context

The S12 walk specified the last six conditions (PL-DOC.1-.3,
PL-PIPE.1-.3) and ran the program close-out audit over all 54:
the three S11-named patterns swept registry-wide (fail-closed
polarity, schema-incompleteness teeth, one-artifact-many-consumers),
the human census, taxonomy closure both directions, the
open-parameter index, and the build inventory.

## Decision

- **The ADR-0004 program is complete at the specification layer:**
  54/54 conditions `specified` across G0-G10 + PL-DOC + PL-PIPE,
  zero `registered`. What remains is activation (Q6 pilot) and
  numbers (Q4 - one clocks.yaml edit plus per-gate constants).
- **The standing-red ledger is named** (audit finding F3 - 0012's
  origin story repeating one level up): one class-E artifact,
  reference `reds.yaml`, holds every open standing red - minimal
  schema {id, condition ref, class, clock origin, window ref,
  status}. Consumers: G0 fix-lane admission, G4.9, G7 admission
  interlock 4, G9.4 disposition tracking, the 0012 `fixes`
  intersection. All arms query one artifact; none redeclare. The
  ledger join is a PL-PIPE.2 golden subject; the artifact rides Q6.
- **Named residues, accepted open-eyed:** G2.4 boundary sets and
  G4.2 rule sets gate *declared* sets with no declared-vs-detected
  cross-check (candidate detected side: environment-definition
  egress facts; revisit at pilot reality). Prose quality and
  conceptual-doc adequacy stay human (oracle-problem family,
  THEORY non-goal).
- **Census confirmed at six:** G1.3, G2.3, G6.1, G6.2, G8.3,
  PL-PIPE.1 - each with recorded non-delegability rationale; G2.3's
  made explicit this session (the Theory kernel's seat: an ADR
  records *why*, and reconciling authored intent is the accountable
  human's articulation; agents draft, the why-holder reviews).

## Consequences

- Registry counts flip to 54/54; the open-parameter index reduces
  to Q4.
- Taxonomy gains two rows: documentation staleness / context rot
  (ODC documentation - the one previously unused anchor) and
  enforcement-layer compromise (CWE-693), the latter anchoring G4's
  agent-self-weakening Closes line.
- The next program is activation: the Q6-conditional inventory is
  the work list; Q5 (harness design) and protect-main remain open
  business decisions.
