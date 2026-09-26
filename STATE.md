# State - sdlc_development_kit

> **Contract** - one question: *what is in flight right now?*
> <=1 page - regenerate at every session end - disposable, always safe to overwrite.
> _Generated 2026-09-25 (session 53 close, project-tree o2 to o4 built)._

## Now
- **`o2-titles`, `o3-stale` and `o4-statuses` are built and closed**; o2
  and o3 Two-Key PASS at round 1, o4 at round 2. o2 (`899b853`): every item line opens on its id
  and its plain name; the schema moves to 1.5.0 with an optional one-line
  `title`, which intake writes from the feature document's title line; a
  contract without one shows `(no title)`. o3 (`34c154d`): each feature
  line reads `stale: document rN, contract from rM`, `no feature
  document` or `no "Ready:" row` from its document's revision table, and
  intake's I7 writes the `Ready:` row. o4 (`83032bc`, fix `155a76e`): the
  approval that holds the current task names its unit's `confirmed_by`
  seats, `seat: <seats>`; a closed contract reads `done` whatever its
  verdicts read (round 1 failed on it; the user chose the contract's
  reading over the narrower USAGE text Claude had written). Suite 710
  passed.
- USAGE section 9's three subsections were refined and approved in one
  batch at `a94c021`; every project-tree mark stays red until o7.
- The 0.15.0 `--follow` pane still runs and now shows plain names; a unit's
  line carries its `done_means` before its status, so the pane's cut can
  hide a unit's status until o5 replaces it.
- PR #62 carries session 53 (branch `session-53-project-tree-o2-o4`); the
  merge, by merge commit once CI reads green, waits on the user's word.
  main is at `7567591`; `v0.15.0` tags `fdd6fe2`.

## Blockers
- None.

## Next actions
1. Session 54: o5 (the Textual outline, the `pane` extra; Textual joins
   the `test` extra), then o6 (keys, mouse, redraw), then o7, which ships
   0.16.0. o5 and o6 may fit one session; o7 is the release.
2. For o7's sweep, from this session's Two-Key rounds: USAGE's green
   paragraph at the top of section 9 ("reads no document") and ADR 0031
   line 43 are stale since o3, and three green paragraphs since o4 (lines
   622-624 on the roll-up, 630-632 on close evidence, 767-771 "History,
   backfilled": a closed contract now reads `done` whatever its verdicts
   read); USAGE does not say a task reopened after a close shows through,
   or state o3's tie-break (the
   lower of two `Ready:` rows with one rN wins) or that an `rM` above the
   document's revision reads as a match; the schema's top-level
   `description` does not name the `title` amendment.
3. Test helpers: the row pattern in `tests/conftest.py` (and its copies in
   `test_progress.py`) splits a plain name at its first ` [`, so a title
   or `done_means` holding ` [` would misparse; no fixture hits it yet.
4. Prerequisites 7 to 9 now show on the kit's own tree: all 16 contracts
   read `(no title)`, the 15 besides project-tree read `no feature
   document`, and the 13 older ones `to do`.
   Each is a one-line backfill (a `title`, a document, a `progress done`).
5. G1 after project-tree ships, so the pane follows G1's conditions. The
   pilot's config line, in the engine's session; the engine's install ref
   moves to the new tag there (pull, not push).
6. Deferred, carried: `derived-language` (prerequisite 5); ADR 0029's
   appendix copy and Gherkin for project-tree, with `feature-document`'s
   open question; flag the Claude pane itself; the hook's key action and
   its four known edges, in its README; `.sdlc/config.yaml` still lists
   `plan.workflow.json` as a free path; the advisories on `tree_view.py`,
   USAGE and CHANGELOG at `a800c34:STATE.md` Next actions 4;
   `feature-document`, `spec-doc-type`; the demo intake; wave B; 5b; the
   G4.6 finding; `no-check-reads-the-source-document`; the prototype
   renderer's two gaps (`styled-rendering`).

## Standing practice
- At resume, read the pilot's `E:\ImSimProject\engine\STATE.md` beside
  this file: the engine hands work to the kit there, and its REQUESTs land
  untracked in this root.
