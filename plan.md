# Plan - Session 41 (2026-09-22) - tree-view t4 and t5

**Deliverable:** two units of `tree-view` (the request for one derived tree
of the work) on one PR, each with a Two-Key PASS (one agent re-runs every
check, a second grades the commit against the contract, and a script
computes the verdict). They are the progress writers: nothing in the herdr
pane moves until they land.

- t4 `t4-check-runs`: `taskcontract progress run <check> [--expect red] --
  <command>` runs a check's command and records red or green beside its
  expectation, with the command, the `HEAD` id, a `dirty` mark and the
  time. It exits 0 when the result met the expectation, else 1. The folder
  `.sdlc/progress/` holds a `.gitignore` of `*`, and a `done` check shows
  its command and commit in the tree.
- t5 `t5-task-writers`: `taskcontract progress start|done|block <id>`
  records task states, each with the time and the `HEAD` id. `done` on
  `approve-tests` or `approve-commit` needs `--by <seat>`, `block` needs
  `--reason`, and `done` on a unit or a contract closes everything under
  it (the backfill). A `done` task shows its commit, an approval its seat.

**Closed.** The deliverable is met: t4 at `0b650bd` and t5 at `a11eab0`,
each a Two-Key PASS at round 1. The PR carrying them opens and merges on
the user's word.

Where things stand: PR #50 (t3 and t2) merged at `a1109df`. Suite 432
green (405 before t5; t4 added 30 cases, t5 27), the 14 contracts
ready-green, the vocabulary, language and scope checks clean. The kit now
records its own progress: t4's and t5's checks carry their runs, t0 to t5
are closed, and the tree reads them done, with the current mark derived to
t6's `approve-tests`.

**Who did what.** The user approved this plan, its five rulings and the
delegation, and merged PR #50. Subagents did each unit's work through the
Workflow tool: a spec-channel agent drafted the test list, proved it red
from the scratchpad and prototyped the interface; a developer agent made
the tests green without opening `tests/`. Claude reviewed and approved each
list and each commit, placed the approved tests, and ran the receipts
before each verifier round.

## Rulings for the test lists

Details the request left open, ruled by the user at plan review:

1. A command that cannot start (not found) is an error: exit 2, one line,
   nothing written. It never counts as red, so a missing test binary
   cannot prove red.
