| Revision Date | Revised By | Changes Made |
| :-: | :-: | :-- |
| 2026-11-22 | Johnathan Hyden | r1: Created through /sdlc:product-specification-interview. The design, in progress, against requirements r4. Engineer seat: Johnathan Hyden |
| 2026-11-22 | Johnathan Hyden | r2: Measured: the checks before signing, on the solution half: 29 findings (CL006 26, CL008 3); Scope against the release unit's paths: covered; ready checks 11 to 15: 3 OPEN |
| 2026-11-22 | Johnathan Hyden | r3: Measured: the checks before signing, on the solution half: 20 findings (CL006 20); Scope against the release unit's paths: covered; ready checks 11 to 15: 0 OPEN |
| 2026-11-22 | Johnathan Hyden | r4: The solution half finished: 12 sections written, 0 OPEN |
| 2026-11-22 | Johnathan Hyden | r5: Signed: solution half. The engineer seat signs r4 |
| 2026-11-22 | intake | r6: Parked: OPEN: Ready check 3: SC1 holds five checks and SC2 four, past the two or three a criterion takes; the extras are Q11's regression checks. Decisions and open questions 9: OPEN: can a timer (`CronCreate`) wake an idle interactive session? Decisions and open questions 10: OPEN: can `herdr pane send-keys` type slash commands into a Claude pane? Decisions and open questions 11: OPEN: how does the 55-minute notice reach the user: phone, email or desktop toast? |
| 2026-11-22 | Johnathan Hyden | r7: Confirmed against requirements r9 |
| 2026-11-22 | Johnathan Hyden | r8: Units cut to four against requirements r9, each at most three sketch entries: `l3-loop-stops` splits from `l2-loop-launcher`, the rules move to `l4-loop-rules`; Order, Risks and cost, Out of scope, Links out and Notes follow |
| 2026-11-22 | Johnathan Hyden | r9: Measured: the checks before signing, on the solution half: 22 findings (CL006 22); Scope against the release unit's paths: covered; ready checks 11 to 15: 0 OPEN |
| 2026-11-22 | Johnathan Hyden | r10: The solution half finished: 12 sections written, 0 OPEN |
| 2026-11-22 | Johnathan Hyden | r11: Signed: solution half. The engineer seat signs r10 |
| 2026-11-22 | intake | r12: Ready: contract `session-loop` validates ready-green, derived from r10, against requirements r9; the engineer seat (Johnathan Hyden) signed the solution half at r10 (r11) |

# session-loop - Sessions restart themselves until you are needed

`sdlc_development_kit` · seat: engineer Johnathan Hyden · requirements: `docs/features/session-loop.md` · contract: `session-loop`, draft · PR: none · merge SHA: none

## Proposed solution

`[Engineer seat · authored]`

### Scope

- `workflows/tools/loop.py` (new): the loop's files and issues: `on`, `off`, `stop`, `reply`, `due`, `wrap`.
- `skills/sdlc/flows/loop.md` (new) and `skills/sdlc/SKILL.md`: the `/sdlc loop on|off` route, and the rules a session in a loop follows at a stop, a reply and a wrap.
- `hooks/loop_on.py` (new) and `hooks/hooks.json`: a SessionStart entry that tells a fresh session the loop is on.
- `E:\herdr-sdlc\herdr_loop.py` (new), `E:\herdr-sdlc\tests\` and `E:\herdr-sdlc\README.md`: the launcher.
- `tests/`: each kit unit's own test file.
- `docs/usage/` (a session-loop page), `USAGE.md`, `docs/components.md`, `CHANGELOG.md`, `pyproject.toml` and `skills/sdlc/init.py` (kit 0.23.0); `.github/workflows/sdlc.yml` takes the `v0.23.0` tag in the self-pin PR.

### Out of scope

The requirements run's state file holds no refused places. The build leaves these untouched:

- `hooks/context_size.py` and `hooks/wall.py`: the 200K message stays the wrap's trigger, unchanged.
- `workflows/tools/task.py` and a team run's files: SC1.3 reads only that no sentinel appears.
- `E:\herdr-sdlc\herdr_seat.py`: the tree pane's flag stays its own (SC1.3).
- The user-global skills `/resume-session`, `/cairn` and `end-session`: the launcher types `/resume-session` as it stands.
- `docs/backlog.md` and the Next it holds: the loop never writes Next (SC5.2).
- herdr's config and plugins: no plugin, no key binding.

### Interfaces

The user starts a loop in two steps, and stops it with one:

```
> /sdlc loop on
session loop on; a launcher may now restart this repo's sessions

PS> python E:\herdr-sdlc\herdr_loop.py w9:p1
herdr-loop: watching pane w9:p1 (E:\sdlc_development_kit)

