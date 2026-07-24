# 9. Custom-analyzer adoption policy

Status: accepted
Date: 2026-07-24

## Context

Q3 - which house conventions become custom analyzers first - is G3.2's
open parameter; STATE rider: does extraction generate stubs? Couples to
the conventions-enforcer arc in `E:\claude-orchestrator`
(`designs/conventions-skill.md`: E1-E5 seed list; extract -> ratify ->
compile, advisory -> gating). A named list today is speculation - no
pilot (Q6), no populated stratum, and the kit selects against the actual
defect distribution. The policy, not the list, is decidable now.

## Decision

1. **Source of truth:** house conventions reach the battery only via the
   ratified conventions registry, on the enforcer arc's discipline -
   never directly from taste, human or agent.
2. **Selection function** (replaces the list): at pilot activation, rank
   by evidence frequency x review cost, auto-fixability, and ladder lift;
   first tranche 3-5 to prove the loop.
3. **Pipeline-native tier, independent of Q3:** sunset-escalation analyzer
   (G10.1) + suppression audit - kit build items per
   [0008](0008-two-layer-condition-model.md), first in construction order.
4. **Stub generation, bounded:** declaratively expressible rules compile
   fully (config, Semgrep, arch-test); semantic rules get stubs with the
   core + code-fix authored. **Fixture-before-gating:** no rule gates
   without its violating/conforming corpus green (PL-PIPE.2 at the rule
   layer). Advisory -> gating never skipped.
5. **Boundary:** extraction infrastructure (E1-E5) stays enforcer-arc;
   the kit consumes ratified entries and compiled packs.

## Consequences

- G3.2 -> `specified`, Q3 closed; Open column "[0009]; tranche at Q6";
  severity map + first-tranche contents ride Q6.
- Accepted risk: enforcer-arc stall starves the house tier - mitigated by
  the independent pipeline-native tier and hand-ratified entries.
