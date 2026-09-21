# State - sdlc_development_kit

> **Contract** - one question: *what is in flight right now?*
> <=1 page - regenerate at every session end - disposable, always safe to overwrite.
> _Generated 2026-09-21 (session 36, at the 0.14.0 release)._

## Now
- **Kit 0.14.0 is released.** `g0-declaration` (ADR 0030) merged as PR
  #44 at `1d306ea` and is tagged `v0.14.0`; the self-pin and this wrap
  ride PR #45 (`session-36-self-pin`). No contract is in flight.
- At the ready profile both G0 inputs are required declarations:
  `entities:` (TC017, schema 1.4.0) and, in a specs tree, a ratified
  `intake-seat` roster (TC018). The draft profile is unchanged.
- Session 36 built d6, which passed Two-Key in round 1 with
  `sweep: true` (`cf518e5`). Its own sweep, run before the verifier,
  found `skills/sdlc/SKILL.md:43` and `:90` stating retired rules outside
  scope; the user ruled r8, and the re-intake added the file (`3ad6cb0`).
- Receipts at the release: pytest 299, `prompt_lang` 13 of 13, thirteen
  contracts ready-green, `/sdlc audit` clean, lang-green, `vocab-check`
  green at 18 terms and 8 constraints, scope-green, CI green on #44.

## Blockers
- None.

## Next actions
1. Choose the next request: `derived-language`, `feature-document` or
   `spec-doc-type`. Each starts with its own plan.
2. Carried: the demo intake in a sandbox consumer, wave B
   (`playbook-loop`, V1-V6), 5b, the engine's G4.6 finding.

## Standing practice, learned this session
- Run the release unit's sweep patterns before its verifier round; a hit
  outside scope goes to an OPEN and a re-intake first, and the round then
  passes once.
- Attribution is off in the user's settings, so a commit's final
  paragraph is `Contract:` alone and a PR body ends at its last sentence.
- A settings file with unrelated uncommitted edits is staged by blob
  (`hash-object`, then `update-index`), so the commit holds one change.

## Open questions
- d6's two open advisories, wording only: USAGE section 8 labels
  `confirmed_by` "optional in the schema", and the G0.2 hook test does
  not assert that its replace changed the text.
- `taskcontract/__init__.py` says `__version__ = "0.3.0"`; nothing reads
  it; a later request.
- To `feature-document`: a check can carry a false premise about today's
  behavior, and intake derives it unchecked; a closing release unit has
  no check to deliver; checks and sketches are not one to one under the
  three-sketch cap; a hand-pasted appendix copy ages at once; a derived
  `done_means` can read broader than the request's line.
- Its own request: `/sdlc audit` drops a `W001` warning that sits beside
  an error.
- Should TC016 ride the parked line? The d7 note in `CHANGELOG.md`
  records the case.
- Track `.claude/workflows/two-key-unit-verifier.js`? It holds the gate's
  rules and exists only on this machine.
- Ratify 5b? The hook command per stack? The four metrics for wave B.
  Q4, Q5, Q6, PL-PIPE.3: unchanged.