- A new feature starts as a feature document written through an
  interview, in the format ADR 0029 ratified, tracked at
  `docs/features/<id>.md`; never a request typed from a sketch. Until
  `feature-document` lands, the interview runs by hand from
  `NOTES_feature-document_2026-09-18.md`.
- Intake from a feature document: ratify its new terms first, in their
  own commit. A term whose single-word name or slug equals a dictionary
  word trips CL003; the dictionary cedes the word in the same commit.
  Check the document's Scope against the release unit's needs:
  `skills/sdlc/init.py` (`KIT_VERSION`) and `.github/workflows/sdlc.yml`.
- A plan is plan.md's numbered steps, shown in chat for the user's
  overview. Several units' USAGE subsections can be approved in one batch
  before any drafting (session 53). A USAGE refinement never narrows a
  contract sentence silently: Two-Key grades the contract, not USAGE, so
  flag any narrowing to the user before approval (o4's round 1 failed on
  one).
- Record each task as it finishes through `taskcontract progress`, and
  each check's run through `progress run <check> [--expect red] --
  <test command>` with `-k`. Run a check's green after its commit with no
  tracked file modified: an edited plan.md marks the run `dirty`, so set
  it aside first (copy, `git restore`, run, copy back). Close each unit
  with `progress done` once its Two-Key passes.
- A REQUEST is untracked, so git cannot restore it: copy it to the
  scratchpad before a revision edits it.
- A delegated session: one Workflow per step, launched by `scriptPath`
  from `.claude/workflows/`. Before approving a drafted list, run the
  whole suite on the drafter's prototype in a scratch worktree (`git
  worktree add --detach`, overlay the prototype package and the drafted
  tests, run pytest there): session 53's o2 drafter missed
  `test_progress.py`, and only that run caught it. The approver amends a
  test the drafter missed. A long interface note goes to a file outside
  the drafter's scratch folder, which the developer may read. The next
  unit's drafter can run beside the previous unit's Two-Key.
- Before approving a drafted list: check each fixed detail against every
  use of its terms in the contract and the feature document; pin output
  caps against free text holding line breaks; strip session labels from
  test names; check for a repeated test name; check that every `done` the
  list pins rests on a rule that ran.
- The whole suite runs 2 to 7 minutes; a local model holding RAM can get
  a background run killed for memory (session 53).
- `scope-check` outside Actions needs `--base <sha>`: main's tip.
- Attribution is off: a commit's final paragraph is `Contract:` alone, and
  a PR body ends at its last sentence.
- Release shape: PR, merge commit, annotated tag at the merge, then the
  self-pin through its own PR, which the wrap rides. Run USAGE's `uv` line
  against the new tag. main's ruleset requires a PR for every change.
- herdr probes run in panes Claude splits with `--no-focus` and closes
  after; never report state on another session's pane.

## Open questions
- The `intake-seat` term says a seat is never delegated to an agent, while
  a delegated session's approvals record `--by claude` (sessions 40 to 42,
  45 to 47, 52, 53). Does the term need a word for a delegated approval?
- Should `page:` print a URL (the kit's repo at the pinned tag)?
- Push `E:\herdr-sdlc` to GitHub, so herdr can install it as a plugin?
- Which request carries `no-check-reads-the-source-document`?
- d6's two open advisories, wording only (USAGE section 8's
  `confirmed_by` label; the G0.2 hook test's replace).
- `taskcontract/__init__.py` says `__version__ = "0.3.0"`; nothing reads it.
- To `feature-document`: the interview skill asks ADR 0026's questions,
  and the ratified format lives only in the session 32 notes; see
  `a800c34:STATE.md` for the full list.
- `/sdlc audit` drops a `W001` warning beside an error.
- Should TC016 ride the parked line?
- Track `.claude/workflows/`? Its three scripts hold the session method
  and exist only on this machine; the Two-Key grade prompt still names a
  Co-Authored-By line.
- Ratify 5b? The hook command per stack? The four metrics for wave B.
- The engine's `plan.md` holds an uncommitted edit; the engine session's
  to commit.
