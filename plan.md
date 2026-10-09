# Plan - Session 88 (2026-10-08) - g1-requirements-spec s1

**Deliverable:** unit `s1-lint` of `g1-requirements-spec` on one PR,
with a Two-Key PASS. It is the first unit of kit 0.20.0:

- `USAGE.md` gains its guide to G1 first, every status mark red (pass
  zero).
- The base the other five units stand on: `taskcontract/g1.py`, the
  record file under `.sdlc/g1/`, the declarations' readers and both
  commands, `g1-check` and `g1-record`.
- The unit's `done_means`: with a boundary schema in a feature's scope,
  G1.1 reads done only when the pinned linter's record shows it clean.
  Checks SC2.1, SC2.2 and SC2.3.
- SC2.1 also takes a manual receipt: a live Spectral run on one clean
  file and one unclean file.
- Retired: USAGE's red-legend test, at pass zero
  (`tests/test_document_split_release.py:517-527`). Replaced: the two
  tests that hold `rules:` to G0's conditions
  (`tests/test_tree_conditions.py:313-327` and `432-442`), each by one
  that holds G1's too. Any other older test that fails on the prototype
  is an amendment or a finding, and each goes to the user.

Session 87 left the contract at ready on main at `fe8bd7b` (PR #104),
and its wrap merged as PR #105 at `4bec8eb`. Read at this resume: HEAD
equals `origin/main` at `4bec8eb`, tag `v0.19.0` stands at `7fe6342`,
the tree holds untracked files only, and the engine's `STATE.md` is
unchanged since 2026-09-21. Node is `v24.10.0`, and Spectral is not
installed.

The tight spot: the design's risk 1. Spectral may not lint a plain JSON
Schema file without a ruleset the kit writes, and prerequisite 8 rests
on it. Step 2 settles it with a live run before any text or test names
the linter's command. A finding that changes the design is an OPEN and
a re-intake, never a silent edit.

Approvals split as in sessions 78 to 83: the user approves the USAGE
text in chat before any drafting; Claude approves the test list and the
unit's commit on review; the plan's commit, each push, each PR and each
merge stay on the user's word.

The cost in agent tokens: about 0.6 to 0.8 million. The basis is `d4`,
the last code unit, at 561K (drafter 213K, developers 94K and 75K,
Two-Key 179K), plus a retirer round, which has run 62K to 159K. A lost
Two-Key round adds about 300K. This unit lays the base, so its drafter
may read more than `d4`'s.

Claude's readings, each told to the user here:

- Risk 1 runs before pass zero. The guide's sentences on the pin and
  the linter's command rest on its finding.
- Spectral's install is one on this machine, on the user's word:
  `npm install -g @stoplight/spectral-cli@6.17.0`, the newest version
  npm lists today. `s6-release`'s receipt needs it again. The kit ships
  no linter (the contract's third non-goal).
- No task is refused this session: `progress start` and `progress done`
  refuse on G1 only from `s5-start`.
- USAGE's drawing of this feature before intake (`USAGE.md:1640-1655`)
  stays as a dated example; `s6-release` redraws it.

The session boundary, if context runs short: after step 6. The approved
list, the prototype and the interface note are copied to an untracked
folder in this root, and the developer round opens the next session.

## Steps

1. Open. Branch `session-88-g1-s1-lint` from `4bec8eb`; this plan,
   committed on the user's word.
2. Spectral, risk 1. Install Spectral on the user's word. Run it live
   on a plain JSON Schema, one clean file and one unclean file, with no
   ruleset and with the one the design names. The finding goes to the
   user with step 3's text.
3. Pass zero. Write USAGE's guide to G1, marks red, under its own red
   subsection, shown in chat before and after. Retire the red-legend
   test in the same commit. Run the whole suite on the new text first:
   the text, the readings and the retirement go to the user as one
   decision. Commit on the user's word.
4. Draft. `spec-channel-drafter.js` drafts the test list for SC2.1,
   SC2.2 and SC2.3 with a stand-in linter, proves it red from the repo
   root, and proves it satisfiable on a scratch copy of the
   `taskcontract` package. It reads the explorers' files in
   `RECEIPT_g1-requirements-spec-design_2026-10-07/`.
5. Retire. The session overlays the prototype on a scratch worktree and
   runs the whole suite there. The two `rules:` tests are replaced.
   `test-retirer.js` runs only if another older test fails, on the
   failing modules alone.
6. Approve the list and prove red. Each fixed detail checked against
   the contract, the pair, its Constraints, the ratified terms under
   `specs/vocabulary/` and USAGE's red text; session labels stripped;
   then `progress run <check> --expect red` for each check, the command
   run alone first.
7. Green. `unit-developer.js` from the interface note, handed over as a
   file outside the drafter's folder. Claude runs the suite after each
   round and tests any deviation against `done_means`.
8. Commit. The unit's commit with the `Contract:` trailer; each check
   green at the clean commit; `validate --profile ready` and
   `scope-check --base 4bec8eb`.
9. Manual receipt. A live Spectral run through `g1-record` on one clean
   file and one unclean file. Its text goes to untracked
   `RECEIPT_g1-requirements-spec-s1_2026-10-08/`.
10. Two-Key. `two-key-unit-verifier.js`, with the receipt's text as a
    focus pointer; `progress done` on PASS.
11. The work's close. The push, the PR and the merge, on the user's
    word after CI reads green.
12. The wrap, after the merge. `STATE.md` regenerated, this plan struck
    and the memory index updated on a new branch off main, in a
    wrap-only PR that names the work's merge commit; merged on the
    user's word.

Steps 1, 2, 11 and 12 sit outside a contract unit, so the tree does not
show them.

Decisions this session: six planned. The user's: (1) the deliverable,
this plan with its commit, and Spectral's install; (2) pass zero's
USAGE text, with risk 1's finding, the retired test and its commit;
(3) the push and the PR, then the merge after CI reads green; (4) the
wrap's commit, its PR and its merge. Claude's, on review: (5) the test
list, with any amendment; (6) the unit's commit. A seventh only if risk
1's finding changes the design.

Deferred, not this session:
- `s2-model` to `s6-release` (ships 0.20.0), one unit a session.
- The engine's install ref, its pilot config line and M0's code: after
  G1 ships.
- The `google_workspace` server failed to connect again at this resume.
- `test-retirer.js` waits on the whole suite inside its agent; the fix
  stays parked, and step 5 works around it.
- `STATE.md` Next actions 2 to 5 and its open questions, carried.

House rules in force: no pipes or chains in any authored command
string; commit messages via Write + `git commit -F`; Workflows launched
by `scriptPath`; a `Contract:` trailer, alone in the final paragraph,
on every commit that touches a bound path; each task recorded through
`taskcontract progress`, each check's run through `progress run`; no
tracked file touched while a verifier runs; never two whole suites at
once; no spawn opens a window; a surprise mid-build is an OPEN and a
re-intake, never a silent edit.
