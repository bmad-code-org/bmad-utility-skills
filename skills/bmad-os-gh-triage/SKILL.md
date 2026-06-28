---
name: bmad-os-gh-triage
description: Analyze all github issues. Use when the user says 'triage the github issues' or 'analyze open github issues'.
---

# GitHub Issue Triage with AI Analysis

**CRITICAL RULES:**
- NEVER include time or effort estimates in output or recommendations
- Focus on WHAT needs to be done, not HOW LONG it takes
- Use Bash tool with gh CLI for all GitHub operations

## Execution

### Step 1: Fetch Issues
Use `gh issue list --json number,title,body,labels` to fetch all open issues.

### Step 2: Batch Creation
Split issues into batches of ~10 issues each for parallel analysis.

### Step 3: Parallel Agent Analysis
For EACH batch, use the Task tool with `subagent_type=general-purpose` to launch an agent with prompt from `agent-prompt.md`

### Step 4: Consolidate & Generate Report

After all agents complete, write a comprehensive markdown report to **`./triage/triage-{datetime}.md`** (e.g. `./triage/triage-2026-06-28-1432.md`), relative to the project root. Create the `triage/` folder if it doesn't exist. `{datetime}` is `YYYY-MM-DD-HHMM`.

Determine whether this is a fresh triage or an update of a prior one (ask if the user hasn't said):

- **Fresh triage** — write a new `./triage/triage-{datetime}.md`.
- **Update a past triage** — the user points to an existing `./triage/triage-*.md`. **Rename** that file to the current `{datetime}` and rewrite its contents with the refreshed analysis, so the latest triage always carries the present timestamp and no stale-named copies are left behind.

## Report Format

### Executive Summary
- Total issues analyzed
- Issue count by priority (CRITICAL, HIGH, MEDIUM, LOW)
- Major themes discovered
- Top 5 critical issues requiring immediate attention

### Critical Issues (CRITICAL Priority)
For each CRITICAL issue:
- **#123 - [Issue Title](url)**
- **What it's about:** [Deep understanding]
- **Affected:** [Components]
- **Why Critical:** [Rationale]
- **Suggested Action:** [Specific action]

### High Priority Issues (HIGH Priority)
Same format as Critical, grouped by theme.

### Theme Clusters
For each major theme:
- **Theme Name** (N issues)
- **What connects these:** [Pattern]
- **Root cause:** [If identifiable]
- **Consolidated actions:** [Bulk actions if applicable]
- **Issues:** #123, #456, #789

### Relationships & Dependencies
- **Duplicates:** List pairs with `gh issue close` commands
- **Related Issues:** Groups of related issues
- **Dependencies:** Blocking relationships

### Cross-Repo Issues
Issues that should be migrated to other repositories.

For each, provide:
```
gh issue close XXX --repo CURRENT_REPO --comment "This issue belongs in REPO. Please report at https://github.com/TARGET_REPO/issues/new"
```

### Cleanup Candidates
- **v4-related:** Deprecated version issues with close commands
- **Stale:** No activity >30 days
- **Low priority + old:** Low priority issues >60 days old

### Actionable Next Steps
Specific, prioritized actions:
1. [CRITICAL] Fix broken installer - affects all new users
2. [HIGH] Resolve Windows path escaping issues
3. [HIGH] Address workflow integration bugs
etc.

Include `gh` commands where applicable for bulk actions.
