# Session 147 plan: G1 unreachable from a plain request, fixed and traced

**Project:** sdlc_development_kit, a spec-first SDLC kit shipped as a Claude Code plugin: gates, task contracts and the agents that build to them.
**Area:** G1, the gate between intake and the first unit's test list, where a feature's requirements and spec are checked before development starts.
**Feature:** g1-requirements-spec (contract `g1-requirements-spec`): G1's three conditions, its venue `/sdlc g1`, and the refusal that keeps a task from starting before G1 passes; units s1 to s6 on main since kit 0.20.0.
**Unit:** a new unit, `s7-plain-request`: intake stops a request with no feature document where G1 is active for the feature, before any contract exists.

## 1. The deliverable

One draft PR that closes the engine's finding `g1-unreachable-from-a-plain-request`: a post-mortem of how it passed every check, the signed requirements and design rows, the re-intake, and `s7-plain-request` built with a Two-Key PASS.

## 2. Where this sits

The engine (`E:\ImSimProject\engine`, kit pinned at `v0.22.0`) filed the finding on 2026-11-12. Confirmed in the kit at `ff03c0a`:

- Intake reads a feature document only when the request is one (`skills/sdlc/flows/intake.md:17`). Its report then names G1 whenever G1 is active and the feature is not exempt (`:40`).
- G1.3's review needs the document. `derived_from` raises when there is none (`taskcontract/g1.py:636`), so `g1-record review` exits 2 (`:1101`) and G1.3 reads `to do` forever (`:701`).
- `progress start` refuses every task while G1 has not passed (design, The refusal). A contract made from a plain request, with G1 active, is green at G0 and can never be built.
- The kit holds a second case: `glossary-alias-disjointness` has a contract, no feature document, and stays off `g1.exempt` by shape call 9 (design `:428`). `g1-check` reads it `G1.3 to do` today.

