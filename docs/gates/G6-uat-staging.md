# G6 - UAT / Staging

<!-- covers: HANDOFF_gate-architecture_2026-07-22.md -->

> **Contract** - one question: *what must the UAT / Staging gate
> contain, and why?*
> Deep page per [0004](../../decisions/0004-per-gate-documentation-program.md);
> registry row: [gates.md](../gates.md). Source: handoff section 5 row 6;
> the G5 promotion ladder ([G5 page](G5-integration-system.md)); ADR
> [0011](../../decisions/0011-criterion-traceability-format.md) (the
> criteria records the walk consumes). Two-layer per
> [0008](../../decisions/0008-two-layer-condition-model.md).

## Identity

- **Venue:** production-like staging environment, reached only through
  G6.3's certified deploy path. The staging *definition* is
  enforcement-layer, class E (frame ruling): a drifted staging silently
  voids every verdict issued here, and a Developer-editable staging
  would let the subject shape its own exam room.
- **Cadence:** per candidate, **principal-paced**: G5 emits a rolling
  stream of promotable snapshots; G6 draws from that stream at the
  principal's pace. No 1:1 coupling - promotion is mechanical and
  continuous, acceptance is human and scheduled.
- **Inputs:** the promoted candidate (verified artifact, pinned sha);
  the delta criteria records (`criteria.yaml`, per 0011); the prior
  acceptance record (for dismissed-finding continuity).
- **FAIL blocks:** candidate acceptance. **Default-deny:** a candidate
  without a complete acceptance record simply is not accepted - there
  is no silent pass.
- **V-model position:** the human boundary - the first judgment venue
  since G1.3, and the pipeline's second attention concentration. Every
  gate since G2 proved *conformance to articulation*; none can prove
  the articulation matched intent. A spec is a compression of intent,
  and compression loses; G6 is where the intent-holder checks the
  artifact against the thing itself.
- **Trust boundary:** the grading is **non-delegable** (frame ruling).
  An agent's only oracle is the spec text, and G6 exists to catch what
  the spec text missed. QA operates the venue - certified deploy,
  walk-sheet preparation, recording, assistive scouting - but cannot
  grade. G6 authors through the front door (frame ruling): findings
  mint REQ-IDs via the spec channel, never via side-door test writing.

## Why this gate exists

The oracle problem's residue is irreducible: mechanical gates prove
the code satisfies the articulated spec; *conformant-but-wrong* is the
code a mechanically satisfied spec still permits. The two human
conditions split that residue exactly - **G6.1: the articulated was
wrong** (criteria walked, found wanting); **G6.2: the unarticulated
was violated** (probing finds what no criterion covers). The
convergence loop makes the check *compounding*: every validated
finding moves a piece of intent from tacit to enforced - minted as a
criterion, reviewed at G1.3, armed red by G2.5, closed by a fix,
witnessed forever by G4.3. G6 shrinks its own residue monotonically.
G8.3 is its sibling at the operations end - the convergence loop's two
intake ports.

Human conditions do not claim loopability (vocabulary rule); for them
`specified` means procedure, record, and pass semantics fixed.
Everything around the judgment is machine-shaped - prepared walk
sheets, committed records, mechanically consumable outcomes - the
G1.3 pattern.

Classes closed: residual requirements misinterpretation; venue drift
(G6.3, adopted this walk).

## Conditions

Per [0008](../../decisions/0008-two-layer-condition-model.md): **Shape**
is normative and ecosystem-free; **Reference binding** is the .NET
profile (thin here - the gate is mostly procedure and records, which
are ecosystem-free by construction).

### G6.1 Human validation against REQ-IDs

