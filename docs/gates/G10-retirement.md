# G10 - Deprecation / Retirement

<!-- covers: HANDOFF_gate-architecture_2026-07-22.md -->

> **Contract** - one question: *what must the Deprecation/Retirement
> gate contain, and why?*
> Deep page per [0004](../../decisions/0004-per-gate-documentation-program.md);
> registry row: [gates.md](../gates.md). Source: handoff section 5 row
> 10; the G7.2 contract-diff + break records ([G7
> page](G7-release-deploy.md)); the G6.3 certified environment ([G6
> page](G6-uat-staging.md)); ADRs
> [0009](../../decisions/0009-custom-analyzer-adoption-policy.md),
> [0012](../../decisions/0012-stop-the-line-economy.md),
> [0013](../../decisions/0013-sunset-policy.md).
> Two-layer per [0008](../../decisions/0008-two-layer-condition-model.md).

## Identity

- **Venue:** the deadline gate (frame ruling) - G10 owns no pipeline
  of its own; it injects declared deadlines into venues that exist:
  the analyzer at build (G10.1), the graph count at the scheduled
  sweep (G10.2), record checks at merge + admission (G10.3).
- **Cadence:** sunset-date driven - the date, not the clock.
- **Inputs:** deprecation records + sunset dates (class S, 0013);
  usage telemetry from the shared instrumentation surface; fleet
  version facts (G7.2 release records); migration specs.
- **Object:** absence - the only gate whose subject is what must
  *stop* existing. Every other gate verifies what exists; G10
  verifies that things scheduled to die actually die, and die
  safely.
- **FAIL blocks:** merges past a sunset date (analyzer error, no
  suppression lane); dead-count breach (standing red, 0012);
  contract-class migration without its complete retirement record
  (no merge, no admission).
- **Trust boundary:** fully mechanical. Deprecation records ride the
  spec channel (deprecation is a contract change - 0013); the
  analyzer, root configs, and flag schema are class E under
  PL-PIPE; removal work enters ordinary intake.

## Why this gate exists

Agents add code and almost never delete it; without an explicit
removal phase the codebase grows monotonically regardless of every
other gate. Deletion has to be *forced* - by deadlines a compiler
enforces - and *safe* - the contract phase of a migration is the
pipeline's only irreversible act. Everything here serves those two
words: G10.1 makes intent-to-remove executable, G10.2 makes
accumulation self-limiting, G10.3 makes the irreversible step
proven before taken.

The deletion pipeline (frame + stop rulings): **G10.1 starves ->
G10.2 counts -> G10.3 clears -> G7.2 records the break.**
Escalation starves internal usage at the date; the starved code
surfaces in the dead count and pressures the ratchet; removal at
the shipped boundary rides G7.2's break-record machinery; the data
far end admits only with its retirement record complete.

