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

**Closed.** The deliverable is met: t7 at `2f8ef03` and t8 at `0e89078`,
each a Two-Key PASS at round 1. The branch is pushed and its PR open on
the user's word; the merge waits on it.

Where things stand: PR #51 (t4, t5) merged at `f2d400a`, where this
branch starts. Suite 486 green (432 before; t7 added 37 cases, t8 17), the
14 contracts ready-green, the vocabulary, language and scope checks clean.
t7 and t8 are closed in the kit's progress file, and the pane on the kit
now stands on t6's `approve-tests`.

**Who did what.** The user approved PR #51's merge, this deliverable, the
delegation, and this plan with its five rulings, then asked for the push
and the PR at the wrap. Subagents did each unit's work through the
Workflow tool: a drafter drafted the test list, proved it red from the
scratchpad and prototyped the interface; a developer made the tests green
without opening `tests/`; Two-Key graded last. t8's drafter ran beside
t7's Two-Key. Claude approved each list and each commit, placed the tests,
recorded each task with `taskcontract progress`, and ran the receipts
before each verifier round.

## Rulings for the test lists

Details the contract and USAGE left open, ruled by the user at plan
review:

1. **The pane reads down to the current task.** Each level's other items
   fold into one line above the item on the path, so the current task is
   always the last line. In `--follow` only, each line is cut to the
   pane's width and ends in `...`: a cut prefix, never other words, and
   the whole tree still prints every line whole.
2. **The pane watches the files the tree reads:** everything under
   `specs/`, `.sdlc/config.yaml`, `.sdlc/findings/`, `.sdlc/progress/`,
   `docs/features/` and the kit's two lists, listed afresh each second so
   a new or deleted file counts. Git is not watched: a commit shows at the
   next progress record, which the task list writes after every commit.
3. **The pane keeps each `G0` verdict in memory** and recomputes it only
   when its contract or the vocabulary changes; nothing is written. A
   render of the kit cost 1.3 s; a warm redraw now costs 0.23 s. A
   vocabulary change still costs the full render, a rare case.
4. **A pane that starts on an approval notifies once:** its first render
   counts as an arrival.
5. **The pane never waits on the notify command.** It starts the command,
   checks it at each one-second tick, and prints the failure line when it
   ends nonzero.

## The pane on the kit, at the close

At 80 columns; the first line is t8's, the rest t7's:

    waiting on a seat: approve-tests for tree-view/t6-query-face
    14 more: 14 to do
    tree-view [waiting on a seat] | A repo holds its work in contracts, gates, fi...
      10 more: 1 to do, 9 done
      tree-view/t6-query-face [waiting on a seat] depends_on: tree-view/t2-summar...
        9 more: 9 to do
        tree-view/t6-query-face/approve-tests [waiting on a seat] current | Appro...

## Diagram

The plan's diagram source is `plan.workflow.json` beside this file (Archify
workflow, step spine: the steps read left to right, approvals dropping onto
it from above, an exception lane below for a Two-Key FAIL or an OPEN).
Render and open:

    node C:/Users/hyden/.claude/skills/archify/bin/archify.mjs deliver workflow plan.workflow.json <scratch>/plan.html --quality showcase --json
    Start-Process <scratch>/plan.html

The HTML is generated, never committed.

## Steps

1. ~~Open.~~ Done at `f71c283`: branch cut from `f2d400a` after PR #51's
   merge, and this plan; the current mark moved to t7's `approve-tests`.
2. ~~t7, draft and approve the test list.~~ 18 tests (37 cases), approved
   with one change: the pane's git test asserts at least two `git status`
   calls, so the dirty mark is read at every render. Settled with it: the
   fold line `<n> more: <counts>`, `no current task` then `<n> items`, a
   10-column floor, unreadable sources on stderr.
3. ~~t7, write the tests and prove red.~~ 37 failed, 432 passed.
4. ~~t7, green.~~ `tree_view.py`, `tree.py`, `progress.py`, `__main__.py`;
   469 passed; a warm redraw on the kit 0.23 s against 1.22 s cold.
5. ~~t7, approve the commit and commit.~~ Done at `2f8ef03`; SC2.1 to
   SC2.3 recorded green there.
6. ~~t7 Two-Key.~~ PASS at round 1, about 200K tokens. Three advisories,
   to t9's notes.
7. ~~t8, draft and approve the test list.~~ 11 tests (17 cases), approved
   as drafted. Its two questions, answered: one t7 test gains the waiting
   line, since its fixture stands on an approval; the failure line prints
   whole on stderr, as t7's stderr lines do.
8. ~~t8, write the tests and prove red.~~ 18 failed, 468 passed.
9. ~~t8, green.~~ `tree_view.py`, `tree.py`, `__main__.py`; 486 passed.
10. ~~t8, approve the commit and commit.~~ Done at `0e89078`; SC8.1 to
    SC8.3 recorded green there, and SC2.1 again.
11. ~~t8 Two-Key.~~ PASS at round 1, about 177K tokens. Two wording
    advisories, to t9.
12. ~~Close.~~ t7 and t8 closed with `progress done`; STATE.md regenerated
    and this plan struck through; the push and the PR on the user's word.

Decisions this session: ten. The user's: (1) PR #51's merge: yes, at
`f2d400a`; (2) the deliverable, t7 and t8: yes; (3) the delegation of the
in-work approvals: yes; (4) this plan and its five rulings: yes. Claude's
on review: (5) t7's test list: yes, with one change; (6) t7's commit: yes;
(7) t8's test list: yes, its two questions answered; (8) t8's commit: yes.
The user's at the close: (9) the push and the PR: yes; (10) the merge:
pending.

Details the rulings left open, fixed with the test lists: a scan that
finds a change always renders; HEAD and the dirty marks are read fresh at
every render; the width is shutil's, never under 10 columns; on Windows
the pane turns on the console's escape processing. The waiting line names
the task key and the unit's full id; `SDLC_NODE` holds the approval
task's full id; the command runs at the repo root with its output sent
nowhere; a command that cannot start prints the failure line with exit
127; a notify value that is not a string holding a command counts as
unset, silently.

Deferred, not this session:
- The herdr hook on t8's notify, outside the kit. Its first question: does
  herdr's own screen detection overwrite an outside `herdr pane
  report-agent --state blocked`? The notify command runs from the pane, so
  it needs the Claude pane's id.
- t6, with its carried advisories: `tree.py`'s docstring on a close; t1's
  id collision; a repeated `depends_on` entry printing twice;
  `tree_view.py`'s docstring on spacing.
- t9 last, releasing 0.15.0: USAGE's `progress` rows and the notes carried
  from t0 to t5 (full list in STATE.md), the pane's text, and the wording
  advisories from t7 and t8.
- Noted: a cached `G0` reading goes stale across a deprecated term's
  sunset date; `cut()` counts characters, not display columns.
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
