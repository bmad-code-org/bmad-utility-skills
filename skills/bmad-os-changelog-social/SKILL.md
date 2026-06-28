---
name: bmad-os-changelog-social
description: Generate social media announcements for Discord, Twitter/X, Facebook, and LinkedIn from the latest changelog entry. Use when user asks to 'create release announcement' or 'create social posts' or share changelog updates.
---

# Changelog Social

Generate engaging social media announcements from changelog entries. This skill uses **progressive disclosure**: identify which platform(s) the user wants, then read only that platform's guide in `references/`.

## Output

Write each platform's announcement to **`{project-root}/.social/{social-type}/post.md`**, where `{social-type}` is one of `discord`, `twitter`, `facebook`, `linkedin`. Create the folders as needed; overwrite the platform's `post.md` to refresh it.

## Step 1: Identify What We're Announcing

### 1a: Check for Marketplace Plugin Metadata

Look for `.claude-plugin/marketplace.json` in the project root. If found, read it to understand what plugins exist and their versions.

**Single plugin:** The announcement is for that plugin specifically. Use its name and version in all posts (e.g., "bmad-utility-skills v1.2.0" not just "BMad v1.2.0").

**Multiple plugins:** Ask the user which plugin(s) they're announcing. Each plugin should be named specifically in the posts.

**No marketplace.json:** Fall back to repo name and git tags.

### 1b: Handle Multi-Changelog Announcements

The user may want to announce across multiple changelogs at once (e.g., releases in two repos the same week). If the user provides multiple changelog paths or mentions multiple repos:

- Read all specified changelogs
- Ask: *"Generate separate announcement batches per plugin, or combine into one unified announcement set?"*
- **Separate:** Generate a full set of posts per plugin
- **Combined:** Weave highlights from all releases into one announcement set, naming each plugin where relevant

### 1c: Extract Changelog Entry

Read `./CHANGELOG.md` and extract the latest version entry. The changelog may use either format:

**Standard format:**
```markdown
## [VERSION]

### 🎁 Features
* **Title** — Description
```

**Multi-plugin format:**
```markdown
## plugin-name - vX.Y.Z - [Date]

* Change description
```

Parse:
- **Plugin/module name** (from marketplace.json or changelog header)
- **Version number** (e.g., `6.0.0-Beta.5`)
- **Features** - New functionality, enhancements
- **Bug Fixes** - Fixes users will care about
- **Documentation** - New or improved docs
- **Maintenance** - Dependency updates, tooling improvements

## Step 2: Get Git Contributors

Use git log to find contributors since the previous version. Get commits between the current version tag and the previous one:

```bash
# Find the previous version tag first
git tag --sort=-version:refname | head -5

# Get commits between versions with PR numbers and authors
git log <previous-tag>..<current-tag> --pretty=format:"%h|%s|%an" --grep="#"
```

Extract PR numbers from commit messages that contain `#` followed by digits. Compile unique contributors.

## Step 3: Find the Sizzle (collaborate — do NOT generate yet)

The difference between a flat release note and a post that *sizzles* is knowing what to put **top-of-fold**. This is a conversation to craft the headline *with* the user — it is **not** a dump of the full post in chat.

1. From the changelog, identify the **1–3 changes you think are the real headline** — the standout, "lead with this" material — and separate them from the supporting/lesser detail.
2. **Prove you understand them.** Reflect each candidate headline back in your own words — what it actually does and *why a user should be excited* — not a restatement of the changelog line. e.g. *"The breakout looks like X: it means people can finally do Y without Z. The rest — A, B, C — are solid but supporting."*
3. **Ask the user to confirm or re-rank:** *"Is that the breakout you want to lead with, or is there something here you're more pumped to push?"* Pull on the angle/hook with them.
4. Lock in: the agreed **headline(s)**, the **hook/angle**, and what's demoted to lesser detail.

Only once the headline and angle are agreed do you move to generation — every platform post then leads with that sizzle.

## Step 4: Pick Target Platform(s) & Generate

Ask the user which platform(s) they want — `discord`, `twitter`, `facebook`, `linkedin`, or `all`. For **each chosen platform**, read its guide and follow it exactly. Load only the guide(s) for the platform(s) in play:

| Platform  | Guide                    | Notes                                          |
| --------- | ------------------------ | ---------------------------------------------- |
| Discord   | `references/discord.md`  | Hard 2,000-character limit                      |
| Twitter/X | `references/twitter.md`  | Series of standalone, schedulable tweets        |
| Facebook  | `references/facebook.md` | Article-style thought piece                      |
| LinkedIn  | `references/linkedin.md` | Major/minor releases with significant features  |

Each guide carries that platform's rules, template, and a pointer to its example.

**Before you draft, read `references/writing-quality.md` and apply its Tier 1 (Universal AI tells)** — banned vocabulary, "it's not X, it's Y", honesty preambles, weapons imagery, stakes inflation. **Do NOT apply Tier 2 (long-form prose mechanics):** social copy keeps its punch — fragments, short lines, emoji, and rule-of-three are on-format here, not errors.

## Step 5: Writing-Quality Pass (subagent)

Before finalizing, run a quality pass with a **subagent** (Task tool, `subagent_type=general-purpose`). Hand it the drafted post(s) and `references/writing-quality.md`, and instruct it to apply **Tier 1 only** — hunt every Universal AI tell (banned vocabulary, metanoia "it's not X, it's Y", hypophora, honesty preambles, weapons imagery, stakes inflation, sycophancy residue) and return concrete fixes. **Tell it explicitly NOT to apply Tier 2** — fragments, short punchy lines, and rule-of-three are correct for social and must survive the pass. Apply the fixes.

Then write each refined result to `{project-root}/.social/{platform}/post.md` (for combined multi-plugin announcements, weave all plugins into that platform's single `post.md`), present a short preview per platform in the chat (include Discord's character count), and offer to adjust emphasis, tone, or content.

## Content Selection Guidelines

**Include:**
- New features that change workflows
- Bug fixes for annoying/blocking issues
- Documentation that helps users
- Performance improvements
- New agents or workflows
- Breaking changes (call out clearly)

**Skip/Minimize:**
- Internal refactoring
- Dependency updates (unless user-facing)
- Test improvements
- Minor style fixes

**Emphasize:**
- "Finally fixed" issues
- "Faster" operations
- "Easier" workflows
- "Now supports" capabilities
