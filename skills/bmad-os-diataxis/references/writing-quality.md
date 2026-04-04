# Writing Quality Reference

Complete pattern catalog for identifying and fixing AI-sounding prose in documentation. Use this reference when refining docs for prose quality.

Your job: read each target file, identify patterns from this reference, and make targeted Edit tool fixes. Preserve all meaning and technical accuracy. Never change structure, Diataxis type, or section organization — only improve the prose within existing sections.

## Banned Vocabulary

Replace these with plain, direct alternatives. Never use them in documentation:

**Inflated verbs:** delve, embark, leverage, utilize, facilitate, elevate, foster, harness, navigate (metaphorical), streamline, bolster, resonate, align

**Inflated adjectives:** robust, comprehensive, intricate, nuanced, multifaceted, cutting-edge, seamless, pivotal, paramount, invaluable, crucial, game-changing, revolutionary, transformative, fundamental (when hyperbolic)

**Filler transitions:** furthermore, moreover, notably, additionally, "it's worth noting," "it's important to note," "while there are many factors to consider"

**AI openers:** "In today's [X] landscape," "In the realm of," "Let's dive in," "Let's unpack," "Have you ever wondered," "Imagine a world where"

**AI closers:** "In conclusion," "To sum up," "In summary," "The future looks bright," "Exciting times ahead"

**Pompous substitutes:** "serves as" / "stands as" / "marks" / "represents" when "is" works. "utilize" when "use" works.

**False authority:** "Experts agree," "Industry reports suggest," "Studies show" without citation.

**False exclusivity:** "The part nobody talks about," "What most people miss," "The secret to."

## Rhetorical Patterns to Fix

### Metanoia / Correctio — "It's not X, it's Y"

The single most identified AI writing tell. Creates false profundity through reframing.

**Variants to watch for:**
- "It's not X, it's Y"
- "Not because X, but because Y"
- "X — not Y"
- "Not just X, but Y"
- Cross-sentence: negating a noun then repositioning it

**Fix:** State the point directly. If the contrast is genuinely informative, keep it but limit to one instance per document. If it's decorative, just say Y.

### Asyndetic Tricolon — Staccato Triplets

Three short punchy sentences (or phrases) in a row for manufactured emphasis. "Fast. Cheap. Reliable." or "Products impress, platforms empower, ecosystems transform."

**Fix:** Break the pattern. Combine two into one longer sentence. Rephrase as prose. One tricolon per document maximum, and only if it genuinely earns the emphasis.

### Amplificatio — Mirror and Extend

Restating what was just said in different words, then adding a small increment. Feels like progression while adding minimal information.

**Fix:** Delete the restatement. Keep only the new information. If the restatement is the clearer version, keep it and delete the original.

### Anaphora — Repetitive Openers

Multiple sentences or paragraphs starting with the same word or phrase. "They assume... They assume... They assume..."

**Fix:** Vary openers. Restructure so the repeated element appears in different positions, or consolidate into a single statement.

### Concessio — Both-Sides Hedging

"While X is true, Y is also important." Diplomatic equilibrium that avoids commitment even when the topic warrants a clear position.

**Fix:** Take a position. State the important thing first. If the counterpoint matters, give it its own sentence rather than a subordinate clause.

### Variatio — Synonym Cycling

Unnecessarily rotating synonyms to avoid repetition: "the system...the platform...the tool...the solution." Humans repeat the natural term.

**Fix:** Pick the most natural term and stick with it. Repetition of the right word is better than forced variation.

### Participial Coda — Significance Injection

Appending "-ing" phrases that add hollow weight: "...contributing to the overall effectiveness of the system."

**Fix:** Cut the participial tail. If the information matters, make it its own sentence. If it doesn't, delete it.

### Hypophora — Self-Posed Q&A

"The result? Devastating." Rhetorical question immediately answered for false drama.

**Fix:** Remove the question. State the point directly.

### Merism — False Ranges

"From innovation to implementation to cultural transformation" where endpoints lack a meaningful spectrum.

**Fix:** Name what you actually mean. If it's a list, use a list. If it's one thing, say one thing.

## Sentence Rhythm (Burstiness)

AI prose has metronomic cadence — sentences hover around the same length. Human writing alternates between short and long naturally.

**What to fix:**
- Three or more consecutive sentences of similar length — restructure so they vary
- All paragraphs roughly the same size — combine some, split others, let a one-sentence paragraph stand alone for emphasis
- Every paragraph following topic-sentence → support → summary structure — use anecdotes, questions, direct evidence, or fragments as paragraph openers instead

**What to aim for:**
- Short sentences next to long ones
- Paragraph lengths that vary visibly
- Occasional sentence fragments for emphasis
- Contractions where tone permits ("don't" over "do not")

## Transition Patterns to Fix

- **"Here's the kicker" / "Here's where it gets interesting"** — false suspense. Cut the preamble, state the point.
- **Academic connectives in casual context** — "Furthermore," "Moreover," "Additionally" where "and," "also," or nothing works better.
- **"The truth is simple"** — asserting obviousness instead of demonstrating it. Cut and let the content speak.
- **Numbered phase labels** — "Phase 1... Phase 2..." when describing a process in prose. Describe what happens, don't announce a numbered march.

## Formatting Patterns to Fix

- **Bold-first bullets everywhere** — Not every bullet needs a bolded lead phrase. Use them for scannable reference lists, not narrative content.
- **Title Case In All Headings** — Prefer sentence case unless the project style guide says otherwise.
- **Em dash overuse** — Max one per paragraph. Replace extras with commas, parentheses, periods, or restructure the sentence.
- **Over-structured short content** — If two paragraphs of prose would work, don't use headers, bullets, and tables.

## Tone Patterns to Fix

- **Stakes inflation** — Don't call routine things "game-changing" or "revolutionary." Reserve strong language for strong claims.
- **Patronizing analogies** — "Think of it like a highway for data." Trust the reader. If an analogy genuinely helps, use it once. Don't explain the explanation.
- **Sycophancy residue** — "Great question!" or "Certainly!" have no place in documentation.
- **Invented concept labels** — Fabricated compound terms ("supervision paradox," "acceleration trap") presented as established. Use plain descriptions.
- **Vague attribution** — "Experts argue" without naming experts. Either cite or remove.

## The Refinement Pass

When reviewing a file:

1. Read the full document to understand its intent and audience
2. Scan for banned vocabulary — replace with plain alternatives
3. Scan for rhetorical pattern overuse — apply the fixes above
4. Check sentence rhythm — ensure burstiness, break metronomic cadence
5. Check transitions — replace hollow connectives with substance or nothing
6. Check tone — deflate stakes inflation, cut patronizing explanations
7. Read the result aloud mentally — if any sentence sounds like it came from a "helpful AI assistant," rewrite it

Use the Edit tool for each fix. Present a per-file summary listing what was changed and why.
