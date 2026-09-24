# av-human-review Implementation Plan

## Big Picture

The verification bottleneck in agentic workflows is not correctness — machine hardening handles that. The bottleneck is **design confidence**: the human's ability to look at a committed change and judge whether it's the right solution for the system, not just a working one. Today, that judgment happens by staring at a raw diff with no context, no sequencing, and no conversation. The result is rubber-stamping or exhaustion.

`av-human-review` exists to activate design judgment. It does this by treating the human's attention as the scarcest resource in the system and structuring everything around it: loading context before showing code, organizing the walkthrough by concern rather than by file, surfacing risk that isn't visible in the diff, and staying quiet once the human is thinking.

The skill operates in two layers. The **document layer** is a self-sufficient review trail embedded in the tech spec — ordered `file:line` stops with framing, sequenced for comprehension, including rejected alternatives. A competent dev can review from this alone. The **conversation layer** is the skill itself, adding interactive depth: detail pass, targeted re-reviews, testing nudge, on-demand Q&A. Spec is the 90% solution; skill is the 10% power tool. (Design decisions 10, 12)

The work spans two artifacts: evolving quick-dev's spec and step 5 to produce the trail, and building the review skill that consumes it.

### Architecture

The skill uses step-file architecture (introduced in Phase 2):

- `SKILL.md` — frontmatter, role, standing rules, config loading, chains to step 1
- `step-01-orientation.md` — entry point + orientation output (Phase 2)
- `step-02-walkthrough.md` — concern-ordered walkthrough (Phase 3)
- `step-03-detail-pass.md` — risk-weighted deep spots (Phase 4)
- `step-04-testing.md` — observable behavior suggestions (Phase 5)

---

## Phase 1 — Quick-dev step 5: Suggested Review Order generation and presentation

Four stories:

### Story 1.1 — Generate the Suggested Review Order ✅

**Intent:** Step 5 has the diff and the spec context — enough to build a concern-ordered trail of clickable `file:line` stops with brief framing, optimized for human comprehension. Add instructions to step 5 to generate this trail and append it to the spec as a Suggested Review Order section before committing. The existing Code Map stays as-is for its original purpose. The Suggested Review Order is a separate, post-implementation artifact. Must be useful without any skill — a developer reading the spec can click through the stops and understand the change top-down. (Design decisions 10, 11; guiding-thoughts on intent-to-implementation traceability)

