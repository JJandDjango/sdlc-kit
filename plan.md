# Plan - Session 20 (2026-07-30) - dotnet tooling profile, G3 slice - EXECUTED

Ratified by the user in-session: F1-F9 kept whole. All steps ran:
contract dotnet-profile-g3 ready-green through intake (first pass, no
TC loop), docs Pass 0 authored red and flipped at ship, four overlay
surfaces + manifest landed (classes per ADR 0019), suite 106 -> 111,
audit clean, kit 0.6.0. Self-run drift = the known self-pin lag; the
self-pin PR follows the v0.6.0 tag per distribution doctrine.
Remaining: commit/PR, tag at merge, self-pin follow-up. Session 19 was harness-side, kit unchanged at 0.5.0.
The G3 slice is the dotnet overlay's first real payload (roadmap step 2,
docs/dotnet-profile.md); gate shape ratified at docs/gates/G3-implementation.md.

## Feature list (WHAT - strike / keep / amend)

- **F1 Directory.Build.props overlay surface** - G3.3's five ratified
  flags (Nullable enable, TreatWarningsAsErrors, AnalysisLevel
  latest-all, CheckForOverflowUnderflow, AllowUnsafeBlocks off) plus
  G3.2 wiring: EnforceCodeStyleInBuild, StyleCop.Analyzers package ref.
- **F2 .editorconfig overlay surface** - G3.1 layout rules + G3.2
  severity map, single-sourced for local build and future G4 echo.
- **F3 Inner-loop CI workflow** (.github/workflows/sdlc-dotnet.yml) -
  format verify + strict build as chain-free steps, beside the G0
  backstop workflow, consumer's own .NET workflow untouched.
- **F4 Drift-class ruling** (the STATE sub-question, decided at
  intake): recommend merge-target for .editorconfig and
  Directory.Build.props (consumers legitimately extend both),
  kit-owned for the workflow file.
- **F5 Local hooks** - overlay-replace the base pre-commit config to
  add the formatter hook; re-register Husky.NET behind a new trigger
  ("a consumer without Python tolerance") - its old trigger names this
  slice, so the gap must close or re-register honestly.
- **F6 Docs** - dotnet-profile.md G3 fit notes, Pass 0 red-first;
  G3 row flips green at ship; gap register updated (F5's re-trigger).
- **F7 Tests** - render, classification, and content assertions for
  the new surfaces; non-dotnet byte-identical regression holds; locked
  profile-authoring rule holds (kit truth + date + stack only).
- **F8 Registry + version** - 0.6.0 (KIT_VERSION + pyproject
  together), CHANGELOG delta note, MAP row touch, tag-on-bump at the
  shipping merge, self-pin follow-up PR per distribution doctrine.
- **F9 ADR 0019** - enforcement-config drift-class precedent
  (generalizes to every future profile's G3 slice). Optional - strike
  if the contract record suffices.

## Steps (scoped by the kept set)

1. Ratify F1-F9 (in conversation).
2. Intake - /sdlc intake authors specs/dotnet-profile-g3/contract.yaml
   to ready-green; entities joined; F4's ruling recorded in-contract.
3. Docs Pass 0 - F6 red-first.
4. Implement (@developer) - F1-F3 + F5 surfaces, profile.json manifest
   entries, tests (F7).
5. ADR 0019 (F9, if kept).
6. Verify (@verifier) - suite green, /sdlc audit clean, self-run still
   exit 0, byte-identical regression green.
7. Registry touches (F8) - version bump last, tag-on-bump at merge.
8. Wrap - docs markers flip, STATE regenerated, commit/PR; self-pin PR
   after the tag.

House rules in force: no pipes/chains in any authored command string
(CI steps included); never Edit/Write under ~/.claude/skills (shell
copy only); /sdlc never touches Cairn strata in target repos; overlay
templates render from kit truth + date + stack only.
