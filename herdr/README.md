# herdr

The SDLC kit's two herdr tools, opt-in: nothing runs them unless you name
them, and the kit's core imports nothing from this folder (ADR 0043). They
lived in a second repo, `E:\herdr-sdlc`, until session 174; its history
stays there. `{kit}` below is the kit's folder: a clone, or the plugin's
install.

`herdr_seat.py` is the hook for the kit's
tree pane: when `python -m taskcontract tree --follow` arrives at an
approval, the kit runs its `tree: notify:` command; this hook is that
command. It flags the seat in herdr's sidebar, shows a toast, and clears
the flag once the seat is answered. `herdr_loop.py` is the session loop's
launcher (below).

Status: 🔴 not built, 🟡 built, not verified, 🟢 verified (Two-Key PASS).

## The session loop's launcher

`herdr_loop.py` restarts a Claude session in its herdr pane each time the
session wraps, until the user is needed. The kit's `/sdlc loop on` turns a
repo's loop on, and the session writes the loop's files under `{git
folder}/sdlc-loop/` (the kit's `workflows/tools/loop.py`). Start the
launcher in a pane of your own, naming the Claude pane:

    python {kit}\herdr\herdr_loop.py w9:p1

Features (the kit's session-loop contract, units l2 and l3):

1. 🟢 **Restart** (l2). Within 60 seconds of a `continue` sentinel, the
   launcher waits until the pane reads idle or done (herdr's two ready
   states), types `/clear` and Enter, then 3 seconds later
   `/resume-session` and Enter, and prints
   `herdr-loop: restarted pane {pane} at {position}`.
2. 🟢 **Quiet ends** (l2). On a `self-wrap` or `pick` sentinel it prints
   `herdr-loop: the loop stopped: {kind}` and exits 0. With the loop
   turned off it prints `herdr-loop: the session loop is off` and exits 0.
   With no loop on at its start it prints `herdr-loop: no session loop is
   on in pane {pane}; run /sdlc loop on there` and exits 2. In each case,
   and while no sentinel is there, it types nothing.
3. 🟢 **Stops** (l3). Two strikes in a row (two sessions that end at the
   position they started from), Claude gone from the pane with no
   sentinel, or a session whose transcript shows no change for 60 minutes:
   typing nothing, it files one `needs-ruling` issue from the pane's
   folder, shows a herdr toast, removes `loop.json`, prints
   `herdr-loop: session-loop stopped: ...` and exits 1. A sentinel of an
   unknown kind is left in place and ends at the hang check.

It calls herdr and `gh` by argument lists, never through a shell (Git Bash
rewrites `/clear`), and types only into the pane its argument names.

## The tree pane's hook: features

1. 🟢 **Seat flag.** At each arrival at an approval, the tree pane shows in
   herdr's sidebar as agent `sdlc`, state `blocked`, with the seat as its
   message: `approve-tests for tree-view/t6-query-face`.
2. 🟢 **The flag clears.** Once the pane's first line stops reading
   `waiting on a seat`, the hook releases the flag; Ctrl-C in the pane
   releases it too. When the line names a different seat, the hook leaves
   the flag to that seat's hook.
3. 🟢 **Toast.** At each arrival, a herdr toast titled `waiting on a seat`
   shows the seat and plays the request sound.

Struck for now: a herdr key action that opens the pane.

Known edges, from Two-Key's advisories (2026-09-23, PASS at round 1):
a Ctrl-C in the instant between the report and the watch does not
release; an `SDLC_NODE` with no `/` gives the seat `<node> for `; a Ctrl-C
during the release sends it twice, harmlessly; a report exit code outside
0 to 255 is truncated by the OS. A manual `release-agent` needs a `--seq`
above the hook's, which is the time in milliseconds.

## Setup

In a repo's `.sdlc/config.yaml`:

    tree:
      notify: python {kit}/herdr/herdr_seat.py

Then run `python -m taskcontract tree --follow` in a herdr pane.

## Why the tree pane carries the flag

Measured on herdr 0.9.0 and 0.9.1 (2026-09-23): an outside `herdr pane
report-agent --state blocked` never changes a Claude pane's state, idle or
working, from any source, with or without the session id; `herdr agent
explain` shows herdr reads Claude's state only from its screen-detection
rules. On a pane with no detected agent, the same report shows as the named
agent in that state, and `release-agent` clears it. The tree pane is such a
pane, and the notify command inherits its `HERDR_PANE_ID`.

## Interface

`herdr_seat.py` is one stdlib-only Python module, run as a script.

**Environment in.** The kit runs the command through the shell at the
repo root, with the tree pane's environment plus `SDLC_NODE`, the
approval task's full id (`tree-view/t6-query-face/approve-tests`).
herdr sets `HERDR_ENV=1` and `HERDR_PANE_ID` in its panes; the herdr
binary is `HERDR_BIN_PATH` when set and non-empty, else `herdr`.

When `HERDR_ENV` is not `1`, or `HERDR_PANE_ID` or `SDLC_NODE` is missing
or empty, the hook calls nothing and exits 0.

**The seat.** `SDLC_NODE` splits at its last `/`: the approval after it,
the unit before it. The seat is `<approval> for <unit>`; the pane's
waiting line for it is `waiting on a seat: <seat>`.

**herdr calls out**, in this order, `<pane>` being `HERDR_PANE_ID`:

1. `herdr pane report-agent <pane> --source sdlc:tree --agent sdlc --state
   blocked --message <seat> --seq <n>`. A nonzero exit ends the hook with
   that exit code, before any other call.
2. `herdr notification show "waiting on a seat" --body <seat> --sound
   request`. A nonzero exit does not stop the hook; it makes the final exit
   1.
3. Once a second: `herdr pane read <pane> --source visible`. The pane's
   first line is the first line of its output that is not blank, stripped
   of surrounding whitespace.
   - It is **this seat's line** when it equals the waiting line, or when it
     ends in `...` and the waiting line starts with the text before the
     `...` (the pane cut it to its width) and that text starts with
     `waiting on a seat: `. Keep watching.
   - It is **another seat's line** when it starts with `waiting on a seat:`
     and is not this seat's line. Exit without releasing (0, or 1 when the
     toast failed): that seat's hook owns the flag.
   - Anything else, or a read that exits nonzero, is **no seat**. Two
     readings in a row of no seat end the watch; one alone does not, since
     a read can land mid-redraw.
4. When the watch ends on no seat: `herdr pane release-agent <pane>
   --source sdlc:tree --agent sdlc --seq <n>`, then exit (0, or 1 when the
   toast failed; a failed release also makes it 1).

`--seq` is the current time in milliseconds, raised so that each call's
value is greater than the previous call's from the same process.

**Ctrl-C.** A `KeyboardInterrupt` at any point after the report releases
the flag (call 4) and exits 0.

**For tests.** The module defines

    main(environ, run, sleep, clock) -> int

`environ` is a mapping like `os.environ`. `run(argv)` runs one command
(`argv[0]` is the herdr binary) and returns `(exit_code, stdout)`.
`sleep(seconds)` waits; the hook calls `sleep(1)` before each read.
`clock()` returns the current time in seconds, as `time.time` does. Run as
a script, the module calls `main(os.environ, <subprocess runner>,
time.sleep, time.time)` and exits with its result; the runner decodes
output as UTF-8 with errors replaced and returns exit 127 when the binary
cannot start.
