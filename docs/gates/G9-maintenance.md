# G9 - Maintenance / Evolution

<!-- covers: HANDOFF_gate-architecture_2026-07-22.md -->

> **Contract** - one question: *what must the Maintenance/Evolution gate
> contain, and why?*
> Deep page per [0004](../../decisions/0004-per-gate-documentation-program.md);
> registry row: [gates.md](../gates.md). Source: handoff section 5 row 9;
> the G7 release records + G7.5 SBOM ([G7 page](G7-release-deploy.md));
> the G8.3 ladder statistics ([G8 page](G8-operations.md)); ADRs
> [0010](../../decisions/0010-write-surface-immutability.md),
> [0012](../../decisions/0012-stop-the-line-economy.md).
> Two-layer per [0008](../../decisions/0008-two-layer-condition-model.md).

## Identity

- **Venue:** scheduled jobs - the clock-driven venue, and the first
  gate that convenes on *time* rather than a change (frame ruling).
  Nothing is in flight when G9 runs; the world moved while the
  codebase sat still - advisories published against pinned packages,
  the ecosystem advanced, the pipeline's own baselines aged against
  its improved reality. Every change-triggered gate is blind to all
  of it.
- **Cadence:** weekly+ reference; every G9 clock (sweep cadences,
  windows, tightening cadences) lives in the clocks artifact
  ([0012](../../decisions/0012-stop-the-line-economy.md)).
- **Inputs:** advisory + EOL feeds; license metadata; the locked
  dependency closure; the G7.5 SBOM join (exposure classes); the
  pipeline's own records - G7.1 measurement records, G5 corpus
  state, G5.5 mutation scores, G8.3 ladder-assignment statistics.
