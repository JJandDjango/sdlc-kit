# State - sdlc_development_kit

> **Contract** - one question: *what is in flight right now?*
> <=1 page - regenerate at every session end - disposable, always safe to overwrite.
> _Generated 2026-07-23._

## Now
<!-- What's actively being worked. -->
- Session 4 (2026-07-23) closed: G0's enforcement pass pulled forward by user
  directive and shipped end-to-end after an interactive three-stop
  walk-through (encoding -> validator -> wiring); every ruling ratified.
- Shipped: ADR 0006 (E1-E5 encoding decisions, P1-P2 parameters, validator +
  wiring, kept feature set); `schemas/task-contract.schema.json` (Draft
  2020-12, draft/ready profiles); `taskcontract` package -
  `python -m taskcontract validate`, stable TC000-TC009 diagnostics,
  `--json` loop output; 13 golden fixtures + `tests/test_validator.py`
  (16/16 green, live-fired); pyproject (`pip install -e` verified);
  `.github/workflows/ci.yml`; deep page `docs/task-contract.md`;
  registry / G0-page / MAP / CONVENTIONS touches. Cairn audit clean
  (2 INFO gate-page orphans, by design).
- G0.1 stays `specified` but is now genuinely mechanical - the registry line
  dropped "(human until schema exists)"; `enforced` awaits the intake venue
  live in a harness (pilot, Q6).
- Direction set this session: the kit stays as self-contained as possible,
  Cairn expected; `/intake` skill's home = this repo, plugin-packaged like
  cairn's skill (record formally in the F10 un-deferral ADR).
- plan.md rewritten for session 4; program schedule shifted one right
  (sessions 5-10); "session N" references in pre-shift pages read +1.
- Session end: single commit of the above, push pre-approved by user.

## Blockers
<!-- What's stopping progress. -->
- None.

## Next actions
<!-- The ordered next steps. -->
1. **Session 5 (user directive, recorded post-close): a once-over of G1** -
   walk the user through `docs/gates/G1-requirements-spec.md` until fully
   understood: G1.1 spec/schema linting, G1.2 model checking (hangs on Q8),
   G1.3 criteria review checklist. Interactive walk-through mode (tour,
   rulings one at a time - the session-4 pacing preference), no new
   artifacts unless rulings force them. Q8's designation criteria (drafted
   in the G1 page) will surface naturally; if ruled on, the Q8 ADR can land
   here instead of the G2 session.
2. Then the program sequence resumes: G2 + G3 pages (8 conditions; specify
   G2.5; Q8 ADR if still open; resolve or defer Q3 first analyzers -
   couples to the conventions-enforcer arc in `E:\claude-orchestrator`).
   `plan.md`'s schedule table shifts one more right.
3. Later sessions per `plan.md`: G4 solo; G5+G6; G7+G8; G9+G10; PL-* +
   close-out. Recorded inputs: G4.6's protected set is the single root
   `specs/**` (E5); native-interop memory-safety gap (taxonomy).
4. Parked G0 work, waits on Q6 pilot: F10 `/intake` skill (its venue going
   live flips G0.1 -> `enforced`) and F11 scaffold subcommand.

## Open questions
<!-- Unresolved decisions that need an answer. -->
- Q1 spec-path immutability mechanism - E5 sharpened the candidate to one
  protected root `specs/**` + CI diff (G4.6, PL-PIPE.1) - G4 session.
- Q3 first custom Roslyn analyzers; does convention extraction generate
  stubs (G3.2) - session 5.
- Q4 thresholds: mutation floor (G5.5), complexity budgets (G4.8), ratchet
  cadence (G9).
- Q5 two-channel decorrelation between Spec and Developer contexts (harness
  design, not a condition parameter).
- Q6 pilot repository selection; greenfield vs retrofit sequencing - gates
  F10/F11 and G0.1's `enforced` flip.
- Q7 enforcement-layer change-control workflow (PL-PIPE.1).
- Q8 which components merit formal models (G1.2, G2.1, G5.6) - criteria may
  get ruled during the session-5 G1 once-over; ADR there or at the G2
  session.
- Protect-main still blocked: rulesets on a private repo need GitHub Pro -
  upgrade, make public, or accept unprotected main?
