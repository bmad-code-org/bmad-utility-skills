# **Ergonomic Architectures for Agentic Code Review: State-of-the-Art Local Diff Affordances (2024–2026)**

The transition from traditional, human-authored software development to agentic coding loops has introduced a fundamental shift in the primary bottleneck of the engineering lifecycle. In the contemporary landscape of 2024 through 2026, the challenge has pivoted from the generation of code to its verification.1 Agentic systems, characterized by tools such as Claude Code, Cursor, and various CLI-based reasoning models, possess the capability to autonomously plan, execute, and iterate on complex multi-file modifications.3 However, the sheer volume and structural density of these machine-generated diffs often overwhelm standard human-in-the-loop (HITL) review mechanisms. The phenomenon of reviewer fatigue, exacerbated by the austerity of raw terminal output, necessitates a sophisticated analysis of the state-of-the-art (SOTA) in local diff review affordances. This report examines the technical mechanisms, ergonomic advantages, and human-computer interaction (HCI) strategies employed to facilitate high-fidelity, local pre-commit reviews, ranging from terminal-native terminal user interfaces (TUIs) to opinionated integrated development environment (IDE) escalation protocols.

## **The Cognitive Crisis of Machine-Generated Diffs**

The fundamental problem identified by developer experience (DevEx) researchers in late 2024 is the qualitative difference between human and AI-authored commits. A human developer typically produces changes that follow a linear narrative of intent, often constrained by a limited number of files and logical steps.6 Conversely, an AI agent may touch twenty or more files in a single session, intermingling security-critical logic changes with boilerplate scaffolding and formatting updates.6 This "cognitive blast radius" renders the standard top-to-bottom git diff review untenable for complex tasks.6

The industry's response has been the emergence of "vibe coding"—a paradigm where developers express high-level intent in natural language and delegate the implementation entirely to the agent.2 While this has led to a perceived 80% increase in productivity for some professionals, actual software delivery throughput increases have been measured at a more modest 2% to 3%, frequently coupled with a 10% increase in delivery instability.8 The resulting instability is largely attributed to the failure of the human review process to catch subtle "hallucinations" or logical errors that pass syntactic checks but fail to align with the developer's original intent.9 Consequently, the local review loop—the period between code generation and the first commit—has become the most critical intervention point for DevEx engineering.

## **Terminal-Native and TUI State-of-the-Art**

For power users who prioritize high-velocity terminal workflows, the evolution of the TUI has provided a middle ground between the primitive less pager and the heavyweight GUI IDE. The current SOTA for terminal-native diffing is characterized by tools that emphasize side-by-side rendering, syntax highlighting, and interactive hunk management.

### **High-Performance Pagers: The Delta Standard**

The standard-bearer for terminal-native diff enhancement is git-delta (often simply called delta). As a high-performance, Rust-based syntax-highlighting pager, delta transforms the unified diff format into a readable document that approximates the clarity of a modern web interface.10

| Tool | Primary Ergonomic Advantage | Language Support | Mechanism |
| :---- | :---- | :---- | :---- |
| **git-delta** | Side-by-side view with line numbers and syntax highlighting. | Multi-language (via Bat/Tree-sitter themes). | Rust-native pager for git/diff output.11 |
| **difftastic** | Structural comparison using Tree-sitter to ignore formatting noise. | 30+ programming languages. | AST-based structural diffing.12 |
| **lazygit** | Multi-panel TUI for interactive staging and hunk-level patching. | Universal Git integration. | Go-based TUI for complex Git workflows.7 |
| **difi** | Minimalist two-pane view with file tree navigation and editor jumping. | Go-based fast start. | Clean side-by-side view with vim-style navigation.14 |
| **git-split-diffs** | Syntax-highlighted side-by-side diffs mimicking GitHub's UI. | Syntax-aware. | Node-based pager for terminal side-by-side.10 |

