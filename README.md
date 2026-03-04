# Crules - Omni-Assistant Context Compiler

A Python utility that acts as a **Swarm Infrastructure Deployer**, turning a single set of universal rules into native formats for multiple AI coding assistants while establishing a self-configuring agent ecosystem.

## The Crules Philosophy: "Skeleton Swarms"
Unlike hardcoded instruction sets, `crules` deploys a generic, role-based architecture into your repository. It provides the **Skeleton**, and your AI Agent (Cursor, Claude Code, Aider, etc.) provides the **Brain**. Upon landing in a "bootstrapped" repo, the AI is instructed to evaluate the codebase, update the project specifications, and self-configure its own operating modes.

| Assistant | Output Directory | File Extension | Metadata Key |
|-----------|-----------------|----------------|--------------|
| **Cursor** | `.cursor/rules/` | `.mdc` | `globs` |
| **Claude Code** | `.claude/rules/` | `.md` | `paths` |
| **GitHub Copilot** | `.github/instructions/` | `.instructions.md` | `applyTo` |

## Core Features

- [cite_start]**Multi-Agent Compilation**: Compiles one source of truth into native rule files for all major IDE assistants[cite: 1, 19].
- [cite_start]**Swarm Bootstrapping**: Initializes a `.crules/` directory with `MANAGER` and `CODER` personas and a task tracking system[cite: 71, 73].
- [cite_start]**Self-Evaluating Spec**: Generates a skeleton `project_spec.md` that triggers the AI to perform an automated repository audit[cite: 18, 21].
- [cite_start]**Universal Preamble**: Injects a standardized preamble into every file to ensure the AI prioritizes the `project_spec.md` as the ultimate source of truth[cite: 19, 79].
- **Cross-IDE Continuity**: Uses `summary.txt` and `instructions.txt` as a "flight recorder" for handoffs between different tools.

## Installation

```bash
git clone [https://github.com/draeician/crules.git](https://github.com/draeician/crules.git)
cd crules
pipx install . --force

```

## Usage

### 1. Initialize Global Config

Creates `~/.config/crules/` with global rules, language templates, and swarm workflow modes.

```bash
crules --setup

```

### 2. Bootstrap a Repository

Deploy the Swarm Infrastructure and the Repository Evaluator into your current project.

```bash
crules --bootstrap

```

*Creates: `.crules/tasks/`, `.crules/modes/`, and `project_spec.md`.*

### 3. Generate Language Context

Compile specific programming language rules for all enabled assistants.

```bash
# Add Python and Bash rules across all tools
crules python bash

# Target only specific assistants
crules -t cursor -t claude python

```

## The Swarm Workflow

Once a repo is bootstrapped, your AI assistant will follow this loop:

1. **Discovery**: AI reads the native rules and adopts the **Manager** persona.
2. **Evaluation**: AI scans the repo and populates the `project_spec.md`.
3. **Tasking**: AI creates task files in `.crules/tasks/wip/`.
4. **Execution**: AI switches to **Coder** mode to implement features based on the `project_spec.md`.

## Configuration

Managed via `~/.config/crules/config.yaml`:

```yaml
enable_cursor: true
enable_claude: true
enable_copilot: true
global_rules_path: "~/.config/crules/cursorrules"
language_rules_dir: "~/.config/crules/lang_rules"

```

## License

MIT License - Copyright (c) 2023-2026 draeician.