> /sdlc loop off
session loop off
```

The kit's files, all under `{git folder}/sdlc-loop/` (the folder `git rev-parse --absolute-git-dir` names), never tracked:

- `loop.json`: `{"on": "2026-11-22T17:44:02"}`. The loop is on while it exists. It names no pane: the kit knows nothing of herdr.
- `waiting.json`: `{"issue": 172, "at": "...", "due": "...", "cron": "36 18 22 11 *"}`. A human-needed stop is open while it exists.
- `sentinel.json`, written last: `{"kind": "continue", "position": "plan step 4, task none", "next": "...", "head": "<sha>", "at": "..."}`. `kind` is `continue`, `self-wrap` or `pick`.

`loop.py`, run by the session as `python {skill-dir}/../../workflows/tools/loop.py`, one Bash call each:

- `on` and `off`: write and remove `loop.json`. `on` when on rewrites the time and prints the same line; `off` when off prints `session loop off` and exits 0.
- `stop --question TEXT`: with no `needs-ruling` label, prints `session-loop: the needs-ruling label is missing; run: gh label create needs-ruling` and exits 1, writing nothing. Else it files the issue (label `needs-ruling`, title the question's first line cut to 70 characters, body the question), writes `waiting.json`, and prints `{"issue": N, "due": "...", "cron": "M H D Mo *"}`.
- `reply`: closes the waiting issue with the comment `answered in the session` and removes `waiting.json`; with none, prints `no stop waiting` and exits 0.
- `due`: exits 0 when `waiting.json` exists, else 3.
- `wrap --plan-step N --task T --next TEXT [--self]`: when the branch has no remote branch, or its head is not HEAD, prints `session-loop: the wrap's commit is not on the remote; push first` and exits 1, with no sentinel. When `--next` is `(none)`, files one issue titled `Pick the next deliverable` (label `needs-ruling`) unless an open one has that title, and the kind is `pick`. `--self` makes the kind `self-wrap`, and the waiting issue stays open. Else the kind is `continue`. A `pick` or `self-wrap` removes `loop.json`. The sentinel is the last write.

The session's rules, in `flows/loop.md`, in force while `loop.json` exists:

- Human-needed stop: run `loop.py stop`; on exit 1 show its line and stop as an ordinary stop. Else set a one-shot `CronCreate` at the printed `cron` with the prompt `session-loop: no reply to issue #{n} in 55 minutes. Run loop.py due: on exit 0 self-wrap by flows/loop.md; on exit 3 do nothing.`, send `PushNotification` with `Ruling needed (#{n}): {question, cut to 150 characters}`, and end the turn on the question.
- Reply: the user's next message while `waiting.json` exists: `CronDelete` the job, run `loop.py reply`, then go on.
- Wrap: commit, push, read Next by `/cairn status`, run `loop.py wrap`, then a closing message that asks nothing. The self-wrap is the same with `--self`.

The SessionStart hook prints, when `loop.json` exists: `A session loop is on in this repo: follow {plugin}/skills/sdlc/flows/loop.md at every stop and wrap.`

The launcher, `python E:\herdr-sdlc\herdr_loop.py <pane>`, prints one line per event in its own pane:

- With no `loop.json` in the git folder of the pane's working directory (`herdr pane get`'s `cwd`): `herdr-loop: no session loop is on in pane {pane}; run /sdlc loop on there`, exit 2.
- On a `continue` sentinel: renames it `sentinel.seen.json`, counts the strike, waits until the pane reads idle, types `/clear` and Enter, then 3 seconds later `/resume-session` and Enter, all within 60 seconds of the sentinel. Prints `herdr-loop: restarted pane {pane} at {position}`.
- On a `self-wrap` or `pick` sentinel: prints `herdr-loop: the loop stopped: {kind}` and exits 0, typing nothing.
- At its own stops it files one `needs-ruling` issue titled with the requirements' verbatim message (SC4.1, SC4.3), with the body `pane {pane}; last position {position}; last sentinel {path, or none}`, shows `herdr notification show "session-loop stopped" --body {message} --sound request`, removes `loop.json` and exits 1.
- When `loop.json` is gone (`/sdlc loop off`): `herdr-loop: the session loop is off`, exit 0.

No endpoint table: the feature has no network endpoint.

### Sources

