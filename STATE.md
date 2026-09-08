# State - sdlc_development_kit

> **Contract** - one question: *what is in flight right now?*
> <=1 page - regenerate at every session end - disposable, always safe to overwrite.
> _Generated 2026-09-08 (session 28 close, home machine)._

## Now
- v0.12.0 is released; the release's last act is still open. PR #37
  (self-pin) is OPEN with checks green at e2b5a6a (2026-08-26). The
  session-27 STATE regeneration cc29aa5 (2026-08-31) was never pushed:
  the remote branch stops at e2b5a6a, origin/main at 8fbaa7f, tag
  v0.12.0 at 8fbaa7f (verified 2026-09-07). One push re-runs the checks.
- Session 28 (2026-09-07 to 2026-09-08) was a conversation, no code:
  branch `session-28-g0-pitch` off cc29aa5 carries only
  NOTES_g0-pitch_2026-09-08.md and this regeneration. The user is
  pitching the kit to a consumer with a PO team and engineers whose
  venue is a feature document (Google Doc: authors, request, business
  use case, prerequisites, technical details, Gherkin, Q&A; a feature
  or a bug fix). Ruled in chat, unratified, recorded in the notes: the
  kit adheres to the SDLC as V-model stage gates; G0 has zero human
  conditions and is where the humans are in the room; the document is
  the raw request and the contract is what intake produces from it
  (worth and design stay in the document, form and entry in the
  contract); unit tests never enter the document (G3 write surface);
  three template changes (Not in scope, Gherkin grouped by unit, Terms).
- Pitch risks named: immutability is a design claim (G4.6 unbuilt;
  0010 rejected CODEOWNERS); G1 is paper (Gherkin to `criteria.yaml` by
  hand); no business fields by design (`provenance.ref` links out).
- Receipts unchanged from 27 (suite 222; validate 10/10; vocab 18
  terms; lang-check 0; prompt_lang 8/8). Cairn audit 0 errors, 21
  warnings, all pre-existing (ADR budgets; four docs pages stale since
  the 2026-08-26 `confirmed_by` stamp of their covered contracts).
- Untracked REQUEST_unit-dag_2026-08-22.md is an inbox item kept
  untracked by the kit rules; unit-dag closed 8/8, so it is served.
  plan.md is session 27's; refresh when 29 picks its thrust.

## Blockers
- None. `/sdlc audit` here still reports TC005 on `id` and
  `confirmed_by`: the pip install is pinned at e81f9a5. Fix:
  `pip install -e E:\sdlc_development_kit`. Not a finding against the
  code.

## Next actions
1. **Session 29 opener (user's ask):** review a YouTube video on this
   topic (spec-first intake, agent-driven SDLC, PO/engineer contracting)
   to check the direction: `/discover-youtube-videos` to find one, or
   `/review-youtube-video <url>` with one in hand. Ratify or amend the
   session-28 notes after it.
2. Push cc29aa5, wait for green, merge PR #37, sync main, delete the
   branch; then PR `session-28-g0-pitch`.
3. **Demo intake:** one real feature document through `/sdlc intake`
   (paste or Drive link), contract drafted as the pitch artifact. On
   ratification the notes graduate to a USAGE section beside section 8
   and a candidate ADR (the document as raw request; the mapping; unit
   tests out).
4. **Work-side upgrade** (work machine): `/plugin marketplace update
   sdlc-kit`, `/plugin update`, re-pin to v0.12.0; id migration first
   (TC001 until every unit carries an `id`), `/sdlc vocab extract`, PO
   seat ratifies domain terms and engineer seat technical ones, ratify
   `intake-seat` with `[po, engineer]`, stamp `confirmed_by` in the same
   commit.
5. **G1 slice:** `criteria.yaml` + `[Criterion]` + the G4.3 join (0011,
   designed, unbuilt). New input from 28: Gherkin as the human authoring
   format for criteria (one scenario = one criterion, tag = REQ-ID).
   ApplyDiscount stays the first fixture; `graph --labels` and
   `graph --done` banked.
6. **Prompt lexicon arc** (later): 395 of 1990 checkable words unknown
   (20%, 2026-08-26); decision first, never a tidy-up.
7. Runner probe at work; M0 pilot; continuations unchanged (PL-PIPE.3
   eval harness, sdlc-spec / sdlc-qa defs, loop runner, verdict
   field-name convergence, `.sdlc/progress/<id>.yaml`, direction
   classifier).

## Open questions
- Does the session-28 mapping hold after the video check? If yes: USAGE
  section or ADR first?
- Order of the next two arcs: G1 slice or prompt lexicon. Recommend G1
  first; the Gherkin input makes it more concrete.
- Q4 thresholds, Q5 decorrelation, Q6 first analyzer tranche,
  comprehension empirics (PL-PIPE.3): unchanged from 25.
