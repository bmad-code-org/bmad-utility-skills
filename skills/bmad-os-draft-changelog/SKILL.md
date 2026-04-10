---
name: bmad-os-draft-changelog
description: "Analyzes changes since last release and updates CHANGELOG.md ONLY. Use when users requests 'update the changelog' or 'prepare changelog release notes'"
---

# Draft Changelog Execution

## ⚠️ IMPORTANT - READ FIRST

**This skill ONLY updates CHANGELOG.md. That is its entire purpose.**

- **DO** update CHANGELOG.md with the new version entry
- **DO** present the draft for user review before editing
- **DO NOT** trigger any GitHub release workflows
- **DO NOT** run any other skills or workflows automatically
- **DO NOT** make any commits

After the changelog is complete, you may suggest the user can run `/bmad-os-release-module` if they want to proceed with the actual release — but NEVER trigger it yourself.

## Input
Project path (or run from project root)

## Step 1: Identify Current State

### 1a: Check for Marketplace Plugin Metadata

Look for `.claude-plugin/marketplace.json` in the project root. If found, read it to understand plugin versioning:

```json
{
  "plugins": [
    { "name": "plugin-a", "version": "1.2.0" },
    { "name": "plugin-b", "version": "2.0.1" }
  ]
}
```

**Single plugin:** Use its version as the changelog version. Confirm with the user: *"marketplace.json shows plugin-name at vX.Y.Z. Drafting changelog for this version - correct?"*

**Multiple plugins:** Ask the user which plugin(s) need changelog entries and what the new version(s) will be. Each plugin gets its own section in the changelog (see Step 3 format).

**No marketplace.json found:** Fall back to git tags for versioning (original behavior).

### 1b: Determine Version Boundaries

- Get the latest released tag (or, for marketplace repos, the last changelog entry for the relevant plugin)
- Get current/target version
- Verify there are commits since the last release

## Step 2: Launch Explore Agent

Use `thoroughness: "very thorough"` to analyze all changes since the last release tag.

**Key: For each merge commit, look up the merged PR/issue that was closed.**
- Use `gh pr view` or git commit body to find the PR number
- Read the PR description and comments to understand full context
- Don't rely solely on commit merge messages - they lack context

**Analyze:**

1. **All merges/commits** since the last tag
2. **For each merge, read the original PR/issue** that was closed
3. **Files changed** with statistics
4. **Categorize changes:**
   - 🎁 **Features** - New functionality, new agents, new workflows, improvements
   - 💥 **Breaking Changes** - Changes that may affect users
   - Anything else that doesn't fit the above categories can be listed as "Other Changes" or similar that are interesting for users to know but don't fit the above categories.

**Provide:**
- Comprehensive summary of ALL changes with PR context
- Categorization of each change
- Identification of breaking changes
- Significance assessment (major/minor/trivial)

## Step 3: Generate Draft Changelog

**Single-plugin or tag-based repos:**
```markdown
## vX.Y.Z - [Date]

* [Change 1 - categorized by type]
* [Change 2]
```

**Multi-plugin repos** (when marketplace.json has multiple plugins):
```markdown
## plugin-name - vX.Y.Z - [Date]

* [Change 1 - categorized by type]
* [Change 2]

## other-plugin - vA.B.C - [Date]

* [Change 3]
```

Each plugin gets its own H2 section. Only include plugins that actually have changes. Changes that affect shared code or the repo generally should be listed under whichever plugin(s) they impact.

**Guidelines:**
- Present tense ("Fix bug" not "Fixed bug")
- Most significant changes first
- Group related changes
- Clear, concise language
- For breaking changes, clearly indicate impact

## Step 4: Present Draft & Update CHANGELOG.md

Show the draft with current version, last tag, commit count, and options to edit/retry.

When user accepts:
1. Update CHANGELOG.md with the new entry (insert at top, after `# Changelog` header) and open the file for the user to review the changes.
2. Suggest: *"When ready, you can run `/bmad-os-release-module` to create the actual release."* but do NOT trigger it yourself.
3. STOP. That's it. You're done.

**DO NOT:**
- Trigger any GitHub workflows
- Run any other skills
- Make any commits
- Do anything beyond updating CHANGELOG.md
