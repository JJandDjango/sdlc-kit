# Plan - Session 25 (2026-08-03) - work-adoption payload (ADR 0023) - EXECUTED (step 9 carries to the work machine)

Work C# environment becomes the first dotnet consumer behind a
one-way membrane; M0 runs second with work findings in hand. This
session builds the payload the work repo will pin: dotnet lane,
return-channel form, membrane docs, v0.10.0.

## Steps

1. ~~ADR 0023~~ - design recorded (decisions/0023).
2. ~~Docs pass 0~~ - USAGE §7 "Restricted environments - the
   one-way membrane": policy 🟢, findings form + NOTICE 🔴 (ship
   0.10.0), uv run line for local checks.
3. ~~Findings template~~ - `.sdlc/findings/TEMPLATE.yaml`, kit-owned
   surface; membrane rule on the form; suite 189.
4. ~~NOTICE~~ - `.sdlc/NOTICE.md` rendered by every init (kit-owned);
   mirror guidance in USAGE §7; suite 190.
5. ~~Dotnet lane~~ - already shipped (ADR 0018: G3+G4 overlay,
   suite-locked; found at step 3). Step 6 is the proof.
6. ~~Smoke~~ - brownfield + greenfield scratch repos: 12-surface
   render, pure no-clobber, contract ready-green, vocab/lang/audit
   green, update scan honest. Build red on pristine code = the
   posture decision surfacing; ruled consumer-side (ADR 0023),
   documented as the day-one posture menu in docs/dotnet-profile.md.
   Kit templates unchanged; suite stands 190.
7. ~~Bump 0.10.0~~ - 9b28084, PR #29, both checks green (contracts
   12s, test 13s); merged at e7421e8, sync + branch cleanup done.
8. ~~Tag v0.10.0 + self-pin~~ - annotated at e7421e8, pushed;
   d29e060, PR #30, both checks green (contracts 16s proved the tag
   install); merged at d4ce337; CHANGELOG 0.10.0 entry + USAGE uv
   line joined the sweep.
9. User acts at work: runner probe (GitHub-hosted vs self-hosted;
   scratch pip-step run if self-hosted); install skill; init the
   work repo pinned to v0.10.0; NOTICE lands in the copy.

Next: M0 (second consumer) starts from work findings; cargo lane
waits on ImSim initialization.

House rules in force: no pipes/chains in any authored command string
(CI steps included); commit messages via Write + git commit -F.
