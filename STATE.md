# State - sdlc_development_kit

> **Contract** - one question: *what is in flight right now?*
> <=1 page - regenerate at every session end - disposable, always safe to overwrite.
> _Generated 2026-09-22 (session 41 close)._

## Now
- **`tree-view` t4 and t5 are built, each a Two-Key PASS at round 1**, on
  branch `session-41-tree-view-t4-t5`, not yet pushed. t4 (`0b650bd`):
  `taskcontract progress run <check> [--expect red|green] -- <command>`
  records red or green beside the expectation, with the command, `HEAD`, a
  `dirty` mark and the time; the folder ignores itself; a done check shows
  `via <command> at <head>`, and a `G0` verdict reads `dirty` when its
  contract file differs from `HEAD`. t5 (`a11eab0`): `progress start`,
  `done` and `block`; `--by` on an approval, `--reason` on a block; `done`
  on a unit or contract is one close; the tree shows `at <head>`, `by
  <seat> at <head>` and `because <reason>`. Suite 432 green (t4 30 cases,
  t5 27, both in `tests/test_progress.py`); 14 contracts ready-green; the
  doors and the scope check clean.
- **The kit records its own progress.** t4's and t5's checks carry their
  runs (t5's red, then green), and t0 to t5 are closed with `progress
  done`, so the kit's tree reads them done. The derived current mark stands
  on `tree-view/t6-query-face/approve-tests`, waiting on a seat. The file is
  local and ignored: a fresh clone starts with no progress.
- PR #50 (t3, t2) merged at `a1109df`; this branch starts from its tip. The
  user ruled five details at plan review and delegated the in-work
  approvals to Claude on review; Workflow subagents did the work.

## Blockers
- None. The push, the PR and the merge wait on the user's word.

## Next actions
1. Next session: the pane. t7 (`taskcontract tree --follow`), then t8 (the
   waiting line and the `tree: notify:` command). Open with `progress start
   tree-view/t7-pane-face/approve-tests`, so the cursor leaves t6.
2. Then the herdr hook on t8's notify, outside the kit, maybe a script or a
   config line. Its first question: does herdr's own screen detection
   overwrite an outside `herdr pane report-agent --state blocked`? The
   notify command runs from the `--follow` pane, so it needs the Claude
   pane's id.
3. Then t6 (the query face) and t9 (the release, 0.15.0).
4. Parked until the pane can follow them: G1, then the pilot's M0 code.
5. Carried advisories. t7: run `git status` with `--no-optional-locks`,
   since the pane redraws while the user runs git. t6: `tree.py`'s docstring
   says a close reads everything under it done (tasks and checks only); t1's
   id collision; a repeated `depends_on` entry prints twice; `tree_view.py`'s
   docstring on spacing. t9: USAGE's `progress` rows (`--expect green`, the
   exit-2 refusals and their lines, a malformed file stopping a writer, the
   task writers' options and evidence), the `G0` verdict's dirty rule, no
   `dirty` key outside git, "done all the way down" (a close never covers a
   verdict), and the notes carried from t0, t1 and t3.
6. Carried: the backfill of the 13 earlier contracts, once each is checked
   finished; `derived-language`, `feature-document`, `spec-doc-type`; the
   demo intake; wave B (`playbook-loop`, V1-V6); 5b; the G4.6 finding;
   `no-check-reads-the-source-document`; from r3, a status field on the
   finding form and the agent personas writing progress.

## Standing practice
- At resume, read the pilot's `E:\ImSimProject\engine\STATE.md` beside
  this file: the engine hands work to the kit there, and its REQUESTs land
  untracked in this root.
- Plans render as Archify diagrams until the herdr pane works.
- Record each task as it finishes: `progress start|done <task>`, `--by
  <seat>` on an approval, and each check's run through `progress run
  <check> [--expect red] -- <test command>`, selecting its tests with `-k`
  (test names carry the check id).
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
  Two-Key, leaving tracked files alone while it runs. Session 41's
  subagents: drafters about 183K and 227K tokens, developers 100K and 81K,
  Two-Key 192K and 193K.
- Before placing a drafted list: strip session labels (`ruling_2`) from its
  names, then check the module for a repeated test name, since a later
  `def` silently replaces an earlier one.
- Run the release unit's sweep patterns before its verifier round; a hit
  outside scope goes to an OPEN and a re-intake first.
- Attribution is off: a commit's final paragraph is `Contract:` alone, and
  a PR body ends at its last sentence.
- Release shape: PR, merge commit, annotated tag at the merge, then the
  self-pin through its own PR; main's ruleset requires a PR for every
  change. `gh pr checks --watch` can exit 1 on "no checks reported"; start
  it again.
- A settings file with unrelated uncommitted edits is staged by blob
  (`hash-object`, then `update-index`), so the commit holds one change.

## Open questions
- The `intake-seat` term says a seat is never delegated to an agent, while
  a delegated session's approvals would record `--by claude` (ruling 4
  keeps the record honest). Does the term need a word for a delegated
  approval?
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
- The engine's `plan.md` holds an uncommitted edit, its cursor ticked after
  the session-10 push; the engine session's to commit.
