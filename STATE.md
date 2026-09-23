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
- **The herdr monitoring path goes first** (user, 2026-09-22). The gate
  work queued after tree-view (G1, then the pilot's M0 code) stays parked
  until a herdr pane can follow it, and that pane then replaces the
  Archify plan diagram as the way the user watches work. The herdr side is
  not started: `herdr plugin list` shows only `herdr-file-viewer`.
- The user delegated this session's in-work approvals to Claude on
  review; Workflow subagents did the work (a spec-channel drafter, a
  developer who never opened `tests/`). Details the request left open
  were fixed with the test lists; `plan.md` names them.
- The branch carries `50b691b` (session 39's STATE fix), the plan
  (`48a96ae`), t3, t2 and this close. Kit 0.14.0 stays the release.

## Blockers
- None. The push, the PR and the merge wait on the user's word.

## Next actions
1. Next session (user, 2026-09-22): start the herdr pane work. Open by
   pushing this branch and opening its PR, on the user's word. Recommended
   first deliverable: t4 and t5, the `taskcontract progress` writers the
   pane needs before anything in it moves; t7 first would build the pane
   but show nothing moving until they land.
2. The monitoring path, in order: t4 (`progress run`) and t5 (`progress
   start/done/block`, the backfill); t7 (`taskcontract tree --follow`)
   and t8 (the waiting line and the `tree: notify:` command); then the
   herdr hook on t8's notify, outside the kit, maybe a script or a config
   line rather than a plugin. The hook's first question: does herdr's own
   screen detection overwrite an outside `herdr pane report-agent --state
   blocked`? The notify command runs from the `--follow` pane, so it
   needs the Claude pane's id.
3. Then t6 (the query face) and t9 (the release, 0.15.0); neither blocks
   monitoring, since the pane can watch the pilot from the kit's checkout
   with `--root`.
4. Parked until the pane can follow them: G1, no request yet, and the
   pilot's M0 code, which waits on G1's criteria review; that review also
   gives intake's exit the successor venue
   `intake-exit-names-no-successor-venue` asks for.
5. Carried advisories. t4: name the evidence keys in `progress.py` as
   their first writer lands; mark a `G0` verdict dirty when its contract
   differs from `HEAD`. t6: t1's id collision; a repeated `depends_on`
   entry prints twice; `tree_view.py`'s docstring on spacing. t9: t0's two
   wording notes; t1's `.yml` note; USAGE's backfill sentence holds only
   for a ready-green contract with no other active gate; USAGE documents
   the line's words and the text rule behind "unchanged".
6. Carried: `derived-language`, `feature-document`, `spec-doc-type`; the
   demo intake in a sandbox consumer; wave B (`playbook-loop`, V1-V6); 5b;
   the G4.6 finding; `no-check-reads-the-source-document`; from r3, a
   status field on the finding form and the agent personas writing
   progress.

## Standing practice
- At resume, read the pilot's `E:\ImSimProject\engine\STATE.md` beside
  this file: the engine hands work to the kit there, and its REQUESTs
  land untracked in this root.
- Plans still render as Archify diagrams until the herdr pane works; then
  the pane replaces them. Once t4 and t5 land, record each task with
  `taskcontract progress` as it finishes, so the pane moves before the
  agent personas learn to do it.
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
  `scriptPath`. The push, the PR and the merge stay the user's. The two
  drafters cost about 300K tokens each with their prototypes and
  mutation runs, half of the session's subagent total.
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
