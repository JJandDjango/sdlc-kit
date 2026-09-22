# State - sdlc_development_kit

> **Contract** - one question: *what is in flight right now?*
> <=1 page - regenerate at every session end - disposable, always safe to overwrite.
> _Generated 2026-09-22 (session 39 close)._

## Now
- **`tree-view` t0 and t1 are built, each a Two-Key PASS at round 1**, on
  branch `session-39-tree-view-t0-t1`. t0 (`73c4987`, the page before the
  code): USAGE section 9, "Following the work", every part red;
  Troubleshooting moved to section 10. t1 (`c6f1222`, the tree's shape):
  `taskcontract tree` prints the gates with their findings, then each
  contract with a verdict per active gate, its units, seven tasks and
  checks, one item per line, full id first. Every status reads `to do`
  until t3 derives them. New: `taskcontract/tree.py`, `tree_view.py`,
  `data/gates.yaml` (13 gates), `data/tasks.yaml` (7 tasks),
  `tests/test_tree.py` (18 tests). Suite 317 green; 14 contracts
  ready-green; the doors and the scope check clean.
- t0 fixed two details the request left open: an unnamed check is
  `sketch-<n>` by position from 1, and an inactive gate prints only when a
  finding names it. On the pilot the tree files each of its 16 findings
  once: ten under G0, one under G3, one under G4, four under `none`.
- **PR #49 is merged** (merge commit `fe83804`), carrying `971b57a`
  (session 38's STATE fix), `9c2fbe4` (the plan), t0, t1 and the close
  (`4d05adc`). Both CI jobs passed. Kit 0.14.0 stays the release (tag
  `v0.14.0` at `1d306ea`). This STATE fix sits on local main, one commit
  ahead of origin; the next session's PR carries it, as PR #49 carried
  `971b57a`.

## Blockers
- None.

## Next actions
1. `tree-view` t2 (summaries and links) and t3 (status and cursor), in a
   fresh session; both follow t1. Then t4, t5 and t7 after t3, t6 after t2
   and t3, t8 after t7, t9 last, releasing 0.15.0. The build tracks its
   tasks in `plan.md` until t4 and t5 ship `taskcontract progress`.
2. Carried advisories. t6: t1's id collision, where a sketch naming
   `(commit)` or a unit named like an active gate repeats an id the query
   needs unique. t9: t0's two wording notes (the line after the `progress
   run` block lacks its red mark; "about fifteen lines" against t7's "at
   most 15") and t1's note that a `.yml` finding is not read.
3. G1, no request yet. The pilot's M0 code waits on G1's criteria review,
   which also gives intake's exit the successor venue
   `intake-exit-names-no-successor-venue` asks for.
4. Carried: `derived-language`, `feature-document`, `spec-doc-type`; the
   demo intake in a sandbox consumer; wave B (`playbook-loop`, V1-V6); 5b;
   the G4.6 finding; `no-check-reads-the-source-document`; from r3, a
   status field on the finding form and the agent personas writing
   progress.

## Standing practice
- At resume, read the pilot's `E:\ImSimProject\engine\STATE.md` beside
  this file: the engine hands work to the kit there, and its REQUESTs
  land untracked in this root.
- A REQUEST is untracked, so git cannot restore it: copy it to the
  scratchpad before a revision edits it.
- The language door checks every sentence of a sketch for an approved
  opening verb, not only the first; open each one on "verify".
- Run the verifier's receipts yourself before its round, then leave
  tracked files alone while it runs: its receipts agent re-runs the suite
  on the working tree, so a red test written early fails the round. t0
  and t1 each passed at round 1 this way.
- Run the release unit's sweep patterns before its verifier round; a hit
  outside scope goes to an OPEN and a re-intake first.
- Attribution is off in the user's settings, so a commit's final
  paragraph is `Contract:` alone and a PR body ends at its last sentence.
- Release shape: PR, merge commit, annotated tag at the merge, then the
  self-pin through its own PR; main's ruleset requires a PR for every
  change. `gh pr checks --watch` started right after `gh pr create` can
  exit 1 on "no checks reported"; start it again.
- A settings file with unrelated uncommitted edits is staged by blob
  (`hash-object`, then `update-index`), so the commit holds one change.

## Open questions
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
  rules and exists only on this machine. Its grade prompt still names a
  Co-Authored-By line, stale since attribution went off; the verdict code
  does not read it.
- Ratify 5b? The hook command per stack? The four metrics for wave B.
  Q4, Q5, Q6, PL-PIPE.3: unchanged.
- The engine's `plan.md` holds an uncommitted edit, its cursor ticked
  after the session-10 push; the engine session's to commit.