**Files modified:**
- `step-05-present.md` — added Suggested Review Order generation before commit (PR #2033, merged)

### Story 1.2 — VS Code opening ergonomics

**Intent:** Figure out how to open the spec (with the Suggested Review Order) in VS Code so the user can click through `file:line` links and navigate the change. The trail's value depends on clickable links working — this story validates that the format and the editor integration actually deliver the promised ergonomic. (Design decision 11; SOTA report on CLI-to-IDE escalation protocols)

### Story 1.3 — Editor cascade and presentation fallback

**Intent:** Not every user has VS Code. Step 5 needs a customizable "open in" mechanism with a cascade of fallbacks: Antigravity if available, VS Code if not, terminal display if neither, or at minimum tell the user where the file is and how to open it. The cascade should be configurable but work out of the box with sensible defaults. (SOTA report on CLI-to-IDE escalation protocols)

### Story 1.4 — Research: diff-view links via GitLens

**Intent:** The Suggested Review Order links currently open the final file at a line. A better review experience would open the *diff view* of the commit at that line — showing what changed, not just the end state. GitLens has a `gitlens://` URI scheme that may support deep-linking to commit diffs at specific lines. Research whether this is possible, what the URI format is, and whether step 5 could optionally emit GitLens-compatible links when the extension is detected. If viable, this upgrades the review trail from "navigate the code" to "navigate the change." Story 1.2 found that `code --diff` works from CLI but doesn't support line targeting.

---

## Phase 2 — Skill entry + orientation ✅

**Intent:** Build the skill's front door: a lenient entry point that assesses what artifacts exist (full spec with trail, partial spec, bare commit, nothing) and fills gaps before starting the review. Then produce orientation output: the intent summary plus a surface area stat line (files changed, modules touched, lines of logic, boundary crossings, new public interfaces). Orientation loads the *why* before any code is shown. The entry point must handle the full spectrum from "spec produced by quick-dev" to "commit from an unknown source" to "user just wants to talk about a vague change." (Design decisions 2, 3, 14, 15, 17, 18; guiding-thoughts on cognitive throttling and handoff gap)

**What was built:**
- `SKILL.md` — replaced placeholder with role, standing rule (`path:line` format), config loading, chain to step 1
- `step-01-orientation.md` — entry assessment, review mode detection, orientation output (intent + stats), inline Suggested Review Order display with path resolution
- `step-02-walkthrough.md` — placeholder with gist
- `step-03-detail-pass.md` — placeholder with gist
- `step-04-testing.md` — placeholder with gist

**Design deviations from original plan:**
- Renamed skill from `av-hitl-review` to `av-human-review` — old name was jargon
- Entry starts from conversation context (not a spec-first scan) — avoids false positives from unrelated specs
- Spec intent displayed verbatim regardless of length (200-token cap only for unstructured sources like commit messages)
- Suggested Review Order displayed inline in terminal with path resolution to current repo, not opened in editor — skill runs inside the IDE already
- After orientation offers `code review`, `advanced elicitation`, `party mode`, or chat

---

## Phase 3 — Walkthrough presentation ✅

**Intent:** Implement the main event: present the full review trail (orientation + walkthrough) as a single front-loaded dump, organized by concern not by file, with every code reference as a clickable `file:line` link. After presenting, the skill goes quiet — human reads, clicks, navigates at their own pace. Skill only speaks again when the human signals they're done or asks a question. This is the "front-load then shut up" principle — minimize agent-initiated turns, maximize human thinking time. (Design decisions 4, 5, 7, 9, 11, 20, 21; guiding-thoughts on topological comprehension and epistemic friction)

**What was built:**
- `step-02-walkthrough.md` — replaced placeholder with full walkthrough logic: concern identification (with/without Suggested Review Order), comprehension ordering, concern-group format (heading + why + stops), front-load-then-shut-up presentation, phase transition to detail pass

---

## Phase 4 — Detail pass

**Intent:** Add the optional, human-triggered detail pass. The skill identifies 2-5 highest-stakes spots in the diff, weighted by risk over complexity — a trivial change to auth matters more than a complex change to logging, because complexity is visible in the diff but risk context isn't. Each spot is one line: clickable `file:line`, short risk tag (e.g. `[auth]`, `[public API]`, `[schema]`), one-phrase reason. Also surface any findings from machine hardening (including borderline/rejected) and enable targeted re-reviews: human spots the area of concern, LLM hammers the details. This is where the correctness review lives, benefiting from the design review having already loaded the full mental model. Treat effectiveness as experimental — iterate based on real use. (Design decisions 6, 9, 13; guiding-thoughts on epistemic friction and agency-mastery gap)

**Files to modify:**
- `step-03-detail-pass.md` — replace placeholder with detail pass logic

---

## Phase 5 — Testing nudge

**Intent:** Add the optional, human-triggered testing nudge phase. Not about CI or test suites (assumed handled). Not "you should test this" but "you could see this working." If the change has user-visible behavior, tell the human how they could observe it — what commands to run, what to click, what output to expect. Human decides whether it's worth their time. This is separate from the detail pass because it serves a different cognitive function: detail pass is analytical ("did you think about X?"), testing nudge is experiential ("you could see this with your own eyes"). (Design decisions 9, 19; SOTA report on asynchronous verification patterns)

**Files to modify:**
- `step-04-testing.md` — replace placeholder with testing nudge logic

---

## Phase 6 — Fallback trail generation

**Intent:** Make the skill work on any change from any source, not just quick-dev output. When no spec with an embedded trail exists — hand-written code, a different agent, a lost spec — the skill builds the trail itself from the diff and codebase context. This is slower and probably lower quality than an author-produced trail, but far better than no trail. The skill already assesses available artifacts in step-01; this phase adds the "build it yourself" path when the assessment finds nothing. Ensures the skill's value proposition isn't gated on adoption of quick-dev. (Design decisions 2, 14, 15; handoff gap research on intent-to-implementation traceability without author cooperation)

**Files to modify:**
- `step-01-orientation.md` — add fallback trail generation when no Suggested Review Order exists

---

## Deferred

**Rejected Alternatives (design decision 16):** "The agent considered X but chose Y because Z" — directly activates design judgment. Requires step 2 and step 3 to record alternatives as they work, not just step 5 appending post-hoc. Needs design pass on how to capture this without burdening the implementation flow.

**Decision 8 (deviation-detection reviewer):** Promising but unproven. Needs a dedicated research pass on whether LLMs can reliably flag pattern deviations without creating automation bias on the significance filter itself. Explicitly excluded per the design document's own instruction: "DO NOT ship without that research."

**Decision 22 (visual structural representations):** Mermaid diagrams and dependency graphs are valuable for multi-module changes but "how and when to generate them is a whole separate subject." Not v1.

**Rename advanced elicitation skill:** "Advanced elicitation" is jargon. The skill name should describe what it does in plain language.

---

## Verification

Each phase can be validated independently:
- **Phase 1:** Run quick-dev on a small change, inspect the spec — does it have a Suggested Review Order section with ordered `file:line` stops and framing?
- **Phase 2:** Invoke the skill with (a) a full spec, (b) a bare commit, (c) no artifacts — does it assess correctly and produce orientation?
- **Phase 3:** Invoke with a full spec — does it present a coherent walkthrough organized by concern, then go quiet?
- **Phase 4:** After walkthrough, trigger detail pass — does it surface risk-weighted spots with one-liner format?
- **Phase 5:** Trigger testing nudge — does it suggest observable behavior for user-visible changes?
- **Phase 6:** Invoke on a commit with no spec — does it build a reasonable trail from the diff?
