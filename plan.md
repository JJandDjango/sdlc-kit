# Plan - Session 95 (2026-10-12) - g1-requirements-spec s4, round 4

```
Project  SDLC kit: gates that stop agent-written code from degrading a codebase.
Area     G1, the requirements gate: a feature's failure points are found before its development starts.
Feature  g1-requirements-spec: the kit computes G1 and refuses a task until G1 passes.
Unit     s4-tree, the fourth of six: the tree shows G1 with each condition's status, its diagnostics and the review.
```

This plan stands under session 94's plan for the same unit and repeats
none of it. That plan reads at
`https://github.com/JJandDjango/sdlc-kit/blob/f23440f/plan.md`: its
sections 2, 5 and 10 hold where the unit sits, the rule for a case no
page names, and the words. The three pages above it stand as they
stood: the feature page, the design page and the contract.

## 1. The deliverable

By the session's end unit `s4-tree` stands on main through one PR, with
a passing independent grade.

## 2. Where this sits

The unit is built. It stands on this branch at `46d2273`, and the whole
suite reads 1697 passed there.

Two-Key is the independent grade: a second agent runs the unit's
receipts and grades it against the contract with no trust in the
builder. It failed the unit three times in session 94. Each round
graded the three checks PASS, and each found one more text a person
can write that makes G1's reading raise an error, which stops the whole
tree print while G1 is active. Each fix guarded the calls that had
failed. The causes cannot be listed, so the plan stopped the build.

The user ruled on 2026-10-12: a round 4, with one guard at the
boundary.

The boundary is `build` in `taskcontract/tree.py`. The print, the pane
and the progress command each take the tree from that one function.
With G1 active, a build that ends on an error is made again with no G1
source read. In that second build every feature holds G1 active, each
G1 condition reads `to do`, and one problem line names what the first
build ended on. If the second build ends on an error too, no G1 text
is the cause, and the error stands as it stands on main.

## 3. The steps

1. This plan, committed and pushed on the branch.
2. The tests, written by the session into `tests/test_g1_tree.py` and
   proven red at `46d2273`. They hold round 3's number under
   `g1.exempt`; a stand-in (a test replaces one function with one that
   raises) at each of the five places G1's code is entered; an error
   whose message cannot be made; and a problem line of another source,
   which keeps its place.
3. The fix note, as a file. One developer agent
   (`.claude/workflows/unit-developer.js`: it changes code and never
   opens the tests) changes `taskcontract/tree.py` from it.
4. USAGE: the sixth problem line's second form, and the pane sentence
   narrowed to the files outside the watched folders (round 3's
   advisory).
5. The whole suite, run by the session. The commit. Each check green at
   the clean commit.
6. The trial of hostile inputs again (`trial.py` in the receipt
   folder), with round 3's two inputs and the scope advisory's added.
7. Two-Key round 4 (`.claude/workflows/two-key-unit-verifier.js`),
   asked to grade the guard.
8. On a PASS: the unit closed in the progress record; `git rm plan.md`
   as the branch's last commit; the push; the PR, its body from the
   receipt folder's draft brought up to date; CI.
9. The user's merge.
10. The wrap in its own PR: `STATE.md`, one metrics row for sessions 94
    and 95 as one build, the memory index.

## 4. Where Claude stops for the user

Twice at most. The work PR (step 9): the merge is the user's word. And
a failed round 4: Claude stops and brings the verdict, and starts no
round 5 alone.

## 5. Where Claude goes on alone, and by what rule

Alone: everything before the PR, and the wrap's merge after green CI.
The rule is session 94's: where the pages name no case, Claude rules
from their purpose, builds on that reading, and lists it at the top of
the PR body. The test for any event: the tree may never read a
condition `done` where `g1-check` does not.

## 6. Rulings needed

None. Three readings join the ten of session 94 at the top of the PR
body:

11. The second build reads no exemption, so every feature holds G1
    active and each of its conditions reads `to do`. Nothing is proven
    there, so nothing reads `done`, and a `g1.exempt` list that cannot
    be read already exempts nothing.
12. The line is the sixth problem line with the gate where a
    condition's id stands: `unreadable G1 reading: G1 (<class>:
    <message>)`. It is the last line of the print and the only G1
    problem line of that print. An error whose message cannot be made
    prints its class name alone.
13. A text that makes the reading run without end raises nothing, so no
    guard holds it. The PR body names it as an open edge.

## 7. What could go wrong, already ruled

- Round 4 fails: section 4.
- One of the 98 older cases fails after the fix: the fix is wrong, and
  the test stands.
- The kit's own print changes: it may not. The hash receipt is taken
  again and must read `31479f04...`, main's.
- The developer returns a question or a shortcut: it is tested against
  each `done_means` sentence before it is accepted.
- The session's context nears 40% before Two-Key returns: the session
  stops at the open PR, and the wrap rides the next session.

## 8. This session's cost, with its basis

About 280K to 360K agent tokens. The basis is session 94's recorded
fix rounds: the developer took 71K and 102K, and Two-Key took 207K,
242K and 256K. The unit's total then stands near 1.6 million against a
first plan of 0.6 million.

## 9. Not in this session

- Units `s5-start` and `s6-release`.
- Session 90's first ruling (one G1.1 record a call) and the fix of
  G1.1's escaped defect, in their own session before `s6-release`.
- `g1-check` calls the three readers bare, so it still ends on a
  traceback where the tree now prints a problem line.
- The older defects session 94 listed for `STATE.md`'s Open questions:
  a contract that is not UTF-8 under G0, and the YAML loader's plain
  ValueError in `tree._load` and `scope_check.contract_scope`.

## 10. Words

- Boundary: the one function a caller enters to reach a body of code.
  Here `build`, for everything the tree does for G1.
- Problem line: a line the tree prints on standard error for a source
  it cannot read. The print goes on.
- Receipt: a command's saved output, kept as proof of a claim.
- Round: one run of Two-Key on one commit.
- Stand-in: a function a test puts in another's place.
- Trial: a script that feeds hostile inputs to the tree and to
  `g1-check` and prints what each does. It asserts nothing.
