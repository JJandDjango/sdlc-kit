# Post-mortem: G1 unreachable from a plain request

Session 147, 2026-11-12. Found by the engine (`E:\ImSimProject\engine`, kit `v0.22.0`), finding `g1-unreachable-from-a-plain-request`. Charged to sessions 97 and 98 (`s5-start`).

## The defect

Intake drafts a contract from a plain request with no feature document. With G1 active, its report ends `Next step: G1. Run /sdlc g1 {id}.` (`skills/sdlc/flows/intake.md:40`). G1.3's review reads the contract's revisions from the feature document and refuses a contract with none (`taskcontract/g1.py:636`, `:1101`), so G1.3 reads `to do` forever (`:701`). `progress start` refuses every task until G1 passes. The contract is green at G0 and can never be built. The kit holds a second case: `glossary-alias-disjointness`, which has a contract, no feature document, and is not on `g1.exempt`.

## How it passed each check

1. **Requirements, r6 (2026-10-08).** SC4.1's scenario opens "Given a contract at intake's report": any contract. Consult case 1 asked whether I9 always names G1 and answered on one axis, whether G1 is active. Nobody asked whether the contract has a document.
2. **Design, r5 and r6 (2026-10-08).** The Review term binds "a pair's two revisions". The Sources row reads only `active_gates` and `g1.exempt`. Shape call 9 kept `glossary-alias-disjointness`, a contract with no document, off the exempt list (design `:428`), so the case stood in the design and nobody read its G1.3. The checks before signing (r2, r8) measured wording and OPEN marks, not paths into G1.
3. **`s3-review`, session 92 (PR #112).** The build found the case and settled it as reading 3: "The cost is real: a feature taken in with no feature document cannot pass G1." The cost was true and small at the time, since G1 refused nothing yet. The user kept all 12 readings (session 93). The PR said they "belong in the design at its next text row".
4. **The design's next text row, r9 (session 101, 2026-10-17).** It carried session 90's G1.1 ruling alone. PR #112's 12 readings, PR #116's 15 and PR #119's 12 stayed in PR bodies and the backlog. The backlog kept reading 3 as a fact ("so a feature with no feature document cannot pass G1"), not as an edge with a fix.
5. **`s5-start`, sessions 97 and 98 (PR #119).** It was built from the design, which held no reading 3. Its refusal turned "cannot pass G1" into "no task can start", and I9 pointed every ready-green contract at G1. The test list, approved by Claude at `be5562b`, held 11 text tests on I9's words and 28 on the refusal. None put intake's output into G1's input. The live receipt ran this exact path, "a plain request" with G1 listed, and took the G1 line and the refusal (`apply-code cannot start`) as the expected output. It never ran the step the line names.
6. **`s6-release`, 0.20.0 (2026-10-18).** G1 went on at the kit. From then on, the tree printed `glossary-alias-disjointness` with G1.3 `to do`, the same words as a feature not yet reviewed. It stood that way in every print for 25 days.
7. **The pilots.** Every feature since G1 went on entered through a pair, by the user's practice (a feature starts as an interviewed feature document). No real run took a plain request through G1 until the engine on 2026-11-12.

## The causes

1. **Readings live outside the design.** Each PR settles cases the design never named and promises them to the next text row. That row came and took none of them. Later units are drafted from the design, so they cannot see a reading whose cost they raise.
2. **A reading's cost is judged once.** Reading 3 was judged against the system of session 92, when G1 refused nothing. `s5-start` raised the cost to "the feature can never be built", and nothing re-read the earlier readings.
3. **Hand-off checks stop at the hand-off.** The test and the receipt checked that intake names G1; neither took the step G1 names. A refusal was the expected output, so the dead end read as success.
4. **`to do` does not tell "not yet" from "never".** The kit's own case was in plain view and looked normal.

## Proposed changes

For an ADR, drafted only on the user's yes:

1. The design's next text row takes every reading the PRs settled since its last row, or names each one it leaves out and why. Its `Measured:` row counts them.
2. A unit that adds a refusal or turns a gate on re-reads its feature's open readings for any whose cost it raises, and its PR names them.
3. A hand-off's tests and receipt take the step it hands to, on each path into the hand-off: a plain request and a pair.
4. A condition that can never read `done` says so, and names its way out.

## The tripwire

The escape traces to an approval Claude gave: `s5-start`'s test list (`.sdlc/progress/g1-requirements-spec.yaml:683`, `by: claude`). By `docs/session-metrics.md`, test lists return to the user until the user rules otherwise.
