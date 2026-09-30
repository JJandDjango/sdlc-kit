# State - sdlc_development_kit

> **Contract** - one question: *what is in flight right now?*
> <=1 page - regenerate at every session end - disposable, always safe to overwrite.
> _Generated 2026-09-30 (session 68 close, feature-document f1 built)._

## Now
- **`f1-format` is built and closed** (session 68, branch
  `session-68-feature-document-f1`): USAGE's interview subsection at
  `6e0b381`, rewritten for f1 to f4 with every mark red; the skill and
  tests at `0e1514e`. The interview's template holds ADR 0029's format
  as 0033 to 0036 amend it, the document lands at `docs/features/<id>.md`
  as r1 at O6, the state file at `docs/features/<id>.state.yaml`
  (`spec-interview-state/2`), and output's render at the end retired.
  Two-Key PASS at round 1, suite 766. Four units remain: `f2-sections`
  (SC1.2, SC3.1, SC3.2+SC3.3), `f3-signing` (SC1.3, SC2.1, SC2.2+SC2.3,
  with `lang-check --draft`), `f4-intake` (SC4.1 to SC4.3, with the tree's
  `Parked:` reading), `f5-release` (SC5.1, SC5.2). Two manual receipts: a
  live run through both signatures (SC1.3), intake parking on it (SC4.1).
- Interim state until f2 and f3, by design: `flows/sections.md` still asks
  ADR 0026's Q1 to Q12 and `flows/readiness.md` its five rules, against
  the new template.
- The contract at intake (session 67): ADR 0036 and 15 terms at
  `fde018d`, the contract at `63508f2`, six readings kept at readback.
- Risk 5 stands: the interview never picks up a document it did not
  start, so G1's solution half is written by hand from the two NOTES
  files.
- Kit 0.17.0 is released and self-pinned (PR #76 merged at `e833283`).
  The user's order (2026-09-29) stands: `feature-document` (0.18.0) before
  G1's solution half. When it ships, tell the user the kit is ready on
  the other machine, with the tag to install. Until then another machine
  installs `v0.17.0` and runs the interview by hand from the two
  `NOTES_feature-document_*` files.
- Carried: 19 features: 18 with a contract, 16 of them `[done]`;
  `glossary-alias-disjointness` parked by the user, `[to do]`;
  `feature-document` `[doing]`, f1 closed; `g1-requirements-spec` before
  intake, `[doing]`.

## Blockers
- None. The session's push and PR wait on the user's word.

## Next actions
1. Build `feature-document`'s remaining units in order, one per session
   (session 69 on: `f2-sections`), then release 0.18.0: three sessions.
   Each unit's Retirements row names what test-retirer should find. Every
   prompt file a unit touches passes `python -m prompt_lang` and stays
   under 12,000 characters (Constraints 1). f1's Two-Key advisories, for
   f2 and f3 to settle:
   - O6 fills no stamp in the derived tags (`[Intake · derived from
     r{n}]` under Record, `[PO seat · derived from r{n}]` under Gherkin),
     so an r1 document carries a literal `r{n}`; say what a block not yet
     derived reads (f2 for the Gherkin, f3 for the stale rule).
   - O6 writes "(none)" into every section not yet asked, the words a
     section with nothing to say reads; f2 decides the placeholder.
   - No flow writes an OPEN mark inline since W1 retired;
     `readiness.md:25` still says to write the document; `sections.md`
     records ADR 0026's answer keys; O4 names `sections.md` Q9 as the
     solution half (true once f2 lands).
   - Wording, for f5's sweep: `SKILL.md:44` and `USAGE.md:139` say
     "then eighteen sections" after the status line, but ADR 0029's
     eighteen count the table, the title and the status line.
2. Then G1's solution half, by hand from the two NOTES files (the
   interview never picks up a document it did not start, feature-document
   risk 5), to ADRs 0033 and 0036; open for it: where the component declaration record and
   the review record live, G1's rules and their codes, the venue, and how
   the 16 features done read G1 inactive once G1 is active. Then its
   intake. The pilot's config line, in the engine's session; the engine's
   install ref moves to the newest tag there (pull, not push).
3. Prerequisite 7: feature documents for the 15 contracts without one,
   each through its own interview.
