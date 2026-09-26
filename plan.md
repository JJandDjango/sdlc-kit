# Plan - Session 53 (2026-09-25) - project-tree o2, o3, o4

**Deliverable:** units `o2-titles`, `o3-stale` and `o4-statuses` of
`project-tree` on one PR, each with its own Two-Key PASS (one agent
re-runs every check, a second grades the commits against the contract, and
a script computes the verdict):

- o2: the contract schema gains an optional one-line `title` (1.4.0 to
  1.5.0); intake copies it from the feature document's title line; every
  item line opens on its id and its plain name, a feature without a title
  showing `(no title)`. o1's four Two-Key advisories ride here.
- o3: the tree reads each feature document's revision table; a feature
  line reads `stale: document rN, contract from rM`, `no feature
  document` or `no "Ready:" row`; intake writes the `Ready:` row in its
  fixed shape.
- o4: a blocked task names its reason and the approval that holds the
  current task names the seat it waits on, each on the item's own line.

**Rulings at plan review** (the user's):

1. Order o2, o3, o4: o2 changes every line's opening, so the later units'
   tests pin the new shape once.
2. Delegation as in session 52. The user approves the three units' USAGE
   subsections in one batch, shown in chat in full before any drafting;
   Claude approves each test list and commit on review. The push, the PR
   and the merge stay on the user's word.
3. o2's plain names: an item's name where its source gives one (a gate, a
   verdict, a condition and a task from the kit's lists; a feature from
   its `title`, else `(no title)`), and its source text where none does (a
   unit's `done_means`, a check's sketch line, a finding's statement).
   That text moves from the line's end to right after the id, so the
   `summary` part keeps only a feature's intent.
4. o4's seat: the unit's `confirmed_by`, the seats that answered for it
   at intake. Nothing else records a seat before the approval's answer,
   and a new contract field would need a re-intake.

**Closed.** The deliverable is met: o2 at `899b853`, o3 at `34c154d`, o4
at `83032bc` and its fix `155a76e`; Two-Key PASS for each (o4 at round 2).
Suite 710 passed, scope-check green. PR #62 carries the session; the
merge waits on the user's word.

## Steps

1. ~~Open.~~ Branch cut from `7567591`; the plan at `ba1504f`.
2. ~~USAGE, one batch.~~ Three subsections refined and o1's two USAGE
   advisories, shown in chat in full, at `a94c021` on the user's word.
3. ~~o2.~~ 21 tests and nine amended modules; Claude added
   `test_progress.py` at approval, after a full run on the prototype
   caught it. At `899b853`; suite 647 passed; Two-Key PASS at round 1
   with five advisories: the G0 page's `title` row needs "reads its
   words", and USAGE's condition query sentence still names `summary:`
   (both carried to o3); the test row pattern splits a plain name at its
   first ` [`; two notes need no action.
4. ~~o3.~~ 21 tests (39 cases) and five amended modules, drafted beside
   o2's Two-Key. At `34c154d`, with o2's two carried advisories; suite 686
   passed; Two-Key PASS at round 1 with three advisories, all for o7's
   sweep: USAGE's green "reads no document" paragraph and ADR 0031 line 43
   are stale, and USAGE does not state the tie-break or that an `rM`
   above the document's revision is a match.
5. ~~o4.~~ 13 tests (21 cases) and five amended tests, drafted beside
   o3's Two-Key. At `83032bc`; Two-Key FAIL at round 1: a closed contract
   read `doing`, `blocked` or `failed` through its verdicts, against
   done_means, which the USAGE text Claude wrote had narrowed. The user
   chose the contract's reading and approved the new USAGE sentence;
   Claude amended five tests red first and added one more for a closed
   contract the tree cannot read. The fix at `155a76e`; suite 710
   passed; Two-Key PASS at round 2 with three advisories for o7's sweep
   (three green 0.15.0 paragraphs in section 9; USAGE does not say a task
   reopened after a close shows through).
6. ~~Close.~~ PR #62; STATE.md regenerated; this plan struck.

Steps 1 and 6 sit outside a contract unit, so the pane does not show them.

Three units is three times session 52's load. If context runs high, the
session wraps after whichever unit closed last, and the rest moves to
session 54.

Known cost: once o2 lands, a unit's or check's line carries its text
before its status, so the 0.15.0 `--follow` pane, which cuts lines to its
width, can hide a unit's status until o5 replaces it.

Decisions this session: sixteen. The user's at plan review: rulings 1 to
4, and the USAGE batch in ruling 2 (5); the three USAGE subsections: yes
(6); o4's closed contract, the contract's reading and its USAGE sentence:
yes (7). Claude's, on review: the three test lists (8 to 10), with
`test_progress.py` added to o2's and the unreadable contract added to
o4's fix round; the four commits (11 to 14). The user's at the close:
(15) the push and the PR: yes; (16) the merge: open.

Deferred, not this session:
- o5 to o7 (o7 ships 0.16.0).
- G1, after project-tree ships.
- The rest of STATE.md's carried list, prerequisites 7 to 9 among it.

House rules in force: no pipes or chains in any authored command string;
commit messages via Write + `git commit -F`; Workflows launched by
`scriptPath`; a `Contract:` trailer, alone in the final paragraph, on every
commit that touches a non-free path; each task recorded through
`taskcontract progress`, each check's run through `progress run`; no
tracked file touched while a verifier runs; a surprise mid-build is an OPEN
(a question written back into the feature document) and a re-intake, never
a silent edit.
