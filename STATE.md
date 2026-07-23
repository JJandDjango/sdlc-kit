# State - sdlc_development_kit

> **Contract** - one question: *what is in flight right now?*
> <=1 page - regenerate at every session end - disposable, always safe to overwrite.
> _Generated 2026-07-22._

## Now
<!-- What's actively being worked. -->
- Session 2 (2026-07-22) closed: gate registry authored. `docs/gates.md` defines
  13 gates - G0-G10 phase gates plus PL-DOC / PL-PIPE cross-cutting - with 47
  conditions registered (per-condition IDs `Gn.m`, kind mechanical|human, tool
  candidates, check intent, open-parameter links). Source-faithful to
  `HANDOFF_gate-architecture_2026-07-22.md` section 5: all enforced items,
  authored columns, and defect classes carried; nothing invented; verified by
  full cross-check.
- `decisions/0003-gate-vocabulary-and-registry.md` fixed vocabulary: a *gate* is
  a phase's blocking enforcement venue (one table row); a *condition* is a check
  attached to it; lifecycle `registered -> specified -> enforced`. All 47
  conditions are `registered`; none `specified` yet.
- Spine touches: MAP.md gate-map row now links `docs/gates.md`; CONVENTIONS.md
  carries the gate-vocabulary rule; covers-marker added. `cairn audit` clean,
  0 findings.
- Correction to session-1 notes: branch is `main` (not master) and a remote IS
  configured - github.com/JJandDjango/sdlc_development_kit. Session-end commit
  (including this STATE.md) and user-approved push to origin/main in progress.

## Blockers
<!-- What's stopping progress. -->
- None.

## Next actions
<!-- The ordered next steps. -->
1. Begin the `registered -> specified` pass on one gate's conditions - G4
   pre-merge CI is highest-leverage (9 conditions incl. G4.6 spec-path
   immutability, G4.3 REQ-ID traceability).
2. Apply `.github/ruleset-protect-main.json` on GitHub now that the remote
   exists and main is pushed.
3. Prior candidate steps (proposed, not yet decided), now anchored to condition
   IDs: CWE gap analysis vs the ten pillars; prototype custom Roslyn analyzer
   (G3.2); REQ-ID traceability format + CI script (G4.3); minimal phase 3-4
   stack on a pilot repo (G3/G4 subset); Verifier spec-path immutability check
   (G4.6); phase-0 task-contract schema (G0.1).

## Open questions
<!-- Unresolved decisions that need an answer. -->
- Spec-path immutability mechanism: protected dirs + CI diff check vs CODEOWNERS vs separate repo/submodule (G4.6, PL-PIPE.1).
- Task-contract schema fields for phase-0 definition-of-ready (G0.1).
- Which house conventions become custom Roslyn analyzers first; does the convention-extraction skill generate analyzer stubs (G3.2)?
- Threshold selection: mutation score floor (G5.5), complexity budgets (G4.8), ratchet-tightening cadence (G9 policy).
- How the harness achieves two-channel decorrelation between Spec and Developer contexts.
- Pilot repository selection; greenfield vs retrofit sequencing.
- Enforcement-layer change-control workflow - who/what approves gate edits (PL-PIPE.1).
- Which components merit formal models - identify the phase-1 hard cores (G1.2, G2.1, G5.6).