4. Small, parked: `test-retirer.js` has its agent wait on the whole
   suite, and the run dies when the agent returns (session 68); hand the
   suite run to the session. t4's four Two-Key advisories (USAGE:904's "The `G0`
   verdict still reads from the validator" unqualified; wrap nits at
   USAGE:686, :1101, :1142; the ratified Diagnostic term,
   `specs/vocabulary/diagnostic.yaml`, still says "under its condition",
   which only a ratification changes); `taskcontract/__main__.py:85`'s
   `--follow` help still describes the 0.15.0 pane; Two-Key's wording
   advisories (CHANGELOG's and ADR 0032's "a closed contract reads done
   whatever its verdicts read" omit the later-record limit); two test gaps
   (no pane test for a `parts:` list without `evidence` hiding a seat;
   `tests/conftest.py`'s row pattern splits a plain name at its first
   ` [`).
5. Deferred, carried: `glossary-alias-disjointness` (parked by the user,
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
  interview, in the format ADR 0029 ratified and 0033 to 0036 amended,
  tracked at `docs/features/<id>.md`; never a request typed from a sketch.
  Until `feature-document` lands, the interview runs by hand from
  `NOTES_feature-document_2026-09-18.md` and
  `NOTES_feature-document-amendment_2026-09-27.md`. A seat signs its half
  with a row `rN: Signed: request half` or `rN: Signed: solution half`,
  written right after the row it signs (ADR 0034). The checks before
  signing run from a scratch script: add the document's new terms as
  drafts to `load_terms`, report CL003 through
  `lang.validate_dictionary_doc`, and run `lang.check_contract` on a draft
  contract holding the statement, the non-goals, the checks and each
  unit's `done_means` (the Units table's Done means cell, which intake
  copies word for word); a `Violation`'s code is its `rule` field.
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
  one sketch ending in both ids. Each `done_means` is copied word for word
  from the document's Units table (ADR 0036). For the language door, a
  scratch script builds `lang._Lexicon(load_repo_dictionary,
  load_terms)`, runs `check_contract` on a draft outside `specs/`, and
  probes words; scaffold only after the draft reads zero.
- A plan is plan.md's numbered steps, shown in chat for the user's
  overview. A USAGE refinement never narrows a contract sentence
  silently: flag any narrowing or reading to the user before approval. A
  release rewrite that simplifies a rule gets checked against the code
  first.
- A release sweep reads each changed page end to end against the code,
  besides a `git grep` per stale class: grep finds a sentence by its
  words, and a table row or a general "a verdict" carries none of the
  words a new kind of item brings (session 64 lost three rounds to it).
  Sweep test docstrings too; the grader counts them as shipped.
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
  0. Session 64's Two-Key rounds: 278K, 242K, 254K and 243K; session
  68's f1: 226K. A workflow agent's whole-suite run can die when the
  agent returns: run it in the session and classify from its output. For
  a prompt-only unit, the drafter's prototype is a scratch copy of the
  skill folder, not the `taskcontract` package (say so in its `notes`).
- Before approving a drafted list: run the whole suite on the prototype
  in a scratch worktree (`git worktree add --detach`, overlay, `python -P
  -m pytest <worktree>/tests`); check each fixed detail against the
  contract, the feature document and its Constraints; pin caps against
  free text holding line breaks; strip session labels; check for a
  repeated name. An edge left unpinned must still agree with the USAGE
  text the user approved.
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
  a background run killed for memory. A PR's CI waits through `gh pr
  checks <n> --watch` in the background.
- `scope-check` outside Actions needs `--base <sha>`: main's tip.
- Attribution is off: a commit's final paragraph is `Contract:` alone, and
  a PR body ends at its last sentence.
- Release shape: PR, merge commit, annotated tag at the merge, then the
  self-pin through its own PR, which the wrap rides. Run USAGE's `uv` line
  against the new tag with `python -P`. main's ruleset requires a PR for
  every change.

## Open questions
- `lang` skips an ALL-CAPS token before it matches a glossary phrase, so
  "OPEN mark" never matches its own term (`mark` reads unknown); the
  contract says "an OPEN". Fix in `lang.py`, or leave?
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
  Co-Authored-By line, and another machine has none of them.
- Ratify 5b? The hook command per stack? The four metrics for wave B.
- The engine's `plan.md` holds an uncommitted edit; the engine session's
  to commit.
