# 10. Write-surface immutability mechanism

Status: accepted
Date: 2026-07-24

## Context

Q1: what mechanically enforces spec-path immutability - protected dirs +
CI diff, CODEOWNERS, or a separate spec repo? Banked: single protected
root `specs/**` incl. task contracts; ratchet artifacts protected; the
G3 config set shares the machinery. Mechanism, never prompt.

## Decision

1. **Committed write-surface manifest + CI diff audit** per merge
   candidate: merged result vs main-at-queue-time; adds, modifies,
   deletes, renames, mode changes all count; diagnostic = path + class
   + governing channel. CODEOWNERS rejected (approval-shaped,
   platform-bound, Pro-gated); separate repo rejected (breaks G2.5's
   single build; the vendored copy recurses the question).
2. **Allowlist polarity, fail-closed:** the manifest enumerates the
   writable set (reference `src/**`, `tests/unit/**`); everything else
   is protected by default - new artifact classes are born protected.
3. **Channel provenance, never identity:** class S (spec, `specs/**`) -
   deltas only on spec-channel candidates exiting G1/G2 sign-off;
   class E (enforcement layer, incl. the manifest itself) - deltas
   need PL-PIPE.1 approval. Implementation candidates have no bypass.
4. **Anti-vacuity:** manifest absent or empty = FAIL; self-listing.
5. **Trust root, explicit:** the harness (task state, branches, runner)
   is trusted; channels are distinguished, agents not authenticated.

## Consequences

- G4.6 renamed "Write-surface immutability", `specified`; Q1 closes.
- Shared substrate: G4.10's suppression audit rides the same diff job;
  PL-PIPE.1 gains its mechanical arm.
- Baselines relocate to `specs/baselines/` (AdditionalFiles wiring);
  build item: the write-surface audit job (0008 register).
- Q7 worked example: direction-conditional channel weight (G4.8/G9
  tightenings auto-approve; loosenings take the full second channel).
