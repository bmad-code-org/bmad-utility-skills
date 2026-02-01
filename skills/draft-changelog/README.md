# draft-changelog

Analyzes changes since the last release and generates a draft changelog entry.

## Usage

Run from project root or pass project path:
```
bmad-utility-skills:draft-changelog
```

## What It Does

1. Identifies current state (last tag, version)
2. Launches Explore agent to investigate changes since last release
3. Reads PR/issue descriptions for context (not just commit messages)
4. Generates draft changelog
5. Returns the draft for review (does not modify files)