- **Procedure (pass condition):** the principal walks the **delta
  criteria** - new or changed since the last accepted candidate - in
  the certified staging environment, judging whether the behavior
  matches *intent* (text-conformance was proved at G4.3; the human
  judges whether text-conformance is the wanted behavior). Clauses:
  1. **Delta scope** - the mechanical layer re-proves every old
     criterion on every merge; human attention goes where
     misinterpretation risk concentrates: freshly articulated, freshly
     implemented criteria. Empty delta = trivially green, recorded as
     such.
  2. **Walkable partition** - QA's prepared walk sheet partitions the
     delta: *staging-observable* criteria the principal walks;
     *internal* criteria (mechanically proven, nothing to experience)
     listed for acknowledgment with their witness status. The
     principal may pull any listed item into the walk.
  3. **Verdicts** - per-criterion accept / reject-with-finding,
     recorded in the acceptance record. The principal may
     **accept-with-findings**: the candidate is accepted while each
     finding mints a criterion that G2.5 arms red - no future
     candidate passes G4.3 until it is implemented. Acceptance plus a
     mechanically enforced forward obligation, never a re-litigated
     promise.
- **Findings indict the spec layer, by construction:** the
  implementation provably conforms (G4/G5 said so), so a rejected
  criterion means the criterion under-specified intent or its witness
  was inadequate. Both are spec-channel work first; the implementation
  fix follows the revised spec.
- **Reference binding:** walk sheet generated from the delta of
  `specs/*/criteria.yaml` (rides the 0011 script family); staging per
  G6.3's certified deploy; verdicts into the acceptance record.
- **Gap status:** none - procedure and records are ecosystem-free.
- **Why:** the far end of the misinterpretation loop. G1.3 checked the
  *spec* against intent before code existed; G6.1 checks the *product*
  against intent after the spec is mechanically satisfied. Same role,
  same scarce resource, the two ends of one loop.
- **Kind:** human - judgment checkpoint; loopability not claimed. The
  scaffold is mechanical: prepared sheet, committed record,
  machine-consumable outcome.
- **Parameters:** walk-sheet format = policy config.
- **Lifecycle:** `specified` (ratified 2026-07-24).

### G6.2 Exploratory testing

- **Procedure (pass condition):** a timeboxed unscripted session per
  candidate - the principal probes beyond the criteria for wrongness
  the spec never articulated. Clauses:
  1. **The principal grades; agents may scout** - QA may run
     *assistive exploration*, surfacing candidate oddities as
     suggestions entering the principal's triage - never verdicts.
     Stated explicitly because this is the drift path the frame ruling
     exists to block: assistive scouting is leverage; "the agent does
     UAT" is the anti-pattern. "Odd, given what this product is *for*"
     is an oracle only the intent-holder has.
  2. **Conversion** - each validated finding enters the convergence
     loop: Spec agent drafts the criterion (REQ-ID per 0011), G1.3
     reviews the articulation, G2.5 arms it red, the fix closes it,
     G4.3 witnesses it forever. Dismissed findings ("works as
     intended") are recorded with disposition - rediscovery next
     candidate costs one glance.
  3. **Attestation** - the record must attest the session happened,
     even at zero findings: the human-condition equivalent of
     zero-tests-FAIL. No silent skip.
- **Reference binding:** session budget = policy config; findings +
  dispositions into the acceptance record.
- **Gap status:** none.
- **Why:** the unarticulated-intent residue - the one class no
  mechanical gate can own, shrunk monotonically by conversion.
  Adversarial pen-testing rides this condition's shape at the
  principal's discretion (close-out ruling: available practice, not
  mandate).
- **Kind:** human; scaffold mechanical (timebox, attestation, recorded
  dispositions).
- **Parameters:** session budget = policy config.
- **Lifecycle:** `specified` (ratified 2026-07-24).

### G6.3 Venue certification

Adopted at this walk's close-out (roster addition; mechanical). 0010
polices *diffs*, not deployed state: runtime drift - manual
environment changes, stale deploys - is invisible to the write-surface
machinery, so the born-protected argument that dissolved G4's
candidates does not dissolve this one.

- **Shape (pass condition):** object = the staging deployment of the
  candidate. The candidate reached staging via the **committed
  environment definition** (class E), through the **same deploy path
  production uses**; deviations only per the declared-delta allowlist
  (class E: scale, data, secrets); certification - definition hash +
  deploy provenance - recorded in the acceptance record. Missing or
  mismatched = the walk cannot start (precondition to G6.1/G6.2).
- **Reference binding:** the release pipeline targeting staging;
  def-hash attestation into the record; drift check of deployed
  environment vs definition + declared deltas.
- **Gap status:** none - environment definitions and deploy tooling
  are ecosystem-universal.
