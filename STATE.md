# State - sdlc_development_kit

> **Contract** - one question: *what is in flight right now?*
> <=1 page - regenerate at every session end - disposable, always safe to overwrite.
> _Generated 2026-09-26 (session 54 close, project-tree o5 and o6 built)._

## Now
- **`o5-pane-outline` and `o6-pane-keys` are built and closed**, each
  Two-Key PASS at round 2. With the `pane` extra (Textual `>=8.2,<9`),
  `taskcontract tree --follow` runs a Textual app, `taskcontract/pane.py`:
  the whole tree as an outline, each feature open down to its units, the
  current task's unit open and marked `current`, a cursor line with the
  item's reference and whole plain name, the keys, clicks and wheel, a
  closed item's group (`(<n> items: <counts>)`, a finding by its kind),
  renders on a source change that keep the cursor and open state by path,
  the waiting line first, notify once per arrival with its failures in the
  pane, Ctrl-C exit 0. Without the extra, the install line and exit 2. o5
  at `b9a2cb1` + `afad4b0`; o6 at `202f01d` + `39811d7`. Suite 638 passed.
- The 0.15.0 loop is gone: `tree_view.follow()` and its helpers retired at
  o6, with 150 test cases that pinned them; the pane's own tests are in
  `tests/test_pane.py`, `test_pane_keys.py` and `test_pane_renders.py`.
- USAGE's "The interactive pane" was refined and approved at `c9e05e6`
  (four readings; its cut sentence aligned at `afad4b0`); every
  project-tree mark stays red until o7.
- Branch `session-54-project-tree-o5-o6` holds the session; the push and
  the PR wait on the user's word. main is at `9d0e897` (PR #62 merged);
  `v0.15.0` tags `fdd6fe2`.

## Blockers
- None.

## Next actions
1. Session 55: o7, which ships 0.16.0 (USAGE marks green, CHANGELOG, ADR
   0032, the kit version). Its sweep: USAGE's green paragraph at the top of
   section 9 ("reads no document") and ADR 0031 line 43 (stale since o3);
   the green paragraphs at USAGE 622-624, 630-632 and 767-771 (a closed
   contract reads `done`, since o4); "The pane's lines", the `--follow`
   bullet of "The three modes" and "Plain names and titles" still describe
   the 0.15.0 pane (where-am-I and fold lines, ANSI, the width cut); USAGE
   should say a closed gate counts a finding by its kind, and state o3's
   tie-break and that an `rM` above the document's revision is a match;
   the schema's top-level `description` does not name `title`;
   `tree_view.py`'s docstring says "name" where `_fold` prints an id;
   `tests/test_pane.py` imports `tree_view` unused and its docstring's cut
   sentence omits the group.
2. Before the release, run the pane live in a herdr pane on Windows: every
   receipt so far is headless (the o5 drafter saw Textual's writer fail on
   the toggle icon only under pytest's cp1252 capture).
3. Test gaps: no pane test checks that a `parts:` list without `evidence`
   hides an approval's seat (the rule lives in the shared `line()`); the
   row pattern in `tests/conftest.py` (and copies) splits a plain name at
   its first ` [`.
4. Prerequisites 7 to 9 on the kit's own tree: all 16 contracts read `(no
   title)`, the 15 besides project-tree `no feature document`, the 13 older
   ones `to do`; one-line backfills each.
5. G1 after project-tree ships, so the pane follows G1's conditions. The
   pilot's config line, in the engine's session; the engine's install ref
   moves to the new tag there (pull, not push).
6. Deferred, carried: `derived-language` (prerequisite 5); ADR 0029's
   appendix copy and Gherkin for project-tree, with `feature-document`'s
   open question; flag the Claude pane itself; the hook's key action and
   its four known edges, in its README; `.sdlc/config.yaml` still lists
   `plan.workflow.json` as a free path; the advisories at
   `a800c34:STATE.md` Next actions 4; `feature-document`, `spec-doc-type`;
   the demo intake; wave B; 5b; the G4.6 finding;
   `no-check-reads-the-source-document`; the prototype renderer's two gaps
   (`styled-rendering`).

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
  overview. Several units' USAGE text can be approved in one batch before
  any drafting. A USAGE refinement never narrows a contract sentence
  silently: Two-Key grades the contract, not USAGE, so flag any narrowing
  or reading to the user before approval.
- Record each task as it finishes through `taskcontract progress`, and
  each check's run through `progress run <check> [--expect red] --
  <test command>` with `-k`. Run a check's green after its commit with no
  tracked file modified. Close each unit with `progress done` once its
  Two-Key passes.
- A REQUEST is untracked, so git cannot restore it: copy it to the
  scratchpad before a revision edits it.
- A delegated session: one Workflow per step, launched by `scriptPath`
  from `.claude/workflows/`. Keep each agent's reading narrow: the user
  stops an agent past about 400K tokens as a hallucination risk (session
  54). Split a unit whose drafting needs both new behavior and a
  retirement: `test-retirer.js` deletes the code in an export, runs the
  suite and reads only the tests that fail. Parallel drafters for one unit
  each take a disjoint slice; a cover note tells the developer which note
  wins where they meet.
- Before approving a drafted list: run the whole suite on the prototype
  in a scratch worktree (`git worktree add --detach`, overlay, run with
  `python -P -m pytest <worktree>/tests`); check each fixed detail against
  the contract and the feature document; pin caps against free text
  holding line breaks; strip session labels from test names; check for a
  repeated name; check that every `done` rests on a rule that ran; check
  one drafter's label assertions against another's new label parts.
- Before accepting a developer deviation, test it against every
  done_means sentence (o5 round 1: the cut dropped `current`). After a fix
  that reverses an order or a rule, search the test docstrings for the old
  statement (o6 round 1). A developer's whole-suite run gets cut off when
  it returns: run the suite yourself after every developer round.
- The whole suite runs 2 to 5 minutes; a local model holding RAM can get
  a background run killed for memory.
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
  45 to 47, 52 to 54). Does the term need a word for a delegated approval?
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
- Track `.claude/workflows/`? Its four scripts hold the session method and
  exist only on this machine (session 54 added `test-retirer.js` and let
  `unit-developer.js` create a file on its list); the Two-Key grade prompt
  still names a Co-Authored-By line.
- Ratify 5b? The hook command per stack? The four metrics for wave B.
- The engine's `plan.md` holds an uncommitted edit; the engine session's
  to commit.
