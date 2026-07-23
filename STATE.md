# State - sdlc_development_kit

> **Contract** - one question: *what is in flight right now?*
> <=1 page - regenerate at every session end - disposable, always safe to overwrite.
> _Generated 2026-07-23._

## Now
<!-- What's actively being worked. -->
- Session 3 (2026-07-23) closed: gate documentation program launched and its
  first increment shipped. ADR 0004 fixes the program - sequential per-gate
  deep pages `docs/gates/<ID>-<slug>.md` (G0 -> G10 -> PL-*), depth =
  document + specify (enforcement artifacts are a later pass), normative
  roster policy (gaps -> PROPOSED conditions, user ratifies), light gates
  batched (~7 sessions; schedule table in `plan.md`).
- Shipped this session: `docs/gates/G0-planning-intake.md` (exemplar) and
  `docs/gates/G1-requirements-spec.md`; substrate pages `docs/taxonomy.md`
  (ladder + CWE/ODC -> condition mapping) and `docs/catalog.md` (8 spec-first
  patterns, cross-ref table moved from registry); ADR 0005 task-contract
  fields (8 fields, Q2 resolved); MAP/CONVENTIONS/registry touches.
- Ratified 2026-07-23: task-contract field set (G0.1 -> `specified`); G1.1
  warnings-block strictness (-> `specified`); G1.3 10-item review checklist
  (-> `specified`); new condition G2.5 spec-suite red run (registered, design
  source: G1 page completeness check). Registry now 48 conditions - 3
  `specified`, 45 `registered`. Cairn audit clean (2 INFO orphan notes are
  by design - gate pages link from the registry, not MAP).
- Session end: committed ff1efdc, pushed to origin/main. Ruleset application
  BLOCKED - GitHub 403: private repos need GitHub Pro (or public visibility)
  for rulesets. `.github/ruleset-protect-main.json` stays stored; direct
  pushes to main continue meanwhile.

## Blockers
<!-- What's stopping progress. -->
- None.

## Next actions
<!-- The ordered next steps. -->
1. **User directive for session 4:** walk through G0 thoroughly and survey
   what implementations exist / could be created to enforce it - task-contract
   schema encoding (JSON Schema over YAML/JSON), validator tooling, harness
   intake wiring. A user-directed pull-forward of G0's enforcement pass;
   spec baseline is `docs/gates/G0-planning-intake.md` + ADR 0005.
2. Resume the program sequence: G2 + G3 pages - specify G2.5, force the Q8
   hard-core-designation ADR (criteria drafted in the G1 page), resolve or
   defer Q3 (first custom analyzers).
3. Sessions 5-9 per the `plan.md` schedule (G4 solo; G5+G6; G7+G8; G9+G10;
   PL-* + close-out). Session inputs already recorded in pages: G4.6's
   protected-path set must include task contracts (G0 page, session 5);
   native-interop memory-safety gap (taxonomy, session 6).

## Open questions
<!-- Unresolved decisions that need an answer. -->
- Q1 spec-path immutability mechanism: protected dirs + CI diff vs CODEOWNERS vs separate repo (G4.6, PL-PIPE.1) - session 5.
- Q3 which house conventions become custom Roslyn analyzers first; does the convention-extraction skill generate stubs (G3.2) - session 4.
- Q4 threshold selection: mutation floor (G5.5), complexity budgets (G4.8), ratchet cadence (G9) - sessions 5/6/8.
- Q5 how the harness achieves two-channel decorrelation between Spec and Developer contexts (harness design, not a condition parameter).
- Q6 pilot repository selection; greenfield vs retrofit sequencing.
- Q7 enforcement-layer change-control workflow (PL-PIPE.1) - session 9.
- Q8 which components merit formal models (G1.2, G2.1, G5.6) - designation criteria proposed in the G1 page; ADR due session 4.
- Protect-main blocked: rulesets on a private repo need GitHub Pro - upgrade,
  make the repo public, or accept unprotected main for now?
- (Q2 resolved 2026-07-23 -> decisions/0005-task-contract-fields.md.)
