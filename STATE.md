# State - sdlc_development_kit

> **Contract** - one question: *what is in flight right now?*
> <=1 page - regenerate at every session end - disposable, always safe to overwrite.
> _Generated 2026-07-24._

## Now
<!-- What's actively being worked. -->
- Session 8 (2026-07-24) closed: the G4 walk ran as an eight-stop
  interactive tour (frame -> Q1 -> echo complex -> suites -> G2-lock
  enforcement -> detectors -> ratchets -> close-out); every ruling
  ratified in-conversation before its edit landed. G4 wrap committed
  `9864fe3` - page `docs/gates/G4-pre-merge-ci.md`, registry now 23
  specified / 50 total (G4 roster grew 9 -> 11).
- Ruled: Q1 closed -> ADR 0010 (write-surface manifest + CI diff audit;
  allowlist polarity - writable set enumerated, everything else born
  protected; channel provenance S/E, no implementation bypass;
  fail-if-missing; harness = explicit trust root; G4.6 renamed
  "Write-surface immutability"). Traceability format -> ADR 0011
  (`REQ-<task>-<nnn>`; `criteria.yaml`; results-surfacing annotations;
  totality both directions; one script, three modes). Roster additions:
  G4.10 suppression audit (four vectors, Verifier-owned), G4.11 full
  test execution (one-run totality, G5.5's named precondition). G4.1
  renamed "Inner-loop echo". Frame: object rubric, subject/object
  operator split, minutes admission rule, merge queue authoritative
  (PR CI = advisory preview). G4 ruled execution-only.
- Sharpenings beyond registry rows: derived-seed determinism (G4.4);
  the G4.5+G4.6 pincer (no Developer path to a surface change); G4.7
  ratchet-at-zero with class-E FP path; G4.8 shape closed incl.
  direction-conditional channel weight (tightenings auto-approve); G4.9
  timeline partition with G9.2 + locked-graph precondition + license
  split with G9.3; battery-CWE map ruled three-strata (703 joins the
  hand-tag set). Build-item register consolidated to four. Cairn audit
  clean (5 INFO gate-page orphans, by design).

## Blockers
<!-- What's stopping progress. -->
- None.

## Next actions
<!-- The ordered next steps. -->
1. Next session (S9): the G5 + G6 walk (8 conditions; refresh plan.md
   at its start). Banked inputs: G4.11 is G5.5's named precondition
   (mutation floor's substrate enforced at merge); native-interop
   memory-safety gap (taxonomy `-` row; couples to G3.3 clause 4's
   compensating-control demand); mandatory generated-input oracle scope
   (anti-overfit - G5.2/G5.3 must fix which components carry
   generated-input oracles; likely back-propagates a G1.3 checklist
   item). Schedule row: Q4 mutation-floor procedure + trace-conformance
   criteria likely forced.
2. S11 inputs banked: G9 tightening-job shape (direction-conditional
   auto-approve per 0010), G9.2 SLA windows (G4.9's soft-seize backstop
   consumes them), G9.3 license-sweep division (new-dep check moved to
   G4.9).
3. S12 inputs banked: Q7's worked example (0010/G4.8 channel-weight
   tiering); PL-PIPE.2 fixture pattern (traceability + battery golden
   tests).
4. Parked G0 work waits on Q6 pilot: F10 `/intake` (venue live flips
   G0.1 -> `enforced`) and F11 scaffold. Build items awaiting
   .NET-profile activation, now four (0008 register): sunset-escalation
   analyzer; write-surface audit job (G4.6 + G4.10); battery-CWE map +
   golden test; traceability script + fixture corpus.

## Open questions
<!-- Unresolved decisions that need an answer. -->
- Q4 thresholds, numeric only (shapes closed at G4): mutation floor
  (G5.5), complexity budgets + capture parameters (G4.8), tightening
  cadence (G9).
- Q5 two-channel decorrelation (harness design); named sub-question:
  what the Developer's context contains - test source vs criteria +
  diagnostics.
- Q6 pilot repository selection; greenfield vs retrofit - gates
  F10/F11, G0.1's `enforced` flip, the analyzer first tranche, all four
  build items, and G4.7's bootstrap variant.
- Q7 enforcement-layer change-control workflow (PL-PIPE.1); worked
  example on record.
- Protect-main still blocked for this repo: rulesets on a private repo
  need GitHub Pro - upgrade, make public, or accept unprotected main?
