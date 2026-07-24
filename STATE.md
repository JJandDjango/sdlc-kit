# State - sdlc_development_kit

> **Contract** - one question: *what is in flight right now?*
> <=1 page - regenerate at every session end - disposable, always safe to overwrite.
> _Generated 2026-07-24._

## Now
<!-- What's actively being worked. -->
- Session 7 (2026-07-24) closed: the G3 walk ran as a five-stop
  interactive tour (frame -> G3.1..G3.3 -> close-out); every ruling
  ratified in-conversation before its edit landed. G3 wrap committed
  `425d72b` and pushed - page `docs/gates/G3-implementation.md`, registry
  now 12 specified / 36 registered.
- Ruled: the G3 <-> G4.1 echo division (latency vs authority;
  single-sourced config; PL-PIPE governance of G3's configs - the one
  gate executing inside its subject's context). Ruled mid-walk on a user
  scope question: the two-layer condition model, ADR 0008 -
  language-agnostic shapes, per-ecosystem tooling profiles, .NET =
  reference profile; gap-closure directive (unreachable rungs become kit
  build items; active-profile trigger only; missing binding gates
  `enforced`, never `specified`). G3 page is the pattern-setter; G0-G2
  pages retrofit lazily.
- Ruled: Q3 closed as policy, ADR 0009 (ratified-registry source of
  truth; selection function at pilot activation; pipeline-native tier
  first; bounded stub generation; fixture-before-gating). G3.2 renamed
  "Analyzer battery". Sharpenings beyond registry rows: G3.2
  no-self-weakening clause; G3.3 loud-failure numerics (drift fix) +
  fenced escape hatches. Taxonomy: 435/691/697 rows added - every
  CWE-1000 pillar now has >=1 tagged row. Cairn audit clean (4 INFO
  gate-page orphans, by design).

## Blockers
<!-- What's stopping progress. -->
- None.

## Next actions
<!-- The ordered next steps. -->
1. Next session: the G4 walk (9 conditions, solo slot per the rebased
   S7-S12 schedule in plan.md; refresh plan.md at its start). Banked
   inputs, from G2 session: protected set = single root `specs/**` incl.
   task contracts; ratchet enforcement package (G4.8 fail-if-missing,
   protected-path residence, bootstrap = Q4 budgets + duplication capture
   from main); REQ-ID / criterion-annotation format (consumers G2.4,
   G2.5, G4.3). From G3 session: G3.1 echo step (identical
   `dotnet format whitespace --verify-no-changes` in the G4 job);
   four-vector suppression audit (pragmas / NoWarn + severity downgrades /
   strictness-flag overrides / generated-code exclusions; joins the
   Verifier's deterministic core); unit-suite-green candidate condition
   (merged-build test execution - also G5.5's precondition); battery
   audit substantiating the 691/697 rows (map enabled rules by CWE tag).
   Q1 immutability-mechanism ADR due here.
2. G5-session inputs on record: native-interop memory-safety gap
   (taxonomy `-` row); mandatory generated-input oracle scope
   (anti-overfit finding - G5.2/G5.3 scope must fix which components
   carry generated-input oracles; likely back-propagates a G1.3
   checklist item).
3. Parked G0 work, waits on Q6 pilot: F10 `/intake` skill (venue live
   flips G0.1 -> `enforced`) and F11 scaffold subcommand; direction on
   record (kit self-contained, `/intake` homed here plugin-packaged).
   Build items awaiting .NET-profile activation (0008/0009):
   sunset-escalation analyzer, suppression-audit check.

## Open questions
<!-- Unresolved decisions that need an answer. -->
- Q1 spec-path immutability mechanism - single protected root `specs/**`
  + CI diff (G4.6, PL-PIPE.1) - the G4 session.
- Q4 thresholds: mutation floor (G5.5), complexity budgets (G4.8),
  ratchet cadence (G9).
- Q5 two-channel decorrelation (harness design); named sub-question on
  record (session 7): what the Developer's context contains - test source
  vs criteria + diagnostics.
- Q6 pilot repository selection; greenfield vs retrofit - gates F10/F11,
  G0.1's `enforced` flip, first-tranche analyzer instantiation (0009),
  and the .NET-profile build items.
- Q7 enforcement-layer change-control workflow (PL-PIPE.1).
- Protect-main still blocked: rulesets on a private repo need GitHub Pro -
  upgrade, make public, or accept unprotected main?
