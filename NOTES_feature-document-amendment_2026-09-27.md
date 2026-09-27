# Feature document notes - what the solution half leaves open

_Session 57, 2026-09-27. Working notes, not a Cairn stratum. A proposal
to amend the format ADR 0029 ratified
(`NOTES_feature-document_2026-09-18.md`). Ratified by the user in
session 57, all six calls and the four ready checks as written; ADR 0033
follows. Source: a
post-mortem of project-tree's build, sessions 51 to 56, read from each
session's closed `plan.md`._

## Why

project-tree's document was ready at r3, and its build still asked the
user 43 decisions. 26 were process by design: plans, delegation, commits,
pushes, merges, the tag. Of the 17 about content, 12 answered questions
r3 could have settled, and the gaps cost three Two-Key FAILs (o4, o5 and
o7, each at round 1) and a drafter stopped past 400K tokens (o6). Every
gap sits below the line: the request half held.

The format tells the engineer seat what to decide (scope, interfaces,
units) but not three things every build asks: where each fact comes from
and which source wins, what each output looks like at its edges, and what
each unit takes away. None of the three is specific to the kit; a web
service, a screen or a CLI asks the same.

## The calls

Six. The first three add blocks to section 13; the next two sharpen blocks
it has; the last adds a step to the interview.

1. **Sources** (a new 13.4; Constraints, Units and Sequencing renumber to
   13.5 to 13.7). A table: each fact the feature shows, stores or acts
   on; the field, file or record it reads; and where two sources can
   disagree, which one wins and when. For example: "account status on the
   profile page: `users.status`; when billing records a suspension,
   billing wins until it lifts." Evidence: SC3.1 said a closed contract
   reads done and never said what wins against a later record or a gate
   verdict (o4's and o7's FAILs, a ruling each); session 53 ruled that a
   unit's plain name comes from its `done_means` and an approval's seat
   from `confirmed_by`.
2. **Examples** (13.3 Interfaces gains them). Each output drawn literally,
   one per kind (a line, a response body, a screen), then its edges: the
   smallest size it must fit, the empty case, a missing or unreadable
   input, and each error. A test may pin an example word for word.
   Evidence: with no line drawn, o2 moved the text before the status by
   ruling; the 0.15.0 pane then hid statuses until o5; o5's cut dropped
   the current-task marker below 72 columns (a FAIL); session 54's USAGE
   batch carried four readings the document never drew.
3. **Retirements** (a field on each unit in 13.6). What the unit removes,
   replaces or reverses: code, tests, user-facing text, and any earlier
   unit's test it flips; "none" when nothing. A unit that both adds
   behavior and retires old behavior splits in two. Evidence: nothing
   named the end of the 0.15.0 follow loop (session 54's ruling 2); o6's
   first drafter, carrying the new keys and that loop's 150 retired cases,
   passed 400K tokens and was split by ruling; o1's test pinning USAGE's
   marks red waited for o7 to flip it.
4. **Tests by check id** (13.6 changes). A unit lists its tests by check
   id and kind: automated, or a manual receipt a person gives, such as a
   live run. Never by file. Evidence: `tests/test_pane.py` and
   `tests/test_tree_view.py` went stale during the build, and o7 needed a
   ruling to take no test list; session 55's live run was ruled onto the
   plan, where a manual receipt under SC4 would have scheduled it.
5. **Order with its reason** (13.7 changes). Each ordering names why;
   "any order" only when no unit changes a shape another unit's tests
   pin. Evidence: "o2, o3 and o4 after o1, in any order"; o2 changes every
   line, so session 53 ruled it first.
6. **The checks, run before signing** (a step in the interview, at each
   seat). Before a seat signs its half, the interview runs on the draft
   each automated check that intake and the gates will run, and writes
   the result into the document: the terms through the vocabulary and
   language checks, Scope against the release unit's paths. A finding the
   seat cannot answer is an OPEN. Evidence: CL003 made the dictionary cede
   eight words at ratification; intake added `skills/sdlc/init.py` and
   `.github/workflows/sdlc.yml` to Scope (session 51).

## The definition of done

The ready checks gain four for the solution half, advisory in the
interview and hard at intake, as checks 1 to 8 are for the request half:

11. Every fact a check names has a Sources row, and every pair of sources
    that can disagree names its winner.
12. Every output kind has a drawn example, with its edges.
13. Every unit names its retirements or "none", and lists its tests by
    check id and kind.
14. The checks run before signing read green, or each finding stands
    answered in the document.

## Not proposed

- Unit confirmation at intake (G0.3) repeated the engineer seat's r3
  signature and added nothing. Letting that signature count changes ADR
  0025's seats, not the format; it joins STATE.md's open question on
  delegated approvals.
- The 26 process approvals stay: the house rules put plans, commits,
  pushes, merges and tags on the user's word.
- The tree-order candidate was never real: the document's own risk said
  the tree would read partial truth until the backfill landed. A deferred
  item that waits on a prerequisite is measured again once the
  prerequisite lands. A session rule, for STATE.md, not the format.

## Consequences

- ADR 0033 amends 0029 in its own text once the calls are ratified; ADRs
  are append-only (`DOCS-SYSTEM.md:45`).
- `feature-document` (its REQUEST, untracked) carries the change into the
  template, the interview's flow and the readiness check.
- The format keeps eighteen sections; 13 gains one subsection.
- The PO seat sees one change, call 6's run of the terms; the other five
  sit with the engineer seat.
