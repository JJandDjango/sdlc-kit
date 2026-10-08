# Plan - Session 86 (2026-10-08) - G1's terms and ADR 0038

**Deliverable:** ADR 0038 and the terms of
`docs/features/g1-requirements-spec.md` at r6 on main through one PR:
14 terms ratified, three ratified terms amended, and `component` and
`venue` ceded by the dictionary.

This is the first half of step 3 toward G1's intake. The second half,
`/sdlc intake docs/features/g1-requirements-spec.md`, is the next
session's, as sessions 76 and 77 split document-split.

Claude's readings, each told to the user here:

- Two commits, in session 76's order: ADR 0038 first, then the terms,
  since the three amendments rest on the ADR. Neither carries a
  `Contract:` trailer: both are spec channel, and the contract these
  terms serve does not exist yet.
- The 14 terms take their definitions word for word from r6's Terms
  block (`docs/features/g1-requirements-spec.md:409`). Claude proposes
  each term's `kind`.
- The three amended definitions stand in no signed text. The design
  names only their reason: Rule and Condition, for rules that read
  records; Active gate, for a feature's exemption. Claude proposes the
  words, and the user ratifies them.
- ADR 0038 holds three decisions, each from the signed design: the
  refusal amends ADR 0031's "shown and never enforced"
  (`decisions/0031-the-work-is-one-derived-tree.md:53`); a gate is
  active by feature; the records stand under `.sdlc/g1/`, and the
  declarations in `specs/components.yaml` and the `g1` key of
  `.sdlc/config.yaml`, which closes the deferrals of ADR 0007 and of
  G1's page.
- The neighbor read covers the 76 ratified terms against the three
  amendments and ADR 0038. A definition the ADR makes false is amended
  in the term commit, on the user's word.
- The signed pair stays as it is. The design's Decisions entry counts
  Review among four terms to amend: a dated record, on the user's word
  of session 85.
- No Workflow is planned, so the cost in agent tokens is none (session
  76's two commits ran none either).

The session boundary, if context runs short: after step 5, where ADR
0038 stands committed and the terms wait.

## Steps

1. Open. Branch `session-86-g1-terms` from `dfab2c6`; this plan,
   committed on the user's word.
2. Measure, in the session, with no agent:
   - the design's sentences ADR 0038 rests on: the refusal, the
     exemption, the homes of the records and the declarations;
   - what ADR 0007 and `docs/gates/G1-requirements-spec.md` defer;
   - the neighbors of Rule, Condition and Active gate among the 76
     terms, and every ratified definition ADR 0038 would make false;
   - every tracked file that quotes one of the three definitions, or
     counts the terms or the dictionary's words;
   - CL003 for each of the 14 names and slugs against the dictionary.
3. Batch 1, ADR 0038: its decisions, one line each, with the full text
   on request.
4. Write ADR 0038 and its line in the decisions index.
5. Commit 1, on the user's word: ADR 0038.
6. Batch 2, the terms: the three amended definitions before and after,
   any neighbor amendment, the 14 kinds, and the two ceded words. The 14
   definitions are r6's, shown on request.
7. Write the 14 term files, the amendments and the dictionary edit.
8. The checks: `vocab-check`, `lang-check`, `validate` on every
   contract, then the whole suite. Any test the terms break is named to
   the user before it changes.
9. Commit 2, on the user's word: the terms. Then the suite at the clean
   commit and `scope-check --base dfab2c6`.
10. Close. `STATE.md` regenerated, this plan struck, the memory index
    updated; the push, the PR and the merge on the user's word, after CI
    reads green.

Decisions this session: five planned, all the user's. (1) This plan and
its commit; (2) batch 1, ADR 0038; (3) batch 2, the terms; (4) the two
commits, the push and the PR; (5) the merge.

Deferred, not this session:
- `/sdlc intake docs/features/g1-requirements-spec.md`, with about 91
  language findings to rewrite in the contract's wording. USAGE's
  drawing of G1 as a feature before intake retires there.
- The build, `s1-lint` first, which opens with pass zero.
- The engine's install ref, its pilot config line and M0's code: after
  G1 ships.
- The `google_workspace` server failed to connect again at this resume.
- `STATE.md` Next actions 2 to 5 and its open questions, carried.

House rules in force: no pipes or chains in any authored command
string; commit messages via Write + `git commit -F`; Workflows launched
by `scriptPath`; a `Contract:` trailer, alone in the final paragraph, on
every commit that touches a bound path; no tracked file touched while
an agent runs; never two whole suites at once; no spawn opens a window.
