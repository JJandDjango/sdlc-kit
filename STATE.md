# State - sdlc_development_kit

> **Contract** - one question: *what is in flight right now?*
> <=1 page - regenerate at every session end - disposable, always safe to overwrite.
> _Generated 2026-09-21 (session 37 close)._

## Now
- **`tree-view` is at r2**, signed by the PO seat on 2026-09-21. The
  strike kept eight criteria, moved SC9 under Decisions, answered the
  three OPENs and recorded two more decisions. The first cut starts at the
  contracts and reads no document. Tasks, approvals, the cursor and check
  runs live in ADR 0024's `.sdlc/progress/<id>.yaml`, a check's run
  written by a kit command. Every unit follows one fixed task list, shown
  and never enforced. A herdr plugin wraps the notify command outside the
  kit. `REQUEST_tree-view_2026-09-21.md` stays untracked, the requester's.
- **The pilot vetted G0 on 0.14.0** (engine session 10): M0 is
  ready-green in CI run 35620384803 and faithful to its document at r3.
  On 0.14.0's findings: `intake-write-locks-its-own-confirmation` closed,
  `coverage-join-inactive-on-undeclared-terms` closed in part, the G4.6
  finding untouched.
- **New finding, `no-check-reads-the-source-document`** (gap, G0, engine
  `d7f82ea`): G0 reads the contract alone, so five terms the M0 document
  defines went undeclared and the door stayed green. Its proposal (engine
  `631dc0f`): intake copies every term the document defines into
  `entities:`, so G0.2 fails until the glossary ratifies them.
- **Kit 0.14.0 is released** (tag `v0.14.0` at `1d306ea`). PR #46 merged
  at `db5db28`, carrying `c87ef7f` (session 36's close) and session 37's
  two commits.

## Blockers
- None.

## Next actions
1. `tree-view` r3, signed by the engineer seat: two or three checks per
   criterion, then the solution half (scope, out of scope, interfaces,
   constraints, units, sequencing). Then intake to ready (r4), the units.
2. G1, no request yet. The pilot's M0 code waits on G1's criteria review,
   which also gives intake's exit the successor venue
   `intake-exit-names-no-successor-venue` asks for.
3. Carried: `derived-language`, `feature-document`, `spec-doc-type`; the
   demo intake in a sandbox consumer; wave B (`playbook-loop`, V1-V6); 5b;
   the G4.6 finding; `no-check-reads-the-source-document`.

## Standing practice
- At resume, read the pilot's `E:\ImSimProject\engine\STATE.md` beside
  this file: the engine hands work to the kit there, and its REQUESTs
  land untracked in this root.
- Run the release unit's sweep patterns before its verifier round; a hit
  outside scope goes to an OPEN and a re-intake first, and the round then
  passes once.
- Attribution is off in the user's settings, so a commit's final
  paragraph is `Contract:` alone and a PR body ends at its last sentence.
- Release shape: PR, merge commit, annotated tag at the merge, then the
  self-pin through its own PR; main's ruleset requires a PR for every
  change. `gh pr checks --watch` started right after `gh pr create` can
  exit 1 on "no checks reported"; start it again.
- A settings file with unrelated uncommitted edits is staged by blob
  (`hash-object`, then `update-index`), so the commit holds one change.

## Open questions
- For `tree-view` r3: does it need its own ADR? The fixed task list
  extends ADR 0027's plan crosswalk, and the progress file gets its first
  writer. And a deliberate red run records the check as failed while
  "prove red" reads done; the tree should show that red as expected.
- Which request carries `no-check-reads-the-source-document`:
  `derived-language`, which already asks for the contract-to-document
  pointer, or its own?
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
