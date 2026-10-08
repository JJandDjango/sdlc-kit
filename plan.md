# Plan - Session 85 (2026-10-08) - G1's requirements, amended

**Deliverable:** `docs/features/g1-requirements-spec.md` amended by hand
and signed by the PO seat at a new revision, and
`docs/features/g1-requirements-spec.design.md` confirmed against that
revision and signed again by the engineer seat, on main through one PR.

- The amendment carries what the design's Notes list: the three stale
  facts, the five points of consult case 1, the Review and Ready check
  terms, and one Gherkin scenario for each of the 15 checks.
- The document was written by hand and holds no state file. The
  amendment starts none: it is a hand edit, a text row and a `Signed:
  request half` row, the standing practice.
- The amendment changes the document's bytes, so the last test of
  `tests/test_document_split_g1_pair.py` retires in the same commit.

This is step 2 of 3 toward G1's intake, which turns the tree's
`gates/G0` line `done`. Step 3 is on the deferred list.

Claude's readings, each told to the user here:

- The rows. The requirements table ends at r4, so the amendment writes
  three: `r5: Measured:`, the text row r6, and `r7: Signed: request
  half. The PO seat signs r6`. The Gherkin block's tag reads `[PO seat ·
  derived from r6]`. The design, whose table ends at r4, takes `r5:
  Confirmed against requirements r6` and `r6: Signed: solution half. The
  engineer seat signs r5`.
- The user answers in two batches of proposed text, as in sessions 75
  and 84. Each batch shows before and after for the sentences that
  change, with the full text on request.
- Messages 6 and 7, I9's condition, the refusal and the review's two
  revisions are copied word for word from the signed design: the design
  is their source, and the amendment adds no call of its own.
- Description's third case is a dated record of kit 0.16.0, so its
  quoted line and its count stay as measured then, with the date said.
  The counts that state today's facts move to 18 features done and 15
  ready checks. The PO seat rules on this in batch 1.
- "Ready check" leaves the terms to ratify and joins the terms mapped to
  a ratified one (`ready-check`, ratified after r3). Review's definition
  names both revisions of a pair.
- The retired test is its module's only test, and the design's signed
  Decisions name its retirement. The session removes the file with `git
  rm` and tells the user: `test-retirer.js` cannot delete a file. If the
  suite names any other test, that one goes through `test-retirer.js`.
- Two commits. The first holds the amended requirements document and the
  removed test, under `Contract: document-split`, since `tests/` is a
  bound path in that contract's scope. The second holds the design
  document and its state file; `docs/` is a free path.
- No Workflow is planned. The cost in agent tokens is none, or about 62K
  if the retirer runs (session 84's run on this module, 61.6K).

The session boundary, if context runs short: after step 8, where the
requirements stand signed and committed and the design reads stale until
step 9 confirms it.

## Steps

1. ~~Open.~~ Branch `session-85-g1-amendment` from `8434a9d`; this plan,
   committed on the user's word (`1af1a50`).
2. ~~Measure,~~ in the session, with no agent:
   - today's tree: the `gates/G0` line, G1's feature line, the count of
     features done;
   - the count of ready checks, from the interview's flows and intake;
   - the design's words for the five points: messages 6 and 7, I9's
     condition, the refusal on `start`, on `done` and on a contract's
     close, and the review record's two revisions;
   - the shape a requirements document holds since kit 0.19.0 (ADR 0037)
     and every step of intake that reads one, against G1's document.
   Result: one list of every sentence the amendment changes and every
   block it adds, counted after it is written.
3. ~~Batch 1, the changed text,~~ before and after: the stale facts, the
   five points in the checks and the error messages, the two terms, and
   one Decisions entry for each call.
4. ~~Batch 2, the Gherkin:~~ 15 scenarios, one for each check from SC1.1
   to SC5.3, each opening on its check's id.
5. ~~The checks before signing.~~ A scratch script builds a state file
   from the document (the statement, the non-goals, the checks, the new
   terms); `python -m taskcontract lang-check --draft` reads it. The
   session reads the document against ready checks 1 to 8. Then the row
   `r5: Measured:` in P5's shape.
6. ~~The PO seat signs,~~ or names a section to go back to. The signature
   writes the text row r6 and the `Signed:` row r7, and the Gherkin tag
   takes r6.
7. ~~The pins.~~ The whole suite on the signed state names every test the
   amendment breaks. The hash test's module goes; any other test is
   named to the user before it changes.
8. ~~Commit 1,~~ on the user's word: the requirements document and the
   removed test, `Contract: document-split` (`fb67328`).
9. ~~The design's confirmation.~~ Check that the installed plugin's
   `skills/` equal `v0.19.0`'s, then run
   `/sdlc:product-specification-interview g1-requirements-spec design`.
   DESIGN CONFIRM shows r6 and asks the engineer seat. Before the seat
   answers, the session reads the design against r6 and names any
   sentence the amendment makes false. On yes the run writes the design's
   r5 and moves the state file, with its new copy of the terms as the
   list. The seat's word then writes r6, the signature.
10. ~~Commit 2,~~ on the user's word: the design document and its state
    file (`c402782`). Then the suite green at the clean commit,
    `scope-check --base 8434a9d`, and `lang-check`.
11. ~~Close.~~ `STATE.md` regenerated, this plan struck, the memory index
    updated; the push, the PR and the merge on the user's word, after CI
    reads green.

Decisions this session: seven planned. The user's: (1) this plan and
its commit; (2) batch 1; (3) batch 2; (4) the PO seat's signature; (5)
the design's confirmation and the engineer seat's signature; (6) the
two commits, the push and the PR; (7) the merge. Claude's, on review
and told: the removed test.

As it went: (1) the user approved this plan and its commit, `1af1a50`.
(2) Batch 1: the user approved 12 items as proposed, the optional
twelfth among them, ADR 0037's shape. Six checks changed their words:
SC1.1, SC1.3, SC4.1, SC4.2, SC5.2 and SC5.3. The measure found a
fourth stale fact: r3 mapped Check to `acceptance-sketch`, and `check`
has been its own ratified term since 2026-09-30. (3) Batch 2: the user
accepted the 15 scenarios as written. The checks before signing read
93 findings (CL003 2, CL006 79, CL008 12), each of a kind r2 answered,
and ready checks 1 to 8 read no gap. (4) The user signed as the PO
seat: r6 is the text row, r7 the signature. (5) The user confirmed the
design against r6 and signed again as the engineer seat, with four
stale sentences named and left as dated records. (6) The user gave the
word for commit 1 with that answer, and for commit 2, the wrap, the
push and the PR once the suite read green. Decision (7), the merge,
waits on the user's word after CI.

Step 7, as it went. The whole suite on the signed state, under the
system Python: 1 failed, 1058 passed, the one failure the hash test.
The session removed its module with `git rm`. Two docstrings named the
module, in `tests/test_tree_halves.py` and
`tests/test_document_split_release.py`; each lost that sentence, and
the two modules read 75 passed. No test changed, and no agent ran.

Steps 9 and 10. The installed plugin sits at `8635064`, and `git diff
--stat v0.19.0 HEAD -- skills/` prints nothing. After the design's two
rows the tree reads `document r6 design r5`, with both halves `done`,
and the state file reads 14 new terms, 6 units and 2 findings (CL003
2). The whole suite read 1058 passed before commit 2 and again at the
clean commit; `scope-check --base 8434a9d` reads `scope-green` and
`lang-check` reads `lang-green` there.

**Closed.** The deliverable is met but for the merge: G1's requirements
document stands signed at r6, and its design confirmed and signed
against it.

Deferred, not this session:
- Step 3 toward intake: the new terms and ADR 0038 in their own commit,
  then `/sdlc intake docs/features/g1-requirements-spec.md`. Review is
  ratified there as r6 defines it, and three ratified terms are
  amended, where the design's Decisions count four. USAGE's drawing of
  G1 as a feature before intake retires there.
- The design's four stale sentences (Risks 7, Links out, Interfaces'
  note on messages 6 and 7, the Decisions entry on Review): left as
  dated records, on the user's word.
- The tree names no feature in flight (the user, 2026-10-07): a feature
  of its own.
- A design run's opening fixes no shape for its copy of the terms
  (`opening.md`); DESIGN CONFIRM wrote that copy again at step 9, and
  the session wrote it as the list. The flow's sentence is a later
  fix.
- The interview's `SKILL.md` reads `$1` as the second word under this
  harness; the session parsed the id from its own arguments.
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