The ergonomic core of delta lies in its sophisticated handling of horizontal space in constrained terminal environments. In side-by-side mode, delta activates line numbering and ensures that syntax highlighting is maintained in both the left (original) and right (modified) panels.11 A critical technical hurdle for terminal side-by-side views is line wrapping. If a line in the left panel wraps, it must not overflow into the right panel. Delta addresses this by implementing context-aware wrapping where wrapped content is right-aligned or left-aligned with specific arrow markers and ellipses (↵) to denote the continuation of a single logical line.11 This prevents the "visual drift" that occurs when mismatched line counts in the two panels cause the reviewer to lose track of the corresponding code logic.

### **Interactive Review Workflows: Lazygit and Difi**

While delta improves the *legibility* of diffs, tools like lazygit and difi focus on the *interactivity* of the review. Lazygit utilizes a set of consistent visual "boxes" or views—status, branches, commits, and stash—that remain visible during the review process.7 This minimizes context switching, as the developer can see the repository's broader state while inspecting specific diffs.

A significant ergonomic feature of lazygit is its native patch editing flow. Rather than forcing a binary "stage all" or "stage file" decision, lazygit allows the user to select specific lines or hunks within a file and move them into a new commit using mnemonic shortcuts (e.g., 2 space A P to select, add, and push).7 This is particularly relevant for agentic loops where an agent may have performed both a core refactor and a set of unrelated formatting changes. The ability to separate these into discrete commits via a TUI reduces the cognitive load of ensuring commit hygiene.18

Difi, a newer entrant developed in Go, addresses the "file tree" problem often missing from terminal diffs. While a raw git diff outputs files sequentially, difi presents a file tree on the left and the diff on the right, allowing the reviewer to jump between files non-linearly.14 It also implements an "editor jump" protocol where pressing e opens the specific file at the exact line number in Neovim or Vim, facilitating immediate manual correction of agent errors.14

## **Structural vs. Line-Based Diffing: The Tree-Sitter Paradigm**

A primary source of reviewer fatigue in agentic workflows is the "noise" generated by automated formatters (e.g., Prettier, Black, Clang-Format) that agents often invoke. Standard line-based diff algorithms, such as Myers or Patience, operate on raw text and can interpret a simple indentation change as a total deletion and re-addition of a code block.19 This forces the human reviewer to manually "de-noise" the diff in their mind to identify the actual semantic change.

### **The Mechanics of Semantic Diffs**

The state-of-the-art approach to this problem is structural diffing, exemplified by tools like difftastic and diffsitter. These tools leverage the Tree-sitter library to parse source code into an Abstract Syntax Tree (AST) before performing the comparison.12

| Feature | Line-Based (Myers/Patience) | Structural (Tree-sitter) |
| :---- | :---- | :---- |
| **Unit of Change** | Raw lines of text. | Syntax nodes (functions, loops, variables). |
| **Formatting Noise** | High; whitespace/indentation trigger diffs. | Low; structural tools ignore non-semantic changes.12 |
| **Complexity** | **![][image1]** where ![][image2] is length, ![][image3] is edit size. | High; requires parsing and tree-matching algorithms. |
| **Contextual Awareness** | Low; no understanding of language syntax. | High; understands delimiters and wrappers.13 |

Source: 12

Difftastic demonstrates this ergonomic advantage by identifying that an inner expression remains unchanged even if the surrounding code has been reformatted or wrapped in a new control structure (e.g., an if block or a try-catch statement).12 It matches delimiters exactly and displays the actual line numbers from the files, rather than the confusing @@ \-5,6 \+5,7 @@ hunk headers of standard diffs.12 To manage the computational overhead of AST parsing, difftastic implements a DFT\_BYTE\_LIMIT (or \--byte-limit) that triggers a fallback to line-oriented diffing if a file is too large or contains excessive parse errors, ensuring the TUI remains responsive.13

### **High-Fidelity Highlighting in Neovim**

