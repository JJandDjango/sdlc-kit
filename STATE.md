# State - sdlc_development_kit

> **Contract** - one question: *what is in flight right now?*
> <=1 page - regenerate at every session end - disposable, always safe to overwrite.
> _Generated 2026-09-23 (session 42 wrap)._

## Now
- **`tree-view` t7 and t8 are built, each a Two-Key PASS at round 1**, on
  branch `session-42-tree-view-t7-t8`, pushed for its PR; the merge waits
  on the user. t7 (`2f8ef03`): `taskcontract tree --follow` keeps a pane
  on the current task: the path to it, each level's other items folded to
  one line of counts by status, the task last; lines cut to the pane's
  width; a redraw within about 1.3 s of a change to a watched file (0.23 s
  warm on the kit), never while nothing changes; each `G0` reading kept in
  memory until its contract or the vocabulary changes; every `git status`
  with `--no-optional-locks`. t8 (`0e89078`): on an approval the first
  line reads `waiting on a seat: {approval} for {unit}`, and `tree:
  notify:` in `.sdlc/config.yaml` runs through the shell once per
  arrival, with `SDLC_NODE`, never waited on; a failure prints `notify
  failed, exit {code}: {command}` on stderr. Suite 486 green (t7 37
  cases, t8 17, in `tests/test_tree_pane.py`); 14 contracts ready-green;
  the doors and the scope check clean.
- **The pane runs on the kit itself.** t7 and t8 are closed with
  `progress done` and their checks carry their red and green runs; the
  pane reads `waiting on a seat: approve-tests for tree-view/t6-query-face`.
  The progress file is local and ignored: a fresh clone starts with none.
- PR #51 (t4, t5) merged at `f2d400a`; this branch starts there. The user
  ruled five details at plan review and delegated the in-work approvals
  to Claude on review; Workflow subagents did the work.

## Blockers
- None. The PR's merge waits on the user's word.

## Next actions
1. Next session: merge this branch's PR on the user's word. Then run
   `python -m taskcontract tree --follow` in a herdr pane, and build the
   herdr hook on t8's notify, outside the kit (a script or a config line).
   Its first question: does herdr's own screen detection overwrite an
   outside `herdr pane report-agent --state blocked`? The notify command
   runs from the pane, so it needs the Claude pane's id.
2. Then t6 (the query face) and t9 (the release, 0.15.0).
3. Parked until the pane can follow them: G1, then the pilot's M0 code.
   The pane now runs; the user says when it replaces the Archify plans.
4. Carried advisories. t6: `tree.py`'s docstring says a close reads
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
5. Carried: the backfill of the 13 earlier contracts, once each is checked
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
- A settings file with unrelated uncommitted edits is staged by blob
  (`hash-object`, then `update-index`), so the commit holds one change.

## Open questions
- The `intake-seat` term says a seat is never delegated to an agent, while
  a delegated session's approvals record `--by claude` (sessions 40 to 42).
  Does the term need a word for a delegated approval?
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
