# Plan - Session 13 (2026-07-26)

The specification program closed at 54/54 (S12); before activation, the
kit becomes distributable the way Cairn did: a `/sdlc` skill in this
repo, flipped public as `sdlc-kit`, installable by shell copy or plugin
marketplace, so the flow is install -> new repo -> `/cairn` (doc spine)
-> `/sdlc` (gate spine) on greenfield and brownfield targets alike.
This re-sequences activation: the delivery vehicle ships first, and
Q6's "pilot" becomes the first repo initialized via the skill. Going
public also dissolves the protect-main blocker (rulesets are free on
public repos; the ruleset JSON is already tracked). Ratified this
session: repo public + renamed `sdlc-kit`; consumer model = pip from
GitHub for the validator machinery plus Cairn-style marketplace/skill
distribution; v1 subcommands = init + new + intake + audit (F10 and
F11 ship inside the skill).

## This session

1. Refresh this plan (done - this file).
2. Pass 0, docs-first: ADR 0016 (distribution before activation - the
   program re-order, v1 scope, naming, consumer model, lifecycle
   stance: G0.1 stays `specified` kit-side, flips `enforced`
   per-target when intake runs live); skeleton README.md + USAGE.md
   with red status markers; MIT LICENSE.
3. Pass 1, engine before skill: `python -m taskcontract new <id>`
   (F11) - 8-field contract skeleton at specs/<id>/contract.yaml;
   tests (tmp-dir round-trip new -> fill -> validate green; id
   rejection).
4. Pass 2, the skill: skills/sdlc/SKILL.md (PromptLang, Cairn-style
   dispatch: no-arg init interview / new / intake / audit), init.py
   (zero-dep, no-clobber, {{var}} templates), templates/* (SDLC.md,
   .sdlc/config+clocks+reds, specs/README, workflow, F8 + F12
   snippets), audit.py (report-only, exit 0/1/2), tests;
   `python -m prompt_lang` clean on SKILL.md.
5. Pass 3, packaging + cascades: .claude-plugin/marketplace.json;
   README/USAGE completed (markers to green); MAP.md row;
   docs/task-contract.md F10/F11 deferred-line update.
6. Pass 4, install + smoke: shell-copy skills/sdlc ->
   ~/.claude/skills/sdlc; scratch greenfield run (init -> new ->
   validate --profile ready green -> audit 0); brownfield run
   (no-clobber proven, snippets printed).
7. Pass 5, publish: GitHub rename -> sdlc-kit + visibility -> public
   (live confirmation each), apply ruleset to main, push on explicit
   approval; STATE.md regen; commit-session (Theory trailers).

House rules in force: no pipes/chains in any authored command string
(CI steps included); never Edit/Write under ~/.claude/skills (shell
copy only); /sdlc never touches Cairn strata in target repos.
