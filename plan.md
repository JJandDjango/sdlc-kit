# Plan - Session 39 (2026-09-21) - tree-view t0 and t1

**Deliverable:** two units of `tree-view` (the request for one derived tree
of the work) on one PR, each with a Two-Key PASS (one agent re-runs every
check, a second grades the commit against the contract, and a script
computes the verdict):

- t0 `t0-usage-pass-zero`: the USAGE section on `taskcontract tree` and
  `taskcontract progress`, written before any code, every part marked red
  until the release.
- t1 `t1-tree-shape`: `taskcontract tree` prints the gates with their
  findings, and each contract with its gate verdicts, units, seven tasks
  and checks; it writes no file.

**Closed.** The deliverable is met: t0 at `73c4987` and t1 at `c6f1222`,
each a Two-Key PASS at round 1. The PR carrying them opens and merges on
your word.

Where things stand: suite 317 green (299 before, 18 new), the 14 contracts
ready-green (ready-green: they pass the validator's strict profile), the
vocabulary, language and scope checks clean. The kit's own tree prints
1,053 lines; the pilot's files each of its 16 findings once. Every status
reads `to do` until t3 derives them.

## Diagram

The plan's diagram source is `plan.workflow.json` beside this file (Archify
workflow, step spine: the steps read left to right, human gates dropping onto
it from above, an exception lane below for a Two-Key FAIL or an OPEN).
Render and open:

    node C:/Users/hyden/.claude/skills/archify/bin/archify.mjs deliver workflow plan.workflow.json <scratch>/plan.html --quality showcase --json
    Start-Process <scratch>/plan.html

The HTML is generated, never committed.

## Steps

1. ~~Open.~~ Done at `9c2fbe4`, with this plan.
2. ~~t0, the page first.~~ Done at `73c4987`: USAGE section 9, "Following
   the work", every part red; Troubleshooting moved to section 10. Two
   details the request left open were fixed there and approved with it: an
   unnamed check is `sketch-<n>` by position from 1, and an inactive gate
   prints only when a finding names it.
3. ~~t0 Two-Key.~~ PASS at round 1, about 145K tokens. Three advisories:
   two wording notes go to t9, and the third (t1 and t6 must meet the two
   fixed details) is held by t1's tests 4 and 8.
4. ~~t1, approve the test list.~~ Eighteen tests, approved as listed.
5. ~~t1, write the tests and prove red.~~ 18 failed, 299 passed.
6. ~~t1, green.~~ `taskcontract/tree.py`, `tree_view.py`, `data/gates.yaml`,
   `data/tasks.yaml`, the `tree` subcommand with `--root`; 317 passed.
7. ~~t1, approve the commit and commit.~~ Done at `c6f1222`.
8. ~~t1 Two-Key.~~ PASS at round 1, about 167K tokens. Two advisories, both
   deferred below.
9. ~~Close.~~ STATE.md regenerated and this plan struck through; push and
   PR on your word; merge on your word.

Decisions this session: six. (1) this plan: yes; (2) t0's section and
commit: yes; (3) t1's test list: yes; (4) t1's commit: yes; (5) the push
and the PR: pending; (6) the merge: pending.

Deferred, not this session:
- `tree-view` t2 to t9, then the release (0.15.0); the herdr plugin outside
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
commit messages via Write + `git commit -F`; Two-Key on every code unit; a
`Contract:` trailer, alone in the final paragraph, on every commit that
touches a non-free path; uncontested decisions batched in one message,
contested ones one per message, each with a recommendation; approval
content shown in chat in full.
