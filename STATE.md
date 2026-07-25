# State - sdlc_development_kit

> **Contract** - one question: *what is in flight right now?*
> <=1 page - regenerate at every session end - disposable, always safe to overwrite.
> _Generated 2026-07-25._

## Now
<!-- What's actively being worked. -->
- Session 10 (2026-07-24/25) closed: the G7+G8 walk ran as an
  eight-stop tour (frame -> benchmarks -> binary compat -> IaC -> SLO
  pair -> runtime assertions -> escape triage -> close-out) plus a
  mid-walk interlock consolidation; every ruling ratified live. Wrap
  committed `11548aa` - pages `docs/gates/G7-release-deploy.md` +
  `G8-operations.md`, registry 41 specified / 53 total (G7 4 -> 5,
  G7.5 adopted; G8.2 renamed license, G8.3 renamed escape triage +
  conversion).
- Ruled: four-interlock G7 admission (record; identity, no rebuild
  lane; can-i-deploy; no standing G8 red + fix lane); G7.4
  intra-rollout / G8.2 inter-rollout license; G7 fully mechanical
  (timing = business policy); budgets + SLOs authored at G2; G7.1
  budgets-only via the new budget-designated column; G7.2 last-ship
  baseline + version coherence; G7.3 = the certified environment
  definition; G7.4 dual-clause canary + migration revert-safety
  (N+1); G8 standing-invariant venue (red seizes rollouts never
  operations); G8.1 spec-derived set on the G5.6-shared surface;
  G8.3 conversion-by-default + ladder assignments; chaos = governed
  practice (plan class E, budget as license).
- Cascades: G6.3 revert leg; taxonomy +2 rows (breaking-change gap
  found at the walk) + 2 extended; G1 declaration-record column; G2
  authored set (+budgets, +slo.yaml); Q4 index +3 rows. Zero new
  ADRs. Cairn audit clean (9 INFO gate-page orphans, by design).

## Blockers
<!-- What's stopping progress. -->
- None.

## Next actions
<!-- The ordered next steps. -->
1. Next session (S11): the G9 + G10 walk (6 conditions; refresh
   plan.md at its start). Banked: G9's tightening job now carries
   four input families (ratchet cadence Q4, corpus growth,
   mutation-floor moves, budget re-tightening from measurement
   records + ladder-assignment statistics); G9.2 SLA windows consumed
   three ways (G4.9 soft-seize, G5 red-window escalation, G8.3
   triage window); stop-the-line mechanics incl. the 0005 fix-lane
   field (serves G5 and G8 reds alike); G9.1 consumes G7.5's SBOM
   for field-impact mapping; G9.3 license-sweep division; G10
   notification consumes G7.2's contract-diff payload; G10.3 takes
   the contract-migration far end. Schedule row: Q4 ratchet cadence +
   sunset policy likely forced.
2. S12: PL-DOC + PL-PIPE (6 conditions) + program close-out audit.
   Banked: Q7 worked example (0010/G4.8 channel-weight tiering);
   PL-PIPE.2 fixture pattern - scope grew S10 (G7 admission
   interlocks + slo.yaml derivation compiles are golden-test
   subjects); PL-PIPE scope consolidation (environment definition,
   monitoring config, rollout policy, chaos plan - the class E
   inventory grew S9-S10).
3. Parked G0 work waits on Q6 pilot: F10 `/intake` (venue live flips
   G0.1 -> `enforced`) and F11 scaffold. Build-item register stays
   four (0008); conditionals: trace-validation harness on first
   hard-core activation (now shared G5.6/G8.1), G7.1's bootstrap
   capture variant.

## Open questions
<!-- Unresolved decisions that need an answer. -->
- Q4 thresholds, numeric only (procedures fixed through G8): mutation
  floor + small-N (G5.5); complexity budgets + capture (G4.8);
  benchmark ceilings/margins/statistic defaults (G7.1); canary
  confidence + minimum-sample constants (G7.4); triage window (G8.3,
  G9.2 family); tightening cadence (G9).
- Q5 two-channel decorrelation (harness design); named sub-question:
  what the Developer's context contains.
- Q6 pilot repository selection - now also gates the first
  oracle-designation records (incl. the budget-designated column)
  and G7.1's bootstrap variant.
- Q7 enforcement-layer change-control workflow (PL-PIPE.1); worked
  example on record.
- Protect-main still blocked for this repo: rulesets on a private
  repo need GitHub Pro - upgrade, make public, or accept unprotected
  main?
