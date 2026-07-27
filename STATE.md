# State - sdlc_development_kit

> **Contract** - one question: *what is in flight right now?*
> <=1 page - regenerate at every session end - disposable, always safe to overwrite.
> _Generated 2026-07-26._

## Now
<!-- What's actively being worked. -->
- Session 13 (2026-07-26): the kit became distributable, Cairn-style
  ([0016](decisions/0016-distribution-before-activation.md) -
  distribution before activation). The `/sdlc` skill shipped:
  `init` (interview + no-clobber payload: SDLC.md status page,
  `.sdlc/` config + clocks + reds seeds, protected `specs/` root, CI
  validate workflow, F8/F12 merge-target snippets - printed, never
  merged, when they exist), `intake` (F10 - the G0 venue), `new`
  (F11 as `python -m taskcontract new` - the skeleton is born red,
  TC007 the tripwire, so a fresh contract can never pass vacuously),
  `audit` (report-only, exit 0/1/2, parked drafts read INFO). Suite
  20 -> 34 green; SKILL.md PromptLang-clean; consumer surfaces
  authored (README + USAGE + LICENSE + marketplace.json); package
  0.2.0.
- **Published**: repo renamed `JJandDjango/sdlc-kit` and flipped
  public; the tracked protect-main ruleset applied (id 19781346) -
  the standing blocker dissolved, and its first live catch was this
  session's own push (main is PR-only now). Skill installed to
  `~/.claude/skills/sdlc`; greenfield + brownfield smoke green
  (no-clobber proven against sentinels).
- Q6 reframed, not answered: the pilot is *the first repo
  initialized via `/sdlc`*; G0.1 flips `enforced` per-target at
  first live intake there.

## Blockers
<!-- What's stopping progress. -->
- None. (Protect-main resolved this session - public repos carry
  rulesets free.)

## Next actions
<!-- The ordered next steps. -->
1. Pilot a real repo: `/cairn` then `/sdlc` (greenfield or
   brownfield), first task through `/sdlc intake` - G0.1 reads
   `enforced` there and that repo becomes the Q6 pilot.
2. Activation build items land *into the skill payload* as they are
   built (the 0015 inventory: trace-validation harness, G7.1
   bootstrap capture, G9.4 tightening job, G10.1 analyzer, G10.2
   reachability, sweeps + bot, samples project, docs-build job,
   staleness ledger + context hook, direction classifier + approval
   ledger, goldens, evals, `reds.yaml` consumers).
3. Q4 numbers when the pilot gives reality (one clocks.yaml edit +
   per-gate constants); Q5 harness design (Developer-context
   sub-question).
4. Distribution follow-ups when wanted: PyPI publish; verify the
   marketplace install path from a second session
   (`/plugin marketplace add JJandDjango/sdlc-kit`).

## Open questions
<!-- Unresolved decisions that need an answer. -->
- Q4 thresholds, numeric only - shapes closed program-wide.
- Q5 two-channel decorrelation (harness design); named sub-question:
  what the Developer's context contains.
- Q6 pilot - now a stream, not a selection: which repo gets
  initialized first, and does it carry real build intent?

(Protect-main resolved this session; Q7 resolved S12 -> [0014](decisions/0014-enforcement-change-control.md).)
