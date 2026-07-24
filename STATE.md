# State - sdlc_development_kit

> **Contract** - one question: *what is in flight right now?*
> <=1 page - regenerate at every session end - disposable, always safe to overwrite.
> _Generated 2026-07-24._

## Now
<!-- What's actively being worked. -->
- Session 6 (2026-07-24) closed: the G2 walk ran as a seven-stop
  interactive tour (frame -> G2.1..G2.5 -> close-out); every ruling
  ratified in-conversation before its edit landed. G2 wrap committed
  `a5a4940` - page `docs/gates/G2-design-architecture.md`, registry now
  9 specified / 39 registered. G3 was not reached; it opens next session.
- Ruled: the G1.2 <-> G2.1 two-model division (spec-side guarantees vs
  design-side realization, same 0007 set). Two sharpenings beyond the
  registry rows: G2.1 property carry-forward; G2.5 clause 2 (coverage via
  the G4.3 traceability script in existence mode). G2.3 ratified with 5
  significance triggers + 7-item checklist (items 6-7 absorb the
  completeness findings); G2.4/G2.3 composition fixed (human judges the
  boundary enumeration, machine checks existence + linkage).
- Ruled: candidate G2.6 rejected (per-repo artifact behind a per-task
  gate); ratchet-baseline enforcement exported to the G4 session.
  Registry drift fixed (ratchet metric phrasing; G4.3 added to G2's
  enforced-at list; G2.5 provenance folded into the page).
- plan.md rewritten for session 6 (G3 steps still pending in it). Cairn
  audit clean (3 INFO gate-page orphans, by design). Push approved.

## Blockers
<!-- What's stopping progress. -->
- None.

## Next actions
<!-- The ordered next steps. -->
1. Next session: the G3 walk (3 conditions; specify G3.1-G3.3; resolve or
   defer Q3 first analyzers - couples to the conventions-enforcer arc in
   `E:\claude-orchestrator`, ratified design + E1-E5 seed list at
   `designs/conventions-skill.md` there). Refresh plan.md schedule
   accordingly (G2+G3 slot split across two sessions; later gates shift
   one right).
2. Recorded G4-session inputs (three): protected set = single root
   `specs/**` (E5) and must include task contracts (G0 page note);
   ratchet enforcement package (G2 page completeness check: G4.8
   fail-if-missing, protected-path residence, bootstrap = Q4 budgets +
   duplication capture from main); REQ-ID / criterion-annotation format
   (consumers: G2.4 linkage, G2.5 coverage, G4.3). Native-interop
   memory-safety gap (taxonomy) waits for the G5 session.
3. Parked G0 work, waits on Q6 pilot: F10 `/intake` skill (venue live
   flips G0.1 -> `enforced`) and F11 scaffold subcommand. Direction on
   record: kit self-contained, `/intake` homed here plugin-packaged -
   formalize in the F10 un-deferral ADR.

## Open questions
<!-- Unresolved decisions that need an answer. -->
- Q1 spec-path immutability mechanism - E5 sharpened the candidate to one
  protected root `specs/**` + CI diff (G4.6, PL-PIPE.1) - the G4 session.
- Q3 first custom Roslyn analyzers; does convention extraction generate
  stubs (G3.2) - the G3 walk.
- Q4 thresholds: mutation floor (G5.5), complexity budgets (G4.8), ratchet
  cadence (G9).
- Q5 two-channel decorrelation between Spec and Developer contexts (harness
  design, not a condition parameter).
- Q6 pilot repository selection; greenfield vs retrofit sequencing - gates
  F10/F11 and G0.1's `enforced` flip.
- Q7 enforcement-layer change-control workflow (PL-PIPE.1).
- Protect-main still blocked: rulesets on a private repo need GitHub Pro -
  upgrade, make public, or accept unprotected main?
