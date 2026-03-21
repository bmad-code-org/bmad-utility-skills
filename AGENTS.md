# bmad-utility-skills

Agentic Skills for a BMad maintainer. Packaged as a Claude Code plugin. Github repo is configured as a private CC marketplace.

## Skill Conventions

```yaml
---
name: bmad-os-<slug>
description: <one-line description, icludng "use when" trigger>
---
```

## Rules

- Use `gh` CLI for all GitHub operations
- Write files instead of heredocs for multi-line content passed to shell commands
- Skills that post to GitHub must include a preview + explicit confirmation step before posting
Output files go to `_bmad-output/<skill-name>/` with date-stamped filenames
- Use conventional commit format.
- Never push to git or create PRs wiithout explicit request by user. If you decide it's time to push:

- prepare it (rebase, commit)
- tell the user how you propose to push: exact command, and if it's not a plain `git push`, one-line explainer for it, and if you intend to create a PR from the push, mention that, too
- STOP and wait for the user to either confirm the push or to execute it
- If you told the user that you intended to create a PR, once the push is executed by the user, or confirmed by the user and executed by you, use GH to create that PR without further questions.
