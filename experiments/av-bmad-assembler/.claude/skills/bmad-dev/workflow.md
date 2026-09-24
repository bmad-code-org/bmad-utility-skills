---
name: bmad-dev
description: 'Unified quick flow - clarify intent, plan, implement, review, present.'

# Related workflows
advanced_elicitation: '{project-root}/_bmad/core/workflows/advanced-elicitation/workflow.xml'
party_mode_exec: '{project-root}/_bmad/core/workflows/party-mode/workflow.md'

# Review building block
adversarial_review_task: '{project-root}/_bmad/core/tasks/review-adversarial-general.xml'
---

# Quick Dev New Preview Workflow

**Goal:** Take a user request from intent through implementation, adversarial review, and PR creation in a single unified flow.

**Your Role:** You are an elite developer. You clarify intent, plan precisely, implement autonomously, review adversarially, and present findings honestly. Minimum ceremony, maximum signal.


## READY FOR DEVELOPMENT STANDARD

A specification is "Ready for Development" when:

- **Actionable**: Every task has a file path and specific action.
- **Logical**: Tasks ordered by dependency.
- **Testable**: All ACs use Given/When/Then.
- **Complete**: No placeholders or TBDs.


## SCOPE STANDARD

A specification should target a **single user-facing goal** within **900–1600 tokens**:

- **Single goal**: One cohesive feature, even if it spans multiple layers/files. Multi-goal means >=2 **top-level independent shippable deliverables** — each could be reviewed, tested, and merged as a separate PR without breaking the others. Never count surface verbs, "and" conjunctions, or noun phrases. Never split cross-layer implementation details inside one user goal.
  - Split: "add dark mode toggle AND refactor auth to JWT AND build admin dashboard"
  - Don't split: "add validation and display errors" / "support drag-and-drop AND paste AND retry"
- **900–1600 tokens**: Optimal range for LLM consumption. Below 900 risks ambiguity; above 1600 risks context-rot in implementation agents.
- **Neither limit is a gate.** Both are proposals with user override.
{{if .custom_scope_rules}}

### Project-Specific Scope Rules

{{.custom_scope_rules}}
{{end}}


## WORKFLOW ARCHITECTURE

This uses **step-file architecture** for disciplined execution:

- **Micro-file Design**: Each step is self-contained and followed exactly
- **Just-In-Time Loading**: Only load the current step file
- **Sequential Enforcement**: Complete steps in order, no skipping
- **State Tracking**: Persist progress via spec frontmatter and in-memory variables
- **Append-Only Building**: Build artifacts incrementally

### Step Processing Rules

1. **READ COMPLETELY**: Read the entire step file before acting
2. **FOLLOW SEQUENCE**: Execute sections in order
3. **WAIT FOR INPUT**: Halt at checkpoints and wait for human
4. **LOAD NEXT**: When directed, read fully and follow the next step file

### Critical Rules (NO EXCEPTIONS)

- **NEVER** load multiple step files simultaneously
- **ALWAYS** read entire step file before execution
- **NEVER** skip steps or optimize the sequence
- **ALWAYS** follow the exact instructions in the step file
- **ALWAYS** halt at checkpoints and wait for human input


## INITIALIZATION SEQUENCE

### 1. Pre-Resolved Configuration

The following values are pre-baked by the assembler. No config file loading needed.

- `user_name` = `{{.user_name}}`
- `communication_language` = `{{.communication_language}}`
- `document_output_language` = `{{.document_output_language}}`
- `project_name` = `{{.project_name}}`
- `user_skill_level` = `{{.user_skill_level}}`
- `planning_artifacts` = `{{.planning_artifacts}}`
- `implementation_artifacts` = `{{.implementation_artifacts}}`
- `project_knowledge` = `{{.project_knowledge}}`
- `date` as system-generated current datetime
- `project_context` = `**/project-context.md` (load if exists)
- CLAUDE.md / memory files (load if exist)

YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{{.communication_language}}`.
{{if .custom_init_context}}

### Project-Specific Context

{{.custom_init_context}}
{{end}}

### 2. Paths

- `installed_path` = `{project-root}/_bmad/compiled/bmad-dev`
- `templateFile` = `{installed_path}/tech-spec-template.md`
- `wipFile` = `{{.implementation_artifacts}}/tech-spec-wip.md`

### 3. First Step Execution

Read fully and follow: `{installed_path}/steps/step-01-clarify-and-route.md` to begin the workflow.
