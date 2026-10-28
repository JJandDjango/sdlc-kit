# greet - A greeting

| Date | Revised By | Changes |
| :-- | :-- | :-- |
| 2026-10-28 | Ann Lee | r1: the text at r1 |
| 2026-10-28 | Ann Lee | r2: the text at r2 |
| 2026-10-28 | Ann Lee | r3: the text at r3 |
| 2026-10-28 | Ann Lee | r4: the text at r4 |
| 2026-10-28 | Ann Lee | r5: the text at r5 |
| 2026-10-28 | intake | r6: Ready: contract `greet` validates ready-green, derived from r5 |

## Statement

`src\greet.bat NAME` prints the line `Hello, NAME!` on stdout and exits 0. With no NAME it prints the line `usage: greet NAME` on stderr and exits 2.

- SC1.1: `src\greet.bat Ann` prints `Hello, Ann!` and exits 0.
- SC1.2: `src\greet.bat` with no name prints `usage: greet NAME` on stderr and exits 2.
