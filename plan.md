# Plan - Session 18 (2026-07-29) - dotnet tooling profile, G0 slice - EXECUTED

Ratified by the user in-session: F1-F9 kept whole. All steps ran:
contract dotnet-profile-g0 ready-green through intake (tooling-profile
ratified at the door, 13/13), overlay container + update parity shipped
(suite 95 -> 106), docs/dotnet-profile.md Pass 0 authored red and
flipped at ship, ADR 0018, kit 0.5.0 (self-run drift named + reconciled,
scaffold-current). PR opened from session-18-dotnet-profile-g0; the
merge is the approval record for the term flip; v0.5.0 tags the merge.

> "C# module" = the kit's **dotnet tooling profile** (registry 0008:
> shapes are language-agnostic; profiles bind them). This session pours
> the profile container and ships the G0 slice; heavy binding content
> starts at the G3 slice (next).

## Steps

1. **Ratify the design** - feature list F1-F9 (in conversation). Strike /
   keep / amend; the kept set scopes everything below.
2. **Intake** - `/sdlc intake` authors `specs/dotnet-profile-g0/contract.yaml`
   to ready-green; declare `entities:`; fork `tooling-profile` as a draft
   vocabulary term if nothing ratified fits (user ratifies, never the loop).
3. **Docs Pass 0** - author `docs/dotnet-profile.md` red-first: binding
   status for all 13 gates (G0 🟡 until shipped, rest 🔴), G0 fit notes,
   registered gaps, roadmap order.
4. **Implement** (@developer): profile-overlay resolution in `init.py`
   (base + `templates/profiles/{stack}/`, unknown stack = base only,
   no-clobber and merge-target semantics preserved) + `update.py` parity
   (stack read from `.sdlc/config.yaml`) + stack-aware next-steps note +
   tests (fixture profile; byte-identical base-payload regression).
5. **ADR 0018** - tooling-profile distribution: in-kit overlay, zero-delta
   G0 finding, promotion rule (project -> profile -> shape), revisit
   trigger (a profile needing independent release cadence).
6. **Verify** (@verifier): suite green, `/sdlc audit` clean, `/sdlc update`
   self-run still exit 0, overlay edge cases (pre-0.5.0 dotnet consumer
   sees no spurious absent rows).
7. **Registry touches** - MAP component row; CHANGELOG delta note;
   KIT_VERSION bump + tag at the shipping merge (tag-on-bump).
8. **Wrap** - docs markers flip, STATE regenerated, commit/PR.

Carried user one-liners (out of scope, unchanged): README.md tree line
and CONVENTIONS.md schema ref still name the old root schemas/ path.

House rules in force: no pipes/chains in any authored command string
(CI steps included); never Edit/Write under ~/.claude/skills (shell
copy only); /sdlc never touches Cairn strata in target repos.
