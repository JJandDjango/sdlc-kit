# State - sdlc_development_kit

> **Contract** - one question: *what is in flight right now?*
> <=1 page - regenerate at every session end - disposable, always safe to overwrite.
> _Generated 2026-09-20 (session 34 wrap, home machine)._

## Now
- Branch `session-33-g0-declaration`, unpushed, over main (`5e26c1b`, kit
  0.13.0). Four requests wait in the untracked inbox; order agreed
  2026-09-20. Only `g0-declaration` is in flight.
- The contract is signed at **r6** and ready-green with **eight** units. The
  OPEN entered at r5 is ruled: a door's input being required has to be
  observable at the audit too, so SC4.3 was added, `skills/sdlc/audit.py`
  joined scope, and the fix went to a new unit `d7-audit-parked-rule`. No
  new ADR; 0030 carries the ruling.
- **Verified**: d0 (`1ad319a`), d1 (`6939082`), d2 (round 5, `c1af342`
  through `d420f80`). **d7** (`8ce629e`, `ff55f5b`) is done in substance:
  all three sketches PASS, `done_means` holds, and the verifier built each
  case itself in a temp repo and confirmed the exact lines and exit codes.
  Its recorded verdict is FAIL on stale prose in `STATE.md` and
  `plan.workflow.json`, both fixed at this wrap. One clean round next
  session records it as PASS.
- Receipts at HEAD: pytest **292 passed**, `/sdlc audit` clean, lang-green,
  `vocab-check` green at 18 terms and 8 constraints, schema 1.4.0, the kit's
  own thirteen contracts through the new door.
- Two writes landed in the spec channel beyond the two the request budgeted,
  both ruled legitimate corrections by the verifier:
  `specs/vocabulary/constraints.yaml`, and the class-S edit to the ratified
  term `specs/vocabulary/task-contract.yaml`, made on the user's ruling.
  They trip different branches of the write-guard, so **the PR must name
  them on two separate grounds**.

## Blockers
- None. No unit waits on a decision.

## Next actions (plan.md step numbers)
1. **Apply the blocking bar** written into `plan.md` before anything else.
   Session 34 spent seven FAIL verdicts and about 1.5M subagent tokens
   without one code defect; every failure was a retired rule still stated
   somewhere else. Three corrections: session-disposable files do not gate
   a unit; the repo-wide sweep runs once inside d6; the per-unit focus list
   is fixed to that unit's sketches.
2. One clean Two-Key round on d7 to record its verdict.
3. Steps 5 to 8: d3, d4, d5, d6. Each one commit with the `Contract:`
   trailer, then Two-Key.
4. Step 9, on the user's word: PR, merge by merge commit, tag v0.14.0, the
   self-pin bound to this contract.
5. Then `derived-language`, `feature-document`, `spec-doc-type`; carried:
   the demo intake, wave B, 5b, the engine's G4.6 finding.

## Standing practice, learned this session
- Read a file whole before editing it. Three FAIL verdicts came from
  targeted string edits that left a stale sentence elsewhere in the same
  file, once three lines from the edit.
- Say only what was checked. A commit message claimed a surface was the
  only survivor without the grep supporting it; the verifier caught it.
- Do not widen a verifier's remit between rounds of the same unit.
- The PowerShell tool here does **not** surface a non-zero exit code. Run
  anything whose exit code is a receipt through Bash.

## Open questions
- To `feature-document`: a closing release unit has no check to deliver;
  checks and sketches are not one to one under the three-sketch cap; a
  hand-pasted appendix contract copy ages at once; a unit's derived
  `done_means` can read broader than the request's verbatim spec (d7 says
  "names each missing field" where the line names rule ids).
- Its own request: `/sdlc audit` drops a `W001` warning that sits beside an
  error, because the verdict branches are chained.
- d6 carries eight USAGE advisories, listed in `plan.md` step 8. Two of them
  are sentences marked green that state the retired rule, so flipping the
  marks without rewriting them would publish it as current.
- Ratify 5b? The hook command per stack? The four metrics for wave B.
  Q4, Q5, Q6, PL-PIPE.3: unchanged.
