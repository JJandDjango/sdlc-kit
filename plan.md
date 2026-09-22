# Plan - Session 39 (2026-09-21) - tree-view t0 and t1

**Deliverable:** two units of `tree-view` (the request for one derived tree
of the work) on one PR, each with a Two-Key PASS (one agent re-runs every
check, a second grades the commit against the contract, and a script
computes the verdict):

- t0 `t0-usage-pass-zero`: the USAGE section on `taskcontract tree` and
  `taskcontract progress`, written before any code, every part marked red
  until the release.
- t1 `t1-tree-shape`: `taskcontract tree` prints the gates with their
  findings, and each contract with its gate verdicts, units, seven tasks
  and checks; it writes no file.

Where things stand: `main` at `971b57a`, one commit ahead of origin (the
session-38 STATE fix, which this session's PR carries). The contract
`specs/tree-view/contract.yaml` is ready-green (it passes the validator's
strict profile) at r4, the request's fourth revision (`f3c80d0`), and ADR
0031 (the decision record) holds the rulings. None of the ten units exists
yet: no
`taskcontract/tree.py`, no `data/gates.yaml` or `data/tasks.yaml`, no USAGE
section. The build tracks its tasks here until t4 and t5 ship
`taskcontract progress`.

## Diagram

The plan's diagram source is `plan.workflow.json` beside this file (Archify
workflow, step spine: the steps read left to right, human gates dropping onto
it from above, an exception lane below for a Two-Key FAIL or an OPEN).
Render and open:

    node C:/Users/hyden/.claude/skills/archify/bin/archify.mjs deliver workflow plan.workflow.json <scratch>/plan.html --quality showcase --json
    Start-Process <scratch>/plan.html

The HTML is generated, never committed.

## Steps

1. Open. Branch `session-39-tree-view-t0-t1` from `main`; commit this plan
   and its diagram source.
2. t0 `t0-usage-pass-zero`, the page first. USAGE gains "9. Following the
   work", and Troubleshooting moves to 10, as it did when section 8 landed.
   The section covers the three modes (`tree`, `tree NODE`,
   `tree --follow`), the seven tasks with the `progress` command for each,
   `progress run` with `--expect red`, the `tree: notify:` key, and the
   backfill by `progress done`. Every part carries the red mark. t0 has no
   check to run, so its tasks come down to the section, your word, the
   commit and Two-Key. The section is shown in chat in full and committed
   on your word, `Contract: tree-view`.
3. t0 Two-Key. The verifier runs by `scriptPath` with `sweep: false` (the
   repo-wide search for stale claims runs only in the release unit), its
   focus fixed to t0's two sketches. A FAIL gets one fix commit and another
   round, at most three rounds.
4. t1 `t1-tree-shape`, approve the test list: one line per test, each naming
   the check it proves (SC1.1, SC1.2, SC1.3), shown in chat while t0's
   verifier runs. It waits for your word.
5. t1, write the tests and prove red. `tests/test_tree.py` builds fixture
   repos under `tmp_path`. The new tests fail, and every other test stays
   green.
6. t1, green. `taskcontract/tree.py` builds the model, `tree_view.py` prints
   it, `data/gates.yaml` lists the thirteen gates (id, name, kit page) and
   `data/tasks.yaml` the seven tasks, and `__main__.py` gains the `tree`
   subcommand. Every status reads `to do` until t3 derives it. Receipts
   (the commands the verifier re-runs): the suite, every contract
   ready-green, `vocab-check`, `lang-check`, `scope-check`.
7. t1, approve the commit and commit: the diff summary and the message shown
   in chat, committed on your word, `Contract: tree-view`.
8. t1 Two-Key, as in step 3.
9. Close. STATE.md regenerated and this plan struck through, committed; push
   and PR on your word; merge on your word.

Decisions this session: six. (1) this plan; (2) t0's section and commit;
(3) t1's test list; (4) t1's commit; (5) the push and the PR; (6) the merge.
A surprise mid-build is an OPEN (a question written back into the request)
and a re-intake (the contract derived again), per ADR 0029, never a silent
edit; the rulings of ADR 0031 stay closed.

Deferred, not this session:
- `tree-view` t2 to t9, then the release (0.15.0); the herdr plugin outside
  the kit.
- G1: the pilot's M0 code waits on its criteria review.
- `no-check-reads-the-source-document`: which request carries it.
- `derived-language`, `feature-document`, `spec-doc-type`; the demo intake
  in a sandbox consumer; wave B (`playbook-loop`, V1-V6); 5b; the G4.6
  finding.
- From r3: a status field on the finding form; the agent personas writing
  progress.

House rules in force: no pipes or chains in any authored command string;
commit messages via Write + `git commit -F`; Two-Key on every code unit; a
`Contract:` trailer, alone in the final paragraph, on every commit that
touches a non-free path; uncontested decisions batched in one message,
contested ones one per message, each with a recommendation; approval
content shown in chat in full.
