# receipts.py - Two-Key's receipts, run by the session in one command

Signed by the user in session 106 (2026-10-19): all ten items kept as
written. Source: the user's standing practice of session 103 (a script runs
the tests and prints only what an agent needs), recorded in
`docs/backlog.md` Next 5. Status: 🔴 not built; 🟡 built, self-tested (24
tests) and run once on a real receipts list at the kit's root (session 106);
🟢 a real Two-Key round took its receipts from it.

Two-Key's receipts are the check commands it re-runs independently at the
unit's commit. Today `two-key-unit-verifier.js` hands them to a Haiku 5.5
agent, which pays a fixed start of about 54K tokens, infers exit codes from
pass lines instead of reading them, and once returned with two commands still
running. `receipts.py` runs the same commands in the session, with no agent,
and prints the minimum.

| # | Feature | Status |
| :-: | :-- | :-: |
| 1 | **Command**: `python receipts.py --repo DIR --receipts FILE --out DIR` prints one compact JSON object in the shape `two-key-unit-verifier.js` already reads (`head`, `branch`, `working_tree_clean_of_tracked_changes`, `commands[]`, `notes`). Exit 0 only when every command exits 0. | 🟡 |
| 2 | **Repo state**: before any command, reports the short HEAD sha, the branch, and whether a tracked file is modified (untracked files ignored). | 🟡 |
| 3 | **Receipts file**: a JSON list of argv lists, run one at a time from the repo root with no shell, so no pipe, redirect or chain can enter a receipt. | 🟡 |
| 4 | **Real exit codes**: each is the process's own, never inferred. A command that never starts reads 254 (the kit's "spawn failed before launch" sentinel). One past its timeout is killed and reads 124, with `timeout` in `key_output`. | 🟡 |
| 5 | **Key output**: a pytest command gives its summary line plus each failing id with its first assertion line. Any other command gives its last non-empty line. The full log goes to `DIR/logs/<n>.log`, and the JSON names its path. | 🟡 |
| 6 | **Watchdog**: writes `DIR/alive` at launch and updates `DIR/progress.json` after each command, so the session follows a long run with a Monitor. Stderr goes to `DIR/logs/`. | 🟡 |
| 7 | **Harness hygiene**: sets `PYTHONUTF8`, decodes with `errors="replace"`, opens no window. `--timeout SECONDS` per command, default 1800 (the whole suite took 607 s). | 🟡 |
| 8 | **Self-test**: `test_receipts.py` beside it, on a toy git repo: all pass, one non-zero, a timeout, a start failure, a trimmed pytest summary, a modified tracked file seen, an untracked file ignored. | 🟡 |
| 9 | **Two-Key wiring**: the workflow takes the script's JSON as `receiptsResult` and then skips the receipts agent, so the grader runs alone. Without it the agent runs as today until a real round uses the script. | 🟡 |
| 10 | **Home**: `.claude/workflows/tools/receipts.py`, untracked like the other tools. The PR carries docs only: the feature page, a `standing-practice.md` line and the backlog row. The self-test run goes in the PR body. | 🟡 |

## Readings the build chose where the list was silent

- Item 1: the JSON also carries `ok`, `out` (the folder) and, per command,
  `log` and `seconds`. `DIR/result.json` holds the same text. The workflow's
  verdict never reads `ok`; it counts the exit codes itself.
- Item 3: a failing command does not stop the run. Every later command still
  runs, as the agent's did, so one round shows every failure.
- Item 4: the script's own exit codes follow `prove.py`: 0 all hold, 1 a
  command did not, 2 usage (a bad receipts file, or a folder that is no git
  repository with a commit), 254 git never started.
- Item 5: `key_output` reads the "short test summary info" lines pytest
  prints, so the command's argv is never changed. A command run with `-rN`
  therefore lists no ids. More than 10 failing ids print the first 10 and
  `+N more in the log`. A command's stderr is merged into its log, so a
  non-pytest command's last line may come from stderr.
- Item 6: `progress.json` is also written before each command, with a
  `running` entry, and once more at the end with `finished: true`.
- Item 9: `receiptsResult` arrives inline in `args`, since a workflow script
  cannot read files. A result with no commands, or a non-integer exit code,
  reads INCOMPLETE. The return value names its source in `receiptsFrom`, and
  `receipts` (the command strings) is not required when a result is given.
  Checked by a scratch Node run with stubbed agents over four cases (valid,
  one failing exit with `ok: true`, malformed, no result), not by a real round.
- Real run (step 4 of the plan): 2 commands at the kit's root, 26.9 s in all
  (`tests/test_g1_release.py` 45 passed, `cairn audit` clean), followed live
  with a Monitor on `progress.json`.
- Measure: the first real Two-Key round that takes a `receiptsResult` is
  compared with the receipts agent's cost (a 54K-token start plus its calls).
  Items go 🟢 on that run. This session added no metrics row, since the
  record keeps rows for sessions that ship a unit.

## Left out on purpose

A check that HEAD equals the graded commit: the agent never made one, and the
workflow never compared the two. Item 3 ends the three-glob suite split,
since the script runs in the background and the 600 s foreground cap no
longer binds. Item 9 settles the open Haiku question in practice: with a
`receiptsResult`, no agent runs.

## Why this page is not under `docs/features/`

The tree reads feature documents from `docs/features/`, so a page there would
enter it as a feature. `receipts.py` is a workflow tool, not a kit feature.
