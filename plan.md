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

t4 goes first: it owns the folder's `.gitignore`, so the first file any
writer creates is already ignored, and t5 adds three verbs to the command
t4 builds.

Where things stand: PR #50 (t3 and t2) is open with both CI jobs green,
waiting on your merge. This branch starts from its tip, so its PR shows
only this session's commits once #50 merges. Suite 375 green, the 14
contracts ready-green, the vocabulary, language and scope checks clean.

**Who does what.** Recommended, as in session 40, where both units passed
at round 1: you delegate the four in-work approvals (two test lists, two
commits) to Claude on review, and rule the open details below now, so the
lists only encode your rulings. Subagents do each unit's work through the
Workflow tool: a spec-channel agent drafts the test list, proves it red
from the scratchpad and prototypes the interface; a developer agent makes
the tests green without opening `tests/`. Claude places the approved
tests, reviews each commit, and runs the receipts before each verifier
round.

## Rulings for the test lists

Details the request leaves open, with the recommended ruling for each:

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

1. Open: branch `session-41-tree-view-t4-t5` from #50's tip, and this plan.
2. t4, draft and approve the test list. The drafter also takes t3's two
   advisories: name the evidence keys (`head`, `by`, `reason`, `command`,
   `dirty`) in `progress.py`'s docstring, and mark a `G0` verdict `dirty`
   when its contract file differs from `HEAD`, since the validator reads
   the working tree.
3. t4, write the tests in `tests/test_progress.py` and prove red.
4. t4, green: `progress.py`, `__main__.py`, and the tree's evidence.
5. t4, approve the commit and commit.
6. t4 Two-Key.
7. t5, draft and approve the test list.
8. t5, write the tests and prove red, each red run recorded with t4's
   `progress run --expect red`.
9. t5, green, each green run recorded with `progress run`.
10. t5, approve the commit and commit.
11. t5 Two-Key.
12. Close: `progress done` on t0 to t5, so the kit's tree reads tree-view's
    real state; STATE.md regenerated and this plan struck through; the
    push and the PR on your word.

Decisions this session: eight. Yours now: (1) this plan, its five rulings
and the delegation; (2) PR #50's merge. Claude's on review, if delegated:
(3) t4's test list; (4) t4's commit; (5) t5's test list; (6) t5's commit.
Yours at the close: (7) the push and the PR; (8) the merge.

Deferred, not this session:
- `tree-view` t6 and t7 (both unblocked), t8 after t7, t9 last, releasing
  0.15.0; then the herdr hook on t8's notify, outside the kit.
- For t6: t1's id collision (a sketch naming `(commit)`, or a unit named
  like an active gate); a repeated `depends_on` entry prints the link
  twice; `tree_view.py`'s docstring says each part follows one space, but
  the summary follows ` | `.
- For t9: t0's two wording notes; t1's note that a `.yml` finding is not
  read; USAGE's backfill sentence holds only for a ready-green contract
  with no other active gate; USAGE documents the line's words and the text
  rule behind "unchanged".
- The backfill of the 13 earlier contracts, once each is checked finished.
- Later: a summary holding a character the console's encoding lacks could
  fail a print piped on Windows; every current contract and finding is
  ASCII.
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
