# Facebook Example - bmad-utility-skills v1.2.0

One of the most frustrating things about automated code review is getting the same finding reported three different ways.

You run two review passes and suddenly you're triaging ten items that are really four. The noise buries the signal, and the whole point of automation - saving time - gets lost in deduplication busywork.

We just shipped a fix for this in bmad-utility-skills v1.2.0. Our PR review tool (Raven's Verdict) now runs its cynical review and edge-case analysis in parallel, then merges and deduplicates the findings before you ever see them. Same thoroughness, dramatically less noise.

It's a small thing, but it's the kind of small thing that changes whether a tool actually gets used or just sits there. The best automation is the kind you don't have to clean up after.

Try it out: github.com/bmad-code-org/bmad-utility-skills

What's the most annoying "automation that creates more work" problem you've run into?

#BMadMethod #AI #OpenSource #DevTools #CodeReview
