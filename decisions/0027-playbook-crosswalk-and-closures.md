# 27. The AI-native SDLC playbook: crosswalk and six closures

Status: accepted
Date: 2026-09-08

## Context

Anthropic's playbook (Claxton, claude.com, 2026-08-21) is the
vocabulary the pitch meets: intent.md (originator writes, PO accepts
by merge) -> spec.md (agent writes, PO accepts) -> plan.md (files,
order, proving tests; the implementing engineer approves; committed)
-> diff and tests -> PR under REVIEW.md passes -> control bands in
production writing the next intent. "Every stage commits an artifact
the next stage can read." Session 29 mapped it play by play against
the 56 conditions: every play is covered, most by a stronger
condition. Crosswalk: intent.md is the feature document (0026);
spec.md is the contract's form, validated at G0 rather than reviewed;
plan.md is the unit graph, computed from `decomposition` and
`depends_on` (0024); REVIEW.md is the advisory pass below; control
bands are G8, whose escapes write the next request (`g8-escape`). The
plan's three questions, which files change, in what order, which
tests prove it, are `scope`, `depends_on`, and `acceptance_sketch`,
asked of the engineer seat.

Alternatives weighed, the playbook's four disagreements, each
rejected:

1. A mutable plan, updated in the diff's commit, drift measured as
   rework count. The contract freezes at ready (0010) and a change
   re-intakes; rework becomes a metric, not a licence to edit.
2. Advisory templates with an LLM compliance pass as the guard. The
   playbook's own rule decides it: "a policy that must always hold
   needs something deterministic behind the skill." G0 validates and
   G4 joins; the LLM pass is kept, advisory only.
3. A committed plan.md. The unit graph derives from the contract, so
   plan and spec cannot drift apart (0024).
4. Tests and code generated together for features, decorrelated only
   for bug fixes. The kit decorrelates always (THEORY; G3 is the
   implementer's only write surface).

## Decision

Six gaps close, in two contracts. `playbook-guardrails` (kit 0.13.0,
before the pitch): (1) session hooks deny writes to ready contracts
and ratified terms, the playbook's fix-task hook generalized to the
spec channel, rendered by `/sdlc init` and tracked by `/sdlc update`;
(2) G4.12, the diff stays within its contract's `scope`, bound to the
contract by a `Contract:` commit trailer unless intake A rules
otherwise; (6a) `.sdlc/REVIEW.md` names the advisory review pass in
USAGE. `playbook-loop` (0.14.0, after the demo intake): (3) G9.5, a
scheduled re-scan of unchanged first-party code under current rules,
with dated coverage; (4) flow metrics computed from git by
`taskcontract metrics`: time-to-ready, rework count (re-intakes after
ready, its threshold a clock in `clocks.yaml`), first-pass merge,
in-scope rate, the final set fixed at intake B; (5) a PO venue with no
engineer at the prompt, and resuming a parked contract when the
answer lands; (6b) a G8.3 disposition gains `eval_ref`, so an escape
adds an agent eval. The registry grows 56 to 58 under 0014's full
lane: both new conditions are mechanical, the direction is
tightening, the principal approves, the merge is the record.

## Consequences

- The pitch speaks the playbook's words with a cited crosswalk, and
  "why not just follow the playbook" has an answer on record.
- The human census stays six (0015).
- Open at intake A: whether gap 1 denies class-E paths outright or
  warns until PL-PIPE.1's approval record exists. Open at intake B:
  the re-scan cadence (clocks, Q4) and the metric set.
- Two intakes, two releases, both self-pinned; the one outside
  consumer at v0.10.0 is undisturbed.
