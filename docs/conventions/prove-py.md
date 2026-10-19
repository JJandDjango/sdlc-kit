# prove.py - the drafter's red, green and mutation proof, in one command

Signed by the user in session 105 (2026-10-18): all ten items kept, item 10 as
written. Source: the user's standing practice of session 103 (a script runs
the tests and prints only what an agent needs), recorded in
`docs/backlog.md` Next 4. Status: 🔴 not built; 🟡 built, self-tested (18
tests) and run once on a real placed test (session 105), the brief naming it;
🟢 used by a real drafter run.

The drafter of a unit's test list proves three things by hand: the list is red
against the repo, green against a prototype, and each pinned behavior is caught
by a one-line mutation. Session 103's `s6-release` drafter spent 299K tokens and
124 tool calls, mostly copying, mutating, running and restoring. `prove.py` does
that plumbing and prints the minimum.

| # | Feature | Status |
| :-: | :-- | :-: |
| 1 | **Command**: `python prove.py --scratch DIR --test NAME [--mutations FILE]` prints one compact JSON object. It exits 0 only when red, green and every mutation hold. | 🟡 |
| 2 | **Setup**: copies the `taskcontract` package to `DIR/proto/` once and never overwrites the drafter's edits. Places the draft and a `conftest.py` in `DIR/red/` and `DIR/green/`; green's `conftest.py` puts `proto/` first on `sys.path`. | 🟡 |
| 3 | **Red run**: runs the draft against the repo's current code. `red_ok` is true only if every test failed on an assertion, none on a fixture, import or collection error. | 🟡 |
| 4 | **Green run**: runs the draft against `proto/`. Reports the summary line, each failing id with its first assertion line, and the resolved package path that shows `proto/`, not the repo, was imported. | 🟡 |
| 5 | **Mutation loop**: reads a JSON list of `{name, file, old, new}` and applies each to `proto/` in turn. Runs green after each and records `caught_by` (failing ids, or "not caught"). Restores the file byte for byte (hash-checked), even after a crash. Refuses an `old` that matches zero times or more than once. | 🟡 |
| 6 | **Compact output**: each run prints the summary line, failing ids and first assertion line only. The full pytest log goes to `DIR/logs/<run>.log`, and the JSON names its path. | 🟡 |
| 7 | **Harness hygiene**: sets `PYTHONUTF8` and decodes with `errors="replace"`. Default pytest timeout is 600 s, with no popup window and stderr in `DIR/logs/`. Exit codes: 0 all hold, 1 a check failed, 2 usage, 254 pytest never started. | 🟡 |
| 8 | **Self-test**: a pytest file for `prove.py` on a toy package covers a red run, a green run, a caught mutation, an uncaught mutation, and restore after a crash. | 🟡 |
| 9 | **Drafter wiring**: the `spec-channel-drafter.js` brief names this one command in place of its red, prototype and mutation recipe. | 🟡 |
| 10 | **Home**: `.claude/workflows/tools/prove.py`, untracked like the other tools there. The PR carries docs only: this page, a `standing-practice.md` line, and the backlog and metrics rows. The self-test run goes in the PR body. | 🟡 |

## Readings the build chose where the list was silent

- Item 7: the timeout default is 600 s, so an override exists: `--timeout SECONDS`.
- Item 3: red prints only the tests that did not fail on an assertion
  (`passed`, `skipped`, `not_assertion` with each one's exception name), since
  the expected state is every test failing.
- Item 5: a hard kill (not a crash) leaves a mutation in place, so each mutation
  is journaled in `DIR/logs/journal.json` with the original bytes, and the next
  run restores the file first and says so under `recovered`. When green is not
  ok the loop is skipped: every mutation would read as caught.
- Item 6: `log` and `package` print relative to the scratch folder, which the
  JSON names once under `scratch`.
- A mutation that makes pytest time out reads `caught_by: ["(timeout)"]`.
- Measure: the first drafter run that uses it (the next unit's) is compared
  in `docs/session-metrics.md` with `s6-release`'s 299K tokens and 124 calls.
  Items go 🟢 on that run. This session added no metrics row, since the record
  keeps rows for sessions that ship a unit.

## Why this page is not under `docs/features/`

The tree reads feature documents from `docs/features/`, so a page there would
enter it as a feature. `prove.py` is a workflow tool, not a kit feature.
