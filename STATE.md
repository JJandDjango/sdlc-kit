# State - sdlc_development_kit

> **Contract** - one question: *what is in flight right now?*
> <=1 page - regenerate at every session end - disposable, always safe to overwrite.
> _Generated 2026-09-25 (session 51 close, project-tree at intake)._

## Now
- **Contract `project-tree` is ready-green** at `1618daa`, derived at
  intake from `docs/features/project-tree.md` r3. The document's r4 is
  intake's "Ready:" row, written by hand this once in the fixed shape o3
  will parse, and its status line reads ready. Seven units, o1 to o7, each
  `confirmed_by: [user]`; 14 sketches, one per check; 29 entities. The
  engineer seat added `skills/sdlc/init.py` and
  `.github/workflows/sdlc.yml` to scope, for o7's version bump and
  self-pin. No `title` field until o2 adds it to the schema.
- The glossary gained the document's 22 terms at `ac19ee4`: 40 terms, all
  ratified. `dictionary.yaml` ceded diagnostic, feature, finding, item,
  rule, status, task and tree (CL003), and `verdict` now calls a rule's
  coded records diagnostics.
- The language door's rewrites, for the drafter to read beside the
  document: a click reads "a touch of the pointer", "opens" reads "makes
  ... open", the revision table reads "the table of changes", and the
  first non-goal dropped "no new authorizations" (the dictionary has no
  word for it). The document stays the reference for each.
- PR #60 carries session 51 (branch `session-51-project-tree-intake`),
  merged by merge commit once CI reads green, on the user's word. main
  was at `7f2b5c1`; `v0.15.0` tags `fdd6fe2`.
- The Google Doc render of r3 predates r4, which changed only the Ready
  row and the status line. `REQUEST_gate-outline_2026-09-23.md`
  (untracked) stays as material. The user's tree pane (`w9:p8`) runs the
  code it started with; restart it to run 0.15.0's.

## Blockers
- None.

## Next actions
1. Session 52: build `o1-conditions` by the delegated method. Then o2,
   o3 and o4 in any order, o5 after all three, o6, and o7, which ships
   0.16.0. o5 and o6 need Textual in the test env (it joins the `test`
   extra at o5). About three build sessions.
2. o3 teaches intake to write the "Ready:" row; until it lands, write the
   row by hand in its fixed shape, `rN: Ready: ... derived from rM ...`.
3. G1 after project-tree ships, so the pane follows G1's conditions. The
   pilot's config line, in the engine's session; the engine's install
   ref moves to the new tag there (pull, not push).
4. Deferred: prerequisites 7 to 9 (the kit's feature documents under
   `docs/features/`; progress for the 13 older contracts; a title in each
   contract, now 16 with project-tree's own); `derived-language`
   (prerequisite 5); ADR 0029's appendix copy and Gherkin for
   project-tree, with `feature-document`'s open question; flag the Claude
   pane itself; the hook's key action and its four known edges, in its
   README; `.sdlc/config.yaml` still lists `plan.workflow.json` as a free
   path.
5. Carried advisories on `tree_view.py`, USAGE and CHANGELOG, wording and
   behavior notes: listed in full at `a800c34:STATE.md`, Next actions 4.
6. Carried: `feature-document`, `spec-doc-type`; the demo intake; wave B
   (`playbook-loop`, V1-V6); 5b; the G4.6 finding;
   `no-check-reads-the-source-document`; from tree-view r3, a status
   field on the finding form and the agent personas writing progress;
   on `styled-rendering`, the prototype renderer's two gaps (it drops
   blockquotes into one paragraph, and its numbered lists count on from
   each other), fixed in session 50's scratchpad copy by an indented
   `quote` block and literal list numbers.

## Standing practice
- At resume, read the pilot's `E:\ImSimProject\engine\STATE.md` beside
  this file: the engine hands work to the kit there, and its REQUESTs land
  untracked in this root.
- A new feature starts as a feature document written through an
  interview, in the format ADR 0029 ratified, tracked at
  `docs/features/<id>.md`; never a request typed from a sketch (user,
  2026-09-24). Until `feature-document` lands, the interview runs by hand
  from `NOTES_feature-document_2026-09-18.md`: one question at a time, a
  vague answer probed once, each section written into the document
  before the next, candidates drafted only from the user's own words.
  The solution half runs the same way: one decision a message, the
  mechanical ones batched, each with its consequence for the request
  half, which collects into one re-signed revision.
- Intake from a feature document: ratify its new terms first, in their
  own commit, since `entities` resolves ratified terms only. A term whose
  single-word name or slug equals a dictionary word trips CL003, drafts
  included; the dictionary cedes the word in the same commit (removal is
  its auto lane). Check the document's Scope against the release unit's
  needs: `skills/sdlc/init.py` (`KIT_VERSION`) and
  `.github/workflows/sdlc.yml` (the self-pin).
