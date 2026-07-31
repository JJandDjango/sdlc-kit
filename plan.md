# Plan - Session 21 (2026-07-30) - dotnet tooling profile, G4 mechanical core slice - EXECUTED

Ratified by the user in-session: F1-F10 kept whole, rulings as
recommended (F3 docker-run gitleaks, F6 battery-CWE re-registration,
F10 ADR 0020 kept). All steps ran: session-20 close merged first
(PR #17), contract dotnet-profile-g4 ready-green through intake
(first pass, no TC loop), docs Pass 0 authored red and flipped at
ship, four conditions bound (G4.1, G4.9.1-2, G4.10, G4.11), the
suppression audit shipped as the first pipeline-native kit module,
suite 111 -> 146, both audit engines clean, kit 0.7.0. PR #18 merged
(819686b) and v0.7.0 tagged there; self-pin PR #19 merged (eb881dc),
its contracts job proving pip install @v0.7.0.

Original scope statement: roadmap step 3 (docs/dotnet-profile.md) -
the merge gate's mechanical core in the dotnet overlay; gate shape
ratified at docs/gates/G4-pre-merge-ci.md; seven conditions stay 🔴
per roadmap step 4.

## Feature list (WHAT - strike / keep / amend)

- **F1 Merge-gate workflow extension** - sdlc-dotnet.yml (kit-owned)
  grows from inner-loop echo to the mechanical core: `merge_group`
  trigger added (queue-authoritative venue; `pull_request` stays as
  advisory preview building the test-merge ref), the existing three
  steps stand as G4.1's echo clauses (build / battery / formatter),
  new steps per F2-F5; header re-scoped; every step chain-free;
  consumer workflows untouched.
- **F2 Full test execution (G4.11)** - `dotnet test` solution-wide
  after the strict build (`--no-build`); zero-tests-discovered = FAIL
  guard (mechanism ruled at developer phase); skip/quarantine policy =
  enforcement-pass material, named line in docs.
- **F3 Secrets clause (G4.9 clause 1)** - gitleaks diff-mode step over
  base..head; masked diagnostics, rotation-first fit note. Binding
  ruled at intake - recommendation: `docker run` of the MIT gitleaks
  image (single chain-free segment, no org license wall) over
  gitleaks-action.
- **F4 Dependency clause (G4.9 clause 2 + locked graph)** -
  Directory.Build.props (merge-target) gains the audit block
  (`RestorePackagesWithLockFile`, `NuGetAuditMode` all, NU1901-1904 as
  errors); workflow restore goes `--locked-mode`; brownfield lockfile
  story in fit notes (absent lockfile = red, adoption pace with the
  consumer). License allowlist + SLA backstop (clause 3) deferred with
  named lines - the first needs the policy artifact, the second G9.2
  tracking.
- **F5 Suppression audit (G4.10)** - the doc-promised build item: new
  `taskcontract` subcommand implementing the four-vector diff check
  (in-source suppressions incl. Skip/Ignore forms; severity
  downgrades; strictness-flag weakening; exclusion widening) over
  base..head with the .NET construct lists; workflow step installs the
  pinned kit and runs it (per-event base resolution inside the
  subcommand, so steps stay dumb and chain-free); per-vector
  diagnostics naming the legitimate channel.
- **F6 Battery-CWE map disposition** - the fourth banked input (three
  strata substantiating taxonomy 691/697/703 rows + golden test).
  Recommendation: re-register (Husky.NET precedent) behind "first
  scanner slice (G4.7) or next taxonomy session" - data-audit work
  orthogonal to the overlay payload; keeping it would dilute the
  shipping slice.
- **F7 Docs** - dotnet-profile.md G4 fit-notes section, Pass-0
  red-first: venue semantics (queue-ready via `merge_group`,
  queue-less fallback = strict serial merges), brownfield lockfile
  story, the G3 "review-blocking by policy" line flips to the live
  audit, deferral register (license allowlist, SLA backstop, seven
  remaining conditions). Binding-table G4 row flips at ship to
  green-core with honest remainder marking.
- **F8 Tests** - content assertions for the new workflow steps + props
  audit block; suppression-audit fixture corpus (positive + negative
  per vector); chain-free check extended over new steps; non-dotnet
  byte-identical regression holds; version equality at 0.7.0;
  profile-authoring lock holds over template edits.
- **F9 Registry + version** - 0.7.0 (KIT_VERSION + pyproject
  together), CHANGELOG delta note, MAP row touch, tag-on-bump at the
  shipping merge, self-pin follow-up PR per distribution doctrine.
- **F10 ADR 0020** - merge-gate distribution shape as precedent: one
  workflow serving both venues (PR advisory / queue authoritative),
  and pipeline-native checks shipping as kit modules behind the pin,
  never copied scripts. Strikeable if the contract record suffices;
  lean keep - it generalizes to every future profile's G4 slice.

## Steps (scoped by the kept set)

1. Ratify F1-F10 (in conversation).
2. Intake - /sdlc intake authors specs/dotnet-profile-g4/contract.yaml
   to ready-green; F3's binding and F6's disposition ruled in-contract.
3. Docs Pass 0 - F7 red-first.
4. Implement (@developer) - F1-F5: workflow + props deltas,
   taskcontract subcommand, tests (F8).
5. ADR 0020 (F10, if kept).
6. Verify (@verifier) - suite green, /sdlc audit clean, self-run still
   exit 0, byte-identical regression green.
7. Registry touches (F9) - version bump last, tag-on-bump at merge.
8. Wrap - docs markers flip, STATE regenerated, commit/PR; self-pin PR
   after the tag.

House rules in force: no pipes/chains in any authored command string
(CI steps included); never Edit/Write under ~/.claude/skills (shell
copy only); /sdlc never touches Cairn strata in target repos; overlay
templates render from kit truth + date + stack only.
