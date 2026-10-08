# Plan - Session 84 (2026-10-07) - G1's design document

**Deliverable:** `docs/features/g1-requirements-spec.design.md` written
from S1 to the engineer seat's signature, through a design run on kit
0.19.0's flows, on main through one PR.

- The run: `/sdlc:product-specification-interview g1-requirements-spec
  design`, from the installed plugin at `8635064`, whose `skills/` equal
  the tag's. It resumes at S1 and ends at E7.
- The design stands against requirements r3 and changes no byte of
  `docs/features/g1-requirements-spec.md`.
- The signature moves the pins that read G1's pair: three tests in
  `tests/test_document_split_g1_pair.py` and USAGE's drawing at
  `USAGE.md:1644`. They move in the same commit, so the suite reads
  green at it.

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
- One commit holds the design document, its state file and the moved
  pins, under `Contract: document-split`: `tests/` and `USAGE.md` are
  bound paths in that contract's scope, and `docs/` is free.
  `scope-check` reads the scope and no closed mark.
- Step 2 runs one Workflow of four read-only agents. This plan's
  approval is the word for it.

The session boundary, if context runs short: after step 2 (the
explorers' files saved); after any batch (the state file names the step
to resume at). The run is resumable at every step.

## Steps

1. Open. Branch `session-84-g1-design` from `8635064`; this plan,
   committed on the user's word.
2. Read the materials. One Workflow of four read-only explorers, a
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
   `RECEIPT_g1-requirements-spec-design_2026-10-07/`.
3. Batch 1, the shape calls, each with Claude's recommendation: where
   the component declaration record lives; the review record's form and
   place; G1's rules and their codes; where a lint result and a
   model-check result are recorded; the venue; how a feature past G0
   reads G1 active while the 18 done read it inactive; the unit count
   and the release.
4. Resume the run. The skill's base directory reads `863506491ca9`;
   DESIGN CONFIRM finds the requirements at r3, no newer.
5. Batch 2: S1 Scope, S2 Out of scope, S3 Interfaces, with each
   command, output and message drawn and the five messages word for
   word.
6. Batch 3: S4 Sources, S5 Constraints.
7. Batch 4: S6 Units, S7 Order. Every check stands in one unit, a unit
   holds at most three sketches, and each done means is probed through
   `lang-check --draft` on a scratch state file and reworded to zero
   findings before the user sees it.
8. Batch 5: S8 Risks and cost, S9 Consult cases, S10 Decisions and open
   questions, S11 Links out, S12 Notes.
9. The checks before signing, E1 to E5: the draft check, Scope against
   the release unit's paths, ready checks 11 to 15, the stale read, and
   the `Measured:` row.
10. E6 and E7: the user signs or names a section to go back to; the
    signature writes the text row and the `Signed:` row.
11. The pins. The whole suite on the signed state names every test the
    signature moves. USAGE's drawing and its lead sentence go to the
    user, before and after; Claude amends the test's strings and tells
    the user each.
12. Commit, on the user's word: one commit, `Contract: document-split`.
    Then the suite green at the clean commit, `scope-check --base
    8635064`, and `lang-check`.
13. Close. `STATE.md` regenerated, this plan struck, the memory index
    updated; the push, the PR and the merge on the user's word, after
    CI reads green.

Decisions this session: ten planned. The user's: (1) this plan and its
commit; (2) to (6) the five batches; (7) the signature; (8) USAGE's
drawing; (9) the commit, the push and the PR; (10) the merge. Claude's,
on review and told: the test's amended strings.

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
