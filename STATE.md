# State - sdlc_development_kit

> **Contract** - one question: *what is in flight right now?*
> <=1 page - regenerate at every session end - disposable, always safe to overwrite.
> _Generated 2026-09-29 (session 63 close, tree-first-level t3 built)._

## Now
- **tree-first-level t3 is built**: `t3-halves` at `a09278b` (USAGE,
  "Revisions and halves" refined at pass zero, still red), `00ce617`
  (code and tests), `e5a814f` (a feature before intake never reads
  `done`) and `f1374c8` (its document read once per print), Two-Key PASS
  at round 2, the unit closed. A feature before intake names `no
  contract: document rN` or `no revision table`, and shows two items at
  the level `half`, `<id>/request` and `<id>/solution`, signed by an ADR
  0034 row (`by <signer> at rN`) or `to do`. The drift mark leaves out
  `Signed:` rows. On the kit, `g1-requirements-spec` reads `doing` with
  its request half `done by user at r3`, and `tree-first-level` lost its
  stale mark. Suite 749 passed.
- Two-Key round 1 failed on Constraint 4 of the feature document (a
  document read twice per print), which no sketch named.
- On branch `session-63-tree-first-level-t3`, not pushed; the push and the
  PR on the user's word. Session 62's PR #73 merged at `1a86561`.
- The user's order (2026-09-29): t4 releases 0.17.0; then
  `feature-document` (0.18.0) ahead of G1's solution half, because the
  user wants to use the kit on another machine and the shipped interview
  skill still asks ADR 0026's questions. When it ships, tell the user the
  kit is ready there, with the tag to install. Until then another machine
  runs the interview by hand from the two `NOTES_feature-document_*`
  files, with `docs/features/tree-first-level.md` as the exemplar.
- Carried: 18 features: 17 with a contract, 15 of them `[done]`;
  `glossary-alias-disjointness` parked by the user, `[to do]`;
  `tree-first-level` `[doing]`; `g1-requirements-spec` before intake,
  `[doing]`.

## Blockers
- None.

