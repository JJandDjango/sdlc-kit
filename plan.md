# Plan - Session 8 (2026-07-24)

The ADR-0004 program sequence continues: the G4 deep page - the largest
gate (9 conditions, G4.1-G4.9, plus one banked candidate condition), solo
slot per the rebased schedule. Interactive walk-through mode (tour,
rulings one at a time, ratified before edits land); docs authored after
the tour. Decisions this session forces: Q1 immutability-mechanism ADR,
the REQ-ID / criterion-annotation format (consumers G2.4, G2.5, G4.3),
the ratchet shape (G4.8; Q4 numbers stay open). Q1 lands early - several
later stops (suppression-audit residence, baseline residence, ratchet
residence) stand on its mechanism.

## This session

1. Refresh this plan (done - this file).
2. Tour stop 1 - Frame: identity + why (the authority end of the G3<->G4
   echo division; merged-result semantics - conditions run on the merge
   result, not the PR head; the last cheap moment, minutes cadence; QA
   executes, Verifier's deterministic core = G4.6 + suppression audit;
   the CI definition itself is PL-PIPE scope). Roster agenda: 9
   registered + 1 banked candidate. Provenance item parked to close-out:
   the registry's authored line ("regression tests from review findings")
   in a pipeline with no human review at G4.
3. Stop 2 - G4.6 + Q1: the spec-path immutability mechanism (single
   protected root `specs/**` incl. task contracts - banked; CI diff
   check vs CODEOWNERS vs separate repo; phase-unconditional check;
   manifest self-protection; shared machinery with the G3 config set /
   enforcement-layer class). -> ADR 0010; G4.6 `specified`.
4. Stop 3 - G4.1 echo complex: battery superset rule (add, never drop);
   G3.1 echo as explicit job step (banked); four-vector suppression
   audit placement (pragmas / NoWarn + severity / flag overrides /
   exclusion edits - banked); battery-audit disposition (substantiate
   the 691/697 taxonomy rows by CWE-tag mapping - banked). -> G4.1
   `specified`.
5. Stop 4 - Suite execution: G4.3 acceptance + REQ-ID traceability -
   fix the criterion-annotation format + script shape (ADR if ruled
   cross-cutting enough); G4.4 property suites; rule on the banked
   candidate condition - merged-build unit-suite-green (G4.10?), also
   G5.5's precondition. -> G4.3, G4.4 `specified` (+ G4.10 if adopted).
6. Stop 5 - G2-lock enforcement: G4.2 architecture tests; G4.5 API
   surface diff + "unapproved" semantics (approval = baseline change
   arriving through the spec channel, not a human click). -> both
   `specified`.
7. Stop 6 - Detectors: G4.7 taint/security scan - "no new findings"
   baseline semantics (absolute-zero vs baseline-relative, residence if
   relative); G4.9 secret + dependency audit - division from G9.2
   (new-at-merge vs newly-disclosed-in-place). -> both `specified`.
8. Stop 7 - G4.8 ratchets: ratify the banked package (fail-if-missing,
   protected-path residence, bootstrap = authored budgets (Q4) +
   duplication captured from main); tighten-only mechanics + tightening
   actor (G9 coupling). Q4 numbers stay open as parameters. ->
   `specified`.
9. Stop 8 - Close-out: completeness check (prepared items: the authored
   line above; CWE-703 error-handling coverage; merge-queue vs PR-CI
   venue semantics), operators & harness, decisions.
10. Authoring pass: `docs/gates/G4-pre-merge-ci.md` (0008 two-layer
    template, G3 page as exemplar) + registry cascade (Deep-page line,
    lifecycle flips, counts, open-parameter index: Q1 closes) + ADR
    0010 (+ 0011 if REQ-ID ruled ADR-worthy) + STATE. Commit the G4
    wrap (Theory trailer); push on explicit approval.
11. Session end: STATE.md regen, commit, push on explicit approval.

## Schedule (rebased: G2+G3 split, later gates shift one right)

| S | Gates | Conditions | Decisions likely forced |
|---|---|---|---|
| 8 | G4 solo (this session) | 9 (+1 candidate) | Q1 ADR; REQ-ID format; ratchet shape |
| 9 | G5 + G6 | 8 | Q4 mutation-floor procedure; trace-conformance criteria |
| 10 | G7 + G8 | 7 | benchmark-budget + SLO procedure shapes |
| 11 | G9 + G10 | 6 | Q4 ratchet cadence; sunset policy |
| 12 | PL-DOC + PL-PIPE | 6 | Q7 change-control ADR; program close-out audit |

Banked inputs (detail in STATE.md): from the G2 session - protected set
= single root `specs/**` incl. task contracts; ratchet enforcement
package; REQ-ID format consumers. From the G3 session - G3.1 echo step;
four-vector suppression audit; unit-suite-green candidate; battery
audit. The G5 session inherits the native-interop memory-safety gap and
the generated-input oracle scope (anti-overfit).
