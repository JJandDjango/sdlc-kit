# Plan - Session 76 (2026-10-06) - document-split, to a ready contract

**Deliverable:** `specs/document-split/contract.yaml` at ready, derived
by intake from `docs/features/document-split.md` under kit 0.18.0, with
ADR 0037 and the term commit before it.

The feature: the one feature document becomes two, a requirements
document the PO seat signs and a design document one engineer seat
writes and signs alone. Both halves stand signed at r7 (session 75, PR
#87 at `419f575`). The document's Prerequisites name two things that do
not exist yet, each the user's to ratify before intake: an ADR that
amends ADR 0029 and ADRs 0033 to 0036 for the pair, and the new terms in
their own commit.

Approvals: six points stay on the user's word. (1) This plan and its
commit; (2) ADR 0037's text and its commit; (3) the fourteen term texts
and their commit; (4) the seats' confirmations at intake, one batch; (5)
intake's commit; (6) the wrap's commit, the push, the PR and the merge.
The user holds both seats.

No code changes this session, so no Two-Key round. The receipts are
`vocab-check`, `lang-check`, `validate --profile ready`, the tree and
the whole suite.

The session boundary, if context runs short: after step 4. The ADR and
the terms stand committed, and intake opens the next session.

**Closed at the boundary.** The deliverable is not met: the session
ended after step 4 on the user's word, with step 5 done besides. PR #88
merged at `1b4173b` with this plan (`8773b04`), ADR 0037 (`bd38eb6`) and
the terms (`62cbe4a`: nine new, seven amended, the dictionary without
`pair`). The two amendments past the document's five, `ready-check` and
`drift-mark`, rest on ADR 0037. Step 5 found the document's Scope
covering the release unit, so no text row is needed. Steps 6 to 8, the
language door, intake and the receipts, open session 77.

Decisions this session: six replies, all the user's. (1) The deliverable
and the plan; (2) the plan's commit, its push and PR #88; (3) ADR 0037
as written; (4) the fourteen term texts and the two extra amendments;
(5) the push of the terms and the merge on CI green; (6) the session's
end at the boundary. Claude's, each told to the user: two reasons worded
in the ADR's Alternatives; the ADR's two bullets past the Notes' list
(the text revision, the tree); `open-mark` left as it is; the suite run
from a scratch venv, since no Python here holds `rich`; step 5 done
while the boundary question waited.

## Steps

1. ~~Open.~~ Branch `session-76-document-split` from `419f575`; this plan,
   committed on the user's word.
2. ~~Materials.~~ Read ADRs 0029 and 0033 to 0036, the document's
   Interfaces, Consult cases and Notes, and intake's flow
   (`skills/sdlc/flows/intake.md`). The installed plugin sits at
   `40eb767`; `git diff --stat v0.18.0 main -- skills/` prints nothing,
   so its flows are 0.18.0's.
3. ~~ADR 0037.~~ Draft `decisions/0037-*.md`. It amends 0029 and 0033 to
   0036 in its own text and carries what the document's Notes list: the
   two templates and each document's sections; each section's one-seat
   tag; the r1 rows and the status lines; ready check 8 for the PO seat
   alone and the new ready check 15; the named revision and its
   `Confirmed against requirements r{m}` row; one `Ready:` or `Parked:`
   row in each table; the three edge messages. Shown whole in chat for
   ratification, then its own commit.
4. ~~Terms.~~ Nine new term files and five amended ones under
   `specs/vocabulary/`, each definition copied from the document's Terms
   block; the dictionary cedes `pair` in the same commit. Read each
   amended term's neighbors for a definition the change contradicts;
   `seat-boundary` and `parked-document` stand as they are. `vocab-check`
   and the whole suite read green. Shown before and after in chat for
   ratification, then its own commit.
5. ~~Scope against the release unit.~~ Read the document's Scope against
   what `d6-release` needs: `skills/sdlc/init.py` (`KIT_VERSION`),
   `pyproject.toml`, `.github/workflows/sdlc.yml`, both skills'
   `SKILL.md`, and each file whose sentences the feature makes false. A
   gap is told to the user before intake: it takes a text row and a
   signature.
6. The language door, on a draft. A scratch script builds the lexicon
   with the terms now ratified and runs `check_contract` on a draft
   contract outside `specs/`. The draft check's 179 findings are
   rewritten there in the contract's wording until it reads zero. Each
   `done_means` is copied word for word from the Units table.
7. Intake. `/sdlc:sdlc intake docs/features/document-split.md` through
   the installed plugin: I1 the seat roster, I2 the document read (a
   stop or a park here writes nothing under `specs/`), I3 the scaffold,
   the seats' confirmations in one batch, I6 the write, I7 the loop to
   ready-green, and the `Ready:` row in the document. Then its own
   commit, with the `Contract:` trailer.
8. Receipts. `validate --profile ready` on the contract, `taskcontract
   tree` showing `document-split` with a ready contract, and the whole
   suite, each read from its output.
9. ~~Close.~~ `STATE.md` regenerated, this plan struck, the memory index
   updated, on branch `session-76-wrap`. The commit, the push, the PR
   and the merge wait on the user's word.

Deferred, not this session:
- The build, `d1-requirements` to `d6-release`, as kit 0.19.0.
- The interview's last step, W1: the Google Docs form, when one is
  wanted. The `google_workspace` server failed to connect this session.
- G1's design document, through a design run once 0.19.0 ships.
- Whether combined documents are in flight on the second machine: not
  known, and the design holds either way.
- `STATE.md` Next actions 2 to 5 and its open questions, carried.

House rules in force: no pipes or chains in any authored command string;
commit messages via Write + `git commit -F`; a `Contract:` trailer,
alone in the final paragraph, on every commit that touches a non-free
path; no spawn opens a window.
