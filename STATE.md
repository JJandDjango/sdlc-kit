# State - sdlc_development_kit

> **Contract** - one question: *what is in flight right now?*
> <=1 page - regenerate at every session end - disposable, always safe to overwrite.
> _Regenerated 2026-09-20 mid-session 34, after unit d7._

## Now
- Branch `session-33-g0-declaration`, unpushed, over main (`5e26c1b`, kit
  0.13.0). Four requests wait in the untracked inbox; order agreed
  2026-09-20: `g0-declaration`, `derived-language`, `feature-document`,
  `spec-doc-type`. Only the first is in flight.
- `g0-declaration` is signed at **r6**. The OPEN entered at r5 is ruled: a
  door's input being required must be observable at the audit too, so SC4.3
  was added, `skills/sdlc/audit.py` joined scope, and the fix went to a new
  unit `d7-audit-parked-rule` rather than d2, which was already full at
  three sketches. No new ADR; 0030 carries the ruling. The contract is
  ready-green with **eight** units and reads zero at the language door.
- Verified, each PASS by an independent Two-Key round: d0 (`1ad319a`),
  d1 (`6939082`), d2 (round 5, `c1af342` through `d420f80`). d7 is at
  `8ce629e`, in its second round.
- Receipts at `8ce629e`: pytest 292 passed, `/sdlc audit` clean, lang-green,
  vocab-green at 18 terms and 8 constraints, schema 1.4.0.
- Two writes landed in the spec channel beyond the two the request budgeted,
  both corrections of statements this arc made false and both ruled
  legitimate by the verifier: `specs/vocabulary/constraints.yaml`, and the
  class-S edit to the ratified term `specs/vocabulary/task-contract.yaml`,
  made on the user's ruling. They trip different branches of the
  write-guard, so the PR names them on two separate grounds.
- Two-Key runs as a saved workflow, `.claude/workflows/two-key-unit-verifier.js`.
  About 160k subagent tokens and four to six minutes a round.

## Blockers
- None. The OPEN is answered and no unit is waiting on a decision.

## Next actions (plan.md step numbers)
1. Steps 5 to 8: d3 `d3-scaffold-comment`, d4 `d4-intake-flow`,
   d5 `d5-init-seeds-roster`, d6 `d6-adoption-and-release`. Each is one
   commit with the `Contract:` trailer, then Two-Key.
2. Step 9, on the user's word: PR, merge by merge commit, tag v0.14.0, the
   self-pin bound to this contract.
3. Steps 2 to 4 of the four-request queue: `derived-language`,
   `feature-document` (fold the queued 0029 amendments first), `spec-doc-type`.
4. Carried: the demo intake; wave B; 5b; the engine's G4.6 finding.

## Standing practice, learned this session
- Search every tracked file with `git grep` for the claim a unit retires,
  while building the unit. d2 failed four rounds on surfaces nobody had
  looked at yet: `docs/`, the G0 deep page, the schema's own `description`,
  a fixture's intent. d7 then failed on this file.
- Say only what was checked. d7's first message claimed a surface was the
  only survivor without the grep supporting it, which the verifier caught.

## Open questions
- Findings this intake sends onward. To `feature-document`: a closing release
  unit has no check to deliver; checks and sketches are not one to one under
  the three-sketch cap; a hand-pasted appendix contract copy ages at once;
  and new, a unit's derived `done_means` can read broader than the request's
  verbatim spec (d7 says "names each missing field" where the line names rule
  ids). Its own request: `/sdlc audit` drops a W001 warning that sits beside
  an error, because the verdict branches are chained.
- Ratify 5b? The hook command per stack? The four metrics for wave B.
  Q4, Q5, Q6, PL-PIPE.3: unchanged.
