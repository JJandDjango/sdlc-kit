# Plan - Session 90 (2026-10-09) - g1-requirements-spec s2

**Deliverable:** unit `s2-model` of `g1-requirements-spec` on one PR,
with a Two-Key PASS. It is the second unit of kit 0.20.0.

What the unit ships:

- The component declaration record's schema,
  `taskcontract/schemas/component-declaration.schema.json` at 1.0.0,
  and its reader in `taskcontract/g1.py`.
- `g1-record model <id>`: it starts the checker of each hard core in
  scope and appends one G1.2 record.
- G1.2's three rules in `g1-check`: `RS201` (a hard core has no model),
  `RS202` (the checker is not installed) and `RS203` (the model does
  not pass).
- The unit's `done_means`: with a hard core in a feature's scope, G1.2
  reads done only when the record shows its model passes the checker.
  Checks SC3.1, SC3.2 and SC3.3.
- SC3.1 also takes a manual receipt: a live TLC run on one passing
  model and one failing model.
- Retirements: none. An older test that fails on the prototype is an
  amendment or a finding, listed at the top of the PR body.

Read at this resume: HEAD equals `origin/main` at `8625df9` (PR #108),
tag `v0.19.0` stands at `7fe6342`, the tree holds untracked files only,
and the engine's `STATE.md` is unchanged since 2026-09-21. Java is
Temurin 21.0.12.1. No `tlc` command is on PATH, and no `tla2tools.jar`
stands where one was looked for (the VS Code extensions).

The flow is "plan approved, then PR review", in its first build. This
plan's approval decides the three rulings below. After it, the next
word needed from the user is the work PR's merge. A reading that
surfaces mid-build is Claude's, listed at the top of the PR body; one
that would change a signed contract sentence, a ratified term or an ADR
stops for the user.

The tight spot: the design's risk 2. TLC is a Java program with no
command of its own, and it ends on more exit codes than a linter. Step
2 probes it live before any test names its call: the code for a passing
model, for a broken invariant, for a deadlock and for an error of its
own, and where it writes its state files. P gets no live run: its call
is read from its reference page and held by a stand-in, as `buf`'s was.

## Rulings

1. **A feature with schemas under two `g1.schemas` entries.** It is
   `STATE.md`'s first open edge: `g1-record lint` refuses such a
   feature, so its G1.1 can never read done. Recommendation: one record
   a call that holds each entry's run, each with its own linter and
   pin. ADR 0038 says "Each call appends one record, and the last
   record of a condition counts", and the design and USAGE repeat it.
   This option keeps that sentence true, and the G1.2 record already
   has the form: one entry a hard core, each with its tool. The other
   option, one record an entry, keeps `s1-lint`'s shape tests and costs
   an amending ADR. The build is not this session's. It changes the
   design's drawing of the record, so it takes a design text row, the
   engineer seat's signature and a re-intake, in its own session before
   `s6-release`. This session only shapes the G1.2 record to match.
2. **How `g1-record model` finds TLC.** Recommendation: by the bare
   name `tlc` on PATH, as `lint` finds Spectral. A consumer whose
   install is the jar alone writes a wrapper script of that name. The
   other option, the kit starting `java` with a jar path from a new
   config key, adds a key the signed design does not draw. USAGE gains
   one red sentence that says so.
3. **TLC on this machine.** Recommendation: `tla2tools.jar` from
   release v1.7.4 of `tlaplus/tlaplus` (2024-08-05, the newest that is
   no pre-release), in `C:/Users/hyden/tools/tlaplus/` with a `tlc.cmd`
   beside it. No global PATH change: the probe and the receipt script
   set PATH for their own child process.

Claude's readings, each told here:

- The unit builds the schema and the reader. The kit's own
  `specs/components.yaml` is a declaration a person writes, and it
  lands when `s6-release` turns G1 on at the kit.
- USAGE holds the unit's guide, red, since pass zero. Its marks stay
  red until `s6-release`.
- Step 2's finding fixes which of TLC's exit codes read `fail` and
  which are an error of its own. Lint's edge is the pattern: a tool
  that ends on its own error gives no result, so `model` prints the
  tool's lines, writes nothing and exits 2.

## Steps

1. Open. Branch `session-90-g1-s2-model` from `8625df9`; this plan,
   committed and pushed, then shown for approval.
2. TLC, risk 2. Fetch the jar by ruling 3. A scratch script starts TLC
   by the bare name from Python on a passing model, a failing one, a
   deadlock, a model that does not parse and an absent configuration,
   and prints each argv, its exit code and both streams. The script and
   its output go to untracked
   `RECEIPT_g1-requirements-spec-s2_2026-10-09/`.
3. Draft. `spec-channel-drafter.js` drafts the test list for SC3.1,
   SC3.2 and SC3.3 with a stand-in checker, proves it red from the repo
   root, and proves it satisfiable on a scratch copy of the
   `taskcontract` package. It reads the probe's files and the
   explorers' `rules.md`.
4. Overlay. The session overlays the prototype on a scratch worktree
   and runs the whole suite there. `test-retirer.js` runs only if an
   older test fails, on the failing modules alone.
5. Approve the list and prove red (Claude). Each fixed detail is
   checked against the contract, the pair, its Constraints and
   Decisions, the ratified terms under `specs/vocabulary/` and USAGE's
   red text; session labels are stripped; then `progress run <check>
   --expect red` for each check.
6. Green. `unit-developer.js` from the interface note, handed over as a
   file. Claude runs the suite after each round and tests each
   deviation and each returned question against `done_means`.
7. Commit (Claude). The unit's commit with the `Contract:` trailer and
   ruling 2's USAGE sentence; each check green at the clean commit;
   `validate --profile ready` and `scope-check --base 8625df9`.
8. Manual receipt. A live TLC run through `g1-record model` on one
   passing model and one failing model, in a small consumer repository
   a script builds. Its text goes to the receipt folder.
9. Two-Key. `two-key-unit-verifier.js`, with the receipt's text as a
   focus pointer; `progress done` on PASS.
10. The work's close. The push, then the PR once CI reads green and
    Two-Key reads PASS, with Claude's readings at the top of its body.
    The merge is on the user's word.
11. The wrap, after the merge. `STATE.md` regenerated, this plan
    struck, the memory index updated and one row appended to
    `docs/session-metrics.md`, on a new branch off main in a wrap-only
    PR that Claude merges after green CI.

Steps 1, 2, 10 and 11 sit outside a contract unit, so the tree does not
show them.

The session boundary, if context runs short: after step 5. The approved
list, the prototype and the interface note are copied to the receipt
folder, and the developer round opens the next session.

## Cost

About 0.6 million agent tokens, in a range of 0.55 to 0.7 million. The
basis is two recorded code units: `d4` at 561K (drafter 213K,
developers 94K and 75K, Two-Key 179K) and `s1-lint`'s first round at
594K (drafter 225K, developers 104K and 60K, Two-Key 205K). A lost
Two-Key round adds about 300K: `s1-lint`'s second cost 316K (developer
69K, Two-Key 247K). A retirer round, if an older test fails, adds 62K
to 159K.

## Deferred, not this session

- `s3-review` to `s6-release` (ships 0.20.0), one unit a session.
- Ruling 1's build: the design's text row, its signature, the re-intake
  and the change to `lint`, before `s6-release`.
- G1.1's four other edges and the four smaller ones, under `STATE.md`'s
  Open questions.
- A live run of P, and of `buf`.
- The engine's install ref, its pilot config line and M0's code: after
  G1 ships.
- The `google_workspace` server failed to connect again at this resume.
- `STATE.md` runs past its one-page budget.
- `STATE.md` Next actions 2 to 5 and its other open questions, carried.
