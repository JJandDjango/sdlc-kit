| Revision Date | Revised By | Changes Made |
| :-: | :-: | :-- |
| 2026-11-24 | Johnathan Hyden | r1: Created through /sdlc:product-specification-interview. The request half, in progress. PO seat: Johnathan Hyden |

# session-loop-sidebar - Each loop's state shows in herdr's sidebar

`sdlc_development_kit` · seat: PO Johnathan Hyden · contract: `session-loop-sidebar`, draft · PR: none · merge SHA: none

## Statement

`[PO seat · authored]`

As the developer running session loops, I want each loop's position, strike count and waiting state in herdr's sidebar, so that I can tell which loop needs me without opening its pane.

## Description

`[PO seat · authored]`

Each pane a launcher watches shows, on its own sidebar entry, the position of its last wrap (plan step and task), its strike count (0 or 1; the second strike stops the loop), and whether a stop waits on the user, with the minutes left before the 55-minute self-wrap. When the launcher stops the loop, the entry says why until the loop is turned on again.

## Background

`[PO seat · authored]`

Session 164 split this from session-loop's SC6 as display work, and 0.23.0 shipped without it. Today a loop's state is spread across `loop.json`, `waiting.json`, the launcher's memory and the launcher pane's output; none of it is visible at a glance. 0.23.0 (2026-11-24) puts loops in daily use, so the gap is now felt each time a loop runs.

### Existing behavior touched

- The launcher holds the last position and the strike count in memory only, and stops the loop at two strikes. (`herdr/herdr_loop.py:185-209`)
- A human-needed stop is waiting while `waiting.json` exists; it holds the stop's issue and the 55-minute timer's due time. (`docs/features/session-loop.design.md:71`)
- The seat hook flags the tree pane in herdr's sidebar as agent `sdlc`, state `blocked`. (`herdr/README.md:55`)
- At its own stops the launcher files one `needs-ruling` issue, shows a toast, removes `loop.json` and exits 1. (`docs/features/session-loop.design.md:97`)

## Success criteria

`[PO seat · authored]`

- SC1: Within 10 seconds of a restart, the pane's sidebar entry shows the new position and strike count.
- SC2: While a stop waits, the pane's sidebar entry shows the minutes left before the self-wrap, never more than one minute stale, and the entry clears within one minute of your reply.
- SC3: When the loop stops on its own (two strikes, the session exited, no change for 60 minutes, a self-wrap, or an empty Next), the pane's sidebar entry shows which of those five ended it, until the loop is turned on again.
- SC4: Within 10 seconds of `/sdlc loop off`, the pane's sidebar entry shows nothing from the loop.

## Non-goals

`[PO seat · authored]`

- No new authorizations are added.
- No actions from the sidebar: the entry cannot reply, restart or turn the loop off; it only displays.
- No history: the entry shows the current state only, never past positions or past stops.
- No new notice: the sidebar adds no toast or sound beyond what session-loop already sends.

## Prerequisites

`[PO seat · authored]`

- session-loop, kit 0.23.0: exists.
- herdr on the machine, at least 0.9.5 (the launcher's measured version, session 171): exists.
- A row in the user's herdr config (`[ui.sidebar.agents] rows`) that shows the loop's tokens: does not exist yet. The design names the line and `herdr/README.md` tells the user to add it, since the kit never writes the user's herdr config.

## Acceptance criteria

`[PO seat · authored]`

### Checks

- SC1.1: verify that after a `continue` sentinel at a new position, the pane's entry shows that position and strike count 0 within 10 seconds of the restart.
- SC1.2: verify that after a session ends at the position it started from, the entry shows strike count 1 within 10 seconds of the restart.
- SC1.3: verify that the seat hook's `sdlc` `blocked` flag on the tree pane still shows while a loop pane's entry shows its state.
- SC2.1: verify that while `waiting.json` exists, in the form 0.23.0 writes it, the entry shows the whole minutes left before its due time, never more than one minute behind the clock.
- SC2.2: verify that within one minute of the reply removing `waiting.json`, the entry no longer shows the waiting state.
- SC3.1: verify that after each of the launcher's three stops (two strikes, the session exited, no change for 60 minutes), the launcher still files its one `needs-ruling` issue, shows its toast, removes `loop.json` and exits 1, and the entry shows that stop's reason, still after the launcher exits.
- SC3.2: verify that a `self-wrap` sentinel and a `pick` sentinel (empty Next) each leave the entry showing their own reason.
- SC3.3: verify that once the loop is on again and a launcher starts on the pane, the entry no longer shows the old reason.
- SC4.1: verify that within 10 seconds of `/sdlc loop off` removing `loop.json`, the entry shows none of the loop's state (position, strikes, waiting, reason).
- SC4.2: verify that turning the loop off while a stop waits clears the waiting state too, within the same 10 seconds.

### Error messages, verbatim

- SC3.1: `stopped: two strikes`
- SC3.1: `stopped: session exited`
- SC3.1: `stopped: no change 60m`
- SC3.2: `stopped: self-wrap`
- SC3.2: `stopped: Next empty`

## Decisions and open questions

`[PO seat · authored]`

1. Decided (session 164): the herdr sidebar (each loop's position, strike count and waiting state) is a feature of its own, split from session-loop's SC6.
2. Decided (ADR 0043): herdr code lives in the kit's opt-in `herdr/` folder; the kit's core imports nothing from herdr and runs no herdr command.

## Notes

`[PO seat · authored]`

- herdr 0.9.1 (measured 2026-09-21 and 2026-09-23): `herdr pane report-metadata <pane> --source ID --token name=value` shows as `$name` in `[ui.sidebar.agents] rows`; `herdr pane report-agent --state blocked` never changes a Claude pane.
- Open for the design run: whether a token row shows on a Claude pane's sidebar entry.

## Appendix

### Gherkin

`[PO seat · derived]`

(none: the Gherkin step writes one scenario per check)

### Terms

`[PO seat · authored]`

- **sidebar entry**: a pane's row in herdr's sidebar, where the loop's state shows beside the pane's name.
- **waiting state**: a human-needed stop is open (`waiting.json` exists) until the reply or the self-wrap.
- **stop reason**: the short text an entry shows after the loop stops on its own, naming which of the five ends it was.
