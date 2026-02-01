---
name: release-bmad-module
description: Automates the complete release process for BMad modules (bmad-builder, cis, game-dev-studio) - version bump, changelog, git tag, npm publish, GitHub release
disable-model-invocation: true
---

# Release BMad Module

Automates the complete release process for BMad modules (bmad-builder, cis, game-dev-studio) after you've reviewed the changelog.

## Usage

```
bmad-utility-skills:release-bmad-module <project-name>
```

Where `<project-name>` is one of:
- `bmad-builder`
- `cis` (Creative Intelligence Suite)
- `game-dev-studio`

## Prerequisite

First run `bmad-utility-skills:draft-changelog <project-name>` to analyze changes and create a draft changelog. Then run this skill to complete the release.

## What This Skill Does

This skill guides you through the final steps of releasing a new version:

1. **Get Changelog**: Asks for the changelog entry (either from draft-changelog skill or manually written)
2. **Confirm Changelog**: Shows you the changelog and asks for confirmation
3. **Confirm Version**: Asks what type of version bump this should be (patch, minor, major, prerelease, etc.)
4. **Update CHANGELOG.md**: Commits the changelog to the repository
5. **Version Bump**: Runs `npm version` to update package.json, create commit, and create tag
6. **Push Tag**: Pushes the new version tag to GitHub
7. **Publish to npm**: Publishes the package to the npm registry
8. **Create GitHub Release**: Creates a GitHub release with the changelog notes

## Directory Paths

Projects are located at:
- bmad-builder: `/Users/brianmadison/dev/bmad-code/bmad-builder`
- cis: `/Users/brianmadison/dev/bmad-code/cis`
- game-dev-studio: `/Users/brianmadison/dev/bmad-code/game-dev-studio`

## Repository Mapping

| Project Name | Package Name | GitHub Repo |
|--------------|--------------|-------------|
| bmad-builder | bmad-builder | bmad-code-org/bmad-builder |
| cis | bmad-creative-intelligence-suite | bmad-code-org/bmad-module-creative-intelligence-suite |
| game-dev-studio | bmad-game-dev-studio | bmad-code-org/bmad-module-game-dev-studio |

## Implementation Steps

### Step 1: Get Current State
- Check the project directory exists
- Verify git working tree is clean: `git -C <project-dir> status --porcelain`
- Get latest tag: `git -C <project-dir> tag --sort=-version:refname | head -1`
- Get current version: `git -C <project-dir> show <tag>:package.json | grep '"version"'`
- Check for unpushed commits: `git -C <project-dir> log origin/main..HEAD --oneline`

### Step 2: Get Changelog Entry

Ask the user:
```
Please provide the changelog entry for this release.

You can:
1. Paste the output from bmad-utility-skills:draft-changelog
2. Type it manually
3. Type "cancel" to abort

Enter changelog:
```

### Step 3: Confirm Changelog

Show the user:
- Project name
- Current version
- Proposed next version (default: patch bump)
- The changelog entry they provided

Ask: "Does this look correct? (yes/edit/cancel)"

If "edit", allow them to modify it
If "yes", proceed
If "cancel", abort

### Step 4: Confirm Version Bump Type

Ask: "What type of version bump is this?

1. **patch** (0.1.3 → 0.1.4) - Bug fixes, small improvements
2. **minor** (0.1.3 → 0.2.0) - New features, backward compatible
3. **major** (0.1.3 → 1.0.0) - Breaking changes
4. **prerelease** (0.1.3 → 0.1.4-rc.0) - Pre-release version
5. **custom** (specify exact version)

Enter choice (1-5):"

Wait for user input, then calculate the new version:
- patch: increment last digit
- minor: increment middle digit, reset last to 0
- major: increment first digit, reset others to 0
- prerelease: append prerelease identifier
- custom: ask for specific version

### Step 5: Update CHANGELOG.md

1. Read existing CHANGELOG.md from project directory
2. Insert new entry at the top (after the `# CHANGELOG` header)
3. Use format:
   ```markdown
   ## vX.Y.Z - [Month DD, YYYY]

   * [Change 1]
   * [Change 2]
   ```
4. Stage and commit:
   ```bash
   cd <project-dir> && git add CHANGELOG.md && git commit -m "docs: update changelog for vX.Y.Z"
   ```
5. Push the commit: `cd <project-dir> && git push`

### Step 6: Bump Version

Run the appropriate npm version command:
```bash
cd <project-dir> && npm version [patch|minor|major|prerelease|X.Y.Z]
```

This automatically:
- Updates package.json (and package-lock.json)
- Creates a git commit
- Creates a git tag (vX.Y.Z)

### Step 7: Push Tag

```bash
cd <project-dir> && git push origin vX.Y.Z
```

### Step 8: Publish to npm

```bash
cd <project-dir> && npm publish
```

Wait for successful publication response.

### Step 9: Create GitHub Release

```bash
cd <project-dir> && gh release create vX.Y.Z \
  --title "vX.Y.Z" \
  --notes "<changelog-notes>" \
  --repo bmad-code-org/<repo-name>
```

Use the full changelog entry as the release notes.

### Step 10: Confirm Completion

Show the user:
```
✅ Release complete!

Project: <project-name>
Version: vX.Y.Z

📦 npm: https://www.npmjs.com/package/<package-name>
🐙 GitHub: https://github.com/bmad-code-org/<repo-name>/releases/tag/vX.Y.Z
```

## Error Handling

If any step fails:
- Stop immediately
- Inform the user of the error
- Show what step failed and why
- Do not continue to subsequent steps
- Suggest how to fix the issue

Common issues:
- Working tree not clean → Commit or stash changes first
- Tag already exists on remote → Use different version or force delete
- npm publish fails (403) → Version already published, use different version
- gh release fails (422) → Release already exists

## Important Notes

- **Always use explicit directory paths**: `cd <project-dir> && command`
  - This avoids Bash tool working directory confusion
- **Wait for user confirmation** before destructive operations (version bump, publish, release)
- **Always push changelog commit** before version bump (prevents tag from being rejected)
- **npm version** creates both commit AND tag automatically

## Example Session

```
bmad-utility-skills:release-bmad-module bmad-builder

📦 Releasing bmad-builder

Current version: 0.1.3
Latest tag: v0.1.3
Working tree: ✅ Clean

Please provide the changelog entry for this release.
[Paste changelog from draft-changelog skill]

✅ Proposed changelog for v0.1.4:

## v0.1.4 - Feb 1, 2026

* Improve module-help.csv descriptions with "Use when..." clauses
* Fix duplicate codes (CA -> AGC, VA -> AGV)
* Reorder workflows for logical flow
* Fix: Update jest to ^30.2.0

Does this look correct? (yes/edit/cancel) yes

What type of version bump is this?
1. patch (0.1.3 → 0.1.4)
2. minor (0.1.3 → 0.2.0)
3. major (0.1.3 → 1.0.0)
Enter choice (1-3): 1

[Proceeds with release steps...]

✅ Release complete!

Project: bmad-builder
Version: 0.1.4

📦 npm: https://www.npmjs.com/package/bmad-builder
🐙 GitHub: https://github.com/bmad-code-org/bmad-builder/releases/tag/v0.1.4
```

## Workflow Suggestion

For best results, use this workflow:

1. Make sure all changes are committed and pushed
2. Run `bmad-utility-skills:draft-changelog <project-name>` to analyze changes
3. Review the draft - make edits if needed
4. Run `bmad-utility-skills:release-bmad-module <project-name>` to complete the release
5. Paste the changelog from step 3 when prompted
