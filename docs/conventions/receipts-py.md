# receipts.py - Two-Key's receipts, run by the session in one command

Signed by the user in session 106 (2026-10-19): all ten items kept as
written. Source: the user's standing practice of session 103 (a script runs
the tests and prints only what an agent needs), recorded in
`docs/backlog.md` Next 5. Status: 🔴 not built; 🟡 built, self-tested and run
once on a real receipts list; 🟢 a real Two-Key round took its receipts from
it.

Two-Key's receipts are the check commands it re-runs independently at the
unit's commit. Today `two-key-unit-verifier.js` hands them to a Haiku 5.5
agent, which pays a fixed start of about 54K tokens, infers exit codes from
pass lines instead of reading them, and once returned with two commands still
running. `receipts.py` runs the same commands in the session, with no agent,
and prints the minimum.

| # | Feature | Status |
| :-: | :-- | :-: |
| 1 | **Command**: `python receipts.py --repo DIR --receipts FILE --out DIR` prints one compact JSON object in the shape `two-key-unit-verifier.js` already reads (`head`, `branch`, `working_tree_clean_of_tracked_changes`, `commands[]`, `notes`). Exit 0 only when every command exits 0. | 🔴 |
| 2 | **Repo state**: before any command, reports the short HEAD sha, the branch, and whether a tracked file is modified (untracked files ignored). | 🔴 |
| 3 | **Receipts file**: a JSON list of argv lists, run one at a time from the repo root with no shell, so no pipe, redirect or chain can enter a receipt. | 🔴 |
| 4 | **Real exit codes**: each is the process's own, never inferred. A command that never starts reads 254 (the kit's "spawn failed before launch" sentinel). One past its timeout is killed and reads 124, with `timeout` in `key_output`. | 🔴 |
| 5 | **Key output**: a pytest command gives its summary line plus each failing id with its first assertion line. Any other command gives its last non-empty line. The full log goes to `DIR/logs/<n>.log`, and the JSON names its path. | 🔴 |
| 6 | **Watchdog**: writes `DIR/alive` at launch and updates `DIR/progress.json` after each command, so the session follows a long run with a Monitor. Stderr goes to `DIR/logs/`. | 🔴 |
| 7 | **Harness hygiene**: sets `PYTHONUTF8`, decodes with `errors="replace"`, opens no window. `--timeout SECONDS` per command, default 1800 (the whole suite took 607 s). | 🔴 |
| 8 | **Self-test**: `test_receipts.py` beside it, on a toy git repo: all pass, one non-zero, a timeout, a start failure, a trimmed pytest summary, a modified tracked file seen, an untracked file ignored. | 🔴 |
| 9 | **Two-Key wiring**: the workflow takes the script's JSON as `receiptsResult` and then skips the receipts agent, so the grader runs alone. Without it the agent runs as today until a real round uses the script. | 🔴 |
| 10 | **Home**: `.claude/workflows/tools/receipts.py`, untracked like the other tools. The PR carries docs only: the feature page, a `standing-practice.md` line and the backlog row. The self-test run goes in the PR body. | 🔴 |

## Left out on purpose

A check that HEAD equals the graded commit: the agent never made one, and the
workflow never compared the two. Item 3 ends the three-glob suite split,
since the script runs in the background and the 600 s foreground cap no
longer binds. Item 9 settles the open Haiku question in practice: with a
`receiptsResult`, no agent runs.

## Why this page is not under `docs/features/`

The tree reads feature documents from `docs/features/`, so a page there would
enter it as a feature. `receipts.py` is a workflow tool, not a kit feature.
