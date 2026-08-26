---
name: sdlc-flow-audit
description: The Audit flow of /sdlc - report-only gate-health check via audit.py; findings reported verbatim, nothing fixed.
---

<purpose>
The Audit flow of the `/sdlc` skill: report-only gate health.
Dispatched by {skill-dir}/SKILL.md on `/sdlc audit`; its constraints
and criteria bind here. {skill-dir} is the directory holding SKILL.md.
</purpose>

<instructions>
A1. RUN - one Bash call, by absolute path: `python "{skill-dir}/audit.py" --cwd .`

A2. REPORT stdout verbatim. Exit 0 = clean; 1 = findings, each carrying a code (e.g. CONTRACT-INVALID, SPINE-MISSING, REDS-SCHEMA); 2 = no gate spine here (offer the init interview instead). Do NOT fix findings unasked - audit automates detection; fixes stay with the user or an explicit follow-up task.
</instructions>
