# Session 179 plan: the requirements document for session-loop-sidebar

**Project:** sdlc_development_kit, a spec-first SDLC kit shipped as a Claude Code plugin: gates, task contracts and the agents that build to them.
**Area:** the session loop as the user watches it: the herdr panes and the sidebar beside them.
**Feature:** session-loop-sidebar (new): herdr's sidebar shows each loop's position, strike count and waiting state. Split from session-loop's SC6 (requirements decision 6, session 164).
**Unit:** none. This is the interview: it writes only the requirements document and its state file.

## 1. The deliverable

`docs/features/session-loop-sidebar.md`, the requirements document, written by `/sdlc:product-specification-interview session-loop-sidebar` through its request half and signed by the PO seat; its state file beside it; a draft PR.

## 2. Where this sits

session-loop shipped as kit 0.23.0 (PR #184 at `adbb07f`; self-pin PR #185 merged, main at `4a13216`). A loop's state is spread across places the user cannot see at a glance: `loop.json` (on), `waiting.json` (a stop waits, with its issue and due time), the launcher's memory (the last position and the strike count) and the launcher's own pane output. The interview's material at O5, each confirmed by the PO seat there:

- What the loop already knows: on or off; the position (`plan step N, task T` from the sentinel); the strike count (held only in the launcher's memory); a waiting stop (`waiting.json`: issue, due); the launcher's stop and its reason.
- What herdr offers (memory, measured on 0.9.1): `herdr pane report-metadata <pane> --source ID --token name=value` shows as `$name` in `[ui.sidebar.agents] rows`; `report-agent --state blocked` never changes a Claude pane; toasts by `herdr notification show`.
- ADR 0031 and ADR 0043: the kit's core runs no herdr command; herdr code lives in the opt-in `herdr/` folder.

## 3. The steps

1. Branch `session-179-loop-sidebar-requirements` off main at `4a13216`; this plan committed and pushed.
2. Opening O1 to O6: id, origin, title, PO seat, the material above; r1 written.
3. Request half, one question at a time, then Terms and the Gherkin.
4. The checks; the PO seat signs.
5. Output W1 and W2.
6. `plan.md` out; push; a draft PR naming the design run's command; backlog Next 31 marked.

## 4. Where Claude stops for the user

At every interview question (the PO seat's answers are the document) and at the PR's review.

## 5. Where Claude goes on alone, and by what rule

The branch, commits, pushes and the draft PR: no approval stands before the PR review (`CONTRIBUTING.md`, Delegation).

## 6. Rulings needed

None beyond the interview's own questions.

## 7. What could go wrong, already ruled

- The interview outlasts the context: wrap at a natural stop past about 20%; the state file resumes at the exact step.
- A mechanism nobody has measured (whether a `$token` row shows on a Claude pane's sidebar entry, how a token is cleared) goes in as an open question for the design run to test, not a trial in this session.

## 8. This session's cost, with its basis

No agent tokens: the interview runs in the main session, one question a turn (session 163 and 164's run of session-loop: about 25 questions over two sessions).

## 9. Not in this session

- The design run (`/sdlc:product-specification-interview session-loop-sidebar design`), intake and any build.
- The launcher's advisories carried from l2 and l3; the flaky `test_sc4_3_a_source_change_renders_within_two_seconds`.

## 10. Words

- **loop**: on while `loop.json` sits in `{git folder}/sdlc-loop/`; a launcher in another pane restarts the session after each wrap.
- **launcher**: `herdr/herdr_loop.py`, the process that restarts a loop's pane and stops the loop.
- **position**: where a session ended (`plan step N, task T`), written in the wrap's sentinel.
- **strike**: a session that ends at the position it started from; two in a row stop the loop.
- **waiting state**: a human-needed stop is open (`waiting.json` exists) until the user replies or the 55-minute timer wraps the session.
- **sidebar**: herdr's list of panes beside the workspace; a row can show tokens a process reports.
- **PO seat**: the person who owns and signs the request half of a feature document.
