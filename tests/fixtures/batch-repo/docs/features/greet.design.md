# greet - A greeting

| Date | Revised By | Changes |
| :-- | :-- | :-- |
| 2026-10-28 | Ann Lee | r1: the text at r1 |
| 2026-10-28 | Ann Lee | r2: the text at r2 |
| 2026-10-28 | Ann Lee | r3: the text at r3 |
| 2026-10-28 | Ann Lee | r4: the text at r4 |
| 2026-10-28 | intake | r5: Ready: contract `greet` validates ready-green, derived from r4 |

## Statement

One batch file, `src\greet.bat`, takes the name as its first argument (`%~1`). The functional tests are batch files under `tests\`, named `test_*.bat`, one file a check; each exits 0 when its check holds and 1 when it fails, and calls `src\greet.bat` from the repository root. `test.bat` at the root is the declared test command: it runs every `tests\test_*.bat`, or the one file named as its first argument, and exits 1 when any fails.