The Neovim community has produced sophisticated implementations like vscode-diff.nvim, which brings VS Code’s specific diffing algorithm into the terminal.21 This tool uses a custom C engine parallelized with OpenMP to calculate diffs asynchronously, preventing the editor UI from freezing during large reviews.22 Its primary ergonomic advantage is a two-tier highlighting system that strictly separates line-level changes from character-level changes, aligning "filler lines" precisely so the code logic matches up visually on both sides of the screen.22 This level of precision is critical for reviewing agentic refactors where subtle character changes—such as a changed variable name in a complex boolean expression—might be missed in a standard terminal highlight.

## **CLI-to-IDE Escalation Protocols: The "Bridge"**

Despite the advancements in TUIs, complex agentic modifications involving multi-file dependencies often necessitate the comprehensive navigation and type-checking capabilities of a GUI IDE. The transition from a terminal-based agent loop to a GUI diff view—the "ejection" or "escalation" protocol—must be seamless and programmatic to maintain the agentic context.

### **Programmatic IDE Triggering and Flags**

Modern IDEs provide specific command-line flags to trigger ephemeral diff views. These commands are essential for agentic tools to provide a "Review in IDE" affordance.

* **VS Code / Cursor**: The \--diff flag is the standard mechanism.  
  * code \--wait \--diff \<file\_a\> \<file\_b\>  
  * cursor \--diff \<file\_a\> \<file\_b\> The \--wait flag is particularly critical; it tells the terminal to pause the agentic loop until the user closes the diff window in the IDE, allowing the human to approve or reject the change before the agent continues to the next step.23  
* **JetBrains (IntelliJ, WebStorm, PyCharm)**: The diff subcommand allows for file and folder comparison.  
  * idea diff \<path\_1\> \<path\_2\> \[\<path\_3\>\] JetBrains supports a three-way viewer, where \<path\_3\> can represent the common base version in merge conflict scenarios. This is often configured via the IDE settings under "Menus and Toolbars" to allow the IDE to act as an external diff tool for the global git config.24  
* **Neovim**: For terminal users who prefer a GUI-like diff experience within their existing editor, the \-d flag is used.  
  * nvim \-d \<file\_1\> \<file\_2\> Neovim also supports vertical splits via :vertical diffsplit \<filename\>, which is essential for comparing a modified buffer against its on-disk original.25

### **Management of Temporary File States**

A technical bottleneck in the escalation protocol is managing the state of files before they are committed. Since agents work in the local environment, they must present the proposed changes without overwriting the "known good" state until the user approves.

One emerging pattern is the use of /tmp or hidden .diff directories to store the agent's proposed versions.18 For instance, Cursor's agent mode applies edits to the local filesystem as it works, but it maintains "checkpoints" that can be restored with a single click ("Restore Checkpoint").26 This is essentially an automated git stash and git apply loop that manages the temporary state of the directory.18

Claude Code introduces a specialized /desktop command that initiates a technical handoff of the terminal session to the Claude Desktop application.4 This handoff allows the user to review diffs visually in a dedicated GUI that supports inline comments and line-by-line feedback, which is then sent back to the CLI agent as a structured JSON object for further iteration.27

## **Emerging Patterns for Mapping AI "Intent" to Diffs**

The most significant advancement in 2025–2026 is the development of "intent-aware" diffing. Standard diff tools show *what* changed, but they do not explain *why*. Modern agentic tools attempt to bridge this gap by mapping the agent's planning phase to the resulting code hunks.

### **Manifests and Rule Systems as Context Layers**

Agents now rely on project-specific configuration files—CLAUDE.md, .cursorrules, or AGENTS.md—to understand the architectural intent of a repository.3

