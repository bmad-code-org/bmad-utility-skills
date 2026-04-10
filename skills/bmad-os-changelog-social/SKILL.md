---
name: bmad-os-changelog-social
description: Generate social media announcements for Discord, Twitter/X, Facebook, and LinkedIn from the latest changelog entry. Use when user asks to 'create release announcement' or 'create social posts' or share changelog updates.
---

# Changelog Social

Generate engaging social media announcements from changelog entries.

## Workflow

### Step 1: Identify What We're Announcing

#### 1a: Check for Marketplace Plugin Metadata

Look for `.claude-plugin/marketplace.json` in the project root. If found, read it to understand what plugins exist and their versions.

**Single plugin:** The announcement is for that plugin specifically. Use its name and version in all posts (e.g., "bmad-utility-skills v1.2.0" not just "BMad v1.2.0").

**Multiple plugins:** Ask the user which plugin(s) they're announcing. Each plugin should be named specifically in the posts.

**No marketplace.json:** Fall back to repo name and git tags.

#### 1b: Handle Multi-Changelog Announcements

The user may want to announce across multiple changelogs at once (e.g., releases in two repos the same week). If the user provides multiple changelog paths or mentions multiple repos:

- Read all specified changelogs
- Ask: *"Generate separate announcement batches per plugin, or combine into one unified announcement set?"*
- **Separate:** Generate a full set of posts (Discord, Twitter, Facebook, LinkedIn) per plugin
- **Combined:** Weave highlights from all releases into one announcement set, naming each plugin where relevant

#### 1c: Extract Changelog Entry

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

### Step 2: Get Git Contributors

Use git log to find contributors since the previous version. Get commits between the current version tag and the previous one:

```bash
# Find the previous version tag first
git tag --sort=-version:refname | head -5

# Get commits between versions with PR numbers and authors
git log <previous-tag>..<current-tag> --pretty=format:"%h|%s|%an" --grep="#"
```

Extract PR numbers from commit messages that contain `#` followed by digits. Compile unique contributors.

### Step 3: Generate Discord Announcement

**Hard limit: 2,000 characters per message** (Discord free account max). This includes spaces, line breaks, markdown formatting characters, and emoji shortcodes. You MUST count the final output and verify it is under 2,000 characters. If a single message would exceed the limit, split into multiple messages and label them (e.g., "1/2", "2/2").

**Priority when trimming to fit:** Cut "Community Philosophy", "Speaking & Media", and "Stats" sections first. Never cut the install command, support links, or contributor shout-outs.

Use this template style:

```markdown
🚀 **PLUGIN-NAME vVERSION RELEASED!**

🎉 [Brief hype sentence]

🪥 **KEY HIGHLIGHT** - [One-line summary]

🎯 **CATEGORY NAME**
• Feature one - brief description
• Feature two - brief description
• Coming soon: Future teaser

🔧 **ANOTHER CATEGORY**
• Fix or feature
• Another item

📚 **DOCS OR OTHER**
• Item
• Item with link

🌟 **COMMUNITY PHILOSOPHY** (optional - include for major releases)
• Everything is FREE - No paywalls
• Knowledge shared, not sold

📊 **STATS**
X commits | Y PRs merged | Z files changed

🙏 **CONTRIBUTORS**
@username1 (X PRs!), @username2 (Y PRs!)
@username3, @username4, username5 + dependabot 🛡️
Community-driven FTW! 🌟

📦 **INSTALL:**
`npx bmad-method@VERSION install`

⭐ **SUPPORT US:**
🌟 GitHub: github.com/bmad-code-org/BMAD-METHOD/
📺 YouTube: youtube.com/@BMadCode
☕ Donate: buymeacoffee.com/bmad

🔥 **Next version tease!**
```

**Content Strategy:**
- Focus on **user impact** - what's better for them?
- Highlight **annoying bugs fixed** that frustrated users
- Show **new capabilities** that enable workflows
- Keep it **punchy** - use emojis and short bullets
- Add **personality** - excitement, humor, gratitude

