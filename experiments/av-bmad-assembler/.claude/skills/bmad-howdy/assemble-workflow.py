#!/usr/bin/env python3
"""assemble-workflow.py — BMAD Workflow Template Assembler

Pre-bakes workflow markdown files by resolving build-time {{.variables}}
from config files and custom overrides. Runtime {variables} (single curlies)
are preserved as-is for LLM execution.

Usage:
  python3 assemble-workflow.py [--force]

Discovers the project root by walking up from CWD looking for a _bmad/ directory.
"""

import argparse
import hashlib
import os
import re
import sys


def find_project_root():
    """Walk up from CWD looking for a _bmad directory — it must sit at the project root.

    First _bmad found wins. If it exists but is broken, fail with why.
    If none found all the way to filesystem root, fail with that.

    Cross-platform: works on macOS, Linux, and Windows.
    Follows symlinks — the resolved target must be a readable/writable directory."""
    current = os.path.abspath(os.getcwd())

    while True:
        candidate = os.path.join(current, "_bmad")

        if not os.path.lexists(candidate):
            # Nothing here — keep climbing
            parent = os.path.dirname(current)
            if parent == current:
                print(
                    f"error: no _bmad directory found searching from {os.getcwd()} to filesystem root",
                    file=sys.stderr,
                )
                sys.exit(1)
            current = parent
            continue

        # Found something named _bmad — this is THE one. Validate it.

        # If it's a symlink, the target must be reachable
        if os.path.islink(candidate):
            if not os.path.exists(candidate):
                real = os.readlink(candidate)
                print(
                    f"error: {candidate} is a symlink -> {real} but the target does not exist or is not accessible",
                    file=sys.stderr,
                )
                sys.exit(1)

        # Must resolve to a directory (follows symlinks)
        if not os.path.isdir(candidate):
            print(
                f"error: {candidate} exists but is not a directory",
                file=sys.stderr,
            )
            sys.exit(1)

        # Must be readable
        if not os.access(candidate, os.R_OK):
            print(
                f"error: {candidate} is a directory but is not readable",
                file=sys.stderr,
            )
            sys.exit(1)

        # Must be writable (compiler writes to _bmad/compiled/)
        if not os.access(candidate, os.W_OK):
            print(
                f"error: {candidate} is a directory but is not writable",
                file=sys.stderr,
            )
            sys.exit(1)

        return current


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))

    parser = argparse.ArgumentParser(description="BMAD Workflow Template Assembler")
    parser.add_argument(
        "--force", action="store_true", help="Force reassembly even if hash matches"
    )
    args = parser.parse_args()

    root = find_project_root()
    source_dir = script_dir
    workflow = os.path.basename(script_dir)

    # 1. Load config values
    vars_ = {}

    # Core config
    core_config = os.path.join(root, "_bmad", "config", "config.yaml")
    load_flat_yaml(core_config, vars_)

    # Module variables
    module_config = os.path.join(root, "_bmad", "config", "module.yaml")
    resolve_module_vars(module_config, vars_)

    # Custom overrides — wins over everything
    custom_config = os.path.join(root, "_bmad", "custom", workflow, "config-overrides.yaml")
    load_flat_yaml(custom_config, vars_)

    # 2. Collect input files for hashing
    output_dir = os.path.join(root, "_bmad", "compiled", workflow)
    hash_file = os.path.join(output_dir, ".hash")

    input_files = []

    # Source workflow .md files (excluding SKILL.md)
    for dirpath, _, filenames in os.walk(source_dir):
        for fname in filenames:
            if fname.endswith(".md") and fname != "SKILL.md":
                input_files.append(os.path.join(dirpath, fname))

    # Config files that affect output
    for f in (core_config, module_config, custom_config):
        if os.path.isfile(f):
            input_files.append(f)

    # 3. Hash check
    current_hash = hash_files(input_files)
    if not args.force:
        try:
            with open(hash_file, "r") as fh:
                if fh.read() == current_hash:
                    sys.exit(0)
        except FileNotFoundError:
            pass

    # 4. Assemble — process each .md through template substitution
    os.makedirs(output_dir, exist_ok=True)

    for dirpath, _, filenames in os.walk(source_dir):
        for fname in filenames:
            path = os.path.join(dirpath, fname)
            if not fname.endswith(".md") or fname == "SKILL.md":
                continue

            rel = os.path.relpath(path, source_dir)
            out_path = os.path.join(output_dir, rel)

            os.makedirs(os.path.dirname(out_path), exist_ok=True)

            with open(path, "r") as fh:
                content = fh.read()

            rendered = render_template(content, vars_)

            with open(out_path, "w") as fh:
                fh.write(rendered)

            print(f"  assembled: {rel}")

    # 5. Write hash
    with open(hash_file, "w") as fh:
        fh.write(current_hash)

    print(f"assembled workflow '{workflow}' -> {output_dir}")


