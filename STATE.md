# State - sdlc_development_kit

> **Contract** - one question: *what is in flight right now?*
> <=1 page - regenerate at every session end - disposable, always safe to overwrite.
> _Generated 2026-09-23 (session 46 close)._

## Now
- **pane-view is built**: p3 and p4 on branch `session-46-pane-view-p3-p4`,
  each Two-Key PASS at round 1: p3 `4e298af` (`tree: pane: parts:`, and the
  pane test helpers moved to `tests/conftest.py` as `ROW`, `cut_lines`,
  `short_line`), p4 `3be9db2` (`tree: pane: fold: names`). All five units
  and the contract are closed in progress. Suite 577 passed, all fifteen
  contracts ready-green, scope-check green from `ee05d24`.
- The live check after p4 passed: a probe pane on a scratch copy at t6's
  first approval, with `parts: [status, marks]` and `fold: names`, drew the
  request's example line for line (`15 more` for its `14 more`), and the
  hook flagged it `sdlc`, `blocked`; `fold: Names` brought the counts back
  with its message at the next render.
- The user's tree pane (`w9:p8`) runs the code it started with; restart it
  after the merge to see p1 to p4. The kit's own config sets neither key.
- PR #56 carries the branch, merged on the user's word (2026-09-23) once
  CI read green; PR #55 (session 45) merged at `ee05d24`.

## Blockers
- None.

## Next actions
1. Session 47: tree-view's t6 (the query face), then t9 (the release,
   0.15.0), by the delegated method; t9's USAGE pass turns p0's marks green.
2. G1 after t9: its criteria review comes before the pilot's M0 code.
3. The pilot's config line, in the engine's session.
4. Deferred: flag the Claude pane itself (a local `claude.toml` detection
   rule shadowing herdr's remote one, or a herdr change); the hook's key
   action; the hook's four known edges, in its README; `.sdlc/config.yaml`
   still lists `plan.workflow.json` as a free path.
5. Carried advisories. t6: `tree.py`'s docstring says a close reads
   everything under it done (tasks and checks only); t1's id collision; a
   repeated `depends_on` entry prints twice; `tree_view.py`'s docstring on
   spacing. t9, USAGE: the `progress` rows (`--expect green`, the exit-2
   refusals, a malformed file stopping a writer, the task writers' options
   and evidence), the `G0` verdict's dirty rule, no `dirty` key outside
   git, "done all the way down", the notes from t0, t1 and t3; the pane's
   text (the width cut, `no current task`, the watched files, the verdict
   cache, a vocabulary change showing in up to about 2.4 s, the waiting
   line, notify at the pane's start, exit 127, the failure line whole on
   stderr); "The pane's lines" example reads `14 more`, now `15 more`
   (p0's Two-Key); the fold message names `{value}` as YAML reads it, not
   "as written" (`fold: yes` prints `True`; p3's parts message does the
   same), so the page's words change (p4's Two-Key); a resize alone does
   not redraw the pane, so a line cut at the old width wraps until the
   next change (the live check). t9, code wording: `follow()`'s docstring
   on Ctrl-C (on POSIX the notify child gets the same SIGINT); `--follow`'s
   help, "at each arrival at an approval"; `tree_view.py`'s module
   docstring runs its parts: and fold: paragraphs into the cut sentence
   with no blank line, and its first paragraph names only counts on the
   fold lines (p4's Two-Key). Noted: a cached `G0` reading goes stale
   across a deprecated term's sunset date; `cut()` counts characters, not
   display columns.
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
  so the evidence names a clean commit. Close each unit with `progress
  done` once its Two-Key passes, and the contract once its last unit
  closes. A unit with no test (a USAGE pass) starts `green` while its page
  is written and `approve-commit` while it waits. Progress files are
  git-ignored, so records never dirty the tree.
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
  Two-Key, leaving tracked files alone while it runs. A drafter may run
  beside the previous unit's Two-Key. When a unit's tests extend a module
  an earlier unit placed, its drafter writes that module whole, with the
  earlier tests amended where needed. The developer may return before its
  own suite run ends; Claude's receipts run is then the suite's receipt.
  Session 46's subagents: drafters 191K and 179K tokens, developers 74K
  and 66K, Two-Key 177K and 174K.
- Before placing a drafted list: strip session labels (`ruling_2`) from its
  names, check the module for a repeated test name, since a later `def`
  silently replaces an earlier one, and diff the earlier tests against the
  repo: a drafter's rename can glue a helper's new name into a test name
  (session 46: `..._is_cut` became `..._iscut_lines`). A later unit may
  amend an earlier unit's test when its contract changes that test's
  expected output; the drafter's pins name such a test, never forbid it.
- `scope-check` outside Actions needs `--base <sha>`: main's tip.
- Run the release unit's sweep patterns before its verifier round; a hit
  outside scope goes to an OPEN and a re-intake first.
- Attribution is off: a commit's final paragraph is `Contract:` alone, and
  a PR body ends at its last sentence.
- Release shape: PR, merge commit, annotated tag at the merge, then the
  self-pin through its own PR; main's ruleset requires a PR for every
  change. `gh pr checks --watch` can exit 1 on "no checks reported"; start
  it again.
- herdr probes run in panes Claude splits with `--no-focus` and closes
  after; never report state on another session's pane. The recipe: `herdr
  pane split --pane <own> --direction down --cwd <root> --no-focus`, then
  `pane run <new> "<command>"`, `pane wait-output <new> --match <text>`
  (plain text, not a regex), `pane read <new> --source visible`, `pane
  get <new>` (its `agent` and `agent_status`), `pane close <new>`. A new
  split may narrow after the pane's first render: touch a watched file to
  redraw before judging a cut. A pane run on a scratch copy (`--root`)
  leaves the kit's progress alone. A manual `release-agent` for the hook's
  flag needs a `--seq` above the hook's (the time in milliseconds).
- A settings file with unrelated uncommitted edits is staged by blob
  (`hash-object`, then `update-index`), so the commit holds one change.

## Open questions
- The `intake-seat` term says a seat is never delegated to an agent, while
  a delegated session's approvals record `--by claude` (sessions 40 to 42,
  45 and 46). Does the term need a word for a delegated approval?
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
