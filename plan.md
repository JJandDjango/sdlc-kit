# Plan - Session 22 (2026-07-31) - per-gate agent arc: design first - EXECUTED

Ratified by the user in-session: F1-F9 kept whole, knobs as
recommended (developer + verifier ship, spec + qa register; profile
commands kept; verdict retrofit document-only; personas-not-per-gate
ruled in conversation). All steps ran: carried one-liners fixed,
contract operator-layer ready-green through intake (first pass, no
TC loop), docs Pass 0 authored red and flipped at ship, the Two-Key
pair shipped as plugin agents/ (sdlc-developer, sdlc-verifier),
dotnet commands: bindings landed, operator + verdict drafted into
the vocabulary, ADR 0021 recorded, suite 146 -> 158, all four check
surfaces green. Kit 0.8.0; v0.8.0 tag at the shipping merge and the
self-pin PR follow per distribution doctrine.

Original scope statement: STATE next-action 1. The arc is named in
every recent contract ("its own arc") but never designed. This
session designs it - feature list ratified before any
implementation - then ships the first slice if the ratified scope
allows. Pilot M0 (engine repo) stays out of scope unless redirected.

## Steps

1. Carried one-liners (direct fix, no gate ceremony): README.md tree
   line and CONVENTIONS.md schema ref -> `taskcontract/schemas/`;
   delete the empty root `schemas/` leftover.
2. Feature list (WHAT) for the per-gate agent arc - strikeable F-items
   covering: harness (how an agent drives a gate to green from
   diagnostics alone), venue (where each gate-agent runs), verdict
   plumbing (the 0/1/2 + `--json` module contract, suppression-audit
   as precedent), context assembly (two-channel decorrelation),
   plugin `agents/` distribution + versioning. Ratify / strike /
   amend in conversation.
3. Record the ratified set as the design doc.
4. Intake - `/sdlc intake` authors the contract for the first
   implementable slice to ready-green.
5. Docs Pass 0 - red-first for the user-facing surface.
6. Implement (@developer) - the ratified slice + tests.
7. Verify (@verifier) - suite green, `/sdlc audit` clean, self-run
   still exit 0.
8. Registry touches - ADR for the arc's precedents (likely), MAP row,
   CHANGELOG, version bump last, tag-on-bump at the shipping merge.
9. Wrap - docs markers flip, STATE regenerated, commit/PR; self-pin
   follow-up PR after the tag.

House rules in force: no pipes/chains in any authored command string
(CI steps included); never Edit/Write under ~/.claude/skills (shell
copy only); /sdlc never touches Cairn strata in target repos; overlay
templates render from kit truth + date + stack only.