## Next actions
1. `t4-release`: kit 0.17.0, USAGE's `tree-first-level` marks green, its
   CHANGELOG entry, `KIT_VERSION`, `pyproject.toml`, `.github/workflows/
   sdlc.yml`; Two-Key with `sweep: true`. Its sweep, named here since t4's
   done_means names none of it:
   - t1: "Six statuses" (`USAGE.md:632`) says a parent reads `to do` when
     nothing under it has started, which a gate item no longer does; the
     contract's SC1.1 sketch says "by the rule for the roll-up of a
     feature", looser than its sources; `709d2cc`'s message counts nine
     amended tests where the diff holds eight plus the release test;
     `Theory:` stands above the final paragraph, so git parses only
     `Contract:` as a trailer (the house form).
   - t2: `tree_view.py`'s module docstring (lines 7, 21-22, 29) gives a
     plain name, a doc reference and `holds` lines to contracts only;
     `tree.py:14` says the tree opens "each file directly under
     docs/features/", where it opens only `*.md`; `tree.py:87` runs to
     about 100 characters.
   - t3: `USAGE.md:994` (0.16.0's drift text) still leaves out only
     `Ready:` and `Measured:` rows, amended in words by the red paragraph
     that closes "Revisions and halves" (the user's pass-zero decision);
     USAGE's no-signature list (about line 1272) omits that a row of fewer
     than three cells signs nothing and that the signer is the cell before
     the last; `tree_view.py`'s docstring names neither the new marks nor
     a half's `file:` line; `tree.py:67` says a feature before intake
     "reads `done` only when every other child does" beside the sentence
     that it never reads `done`.
   Release shape as below; then the self-pin PR, which the wrap rides.
2. `feature-document`: interview `REQUEST_feature-document_2026-09-18.md`
   (untracked, r1 typed by hand, says "Ships as kit 0.14.0") into
   `docs/features/feature-document.md`, both halves signed, folding in
   ADRs 0033 and 0034 and the five open questions at `a800c34:STATE.md`
   (a check's false premise, a release unit with no check, the
   three-sketch cap, an appendix copy that ages, a `done_means` broader
   than its line). Then intake, the build (template, interview flows,
   readiness check, intake's definition of done, Gherkin derivation),
   release 0.18.0. Estimate seven to nine sessions.
3. Then G1's solution half, through the interview at the engineer seat,
   to ADR 0033; open for it: where the component declaration record and
   the review record live, G1's rules and their codes, the venue, and how
   the 15 features done read G1 inactive once G1 is active. Then its
   intake. The pilot's config line, in the engine's session; the engine's
   install ref moves to the newest tag there (pull, not push).
4. Prerequisite 7: feature documents for the 15 contracts without one,
   each through its own interview.
5. Small, parked: `taskcontract/__main__.py:85`'s `--follow` help still
   describes the 0.15.0 pane; Two-Key's wording advisories (CHANGELOG's
   and ADR 0032's "a closed contract reads done whatever its verdicts
   read" omit the later-record limit; USAGE's evidence paragraph reads
   best as "after its own close"; the no-red test covers section 9 only,
   and since `709d2cc` only project-tree's subsections up to the first red
   heading); two test gaps (no pane test for a `parts:` list without
   `evidence` hiding a seat; `tests/conftest.py`'s row pattern splits a
   plain name at its first ` [`).
6. Deferred, carried: `glossary-alias-disjointness` (parked by the user,
   2026-09-26); `derived-language` (prerequisite 5); ADR 0029's appendix
   copy and Gherkin for project-tree; flag the Claude pane itself; the
   hook's key action and its four known edges, in its README;
   `.sdlc/config.yaml` still lists `plan.workflow.json` as a free path;
   the advisories at `a800c34:STATE.md` Next actions 4; `spec-doc-type`;
   the demo intake; wave B; 5b; the G4.6 finding;
   `no-check-reads-the-source-document`; the prototype renderer's two gaps
   (`styled-rendering`).

## Standing practice
- At resume, read the pilot's `E:\ImSimProject\engine\STATE.md` beside
  this file: the engine hands work to the kit there, and its REQUESTs land
  untracked in this root.
- A new feature starts as a feature document written through an
  interview, in the format ADR 0029 ratified and 0033 and 0034 amended,
  tracked at `docs/features/<id>.md`; never a request typed from a sketch.
  Until `feature-document` lands, the interview runs by hand from
  `NOTES_feature-document_2026-09-18.md` and
  `NOTES_feature-document-amendment_2026-09-27.md`. A seat signs its half
  with a row `rN: Signed: request half` or `rN: Signed: solution half`,
  written right after the row it signs (ADR 0034). The checks before
  signing run from a scratch script: add the document's new terms as
  drafts to `load_terms`, report CL003 through
  `lang.validate_dictionary_doc`, and run `lang.check_contract` on a draft
  contract holding the statement, the non-goals and the checks; a
  `Violation`'s code is its `rule` field.
- A deferred item that waits on a prerequisite is measured again once the
  prerequisite lands, before it becomes work.
- Intake from a feature document: ratify its new terms first, in their
  own commit, with any ADR the document's prerequisites name. A term
  whose single-word name or slug equals a dictionary word trips CL003;
  the dictionary cedes the word in the same commit. Check each amended
  term's neighbors for a definition the change contradicts. Check the
  document's Scope against the release unit's needs:
  `skills/sdlc/init.py` (`KIT_VERSION`) and `.github/workflows/sdlc.yml`.
  Intake copies the document's title line into the contract's `title`,
  and derives from the newest text revision both seats signed, never from
  a `Signed:` row. A unit holds at most three sketches: pair two checks in
  one sketch ending in both ids.
- A plan is plan.md's numbered steps, shown in chat for the user's
  overview. A USAGE refinement never narrows a contract sentence
  silently: flag any narrowing or reading to the user before approval. A
  release rewrite that simplifies a rule gets checked against the code
  first.
- ADRs are append-only (`DOCS-SYSTEM.md:45`): a later ADR amends an
  earlier one in its own text, never an edit.
- Record each task as it finishes through `taskcontract progress`, and
  each check's run through `progress run <check> [--expect red] --
  <test command>` with `-k`. Run a check's green after its commit with no
  tracked file modified: commit a plan edit on its own first. Close each
  unit with `progress done` once its Two-Key passes. A failed round is
  `progress block <unit>/two-key --reason`, then `start` again. A release
  unit that writes no tests skips write-tests and prove-red.
- A REQUEST is untracked, so git cannot restore it: copy it to the
  scratchpad before a revision edits it.
- A delegated session: one Workflow per step, launched by `scriptPath`
  from `.claude/workflows/`. Keep each agent's reading narrow (the user
  stops an agent past about 400K tokens). `test-retirer.js` takes
  `overlay` (the prototype's changed files) when no name goes. The release
  unit's Two-Key runs with `sweep: true`. Every Two-Key receipt must exit
  0. Session 63's subagents: drafter 196K, retirer 66K, developers 111K,
  62K, 64K and 59K, Two-Key 198K and 204K a round.
- Before approving a drafted list: run the whole suite on the prototype
  in a scratch worktree (`git worktree add --detach`, overlay, `python -P
  -m pytest <worktree>/tests`); check each fixed detail against the
  contract, the feature document and its Constraints (session 63's round
  1 failed on Constraint 4, which no sketch names); pin caps against free
  text holding line breaks; strip session labels; check for a repeated
  name. An edge left unpinned must still agree with the USAGE text the
  user approved.
- Before accepting a developer deviation, test it against every
  done_means sentence. Run the suite yourself after every developer round;
  a developer whose suite run outlasts its turn leaves Claude's run as the
  receipt. A path wrapper left with no caller goes.
- A manual receipt (a live pane) is taken after the commit and handed to
  Two-Key as a focus pointer holding its text. The herdr probe: `herdr
  pane split --pane <own> --direction down --cwd <root> --no-focus`, `pane
  run <new> "python -m taskcontract tree --follow --root <root>"`, `pane
  wait-output <new> --match <text>`, `pane send-keys <new> down ...` to
  move, `pane read <new> --source visible`, `pane close <new>`. Own pane:
  `printenv HERDR_PANE_ID`. Never report state on another session's pane.
- The whole suite runs 3 to 6 minutes; a local model holding RAM can get
  a background run killed for memory.
- `scope-check` outside Actions needs `--base <sha>`: main's tip.
- Attribution is off: a commit's final paragraph is `Contract:` alone, and
  a PR body ends at its last sentence.
- Release shape: PR, merge commit, annotated tag at the merge, then the
  self-pin through its own PR, which the wrap rides. Run USAGE's `uv` line
  against the new tag. main's ruleset requires a PR for every change.

## Open questions
- The `intake-seat` term says a seat is never delegated to an agent, while
  a delegated session's approvals record `--by claude` (sessions 40 to 42,
  45 to 47, 52 to 54, 61 to 63). Does the term need a word for a
  delegated approval? Beside it: G0.3's unit confirmation repeated the
  engineer seat's signature on project-tree and tree-first-level.
- A feature before intake's id compares as an exact string, so on
  Windows `docs/features/Ready.md` beside `specs/ready/` shows as a
  second feature. Leave it, or match ids without case?
- `lang-check` does not resolve a plural of a glossary term (`features`
  against Feature, `halves` against Half).
- Should `page:` print a URL (the kit's repo at the pinned tag)?
- Push `E:\herdr-sdlc` to GitHub, so herdr can install it as a plugin?
- Which request carries `no-check-reads-the-source-document`?
- d6's two open advisories, wording only (USAGE section 8's
  `confirmed_by` label; the G0.2 hook test's replace).
- `taskcontract/__init__.py` says `__version__ = "0.3.0"`; nothing reads it.
- `/sdlc audit` drops a `W001` warning beside an error.
- Should TC016 ride the parked line?
- Track `.claude/workflows/`? Its four scripts hold the session method and
  exist only on this machine; the Two-Key grade prompt still names a
  Co-Authored-By line.
- Ratify 5b? The hook command per stack? The four metrics for wave B.
- The engine's `plan.md` holds an uncommitted edit; the engine session's
  to commit.
