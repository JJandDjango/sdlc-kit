# Session 162 plan: measure which of 0.18.0's deferred advisories a consumer meets

**Project:** sdlc_development_kit, a spec-first SDLC kit shipped as a Claude Code plugin: gates, task contracts and the agents that build to them.
**Area:** the feature document: the interview that writes it, intake that reads it, and the pages that describe both.
**Feature:** feature-document (released as 0.18.0, PR #84), later split into two documents (0.19.0) and read by G1 (0.20.0 to 0.22.2).
**Unit:** none. This is a measure, not a build: it reads and writes no code.

## 1. The deliverable

Backlog Next 2 (`docs/backlog.md:455-496`) rewritten: each of its 27 advisories carries two readings, whether it still stands on main at `0c2f9f6` and whether a consumer met it, and one verdict (a unit, parked, or closed); a draft PR.

## 2. Where this sits

G1's open edges closed in session 161 (B6, PR #169). Next 2 is the first open Next. It says "a measure comes first: which of them a consumer meets", and the only measure so far, the user's 2026-10-05 feedback from a second machine, named none. Since then the engine (`E:/ImSimProject/engine`, the kit's first real consumer) ran the interview and intake on two features, `m0-window-vulkan-cleared-frame` and `subset-lint`, both halves, and kept notes in `PILOT-NOTES.md` and `.sdlc/findings/`. Several items may already be gone: 0.19.0 to 0.22.2 rewrote the interview's flows, and `MAP.md` left in the Cairn 2.0 migration.

## 3. The steps

1. Branch `session-162-advisories-measure` off main at `0c2f9f6`; this plan committed and pushed.
2. Stands: for each item, Grep the named step or page on main; record `stands`, `gone` or `changed`, with a `file:line`.
3. Met: for each item that stands, search the engine's record (its four feature documents, their state files, `PILOT-NOTES.md`, `.sdlc/findings/`, its git log) for the step or symptom; record `met` with a `file:line` or `not met`.
4. Verdict per item: `met` makes it a unit candidate; `stands` and `not met` parks it; `gone` closes it.
5. Rewrite Next 2 in the backlog with the table's result; `plan.md` out; push; a draft PR with the readings at the top.

## 4. Where Claude stops for the user

At the PR's review only. Otherwise only on a discovery that needs a decision.

## 5. Where Claude goes on alone, and by what rule

Every step: no approval stands before the PR review (`CONTRIBUTING.md`, Delegation). The measure writes only the backlog, and the backlog already says the measure comes first.

## 6. Rulings needed

None. Readings, each listed at the top of the PR body:

- "A consumer" means the engine and the 2026-10-05 feedback. `deadlock-mod` ran no interview (its contracts predate the feature document).
- "Met" means the engine's record shows the step ran on the path the item names, or shows the symptom. An item on a path the engine never took is `not met`, not unknown.
- No Two-Key run: Two-Key grades a unit, and this is no unit and changes no code.

## 7. What could go wrong, already ruled

- The engine's record is silent on a path it ran: the item reads `not met` and parks; the PR says the measure is one consumer deep.
- An item stands but its step was renamed: record `changed` with the new name, then measure it as `stands`.

## 8. This session's cost, with its basis

No agent tokens: this session has no subagent tool, so the main session sweeps by Grep with targeted reads, about two searches an item (27 items).

## 9. Not in this session

- Building any unit the measure names.
- The engine's newest finding `g1-unreachable-from-a-plain-request` (2026-11-12), unless the kit backlog lacks it, in which case it gets one line on the backlog.
- The other Next items.

## 10. Words

- **advisory**: a Two-Key finding that did not block the unit; it goes on the backlog.
- **Two-Key**: a unit is done only when independent verifiers, rerunning the tests, grade PASS.
- **consumer**: a repository other than the kit that installs it and runs its commands.
- **the interview**: the skill that writes a feature document one question at a time; its steps carry letter codes (P for the plan of a session, Q for a question, S for the design half, E for an edit, O for output).
- **intake**: `/sdlc intake`, which reads a signed feature document and writes the task contract; its steps are I1 to I5.
- **stands / gone / changed**: the item's text is still true on main / no longer true / true under a new name.
