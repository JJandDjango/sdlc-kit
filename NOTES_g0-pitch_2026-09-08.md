# G0 pitch notes - the feature document and the contract

_Session 28, 2026-09-08. Working notes, not a Cairn stratum. Unratified:
the mapping below is the agent's proposal, discussed and not pushed back
on. It graduates to USAGE.md (a section beside section 8) and a candidate
ADR once the user ratifies it after the session-29 video check._

## Purpose

The user pitches the kit to a consumer with a PO team and engineers. The
venue they already have is a feature document (a Google Doc, editable by
the PO team) discussed by both teams. Sections: authors, the feature
request at a high level, the business use case, prerequisites (usually
user permissions), technical implementation details (a REST endpoint
table, tech stack, integrations), functional tests (Gherkin), and misc
Q&A. A document is a new feature or a bug fix.

## Verdicts on record this session

- The kit adheres to the SDLC by construction, to the V-model with stage
  gates, not to waterfall activities (handoff section 5). Three
  departures, each ADR-ruled: a phase is a venue (0003); testing is
  redistributed by feedback latency (G3 seconds, G4 minutes, G5 hours,
  G6 principal-paced); documentation and the pipeline are gated peers
  (PL-DOC, PL-PIPE). Human census six of 56 (0015).
- Gaps named: enforcement live at G0 only (three conditions enforced, 56
  specified); G0 checks well-formedness, never worth; the lifecycle is
  per task, with no gate for system conception, and G10 retires
  components, not systems.
- G0 has zero human conditions and is the one venue where the humans
  are in the room. The human act is answering; the gate checks the
  record of the answer. Nobody writes YAML or the controlled register.

## G0 pitch readiness

Nailed and shippable as shown: the valid/sound split (NOTES_phase0); the
eight fields and the seat map (USAGE section 8); seats as a per-repo
term; `confirmed_by` + TC016; the meeting shape (one session, both
seats, one artifact, ready-green or parked); ApplyDiscount with the
house rule left open.

Loose, in fix order:

1. Where the PO sits. The venue is a Claude Code session with prompts
   per unit. Default: synchronous, engineer drives, PO answers; the PR
   is the asynchronous record. Nothing checks who was in the room, by
   design (0025 rejected author checks).
2. Immutability is a design claim today. G4.6 (the write-surface diff
   audit) is specified, unbuilt; CI validates form and PR review is the
   guard. CODEOWNERS was rejected in 0010 (approval-shaped,
   platform-bound); the answer is the audit job, not a GitHub setting.
3. No business fields (priority, estimate, value), correctly: the
   contract is immutable and priority is not. The tracker keeps
   priority; the contract links out via `provenance.ref` or a matching
   id.
4. G1 is paper. After intake, criteria are written by hand until the
   G1 slice ships. Say so.
5. Vocabulary overhead objection. Accretion only: a term is forked when
   a contract needs it (TC010); this repo holds 18 ratified terms after
   27 sessions; never ratify to go green.

## The feature document is the raw request

Keep the document. It is the raw request the intake venue consumes and
the PO team's venue for their own words. The contract is what the
intake meeting produces from it, never a replacement. The document
holds worth and design; the contract holds form and entry. This closes
the "worth" gap: the business case is decided in the document, by its
owners, before intake.

| Document section | Lands as | Gate |
|---|---|---|
| Authors | the seats that answer per unit, recorded in `confirmed_by` | G0 |
| Feature request, high level | `intent`, in the PO's words | G0 |
| Business use case | stays in the document; `provenance.ref` links back | upstream of G0 |
| Prerequisites (permissions) | an existing permission is a ratified term under `entities`; one another task must create is a `dependencies` entry; the access rule itself is a guard unit with a sketch | G0 |
| Technical implementation | `scope` paths only at G0; the endpoint table is the boundary schema G1.1 lints and G2.2 locks | G0, G1, G2 |
| Functional tests (Gherkin) | 1 to 3 sketches per unit at G0; numbered criteria and immutable tests at G1 | G0, G1 |
| Misc Q&A | every decided answer lands as a sketch, a criterion, a non-goal, or a term; open ones carried visibly, decided at G1.3 | G0, G1 |
| Feature or bug fix | `provenance.origin`: `human-request`, or `g8-escape` with the incident ref (TC009 requires it) | G0 |
| Unit tests | nowhere in the document | G3 |

Unit tests: the implementer's only write surface (G3), derived from the
implementation, mutable by its author. The document and the contract
are the spec channel; the channels stay decorrelated (THEORY). The
document stops at Gherkin. G4.11 checks unit tests exist and pass, G5.5
that the spec suite has teeth; nothing checks their content.

## Template changes proposed, in priority order

1. Add "Not in scope": `non_goals`. TC002 rejects a contract without
   them; "what is this not?" is the PO's question before the meeting.
2. Group the Gherkin by unit. A group's title is the unit's `done_means`
   and its first scenarios are the sketches; the decomposition falls out
   of the grouping, and units stay outcomes a test can decide, never
   implementation steps.
3. Add "Terms": the PO's nouns in their words, the source for the
   vocabulary files the PO ratifies. The join is optional; this can wait
   a round.

Add a status line to the document naming its contract and state (ready
or parked, dated). A change after ready goes back through intake: new
answers, new merge.

## What the document already gets right

- Gherkin is a head start on G1: 0011 fixes one row per criterion with a
  task-scoped REQ-ID and tests annotated to it; a scenario is one
  criterion. The same scenarios run by machine at G4.3 and are walked
  by the PO at G6.1. Today Gherkin to `criteria.yaml` is by hand; the
  G1 slice makes it mechanical. Input to the G1 slice design: Gherkin
  as the human authoring format for criteria.
- A bug fix is the convergence loop verbatim: a `g8-escape` document
  whose Gherkin carries the regression scenario, which becomes a test
  the implementer cannot edit.

## Open

- Next decision: which real feature document goes through intake first
  (paste, or a Drive link); the agent drafts its contract as the demo
  artifact.
- Session 29 opens with a YouTube video review on this topic, the
  user's check that the direction is right, before any of the above is
  ratified.

Sources: docs/gates.md; docs/gates/G0-planning-intake.md;
docs/gates/G1-requirements-spec.md (G1.3 checklist);
docs/task-contract.md; docs/vocabulary.md; USAGE.md section 8;
NOTES_phase0_2026-08-25.md; skills/sdlc/flows/intake.md; decisions
0002, 0003, 0005, 0006, 0010, 0011, 0015, 0020, 0025;
HANDOFF_gate-architecture_2026-07-22.md sections 2 and 5.