The user ruled this the repository's top priority (session 147) and asked how it was missed. It was already on the backlog as one of G1.3's unnamed cases (PR #112's reading 3, kept in session 93), priced before the refusal existed; it is now the first edge of the backlog's Next 26, G1's open edges. Next 26's other edges keep their place.

## 3. The steps

Where it stands at session 147's close (the 200K mark): steps 1 to 3 done; step 4 drafted, with requirements r10 and design r12 written, ADR 0041 proposed, and the checks before signing not yet run. The next session opens on those checks (the two `Measured:` rows, `lang-check --draft` and ready checks 1 to 8 and 11 to 15), then step 5. Design r12 moved the fix from I2 into `new` (its Decisions say why), so the plan's I2 wording below is superseded there.

1. Stay on `session-146-g1-edges` (one commit past main's `7ee90c8`); this plan committed and pushed.
2. Backlog: the finding joins Next 26 as its first edge, and Open questions' G1 entries gain it with its second case.
3. Post-mortem. Trace the bug past each check that could have stopped it, from its record: the requirements (SC4.1's scenario, consult case 1), the design (shape call 9, the Review term, the Sources row), the checks before signing (design r2 and r8), `s3-review`'s and `s5-start`'s test lists and Two-Key receipts, `s5-start`'s manual receipt, the 0.20.0 release, and the tree's reading of `glossary-alias-disjointness` since then. For each: what the check read, and why the case fell outside it. Written to `NOTES_g1-plain-request-post-mortem_2026-11-12.md`; the escape charged in `docs/session-metrics.md`. A process change it points to goes to the user as a proposed ADR, drafted only on their yes.
4. The amendment, drafted:
   - Requirements row (PO seat): SC4 gains SC4.4 with its scenario, "intake stops a request with no feature document where G1 is active for the feature, before any contract exists, and names both ways out"; the ruling on `glossary-alias-disjointness`.
   - Design row (engineer seat): the sentence at I2 and its message; whether `g1-check` names a missing document (today a silent `to do`); the unit `s7-plain-request` in Units and Order; the test floor (one test runs `g1-record review` on a contract from a plain request); the retirements (`tests/test_g1_intake.py:118-120` and `:168-169`, which pin G1 and the config file to I9 alone); room under intake's 12,000-character ceiling.
   - The checks before signing, each recorded as a `Measured:` row.
5. Stop: the user signs both rows, and rules on any ADR the post-mortem proposes.
6. Re-intake: `/sdlc intake docs/features/g1-requirements-spec.md` adds the unit and writes the `Ready:` rows.
7. Build `s7-plain-request` through `/sdlc execute`: write-tests to two-key, with the readings in section 6 given as pins and rulings.
8. Close: `progress done`, the backlog's edge closed, a row in `docs/session-metrics.md`, `plan.md` out, push, a draft PR with the readings and the post-mortem's findings at its top.

## 4. Where Claude stops for the user

At step 5 (two seat signatures, and an ADR only on a yes), at step 7's test list (the tripwire, section 5) and at the PR's review. Otherwise only on a case the signed documents leave open, or a discovery that needs a decision; a third failed round is one.

## 5. Where Claude goes on alone, and by what rule

Steps 1 to 4 and 6 to 8: no approval stands before the PR review (`CONTRIBUTING.md`, Delegation). Seat signatures are the user's. The test list is the user's until the user rules otherwise: this escape traces to `s5-start`'s test list, which Claude approved, so the tripwire in `docs/session-metrics.md` fired. Step 7 shows the list in chat and records it `--by user`.

## 6. Rulings needed

Two, both carried by the signatures at step 5:

- `glossary-alias-disjointness`: recommend it stays off `g1.exempt` and its backlog line says it needs a pair (a requirements and a design document) before it unparks. Exempting it would skip a review it has not had.
- A silent `to do`: recommend `g1-check` and the tree name the missing document for a contract that has none. Intake's stop prevents new cases; the message makes the old ones visible, which is how the kit's own case went unseen.

Readings from the documents' purpose, listed at the top of the PR:

- The check sits at I2, after the id is derived, not at I1: the exempt list is read by id.
- G1.3 stays as it is: its 11 items read a document, so the fix stops the path rather than loosening the review (the finding's own call).
- `g1-requirements-spec` is on `g1.exempt` (`.sdlc/config.yaml:18`), so no G1 review gates its own build; Next 26's "a re-intake reopens G1.3" binds only a feature G1 gates.
- The engine's stuck contract is the engine's to clear, in its own session.

## 7. What could go wrong, already ruled

- Intake stands at 11,833 of its 12,000 characters. The design row names what it trims; the ceiling stays, since PromptLang fails at 4,000 tokens.
- The post-mortem reads many records. Each is read by section and by `Grep`, never whole; past 40% of this session's window, the session splits at step 5 with a handoff file in `RECEIPT_g1-requirements-spec-s7_2026-11-12/`.
- The new prose fails the controlled-register check: the suite holds the `lang` tests, and a fix round is narrow.
- Older tests pin I9's words and the config file's one mention: the test-retirer amends them.

## 8. This session's cost, with its basis

About 0.2M to 0.3M tokens in this session for steps 2 to 4: targeted reads of about ten records, and two drafted rows. About 0.7M to 1.0M agent tokens for the team at one round: rs4 ran 634K, rs1 to rs3 about 1.0M each (`docs/session-metrics.md`). Each failed round adds one member run, about 100K to 200K.

## 9. Not in this session

- Next 26's other edges: the readings of PRs #116 and #119, the hand-written files, G1.3's seven unnamed cases, G1.2's three, G1.1's four, the three smaller ones and the `s4-tree` folds.
- The engine's contract made from a plain request.
- G2.

## 10. Words

- **G1**: the gate a feature passes before development starts; active for a feature when `G1` is under `active_gates` in `.sdlc/config.yaml` and the feature is not on `g1.exempt`.
- **G1.3**: G1's third condition, a person's review of 11 items on the feature's documents, recorded by `g1-record review`.
- **intake**: `/sdlc intake`, the G0 venue: a request in, a ready contract out.
- **plain request**: a request typed to intake with no feature document behind it.
- **feature document**: a requirements document (`docs/features/{id}.md`, the PO seat's half), with its design document beside it (`{id}.design.md`, the engineer seat's half); together, a pair.
- **seat**: a role that signs a document's half: the PO seat or the engineer seat.
- **text row, `Measured:` row, `Ready:` row**: rows of a document's revision table: a change to its text; the checks run before signing; intake's record that the contract was derived from a signed revision.
- **re-intake**: intake run again on a changed pair, so the contract follows the documents.
- **exempt list**: `g1.exempt`, the features G1 does not gate.
- **escape**: a defect that passed a gate green.
- **post-mortem**: a trace of how a defect passed each check, with the evidence.
- **Two-Key**: a unit is done only when an independent verifier, rerunning the tests, grades PASS.
- **execution team**: the agents `/sdlc execute` starts to build one unit: QA, the QA verifier, the Developer and the Dev verifier.
- **test-retirer**: an agent that finds and amends the older tests a change makes false.
