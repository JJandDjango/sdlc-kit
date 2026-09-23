# Plan - Session 42 (2026-09-22) - tree-view t7 and t8

**Deliverable:** two units of `tree-view` (the request for one derived tree
of the work) on one PR, each with a Two-Key PASS (one agent re-runs every
check, a second grades the commit against the contract, and a script
computes the verdict). Together they are the kit's half of the herdr pane.

- t7 `t7-pane-face`: `taskcontract tree --follow` keeps a pane on the
  current task. Every item on the path to it shows, each level's other
  items fold to one line with counts by status, and the pane redraws
  within two seconds of a source change, never while nothing changes. It
  also takes the carried advisory: every `git status` the kit runs gets
  `--no-optional-locks`, since the pane redraws while the user runs git.
- t8 `t8-approval-notify`: when the current task is `approve-tests` or
  `approve-commit`, the pane's first line reads `waiting on a seat:
  {approval} for {unit}`, and the `tree: notify:` command in
  `.sdlc/config.yaml` runs once per arrival, with the task's id in
  `SDLC_NODE`. A failure prints `notify failed, exit {code}: {command}`,
  and the pane keeps running.

Where things stand: PR #51 (t4, t5) merged at `f2d400a`, and branch
`session-42-tree-view-t7-t8` starts there. Suite 432 green, the 14
contracts ready-green. USAGE section 9, written at t0, already pins most of
both units: the one-second poll of modification times, ANSI redraws,
Ctrl-C exiting 0, the shell, the config key and the failure line. The
kit's current mark sits on t6's `approve-tests`; step 1 moves it to t7's.

**Who does what.** The user approved PR #51's merge, this deliverable and
the delegation, and reviews this plan and its rulings. Subagents do each
unit's work through the Workflow tool, launched by `scriptPath`: the
drafter drafts the test list, proves it red from the scratchpad and
prototypes the interface; the developer makes the tests green from the
interface note without opening `tests/`; Two-Key grades last. Claude
approves each list and each commit, places the tests, records each task
with `taskcontract progress` (`--by claude` on the approvals it gives), and
runs the receipts before each verifier round.

## Rulings for the test lists

Details the contract and USAGE leave open, for the user to rule:

1. **The pane reads down to the current task.** Each level's other items
   fold into one line above the item on the path, so the current task is
   always the last line. In `--follow` only, each line is cut to the
   pane's width and ends in `...`: a cut prefix, never other words, and
   the whole tree still prints every line whole. Recommended: a contract's
   intent alone runs to about 900 characters, eleven rows of an 80-column
   pane, which breaks the fifteen-line pane.
2. **The pane watches the files the tree reads:** everything under
   `specs/` (the contracts, and the vocabulary the validator reads),
   `.sdlc/config.yaml`, `.sdlc/findings/`, `.sdlc/progress/`,
   `docs/features/` and the kit's two lists, listed afresh each second so
   a new or deleted file counts. Git is not watched. Recommended: it
   matches USAGE's words, and a commit shows at the next progress record,
   which the task list writes after every commit.
3. **The pane keeps each `G0` verdict in memory** and recomputes it only
   when its contract or the vocabulary changes; nothing is written.
   Recommended: a render of the kit costs 1.3 s today, nearly all of it
   the validator reloading the vocabulary for each of 28 validations, so a
   one-second poll can take 2.3 s. With the verdicts kept, a redraw after
   a progress record costs about 0.2 s. A vocabulary change still costs
   the full render, a rare case. The validator's files sit outside the
   contract's scope, so the fix stays in `tree.py`.
4. **A pane that starts on an approval notifies once:** its first render
   counts as an arrival. Recommended: the pane may start after the
   approval was reached, and nothing else tells the seat; a restart
   repeats one notice at most.
5. **The pane never waits on the notify command.** It starts the command,
   checks it at each one-second tick, and prints the failure line when it
   ends nonzero. Recommended: a command that hangs never freezes the pane,
   and the pinned failure line has no form for a timeout.

## The pane, as the rulings draw it

The kit at step 1, once both units land, in an 80-column pane. The first
line is t8's; the rest is t7's. t7's test list pins the fold lines' words.

    waiting on a seat: approve-tests for tree-view/t7-pane-face
    14 more: 14 to do
    tree-view [waiting on a seat] | A repo holds its work in contracts, gates, fi...
      10 more: 7 done, 3 to do
      tree-view/t7-pane-face [waiting on a seat] depends_on: tree-view/t3-status-...
        9 more: 9 to do
        tree-view/t7-pane-face/approve-tests [waiting on a seat] | Approve the te...

## Diagram

The plan's diagram source is `plan.workflow.json` beside this file (Archify
workflow, step spine: the steps read left to right, approvals dropping onto
it from above, an exception lane below for a Two-Key FAIL or an OPEN).
Render and open:

    node C:/Users/hyden/.claude/skills/archify/bin/archify.mjs deliver workflow plan.workflow.json <scratch>/plan.html --quality showcase --json
    Start-Process <scratch>/plan.html

The HTML is generated, never committed.

## Steps

1. **Open.** Branch cut from `f2d400a` (done); this plan and its diagram,
   committed once the user approves them; then `progress start
   tree-view/t7-pane-face/approve-tests`, so the current mark leaves t6.
2. **t7, draft and approve the test list.** The drafter covers SC2.1 to
   SC2.3 and rulings 1 to 3, with the loop driven in-process through an
   injected clock, so no test waits on a real second.
3. **t7, write the tests and prove red.** Each check's red recorded with
   `progress run --expect red`.
4. **t7, green.** Then the receipts: the suite, the 14 contracts
   ready-green, the doors, the scope check, and one timed redraw on the
   kit itself, under two seconds.
5. **t7, approve the commit and commit.** Each check's green recorded with
   `progress run` at the commit.
6. **t7 Two-Key.**
7. **t8, draft and approve the test list.** SC8.1 to SC8.3 and rulings 4
   and 5.
8. **t8, write the tests and prove red.**
9. **t8, green.**
10. **t8, approve the commit and commit.**
11. **t8 Two-Key.**
12. **Close.** t7 and t8 closed with `progress done`; STATE.md regenerated
    and this plan struck through; the push and the PR on the user's word.

Decisions this session: ten. The user's: (1) PR #51's merge: yes, at
`f2d400a`; (2) the deliverable, t7 and t8: yes; (3) the delegation of the
in-work approvals: yes; (4) this plan and its five rulings: pending.
Claude's on review: (5) t7's test list; (6) t7's commit; (7) t8's test
list; (8) t8's commit. The user's at the close: (9) the push and the PR;
(10) the merge.

Deferred, not this session:
- The herdr hook on t8's notify, outside the kit. Its first question: does
  herdr's own screen detection overwrite an outside `herdr pane
  report-agent --state blocked`? The notify command runs from the pane, so
  it needs the Claude pane's id.
- t6, with its carried advisories: `tree.py`'s docstring on a close; t1's
  id collision; a repeated `depends_on` entry printing twice;
  `tree_view.py`'s docstring on spacing.
- t9 last, releasing 0.15.0: USAGE's `progress` rows and the notes carried
  from t0 to t5 (full list in STATE.md), plus what t7 and t8 leave for
  USAGE.
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
paragraph, on every commit that touches a non-free path; before placing a
drafted list, session labels stripped from its names and the module
checked for a repeated test name; receipts run before each verifier round,
and no tracked file touched while it runs; a surprise mid-build is an OPEN
and a re-intake, never a silent edit.
