# 1. Record architecture decisions

Status: accepted
Date: 2026-07-22

## Context
sdlc_development_kit needs a durable record of *why* it is built the way it is - not
just *what* was built. A future session (human or LLM) picking this up cold should
be able to learn the reasoning behind a choice without reverse-engineering it.

## Decision
We will keep Architecture Decision Records (ADRs), per Michael Nygard's
convention. Each significant decision gets one numbered file in `decisions/`.

## Consequences
- **Append-only.** An ADR is never edited. A decision that changes gets a NEW
  record; the old one is marked `Status: superseded by NNNN`. Each record stays
  true about what was believed at the time - zero maintenance cost.
- **Significance test.** Write an ADR when a future session would plausibly ask
  "why is it done this way?" - otherwise skip it.
- **Half a page max.** Longer means it is a design doc, not a decision record;
  link out to the design doc and keep the ADR to the decision itself.