- **Why:** a drifted staging voids every G6 verdict silently -
  vacuity-shaped, and mechanically checkable. Bonus bought free: every
  G6 walk *rehearses the G7 deploy* - deployability defects surface
  one gate early (formalization from G7's side banked, S10).
- **Kind & loopability:** mechanical; diagnostic = the drift diff or
  the missing certification - loopable by the enforcement channel
  (environment fixes are class E work, never Developer work).
- **Parameters:** declared-delta allowlist content = class E policy
  artifact.
- **Lifecycle:** `specified` (adopted + ratified 2026-07-24).

## The acceptance record

One committed artifact per candidate - the gate's machine-readable
residue, and the reason human judgment can sit inside a mechanical
pipeline without becoming a verbal handshake:

- **Contents:** candidate sha; walker identity; per-criterion verdicts
  (delta set); acknowledgment of the internal list; exploratory
  attestation + findings + dispositions; venue certification (G6.3);
  overall verdict.
- **Residence:** class S - acceptance *is* a spec-channel act: the
  principal ratifying "this matches intent."
- **Downstream teeth:** G7's admission mechanically consumes it -
  record present, verdict accepted, no unresolved blocking findings.
  Absent record = not accepted, default-deny.

## Completeness check

Gate purpose: the judgment residue - everything requiring intent no
artifact captures - decided per candidate; the check asks what escapes
three conditions. Examined:

- **Staging parity.** Adopted as G6.3 (close-out): runtime drift is
  outside 0010's sight, vacuity-shaped, mechanically checkable.
- **Sign-off record.** Resolved into the acceptance record (stop-7
  ruling): committed, class S, G7-consumed, default-deny.
- **Adversarial pen-testing.** Not mandated; available as
  G6.2-flavored practice at the principal's discretion (the mechanical
  security stack is G2.4 -> G4.7 -> G5.3).
- **Accessibility / UX polish.** The unarticulated-intent class -
  G6.2's domain by construction; no separate condition.
- **Pillar sweep verdict:** everything mechanizable stays upstream by
  the admission logic; the judgment residue is fully housed in two
  human conditions plus one mechanical venue guard. G6 stays small by
  design - human attention is the pipeline's scarcest resource, spent
  only where no mechanism substitutes.

Roster verdict: complete at three - one adopted at close-out (G6.3);
human conditions remain exactly two, and the vocabulary's
"concentrated at G1 and G6" holds.

## Operators & harness

QA operates the venue: the certified deploy (G6.3), walk-sheet
preparation from the criteria delta, recording, and assistive
scouting - suggestions, never verdicts. **The principal grades** -
non-delegable by construction: an agent's only oracle is the spec
text, and G6 exists to catch what the spec text missed. Findings route
spec-channel by construction (G6.1 indicts the spec layer; G6.2 mints
through the front door) - the Developer appears at G6 only as the
downstream consumer of the tasks those findings generate. The
acceptance record is the machine-readable residue every later gate
trusts. The pipeline's attention concentrations stay exactly G1.3 and
here.

## Decisions & open items

- All three conditions `specified` 2026-07-24 (session-9 walk; G6.3
  adopted at close-out).
- Frame rulings applied: the principal is the grader (non-delegable;
  QA operates, never grades); G6 authors through the front door (spec
  channel, no side-door tests); staging definition = class E;
  principal-paced draw from the promoted stream (no 1:1 coupling with
  G5 runs).
- G6.1 ruled: delta scope; walkable partition with pull-in; findings
  indict the spec layer by construction; accept-with-findings = an
  auto-armed forward obligation (G2.5 arms, G4.3 blocks until
  implemented).
- G6.2 ruled: assistive-exploration lane (suggestions never verdicts);
  the conversion loop as stated; attestation anti-vacuity.
- G6.3 adopted: venue certification via the production deploy path;
  declared-delta allowlist; walk-blocking precondition; G7 rehearsal
  bonus.
- The acceptance record ruled: class S, per candidate, G7-consumed,
  default-deny.
- S10 inputs banked: G7 admission consumes the acceptance record;
  deploy-path formalization from G7's side; G8.3 reuses the
  conversion-record shape; production chaos (G8 venue question).
