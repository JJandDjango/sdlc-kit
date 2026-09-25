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

## Steps

1. Open. Branch `session-53-project-tree-o2-o4` from `7567591`; commit
   this plan.
2. USAGE, one batch: "Plain names and titles" (o2, with o1's two USAGE
   advisories), "Drift from the feature document" (o3), "Blocked and
   waiting, named" (o4), each refined, shown in chat in full, committed on
   the user's word.
3. o2: test list drafted and approved; tests placed, red; green; commit;
   Two-Key; o2 closed.
4. o3: the same six tasks; o3 closed. Its drafter may run beside o2's
   Two-Key, since it writes only the scratchpad.
5. o4: the same six tasks; o4 closed.
6. Close. PR; STATE.md regenerated; this plan struck.

Steps 1 and 6 sit outside a contract unit, so the pane does not show them.

Three units is three times session 52's load. If context runs high, the
session wraps after whichever unit closed last, and the rest moves to
session 54.

Known cost: once o2 lands, a unit's or check's line carries its text
before its status, so the 0.15.0 `--follow` pane, which cuts lines to its
width, can hide a unit's status until o5 replaces it.

Decisions this session so far: five. The user's at plan review: rulings 1
to 4, and the USAGE batch in ruling 2.

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
