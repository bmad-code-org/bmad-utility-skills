---
name: av-human-review
description: 'Guided walkthrough of a change, from purpose and context into details. Use when the user says "walk me through this change", "human review", or "review walkthrough".'
---

You are assisting the user in reviewing a change.

**Standing rule:** Every code reference you produce must use clickable `path:line` format — absolute or relative to the current working directory (e.g., `src/auth/middleware.ts:42`).

## INITIALIZATION

Load and read full config from `{project-root}/_bmad/bmm/config.yaml` and resolve:

- `implementation_artifacts`
- `communication_language`

## FIRST STEP

Read fully and follow `./step-01-orientation.md` to begin.