| Fact | Read from | When two disagree |
| :-- | :-- | :-- |
| The loop is on | `loop.json` in the git folder | one source |
| The pane the launcher drives | the launcher's argument; its repo from `herdr pane get`'s `cwd` | one source |
| Position | the sentinel's `position`, from the wrap's `--plan-step` and `--task`; the launcher holds the previous sentinel's in memory as the next session's start | one source |
| Next | `/cairn status`'s Next, passed by the session as `--next` | one source |
| The wrap's commit is on the remote | `git ls-remote origin refs/heads/{branch}` against `git rev-parse HEAD` | the remote wins over the local tracking ref |
| A stop is waiting | `waiting.json` | `waiting.json` wins over the issue's state: the reply comes in the session, never on the issue (requirements decision 7) |
| The reply came | the user's next message in the session while `waiting.json` exists | one source |
| The waiting issue's state | `gh issue view {n} --json state` | one source |
| A wrap finished | `sentinel.json` present | one source |
| The stop's time and the timer's due | `waiting.json`'s `at` and `due` | one source |
| The self-wrap's start | the cron prompt's arrival in the transcript | one source |
| The label exists | `gh label list --search needs-ruling`, exact name | one source |
| An open pick issue | `gh issue list --state open --label needs-ruling`, exact title | one source |
| Claude runs in the pane | `herdr pane process-info`: a foreground process named `claude.exe` or `claude` (trial 2: after `/exit` the foreground was `pwsh.exe`) | process-info wins over `herdr pane get`'s `agent` key |
| The pane is idle | `herdr pane get`'s `agent_status` | one source |
| The pane changed (hung) | the transcript's last write, `~/.claude/projects/*/{id}.jsonl`, the id from `herdr pane get`'s `agent_session` | the transcript; the pane's text is never read, since its status line redraws every second (trial 2) |

### Constraints