- A plan is plan.md's numbered steps, shown in chat for the user's
  overview; nothing renders it. Work outside a contract unit does not show
  in the pane; the plan says so.
- Record each task as it finishes: `progress start|done <task>`, `--by
  <seat>` on an approval, and each check's run through `progress run
  <check> [--expect red] -- <test command>`, selecting its tests with `-k`
  (test names carry the check id). Run a check's green after its commit,
  so the evidence names a clean commit. Record a failed Two-Key round as
  `progress block <unit>/two-key --reason`, and start it again for the
  next round. Close each unit with `progress done` once its Two-Key
  passes, and the contract once its last unit closes. Progress files are
  git-ignored.
- A REQUEST is untracked, so git cannot restore it: copy it to the
  scratchpad before a revision edits it.
- The language door checks every sentence of a sketch for an approved
  opening verb; open each one on "verify". Filter its output to one
  contract (a ten-line script over `lang-check --json`); the rest is the
  exempt findings of six pre-arc contracts. Probe words against the real
  lexicon (`taskcontract.lang._Lexicon`) before drafting.
- A delegated session: one Workflow per step, launched by `scriptPath`.
  `.claude/workflows/` holds the drafter (`spec-channel-drafter.js`), the
  developer (`unit-developer.js`) and Two-Key. The drafter proves red from
  the scratchpad and builds a prototype; Claude approves, places the tests
  and proves red; the developer greens from the interface note without
  opening `tests/`; Claude reviews, runs the receipts, commits and runs
  Two-Key, leaving tracked files alone while it runs. A fix round: Claude
  amends or adds tests as the list's approver, red first; the developer
  fixes from a delta note; the fix is its own commit, and the next round
  grades every commit of the unit.
- Before approving a drafted list: check each fixed detail against every
  use of its terms in the contract and the feature document, and pin any
  output cap against free text holding line breaks; strip session labels
  (`ruling_2`) from test names; check the module for a repeated test
  name; diff earlier tests.
- `scope-check` outside Actions needs `--base <sha>`: main's tip. A commit
  that touches only `specs/` needs no `Contract:` trailer, and one naming
  a contract that does not exist yet reads SC003.
- Run the release unit's sweep patterns before its verifier round; a hit
  outside scope goes to an OPEN and a re-intake first. Date any example of
  live output to its moment.
- Attribution is off: a commit's final paragraph is `Contract:` alone, and
  a PR body ends at its last sentence.
- Release shape: PR, merge commit, annotated tag at the merge, then the
  self-pin through its own PR, which the wrap rides; open that PR before
  writing the wrap, so STATE names its number. Run USAGE's `uv` line as
  written against the new tag: CI covers only the `pip` install. main's
  ruleset requires a PR for every change. `gh pr checks --watch` can exit
  1 on "no checks reported"; start it again.
- herdr probes run in panes Claude splits with `--no-focus` and closes
  after; never report state on another session's pane (the recipe is in
  session 46's STATE, `205bbd5:STATE.md`). `herdr pane send-keys <pane>
  down right ...` drives a probe's keys; clicks and the wheel need the
  user.
- A settings file with unrelated uncommitted edits is staged by blob
  (`hash-object`, then `update-index`), so the commit holds one change.

## Open questions
- The `intake-seat` term says a seat is never delegated to an agent, while
  a delegated session's approvals record `--by claude` (sessions 40 to 42,
  45 to 47). Does the term need a word for a delegated approval?
- Should `page:` print a URL (the kit's repo at the pinned tag), so a
  consumer's agent can open a kit page?
- Push `E:\herdr-sdlc` to GitHub, so herdr can install it as a plugin
  later? It has no remote.
- Which request carries `no-check-reads-the-source-document`:
  `derived-language` or its own?
- d6's two open advisories, wording only: USAGE section 8 labels
  `confirmed_by` "optional in the schema", and the G0.2 hook test does not
  assert that its replace changed the text.
- `taskcontract/__init__.py` says `__version__ = "0.3.0"`; nothing reads it.
- To `feature-document`: the interview skill asks ADR 0026's questions,
  and the ratified format lives only in the session 32 notes (sessions 49
  and 50 ran the interview by hand); a check can carry a false premise
  about today's behavior; checks and sketches are not one to one under
  the three-sketch cap; a pasted appendix copy ages at once (session 51
  skipped project-tree's); a derived `done_means` can read broader than
  its line; a unit must deliver a check (check 9), so a USAGE pass zero
  folds into the first unit and a release unit takes a regression check.
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
