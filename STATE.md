# State - sdlc_development_kit

> **Contract** - one question: *what is in flight right now?*
> <=1 page - regenerate at every session end - disposable, always safe to overwrite.
> _Generated 2026-07-31 (session 22 close)._

## Now
- Session 22 (2026-07-31): **the operator layer shipped its first
  slice** - the arc carried as "its own" since ADR 0017, designed
  and landed in one session. Contract `operator-layer` ready-green
  at intake first pass (F1-F9 ratified whole; personas-not-per-gate
  ruled in conversation). Shipped: plugin `agents/` with the
  Two-Key pair - sdlc-developer (G3 write surface, never reads
  acceptance-test source: the anti-gaming ruling ratified) and
  sdlc-verifier (zero-trust grader, no Edit/Write in its toolset) -
  docs/operators.md making the verdict contract (exit 0/1/2 +
  --json) and loop protocol (cap 5, no retry-to-green) normative,
  the 13-gate venue map (G4 = local preflight, CI authoritative and
  agentless), dotnet profile.json `commands:` bindings (g3 +
  g4-preflight), operator + verdict as draft terms, ADR 0021.
- Receipts: suite 146 -> 158; six contracts ready-green;
  vocab-green 15 terms; audit clean; suppression-audit main..HEAD
  green; kit 0.8.0. PR #21 merged (51a1b18), v0.8.0 tagged there;
  self-pin PR #22 merged (4bbd7aa), its contracts job proving
  `pip install @v0.8.0`. Carried one-liners fixed (README tree
  line, CONVENTIONS schema ref -> taskcontract/schemas/; empty
  root schemas/ removed).
- Prior close: #21 (0385242) - G4 mechanical core, 0.7.0.

## Blockers
- None.

## Next actions
1. Rule the draft terms: ratify or amend `operator` and `verdict`
   (class-S flip in review).
2. **Pilot M0 session** (engine repo): first profile-aware
   consumer - dotnet payload spans G3 + G4 core and now carries
   operators to exercise; Q5 reality data.
3. Registered continuations: sdlc-spec / sdlc-qa defs behind venue
   existence; PL-PIPE.3 eval harness (own arc); mechanical loop
   runner; verdict field-name convergence (rides the next
   pipeline-native module).
4. Deferrals unchanged: Q4 numbers, PyPI publish (trigger stands),
   explainer PDF, V8 RDF map; gaps behind triggers: Azure DevOps
   variant, Husky.NET, dotnet-tool wrapper, battery-CWE map.

## Open questions
- Q4 thresholds, numeric only (G4.8 ratchet budgets ride these).
- Q5 two-channel decorrelation - content half ruled (context
  manifests, ADR 0021); mechanism rides M0.
- Q6 first analyzer tranche - rides pilot activation.
- Operator activation in consumers: when does a consumer's
  `active_gates` reflect operator-driven G3/G4 preflight - M0
  should surface the shape.
