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

**Closed.** The deliverable is met: t3 at `ff3fbfb` and t2 at `5bd596a`,
each a Two-Key PASS at round 1. The PR carrying them opens and merges on
the user's word.

Where things stand: suite 375 green (317 before; t3 added 39 cases, t2
19), the 14 contracts ready-green, the vocabulary, language and scope
checks clean. The kit's own tree prints 1052 lines, each ending in its
item's summary; every task reads `to do` until t4 and t5 ship the
progress writers.

**Who did what.** The user delegated this session's in-work approvals to
Claude, on review. Subagents did each unit's work through the Workflow
tool: a spec-channel agent drafted the test list and its interface,
proved it red from the scratchpad and built a scratch prototype to show
the interface could be met; a developer agent made the tests green
without opening `tests/`. Claude reviewed and approved each list and
each commit, placed the approved tests, and ran the receipts before each
verifier round.

## Diagram

The plan's diagram source is `plan.workflow.json` beside this file (Archify
workflow, step spine: the steps read left to right, approvals dropping onto
it from above, an exception lane below for a Two-Key FAIL or an OPEN).
Render and open:

    node C:/Users/hyden/.claude/skills/archify/bin/archify.mjs deliver workflow plan.workflow.json <scratch>/plan.html --quality showcase --json
    Start-Process <scratch>/plan.html

The HTML is generated, never committed.

## Steps

1. ~~Open.~~ Done at `48a96ae`: branch `session-40-tree-view-t3-t2` from
   main (carrying `50b691b`), and this plan.
2. ~~t3, draft and approve the test list.~~ 25 tests (39 cases), approved
   as drafted. Its one question, answered: a close never covers a
   verdict, since SC7.3 lets `G0` read done only at ready-green.
3. ~~t3, write the tests and prove red.~~ 39 failed, 317 passed, each on
   an assertion.
4. ~~t3, green.~~ `taskcontract/progress.py` (new), `tree.py`,
   `tree_view.py`; 356 passed.
5. ~~t3, approve the commit and commit.~~ Done at `ff3fbfb`.
6. ~~t3 Two-Key.~~ PASS at round 1, about 193K tokens. Three advisories,
   one fixed in t2, two deferred to t4.
7. ~~t2, draft and approve the test list.~~ 19 tests, approved with one
   change: the two imports moved to the file's top block. Its one
   question, answered: the line's new words go into USAGE at t9.
8. ~~t2, write the tests and prove red.~~ 19 failed, 356 passed.
9. ~~t2, green.~~ `tree.py` and `tree_view.py`; 375 passed.
10. ~~t2, approve the commit and commit.~~ Done at `5bd596a`.
11. ~~t2 Two-Key.~~ PASS at round 1, about 182K tokens. Three advisories,
    deferred to t6 and t9.
12. ~~Close.~~ STATE.md regenerated and this plan struck through; push
    and PR on the user's word; merge on the user's word.

Decisions this session: seven. Claude's on review: (1) this plan: yes;
(2) t3's test list: yes; (3) t3's commit: yes; (4) t2's test list: yes,
with the import change; (5) t2's commit: yes. The user's: (6) the push
and the PR: pending; (7) the merge: pending.

Details the request left open, fixed with the test lists: a verdict
counts toward failed, blocked and done but never starts its contract, so
a ready-green contract with no progress reads `to do`; a close never
covers a verdict; a gate item reads `to do`; a record counts only in its
own contract's file and where its kind fits; a tie on its time goes to
the later record, then the later contract; with no `to do` task in the
latest contract, no task is current; a verdict's summary is its gate's
name; `gates/none` has no summary; a field's ends are stripped and each
line break prints as one space; a blank field has no summary; a dangling
`depends_on` entry still prints its link.

Deferred, not this session:
- `tree-view` t4, t5, t6 and t7 (all unblocked now), t8 after t7, t9 last,
  releasing 0.15.0; the herdr plugin outside the kit.
- For t4: name the evidence keys (`head`, `by`, `reason`, `command`,
  `dirty`) in `progress.py`'s docstring as their first writer lands; mark
  a `G0` verdict's evidence dirty when its contract file differs from
  `HEAD`, since the validator reads the working tree.
- For t6: t1's id collision (a sketch naming `(commit)`, or a unit named
  like an active gate); a `depends_on` list that repeats an entry prints
  the link twice; `tree_view.py`'s docstring says each part follows one
  space, but the summary follows ` | `.
- For t9: t0's two wording notes (the line after the `progress run` block
  lacks its red mark; "about fifteen lines" against t7's "at most 15");
  t1's note that a `.yml` finding is not read; USAGE's backfill sentence
  holds only for a ready-green contract with no other active gate; USAGE
  documents the line's words (marks, evidence, links, the doc reference,
  ` | ` and the summary) and the text rule behind "unchanged".
- Later: a summary holding a character the console's encoding lacks could
  fail a print piped on Windows; every current contract and finding is
  ASCII.
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