2. Each writer checks its id against the tree first: `run` takes a check,
   `start` and `block` a task, `done` a task, a unit or a contract. An
   unknown id exits 2 with t6's line, `no node '{id}' - print the tree to
   list every node id`; a wrong kind exits 2 with one line of its own.
   Nothing is written either way, since the reader drops a misplaced
   record without a word.
3. A malformed progress file stops every writer with one line naming it,
   and nothing is written: a writer never rewrites records it cannot read.
4. `--by` takes the seat's name as written. The `intake-seat` term says a
   seat is never delegated to an agent, but the progress file is display
   evidence no gate reads, so the tree shows who approved rather than the
   writer refusing an honest record. TC016 stays the roster check.
5. Evidence reads like t3's `G0` verdict: a check `via <command> at
   <head>`, a task `at <head>`, an approval `by <seat> at <head>`, each
   followed by `dirty` when a tracked file differed from `HEAD`.

## Diagram

The plan's diagram source is `plan.workflow.json` beside this file (Archify
workflow, step spine: the steps read left to right, approvals dropping onto
it from above, an exception lane below for a Two-Key FAIL or an OPEN).
Render and open:

    node C:/Users/hyden/.claude/skills/archify/bin/archify.mjs deliver workflow plan.workflow.json <scratch>/plan.html --quality showcase --json
    Start-Process <scratch>/plan.html

The HTML is generated, never committed.

## Steps

1. ~~Open.~~ Done at `8f6db7d`: branch `session-41-tree-view-t4-t5` from
   #50's tip, and this plan; PR #50 merged at `a1109df`.
2. ~~t4, draft and approve the test list.~~ 24 tests (30 cases), approved
   with three changes: a check keeps its last green run's evidence after a
   close (one assertion added), durable test names, and two hints in the
   interface note. Its one question, answered: `gates/none` reads `gate`,
   unpinned.
3. ~~t4, write the tests and prove red.~~ 30 failed, 375 passed, each on
   an assertion.
4. ~~t4, green.~~ `progress.py`, `tree.py`, `tree_view.py`, `__main__.py`;
   405 passed.
5. ~~t4, approve the commit and commit.~~ Done at `0b650bd`; its three
   checks then recorded green through `progress run`.
6. ~~t4 Two-Key.~~ PASS at round 1, about 192K tokens. Three advisories,
   all to t9.
7. ~~t5, draft and approve the test list.~~ 25 tests (27 cases), approved
   with durable names (one would have repeated a t4 test's name) and a
   docstring line. Its two questions, answered: about 7 seconds is
   acceptable; neither check order needs pinning.
8. ~~t5, write the tests and prove red.~~ 27 failed, 405 passed; each
   check's red recorded with `progress run --expect red`.
9. ~~t5, green.~~ The same four files; 432 passed; each check's green
   recorded with `progress run` at `a11eab0`.
10. ~~t5, approve the commit and commit.~~ Done at `a11eab0`.
11. ~~t5 Two-Key.~~ PASS at round 1, about 193K tokens. Three advisories:
    one to t6, one to t9, one noted.
12. ~~Close.~~ t0 to t5 closed with `progress done`, so the kit's tree
    reads them done; STATE.md regenerated and this plan struck through;
    the push and the PR on the user's word.

Decisions this session: eight. The user's: (1) this plan, its five rulings
and the delegation: yes; (2) PR #50's merge: yes. Claude's on review: (3)
t4's test list: yes, with three changes; (4) t4's commit: yes; (5) t5's
test list: yes, with the names and a docstring line; (6) t5's commit: yes.
The user's at the close: (7) the push and the PR: pending; (8) the merge:
pending.

Details the rulings left open, fixed with the test lists: `--expect` takes
red or green, default green, always recorded; the command runs at the root
from its argv, with no shell and its output passed through, then one line,
`<id>: <result>, expected <expect>`; `HEAD` and dirty are read before the
command starts; outside git the head reads `no commit` and no dirty key is
written; a `G0` verdict reads dirty when its own contract file differs from
`HEAD` or is not in it; a check keeps its last run's evidence when that run
was green as expected. `--by` on anything but an approval, and a blank
`--by` or `--reason`, exit 2; start and block take an approval too; every
call appends; a close is one record; a close neither adds evidence to the
items under it nor hides theirs; a closed unit or contract shows its close's
`at <head>`; a blocked task shows `because <reason>` while blocked.

Deferred, not this session:
- `tree-view` t7 (unblocked), t8 after t7, then the herdr hook on t8's
  notify, outside the kit; t6; t9 last, releasing 0.15.0.
- For t7: `git status` with `--no-optional-locks`, since the pane redraws
  while the user runs git.
- For t6: `tree.py`'s docstring says a close reads everything under it
  done, where it reads every task and check; t1's id collision; a repeated
  `depends_on` entry prints the link twice; `tree_view.py`'s docstring on
  spacing.
- For t9: USAGE's `progress` rows (`--expect green`, the exit-2 refusals,
  a malformed file stopping a writer, the task writers' options and
  evidence), the `G0` verdict's dirty rule, no `dirty` key outside git,
  "done all the way down" (a close never covers a verdict); t0's two
  wording notes; t1's `.yml` note; the backfill qualifier; the line's words
  and the text rule behind "unchanged".
- The backfill of the 13 earlier contracts, once each is checked finished.
- Parked until the pane can follow them: G1, then the pilot's M0 code.
- `no-check-reads-the-source-document`: which request carries it.
- `derived-language`, `feature-document`, `spec-doc-type`; the demo intake
  in a sandbox consumer; wave B (`playbook-loop`, V1-V6); 5b; the G4.6
  finding.
- From r3: a status field on the finding form; the agent personas writing
  progress.

House rules in force: no pipes or chains in any authored command string;
commit messages via Write + `git commit -F`; Two-Key on every code unit,
launched by `scriptPath`; a `Contract:` trailer, alone in the final
paragraph, on every commit that touches a non-free path; receipts run
before each verifier round, and no tracked file touched while it runs; a
surprise mid-build is an OPEN and a re-intake, never a silent edit.
