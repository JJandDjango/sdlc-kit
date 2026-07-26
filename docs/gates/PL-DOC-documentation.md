# PL-DOC - Documentation lifecycle (cross-cutting)

<!-- covers: HANDOFF_gate-architecture_2026-07-22.md -->

> **Contract** - one question: *what must the Documentation lifecycle
> contain, and why?*
> Deep page per [0004](../../decisions/0004-per-gate-documentation-program.md);
> registry row: [gates.md](../gates.md). Source: handoff section 5 PL
> rows; the G7.2 contract-diff payloads ([G7
> page](G7-release-deploy.md)); the 0013 deprecation dossiers ([G10
> page](G10-retirement.md)); ADRs
> [0012](../../decisions/0012-stop-the-line-economy.md),
> [0014](../../decisions/0014-enforcement-change-control.md),
> [0015](../../decisions/0015-program-close-out.md).
> Two-layer per [0008](../../decisions/0008-two-layer-condition-model.md).

## Identity

- **Venue:** no venue of its own (frame ruling) - the merge arm rides
  G4-time CI (samples via the ordinary solution build, coverage via
  the committed compiler config + the docs build); the sweep arm
  rides G9's scheduled infrastructure (staleness).
- **Cadence:** per merge + the sweep's clocks.yaml cadence.
- **Inputs:** the doc set + its front-matter (`reviewed:` /
  `covers:`); the declared public surface (API baselines, the G7.2
  shipped set); the compiled samples project; git facts; clocks.yaml;
  the generated-doc payloads (G7.2 contract-diffs, 0013 dossier
  records).
- **Object:** injected context - the doc set is the agents' ground
  truth at generation time. Staleness is a defect *vector*, not a
  cosmetic issue.
- **FAIL blocks:** any merge breaking a sample (including API merges -
  charged to the causing change); undocumented new public surface
  (surfaced at the inner loop); doc-touching merges without current
  dates; past-window staleness = standing red (0012); drift-stale
  docs excluded from context assembly.
- **Trust boundary:** fully mechanical - no principal. QA owns the
  doc-set config, sample-relaxation ruleset, and dating config as
  class E (PL-PIPE). Prose quality is named residue: human,
  oracle-problem family ([0015](../../decisions/0015-program-close-out.md)).

## Why this gate exists

For agent pipelines documentation is injected context: a stale doc
does not mislead a reader, it *generates wrong code at scale* - the
agent consumes it as ground truth. So the doc set gets the same
two-front defense as the dependency graph (the diff/world division's
third instance, after G4.9/G9): a merge arm charging drift to the
change that causes it, and a sweep arm catching what time does to
the unchanged set. Pace-layering structures the sweep - fast layers
get short windows, slow layers get change control instead of
age-out - and the boundary with PL-PIPE is the frame's line: *a
prompt instructs, a doc informs*; anything decision-bearing is
enforcement config and moves layers.

