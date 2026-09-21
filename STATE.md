# State - sdlc_development_kit

> **Contract** - one question: *what is in flight right now?*
> <=1 page - regenerate at every session end - disposable, always safe to overwrite.
> _Generated 2026-09-20 (session 33 wrap, home machine)._

## Now
- Branch `session-33-g0-declaration`, unpushed, nine commits over main
  (`5e26c1b`, kit 0.13.0, unchanged). Four requests wait in the inbox in
  ADR 0029's format; order agreed 2026-09-20: `g0-declaration`,
  `derived-language`, `feature-document`, `spec-doc-type`. Only the first is
  in flight.
- `g0-declaration` (the pilot consumer proved G0.2 and G0.3 pass green on an
  absent input): the request is signed by both seats at r3 after seven
  engineer-half decisions; ADR 0030 (`436b1ee`); the contract is ready-green
  and reads zero at the language door (`7fd7127`), seven units d0 to d6, each
  `confirmed_by: [user]`. Schema 1.4.0, kit 0.14.0, diagnostics TC017 and
  TC018, words ratified verbatim in the request.
- d0 (USAGE at pass zero) is PASS after two verifier rounds (`8239468`,
  `1ad319a`; round 1 caught a false cross-reference). d1 is saved as
  `3a3261a`: **WIP, unverified, suite red (3 failing of 285), amend before
  any push.** Its message lists what is done and what is not.
- **An OPEN entry stands in the request (r5), so no unit commit stands until
  the seats rule.** `/sdlc audit` reads a contract as parked only when its
  ready errors are exactly TC003 (`skills/sdlc/audit.py:172`); a legal parked
  draft carrying neither input now returns TC003 with TC017 (and TC018 after
  d2) and would read CONTRACT-INVALID. `audit.py` is outside scope.
  Recommended: a check SC4.3, the file added to scope, the fix owned by d2
  (parked = TC003 present and every other error a declaration miss), the
  contract amended through intake, the appendix re-stamped.
- Two-Key runs as a saved workflow, `.claude/workflows/two-key-unit-verifier.js`
  (a receipts agent and a zero-trust grader, the verdict computed). Its
  arguments are in this session's d0 run; change `unit`, `commit`, `receipts`
  and `focus` per unit. About 150k subagent tokens and three minutes a round.
- Receipts at the last verified commit (`26b464b`): suite 282, thirteen
  contracts ready-green, language door zero for the new contract, scope-green.

## Blockers
- The OPEN decision above is the user's. The stale pip install persists
  (`sdlc-taskcontract` 0.10.0, non-editable); `python -m` from the repo root
  shadows it.

## Next actions (plan.md step numbers)
1. Step 1, `g0-declaration`: rule on the OPEN; finish d1 (the scaffold
   round-trip test expects the fresh skeleton red on TC007 and TC017 and the
   fill declares the field; `VALID_DOC` in the audit tests declares it; the
   CHANGELOG delta note under a 0.14.0 heading; `docs/task-contract.md`; the
   `vocabulary-layer` contract declares vocabulary-term, task-contract, gate,
   dependency, spec-artifact, the PO seat's answer); amend the WIP into the
   unit commit; verify. Then d2 to d6, each with Two-Key; d6 carries five
   USAGE advisories listed in plan.md. Release on the user's word: PR, merge
   by merge commit, tag v0.14.0, self-pin bound to this contract.
2. Steps 2 to 4: `derived-language` (its token rule lets a check id lead a
   sketch), `feature-document` (fold the queued 0029 amendments first),
   `spec-doc-type`.
3. Carried: the demo intake; wave B; 5b; the engine's G4.6 finding (the
   write-guard binds an editing-tool list).

## Open questions
- Findings this intake sends to `feature-document`: a closing release unit
  has no check to deliver; checks and sketches are not one to one under the
  three-sketch cap; a hand-pasted appendix contract copy ages at once. Also
  queued for 0029: state in revision rows, no Statement heading, a
  three-column revision table, no owner tags, a spec doc is living.
- Process: the engineer half ran as seven one-per-message decisions and the
  session ran far past its context. Batch the uncontested ones next time and
  propose the session boundary earlier.
- Ratify 5b? Promote "plans as Archify" to the global CLAUDE.md? The hook
  command per stack? The four metrics for wave B. Q4, Q5, Q6, PL-PIPE.3:
  unchanged.
