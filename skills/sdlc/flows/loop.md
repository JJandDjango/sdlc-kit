---
name: sdlc-flow-loop
description: The Loop flow of /sdlc - turn the session loop on and off, and the rules a session follows at a stop and a wrap while the loop is on.
---

<purpose>
The Loop flow of the `/sdlc` skill: `/sdlc loop on` and `/sdlc loop off` turn
the session loop of this repo on and off, and a session in a loop follows its
rules at every stop and wrap. {plugin} is the kit's folder in forward slashes:
the SessionStart line names it in full, and from /sdlc loop on it is two
folders above the folder holding SKILL.md.
The loop is on while `loop.json` exists in `{git folder}/sdlc-loop/`. A
session that starts in a loop reads this line from the SessionStart hook:
`A session loop is on in this repo, and the user may be away. Every question to the user is a stop: first run the stop rule (L3) in {plugin}/skills/sdlc/flows/loop.md, then ask in a plain message, never by AskUserQuestion. Follow the same file at every wrap. Run loop.py as python {plugin}/workflows/tools/loop.py.`
L1 and L2 turn the loop on and off. L3 to L6 are the rules of a session in a
loop, in force while `loop.json` exists: the stop that needs the user, the
reply, the wrap and the self-wrap. Every command is one Bash call.
</purpose>

<instructions>
L1. ON - RUN `python {plugin}/workflows/tools/loop.py on` in one Bash call, then SHOW the line it prints.
    On a refusal, SHOW its line and go back to the conversation; the loop stays as it was.

L2. OFF - RUN `python {plugin}/workflows/tools/loop.py off` in one Bash call, then SHOW the line it prints.

L3. STOP - Every question to the user while the loop is on is this stop. At a stop that needs the user's answer, RUN `python {plugin}/workflows/tools/loop.py stop --question "{question}"` before asking, one Bash call.
    On exit 1, SHOW its line and STOP as an ordinary stop: set no timer.
    Else HOLD the printed `issue` as {n}, `due` as {due} and `cron` as {cron}.
    CronCreate a one-shot timer, set at {cron}, with the prompt `session-loop: no reply to issue #{n} in 55 minutes. Run loop.py due: on exit 0 self-wrap by flows/loop.md; on exit 3 do nothing.` then HOLD the job id as {job}.
    PushNotification: Ruling needed (#{n}): {question, cut to 150 characters}
    END the turn on the question: the last message is the question, and it ends on `?`.
    Ask the question in a plain message, never by AskUserQuestion: a dialog that waits is no idle session, so the timer's prompt never lands.
    This rule outranks a flow step that asks by AskUserQuestion (`init`, `intake`).
    Run no wrap here: the stop files no sentinel, so no launcher types anything while the session waits.

L4. REPLY - While the L3 stop waits, the user answers in the session, never on the issue: the reply is the user's next message.
    On that message, run CronDelete {job}.
    Then RUN `python {plugin}/workflows/tools/loop.py reply`, one Bash call, which closes the issue, and then go on with the work the reply rules.
    Run no wrap and write no sentinel.

L5. WRAP - At the end of a session in a loop: commit the work, push the branch, then RUN `/cairn status` and read its Next.
    Pass Next as `/cairn status` prints it: when it prints `(none)`, pass `(none)`.
    Do NOT name a deliverable yourself: the loop never picks one.
    RUN `python {plugin}/workflows/tools/loop.py wrap --plan-step {step} --task {task} --next "{next}"`, one Bash call; it writes the sentinel last, after the push.
    Then SHOW the closing message. The closing message asks nothing: it holds no question.

L6. SELF-WRAP - A prompt that starts `session-loop: no reply to issue` came from the timer of an L3 stop.
    RUN `python {plugin}/workflows/tools/loop.py due` first, one Bash call.
    On exit 0 self-wrap; on exit 3 do nothing: a reply or a wrap came first, and the prompt is stale.
    To self-wrap: commit the work, push the branch, RUN `/cairn status`, then RUN `python {plugin}/workflows/tools/loop.py wrap --plan-step {step} --task {task} --next "{next}" --self`, one Bash call.
    The needs-ruling issue stays open, and `/cairn status` lists it under Waiting on you in the user's next session; the loop stays stopped.
    Then SHOW the closing message. The closing message asks nothing: it holds no question.
</instructions>