- `loop.py` and `herdr_loop.py` use the standard library only, and decode subprocess output as UTF-8 with errors replaced.
- The launcher calls herdr and `gh` with argument lists, never through a shell: in trial 2, Git Bash rewrote `/clear` to `C:/Program Files/Git/clear`.
- The launcher types only into the pane its argument names, and only while that pane reads idle.
- The kit imports nothing from `E:\herdr-sdlc` and runs no herdr command; the launcher imports nothing from the kit and reads its files by path (ADR 0031's split).
- The timer's minute: the stop's time plus 55 minutes, cut to the minute; a minute of :00 or :30 moves one minute on, since a one-shot landing there may fire up to 90 seconds early. The wrap then starts within 54 to 56 minutes (SC3.1).
- The sentinel is the wrap's last write, after the push check (SC1.2).
- `loop.md` stays under 12,000 characters, the flow files' ceiling, and every Bash call in it is one segment.
- No new window or tab: the user starts the launcher in a pane of their own.

### Units

| Unit | Checks | Done means | Tests by check id and kind | Retirements |
| :-- | :-- | :-- | :-- | :-- |
| l1-loop-files | SC1.2, SC2.1, SC5.1+SC5.2 | `loop.py stop` files the `needs-ruling` issue and writes the waiting file. `reply` closes that issue. `wrap` writes the sentinel last, after the push. With Next empty, `wrap` files one pick issue. | SC1.2, SC2.1: automated, with git and `gh` behind a run seam. SC5.1+SC5.2: automated, with `gh` behind the run seam, and `loop.py` writes nothing outside `{git folder}/sdlc-loop/`. | none |
| l2-loop-launcher | SC1.1, SC1.3, SC3.2 | `herdr_loop.py` restarts the pane within 60 seconds of a `continue` sentinel. The launcher types nothing on any other sentinel or with none. | SC1.1: automated, and a manual receipt: one live restart in a herdr pane, whose new session names the Next the sentinel holds. SC1.3: automated (no keystroke with no sentinel; no `report-agent` or `release-agent` call), and a manual receipt: the tree pane flagged while the launcher runs. SC3.2: automated, with herdr, `gh`, sleep and the clock faked. | none |
| l3-loop-stops | SC4.1, SC4.2, SC4.3 | Two strikes, an exit or a 60-minute hang stop the loop with one issue, and the launcher types nothing. | SC4.1, SC4.2, SC4.3: automated, with herdr, `gh`, sleep and the clock faked. | none |
| l4-loop-rules | SC2.2, SC2.3, SC3.1+SC3.3 | `/sdlc loop on` turns the loop on. In a loop, a session files its stop and sets its timer. A reply continues the session. With no reply, the session wraps itself. Kit 0.23.0 ships. | SC2.3: automated (a text test on `loop.md`). SC2.2, SC3.1+SC3.3: manual receipts in one live sitting of two panes, one answered at 54 minutes, one left to 55. | none |

### Order

l1, then l2, then l3, then l4. l1's files are the contract the others read. l2 tests against those file shapes with herdr faked; l3 adds its stops to l2's launcher. l4's live receipts need l1 to l3 in place.

## Risks and cost

`[Engineer seat · authored]`

- The timer lives only in the session; a Claude restart loses it. The launcher's 60-minute hang check is the net.
- `PushNotification` is held back while the terminal is active (trial 3), and reaches the phone only with Remote Control connected. The issue is the record either way. GitHub sends no notice for an issue filed under the user's own account (assumed, not measured).
- A session that writes a wrong position defeats the strike count; the exit and hang checks still stop the loop.
- Typing into a pane mid-turn: the launcher waits for the idle reading.
- l2 and l3 land in a second repo, `E:\herdr-sdlc`, with their tests there; the tree hook, `herdr_seat.py`, is the precedent.
- Cost: about eight build sessions, two a unit (standing practice, session 96), plus one live sitting of about an hour, idle while the timers run.

## Consult cases

`[Engineer seat · authored]`

| Case | Answer | Who was asked | What was decided |
| :-- | :-: | :-- | :-- |
| 1. An ambiguity in the requirements | yes | The engineer seat, Johnathan Hyden, on Claude's recommendation (session 165) | "The pane shows no change" reads the transcript's last write, since the pane's status line redraws every second. Every stop, the launcher's too, removes `loop.json`, so the loop stays stopped until the user turns it on. |
| 2. More than one solution | yes | The engineer seat, Johnathan Hyden, on Claude's recommendation (session 165) | The 55-minute timer is a `CronCreate` in the session (trial 1), not the launcher typing a wrap prompt: the self-wrap stays the session's own act and needs no typing. |
| 3. A solution unconventional to the codebase | no | | |
| 4. A change to a public contract: routes, a gateway definition, events, a schema | yes | The engineer seat, Johnathan Hyden, on Claude's recommendation (session 165) | A new command, `/sdlc loop on|off`, a SessionStart hook, and three JSON files `E:\herdr-sdlc` reads: their shapes in Interfaces are the contract. |

## Decisions and open questions

`[Engineer seat · authored]`

1. Decided (trial 1, 2026-11-22): a one-shot `CronCreate` set at 17:41:44 for 17:44 fired at 17:44:02 while the session sat idle. The 55-minute timer is `CronCreate` in the session. Closes the requirements' OPEN 9.
2. Decided (trial 2): in a Claude pane, `herdr pane send-text` then `send-keys Enter` ran `/clear` (context back to 0%) and `/cairn status`. Through Git Bash, `/clear` arrived as `C:/Program Files/Git/clear`. Closes OPEN 10.
3. Decided (trial 3): the notice at a human-needed stop is `PushNotification` from the session: a desktop notice, and the phone over Remote Control. The tool held the trial's notice back while the terminal was active. The launcher's own stops show a herdr toast. Closes OPEN 11.
4. Decided: the loop is on while `loop.json` exists. `/sdlc loop on` writes it; the session removes it at a `self-wrap` or `pick`, the launcher at its own stops.
5. Decided: the launcher's stop issues carry the `needs-ruling` label, so `/cairn status` lists them under "Waiting on you".
6. Decided: a human-needed issue's title is the question's first line, cut to 70 characters.
7. Decided: the push check's message, `session-loop: the wrap's commit is not on the remote; push first`, is the design's; the requirements give none for SC1.2.

## Traceability

### Links out

`[Engineer seat · authored]`

- Requirements: `docs/features/session-loop.md`, signed at r4 (PR #171), and again at r9 after intake parked the pair (session 166).
- ADR 0031, `decisions/0031-the-work-is-one-derived-tree.md`: the kit writes files, the herdr side reads them.
- ADR 0039, `decisions/0039-the-kit-ships-plugin-hooks-and-a-node-starts-at-its-rows-settings.md`: the kit ships plugin hooks.
- `docs/features/run-restart.design.md`: the git-folder files a run keeps.
- `E:\herdr-sdlc\README.md`: the tree hook, the launcher's neighbour.
- `docs/backlog.md` Next 30 (this design) and Next 31 (`session-loop-sidebar`).

### Record

`[Intake · derived]`

(none: intake writes the record)

## Notes

`[Engineer seat · authored]`

- Every answer in this design is Claude's recommendation, taken on the engineer seat's word of 2026-11-22: "Go with all of your recommendations on this session, then give me a recap of what those were".
- The trials ran in session 165 on herdr 0.9.1 and Claude Code v2.1.330, in a scratch pane closed afterwards.
- The draft check's CL006 findings stand answered: they are the feature's own terms (wrap, sentinel, strike, `needs-ruling`) and plain words outside the controlled dictionary (issue, reply, timer, seconds), the class the request half signed with at 56. Adding them to the dictionary is the full lane's work; this design adds no entry.
- Session 166: intake parked the pair at r6 on the requirements' four OPEN marks, and the requirements' r9 merged 18 checks to 14. The contract holds at most three sketch entries a unit, so r8 cut the units to four, with `+` pairing two checks one test reads. Each answer is Claude's recommendation, on the engineer seat's word of 2026-11-22: "Yes".

## Appendix

### Contract

`[Intake · derived]`

(none: intake writes `specs/session-loop/contract.yaml`)
