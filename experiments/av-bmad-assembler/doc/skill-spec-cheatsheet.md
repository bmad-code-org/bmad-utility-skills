# Skill Spec Cheatsheet

Quick-reference for building skills that target Claude Code and the Agent Skills open standard.
For full details, see source docs with line references below.

---

## Part 1 — Agent Skills Open Standard

Source: `doc/agent-skills-overview.md`

### Structure
- Every skill is a directory with `SKILL.md` as the required entrypoint (L170)
- YAML frontmatter between `---` markers provides metadata; markdown body provides instructions (L170-185)
- Supporting files (scripts, templates, references) live alongside SKILL.md (L76-85)

### Frontmatter fields (standard)
- `name`: lowercase letters, numbers, hyphens only; max 64 chars; no "anthropic" or "claude" (L191-195)
- `description`: required, max 1024 chars; should state what the skill does AND when to use it (L197-202)

### Progressive disclosure — three loading levels
- **L1 Metadata** (~100 tokens): `name` + `description` loaded at startup into system prompt (L38-49, L97)
- **L2 Instructions** (<5k tokens): SKILL.md body loaded only when skill is triggered (L51-72, L98)
- **L3 Resources** (unlimited): additional files + scripts loaded/executed on demand; script output enters context, script code does not (L74-93, L99)

### Key design principle
- Skills are filesystem-based directories, not API payloads — Claude reads them via bash/file tools (L30, L105-109)
- Keep SKILL.md focused; offload detailed reference to separate files (L87-93)

### Cross-platform portability
- Same SKILL.md format works on Claude Code, Claude API, Claude.ai, Agent SDK (L129-158)
- Runtime differs per surface: Code has full network access, API has none, claude.ai varies (L249-260)
- Skills don't sync across surfaces — deploy separately to each (L236-240)

---

## Part 2 — Claude Code Extensions

Source: `doc/claude-code-skills.md`

### Skill locations (Claude Code specific)
- Enterprise > Personal (`~/.claude/skills/`) > Project (`.claude/skills/`) > Plugin — higher wins on name collision (L83-90)
- Nested `.claude/skills/` in subdirectories are auto-discovered (monorepo support) (L92-94)
- `--add-dir` skills get live reload without restarting session (L112-114)

### Extra frontmatter fields (Claude Code only)
- `disable-model-invocation`: `true` = only user can invoke via `/name` (L176)
- `user-invocable`: `false` = hidden from `/` menu, only Claude auto-loads it (L177)
- `allowed-tools`: restrict tools available during skill execution (L178, L248-256)
- `model`: override model for this skill (L179)
- `context`: `fork` runs skill in isolated subagent (L180, L324-361)
- `agent`: which subagent type for `context: fork` — `Explore`, `Plan`, `general-purpose`, or custom (L181, L361)
- `hooks`: skill-scoped lifecycle hooks (L182)
- `argument-hint`: autocomplete hint like `[issue-number]` (L175)

### String substitutions
- `$ARGUMENTS` / `$ARGUMENTS[N]` / `$N` — argument placeholders (L186-206)
- `${CLAUDE_SESSION_ID}` — current session ID (L193)
- If `$ARGUMENTS` absent from content, args appended as `ARGUMENTS: <value>` (L190)

### Dynamic context injection
- `` !`command` `` syntax runs shell commands at load time, output replaces placeholder (L294-320)
- Runs before Claude sees content — pure preprocessing (L318-320)

### Subagent execution
- `context: fork` = skill runs in isolated context without conversation history (L324-327)
- Only useful for skills with explicit task instructions, not pure guidelines (L328)
- `agent` field picks execution environment; defaults to `general-purpose` (L361)

### Invocation control matrix
| Frontmatter | User invokes | Claude invokes | Description in context |
|---|---|---|---|
| (default) | yes | yes | yes |
| `disable-model-invocation: true` | yes | no | no |
| `user-invocable: false` | no | yes | yes |
(L240-244)

### Context budget
- Skill descriptions budget = 2% of context window, fallback 16k chars (L419-420)
- Override with `SLASH_COMMAND_TOOL_CHAR_BUDGET` env var (L421)

### Practical tips
- Keep SKILL.md under 500 lines (L230)
- `description` drives auto-discovery — use keywords users would naturally say (L403-405)
- Include "ultrathink" in skill content to enable extended thinking (L322)
- `.claude/commands/` files still work but skills take precedence on name collision (L90, L110)
