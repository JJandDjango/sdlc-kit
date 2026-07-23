# State - sdlc_development_kit

> **Contract** - one question: *what is in flight right now?*
> <=1 page - regenerate at every session end - disposable, always safe to overwrite.
> _Generated 2026-07-22._

## Now
<!-- What's actively being worked. -->
- Session 1 (2026-07-22) closed: repo initialized with the Cairn spine (rendered
  via `E:/cairn/skills/cairn/render.py`; answers: code / greenfield / backend
  none). `cairn audit` clean, exit 0.
- Design content from `HANDOFF_gate-architecture_2026-07-22.md` distributed into
  the spine: THEORY.md (intent + 9 invariants + success criteria + non-goals),
  MAP.md (gate-pipeline diagram + 8-component table), and
  `decisions/0002-spec-first-gates-over-static-detectors.md` (settled verdict:
  degradation closed statically, bugs closed spec-first; do not re-litigate).
- Git initialized on `master`; the initial commit (whole tree, including this
  STATE.md) is being assembled at session end. No remote configured.
- Design/exploration pass complete; **no implementation started**.

## Blockers
<!-- What's stopping progress. -->
- None.

## Next actions
<!-- The ordered next steps. -->
Candidate next steps from the handoff (proposed, not yet decided):
1. CWE gap analysis: enabled analyzer rules vs the ten CWE-1000 pillars; list uncovered nodes.
2. Prototype one custom Roslyn analyzer + code fix for a single house convention.
3. Define the REQ-ID traceability format and write the CI traceability script.
4. Stand up the minimal phase 3-4 stack on a pilot repo, then add ratchets.
5. Draft the Verifier spec-path immutability check.
6. Write the phase-0 task-contract schema.

## Open questions
<!-- Unresolved decisions that need an answer. -->
- Spec-path immutability mechanism: protected dirs + CI diff check vs CODEOWNERS vs separate repo/submodule.
- Task-contract schema fields for phase-0 definition-of-ready.
- Which house conventions become custom Roslyn analyzers first; does the convention-extraction skill generate analyzer stubs?
- Threshold selection: mutation score floor, complexity budgets, ratchet-tightening cadence.
- How the harness achieves two-channel decorrelation between Spec and Developer contexts.
- Pilot repository selection; greenfield vs retrofit sequencing.
- Enforcement-layer change-control workflow - who/what approves gate edits.
- Which components merit formal models (identify the phase-1 hard cores).
