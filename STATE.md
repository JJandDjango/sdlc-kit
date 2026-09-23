# State - sdlc_development_kit

> **Contract** - one question: *what is in flight right now?*
> <=1 page - regenerate at every session end - disposable, always safe to overwrite.
> _Generated 2026-09-23 (session 43 close)._

## Now
- **The herdr hook is built, a Two-Key PASS at round 1**, outside the kit
  in a new local repo, `E:\herdr-sdlc` (no remote): `herdr_seat.py` at
  `787e415`, its README verified at `a03ee84`. At each arrival at an
  approval it reports the tree pane to herdr as agent `sdlc`, `blocked`,
  with the seat as its message, and shows a toast; it reads the pane once
  a second and releases the flag after two readings without this seat's
  waiting line, leaves another seat's flag alone, and releases on Ctrl-C.
  37 tests; live checks in real herdr panes: flag in about 1.6 s, release
  about 2 s after the line goes.
- **Why the tree pane carries the flag.** Measured on herdr 0.9.0 and
  0.9.1: an outside `report-agent` never changes a Claude pane's state
  (`herdr agent explain`: Claude's state comes only from screen
  detection); a pane with no detected agent shows it. So STATE's old
  question is answered, and no Claude pane id is needed.
- **The kit's config line** (`28d09d8`): `tree: notify: python
  E:/herdr-sdlc/herdr_seat.py`. Started on the kit, the pane reads
  `waiting on a seat` for t6's `approve-tests`, and herdr shows it as
  `sdlc`, `blocked`. That pane (`w9:p8`) was left running.
- PR #52 (t7, t8) merged at `fa0e944`; branch `session-43-herdr-hook`
  starts there. herdr's server moved to 0.9.1 mid-session (the user ran
  the update); the Claude integration is current.

## Blockers
- None. The push and the PR wait on the user's word.

## Next actions
1. Ask the user: is the pane enough to unpark G1 and to replace the
   Archify plans? If yes, G1 (its criteria review before the pilot's M0
   code), then the pilot's M0 code.
2. `pane-view` (`REQUEST_pane-view_2026-09-23.md`, untracked, at r2):
   features 1 to 4 kept (a where-am-I line, `tree: pane: parts:`, short
   ids in the pane, `fold: names`), 5 and 6 struck. Next: its checks and
   solution half (r3), with OPEN 1 (can the id be hidden), then intake.
   It lands before tree-view's t6; then t6 (the query face) and t9 (the
   release, 0.15.0), whose USAGE pass documents it.
3. The pilot's config line, in the engine's session.
4. Deferred: flag the Claude pane itself (a local `claude.toml` detection
   rule shadowing herdr's remote one, or a herdr change); the hook's key
   action that opens the pane; the hook's four known edges, in its
   README.
5. Carried advisories. t6: `tree.py`'s docstring says a close reads
   everything under it done (tasks and checks only); t1's id collision; a
   repeated `depends_on` entry prints twice; `tree_view.py`'s docstring on
   spacing. t9, USAGE: the `progress` rows (`--expect green`, the exit-2
   refusals, a malformed file stopping a writer, the task writers' options
   and evidence), the `G0` verdict's dirty rule, no `dirty` key outside
   git, "done all the way down", the notes from t0, t1 and t3; the pane's
   text (the width cut, `no current task`, the watched files, the verdict
   cache, a vocabulary change showing in up to about 2.4 s, the waiting
   line, notify at the pane's start, exit 127, the failure line whole on
   stderr). t9, code wording: `follow()`'s docstring on Ctrl-C (on POSIX
   the notify child gets the same SIGINT); `--follow`'s help, "at each
   arrival at an approval". Noted: a cached `G0` reading goes stale across
   a deprecated term's sunset date; `cut()` counts characters, not
   display columns.
6. Carried: the backfill of the 13 earlier contracts, once each is checked
   finished; `derived-language`, `feature-document`, `spec-doc-type`; the
   demo intake; wave B (`playbook-loop`, V1-V6); 5b; the G4.6 finding;
   `no-check-reads-the-source-document`; from r3, a status field on the
   finding form and the agent personas writing progress.

## Standing practice
- At resume, read the pilot's `E:\ImSimProject\engine\STATE.md` beside
  this file: the engine hands work to the kit there, and its REQUESTs land
  untracked in this root.
- Plans render as Archify diagrams until the user retires them for the
  pane.
- Record each task as it finishes: `progress start|done <task>`, `--by
  <seat>` on an approval, and each check's run through `progress run
  <check> [--expect red] -- <test command>`, selecting its tests with `-k`
  (test names carry the check id). Close each unit with `progress done`.
- A REQUEST is untracked, so git cannot restore it: copy it to the
  scratchpad before a revision edits it.
- The language door checks every sentence of a sketch for an approved
  opening verb; open each one on "verify".
- A delegated session: one Workflow per step, launched by `scriptPath`.
  `.claude/workflows/` holds the drafter (`spec-channel-drafter.js`), the
  developer (`unit-developer.js`) and Two-Key. The drafter proves red from
  the scratchpad and builds a prototype; Claude approves, places the tests
  and proves red; the developer greens from the interface note without
  opening `tests/`; Claude reviews, runs the receipts, commits and runs
  Two-Key, leaving tracked files alone while it runs. A drafter may run
  beside the previous unit's Two-Key, since neither touches tracked files.
  Session 42's subagents: drafters about 182K and 161K tokens, developers
  98K and 72K, Two-Key 200K and 177K.
- Before placing a drafted list: strip session labels (`ruling_2`) from its
  names, then check the module for a repeated test name, since a later
  `def` silently replaces an earlier one. A later unit may amend an
  earlier unit's test when its contract changes that test's expected
  output; the drafter's pins name such a test, never forbid it.
- `scope-check` outside Actions needs `--base <sha>`: main's tip.
- Run the release unit's sweep patterns before its verifier round; a hit
  outside scope goes to an OPEN and a re-intake first.
- Attribution is off: a commit's final paragraph is `Contract:` alone, and
  a PR body ends at its last sentence.
- Release shape: PR, merge commit, annotated tag at the merge, then the
  self-pin through its own PR; main's ruleset requires a PR for every
  change. `gh pr checks --watch` can exit 1 on "no checks reported"; start
  it again.
- herdr probes run in panes Claude splits with `--no-focus` and closes
  after; never report state on another session's pane. A manual
  `release-agent` for the hook's flag needs a `--seq` above the hook's
  (the time in milliseconds).
- Session 43's subagents (inline Workflow scripts, persisted in the session
  folder): drafter about 78K tokens, developer 52K, Two-Key 133K.
- A settings file with unrelated uncommitted edits is staged by blob
  (`hash-object`, then `update-index`), so the commit holds one change.

## Open questions
- The `intake-seat` term says a seat is never delegated to an agent, while
  a delegated session's approvals record `--by claude` (sessions 40 to 42).
  Does the term need a word for a delegated approval?
- Push `E:\herdr-sdlc` to GitHub, so herdr can install it as a plugin
  later? It has no remote.
- Which request carries `no-check-reads-the-source-document`:
  `derived-language` or its own?
- d6's two open advisories, wording only: USAGE section 8 labels
  `confirmed_by` "optional in the schema", and the G0.2 hook test does not
  assert that its replace changed the text.
- `taskcontract/__init__.py` says `__version__ = "0.3.0"`; nothing reads it.
- To `feature-document`: a check can carry a false premise about today's
  behavior; a closing release unit has no check to deliver; checks and
  sketches are not one to one under the three-sketch cap; a pasted appendix
  copy ages at once; a derived `done_means` can read broader than its line.
- Its own request: `/sdlc audit` drops a `W001` warning beside an error.
- Should TC016 ride the parked line? The d7 note in `CHANGELOG.md` records
  the case.
- Track `.claude/workflows/`? Its three scripts hold the session method and
  exist only on this machine; the Two-Key grade prompt still names a
  Co-Authored-By line, which the verdict code does not read.
- A summary holding a character the console's encoding lacks could fail a
  print piped on Windows; every current contract and finding is ASCII.
- Ratify 5b? The hook command per stack? The four metrics for wave B. Q4,
  Q5, Q6, PL-PIPE.3: unchanged.
- The engine's `plan.md` holds an uncommitted edit, its cursor ticked
  after the session-10 push; the engine session's to commit.
