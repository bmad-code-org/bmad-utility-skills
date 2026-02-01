---
name: draft-changelog
description: Analyzes changes since the last release and generates a draft changelog entry for BMad projects (bmad-builder, cis, game-dev-studio)
disable-model-invocation: true
---

# Draft Changelog

Analyzes changes since the last release and generates a draft changelog entry for any BMad project.

## Usage

```
bmad-utility-skills:draft-changelog <project-name>
```

Where `<project-name>` is one of:
- `bmad-builder`
- `cis` (Creative Intelligence Suite)
- `game-dev-studio`

## What This Skill Does

1. **Identifies current state**: Finds the last published tag and current version
2. **Launches Explore agent**: Thoroughly investigates all changes since the last release
3. **Generates draft changelog**: Creates a well-formatted changelog entry based on the analysis
4. **Returns the draft**: Presents the draft for review/editing (does not modify any files)

## Directory Paths

Projects are located at:
- bmad-builder: `/Users/brianmadison/dev/bmad-code/bmad-builder`
- cis: `/Users/brianmadison/dev/bmad-code/cis`
- game-dev-studio: `/Users/brianmadison/dev/bmad-code/game-dev-studio`

## Implementation

### Step 1: Identify Project and Current State
- Map the project name to its directory path
- Get the latest published tag: `git -C <project-dir> tag --sort=-version:refname | head -1`
- Get the current package.json version: `git -C <project-dir> show <tag>:package.json | grep version`
- Verify there are commits since the last tag: `git -C <project-dir> log <tag>..HEAD --oneline`

### Step 2: Launch Explore Agent

Launch an Explore agent with **thoroughness: "very thorough"** to investigate changes since the last tag.

**Provide the Explore agent with:**
- Project directory path
- Last tag (e.g., v0.1.3)
- Current HEAD

**Ask the Explore agent to analyze:**

1. **All commits** since the last tag:
   ```bash
   git log <last-tag>..HEAD --pretty=format:"%h %s%n%b" --no-merges
   ```

2. **Files changed** with statistics:
   ```bash
   git diff <last-tag>..HEAD --stat
   ```

3. **Specific areas to investigate**:

   **Core module files:**
   - `src/module-help.csv` - workflow descriptions, codes, structure changes
   - `src/module.yaml` - module metadata
   - `package.json` - dependencies, version changes

   **Agents:**
   - New agents added?
   - Existing agents modified?
   - Changes to agent personas, menus, prompts?
   - Agent schema validation changes?

   **Workflows:**
   - New workflows added?
   - Existing workflows modified?
   - Workflow phase changes (anytime vs phased)?
   - Changes to workflow instructions or templates?

   **Documentation:**
   - README changes?
   - New documentation?
   - Updated examples?

   **Infrastructure:**
   - Test changes?
   - Build/tooling updates?
   - CI/CD changes?
   - Dependencies updated?

4. **Categorize changes by type:**
   - 🎁 **Features** - New functionality, new agents, new workflows
   - 🐛 **Bug Fixes** - Fixed bugs, corrected issues
   - ♻️ **Refactoring** - Code improvements, reorganization
   - 📚 **Documentation** - Docs updates, README changes
   - 🔧 **Maintenance** - Dependency updates, tooling, infrastructure
   - 💥 **Breaking Changes** - Changes that may affect users

**Ask the Explore agent to provide:**
- A comprehensive summary of ALL changes
- Categorization of each change
- Identification of breaking changes
- Significance assessment (major/minor/trivial)

### Step 3: Generate Draft Changelog

Based on the Explore agent's findings, generate a changelog entry in this format:

```markdown
## v0.X.X - [Date]

* [Change 1 - categorized by type]
* [Change 2]
* [Change 3]
```

**Changelog formatting guidelines:**
- Use present tense ("Fix bug" not "Fixed bug")
- Start with the most significant changes first
- Group related changes together
- Use clear, concise language
- Include technical details when relevant
- For user-facing changes, explain the impact
- For breaking changes, clearly indicate what breaks

**Example entries:**
- `* Add new brainstorming workflow with 5 ideation frameworks`
- `* Fix: Update jest to ^30.2.0 to resolve installation failure`
- `* Improve module-help.csv descriptions with "Use when..." clauses for better LLM comprehension`
- `* Move Correct Course workflow from anytime to 4-production phase`
- `* Breaking: Change agent schema to require metadata.module field`

### Step 4: Present the Draft

Show the user:

```
📦 Draft Changelog for <project-name>

Current version: <version>
Last tag: <tag>
Commits since last release: <count>

📋 Proposed changelog for v0.X.X:

<generated changelog>

---
Options:
- Type "edit" to modify the changelog
- Type "add" to add more items
- Type "retry" to re-run the analysis
- Type "copy" to copy this to clipboard (for use with release skill)
- Or just close this when done
```

## Important Notes

- This skill does NOT modify any files - it only analyzes and drafts
- The draft can be copied and passed to the release-bmad-module skill
- Always use explicit directory paths: `git -C <project-dir> <command>`
- If no commits are found since the last tag, inform the user

## Output Format

Return the draft changelog as plain text that can be easily copied or passed to another skill.