### Step 4: Generate Twitter/X Posts

Generate a **series of standalone tweets** designed to be scheduled and spaced out over days. Each tweet should work on its own as an exciting announcement, not depend on the others.

**Tweet 1 - Release Announcement (flagship tweet):**
The main "we just released vX.Y.Z" tweet. High energy, top 2-3 highlights, install command, link to repo. This one goes out on release day.

**Tweets 2-N - Feature/Fix Spotlights:**
One tweet per noteworthy feature, improvement, or bug fix. Each should:
- Open with a hook (question, bold claim, or pain point solved)
- Describe the single feature/fix and why it matters
- End with a CTA (try it, star the repo, check the docs, etc.)
- Include relevant hashtags

**Guidelines:**
- Target **280 characters or fewer** per tweet (X free tier limit) so posts work for any account tier
- Generate **3-8 tweets** depending on how much is in the changelog
- Order them by impact/excitement so the best content posts first
- Each tweet should feel like its own mini-announcement, not a fragment
- Include a suggested posting schedule (e.g., "Day 1", "Day 2", "Day 3") to space them out

See `examples/twitter-example.md` for tone reference.

### Step 5: Generate Facebook Article Post

Generate a Facebook post formatted as a short article or thought piece. Rather than a bullet-point feature list, pick the **single most interesting thing** from the release and write about it as a topic worth discussing.

**Approach:**
- Choose the most compelling feature, fix, or theme from the changelog
- Frame it as a mini-article: what problem does it solve, why does it matter, what does it mean for the space?
- Write it as if you're sharing an insight or lesson learned, not just announcing a version bump
- The release details are secondary context, not the headline

**Guidelines:**
- **Aim for 500-1,500 characters** - Facebook rewards longer, thoughtful posts
- Conversational, first-person voice - write as BMad sharing thoughts with the community
- Plain text only (Facebook doesn't render markdown) - use line breaks and emoji sparingly for structure
- End with a question or discussion prompt to drive comments
- Include the install command and GitHub link at the bottom, but keep them low-key
- Add 3-5 relevant hashtags at the end

**Template style:**

```
[Hook - an observation, question, or bold statement about the topic]

[2-3 paragraphs exploring the idea - what we built, why it matters, what we learned. This is the article body.]

[Tie it back to the release - "This is exactly why we built X in vVERSION"]

Try it out: npx bmad-method@VERSION install
More at github.com/bmad-code-org/BMAD-METHOD

[Discussion question]

#BMadMethod #AI #OpenSource #DevTools #Agile
```

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

## Examples

Reference example posts in `examples/` for tone and formatting guidance:

- **discord-example.md** — Plugin-specific Discord announcement under 2,000 chars
- **twitter-example.md** — Series of standalone tweets with posting schedule
- **facebook-example.md** — Article-style thought piece anchored to a release
- **linkedin-example.md** — Professional post for major/minor releases with significant features

**When to use LinkedIn:**
- Major version releases (e.g., v6.0.0 Beta, v7.0.0)
- Minor releases with exceptional new features
- Community milestone announcements

Read the appropriate example file before generating to match the established style and voice.

## Output Format

**CRITICAL: ALWAYS write to files** - Create files in `_bmad-output/social/` directory:

1. `{plugin-name}-discord-{version}.md` - Discord announcement
2. `{plugin-name}-twitter-{version}.md` - Series of standalone tweets with suggested schedule
3. `{plugin-name}-facebook-{version}.md` - Facebook post
4. `{plugin-name}-linkedin-{version}.md` - LinkedIn post (if applicable)

For combined multi-plugin announcements, use `combined-social-{date}.md` with all platforms in one file.

Also present a preview in the chat:

```markdown
## Discord Announcement
[Character count: X/2000]

[paste Discord content here]

## Twitter/X Posts
[X tweets, suggested schedule included]

[paste tweets here]

## Facebook Post

[paste Facebook content here]
```

Files created:
- `_bmad-output/social/{filename}`

Offer to make adjustments if the user wants different emphasis, tone, or content.