| Manifest File | Functionality | Scope |
| :---- | :---- | :---- |
| **CLAUDE.md** | Sets coding standards, architecture decisions, and review checklists.4 | Project-wide. |
| **.cursorrules** | Defines rules for specific file types or directory paths to guide agent behavior.29 | Directory-specific or Project-wide. |
| **AGENTS.md** | Provides structured knowledge organization designed to be portable across agents.3 | Project-wide. |

These manifests allow the agent to self-verify its diffs against the project's stated goals before presenting them to the human. For example, if CLAUDE.md specifies that "all new API endpoints must include rate-limiting middleware," the agent can review its own diff for that requirement.4 This reduces the cognitive burden on the human reviewer, as the agent can pre-filter its output for common pattern violations.

### **Intent-Aware Verification Engines: Kluster.ai**

A noteworthy development in the local review loop is the emergence of tools like kluster.ai. Unlike traditional static analysis tools that look for syntax errors, kluster.ai uses an "intent engine" to compare the AI's output against the developer's original prompt and the existing repository context.9 It provides feedback in approximately five seconds, catching "hallucinations" or logical errors where the code is syntactically correct but functionally misaligned with the human's request.9 This represents the high-water mark for "intent-aware" diffing in 2025, as it transforms the diff review from a manual line-check into a semantic validation of the AI's logic.

## **HCI Principles in Diff Review: Reducing Reviewer Fatigue**

HCI research into agentic coding has identified several key design principles that mitigate reviewer fatigue. The most effective local review loops prioritize the following affordances:

1. **Significance Categorization**: Diffs should be categorized by security tier. Files handling authentication or database queries require line-by-line review, while UI styling changes can be reviewed as a high-level summary.6  
2. **Context Preservation**: Escalation protocols (like /desktop or code \--diff) must preserve the agent's chat history and reasoning. A diff without the prompt that generated it is significantly harder to verify than one that includes the agent's plan.4  
3. **Parallel Staging**: Power users increasingly utilize multiple agent sessions in parallel. Tools that support "multi-root" diff views or "virtual buffers" allow a human to review three or four independent feature implementations simultaneously without mixing the changes.4  
4. **Asynchronous Verification**: The "verify-as-you-work" pattern in Cursor allows a human to watch diffs appear in real-time and interrupt the agent if it heads in the wrong direction.18 This "early exit" affordance is critical for preventing the generation of massive, unreviewable changesets.

## **Implementation Details for Programmatic Escalation**

For DevEx engineers building custom agentic loops, the following technical reference documents the precise command-line signatures for the most common GUI escalation targets.

### **VS Code and Cursor Integration**

The VS Code CLI is the most common target for ejection. It requires the code binary to be in the system $PATH.

* **Standard Diff**: code \--diff path/to/original.ts path/to/proposed.ts  
* **Wait Protocol**: code \--wait \--diff file1 file2 (This blocks the terminal until the window is closed).  
* **Insiders Handoff**: code-insiders \--diff file1 file2  
* **Custom User Data**: code \--user-data-dir /tmp/agent-session \--diff file1 file2 (Isolates the agent's diff view from the user's primary IDE settings).

### **JetBrains Protocol**

JetBrains IDEs use a single executable that handles different commands. The diff command is highly optimized for folder comparisons.

* **File Compare**: idea diff file1.java file2.java  
* **Folder Compare**: idea diff dir1/ dir2/ (Opens the specialized "Diff Viewer for Folders").24  
* **Three-Way Merge**: idea merge file1 file2 base result (Used for resolving complex agentic merge conflicts).23

### **Neovim Diff Mode**

Neovim provides the most lightweight escalation for terminal-heavy users.

