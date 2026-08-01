# 21. Operator-layer shape

Status: accepted
Date: 2026-07-31

## Context

The registry has named operators since the harness design - Spec
agent authors G0-G2 artifacts, Developer works only inside G3, QA
executes G4-G7, Verifier is cross-cutting - but nothing shipped
them: no defs, no distribution channel, no written contract for how
an agent consumes a check. Three shape questions had no precedent.
Granularity: one agent per gate, or one per persona? Residence:
prompts are neither pip modules nor committed scaffold - which
channel carries them? Loop: intake I5 proved the discipline for one
gate; nothing bound it kit-wide. Meanwhile the suppression audit
shipped the first deliberate verdict surface (exit 0/1/2 +
`--json`), and gates.md already scoped agent prompts as class-E
artifacts (PL-PIPE) with the eval obligation specified.

## Decision

1. **Personas, not per-gate files.** One def per operator -
   `sdlc-developer` and `sdlc-verifier` now; `sdlc-spec` and
   `sdlc-qa` registered behind venue existence. Per-gate behavior
   lives in venue bindings inside each def: the two-layer model
   (0008) applied to agents - the persona is the shape, the gate
   binding is the profile.
2. **Prompts ride the plugin channel.** `agents/` at the plugin
   root, versioned with the kit, delivered by `claude plugin
   update` - never rendered into consumers, never merge targets
   (0020's anti-fork doctrine applied to prompt artifacts).
   `/sdlc update` does not cover them.
3. **The verdict contract is normative.** Exit 0 green / 1 red with
   findings / 2 not applicable; `--json` findings arrays; stable
   codes. Existing surfaces grandfathered with named deltas; every
   future pipeline-native check speaks it (extends 0020 rule 4).
4. **The loop protocol is normative.** Single-segment invocations,
   fix exactly what diagnostics name, cap 5, persistent red reports
   and returns control, no retry-to-green, checks and gating
   configs read-only to the looper. Every shipped def instantiates
   it.
5. **Context manifests rule content; the anti-gaming line is
   fixed.** The Developer reads criteria + diagnostics, never
   acceptance-test source (the session-7 finding becomes doctrine);
   the Verifier re-runs every check fresh - a reported green is
   hearsay. Q5's decorrelation mechanism stays open for M0 data.
6. **G4's agent venue is local preflight.** Operators drive the
   same modules the merge gate runs green before push; CI stays
   authoritative and agentless.

## Consequences

- Consumers get operators the day they update the plugin - no
  per-repo prompt forks to reconcile, one implementation per kit
  version.
- Machine-readable commands (`profile.json` `commands:`) keep defs
  stack-independent; a stack binds an inner loop by declaring the
  block, and an absent block reads honestly as no mechanical venue
  yet.
- Agent prompts join the enforcement layer in practice, not only in
  scope: the defs carry their own regression suite (structure,
  chain-free, resolution, coherence) like every class-E artifact;
  the PL-PIPE.3 eval debt stays named on each def until the eval
  arc builds.
- Two registered defs (spec, qa) and the mechanical loop runner
  stay visible deferrals - venue existence, not ambition, triggers
  them.
