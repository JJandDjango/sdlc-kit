# State - sdlc_development_kit

> **Contract** - one question: *what is in flight right now?*
> <=1 page - regenerate at every session end - disposable, always safe to overwrite.
> _Generated 2026-09-23 (session 47 close)._

## Now
- **tree-view is built; 0.15.0 waits on its release.** Branch
  `session-47-tree-view-t6-t9` holds t6 (`c1380d5`, fixed at `ba4c117`
  and `7945f13`, Two-Key PASS at round 3) and t9 (`497418a`, fixed at
  `bf18594` and `c48ae8c`, PASS at round 2 with the release sweep). All
  ten units and the contract are closed in progress. Suite 592 passed,
  fifteen contracts ready-green, scope-check green from `84ebc5e`.
- t6 is `taskcontract tree <id>`: one block of at most seven lines per
  item. Its round 1 failed on the `doc:` line (SC4.2 calls a feature doc
  a file reference, so it carries `:1`); round 2 on line breaks in free
  text (a `--reason`, seat, command or finding kind) passing the cap,
  fixed at the root: `line()` reads every field by the text rule on every
  face. Claude added three tests as the list's approver, each red first.
  t9's round 1 failed on one sentence naming a close's evidence without
  its condition. The user approved t9's commit.
- PR #57 carries the branch, opened at this close on the user's word
  ("stop at PR"); the release is session 48's.

## Blockers
- None. The merge, the tag and the self-pin wait on the user's word.

## Next actions
1. Session 48, the release: merge PR #57 by merge commit on the user's
   word once CI reads green, tag `v0.15.0` (annotated) at the merge, then the
   self-pin through its own PR: `.github/workflows/sdlc.yml` and USAGE
   section 7's `uv run` line move to `@v0.15.0`, as `af9e587` did for
   0.14.0. Then restart the user's tree pane (`w9:p8`).
2. G1 after the release: its criteria review comes before the pilot's M0
   code.
3. The pilot's config line, in the engine's session.
4. Deferred: flag the Claude pane itself (a local `claude.toml` detection
   rule shadowing herdr's remote one, or a herdr change); the hook's key
   action; the hook's four known edges, in its README; `.sdlc/config.yaml`
   still lists `plan.workflow.json` as a free path.
5. Carried advisories, wording unless noted. `tree_view.py`: the module
   docstring's 127 means the shell itself cannot start; `follow()`'s
   Ctrl-C note names only POSIX; `_flat()`'s docstring understates (it
   keeps trailing space too); the private `_no_node` import. USAGE: `run`
   refuses before it starts the command, save its `cannot start` line,
   and an argparse error prints two lines; a closed unit reads `done`
   only while the close is its latest record; the width cut never goes
   below 10 columns. CHANGELOG: drop "now" from the repeated-link note.
   Behavior, not t6's: the pane's waiting, where-am-I and fold-name
   lines pass a line break held inside an id; a task and a check that
   share an id also share their progress readings (`_apply` and `derive`
   key by id); `page:` prints a kit-repo path that does not open in a
   consumer. Noted: a cached `G0` reading goes stale across a deprecated
   term's sunset date; `cut()` counts characters, not display columns.
6. Carried: the backfill of the 13 earlier contracts, once each is checked
   finished; `derived-language`, `feature-document`, `spec-doc-type`; the
   demo intake; wave B (`playbook-loop`, V1-V6); 5b; the G4.6 finding;
   `no-check-reads-the-source-document`; from r3, a status field on the
   finding form and the agent personas writing progress.

## Standing practice
- At resume, read the pilot's `E:\ImSimProject\engine\STATE.md` beside
  this file: the engine hands work to the kit there, and its REQUESTs land
  untracked in this root.
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
  self-pin through its own PR; main's ruleset requires a PR for every
  change. `gh pr checks --watch` can exit 1 on "no checks reported"; start
  it again.
- herdr probes run in panes Claude splits with `--no-focus` and closes
  after; never report state on another session's pane (the recipe is in
  session 46's STATE, `205bbd5:STATE.md`).
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
