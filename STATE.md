# State - sdlc_development_kit

> **Contract** - one question: *what is in flight right now?*
> <=1 page - regenerate at every session end - disposable, always safe to overwrite.
> _Generated 2026-09-08 (session 29 close, home machine)._

## Now
- v0.12.0 is released (tag and origin/main at 8fbaa7f). PR #37 (self-pin,
  `session-27-self-pin`) is OPEN and mergeable, both checks green at cc29aa5
  (2026-09-08 13:53 UTC). The session-28 "cc29aa5 never pushed" line was
  stale: the push landed before session 29. Only the merge remains.
- Session 29 (2026-09-08) was the direction check, no kit code. Branch
  `session-28-g0-pitch` (e7af41e pushed, no PR) gains plan.md (rewritten)
  and plan.workflow.json (new) in the session-close commit. The opener
  YouTube review held the session-28 mapping. Anthropic's AI-Native SDLC
  playbook (claude.com/blog/the-ai-native-sdlc-playbook, Claxton,
  2026-08-21) was fetched and mapped play by play against the 56
  conditions: every play covered, mostly stronger. Six gaps ratified for
  implementation: (1) hooks denying writes to ready contracts and ratified
  terms; (2) a G4 diff-within-contract-scope condition; (3) a G9 scheduled
  re-scan of unchanged code; (4) flow metrics; (5) a PO venue without an
  engineer at the prompt; (6) an advisory review pass named in USAGE, and
  escapes adding agent evals. Plan: two contracts, `playbook-guardrails`
  (1, 2, 6a; kit 0.13.0, before the pitch) and `playbook-loop` (3, 4, 5,
  6b; 0.14.0, after the demo intake).
- Standing rule from this session: every plan is presented as an Archify
  diagram (skill installed globally, `~/.claude/skills/archify`).
  plan.workflow.json beside plan.md is the diagram source; HTML is
  generated, never committed.
- Session-28 notes still unratified. Five amendments recommended after the
  video and the playbook: a terms crosswalk to intent.md / spec.md /
  plan.md; the playbook's three plan questions as intake prompts; "linkage
  as the minimum bar" named; rework count as a clock; the playbook's four
  disagreements (mutable plan, advisory templates, committed plan,
  co-generated tests) as the ADR's alternatives.
- Receipts not re-run (no code changed): suite 222, validate 10/10, vocab
  18 terms, lang-check 0, prompt_lang 8/8 as of session 27. Cairn audit 0
  errors, 21 warnings, all pre-existing (ADR budgets, 0024 edited after
  creation, four docs pages stale since the 2026-08-26 `confirmed_by`
  stamp).
- Untracked REQUEST_unit-dag_2026-08-22.md stays untracked by kit rules.

## Blockers
- None. `/sdlc audit` here still reports TC005 on `id` and `confirmed_by`:
  the pip install is pinned at e81f9a5. Fix:
  `pip install -e E:\sdlc_development_kit`. Not a finding against the code.

## Next actions (plan.md step numbers)
1. **Step 2, the session-30 opener:** ratify NOTES_g0-pitch with the five
   amendments; write ADR 0026 (the feature document is the raw request)
   and ADR 0027 (playbook crosswalk, four disagreements, six closures).
   Present the plan first: `node ~/.claude/skills/archify/bin/archify.mjs
   deliver workflow plan.workflow.json <scratch>/plan.html --quality
   showcase --json`, then `Start-Process` the HTML.
2. Step 3: merge PR #37 on the user's word, sync main, delete
   `session-27-self-pin`, prune the five gone local branches; PR
   `session-28-g0-pitch` carrying notes + ADRs + plan, merge on green.
3. Step 4: `/sdlc intake playbook-guardrails`, after deciding the
   diff-to-contract binding (recommend a `Contract:` commit trailer). Units
   U1-U7, one commit each, Two-Key, v0.13.0, self-pin.
4. Step 5: demo intake, one real feature document, in a sandbox consumer.
5. Step 6: `/sdlc intake playbook-loop` after fixing the re-scan cadence
   and the final metric set; V1-V6, v0.14.0.
6. Carried: work-side upgrade to v0.12.0 (id migration, vocab extract,
   seats); G1 slice (Gherkin as the authoring format); prompt lexicon arc;
   runner probe, M0 pilot, PL-PIPE.3 harness, other continuations unchanged.

## Open questions
- Promote "plans as Archify diagrams" to the global CLAUDE.md workflow
  preferences? Project memory holds it today.
- Gap 1 for class-E paths: deny outright in wave A, or warn now and require
  the PL-PIPE.1 approval record later?
- Gap 4: which four metrics stay (time-to-ready, rework count, first-pass
  merge, in-scope rate proposed).
- Q4 thresholds, Q5 decorrelation, Q6 first analyzer tranche, PL-PIPE.3
  comprehension empirics: unchanged from 25.
