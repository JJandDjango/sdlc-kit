# Plan - Session 16 (2026-07-28) - EXECUTED

Implementation session for the ratified vocabulary layer (ADR 0017,
V1-V10). All ten steps ran to completion in seven commits
(5e47b87..2f7e11a + the close); suite 37 -> 85 green throughout, audit
clean, Two-Key consumer-path verification passed.

## This session (all done)

1. Plan refreshed and user-ratified.
2. V9 self-host: /sdlc init brownfield+python; audit clean (5e47b87).
3. V9 first contract: vocabulary-layer ready-green through this repo's
   own intake - G0.1 enforced-in-fact here (830fd3e).
4. V10 docs Pass 0: docs/vocabulary.md + USAGE section 5, red-marked
   before code (2395554).
5. Pass A glossary door: glossary-term schema v1, VT000-VT009, schemas
   relocated into the package - closed a live distribution gap (the
   wheel shipped no schemas; non-editable installs crashed) (6b927dd).
6. Pass B entities + G0.2 join: schema 1.1.0, TC010-012 + W001
   warning channel, sunset window semantics (ee86ad6).
7. Pass C vocab family: vocab-list / vocab-add / vocab-check CLI,
   SKILL.md flows + greenfield seed, extraction fixture live (10 real
   terms: 3 ratified, 7 draft), audit VOCAB-INVALID / CONTRACT-WARNED
   + vocabulary-dir orphan exemption (eed47fb).
8. Pass D constraint registry: born non-empty (5 entries incl. the
   live entities-coverage join), class E self-declared, VC000-003
   (c06bc7b).
9. Docs to green: gates.md G0.2 row, G0 deep page condition block +
   field-table row, enforced-in-fact recorded; verification battery
   (2f7e11a).
10. Close: MAP row, this plan, STATE regen, session commit.

Left for the user (out of contract scope, one-liners or a g9 intake):
README.md tree line, CONVENTIONS.md schema ref, .vscode/settings.json
raw URL - all still name the old root schemas/ path. Post-push: update
the /sdlc plugin (the cached copy predates this session). Ratify or
prune the 7 draft terms (class-S flips) at leisure.

Deferred unchanged: per-gate agent arc (0017's named neighbor); V8 RDF
projection map (trigger-gated); Q4 numbers incl. the sunset notice
floor; PyPI publish; explainer PDF into docs/.

House rules in force: no pipes/chains in any authored command string
(CI steps included); never Edit/Write under ~/.claude/skills (shell
copy only); /sdlc never touches Cairn strata in target repos.
