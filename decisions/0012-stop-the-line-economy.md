# 12. Define the stop-the-line economy: aging windows, one clocks artifact, the fixes field

Status: accepted
Date: 2026-07-26

## Context
Standing reds grew per venue: G4.9 blocks merges on vulnerabilities past
"the G9.2 SLA window" (S8), G5 reds escalate past a remediation window
to stop-the-line at task intake (S9), G8 reds funnel into G7's admission
interlock 4 with a fix lane "via contract reference" (S10), and G8.3's
disposition window banked to "the G9.2 family". Three venues borrowed a
family no condition had defined, and 0005's eight task-contract fields
carry no fix-lane reference despite every arm honoring one. The S11
G9+G10 walk forced the definition at G9.2 and consolidated at close-out.

## Decision
- An aging window = (clock origin, duration per class, breach effect).
  G9.2 owns the family; every consumer references it, none redeclare.
- One clocks artifact (class E; reference name `clocks.yaml`) holds
  every pipeline clock: vulnerability SLA windows (severity x exposure
  class), G5 remediation, G8.3 disposition, G9.3 and G10.2 breach
  windows, G10.1 notice floors, G10.3 drainage window, G9.4 tightening
  cadences, sweep and attestation cadences, suppression expiries.
  Change control is 0010 direction-conditional: shorter/tighter
  auto-approves, longer/looser takes the full second channel. Q4's
  numbers land in this one file.
- Breach effect is uniform - a standing red engaging three arms: task
  intake (G0 admits only fix-referencing tasks in the red's scope),
  merge (G4.9), release admission (G7 interlock 4). Proportionality
  lives in window durations only, never in which teeth engage.
- The task contract gains a ninth field `fixes` (amending 0005,
  append-only): optional finding-ref list; a non-empty intersection
  with an open standing red admits the task through every arm - the
  fix lane, made mechanical.

## Consequences
- G5, G8, G9, and G10-breach reds ride one economy; bespoke per-venue
  escalation ends.
- 0005's JSON-Schema build item picks up `fixes`; the register stays
  four.
- Q4 resolution becomes a single-file edit; the registry's Q4 index
  repoints at the artifact.
- Windows lengthen only through the second channel - the
  quiet-loosening vector is closed.
