# BMad Utility Skills Plugin

Utility skills for BMad Method contributors - issue triage, changelog drafting, and release automation.

## Installation

### Option 1: Install directly from GitHub

```bash
cd /path/to/your/project
claude plugin install github:bmad-code-org/bmad-utility-skills
```

### Option 2: Install from local path

```bash
cd /path/to/your/project
claude plugin install /path/to/bmad-utility-skills
```

### Option 3: Add via marketplace

Add to your project's `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "bmad-tools": {
      "source": {
        "source": "github",
        "repo": "bmad-code-org/bmad-utility-skills"
      }
    }
  },
  "enabledPlugins": {
    "bmad-utility-skills@bmad-tools": true
  }
}
```

## Skills

After installation, restart Claude Code. The following skills will be available:

| Skill | Invocation | Description |
|-------|------------|-------------|
| GitHub Issue Triage | `bmad-utility-skills:gh-triage` | AI-powered issue triage with deep analysis and clustering |
| Draft Changelog | `bmad-utility-skills:draft-changelog <project>` | Generate changelog drafts for BMad projects |
| Release BMad Module | `bmad-utility-skills:release-bmad-module <project>` | Automate BMad module releases |

## Requirements

- Claude Code 1.0.33 or later
- `gh` GitHub CLI (for gh-triage)
- `npm` (for release-bmad-module)
- Git repository

## Usage Examples

```bash
# Triage GitHub issues
bmad-utility-skills:gh-triage

# Draft changelog for bmad-builder
bmad-utility-skills:draft-changelog bmad-builder

# Release a new version
bmad-utility-skills:release-bmad-module cis
```

## License

MIT

## Author

bmad-code-org
