# State - sdlc_development_kit

> **Contract** - one question: *what is in flight right now?*
> <=1 page - regenerate at every session end - disposable, always safe to overwrite.
> _Generated 2026-09-24 (session 49, the pane's feature document mid-interview)._

## Now
- **The pane work went back to the beginning.** Kit 0.15.0's tree and pane
  were built from requests typed from the user's 2026-09-21 sketch, never
  interviewed. tree-view's r1 dropped the sketch's gate conditions (g0.1
  to g0.3, each with a status and findings) with no ruling, and with no
  task in flight the pane reads two lines: `no current task`, `16 items:
  14 to do, 2 done`. The user ruled on 2026-09-24: a fleshed-out feature
  document before any build, the drift the kit exists to close.
- **`docs/features/project-tree.md`**, the feature document for
  `project-tree`, is mid-interview at r1, the request half. The interview
  runs by hand in the format ADR 0029 ratified
  (`NOTES_feature-document_2026-09-18.md`), since the kit's interview
  skill still asks ADR 0026's questions. Written: statement, description,
  background (the sketch verbatim, a 13-row trace against 0.15.0, the
  measured tree), seven existing behaviors each tagged with its
  regression check, five success criteria (SC4 makes the pane an outline
  moved through with the arrow keys and the mouse), eight non-goals, eight
  prerequisites (four missing, each with its owner), 14 checks, no new
  error message, nine decisions. Two OPENs stand: the terms (Q11, drafted
  in the appendix) and, for the engineer seat, where a feature's title
  comes from, since ADR 0029 keeps tooling off headings.
- `REQUEST_gate-outline_2026-09-23.md` (r1, untracked), the first plan's
  request from the sketch, is superseded by the document and stays as
  material.
- Branch `session-49-pane-spec` holds `2311a17` (open), `979f2f0`
  (replan) and this wrap, unpushed. main is at `7c79ba3` (PR #58, session
  48's wrap); `v0.15.0` tags `fdd6fe2`.
- The user's tree pane (`w9:p8`) runs the code it started with; restart it
  to run 0.15.0's.

## Blockers
- None.

## Next actions
1. Session 50: resume the interview at Q11, the terms drafted in the
   document's appendix. Then readiness: the format's checks 1 to 8 read
   back, OPEN marks on the user's word, and the PO seat's signature as a
   revision row.
2. Then the solution half (proposed solution, risks and cost), signed by
   the engineer seat, which answers the title OPEN. SC4 makes the pane an
   interactive program (keys and mouse, on Windows and POSIX), so risks
   and cost weigh a new dependency against the kit's own input handling.
   Then `/sdlc intake docs/features/project-tree.md`.
3. Push `session-49-pane-spec` and open its PR, on the user's word; merge
   by merge commit once CI reads green.
4. G1, after project-tree is built, so the pane shows G1's conditions.
   The pilot's config line, in the engine's session; the engine's install
   ref moves to `v0.15.0` there (pull, not push).
5. Deferred: the backfill of the 13 earlier contracts (project-tree's
   prerequisite 8); the kit's feature documents where the tree finds them
   (prerequisite 7); `derived-language` (prerequisite 5); flag the Claude
   pane itself; the hook's key action and its four known edges, in its
   README; `.sdlc/config.yaml` still lists `plan.workflow.json` as a free
   path.
6. Carried advisories on `tree_view.py`, USAGE and CHANGELOG, wording and
   behavior notes: listed in full at `a800c34:STATE.md`, Next actions 4.
7. Carried: `feature-document`, `spec-doc-type`; the demo intake; wave B
   (`playbook-loop`, V1-V6); 5b; the G4.6 finding;
   `no-check-reads-the-source-document`; from r3, a status field on the
   finding form and the agent personas writing progress.

## Standing practice
- At resume, read the pilot's `E:\ImSimProject\engine\STATE.md` beside
  this file: the engine hands work to the kit there, and its REQUESTs land
  untracked in this root.
- A new feature starts as a feature document written through an
  interview, in the format ADR 0029 ratified, tracked at
  `docs/features/<id>.md`; never a request typed from a sketch (user,
  2026-09-24). Until `feature-document` lands, the interview runs by hand
  from `NOTES_feature-document_2026-09-18.md`: one question at a time, a
  vague answer probed once, each section summarized and written into the
  document before the next, candidates drafted only from the user's own
  words, each citing its source.
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
  passes, and the contract once its last unit closes. A unit with no test
  (a USAGE pass) starts `green` while its page is written and
  `approve-commit` while it waits. Progress files are git-ignored.
- A REQUEST is untracked, so git cannot restore it: copy it to the
  scratchpad before a revision edits it.
- The language door checks every sentence of a sketch for an approved
  opening verb; open each one on "verify". Filter its output to one
  contract (a ten-line script over `lang-check`); the rest is the exempt
  findings of six pre-arc contracts.
- A delegated session: one Workflow per step, launched by `scriptPath`.
  `.claude/workflows/` holds the drafter (`spec-channel-drafter.js`), the
  developer (`unit-developer.js`) and Two-Key. The drafter proves red from
  the scratchpad and builds a prototype; Claude approves, places the tests
  and proves red; the developer greens from the interface note without
  opening `tests/`; Claude reviews, runs the receipts, commits and runs
  Two-Key, leaving tracked files alone while it runs. A fix round: Claude
  amends or adds tests as the list's approver, red first; the developer
  fixes from a delta note; the fix is its own commit, and the next round
  grades every commit of the unit. Session 47's subagents: drafter 165K;
  developers 105K, 65K, 67K and 52K; Two-Key 190K to 242K a round.
- Before approving a drafted list: check each fixed detail against every
  use of its terms in the contract and the REQUEST, and pin any output
  cap against free text holding line breaks (session 47 lost two t6
  rounds to these); strip session labels (`ruling_2`) from test names;
  check the module for a repeated test name; diff earlier tests.
- `scope-check` outside Actions needs `--base <sha>`: main's tip.
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
  session 46's STATE, `205bbd5:STATE.md`).
- A settings file with unrelated uncommitted edits is staged by blob
  (`hash-object`, then `update-index`), so the commit holds one change.

## Open questions
- A feature document's title is a heading, which ADR 0029 keeps tooling
  from reading, yet project-tree shows it as each feature's plain name:
  where does the title come from (the document's engineer-seat OPEN)?
- Move the kit's feature documents from untracked root REQUESTs to
  `docs/features/<id>.md`, so the tree finds them (project-tree's
  prerequisite 7)?
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
  and the ratified format lives only in the session 32 notes (session 49
  ran the interview by hand); a check can carry a false premise about
  today's behavior; a closing release unit has no check to deliver;
  checks and sketches are not one to one under the three-sketch cap; a
  pasted appendix copy ages at once; a derived `done_means` can read
  broader than its line.
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
