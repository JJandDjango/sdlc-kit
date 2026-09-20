# State - sdlc_development_kit

> **Contract** - one question: *what is in flight right now?*
> <=1 page - regenerate at every session end - disposable, always safe to overwrite.
> _Generated 2026-09-20 (session 32 closed, session 33 open, home machine)._

## Now
- Kit 0.13.0 is released (2026-09-18): PR #40 at a0a9010 (the interview
  skill, ADR 0028), PR #41 at 210d476 with tag `v0.13.0` (wave A,
  `playbook-guardrails`), the self-pin PR #42 at f6fb265, PR #43 at 5e26c1b,
  main's tip. One lesson: `gh pr merge --delete-branch` closes a stacked PR
  instead of retargeting it; restore the base ref, reopen, retarget, delete.
- Session 32 (2026-09-18) ratified the feature document's format and its
  definition of done: `NOTES_feature-document_2026-09-18.md`, ADR 0029;
  `NOTES_*.md` is a free path (`.sdlc/config.yaml`). The Google Docs look was
  settled with the user over seven renders and lives in the prototype
  `REQUEST_styled-rendering_2026-09-18.prototype.py` (Markdown to .docx; the
  google_workspace import reads only `~/.workspace-mcp/attachments`).
- The first spec doc exists outside the kit: ImSim Engine's
  `docs/feature-map.md`, written by hand in 0029's format (signed r3 on
  2026-09-19, r5 since). Reviewed from here as sufficient, three fixes
  suggested (the `subset-lint` horizon, homes for two renderer decisions,
  SC2's measurement run).
- Inbox, untracked by the kit rules, four unprocessed requests in 0029's
  format: `feature-document` (09-18, the kit's own, both halves),
  `spec-doc-type` (09-19), `derived-language` (09-19), `g0-declaration`
  (09-20); the last three are the engine's, request half only. Order agreed
  2026-09-20: g0-declaration, derived-language, feature-document,
  spec-doc-type.
- Amendments queued for ADR 0029 and the note, one commit when the look is
  final: state lives in revision rows (no status line); the Statement has no
  heading; the revision table has three columns with rN leading Changes Made;
  owner tags leave the format (user ruling 2026-09-18, rule 6); a spec doc is
  ready and then living, never closed.
- Receipts as of 2026-09-18: suite 282, scope-check green, twelve contracts
  ready-green, lang-check 0. Not re-run since.

## Blockers
- None. The stale pip install persists (`sdlc-taskcontract` 0.10.0,
  non-editable); `pip install -e E:\sdlc_development_kit` on the user's word.
  `python -m` from the repo root shadows it.

## Next actions (plan.md step numbers)
1. `g0-declaration`: G0.2's `entities` and G0.3's seat roster become required
   declarations at ready (a consumer proved both doors pass green on
   absence). The engineer half, intake under ADR 0014's lane, units, Two-Key,
   release. Until `derived-language` lands, contract sketches stay verb-first
   with the check id trailing.
2. `derived-language`: the language door binds derived text only; a check id
   at the head of a sketch survives the verb-first rule (its SC3); a contract
   names its source document.
3. `feature-document`: units F1-F6 implement 0029, with the queued amendments
   folded in first.
4. `spec-doc-type`, cut from the engine's feature map; amends 0028's non-goal.
5. Carried: the demo intake in a sandbox consumer; wave B (`playbook-loop`,
   V1-V6); step 5b (graph emits Archify), unratified; the work-side upgrade;
   the G1 slice; the prompt lexicon arc.

## Open questions
- The engine's second finding, `write-guard-binds-to-an-editing-tool-list`
  (G4.6: the guard binds Edit and Write, shell writes pass), has no request
  yet. A held-back request for a plain-language gates layer waits on the
  engine's `docs/gates-explained.md`.
- Ratify step 5b? Promote "plans as Archify" to the global CLAUDE.md? Render
  the hook command per stack (`python` or `python3`)? The four metrics for
  wave B. Q4 thresholds, Q5 decorrelation, Q6 first analyzer tranche,
  PL-PIPE.3 empirics: unchanged.