* **Basic Diff**: nvim \-d file1 file2  
* **Horizontal Split**: nvim \-d \-o file1 file2  
* **Read-Only Mode**: nvim \-d \-R file1 file2 (Prevents accidental edits during the review process).25  
* **Jumping between Hunks**: Use \]c for the next change and \[c for the previous change.25

## **Conclusion: The Future of the Human-in-the-Loop Loop**

As we progress through 2026, the bottleneck of human verification in agentic coding loops remains the primary target for innovation. The evolution of local diff affordances has moved through three distinct phases: first, the enhancement of legibility through high-performance pagers like delta; second, the shift from line-based to structural comparison via AST-based tools like difftastic; and third, the emergence of intent-aware verification through manifest files and specialized verification agents.9

The current state-of-the-art is a multi-modal experience where the developer stays in the terminal for routine changes, utilizing sophisticated TUIs like lazygit, but seamlessly "ejects" to a GUI IDE for complex structural reviews using programmatic escalation protocols. The integration of "intent" into the diff view—where the agent’s reasoning is displayed alongside the code hunks—represents the most promising path forward for reducing reviewer fatigue and maintaining software quality in the age of AI. For the DevEx engineer, the goal is not to eliminate the human from the loop, but to provide the ergonomic infrastructure that makes the human's verification task as high-signal and low-friction as possible.

#### **Works cited**

1. Testing AI coding agents (2025): Cursor vs. Claude, OpenAI, and Gemini | Render Blog, accessed on March 13, 2026, [https://render.com/blog/ai-coding-agents-benchmark](https://render.com/blog/ai-coding-agents-benchmark)  
2. Generative AI and the Transformation of Software Development Practices \- arXiv.org, accessed on March 13, 2026, [https://arxiv.org/html/2510.10819v1](https://arxiv.org/html/2510.10819v1)  
3. Codified Context: Infrastructure for AI Agents in a Complex Codebase \- arXiv.org, accessed on March 13, 2026, [https://arxiv.org/html/2602.20478v1](https://arxiv.org/html/2602.20478v1)  
4. Claude Code overview \- Claude Code Docs, accessed on March 13, 2026, [https://code.claude.com/docs/en/overview](https://code.claude.com/docs/en/overview)  
5. Best AI Coding Tools for Developers in 2026 \- Builder.io, accessed on March 13, 2026, [https://www.builder.io/blog/best-ai-tools-2026](https://www.builder.io/blog/best-ai-tools-2026)  
6. How to Review Code from AI Agents | VibeEval, accessed on March 13, 2026, [https://vibe-eval.com/agentic-coding-security/agentic-code-review-guide](https://vibe-eval.com/agentic-coding-security/agentic-code-review-guide)  
7. The (lazy) Git UI You Didn't Know You Need \- @bwplotka, accessed on March 13, 2026, [https://www.bwplotka.dev/2025/lazygit/](https://www.bwplotka.dev/2025/lazygit/)  
8. What happened in the last few months (1 to 3\) that suddenly people are having their come to Jesus moment with AI and Agentic Coding? : r/ExperiencedDevs \- Reddit, accessed on March 13, 2026, [https://www.reddit.com/r/ExperiencedDevs/comments/1p6lyoq/what\_happened\_in\_the\_last\_few\_months\_1\_to\_3\_that/](https://www.reddit.com/r/ExperiencedDevs/comments/1p6lyoq/what_happened_in_the_last_few_months_1_to_3_that/)  
9. Top 12 Automated Code Review Tools for 2025 \- kluster.ai, accessed on March 13, 2026, [https://kluster.ai/blog/automated-code-review-tools](https://kluster.ai/blog/automated-code-review-tools)  
10. Diff Terminal Tools \- Terminal Trove, accessed on March 13, 2026, [https://terminaltrove.com/categories/diff/](https://terminaltrove.com/categories/diff/)  
11. git-delta \- crates.io: Rust Package Registry, accessed on March 13, 2026, [https://crates.io/crates/git-delta/0.10.1](https://crates.io/crates/git-delta/0.10.1)  
12. Difftastic, a structural diff, accessed on March 13, 2026, [https://difftastic.wilfred.me.uk/](https://difftastic.wilfred.me.uk/)  
13. GitHub \- Wilfred/difftastic: a structural diff that understands syntax, accessed on March 13, 2026, [https://github.com/Wilfred/difftastic](https://github.com/Wilfred/difftastic)  
14. I built a TUI tool to make reviewing git diffs less painful \- Reddit, accessed on March 13, 2026, [https://www.reddit.com/r/git/comments/1qrugir/i\_built\_a\_tui\_tool\_to\_make\_reviewing\_git\_diffs/](https://www.reddit.com/r/git/comments/1qrugir/i_built_a_tui_tool_to_make_reviewing_git_diffs/)  
15. mmueller2012/awesome-diff-tools \- GitHub, accessed on March 13, 2026, [https://github.com/mmueller2012/awesome-diff-tools](https://github.com/mmueller2012/awesome-diff-tools)  
16. dandavison/delta: A syntax-highlighting pager for git, diff ... \- GitHub, accessed on March 13, 2026, [https://github.com/dandavison/delta](https://github.com/dandavison/delta)  
17. Context-aware line wrapping · Issue \#657 · dandavison/delta \- GitHub, accessed on March 13, 2026, [https://github.com/dandavison/delta/issues/657](https://github.com/dandavison/delta/issues/657)  
18. Reviewing and Testing Code | Cursor Learn, accessed on March 13, 2026, [https://cursor.com/learn/reviewing-testing](https://cursor.com/learn/reviewing-testing)  
19. Explore AST based diff tools, diff minimisation, etc · Issue \#3 · 0xdevalias/chatgpt-source-watch \- GitHub, accessed on March 13, 2026, [https://github.com/0xdevalias/chatgpt-source-watch/issues/3](https://github.com/0xdevalias/chatgpt-source-watch/issues/3)  
20. Making Sense of Code Changes with diff \- OpenReplay Blog, accessed on March 13, 2026, [https://blog.openreplay.com/sense-code-changes-diff/](https://blog.openreplay.com/sense-code-changes-diff/)  
21. diff visual select against registers/files with diff.nvim : r/neovim \- Reddit, accessed on March 13, 2026, [https://www.reddit.com/r/neovim/comments/1p8telt/diff\_visual\_select\_against\_registersfiles\_with/](https://www.reddit.com/r/neovim/comments/1p8telt/diff_visual_select_against_registersfiles_with/)  
22. I built vscode-diff.nvim: A C-powered plugin to bring VSCode's exact ..., accessed on March 13, 2026, [https://www.reddit.com/r/neovim/comments/1p5t0x0/i\_built\_vscodediffnvim\_a\_cpowered\_plugin\_to\_bring/](https://www.reddit.com/r/neovim/comments/1p5t0x0/i_built_vscodediffnvim_a_cpowered_plugin_to_bring/)  
23. Command Line Interface (CLI) \- Visual Studio Code, accessed on March 13, 2026, [https://code.visualstudio.com/docs/configure/command-line](https://code.visualstudio.com/docs/configure/command-line)  
24. Compare files, folders, and text sources | IntelliJ IDEA Documentation, accessed on March 13, 2026, [https://www.jetbrains.com/help/idea/comparing-files-and-folders.html](https://www.jetbrains.com/help/idea/comparing-files-and-folders.html)  
25. Diff \- Neovim docs, accessed on March 13, 2026, [http://neovim.io/doc/user/diff/](http://neovim.io/doc/user/diff/)  
26. Agent mode | Cursor Docs, accessed on March 13, 2026, [https://cursor.com/help/ai-features/agent](https://cursor.com/help/ai-features/agent)  
27. Use Claude Code Desktop \- Claude Code Docs, accessed on March 13, 2026, [https://code.claude.com/docs/en/desktop](https://code.claude.com/docs/en/desktop)  
28. Technical Code Review Protocol | Claude Code Skill \- MCP Market, accessed on March 13, 2026, [https://mcpmarket.com/tools/skills/technical-code-review-protocol-1](https://mcpmarket.com/tools/skills/technical-code-review-protocol-1)  
29. Using Agent in CLI | Cursor Docs, accessed on March 13, 2026, [https://cursor.com/docs/cli/using](https://cursor.com/docs/cli/using)  
30. Best Practices for Claude Code, accessed on March 13, 2026, [https://code.claude.com/docs/en/best-practices](https://code.claude.com/docs/en/best-practices)

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADkAAAAWCAYAAAB64jRmAAACQ0lEQVR4Xu2WzatOURTGH0UiUSK6omSgDPwBBsyQTG5ioshEJhiJgUwoE2VCiYm4klIGBpSZP4AkGch3JB/FRCIf+2nt3Vnvc9Y+552ITvdXq/vu51lr733uPnufDUwzzeCYpUIHP1T4X5mZ4lmK3ylupbiaf1/3SQEPU2xWMcN6H8oJ9Od8QzvHx4cmtZvZsIJJ0edmvdbR0RSfVRTWopnQNfEI3xh6q9UQon8CF+ZM1leKN8J9tIs95UG5Yp4ZWe/jY/4bTbKwQwVhKaz2heiFuzB/kRrkIMy8oYYQTfB2iu+iRZS68+63Z54KAWdhtbvUyGyC+eHWiiYfEeWxfVo0hav91LVZc8m1yUlpR/xCe3xP2RKtrXMRZjwXPaL2kMtFUw6k2OnaL9HuZ5yTORrfsw/ms/8RSuE2NYS9aA+yRNo1Pkl7Iaxuu9P6+lkMy3mihoPnBXP0LWlNvEbJ8xMre6CPKMePuzXFKedFPIblT6jhqD5L1XDwWI7ytgRaxAUVEq9gtYdS3Esxf9RuEY2v0H+gIhm3mLFG9FVZ7yPaszzmS7/j9NGXdw4dPo9/mnzna9A/rGKGHk/PGutUcJSJ932C9sDy+PmJWAHz56hRKDeNt2rAbhL09qvhoL9BRccjFRzc36znta6Ld7C8ZWqgWcEpNZSNsMQ3uc3r3eWsHS9JFZhzU8XEezQrxeAdOKJrBY6l+Immj6+wb+AXNN/M1ykWlIK/xXrYYIOHD7lbxaFRrlOD50iKOyoOkSsq/Gv+AE1uu72sgwWwAAAAAElFTkSuQmCC>

[image2]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA8AAAAWCAYAAAAfD8YZAAAAq0lEQVR4XmNgGAUg8B8JX0eTAwFkeayAkIJ4BtxyDK+AOJMBouAjmhwIlAJxAbogDGRAaZjtjEhyIPAeixgG2MQA0bwZTRynk9PQ+Oh+ZwLiF0h8FPAcjQ9yIrLmIgZMC+AAm5NAYuuQ2FiBDhAvRhcEgqsMCE04NW8AYlV0QSDgZoBoWgjE89Dk4ACnqQyIgJNBlwABXgbiNKOARCQJrAqgAJRwcMmNAmIAAJnCM1yK62TgAAAAAElFTkSuQmCC>

[image3]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAXCAYAAAA7kX6CAAAAs0lEQVR4XmNgGHmAC4j/48F/gbgYrhoLAEmCFKIDPwaEIVjBfQY8kgx45PCaCgQ30AVgAKTpN7ogEpiILgACMH90oUsggQ3oAiBwhgGikR9dAgn8QRcAAUL+AwEMeV6o4CV0CSSQwoBFYwdUMARdAglgdRHI7RiCSGAhA0TeEl0Cq2lQ0MoAkStCl3CBSjxHEy9kgKRRkJwKskQdAySyYbaBMEjhLyD+BsT7gNgMrnoUEAYAzKA4vltMDloAAAAASUVORK5CYII=>