Classes closed: accretion - dead code, stale feature flags,
zero-edge packages (an entropy process, per the
[taxonomy](../taxonomy.md)'s structural-degradation note); unsafe
removal - data loss at contraction (the build/config/deployment
row's destructive-migration end).

## Conditions

Per [0008](../../decisions/0008-two-layer-condition-model.md): **Shape**
is normative and ecosystem-free; **Reference binding** is the .NET
profile. Object default: the current codebase plus the fielded
release set.

### G10.1 Obsolete-sunset escalation

- **Shape (pass condition):** no usage of a sunset-bearing subject
  at or past its date. Clauses:
  1. **Declaration + projection** (the slo.yaml shape) - the
     deprecation record is class S: {api id, replacement ref,
     migration-spec ref where the path carries data/behavior,
     sunset date, notification ref, provenance}. The in-code mark
     is the record's compiled projection, carrying the date into
     binary metadata (the mark is what a consumer's compiler
     reads). The analyzer checks coherence both ways: mark <->
     complete record; incomplete = merge red - never a silently
     unarmed sunset.
  2. **Escalation** - usage warns before the date, errors at and
     past it (G3 editor surface + G4 merge block from one
     analyzer). No ordinary suppression lane exists; the only exit
     is a governed date move.
  3. **The clock starts at notification** (0013) - a date is valid
     only >= notification + the minimum-notice floor for its
     surface class (shipped per the G7.2 package set vs internal;
     floors in clocks.yaml, Q4). The notification ref is the G7.2
     contract-diff payload of the release that shipped the mark -
     notice a consumer could not have seen is not notice.
  4. **Move asymmetry** (0013) - later = loosening, full second
     channel; earlier = never below minimum notice from the
     original notification. All moves are record edits; the
     coherence check catches attribute-only drift.
  5. **Subjects include declared config surfaces** (close-out
     fold-in) - feature flags are sunset-bearing by schema: a flag
     declaration requires a sunset date, references past it read
     error. Stale flags are the accretion vector the dead-code
     oracle cannot see (a flag check keeps both branches
     reachable); the deadline machinery closes them at zero new
     conditions.
  6. **Boundary honesty** - enforcement reach ends at the shipped
     boundary: internally the build breaks; externally the
     obligation is notification, notice floors, and published
     migration specs. The kit governs its side completely and
     claims nothing beyond it.
- **Reference binding (.NET):** custom Roslyn analyzer - a
  0009-family adoption riding the enforcer arc - reading
  `[Obsolete]`/`[Sunset]`-family attributes + `specs/deprecations/`
  records; ApiCompat diff payloads as notification refs;
  release-notes generation from the same payload (PL-DOC input);
  flag declarations in the class-E flag schema.
- **Gap status:** the analyzer is a build item under 0009's policy,
  riding pilot activation (Q6) with the first tranche.
- **Why:** deprecation without a date is a suggestion; a date
  without escalation is a lie. The only counter to monotonic growth
  is a deadline a compiler enforces - made legitimate by
  declaration, notification, and notice.
- **Kind & loopability:** mechanical; diagnostic = subject + date +
  usage site; loop consumers are migration tasks (off the old path)
  and the removal task the starvation enables.
- **Parameters:** notice floors in clocks.yaml (Q4); record + flag
  schemas = reference binding.
- **Lifecycle:** `specified` (ratified 2026-07-26).

### G10.2 Dead-code ratchet

- **Shape (pass condition):** graph-level dead count <= the
  captured shrink-only baseline. Clauses:
  1. **The count** - unreachability over product assemblies from
     declared roots: entry points, the shipped public surface
     (G7.2's package set - external liveness is contractual, not
     provable from inside), framework-convention roots, explicit
     keep-declarations. **Undeclared liveness reads dead** - a
     reflection or DI edge the tool cannot see must be declared
     (class-E root config with rationale); the red is productive
     pressure to make implicit edges explicit - an agent pipeline
     cannot respect invisible liveness. The initial capture absorbs
     the existing undeclared stock.
  2. **Ratchet discipline = G4.8's, verbatim** - count <= captured
     baseline; shrink-only; static between G9.4 tightenings; zero
     at greenfield. Every deletion becomes permanent.
  3. **Post-sunset members count** - G10.1-starved corpses are
     expected dead and never excludable: they fill the headroom
     until breach forces the removal work. That is the conveyor
     operating; excluding them stalls it with corpses sitting
     forever. Zero-edge packages count too (close-out fold-in): a
     referenced package no code calls is accretion at the graph's
     coarsest grain.
  4. **Trend is structural, never mandated** - the registry's
     "trending down" struck (close-out): a per-period decrease
     mandate forces deletion regardless of capacity and
     self-destructs at zero. The downtrend emerges - tightening
     makes deletions permanent, the conveyor makes accumulation
     self-limiting. Initial-stock pay-down routes through G9.4's
     report lane; capacity is business policy.
  5. **Venue split** - local unused-member diagnostics ride G3/G4
     analyzers (cheap, immediate); the *gate* is the whole-graph
     count at the scheduled sweep - a diff removing the last
     caller of code elsewhere looks innocent; only the graph
     knows. Breach = standing red (0012 economy, window in
     clocks.yaml).
- **Reference binding (.NET):** ILLink-informed reachability with
  trimmer root descriptors as the keep-declaration format and
  `[DynamicDependency]` as the reflection-edge declaration - the
  ecosystem already built the root-declaration language; the gate
  reuses it.
- **Gap status:** none at shape level; the reachability job rides
  pilot activation (Q6).
- **Why:** the accretion counter itself - the ratchet makes
  deletion the only direction the count durably moves, and its
  false-liveness problem is solved by declaration, not heuristics.
- **Kind & loopability:** mechanical; diagnostic = the dead-set
  delta; loop consumers are removal tasks and the G9.4 tightening.
- **Parameters:** sweep cadence + breach window in clocks.yaml
  (Q4); root format = reference binding.
- **Lifecycle:** `specified` (ratified 2026-07-26).

### G10.3 Data-migration verification

- **Shape (pass condition):** no contract-class migration without
  its complete retirement record. Clauses:
  1. **Mechanical classification** - every schema migration
     classifies lexically as *expand* (additive/compatible) or
     *contract* (drop, narrow, incompatible rewrite);
     **unclassifiable reads contract** (fail-closed). Expand rides
     G7.4's revert-safety clause; contract arms this condition.
  2. **The retirement record** (class S) - a contract-class
     migration merges and admits only with: (a) the deprecation
     chain ref (the G10.1 dossier - the conveyor's paper trail);
     (b) backfill reconciliation evidence (counts, checksums,
     dual-read comparison - never "the job finished"); (c)
     drainage evidence - zero old-path usage over the declared
     window (usage counters on the shared instrumentation surface;
     window in clocks.yaml); (d) fleet coherence - no fielded
     version still requires the old path (G7.2 release records);
     (e) rehearsal - the contract executed green against
     production-shaped data in the certified environment through
     the production deploy path (G6.3's machinery, last consumer);
     (f) recoverability ref - pre-contract snapshot + retention;
     verification must be able to have been wrong once.
  3. **Irreversibility honesty** - contraction is the pipeline's
     only irreversible act: the canary still runs but its revert
     promise is void for the schema, so the entire verification
     burden front-loads - proof before action, never monitoring
     after.
  4. **Venue** - per-retirement, event-driven: merge arm (G4:
     classification + record presence) and admission arm (G7:
     record verified). No sweep - nothing here ages on its own;
     the time pressure arrives from upstream (G10.1's date,
     G10.2's ratchet).
- **Reference binding (.NET):** EF Core migration operations as the
  classification lexicon (`DropTable`, `DropColumn`, narrowing
  `AlterColumn`); OTel usage counters on old paths; dual-read
  reconciliation jobs; G6.3 rehearsal; platform backup refs.
- **Gap status:** none at shape level; classification joins the
  PL-PIPE.2 golden-test set (S12).
- **Why:** every other gate's subject can revert; this one act
  cannot. Irreversibility inverts the verification order.
- **Kind & loopability:** mechanical; diagnostic = the missing or
  failing record field; loop consumer is the retirement task.
- **Parameters:** drainage window in clocks.yaml (Q4); lexicon =
  reference binding.
- **Lifecycle:** `specified` (ratified 2026-07-26).

## Completeness check

Gate purpose: force deletion; the check asks what accretion escapes
three conditions. Examined:

- **Feature-flag debris.** The walk's real find: a stale flag
  defeats the dead-code oracle by construction (both branches stay
  reachable). Folded into G10.1's subject class - flags are
  sunset-bearing by schema; zero new conditions.
- **Package-level dead.** A referenced package with zero call
  edges; folded into G10.2's count.
- **Whole-service retirement.** Beyond the per-repo frame; the
  record machinery scales conceptually, noted for the program
  level.
- **Backup / restore practice.** Ops practice (G8 precedent);
  recoverability appears exactly where the pipeline acts - clause
  2(f).
- **Pillar sweep verdict:** dates with teeth (G10.1), counted
  corpses (G10.2), proven-safe removal (G10.3) cover the
  endogenous half of the anti-entropy thesis; the exogenous half
  is G9's.

Roster verdict: complete at three - zero adopted, zero renamed, two
fold-ins (flags -> G10.1, packages -> G10.2); fully mechanical
(census unchanged at six).

Three patterns this walk used three times each, named for the
program audit (S12): fail-closed polarity (unknown license,
undeclared liveness, unclassifiable migration);
schema-incompleteness teeth (G8.3 dispositions, G10.1 records,
G10.3 records); one-artifact-many-consumers (the SBOM join, the
instrumentation surface, the clocks artifact).

## Operators & harness

Fully mechanical. The spec channel authors deprecation records
(0013); QA owns the analyzer, root configs, and flag schema as
class E; the starve -> count -> clear conveyor generates removal
tasks that enter ordinary intake; nobody grades anything. The
Developer appears only as the consumer of migration and removal
tasks - and the analyzer's error is not theirs to suppress.

## Decisions & open items

- All three conditions `specified` 2026-07-26 (session-11 walk).
- Frame ruling applied: the deadline gate - class-S intent,
  compiled enforcement in existing venues; anti-entropy pair
  (endogenous half).
- ADR [0013](../../decisions/0013-sunset-policy.md) minted here:
  spec-side authorship, clock-from-notification, notice floors by
  surface class, move asymmetry, flags as sunset-bearing subjects.
- G10.1 ruled: declaration + projection with two-way coherence;
  warning -> error with no suppression lane; notification
  structurally unavoidable (G10.4 rejected); boundary honesty.
- G10.2 ruled: declared-roots count with
  undeclared-liveness-reads-dead; G4.8 ratchet discipline under
  G9.4 management; post-sunset corpses + zero-edge packages count;
  trend mandate struck.
- G10.3 ruled: lexical expand/contract classification
  (fail-closed); the six-field retirement record;
  verification-before for the pipeline's only irreversible act;
  no-sweep venue.
- S12 banked from here: record <-> mark coherence,
  notification-clock computation, and migration classification
  join PL-PIPE.2's golden-test set; deprecation dossiers +
  release-notes generation are PL-DOC subjects; the analyzer joins
  the 0009 first tranche (Q6).
