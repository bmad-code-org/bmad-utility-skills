---
name: bmad-os-diataxis
description: Create, update, fix, or refine documentation using Diataxis framework and BMad Method style guide. Use when user asks to 'create a doc', 'update docs', 'fix docs style', 'refine docs', or 'improve docs writing'.
---

# Diataxis Documentation Skill

## Overview

Create, update, fix, or refine documentation that conforms to the Diataxis framework and the project's BMad Method style guide. Act as a meticulous technical editor who understands the Diataxis taxonomy, the project's structural conventions, and what makes prose read as authentically human rather than AI-generated.

**Args:** A mode (`create`, `update`, `fix`, `refine`) and a target (file path, directory, or topic). Mode is inferred from context if not explicit. Target defaults to `docs/` for fix and refine modes.

## Critical Constraints

- **Never commit or push** — let the user review first
- **Use Edit tool** for updates, fixes, and refinements — targeted, not destructive

## On Activation

1. Read the project's style guide at `docs/_STYLE_GUIDE.md`
2. Determine the mode and route accordingly

## Modes

### Create

Write new documentation for a given topic or feature. Determine the appropriate Diataxis type from the user's intent (or ask if ambiguous), place the file in the correct directory, and build it with the required structure for that type. Apply the writing quality rules below from the start. After writing, spawn a refinement subagent to polish prose quality.

### Update

Revise existing documentation — add new content, restructure sections, or reflect changes in the codebase. Read the target file first, preserve what's still accurate, and ensure the result conforms to style conventions and required structure for its type. Apply writing quality rules to new and changed content. After updating, spawn a refinement subagent to polish prose quality.

### Fix

Scan existing files for structural and formatting violations only. For each file, determine its Diataxis type from location, apply the universal style rules and type-specific structure requirements below, and present a per-file summary of all changes. Does not touch prose quality — use Refine for that.

### Refine

Improve prose quality of existing documentation without changing structure or meaning. When given a directory, spawn parallel subagents — one per file — for concurrent processing. When given a single file, spawn one subagent. Collect and present the combined per-file summaries when all subagents complete.

**Subagent prompt** (used for Refine and post-Create/Update polish):

> You are a prose quality editor. Read `{skill-path}/references/writing-quality.md` for the complete pattern reference. Then read `{target-file}` and make targeted Edit tool fixes to eliminate AI writing patterns. Focus on: banned vocabulary, rhetorical tics (metanoia, tricolon overuse, amplificatio), sentence rhythm (burstiness), hedging, filler transitions, and structural monotony. Preserve all meaning and technical accuracy. Use the Edit tool for each fix. Present a summary of changes when done. Never commit or push.

Replace `{skill-path}` with the absolute path to this skill and `{target-file}` with the file being refined. When spawning parallel subagents for a directory, each gets its own file path.

## Writing Quality Rules

Apply when generating or revising prose (Create, Update, Refine). Not applicable to Fix mode.

- **Plain vocabulary** — No "delve," "tapestry," "landscape," "robust," "comprehensive," "leverage," "utilize," "foster," "harness," "pivotal," "paramount," "furthermore," "moreover," or "notably." Use direct, common words.
- **No restatement openers** — Don't open a section by paraphrasing the heading. Start with the substance.
- **No mirror-and-extend** — Every sentence must advance the content. If it restates what was just said in different words, cut it.
- **Vary sentence rhythm** — Alternate short and long sentences. No three consecutive sentences of similar length. Break metronomic cadence.
- **Limit rhetorical devices** — One "not X, it's Y" per doc max. One tricolon per doc max. One em dash per paragraph max. If a device appears twice, cut one.
- **No hedging filler** — Cut "it's worth noting," "it's important to note," "while there are many factors." State the point directly.
- **No stakes inflation** — Don't call things "game-changing," "revolutionary," or "fundamental" unless they genuinely are.
- **No signposted conclusions** — Don't write "In conclusion" or "To sum up." Just conclude.
- **Audience-calibrated depth** — Don't explain what the target audience already knows. If it would bore a practitioner, cut it.
- **Contractions are fine** — Use natural language. "Don't" over "do not" when tone permits.

## Document Type by Location

| Location | Type |
|---|---|
| `docs/tutorials/` | Tutorial |
| `docs/how-to/` | How-to guide |
| `docs/explanation/` | Explanation |
| `docs/reference/` | Reference |
| `docs/glossary/` | Glossary |

## Universal Style Rules

Project conventions — apply to all document types, all modes:

- **Horizontal rules (`---`)** — Never use outside frontmatter; use `##` headers or admonitions instead
- **`####` headers** — Use **bold text** or admonitions instead
- **"Related"/"Next:" sections** — Omit (sidebar handles navigation)
- **Deep nesting** — Max 3 list levels; break into `##` sections beyond that
- **Code blocks for dialogue** — Use `:::note[Example]` admonitions
- **Bold callout paragraphs** — Use typed admonitions (`:::caution`, `:::tip`, etc.)
- **Admonition density** — Max 1-2 per section (tutorials allow 3-4 per major section)
- **Verbose table/list cells** — Keep to 1-2 sentences
- **Header budget** — Target 8-12 `##` per doc, 2-3 `###` per section

## Required Structure by Type

**Tutorials** — Outcome-focused hook, "What You'll Learn" bullets, `:::note[Prerequisites]`, `:::tip[Quick Path]` TL;DR, tables for phases/commands/agents, "What You've Accomplished", Quick Reference table, Common Questions, Getting Help, `:::tip[Key Takeaways]`

**How-to guides** — Hook starting "Use the `X` workflow to...", "When to Use This" (3-5 bullets), `:::note[Prerequisites]`, numbered `###` steps with action verbs, "What You Get" outputs section

**Explanation** — Hook stating what it explains, scannable `##` sections, comparison tables for 3+ options, links to how-to guides for procedural topics, max 2-3 admonitions

**Reference** — Hook stating what it references, consistent item structure, tables for structured/comparative data, links to explanation docs for depth, max 1-2 admonitions

**Glossary** — Categories as `##` headers, terms in tables (not individual headers), definitions 1-2 sentences max, bold term names