def load_flat_yaml(path: str, vars_: dict) -> None:
    """Parse a simple YAML file with flat key: value pairs.
    Supports single-line values and multiline | blocks."""
    try:
        with open(path, "r") as fh:
            data = fh.read()
    except FileNotFoundError:
        return

    lines = data.split("\n")
    current_key = None
    multiline_value = []
    in_multiline = False
    multiline_indent = 0

    def flush_multiline():
        nonlocal current_key, multiline_value, in_multiline
        if current_key:
            vars_[current_key] = "\n".join(multiline_value).rstrip("\n")
            current_key = None
            multiline_value = []
            in_multiline = False

    for line in lines:
        trimmed = line.strip()

        # Skip comments and empty lines at top level
        if trimmed == "" or trimmed.startswith("#") or trimmed.startswith("---"):
            if in_multiline:
                multiline_value.append("")
            continue

        if in_multiline:
            indent = len(line) - len(line.lstrip(" "))
            if indent >= multiline_indent:
                multiline_value.append(line[multiline_indent:])
                continue
            # Dedent — flush and fall through
            flush_multiline()

        # Skip nested YAML (indented lines)
        if line.startswith(" ") or line.startswith("\t"):
            continue

        # Parse top-level key: value
        colon_idx = trimmed.find(":")
        if colon_idx < 0:
            continue

        key = trimmed[:colon_idx].strip()
        value = trimmed[colon_idx + 1 :].strip()

        if not key:
            continue

        # Multiline block scalar
        if value in ("|", "|+", "|-"):
            current_key = key
            multiline_value = []
            in_multiline = True
            multiline_indent = 2
            continue

        # Strip quotes
        value = value.strip("'\"")

        # Skip empty or complex values
        if not value or value.startswith("[") or value.startswith("{"):
            continue

        vars_[key] = value

    flush_multiline()


def resolve_module_vars(path: str, vars_: dict) -> None:
    """Extract and resolve known variable patterns from module.yaml."""
    try:
        with open(path, "r") as fh:
            data = fh.read()
    except FileNotFoundError:
        return

    lines = data.split("\n")

    known_vars = {
        "project_name",
        "user_skill_level",
        "planning_artifacts",
        "implementation_artifacts",
        "project_knowledge",
    }

    current_var = None
    var_defaults = {}
    var_results = {}

    for line in lines:
        trimmed = line.strip()

        # Top-level key (no indent)
        if not line.startswith(" ") and not line.startswith("\t") and ":" in trimmed:
            key = trimmed.split(":", 1)[0].strip().rstrip(":")
            current_var = key if key in known_vars else None
            continue

        if current_var is None:
            continue

        if trimmed.startswith("default:"):
            val = trimmed[len("default:") :].strip().strip("'\"")
            var_defaults[current_var] = val
        elif trimmed.startswith("result:"):
            val = trimmed[len("result:") :].strip().strip("'\"")
            var_results[current_var] = val

    # Resolve variable chains
    for name in known_vars:
        if name in vars_:
            continue

        default_val = var_defaults.get(name)
        if default_val is None:
            continue

        resolved = resolve_runtime_vars(default_val, vars_)

        result_pattern = var_results.get(name)
        if result_pattern:
            result = result_pattern.replace("{value}", resolved)
            vars_[name] = result
        else:
            vars_[name] = resolved


def resolve_runtime_vars(s: str, vars_: dict) -> str:
    """Substitute {var} references in a string using known vars.
    Leaves unresolved references (like {project-root}) as-is."""
    result = s
    for key, val in vars_.items():
        result = result.replace("{" + key + "}", val)
    # Also handle underscore/hyphen variants
    for key, val in vars_.items():
        hyphen_key = key.replace("_", "-")
        if hyphen_key != key:
            result = result.replace("{" + hyphen_key + "}", val)
    return result


def render_template(content: str, vars_: dict) -> str:
    """Resolve Go-style {{.variable}} placeholders and {{if .var}}...{{end}} blocks.
    Unresolved variables are replaced with empty string (matching Go's missingkey=zero).
    Conditional blocks are stripped entirely when the variable is empty/missing."""
    # First: resolve {{if .var}}...{{end}} conditional blocks
    # Use non-greedy match; handle nested by iterating until stable
    if_pattern = re.compile(r"\{\{if \.(\w+)\}\}(.*?)\{\{end\}\}", re.DOTALL)
    prev = None
    result = content
    while result != prev:
        prev = result
        def if_replacer(match):
            key = match.group(1)
            body = match.group(2)
            val = vars_.get(key, "")
            if val:
                return body
            return ""
        result = if_pattern.sub(if_replacer, result)

    # Then: resolve {{.variable}} simple substitutions
    def replacer(match):
        key = match.group(1)
        return vars_.get(key, "")

    return re.sub(r"\{\{\.(\w+)\}\}", replacer, result)


def hash_files(paths: list) -> str:
    """Compute a deterministic SHA-256 hash of all input files."""
    paths = sorted(paths)
    h = hashlib.sha256()
    for p in paths:
        try:
            with open(p, "rb") as fh:
                data = fh.read()
            h.update(p.encode())
            h.update(data)
        except FileNotFoundError:
            continue
    return h.hexdigest()


if __name__ == "__main__":
    main()
