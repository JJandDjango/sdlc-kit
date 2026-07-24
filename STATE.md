# State - sdlc_development_kit

> **Contract** - one question: *what is in flight right now?*
> <=1 page - regenerate at every session end - disposable, always safe to overwrite.
> _Generated 2026-07-23._

## Now
<!-- What's actively being worked. -->
- Session 5 (2026-07-23) closed: the G1 once-over ran as a five-stop
  interactive tour (frame -> G1.1 -> G1.2/Q8 -> G1.3 -> close-out); both
  rulings ratified in-conversation before their edits landed.
- Ruled: Q8 hard-core designation criteria ratified as drafted ->
  [0007](decisions/0007-hard-core-designation-criteria.md) (three prongs,
  conjunction; recording venue deferred to the enforcement pass). G1.2
  flipped `registered` -> `specified` - all three G1 conditions
  `specified`; registry count now 4 specified / 44 registered; Q8 moved to
  the open-parameter index's resolved list; G1.2/G2.1/G5.6 Open cells ->
  0007. G2.1/G5.6 stay `registered` (pass conditions fix at their own
  sessions).
- Ruled: stale forward session references re-anchored to gate-anchored
  phrasing - G1 page x2 ("the G2+G3 session"), G0 page x1 ("the G4
  session"). Historical session mentions stay numeric.
- plan.md rewritten for session 5; schedule table now 6 = G2+G3 through
  11 = PL-*. Cairn audit clean (2 INFO gate-page orphans, by design).
- Session end: single commit of the above; push approved by user.

## Blockers
<!-- What's stopping progress. -->
- None.

## Next actions
<!-- The ordered next steps. -->
1. Session 6: the program sequence resumes - G2 + G3 pages (8 conditions;
   specify G2.5; resolve or defer Q3 first analyzers - couples to the
   conventions-enforcer arc in `E:\claude-orchestrator`). Q8 already
   resolved (0007) - the session slims to Q3 + condition specification.
2. Later sessions per `plan.md`: G4 solo (7); G5+G6 (8); G7+G8 (9);
   G9+G10 (10); PL-* + close-out (11). Recorded G4 inputs: protected set =
   single root `specs/**` (E5) and must include task contracts (G0 page
   note); native-interop memory-safety gap (taxonomy) for the G5 session.
3. Parked G0 work, waits on Q6 pilot: F10 `/intake` skill (venue live
   flips G0.1 -> `enforced`) and F11 scaffold subcommand. Direction on
   record: kit self-contained, `/intake` homed here plugin-packaged -
   formalize in the F10 un-deferral ADR.

## Open questions
<!-- Unresolved decisions that need an answer. -->
- Q1 spec-path immutability mechanism - E5 sharpened the candidate to one
  protected root `specs/**` + CI diff (G4.6, PL-PIPE.1) - G4 session.
- Q3 first custom Roslyn analyzers; does convention extraction generate
  stubs (G3.2) - session 6.
- Q4 thresholds: mutation floor (G5.5), complexity budgets (G4.8), ratchet
  cadence (G9).
- Q5 two-channel decorrelation between Spec and Developer contexts (harness
  design, not a condition parameter).
- Q6 pilot repository selection; greenfield vs retrofit sequencing - gates
  F10/F11 and G0.1's `enforced` flip.
- Q7 enforcement-layer change-control workflow (PL-PIPE.1).
- Protect-main still blocked: rulesets on a private repo need GitHub Pro -
  upgrade, make public, or accept unprotected main?
