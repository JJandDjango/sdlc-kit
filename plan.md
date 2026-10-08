# Plan - Session 84 (2026-10-07) - G1's design document

**Deliverable:** `docs/features/g1-requirements-spec.design.md` written
from S1 to the engineer seat's signature, through a design run on kit
0.19.0's flows, on main through one PR.

- The run: `/sdlc:product-specification-interview g1-requirements-spec
  design`, from the installed plugin at `8635064`, whose `skills/` equal
  the tag's. It resumes at S1 and ends at E7.
- The design stands against requirements r3 and changes no byte of
  `docs/features/g1-requirements-spec.md`.
- The signature breaks the pins that read G1's pair: three tests in
  `tests/test_document_split_g1_pair.py`. They retire in the same
  commit, so the suite reads green at it. USAGE's drawing at
  `USAGE.md:1644` stays, a dated example (shape call 13).

This is step 1 of 3 toward G1's intake, which turns the tree's
`gates/G0` line `done`. Steps 2 and 3 are on the deferred list.

Claude's readings, each told to the user here:

- The user answers in batches of proposed text, as in session 75: five
  batches and the signature. The flow asks one question at a time; each
  section is still written as its step closes.
- The shape calls come first, before S1: Scope depends on them, and
  each lands as an entry under Decisions at S10.
- Requirements r3 holds three stale facts (15 features done where 18
  are, 14 ready checks where 15 are, the `gates/G0` line as 0.16.0
  printed it). The design says what it builds against each, and consult
  case 1 records the question and its answer. The requirements
  document's own words are the PO seat's to amend.
- One commit holds the design document, its state file and the retired
  pins, under `Contract: document-split`: `tests/` is a bound path in
  that contract's scope, and `docs/` is free. `scope-check` reads the
  scope and no closed mark.
- Step 2 runs one Workflow of four read-only agents. This plan's
  approval is the word for it.

The session boundary, if context runs short: after step 2 (the
explorers' files saved); after any batch (the state file names the step
to resume at). The run is resumable at every step.

## Steps

1. ~~Open.~~ Branch `session-84-g1-design` from `8635064`; this plan,
   committed on the user's word (`ce9f7ff`).
2. ~~Read the materials.~~ One Workflow of four read-only explorers, a
   slice each, every one returning change sites, pinning tests and
   design questions with `file:line`:
   - the rules: the validator, `taskcontract/data/gates.yaml`, how G0's
     conditions own their codes, G1's page and ADR 0007;
   - the tree and the pane: where a G1 verdict and its conditions take
     a status, the inactive mark, the roll-up;
   - the progress record: `progress start`, where SC4.2's refusal
     lands, and how `.sdlc/config.yaml` activates a gate;
   - intake's I9, the `/sdlc` skill, and the pages and version files a
     release changes.
   Results saved, one file a slice, in untracked
   `RECEIPT_g1-requirements-spec-design_2026-10-07/` (`rules.md`,
   `tree.md`, `progress.md`, `intake-release.md`); 897K tokens.
3. ~~Batch 1, the shape calls,~~ each with Claude's recommendation: where
   the component declaration record lives; the review record's form and
   place; G1's rules and their codes; where a lint result and a
   model-check result are recorded; the venue; how a feature past G0
   reads G1 active while the 18 done read it inactive; the unit count
   and the release.
4. ~~Resume the run.~~ The skill's base directory reads `863506491ca9`;
   DESIGN CONFIRM finds the requirements at r3, no newer.
5. ~~Batch 2:~~ S1 Scope, S2 Out of scope, S3 Interfaces, with each
   command, output and message drawn and the five messages word for
   word.
6. ~~Batch 3:~~ S4 Sources, S5 Constraints.
7. ~~Batch 4:~~ S6 Units, S7 Order. Every check stands in one unit, a unit
   holds at most three sketches, and each done means is probed through
   `lang-check --draft` on a scratch state file and reworded to zero
   findings before the user sees it.
8. ~~Batch 5:~~ S8 Risks and cost, S9 Consult cases, S10 Decisions and open
   questions, S11 Links out, S12 Notes.
9. ~~The checks before signing,~~ E1 to E5: the draft check, Scope against
   the release unit's paths, ready checks 11 to 15, the stale read, and
   the `Measured:` row.
10. ~~E6 and E7:~~ the user signs or names a section to go back to; the
    signature writes the text row and the `Signed:` row.
11. ~~The pins.~~ The whole suite on the signed state names every test the
    signature breaks; `test-retirer.js` retires them, run on those
    modules alone. USAGE's drawing stays as it reads.
12. ~~Commit,~~ on the user's word: one commit, `Contract: document-split`.
    Then the suite green at the clean commit, `scope-check --base
    8635064`, and `lang-check`.
13. ~~Close.~~ `STATE.md` regenerated, this plan struck, the memory index
    updated; the push, the PR and the merge on the user's word, after
    CI reads green.

Decisions this session: nine planned. The user's: (1) this plan and
its commit; (2) to (6) the five batches; (7) the signature; (8) the
commit, the push and the PR; (9) the merge. Claude's, on review and
told: the retired tests.

As it went: (1) the user approved this plan and its commit, `ce9f7ff`.
(2) Batch 1: the user ratified 13 shape calls as proposed. (3) Batch
2: the user ratified Scope (28 paths), Out of scope (12 places) and
Interfaces with 11 details. (4) Batch 3: Sources (15 rows) and
Constraints (15). (5) Batch 4: six units, `s1-lint` to `s6-release`,
each done means at zero language findings, and the order; SC4.3 moved
to the release unit, since intake refuses a unit with no check; detail
8 changed, so a contract's close is refused too. (6) Batch 5: Risks
and cost, the four consult cases (each yes), 21 decisions, Links out
and Notes; the cost line reads 3.7 million agent tokens at
document-split's recorded pace, 4 to 5 million likely. The checks
before signing: 3 findings, each a copied term's and each answered;
Scope covered; ready checks 11 to 15 with no gap, after two drawings
joined Interfaces. (7) The user signed: r3 is the text row, r4 the
signature, and the run pauses at W1.

