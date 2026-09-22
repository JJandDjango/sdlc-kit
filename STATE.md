# State - sdlc_development_kit

> **Contract** - one question: *what is in flight right now?*
> <=1 page - regenerate at every session end - disposable, always safe to overwrite.
> _Generated 2026-09-22 (session 40 close)._

## Now
- **`tree-view` t3 and t2 are built, each a Two-Key PASS at round 1**, on
  branch `session-40-tree-view-t3-t2`, not yet pushed. t3 (`ff3fbfb`):
  every item reads one of the six statuses, a parent reads `done` only
  when every child does, each `G0` verdict reads the validator and names
  its command and `HEAD`, and the current task derives from
  `.sdlc/progress/<contract>.yaml`, whose format lands in the new
  `taskcontract/progress.py` (task states, check runs, closes). t2
  (`5bd596a`): each line ends in its links (`depends_on:`, a finding's
  `gate:`), a contract's `doc:` reference, then ` | ` and the item's
  summary, its source field's own text. Suite 375 green (t3 added 39
  cases in `tests/test_tree_status.py`, t2 19 in `tests/test_tree.py`);
  14 contracts ready-green; the doors and the scope check clean.
- The user delegated the in-work approvals to Claude on review. Subagents
  did the work through Workflow: a spec-channel agent drafted each test
  list, proved it red from the scratchpad and prototyped the interface; a
  developer agent made it green without opening `tests/`. Details the
  request left open were fixed with the lists; `plan.md` names them.
- The branch carries `50b691b` (session 39's STATE fix), the plan
  (`48a96ae`), t3, t2 and this close. Kit 0.14.0 stays the release.

## Blockers
- None. The push, the PR and the merge wait on the user's word.

## Next actions
1. Push the branch, open the PR, merge on the user's word; both CI jobs
   must pass.
2. `tree-view` t4 (check runs), t5 (task writers), t6 (query face) and t7
   (the `--follow` pane) are all unblocked; t8 follows t7; t9 last,
   releasing 0.15.0. The build tracks its tasks in `plan.md` until t4 and
   t5 ship `taskcontract progress`.
3. Carried advisories. t4: name the evidence keys in `progress.py` as
   their first writer lands; mark a `G0` verdict dirty when its contract
   differs from `HEAD`. t6: t1's id collision; a repeated `depends_on`
   entry prints twice; `tree_view.py`'s docstring on spacing. t9: t0's two
   wording notes; t1's `.yml` note; USAGE's backfill sentence holds only
   for a ready-green contract with no other active gate; USAGE documents
   the line's words and the text rule behind "unchanged".
4. G1, no request yet. The pilot's M0 code waits on G1's criteria review,
   which also gives intake's exit the successor venue
   `intake-exit-names-no-successor-venue` asks for.
5. Carried: `derived-language`, `feature-document`, `spec-doc-type`; the
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
  tracked files alone while it runs. Four rounds passed at round 1 this
  way across sessions 39 and 40.
- A delegated session (the user approves nothing in-work): one Workflow
  per step. The spec channel drafts the list read-only and proves red
  from the scratchpad; Claude approves, places the tests and proves red
  in the repo; the developer greens without opening `tests/` or the
  scratchpad; Claude reviews the diff, commits, runs Two-Key by
  `scriptPath`. The push, the PR and the merge stay the user's.
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
- A summary holding a character the console's encoding lacks could fail
  a print piped on Windows; every current contract and finding is ASCII.
- Ratify 5b? The hook command per stack? The four metrics for wave B.
  Q4, Q5, Q6, PL-PIPE.3: unchanged.
- The engine's `plan.md` holds an uncommitted edit, its cursor ticked
  after the session-10 push; the engine session's to commit.
