# Plan - Session 66 (2026-09-30) - feature-document's solution half

**Deliverable:** `docs/features/feature-document.md`, its solution half
written through the interview at the engineer seat and signed, in the
format ADR 0029 ratified and ADRs 0033 to 0035 amended. The request half
stays as the PO seat signed it at r3 (r4). Intake is the next session's.

**Closed.** The deliverable is met: both halves signed at r8 (r9, r10).
The tree reads `no contract: document r8`, both halves done. The request
half changed twice on the way, each time re-signed: r5 (r6) and r8 (r9).

## Steps

1. ~~Open.~~ Branch `session-66-feature-document` from `40eb7b8`.
2. ~~The interview at the engineer seat.~~
   - Q10 Scope and Out of scope; a check's id sits at the end of its
     sketch line, not the head (r5); the `Parked:` OPEN answered: it
     changes no text.
   - Q11 Interfaces: `lang-check --draft` on the state file, `CL014`,
     the state file beside the document, the document from r1, the
     Gherkin block, the rows.
   - Q12 Sources, with SC2.1 and prerequisite 5 gaining `done_means`.
   - Q13 Constraints. Q14 Units, f1 to f5. Q15 Order. Q16 Risks and cost.
3. ~~The checks before signing.~~ Scope holds the release unit's paths;
   no clash; `check` and `tag` trip CL003; 177 request-half findings left
   to intake; 5 in `done_means` (r7).
4. ~~Ready checks 9 and 11 to 14.~~ Four fixes: three `done_means`
   rewritten (zero after), three Sources rows, `MAP.md:42` in f5,
   prerequisite 6 widened (r8).
5. ~~The seats sign.~~ r9 and r10 sign r8.
6. ~~Close.~~ `STATE.md` regenerated; this plan struck; the commit, push
   and PR on the user's word.

Decisions this session: fifteen, all the user's. (1) This plan; (2) to
(4) Q10: the id's place, the `Parked:` answer, Scope; (5) Q11; (6) Q12's
`done_means` finding and (7) Sources; (8) Q13; (9) Q14; (10) Q15 with
(11) f3's retirement, (12) Q16; (13) the r7 results, (14) the four
fixes, (15) the signatures. The commit, push and PR follow.

Deferred, not this session:
- Intake (session 67), then the build and the 0.18.0 release.
- G1's solution half by hand (risk 5), after 0.18.0, by the user's order.
- `STATE.md` Next actions 3 to 5 and its open questions, carried.

House rules in force: no pipes or chains in any authored command string;
commit messages via Write + `git commit -F`; the push, the PR and the
merge on the user's word.
