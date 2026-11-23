# 43. The herdr tools ship in the kit's opt-in herdr folder

Status: accepted
Date: 2026-11-23

## Context

ADR 0031 made the tree pane's notify command the kit's edge and put the
multiplexer plugin that wraps it outside the kit. The hook,
`herdr_seat.py`, landed in a second repo, `E:\herdr-sdlc` (pane-view,
2026-09-23). session-loop's design put its launcher, `herdr_loop.py`,
beside it (units l2 and l3, sessions 170 to 173).

The second repo cost each unit that touched it. It has no remote, so no
one else can install it and nothing backs it up. CI never runs its tests.
`/sdlc execute` commits only in its own repo, so sessions 170 to 172 ran
the team by hand through a `prove.py` shim. In session 173 the user ruled
the second repo a cost and the fold backlog Next 32, before l4 ships kit
0.23.0.

## Decision

- **One folder, `herdr/`.** `herdr_loop.py`, `herdr_seat.py` and their
  README move into the kit's `herdr/` folder, unchanged but for the paths
  they print. Their tests join the kit's `tests/`, so CI runs them;
  pytest's `pythonpath` names `herdr`.
- **Opt-in.** Nothing runs a herdr tool unless the user names it: the
  tree hook as a repo's `tree: notify:` command, the launcher in a pane
  of the user's own.
- **ADR 0031's line stands.** The kit's core (`taskcontract/`,
  `skills/`, `workflows/`, `hooks/`) imports nothing from `herdr/` and
  runs no herdr command. The tools import nothing from the kit and read
  its files by path.
- **This supersedes ADR 0031 in part.** Its clause "A multiplexer plugin
  wraps that command outside the kit" gives way to this folder. ADR 0031
  stays as written.

## Consequences

- One repo ships the session loop: a consumer gets both tools with the
  kit, at the plugin's folder.
- `/sdlc execute` builds a herdr unit like any other, with no hand run
  and no shim.
- The kit's suite grows by the tools' 109 tests, which fake herdr and
  `gh` and need neither.
- `E:\herdr-sdlc` keeps the tools' history (pane-view, l2 and l3); the
  kit takes a copy, since the scope check would flag each of its commits
  as carrying no `Contract:` trailer.
- No test yet pins the line above; a core file that names herdr is
  caught in review.
