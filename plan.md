# Plan - Session 75 (2026-10-06) - document-split, the solution half

**Deliverable:** the solution half of `docs/features/document-split.md`,
written through the interview's steps S1 to S11, checked by E1 to E5,
and signed by the engineer seat at E7.

The feature: the one feature document becomes two, a requirements
document the PO seat signs and a design document one engineer seat
writes and signs alone. Its request half is signed at r4 (session 74,
PR #86 at `5553193`). The format change is permanent; the one-time part,
splitting an existing combined document, is a non-goal (G1's is split by
hand). This document is the last one written combined.

Approvals: this plan, each batch of proposed text, the signature, each
commit, the push, the PR and the merge stay on the user's word. The
user holds both seats (`seats.po: user`, `seats.engineer: user`).

**Closed.** The deliverable is met: the document stands at r7, `Signed:
solution half. The engineer seat signs r6`, with six units, 32 Sources
rows, ten constraints and no OPEN. The state file reads `phase: output`,
`next: W1`. The draft check's 179 findings are left to intake's rewrite;
the six `done_means` read clean.

## Steps

1. ~~Open.~~ Branch `session-75-document-split` from `5553193`; the plan
   at `58ec2bf`.
2. ~~Materials.~~ The request half, the interview's flows and template,
   intake's flow and `feature-document.md`'s solution half read in the
   session; four read-only explorers mapped the change sites, the
   pinning tests and the release paths (610K tokens, 11 minutes). The
   flows ran from `skills/` here, which equals the `v0.18.0` tag.
3. ~~S1 Scope and S2 Out of scope.~~ One batch, led by three shape
   calls: the pair's paths, two state files, the `design` argument. No
   refusal was a thing not built, so the request half stayed as signed.
4. ~~S3 Interfaces.~~ One batch, thirteen calls folded in. Three
   behaviors the request half gives no words for became edges; the tree
   gained a drift mark for a design no check asks for; G1's document
   was found to hold no solution half.
5. ~~S4 Sources and S5 Constraints.~~ One batch: 31 rows, ten
   constraints, no new `taskcontract` command.
6. ~~S6 Units and S7 Order.~~ One batch: six units, `d1-requirements`
   to `d6-release`, one at a time; `d6` takes SC4.3; kit 0.19.0.
7. ~~S8 to S11.~~ One batch. The document's four "not yet decided"
   lines are answered; the fact on combined documents on the second
   machine was not given, and is recorded as not known.
8. ~~E1 to E5.~~ The draft check found 197, 18 on the six `done_means`;
   six rewordings, one Sources row (ready check 11) and one drawn
   `Parked:` row (ready check 12) closed every gap before the
   `Measured:` row, r5: 179 findings, Scope covered, 0 OPEN.
9. ~~E6 and E7.~~ r6 the finishing row, r7 the signature; the Gherkin
   stamp moved to r6.
10. ~~Close.~~ `STATE.md` regenerated, this plan struck. The commit, the
    push, the PR and the merge wait on the user's word.

Decisions this session: nine, all the user's. (1) The deliverable; (2)
the plan and its commit; (3) the three shape calls with Scope and Out of
scope; (4) Interfaces, with its thirteen calls; (5) Sources and
Constraints; (6) the six units, their order and 0.19.0; (7) Risks and
cost, the decisions, the links and the notes; (8) the six rewordings and
the two additions before the `Measured:` row; (9) the signature.
Claude's, each told to the user: the four explorers for the materials;
"An OPEN" reworded to "an open mark" in one Decisions line, so intake
does not park on it; the unanswered fact recorded as not known after one
probe.

Deferred, not this session:
- The ADR, 0037, that amends 0029 and 0033 to 0036; the nine terms and
  five amendments, ratified in their own commit; intake under kit
  0.18.0, with the draft check's 179 findings rewritten there; the
  build, `d1` to `d6`, as kit 0.19.0.
- The interview's last step, W1: the Google Docs form, when one is
  wanted.
- G1's design document, through a design run once 0.19.0 ships.
- `STATE.md` Next actions 2 to 5 and its open questions, carried.

House rules in force: no pipes or chains in any authored command string;
commit messages via Write + `git commit -F`; a `Contract:` trailer,
alone in the final paragraph, on every commit that touches a non-free
path; no spawn opens a window.
