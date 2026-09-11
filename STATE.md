# State - sdlc_development_kit

> **Contract** - one question: *what is in flight right now?*
> <=1 page - regenerate at every session end - disposable, always safe to overwrite.
> _Generated 2026-09-10 (session 30 close, home machine)._

## Now
- v0.12.0 is closed: PR #37 (self-pin) merged as 673cc24 on 2026-09-09.
  Main is at 7824b7a after PR #38 (`session-28-g0-pitch`): the session-28
  notes ratified with five playbook amendments, ADR 0026 (the feature
  document is the raw request) and ADR 0027 (playbook crosswalk, four
  disagreements as alternatives, six closures in two contracts), the
  CONVENTIONS raw-request rule, plan.md and its diagram source. Seven
  merged local branches pruned; `session-17-*` and `session-18-close` keep
  live upstreams. No kit code changed this session.
- Session 30 (2026-09-08 to 2026-09-10) was documentation and direction.
  The session plan diagram was reshaped from actor swimlanes into a step
  spine (one lane of plan steps, human gates above, waits below); routing
  lessons live in project memory. plan.workflow.json beside plan.md is the
  diagram source; the HTML is generated, never committed. The close commit
  carries both files with steps 1-3 struck.
- Prototype venue decided: Google Docs, the consumer's own venue. The
  consumer's real template was mapped section by section; three additions
  ratified (a Seats line under the title, an Implementation section after
  Business Requirements carrying the engineer's three answers, a "Not in
  scope" line at the top of Requirements with the standing placeholder "No
  new authorizations are added", confirmed at every intake). The revision
  table is the linkage record: intake appends contract id, state, merge
  SHA. Skeleton: "TEMPLATE - Feature Document (intake-ready)" in the
  user's Drive; the mapping graduates to USAGE beside section 8 with the
  demo, using this template, not 0026's generic one.
- Receipts not re-run (no code changed): suite 222, validate 10/10, vocab
  18 terms, lang-check 0, prompt_lang 8/8 as of session 27. Cairn audit 0
  errors, 23 warnings: 21 pre-existing plus budget warnings on 0026 (64
  lines) and 0027 (71), the house pattern since 0012.
- Untracked REQUEST_unit-dag_2026-08-22.md stays untracked by kit rules.

## Blockers
- None. `/sdlc audit` here still reports TC005 on `id` and `confirmed_by`:
  the pip install is pinned at e81f9a5. Fix:
  `pip install -e E:\sdlc_development_kit`. Not a finding against the code.

## Next actions (plan.md step numbers)
1. **Step 4, the session-31 opener:** two decisions, then
   `/sdlc intake playbook-guardrails`. The diff-to-contract binding
   (recommended: a `Contract:` commit trailer, parsed like the Theory
   trailer) and gap 1 on class-E paths (recommended: no special case; the
   hook denies the spec channel and warns outside the bound contract's
   scope, tightening to deny in wave B). Units U1-U6 plus the amendment-2
   intake prompt (the playbook's three plan questions), one commit each,
   Two-Key, v0.13.0, self-pin. Present the plan first: `node
   ~/.claude/skills/archify/bin/archify.mjs deliver workflow
   plan.workflow.json <scratch>/plan.html --quality showcase --json`, then
   `Start-Process` the HTML.
2. Step 4b, proposed and unratified: `taskcontract graph` emits Archify
   beside its Mermaid, so a contract's picture is derived, never hand
   authored (ADR 0024's rule). Two units, its own small contract, before
   the demo.
3. Step 5: demo intake. The user copies the template for one feature (3-5
   success criteria, 2-3 Gherkin scenarios each); intake runs in a sandbox
   consumer, never the kit's own specs/; USAGE gains the section.
4. Step 6: `/sdlc intake playbook-loop` (V1-V5) after fixing the re-scan
   cadence and the metric set; v0.14.0.
5. Carried: work-side upgrade to v0.12.0 (id migration, vocab extract,
   seats); G1 slice (Gherkin as the authoring format); prompt lexicon arc;
   runner probe, M0 pilot, PL-PIPE.3 harness, other continuations unchanged.

## Open questions
- Promote "plans as Archify diagrams", now in the step-spine shape, to the
  global CLAUDE.md workflow preferences? Project memory holds it today.
- Ratify step 4b (the derived contract diagram) into the plan?
- Gap 4: which four metrics stay (time-to-ready, rework count, first-pass
  merge, in-scope rate proposed).
- Q4 thresholds, Q5 decorrelation, Q6 first analyzer tranche, PL-PIPE.3
  comprehension empirics: unchanged from 25.