Step 11, as it went. The whole suite on the signed state, under the
system Python: 3 failed, 1059 passed, the three in
`tests/test_document_split_g1_pair.py`. `test-retirer.js` retired them
on that module alone (61.6K tokens): the tree's line, the pane's line
and USAGE's drawing of G1's pair, each a pin of the pair before the
signature. The module's fourth test stays; its unused names, imports
and docstring sentences went with the three. Claude reviewed the
module and placed it.

Steps 12 and 13. (8) The user gave the word for both commits, the push
and the PR. `cb56c87` holds the design document, its state file and the
retired tests. The whole suite read 1059 passed before the commit;
`scope-check --base 8635064` reads `scope-green` and `lang-check` reads
`lang-green` at it. The wrap rides the same PR. Decision (9), the
merge, waits on the user's word after CI.

**Closed.** The deliverable is met: G1's design document stands signed
at r3. The session closed near the user's 40% context mark.

The shape calls, ratified 2026-10-07. Calls 3, 8 and 10 go past
requirements r3, so the PO seat's amendment carries them.

1. Command: G1's rules run in a new subcommand, `python -m taskcontract
   g1-check`, never inside `validate`; ready-green keeps meaning G0
   alone.
2. Codes: a new prefix, `RS`, numbered by condition (`RS1nn` G1.1,
   `RS2nn` G1.2, `RS3nn` G1.3), listed under `rules:` in `gates.yaml`.
3. Status: a condition reads `to do` and lists nothing when nothing is
   recorded or its record no longer matches its inputs; `failed` on a
   missing tool, a missing model, a red run or an unchecked item; else
   `done`. A lint that ran red and a model check that ran red get
   messages 6 and 7, which the design draws.
4. Verdict: G1 is the ratified roll-up of its three conditions, so a
   feature with no schema and no hard core reads G1 `doing` until its
   review is signed.
5. Results: a kit command runs the repository's pinned tool and writes
   a committed record bound to its inputs (each file's hash and the
   pin); the rule reads only the record. One file a feature,
   `.sdlc/g1/<feature>.yaml`, holds lint results, model-check results
   and the review.
6. Review signature: the review record carries the signer's name, seat,
   date and both revisions, and counts only while both match the
   contract's `Ready:` rows. "No agent signs" is a rule of the flow.
7. Declarations: the component declaration record is
   `specs/components.yaml` with a new schema at 1.0.0; the
   boundary-schema patterns and the tool pins sit in
   `.sdlc/config.yaml`. Each is required once G1 is active: absent
   reads `to do`, an empty list says none. The contract schema stays at
   1.5.0.
8. Venue: a new flow, `/sdlc g1 {id}`, runs the two checks, asks the
   person the 11 items one at a time and writes the records through one
   writer. Intake's I9 names it only where `G1` is active.
9. Done features: `G1` joins `active_gates`, and a committed list in
   `.sdlc/config.yaml` names the features exempt from it; a feature not
   on the list needs G1.
10. The refusal: `progress start` and `progress done` refuse any task
    of any unit until G1 passes; `block` and `run` stay open.
11. CI: no change.
12. Units and release: six units as kit 0.20.0: lint, model check,
    review, the refusal with I9, the tree, then a release unit of
    versions and pages where the kit turns G1 on for itself.
13. This session's pins: retire the three tests the signature breaks,
    through the test-retirer; USAGE's drawing stays, a dated example.

Deferred, not this session:
- Step 2 toward intake, the PO seat's: amend the requirements document
  (the three stale facts, the "Ready check" term's count) and add one
  Gherkin scenario for each of its 15 checks. It holds no state file,
  so whether a requirements run takes it or the seat amends it by hand
  is open. The engineer seat then confirms the design against the new
  revision and signs again.
- Step 3 toward intake: the new terms ratified in their own commit,
  then `/sdlc intake docs/features/g1-requirements-spec.md`. USAGE's
  drawing of G1 as a feature before intake retires there.
- The tree names no feature in flight: the top line is always
  `gates/G0`, and the feature shows only in its diagnostic and in the
  one `[doing]` feature line (the user, 2026-10-07). A top line for it,
  or features not done printed first, is a feature of its own.
- A design run's opening fixes no shape for its copy of the terms: kit
  0.19.0's live run wrote `answers.terms` as a mapping, and `lang-check
  --draft` reads a list, so E1 read no copied term. This session
  rewrote G1's copy as the list (`tools/state_terms.py`); the flow's
  sentence in `opening.md` is a later fix.
- The interview's `SKILL.md` printed its id variable as `design` at this
  session's dispatch: the harness reads `$1` as the second word. The
  session parsed the id from its own arguments.
- The engine's install ref, its pilot config line and M0's code: after
  G1 ships.
- W1, the Google Docs form. The `google_workspace` server failed to
  connect again at this resume.
- `STATE.md` Next actions 2 to 5 and its open questions, carried.

House rules in force: no pipes or chains in any authored command
string; commit messages via Write + `git commit -F`; Workflows launched
by `scriptPath`; a `Contract:` trailer, alone in the final paragraph, on
every commit that touches a bound path; no tracked file touched while
an agent runs; never two whole suites at once; no spawn opens a window.
