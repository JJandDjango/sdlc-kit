# Plan - Session 40 (2026-09-22) - tree-view t3 and t2

**Deliverable:** two units of `tree-view` (the request for one derived tree
of the work) on one PR, each with a Two-Key PASS (one agent re-runs every
check, a second grades the commit against the contract, and a script
computes the verdict), t3 first because t4, t5 and t7 wait on it alone:

- t3 `t3-status-and-cursor`: every item shows one of the six statuses, a
  parent reads `done` only when every item under it does, each `G0`
  verdict reads from the validator and names its command and `HEAD` id,
  and the current task derives from the progress files, whose format
  lands here.
- t2 `t2-summaries-and-links`: each item shows its source field unchanged,
  links name their kind and come only from `depends_on` or a finding's
  `gate`, and a feature doc shows only as a file reference.

**Who does what.** The user delegated this session's in-work approvals to
Claude, on review. A subagent does each unit's work through the Workflow
tool (this session has no Agent tool): a spec-channel agent writes the
tests and proves red, and a developer agent makes them green without
opening `tests/` (ADR 0031: tests and red are the spec channel's, green
the developer's). The push, the PR and the merge stay on the user's word.

## Diagram

The plan's diagram source is `plan.workflow.json` beside this file (Archify
workflow, step spine: the steps read left to right, approvals dropping onto
it from above, an exception lane below for a Two-Key FAIL or an OPEN).
Render and open:

    node C:/Users/hyden/.claude/skills/archify/bin/archify.mjs deliver workflow plan.workflow.json <scratch>/plan.html --quality showcase --json
    Start-Process <scratch>/plan.html

The HTML is generated, never committed.

## Steps

1. Open: branch `session-40-tree-view-t3-t2` from main (it carries
   `50b691b`, session 39's STATE fix), and this plan.
2. t3, draft and approve the test list, with the progress file's format
   and the print's new words.
3. t3, write the tests and prove red.
4. t3, green.
5. t3, approve the commit and commit.
6. t3 Two-Key.
7. t2, draft and approve the test list.
8. t2, write the tests and prove red.
9. t2, green.
10. t2, approve the commit and commit.
11. t2 Two-Key.
12. Close: STATE.md regenerated and this plan struck through; push and PR
    on the user's word; merge on the user's word.

Decisions this session: seven. Claude's on review: (1) this plan, (2) t3's
test list, (3) t3's commit, (4) t2's test list, (5) t2's commit. The
user's: (6) the push and the PR, (7) the merge.

Deferred, not this session:
- `tree-view` t4 to t9, then the release (0.15.0); the herdr plugin outside
  the kit.
- For t6: t1's id collision, where a sketch naming `(commit)`, or a unit
  named like an active gate, repeats an id the query needs unique.
- For t9: t0's two wording notes (the line after the `progress run` block
  lacks its red mark; "about fifteen lines" against t7's "at most 15"), and
  t1's note that a `.yml` finding is not read.
- G1: the pilot's M0 code waits on its criteria review.
- `no-check-reads-the-source-document`: which request carries it.
- `derived-language`, `feature-document`, `spec-doc-type`; the demo intake
  in a sandbox consumer; wave B (`playbook-loop`, V1-V6); 5b; the G4.6
  finding.
- From r3: a status field on the finding form; the agent personas writing
  progress.

House rules in force: no pipes or chains in any authored command string;
commit messages via Write + `git commit -F`; Two-Key on every code unit,
launched by `scriptPath`; a `Contract:` trailer, alone in the final
paragraph, on every commit that touches a non-free path; receipts run
before each verifier round, and no tracked file touched while it runs; a
surprise mid-build is an OPEN and a re-intake, never a silent edit.
