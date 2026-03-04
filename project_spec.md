# Crules - Omni-Assistant Rules Generator

## Overview
A Python utility for managing and generating AI context rules simultaneously across multiple assistants (Cursor, Claude Code, GitHub Copilot). It acts as a Context Compiler, turning a single set of universal rules into the native formats required by different AI tools.

## Core Features
1. **Multi-Agent Support**: Generates native directory structures and file formats for:
   - Cursor (`.cursor/rules/*.mdc`)
   - Claude Code (`.claude/rules/*.md`)
   - GitHub Copilot (`.github/instructions/*.instructions.md`)
2. **Universal Preamble**: Injects a standardized preamble to lock down behavior across all tools.
3. **Metadata Translation**: Automatically converts target extensions into the specific YAML dialect of each tool (e.g., `globs` vs `paths` vs `applyTo`).

## Configuration
**Location**: `~/.config/crules/config.yaml`
**Format**:
```yaml
global_rules_path: "~/.config/crules/cursorrules"
language_rules_dir: "~/.config/crules/lang_rules"
enable_cursor: true
enable_claude: true
enable_copilot: true
delimiter: "\n# --- Delimiter ---\n"
```

## Architecture
- `ai_managers.py`: Contains `BaseAIManager` and specific implementations (`CursorManager`, `ClaudeManager`, `CopilotManager`).
- `file_ops.py`: Coordinates the parsing of core rules and loops through active managers to write files.
- `cli.py`: Exposes `--target` options for generating specific tool formats.
