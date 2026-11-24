### The session loop: `/sdlc loop on` 🟢

> 🟢 **Shipped** (kit 0.23.0, contract `specs/session-loop/`, units l1 to
> l4; design [session-loop.design.md](../features/session-loop.design.md);
> [ADR 0043](../../decisions/0043-the-herdr-tools-ship-in-the-kits-opt-in-herdr-folder.md)).
> 🟢 shipped, 🟡 built, not verified.

A session in a loop wraps itself, and a launcher in another pane restarts
it with `/clear` and `/resume-session`, until the work needs you. Turn it
on in the session, then start the launcher in a pane of your own
([herdr](../../herdr/README.md), opt-in; the kit never needs it):

```
> /sdlc loop on
session loop on; a launcher may now restart this repo's sessions

PS> python E:\sdlc_development_kit\herdr\herdr_loop.py w9:p1
herdr-loop: watching pane w9:p1 (E:\sdlc_development_kit)

> /sdlc loop off
session loop off
```

🟢 **On and off.** `/sdlc loop on` writes `loop.json` in
`{git folder}/sdlc-loop/`; the loop is on while it exists. `/sdlc loop off`
removes it, and the launcher then ends with `herdr-loop: the session loop
is off`. None of the loop's files is ever tracked.

🟢 **A fresh session knows.** While the loop is on, each session starts
with: `A session loop is on in this repo, and the user may be away. Every question to the user is a stop: first run the stop rule (L3) in {plugin}/skills/sdlc/flows/loop.md, then ask in a plain message, never by AskUserQuestion. Follow the same file at every wrap. Run loop.py as python {plugin}/workflows/tools/loop.py.`

🟢 **A stop that needs you.** The session files a `needs-ruling` issue
holding its question, sets a 55-minute timer, sends a notice, and ends its
turn on the question, asked in a plain message: while the loop is on, an
AskUserQuestion dialog is refused and turned back to this stop. With no `needs-ruling` label in the repo it says
`run: gh label create needs-ruling` and stops as an ordinary stop.

🟢 **Your reply.** Answer in the session, never on the issue: your next
message deletes the timer, closes the issue with `answered in the
session`, and the session goes on. It runs no wrap.

🟢 **No reply.** When the timer runs out, the session wraps itself. Its
closing message asks nothing; the issue stays open, and your next
session's `/cairn status` lists it under Waiting on you. The loop stays
off until you turn it on again.

🟢 **The wrap.** The wrap commits, pushes, then writes its sentinel last;
with the commit not on the remote it writes none. With Next empty it files
one `Pick the next deliverable` issue and the loop stops (l1).

🟢 **The restart and the stops.** The launcher restarts the pane within 60
seconds of a `continue` sentinel, and types nothing on any other. Two
sessions in a row that end where they started, Claude gone from the pane,
or 60 minutes with no change stop the loop with one issue
([herdr/README.md](../../herdr/README.md), l2 and l3).