- **Detection model:** standing invariants, sweep-detected (frame
  ruling - G8's standing-invariant frame transposed). G9.2/G9.3 hold
  continuously over the graph; the scheduled sweep is merely
  *detection*, because feeds are polled, never pushed. Liveness
  transposes to the clock: **a sweep past its declared cadence reads
  red** - a dead sweep is a gutted gate, not a quiet week.
- **FAIL blocks:** the diff/world division (frame ruling): G4.9 is
  the intake arm - what a *change* may introduce; G9 is the standing
  arm - what *time* introduced into the unchanged set. Same
  invariants, same sources, two venues. A breach opens a standing
  red in the 0012 economy: intake, merge, and admission arms engage
  uniformly, the fix lane (`fixes` field) keeps the remedy always
  admissible, and proportionality lives in window durations only.
- **Trust boundary:** fully mechanical - no maintenance principal
  (frame ruling; the human census stays six). The bot lane runs on a
  standing task contract - the dependency update policy itself
  (class E); sweeps run unattended; QA owns schedules, feeds,
  allowlists, root configs, and the tightening job's configuration
  as class E through PL-PIPE. Tightenings ride 0010's
  direction-conditional lane.

## Why this gate exists

Supply-chain rot and slow entropy accrue in the quiet weeks, not
inside feature work - and an agent pipeline makes the quiet weeks
quieter: agents never spontaneously upgrade a dependency, never
revisit a baseline, and never notice a feed. Both drifts this tier
gates are silent and compounding, which is why the venue is a clock.

The subtlest exogenous drift is the gate set's own: a ratchet whose
baseline never re-captures becomes slack - un-enforced headroom the
codebase can regress into without any gate noticing (Goodhart
decay). G9.4 exists to make enforcement track reality on a cadence.

Classes closed: supply-chain rot - known-vulnerable and EOL
components (G9.2), license noncompliance (G9.3), update stagnation
(G9.1); enforcement staleness (G9.4) ([taxonomy](../taxonomy.md)).

## Conditions

Per [0008](../../decisions/0008-two-layer-condition-model.md): **Shape**
is normative and ecosystem-free; **Reference binding** is the .NET
profile. Object default: the current locked dependency closure and
the enforcement baseline set.

### G9.1 Dependency PRs gated by full suite

- **Shape (pass condition):** every dependency change reaches main
  only through the full ordinary gate set. Clauses:
  1. **No reduced lane** - a dependency update is an ordinary
     change: full G4 at merge (including G4.9's delta arm on its own
     diff), ordinary G5 promotion downstream; no dependency-specific
     check profile exists anywhere. Auto-merge-on-green is
     legitimate *because* it rides the full result - the policy
     decides whether, never what gets checked.
  2. **Write surface = manifest + lockfile, exactly** - the 0010
     machinery applied: the bot lane's surface is the dependency
     manifest + lockfile (policy may name generated artifacts that
     mechanically follow). An update needing source adaptation exits
     the lane and enters ordinary intake as a task.
  3. **Standing contract** - the lane runs on the dependency update
     policy itself (class E: cadence, grouping, auto-merge, holds)
     as its standing task contract, escalating to a per-task
     contract exactly when the write surface must widen. **Holds
     never stop the G9.2 clock** - a hold is an update-lane
     decision, never an SLA exemption.
  4. **Atomicity** - single-dependency PRs by default; batching only
     within declared version-locked groups (where a partial bump is
     the broken state); transitive churn rides its direct parent.
     No revert leg exists or is needed - a red update simply never
     merges.
  5. **Field-impact ordering** - the G7.5 SBOM join yields exposure
     classes (*fielded-runtime / build-time-only / dev-only*); the
     update queue orders by them, and G9.2's windows key off the
     same classification. One join, two consumers.
- **Reference binding (.NET):** Renovate/Dependabot over central
  package management (`Directory.Packages.props` as manifest,
  `packages.lock.json` as lockfile); NuGetAudit rides G4.9; the
  SBOM join reads the G7.5 CycloneDX records. Bot liveness rides
  the venue rule (an update-check job past cadence reads red).
- **Gap status:** none at shape level; bot activation rides the
  pilot (Q6).
- **Why:** closes the silent half of supply-chain rot - updates
  happen, happen safely, and happen unattended, escalating to
  human-shaped work exactly at the write-surface boundary.
- **Kind & loopability:** mechanical; diagnostic = the failing
  gate's own diagnostic on the update PR; loop consumer is the lane
  (retry with next version) or intake (escalated task).
- **Parameters:** cadence, grouping, auto-merge, holds = the update
  policy (class E); nothing numeric is kit-level.
- **Lifecycle:** `specified` (ratified 2026-07-26).

### G9.2 Vulnerability-fix SLAs

The pipeline's only clock-based condition - and the owner of the
aging-window family every other venue borrows
([0012](../../decisions/0012-stop-the-line-economy.md)).

- **Shape (pass condition):** no advisory- or EOL-matched component
  in the locked closure past its window. Clauses:
  1. **The family, defined here** - an aging window = (clock origin,
     duration per class, breach effect); every pipeline window lives
     in the clocks artifact (class E, 0010 direction-conditional:
     shortening auto-approves, lengthening takes the second
     channel). Consumers reference, never redeclare (0012).
  2. **Clock origin = publication** - the advisory feed's
     publication timestamp, not local detection: detection-as-origin
     would let a lazy sweep grant extra grace. Feed lag is priced
     into the Q4 durations. EOL fold-in (close-out): end-of-support
     is the same aging shape - feeds include EOL sources, origin =
     the announced EOL date.
  3. **Windows are two-axis** - advisory severity x exposure class
     (G9.1 clause 5's join). Proportionality lives here, in the
     durations, and only here.
  4. **What "fixed" means** - the non-vulnerable graph merges (bump,
     replacement, removal - via the lane or an escalated task), or
     a **not-affected disposition**: class-E suppression with
     written rationale and an expiry (VEX-shaped, re-affirmation
     forced, never silently permanent; loosening polarity per
     0010).
  5. **Breach = standing red, uniform teeth** - the three 0012 arms
     (intake; merge - already encoded in G4.9's row; admission,
     scoped by the SBOM join to fielded services embedding the
     component); fix lane via `fixes`. Tiered teeth rejected:
     uniform teeth, tiered windows.
  6. **Burn-down visibility** - the sweep publishes time-to-breach
     per open advisory; a warning surface, never the gate.
- **Reference binding (.NET):** NuGetAudit/OSV + EOL feeds over the
  lockfile closure; suppressions as VEX-style records in
  enforcement config; exposure classes from the CycloneDX join.
- **Gap status:** none - audit feeds and lockfiles are
  ecosystem-standard.
- **Why:** a known vulnerability is the one defect class that
  worsens while untouched - exposure compounds with time, so the
  only honest gate shape is a clock.
- **Kind & loopability:** mechanical; diagnostic = advisory id +
  component + window state; loop consumers are the G9.1 lane and
  intake (fix tasks, provenance `G9 maintenance`).
- **Parameters:** every duration Q4, resident in clocks.yaml;
  severity from the feed; exposure from the join.
- **Lifecycle:** `specified` (ratified 2026-07-26).

### G9.3 License audit

- **Shape (pass condition):** every package in the full locked
  closure carries a license allowed for its exposure class. Clauses:
  1. **Why a sweep at all** - packages do not change license sitting
     still, but the verdict has two moving parts no diff contains:
     the allowlist itself (legal posture shifts) and the world's
     license knowledge (registries correct misdeclared metadata).
     The diff/world division, instantiated.
  2. **Unknown reads red** - no machine-readable license, bespoke
     license text: fail-closed; resolution is a human
     classification recorded as an explicit entry. Fail-open on
     unknowns guts the gate, and unknowns are the common case.
  3. **One allowlist, exposure-scoped, two arms** - class E; entries
     scoped by exposure class (a license may be allowed dev-only,
     disallowed fielded-runtime - copyleft binds at distribution);
     G4.9 enforces the delta at merge, G9.3 sweeps the set.
  4. **Direction-conditional change control** - removing an entry
     (tightening) auto-approves even when it reds the standing set;
     additions and per-package exceptions are loosenings - full
     second channel. Exceptions carry written rationale + expiry
     (annual reference cadence).
  5. **Breach joins the aging family** - remediation window keyed by
     exposure class (clocks.yaml), then the uniform arms; the delta
     arm holds new introductions at zero while the window burns -
     the problem can shrink but never grow.
- **Reference binding (.NET):** SPDX expressions from NuGet metadata
  over the lockfile closure; ClearlyDefined-family enrichment for
  unknowns; exposure classes from the CycloneDX join.
- **Gap status:** none.
- **Why:** license risk has the CVE drift profile - obligations bind
  at distribution, verdicts change without diffs, and nobody
  re-reads licenses during feature work. Same gate shape, legal
  defect class.
- **Kind & loopability:** mechanical; diagnostic = package + license
  + failing class; loop consumers as G9.2.
- **Parameters:** windows in clocks.yaml (Q4); exception cadence =
  config; allowlist *content* = business/legal authority - the kit
  fixes residence and change control, never the org chart.
- **Lifecycle:** `specified` (ratified 2026-07-26).

### G9.4 Tightening & baseline freshness

Adopted at the S11 walk (stop 5) - G9's authored-here core had no
condition enforcing it, the same gap shape that minted G7.5.

- **Shape (pass condition):** no ratchet-managed parameter past its
  tightening cadence; no tightening evidence without an outcome.
  Clauses:
  1. **Four evidence families in** - (a) ratchet actuals vs
     baselines (G4.7, G4.8, G10.2): gap = slack = candidate; (b)
     corpus growth (G5's discovered state: new entries, minimized
     crashers); (c) mutation scores vs floor (G5.5, under the S9
     small-N rules); (d) measurement records (G7.1) beating
     ceilings + ladder-assignment statistics (G8.3): where escapes
     cluster, which gates under-catch.
  2. **Three output lanes by artifact class** - **land**: class-E
     ratchet baselines re-capture to actual, auto-approved through
     0010's tightening lane, full CI applies (capture-to-actual
     passes current main by construction); **draft**: class-S
     parameters (perf budgets, SLO targets) get tightening
     *proposals* as spec-channel PRs - the job never auto-lands
     class S; **report**: directional evidence (ladder statistics)
     routes to the owning gate's channel as suggestions - the job
     lands nothing structural.
  3. **Tighten-by-default** - declining a candidate takes a written
     rationale (disposition record; G8.3's conversion-by-default,
     transposed). A declined tightening is not a loosening - but
     silent evidence-dumping is a dead convergence loop.
  4. **The job never loosens** - contrary evidence (a budget
     consistently breached) routes as a second-channel suggestion,
     never a landed change.
  5. **Liveness + config** - the job past its cadence reads red
     (the venue rule); its configuration (cadences, capture rules,
     managed-parameter set) is class E under PL-PIPE.
- **Reference binding (.NET):** a scheduled job over committed
  records (measurement records, ladder records, corpus state) and
  the class-E baseline files; cadences in clocks.yaml.
- **Gap status:** none at shape level; job implementation is
  enforcement-pass work, conditional on pilot activation (Q6) - the
  trace-validation-harness pattern; the build-item register stays
  four.
- **Why:** a ratchet that never re-captures is theater - the gap
  between baseline and actual is headroom regressions pass through.
  The pipeline accumulates evidence about itself (measurements,
  corpus, scores, ladder stats) that nothing consumed until now;
  G9.4 is the convergence loop pointed at the gate set.
- **Kind & loopability:** mechanical - the gate passes by landing;
  judgment appears only in the optional, rationale-bearing decline.
  Diagnostic = stale parameter or undispositioned candidate; loop
  consumer = the job's next run and the owning gate's channel.
- **Parameters:** cadences Q4 (clocks.yaml); per-family cadences
  may differ (corpus rides the merge queue continuously; baselines
  monthly reference; budget reviews quarterly reference).
- **Lifecycle:** adopted + `specified` (ratified 2026-07-26).

## Refactoring budgets (routed out)

The third authored-here item of the source table is resource
allocation - how much capacity entropy pay-down gets. That is
business policy, outside gate scope (the G7 deploy-timing
precedent). The kit's hooks: G9.4's report lane generates the work
candidates; 0005's `provenance: G9 maintenance` tags the tasks; the
gate never enforces a staffing decision.

## Completeness check

Gate purpose: hold the line between features; the check asks what
exogenous drift escapes four conditions. Examined:

- **Platform/runtime EOL.** Same aging shape as advisories; folded
  into G9.2 (feeds include EOL sources, origin = announced date).
- **Backup verification / restore drills.** Ops practice outside
  gate scope (the G8 boundary precedent); the pipeline's own
  recoverability appears exactly where it acts - G10.3's record.
- **Documentation rot.** PL-DOC's business (S12).
- **Stale branches / unmerged work.** Hygiene, not a gated defect
  class.
- **Pillar sweep verdict:** updates (G9.1), vulnerabilities + EOL
  (G9.2), licenses (G9.3), enforcement staleness (G9.4) cover the
  exogenous half of the anti-entropy thesis; the endogenous half is
  G10's.

Roster verdict: complete at four - one adopted (G9.4), zero
renamed; no human condition (census unchanged at six: G1.3, G2.3,
G6.1, G6.2, G8.3, PL-PIPE.1).

## Operators & harness

Nobody attends this gate. The bot authors update PRs under its
standing contract; sweeps detect; breaches open standing reds whose
remediation enters ordinary intake as fix tasks (`fixes` field,
provenance `G9 maintenance`); accountability sits with the standing
red's owner. QA owns every class-E surface (schedules, feeds,
allowlists, baselines, the tightening job's config) through
PL-PIPE. The tightening job is the one authoring surface: it lands
class-E tightenings, drafts class-S proposals, and reports
directional evidence - never loosening, never touching what was
never its.

## Decisions & open items

- All four conditions `specified` 2026-07-26 (session-11 walk);
  G9.4 adopted at stop 5.
- Frame rulings applied: anti-entropy pair (exogenous half);
  standing invariants, sweep-detected; dead-sweep liveness; the
  diff/world division; the 0012 red economy; no maintenance
  principal.
- ADR [0012](../../decisions/0012-stop-the-line-economy.md) minted
  here: aging-window family + one clocks artifact + the ninth
  task-contract field `fixes`.
- G9.1 ruled: no reduced lane; manifest+lockfile write surface with
  exit-to-intake; standing contract; single-dep atomicity with
  declared groups; holds never stop the clock; SBOM exposure
  ordering.
- G9.2 ruled: family ownership; publication clock; severity x
  exposure windows; VEX-shaped suppression with expiry; uniform
  teeth (tiered rejected); burn-down surface; EOL fold-in.
- G9.3 ruled: unknown-fail-closed; exposure-scoped allowlist;
  direction-conditional control; expiring exceptions; breach joins
  the family.
- G9.4 ruled: four families, three lanes (land/draft/report by
  artifact class); tighten-by-default with rationale-bearing
  decline; never loosens; refactoring budgets routed to business
  policy.
- S12 banked from here: clocks.yaml derivations + three-lane
  routing as PL-PIPE.2 golden-test subjects; direction-conditional
  now has four instances for Q7's worked-example set; sweep + bot
  activation joins the Q6 pilot scope.
