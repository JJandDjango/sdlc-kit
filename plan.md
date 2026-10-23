Project  SDLC kit: gates that stop agent-written code from degrading a codebase.
Area     The kit's own flow: how a session in this repo is sized, started and closed.
Feature  small-session-flow: each stage of the flow runs as a node at its own agent model and effort; this deliverable trims what a session loads.
Unit     None: backlog Next 13, trim what sessions load (the user, session 117). Session 118.

1. The deliverable. By this session's end `MEMORY.md` holds one short hook per entry, and `USAGE.md` is a short index whose pages sit under `docs/usage/`, on the branch `session-118-usage-split`, with its PR open for the user's review.
2. Where this sits. `MEMORY.md` (the memory index, outside the repo) loads every session at about 4.5K tokens; each entry links a topic file that holds the detail. `USAGE.md` runs 2,193 lines (about 27K tokens) in ten numbered sections; section 4 (860 lines) and section 9 (944 lines) are most of it. Six test files read it, and `docs/gates.md` with one page a gate is the shape to follow.
3. The steps (six). (1) Claude pushes this plan. (2) `MEMORY.md`: a script checks that each entry's facts (shas, PR numbers, versions, session numbers) stand in its topic file and lists any that do not; Claude moves those into the topic file, then cuts each entry to a hook of about 100 characters. (3) A script splits `USAGE.md` at fixed line ranges into the 14 pages below, fixes the 19 relative links for the new folder depth, and writes the index; it asserts that the pages joined in index order equal the old text from section 1 on, links and the `---` rules between pages aside. (4) The six test files read USAGE as the index plus its pages joined in order: one helper each. Claude runs them. (5) `README.md:38` links the install page; `ARCHITECTURE.md:47` names `docs/usage/`; the Cairn audit runs clean. (6) The close: commit with `Contract: small-session-flow`, tick Next 13, Next 14 goes first, `plan.md` out, a draft PR, ready after green CI.
4. Where Claude stops for the user. The PR review and its merge. A stop earlier only if a test pins text that cannot move without changing a signed sentence.
5. Where Claude goes on alone, and by what rule. Steps 1 to 6. The rule (`CONTRIBUTING.md:19`): no approval before the final PR review; the backlog entry is the user's ask, and a reading it leaves open is ruled from its purpose (a reader loads only the feature at hand) and listed at the top of the PR body.
6. Rulings needed: none. Readings: (a) The pages, one a section, with sections 4 and 9 split at their subsections, each run of subsections kept whole so the joined pages read as USAGE did:

   | § | Page | Old lines |
   |---|---|---|
   | 1-3 | `install.md`: when to run it, install, `/sdlc` | 19-99 |
   | 4 | `feature-document.md`: the interview | 102-476 |
   | 4 | `intake.md`: `/sdlc intake`, what `ready` requires | 477-530 |
   | 4 | `g1.md`: `/sdlc g1` | 531-835 |
   | 4 | `contract-tools.md`: `new`, `audit`, the session hook, `scope-check`, `REVIEW.md` | 836-909 |
   | 4 | `node.md`: `taskcontract node` | 910-961 |
   | 5 | `vocabulary.md` | 964-1001 |
   | 6 | `worked-example.md` | 1004-1021 |
   | 7 | `restricted-environments.md` | 1024-1065 |
   | 8 | `intake-seats.md` | 1068-1234 |
   | 9 | `the-tree.md`: what it holds, statuses, modes, tasks, recording, notify | 1237-1521 |
   | 9 | `the-pane.md`: the pane's lines, conditions, names, drift, blocked, the interactive pane | 1522-1885 |
   | 9 | `documents-on-the-tree.md`: roll-up, before intake, revisions, parked, pair, G1 active | 1886-2178 |
   | 10 | `troubleshooting.md` | 2181-2193 |

   (b) Text moves verbatim: each page opens on its old heading, and a "§8" reference stays; the index's § column resolves it. (c) "USAGE" now names the index and its pages, so the ratified `release-unit` term ("USAGE marks"), the done contracts' "`USAGE.md` reads green throughout", `tasks.yaml`'s `page: USAGE.md` and the consumer `NOTICE.md` link stay true, and no signed text changes; the ADRs keep their "USAGE §N" references. (d) No Two-Key round: no shipped code changes, and the tests change only how they read USAGE. The check is step 3's assertion, the six test files and CI's full suite. (e) `MEMORY.md` lives outside the repo, so it takes no commit. (f) No session-metrics row: no unit ships.
7. What could go wrong, already ruled. A test compares a paragraph that holds a moved link: its expectation takes the new prefix, nothing else. A heading inside a code fence read as a boundary: the line ranges come from a fence-aware outline. A topic file lacks a fact its index entry held: step 2 moves the fact before the cut.
8. This session's cost, with its basis. No agent runs, so about 0 agent tokens. The six test files run in a few minutes; CI runs the whole suite (about 460 s). The session's own context is the cost: about 60K at this plan, and the split is one script, so the close should land near 150K.
9. Not in this session. Turning "§N" references into links. Pointing each task in `tasks.yaml` at its own page (shipped data). Next 14, the faster suite. A CHANGELOG entry: it waits for a release.
10. Words. Index: the new `USAGE.md`, a table of pages. Page: one file under `docs/usage/`. § column: the index column that keeps each page's old section number. Hook: the text after the dash on a `MEMORY.md` line. Topic file: the memory file a `MEMORY.md` line links. Two-Key: the grade of a unit by an agent that re-runs its receipts on its own.
