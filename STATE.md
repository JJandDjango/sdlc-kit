# State - sdlc_development_kit

> **Contract** - one question: *what is in flight right now?*
> <=1 page - regenerate at every session end - disposable, always safe to overwrite.
> _Generated 2026-07-27._

## Now
- Session 14 (2026-07-27): **the pilot exists - Q6 is answered.** ImSimEngine
  (`E:/ImSimProject/engine`, nested repo of the Kallipolis worldbuilding home)
  was initialized in its own session via `/cairn` + `/sdlc` and took its
  first task (M0: window + Vulkan cleared frame, ash + winit) through
  `/sdlc intake` to ready-green on day one - G0.1 reads `enforced` there.
  Parent-side pivot recorded in ImSimProject (its ADR 0003: S&Box retired,
  Rust+Vulkan ground-up engine as the game-code home).
- **Round 1 of the feedback loop closed**: the pilot filed five friction
  items (engine repo `PILOT-NOTES.md`); all five fixed on branch
  `pilot-fixes-r1` - install id documented as `sdlc@sdlc-kit`, one-channel
  guidance, `material` -> `adoption` axis rename (lockstep with cairn's
  paired `pilot-fixes-r1` branch - its Q3 carried the same word), validator
  prints `<profile>-green: <path>`, invocation-supplied answers blessed as
  interview-equivalent. Suites: kit 34, cairn 213 green. Engine consumer
  synced (`adoption:` key; kit-source audit reads it clean). Marketplace
  install path verified live by the pilot (friction item 1 was its finding).
- **New roadmap direction (user)**: one or more **LLM review agents per
  gate** - the substance key beside each mechanical form check - shipped
  through the kit plugin channel (`agents/` in the plugin payload; consumers
  get them on plugin update). Design input = the pilot's per-gate
  observations; the first (G0: slot, judgments, context, output shape) is
  logged in engine `PILOT-NOTES.md`.
- Coworker-facing explainer PDF (6pp: gates tour, contract, principles,
  roadmap) generated from THEORY/gates.md/USAGE - scratchpad artifact,
  uncommitted; offer stands to land it in `docs/`.
- Observation routed to the foundations arc: the PromptLang write-time hook
  resolves `prompt-lang.config.yaml` from session cwd, so cross-repo edits
  validate against the wrong tag set (false positives on cairn's three
  section tags from a kit-cwd session; cairn's batch gate is authoritative).

## Blockers
- None. (Two PRs await the user's merge click - not blocked, just gated.)

## Next actions
1. **Merge the two PRs** (`pilot-fixes-r1` -> main in sdlc-kit and cairn;
   mains are PR-only). Then: delete `~/.claude/skills/sdlc` (one-channel),
   update the plugin, re-run engine audit (clears the transient where stale
   audit copies expect `material`).
2. **Pilot continues**: next engine session implements M0 through the gates
   (fresh Developer context - Q5 reality data); its gate-passage notes keep
   feeding the per-gate agent design.
3. **Per-gate agent design**: shape the first agent (G0 contract review has
   its design input already) + the plugin `agents/` distribution shape.
4. Activation build items land into the skill payload as built (0015
   inventory); Q4 numbers when the pilot gives reality (clocks.yaml +
   per-gate constants).
5. Distribution follow-ups when wanted: PyPI publish; explainer PDF into
   `docs/` if the user wants it versioned.

## Open questions
- Q4 thresholds, numeric only - shapes closed program-wide.
- Q5 two-channel decorrelation (harness design); named sub-question: the
  Developer's context contents. The M0 implementation session is the first
  live data point.
- **Per-gate agent shape** (new): venue per gate, context assembly, verdict
  format (PASS/annotations, never edits), and how agents version inside the
  plugin - first design input on record at the pilot.

(Q6 answered this session - the pilot is ImSimEngine; the stream framing
holds: every further `/sdlc`-initialized repo adds reality data.)