Classes closed: documentation staleness / context rot (ODC
documentation - the taxonomy's one previously-unused anchor).

## Conditions

Per [0008](../../decisions/0008-two-layer-condition-model.md): **Shape**
is normative and ecosystem-free; **Reference binding** is the .NET
profile. Object default: the doc set plus the declared public
surface.

### PL-DOC.1 Doc samples compile/execute

- **Shape (pass condition):** every declared sample resolves and
  compiles; run-class samples execute. Clauses:
  1. **Inclusion over inline** (the ladder move) - samples live in a
     compiled samples project inside the solution; docs include them
     by region reference and the doc build inlines the source. An
     included sample cannot rot - it is code, built every merge; the
     check degrades to reference resolution, dangling = FAIL. Inline
     fenced blocks are the declared fallback for fragments:
     extracted, template-wrapped, compiled by the harness.
  2. **Two sample classes** - `compile` (default: compiles against
     the current shipped surface) and `run` (declared: additionally
     executes clean, output optionally pinned as an approval
     snapshot - catalog pattern 5). Opt-out is explicit: a fenced
     block in a compile-set language is a sample unless marked;
     unmarked non-compiling prose-in-a-fence = FAIL.
  3. **Strict config, deprecation reach** - samples compile under
     the committed strict config (G3.3's) with a committed
     sample-relaxation ruleset (class E); deprecation diagnostics
     are never relaxed, so G10.1's escalation reaches docs: a doc
     teaching a sunset API warns in the notice window and reads red
     at the date. "Docs teaching the dead API" becomes mechanically
     impossible.
  4. **Venue: every merge** - the samples project rides the ordinary
     solution build (G4.1/G4.11, zero new machinery); an
     API-breaking merge that breaks a sample blocks, charged to the
     change that caused it, never discovered by a later sweep.
  5. **Polarity** - subject absence is green (prose-only docs are
     legitimate; no minimum-sample floor - samples are optional
     content, unlike G4.11's tests). Structural failures are red:
     dangling reference, extraction/parse failure, compile failure,
     non-running run-class sample. Generated docs draw samples only
     from the compiled inclusion set, never freehand template text.
- **Reference binding (.NET):** samples `.csproj` in-solution;
  region-include mechanism (DocFX code-link / mdsnippets family);
  extraction harness for inline blocks; `dotnet run` for run-class;
  Verify-family output pins.
- **Gap status:** samples project + extraction harness ride pilot
  activation (Q6).
- **Why:** a sample is a promise that the shown code still works;
  inclusion makes the promise structural instead of aspirational.
- **Kind & loopability:** mechanical; diagnostic = reference/site +
  failure kind; loop consumers are the doc-touching or API-touching
  task that broke it.
- **Parameters:** none numeric; the relaxation ruleset is class E.
- **Lifecycle:** `specified` (ratified 2026-07-26).

### PL-DOC.2 Doc coverage

- **Shape (pass condition):** the declared public surface of the
  shipped set is fully documented. Clauses:
  1. **Borrowed denominator** - coverage spans the declared public
     surface of the shipped package set: the same artifacts G4.5
     diffs and G7.2 baselines. Never an independent reflection scan;
     internal/private surface is out of scope by definition
     (one-artifact-many-consumers).
  2. **Covered = structurally complete** - non-empty summary; every
     parameter, return, and declared exception documented; every
     cref resolves (dangling = red); the docs-site build runs clean.
     Prose *quality* is deliberately not gated - named residue
     (oracle-problem family, THEORY non-goal): presence and
     structure are mechanical, goodness stays human and
     cheap-to-review like specs.
  3. **Teeth in the strict config** - `GenerateDocumentationFile` +
     CS1591 and the missing-param family at error severity in the
     committed props (class E): missing docs surface at G3.3 in
     seconds, echo at G4.1, and undocumented *new* surface cannot
     merge. The condition proper owns the policy, the cref/docs-build
     job, and the baseline mechanics.
  4. **Absolute at greenfield, ratcheted at brownfield** - the shape
     is zero undocumented members; brownfield adoption enters via a
     captured shrink-only baseline of legacy gaps (G4.8 discipline,
     G9.4-managed). Declared-baseline-missing = FAIL.
  5. **Merge arm only** - coverage moves only when surface moves
     (surface and docs travel in the same diff); the scheduled arm
     belongs wholly to PL-DOC.3. Existence-per-release of generated
     subjects is G7.2/0013 record completeness, not coverage.
- **Reference binding (.NET):** CS1591 + CS1573-family via
  `Directory.Build.props`; DocFX-family build with
  warnings-as-errors and cref resolution; coverage report scoped by
  the shipped set; brownfield baseline file.
- **Gap status:** docs-build job rides pilot activation (Q6).
- **Why:** undocumented surface is context the next agent cannot
  have - the coverage floor is what keeps the injected-context layer
  total over the API it describes.
- **Kind & loopability:** mechanical; diagnostic = member + missing
  element; loop consumer is the surface-introducing task.
- **Parameters:** none numeric.
- **Lifecycle:** `specified` (ratified 2026-07-26).

### PL-DOC.3 Staleness dating

- **Shape (pass condition):** every doc subject is dated and within
  its freshness bounds. Clauses:
  1. **Two staleness notions** - *drift*: a doc declares what it
     covers (`covers:` front-matter, the registry-header precedent
     generalized) and is stale the moment any covered subject
     changed after its `reviewed:` date - subject side from git
     facts, doc side from the authored date. *Age*: stale past a
     per-layer window even with unchanged subjects. Dating is
     authored, never inferred - git mtime never substitutes (a typo
     fix must not launder freshness). Missing date = red; dangling
     covers-target = red.
  2. **Pace layers structure the thresholds** - the doc-set config
     (class E) assigns each doc a layer: fast layers get short age
     windows; slow layers (THEORY-class, rarely-edited-by-design)
     get change control instead of age-out, drift checks still
     applying. A doc with no covers-anchor takes the fast-layer
     window - undetectable drift shortens the leash. Windows live in
     clocks.yaml (0012; numbers Q4). This repo's Cairn spine is the
     worked instance: STATE generated-fresh per session, THEORY
     slow-layer.
  3. **Thin merge arm** - a doc-touching diff must carry a current
     `reviewed:` date on every touched doc: substantive edits cannot
     forget the date, and the date cannot go stale silently on an
     actively-edited doc.
  4. **Sweep, ledger, escalation** - the scheduled sweep (G9
     infrastructure) emits the *staleness ledger*: subject, layer,
     dates, drift/age verdicts; external-link rot folds in as age
     evidence. Findings open remediation windows in the 0012 aging
     family; past-window entries escalate to standing reds with the
     standard three arms. A sweep past its clocks.yaml cadence reads
     red - a dead sweep is a gutted gate, not a quiet week.
  5. **The consumption coupling is the point** - context assembly
     consumes the same ledger (one-artifact-many-consumers):
     drift-stale docs are *excluded* from agent context by default -
     injecting known-wrong context is worse than injecting none -
     includable only by explicit recorded waiver; age-stale docs
     inject carrying a staleness annotation the agent sees.
     Generated docs (STATE, release notes, dossiers) are exempt from
     review-dating: their date is the generation date, their
     freshness is the generating job's liveness.
- **Reference binding (.NET / repo-level):** front-matter check over
  git facts; sweep job on the G9 scheduled infrastructure; the
  staleness ledger artifact; context-assembly hook in the harness.
- **Gap status:** sweep + ledger + context-assembly hook ride pilot
  activation (Q6).
- **Why:** the doc set is the one artifact whose consumers cannot
  tell fresh from stale by looking - the date and the covers-binding
  are what make staleness a decidable fact instead of a discovered
  surprise.
- **Kind & loopability:** mechanical; diagnostic = subject + verdict
  + dates; loop consumers are review/refresh tasks.
- **Parameters:** age windows per layer, remediation window, sweep
  cadence - clocks.yaml rows (Q4).
- **Lifecycle:** `specified` (ratified 2026-07-26).

## Completeness check

Gate purpose: keep injected context true; the check asks what
staleness escapes three conditions. Examined:

- **Generated-doc coherence** (release notes <- G7.2 payloads,
  dossiers <- 0013 records) - a derivation, same family as slo.yaml:
  routed to PL-PIPE.2 as golden-test subjects, not a condition.
- **Conceptual adequacy / prose quality** - not mechanically
  decidable; named residue (human, oracle-problem family, 0015).
- **Link rot** - folded into the sweep's age evidence; no fourth
  condition.
- **Minimum-sample floor** - struck; subject absence is green.
- **Roster verdict:** complete at three - zero adopted, two routes,
  one fold-in; fully mechanical (census unchanged).

## Operators & harness

Fully mechanical, unattended. QA owns the class-E config set
(doc-set config, sample-relaxation ruleset, dating config); the
Developer meets PL-DOC as inner-loop diagnostics (CS1591, sample
breaks) and as staleness-driven refresh tasks; the staleness ledger
decides what context assembly may inject. Nobody grades anything.

## Decisions & open items

- All three conditions `specified` 2026-07-26 (session-12 walk).
- Frame rulings applied: the diff/world division's third instance;
  the prompt-instructs / doc-informs boundary (decision-bearing docs
  are class E under PL-PIPE); pace-layering with the Cairn spine as
  worked instance.
- Taxonomy row added: documentation staleness / context rot (ODC
  documentation).
- Q4 gains three clocks.yaml rows: age windows per layer,
  remediation window, sweep cadence.
- Build items riding Q6: samples project + extraction harness,
  docs-build job, staleness sweep + ledger + context-assembly hook,
  the doc-set config set (class E).
