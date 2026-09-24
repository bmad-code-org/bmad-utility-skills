# BMAD Assembler

A JIT prompt compiler for BMAD workflows. The skill carries its own templates and compiler — invoke the skill, it compiles, it executes.

## Architecture

Three concerns, cleanly separated:

### 1. Skill (portable, installed anywhere)

Lives wherever Claude Code resolves skills — `.claude/skills/bmad-dev/` in this repo, but could be a central install or symlinked. Doesn't matter.

Contents:
- `SKILL.md` — entry point Claude Code invokes
- `assemble-workflow.py` — the compiler
- `workflow.md` — master workflow template (with `{{.double-curly}}` build-time variables)
- `steps/` — step-file templates (step-01 through step-05)
- `tech-spec-template.md` — spec template used during planning

The skill is self-contained. The compiler discovers everything from its environment — no flags required.

### 2. Project `_bmad/` directory (project-root)

Everything BMAD-related in the target project lives under a single `_bmad/` directory:

```
_bmad/
  config/             # checked in — project-specific configuration
    config.yaml       #   core values (user name, language, skill level, etc.)
    module.yaml       #   variable definitions with defaults and resolution patterns
  custom/             # checked in — per-workflow overrides
    bmad-dev/
      config-overrides.yaml
  compiled/           # gitignored — compiler output
    bmad-dev/         #   compiled workflow with variables resolved, real paths baked in
  artifacts/          # gitignored — specs, WIPs, planning state
```

- **config/** and **custom/** are checked in. Different projects get different compiled workflows from the same skill.
- **compiled/** and **artifacts/** are gitignored. Rebuilt/generated during workflow execution.

## Compiler flow

```
skill-dir/templates  +  project-root/_bmad/config/  -->  project-root/_bmad/compiled/
```

```sh
python3 .claude/skills/bmad-dev/assemble-workflow.py [--force]
```

The script derives everything from its environment:
- **Skill directory**: from `__file__`
- **Workflow name**: from its parent directory name
- **Project root**: walks up from CWD looking for `_bmad/`

- Loads config from `{project-root}/_bmad/config/`
- Resolves `{{.double-curly}}` build-time variables in templates
- Writes compiled `.md` files to `{project-root}/_bmad/compiled/{workflow}/`
- Hashes all inputs; skips rebuild if nothing changed
- Single-curly `{runtime-vars}` pass through untouched for LLM execution

## Design principles

- **Zero dependencies**: The compiler uses only the Python 3 standard library. No pip, no virtualenv, no requirements.txt. If Python 3 exists on the machine, it runs. This is a hard rule — never add third-party library dependencies.
- **Zero-config invocation**: The compiler derives skill directory from `__file__`, workflow name from its parent directory, and project root by walking up from CWD to find `_bmad/`. No arguments required.
- **No magic tokens**: The compiler resolves `{project-root}` and similar placeholders to real absolute paths. The LLM never has to guess.
- **Hash-based caching**: JIT compilation is cheap — inputs are hashed and rebuilds are skipped when nothing changed.
- **Skill is the engine, project is the workspace**: The skill doesn't care where it's installed. It discovers its context from the environment.
