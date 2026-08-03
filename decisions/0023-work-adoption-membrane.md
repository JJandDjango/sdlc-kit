# 23. Work adoption: first dotnet consumer behind a one-way membrane

Status: accepted
Date: 2026-08-03

## Context

Post-0.9.0 state: kit tagged and self-pinned, lang door armed in CI
(0022). Activation's named next was the M0 pilot (engine repo) as
first profile-aware consumer. The user re-sequenced: a work C#
environment becomes the first dotnet consumer; M0 runs second and
starts with work findings in hand.

Work facts established in the ratifying conversation: work CI is
GitHub Actions (Azure DevOps variant moot); skill fetch from public
GitHub is proven at work by the Cairn install precedent; Python is
present on the target machine; runner type (GitHub-hosted vs
self-hosted) is unknown pending a probe.

Constraint set: work code never reaches this repo nor the
maintainer's personal Anthropic license. The kit's enforcement
machinery is deterministic local Python - no network calls, no LLM
required - so the outbound direction is safe by construction. The
return direction needs structure; 0022 already named the instrument:
the controlled lexicon is the channel-invariant. Findings expressed
in kit vocabulary, gate IDs, and counts carry no work IP.

## Decision

- **The membrane, as policy.** Kit flows to work by public tag only.
  Findings flow home expressed in controlled-dictionary terms, gate
  IDs, and counts - never code, never identifiers. Work-side code
  contributions stay at work (employer IP); ideas re-implement
  kit-side. Work copies carry a NOTICE naming upstream URL, pinned
  tag, and license.
- **Ratified payload:** (1) dotnet lane proven - the lane itself
  already ships (0018's profile distribution: G3 + G4 surfaces,
  suite-locked); the work consumer adds the end-to-end proof via
  (2), and only what that run flags gets built. (2) Home smoke repo - synthetic dotnet brownfield
  full flow (init -> intake -> contract -> validate -> lang) before
  first work init; first-contact breakage is caught where iteration
  is free. (3) Findings template - the return-channel form; fields
  admit controlled terms, gate IDs, and counts, with "no identifiers,
  no code" on the form; doubles as the Q5 curation intake. (4)
  Membrane policy section in consumer docs, including the uvx line
  for local runs. (5) NOTICE template. (6) Release v0.10.0 carries
  1-5; work pins it. (7) Runner probe - work-side act, no repo
  change.
- **Posture toggles live with the consumer.** The dotnet templates
  ship maximal strictness and choose no XML-documentation or
  localization posture; the 0.10.0 smoke surfaced day-one red on a
  pristine render and the ruling kept the toggle set consumer-side:
  exercised in the consumer-owned enforcement files (merge-target
  class), at adoption time, baseline-not-diff - so the suppression
  audit never reads a posture choice as tampering. The kit's part is
  the documented menu (docs/dotnet-profile.md, day-one posture).
- **Validators stay single-source Python.** Profile lanes are native
  per stack (dotnet now; cargo when ImSim initializes). No ports:
  parallel implementations of gate semantics drift, and gate drift is
  the disease the kit exists to cure. Local convenience is uvx; a
  single-file binary is parked behind a real refusal.
- **Register moves.** Azure DevOps variant: killed (GitHub
  confirmed). dotnet-tool wrapper: parked (Python present).
  Husky.NET: parked. Mirror + configurable KIT_REPO and
  wheel-on-release: parked behind the runner probe. PyPI: unchanged.
- **v1.0.0 line.** Deferred until real consumer findings land; work
  pins v0.10.0, upgrades pull-only via `/sdlc update`.

## Consequences

- The distribution surface gains a membrane: USAGE speaks to
  consumers who are not the maintainer, and the scaffold payload
  gains the findings template and NOTICE.
- The smoke repo becomes the kit-side rehearsal fixture for every
  dotnet-facing change.
- First consumer outside maintainer control exists: version
  discipline hardens to tags-only for work, and every first-contact
  bug found there reproduces at home from a sanitized report - the
  membrane's accepted cost, narrowed by the smoke repo.
- Q5 reality data gains a second feed, pre-sanitized by construction;
  M0 keeps the raw-trace feed.
