# State - sdlc_development_kit

> **Contract** - one question: *what is in flight right now?*
> <=1 page - regenerate at every session end - disposable, always safe to overwrite.
> _Generated 2026-09-27 (session 58 close, G1's request half)._

## Now
- **G1's feature document: the request half is signed** by the PO seat at
  r3 (`docs/features/g1-requirements-spec.md`), the first document written
  to ADR 0033. Five criteria: the G1.3 review, schema linting, model
  checking, G1 before development (intake names G1 next, and no unit's
  task starts before G1 passes), and the tree. Seven non-goals, among them
  no agent attests G1.3 and no G1 review for the 15 features done.
- Three terms settled at Q9: an unchecked review item is a diagnostic
  (Finding keeps its meaning, about the kit); G1's rules are validator
  tests that read the recorded results (the ratified Rule); Ready check is
  its own term.
- The checks before signing (r2): `component` and `venue` trip CL003, and
  the dictionary cedes both at intake; 86 language findings are left to
  intake's rewrite of the contract's wording.
- On branch `session-58-g1-feature-document`; the commit, push and PR on
  the user's word. Session 57's PR #68 merged at `af8c261`.
- Carried: 15 features read `[done]`; `glossary-alias-disjointness` is
  parked by the user, `[to do]`.

## Blockers
- None.

## Next actions
1. G1's solution half, through the interview at the engineer seat, to
   ADR 0033: Sources, Examples, Retirements, tests by check id and kind,
   order with its reason, and the checks before signing (Scope against the
   release unit's paths). Open for it: where the component declaration
   record and the review record live, G1's rules and their codes, the
   venue, and how the 15 features done read G1 inactive once G1 is active.
   Then intake. The pilot's config line, in the engine's session; the
   engine's install ref moves to `v0.16.0` there (pull, not push).
2. Prerequisite 7: feature documents for the 15 contracts without one,
   each through its own interview.
3. `feature-document` absorbs ADR 0033 into the template, the interview's
   flow and the readiness check, when it is built.
4. The tree's `gates/G0` item reads `to do` with no finding filed,
   whatever each feature's G0 verdict reads (found session 58; a gap in
   project-tree's requirements): decide what its status means.
5. Small, parked: `taskcontract/__main__.py:85`'s `--follow` help still
   describes the 0.15.0 pane; Two-Key's wording advisories (CHANGELOG's
   and ADR 0032's "a closed contract reads done whatever its verdicts
   read" omit the later-record limit; USAGE's evidence paragraph reads
   best as "after its own close"; the no-red test covers section 9
   only); two test gaps (no pane test for a `parts:` list without
   `evidence` hiding a seat; `tests/conftest.py`'s row pattern splits a
   plain name at its first ` [`).
6. Deferred, carried: `glossary-alias-disjointness` (parked by the user,
   2026-09-26); `derived-language` (prerequisite 5); ADR 0029's
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
  interview, in the format ADR 0029 ratified and 0033 amended, tracked at
  `docs/features/<id>.md`; never a request typed from a sketch. Until
  `feature-document` lands, the interview runs by hand from
  `NOTES_feature-document_2026-09-18.md` and
  `NOTES_feature-document-amendment_2026-09-27.md`. The checks before
  signing run from a scratch script: add the document's new terms as
  drafts to `load_terms`, report CL003 through
  `lang.validate_dictionary_doc`, and run `lang.check_contract` on a draft
  contract holding the statement, the non-goals and the checks.
- A deferred item that waits on a prerequisite is measured again once the
  prerequisite lands, before it becomes work (the tree's order, session
  57).
- Intake from a feature document: ratify its new terms first, in their
  own commit. A term whose single-word name or slug equals a dictionary
  word trips CL003; the dictionary cedes the word in the same commit.
  Check the document's Scope against the release unit's needs:
  `skills/sdlc/init.py` (`KIT_VERSION`) and `.github/workflows/sdlc.yml`.
  Intake copies the document's title line into the contract's `title`.
- A plan is plan.md's numbered steps, shown in chat for the user's
  overview. Several units' USAGE text can be approved in one batch before
  any drafting. A USAGE refinement never narrows a contract sentence
  silently: Two-Key grades the contract, not USAGE, so flag any narrowing
  or reading to the user before approval. A release rewrite that
  simplifies a rule gets checked against the code first (o7 round 1).
- ADRs are append-only (`DOCS-SYSTEM.md:45`): a later ADR amends an
  earlier one in its own text, as 0032 does 0031, never an edit.
- Record each task as it finishes through `taskcontract progress`, and
  each check's run through `progress run <check> [--expect red] --
  <test command>` with `-k`. Run a check's green after its commit with no
  tracked file modified. Close each unit with `progress done` once its
  Two-Key passes; a contract close marks every task and check under it
  done. A release unit that writes no tests skips write-tests and
  prove-red, as t9 and o7 did.
- A REQUEST is untracked, so git cannot restore it: copy it to the
  scratchpad before a revision edits it.
- A delegated session: one Workflow per step, launched by `scriptPath`
  from `.claude/workflows/`. Keep each agent's reading narrow: the user
  stops an agent past about 400K tokens as a hallucination risk. Split a
  unit whose drafting needs both new behavior and a retirement:
  `test-retirer.js` deletes the code in an export, runs the suite and
  reads only the tests that fail. The release unit's Two-Key runs with
  `sweep: true`.
- Before approving a drafted list: run the whole suite on the prototype
  in a scratch worktree (`git worktree add --detach`, overlay, run with
  `python -P -m pytest <worktree>/tests`); check each fixed detail against
  the contract and the feature document; pin caps against free text
  holding line breaks; strip session labels from test names; check for a
  repeated name; check that every `done` rests on a rule that ran; check
  one drafter's label assertions against another's new label parts.
- Before accepting a developer deviation, test it against every
  done_means sentence. After a fix that reverses an order or a rule,
  search the test docstrings for the old statement. Run the suite
  yourself after every developer round.
- The whole suite runs 3 to 6 minutes; a local model holding RAM can get
  a background run killed for memory.
- `scope-check` outside Actions needs `--base <sha>`: main's tip.
- Attribution is off: a commit's final paragraph is `Contract:` alone, and
  a PR body ends at its last sentence.
- Release shape: PR, merge commit, annotated tag at the merge, then the
  self-pin through its own PR, which the wrap rides. Run USAGE's `uv` line
  against the new tag. main's ruleset requires a PR for every change.
- herdr probes run in panes Claude splits with `--no-focus`; `herdr pane
  run` makes the command the pane's program, so the pane closes when it
  exits. Never report state on another session's pane.

## Open questions
- The `intake-seat` term says a seat is never delegated to an agent, while
  a delegated session's approvals record `--by claude` (sessions 40 to 42,
  45 to 47, 52 to 54). Does the term need a word for a delegated approval?
  Beside it: G0.3's unit confirmation repeated the engineer seat's
  signature on project-tree (ADR 0033's recorded non-goal).
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
  exist only on this machine; the Two-Key grade prompt still names a
  Co-Authored-By line.
- Ratify 5b? The hook command per stack? The four metrics for wave B.
- The engine's `plan.md` holds an uncommitted edit; the engine session's
  to commit.
