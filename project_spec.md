# Crules - Omni-Assistant Rules Generator

## Overview
A Python utility for managing and generating AI context rules simultaneously across **seven** assistants: Cursor, Claude Code, GitHub Copilot, Cline, Roo Code, Windsurf, and Aider. It acts as a context compiler, turning a single set of universal rules into the native formats each tool expects. **`crules --bootstrap`** deploys the Swarm skeleton (`.crules/` modes—including the Bootstrapper—task pipeline, `AGENTS.md`, and scaffolded `project_spec.md`) without a separate shell script.

## Core Features
1. **Multi-agent support**: Generates native directory structures and file formats for:
   - **Cursor** — `.cursor/rules/*.mdc` with `globs` frontmatter
   - **Claude Code** — `.claude/rules/*.md` with `paths` frontmatter (globstar style)
   - **GitHub Copilot** — `.github/instructions/*.instructions.md` with `applyTo` frontmatter
   - **Cline** — `.clinerules/*.md` with `globs`
   - **Roo Code** — `.roorules/*.md` with `globs`
   - **Windsurf** — `.windsurf/rules/*.md` with `globs`
   - **Aider** — `.aider/rules/*.md` with `globs`, plus append-only `read:` entries in root `.aider.conf.yml` so rules load into context
2. **Universal preamble**: Injects a standardized preamble (including the root `AGENTS.md` Bootstrapper gatekeeper) into every generated file.
3. **Metadata translation**: Maps globs into each tool’s YAML dialect (`globs`, `paths`, or `applyTo` as required).
4. **Swarm / Bootstrapper**: Repository-local `.crules/modes/` workflow files, `AGENTS.md` template state, and `project_spec.md` placeholders for stack discovery.

## Configuration
**Location**: `~/.config/crules/config.yaml`  
**Format** (booleans default to `true` when omitted for the seven `enable_*` keys):
```yaml
global_rules_path: "~/.config/crules/cursorrules"
language_rules_dir: "~/.config/crules/lang_rules"
enable_cursor: true
enable_claude: true
enable_copilot: true
enable_cline: true
enable_roo: true
enable_windsurf: true
enable_aider: true
delimiter: "\n# --- Delimiter ---\n"
```

**CLI**: Repeatable `--target` / `-t` (`cursor`, `claude`, `copilot`, `cline`, `roo`, `windsurf`, `aider`) restricts generation to specific assistants; with no `--target`, all seven default on via `setdefault`.

## Architecture
- **`ai_managers.py`**: `BaseAIManager` plus `CursorManager`, `ClaudeManager`, `CopilotManager`, `ClineManager`, `RooManager`, `WindsurfManager`, and `AiderManager` (Aider merges rule paths into `.aider.conf.yml` using non-destructive text edits).
- **`file_ops.py`**: Orchestrates rule loading and `write_rules_to_ai_dirs()`, which instantiates every manager whose `enable_*` flag is true.
- **`config.py`**: `DEFAULT_CONFIG` includes defaults for the new `enable_*` keys.
- **`cli.py`**: Loads config, applies `--target` toggles, and invokes bootstrap/sync/generate flows.
