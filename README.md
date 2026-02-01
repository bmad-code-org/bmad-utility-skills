# BMad Utility Skills Plugin

Utility skills for BMad Method contributors - issue triage, changelog drafting, and release automation.

## Quick Start

```bash
# From any BMad project directory
claude plugin marketplace add bmad-code-org/bmad-plugins-marketplace
claude plugin install --scope project bmad-utility-skills@bmad-plugins
```

Then **restart Claude Code**.

## Installation: User vs Project Scope

Plugins can be installed at two scopes - choose based on your needs:

### Project Scope (Recommended for Teams)

Installs the plugin for **this project only**. The configuration is saved to `.claude/settings.json` and can be committed to git.

```bash
claude plugin install --scope project bmad-utility-skills@bmad-plugins
```

**Use this when:**
- Working on a team project
- You want the plugin to be available to all contributors
- You want to commit the plugin configuration to version control

**After installation, commit these files:**
```bash
git add .claude/settings.json
git commit -m "Add bmad-utility-skills plugin"
```

### User Scope

Installs the plugin **globally for all your projects**. Configuration is saved to `~/.claude/settings.json`.

```bash
claude plugin install --scope user bmad-utility-skills@bmad-plugins
```

**Use this when:**
- You want the plugin available across all your personal projects
- You're the only developer working on your projects

**Note:** This is the default if `--scope` is omitted.

## Available Skills

After restarting Claude Code, the following skills are available:

| Skill | Command | Description |
|-------|---------|-------------|
| GitHub Issue Triage | `bmad-utility-skills:gh-triage` | AI-powered issue triage with deep analysis and clustering |
| Draft Changelog | `bmad-utility-skills:draft-changelog <project>` | Generate changelog drafts for BMad projects |
| Release BMad Module | `bmad-utility-skills:release-bmad-module <project>` | Automate BMad module releases |

## Usage Examples

```bash
# Triage GitHub issues in the current repo
bmad-utility-skills:gh-triage

# Draft changelog for bmad-builder
bmad-utility-skills:draft-changelog bmad-builder

# Draft changelog for cis
bmad-utility-skills:draft-changelog cis

# Release a new version of game-dev-studio
bmad-utility-skills:release-bmad-module game-dev-studio
```

## Setup for BMad Module Maintainers

To automatically enable this plugin for all contributors, add to your module's `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "bmad-plugins": {
      "source": {
        "source": "github",
        "repo": "bmad-code-org/bmad-plugins-marketplace"
      }
    }
  },
  "enabledPlugins": {
    "bmad-utility-skills@bmad-plugins": true
  }
}
```

Commit this to your repository and contributors will be prompted to install the plugin when they open the project.

## Requirements

- Claude Code 1.0.33 or later
- `gh` GitHub CLI (for gh-triage) - install from https://cli.github.com/
- `npm` (for release-bmad-module)
- Git repository

## Troubleshooting

**Plugin not found?**
```bash
# Add the marketplace first
claude plugin marketplace add bmad-code-org/bmad-plugins-marketplace

# Then install
claude plugin install --scope project bmad-utility-skills@bmad-plugins
```

**Skills not showing up?**
- Restart Claude Code after installing
- Check the plugin is installed: `claude plugin list`

**Want to remove the plugin?**
```bash
claude plugin uninstall bmad-utility-skills@bmad-plugins
```

## License

MIT

## Author

bmad-code-org
