# Crules - Omni-Assistant Context Compiler

A Python utility that acts as a **Swarm Infrastructure Deployer**, turning a single set of universal rules into native formats for **seven** AI coding assistants while establishing a self-configuring agent ecosystem (Bootstrapper lockout via root `AGENTS.md`, task pipeline, and `project_spec.md`).

## The Crules Philosophy: "Skeleton Swarms"
Unlike hardcoded instruction sets, `crules` deploys a generic, role-based architecture into your repository. It provides the **Skeleton**, and your AI agent (Cursor, Claude Code, GitHub Copilot, Cline, Roo Code, Windsurf, Aider, etc.) provides the **Brain**. Upon landing in a "bootstrapped" repo, the AI is instructed to evaluate the codebase, update the project specifications, and self-configure its own operating modes.

| Assistant | Output directory | File extension | Metadata |
|-----------|------------------|----------------|----------|
| **Cursor** | `.cursor/rules/` | `.mdc` | `globs` |
| **Claude Code** | `.claude/rules/` | `.md` | `paths` |
| **GitHub Copilot** | `.github/instructions/` | `.instructions.md` | `applyTo` |
| **Cline** | `.clinerules/` | `.md` | `globs` |
| **Roo Code** | `.roorules/` | `.md` | `globs` |
| **Windsurf** | `.windsurf/rules/` | `.md` | `globs` |
| **Aider** | `.aider/rules/` | `.md` | `globs` (append-only `read:` entries in `.aider.conf.yml`) |

## Core Features

- **Multi-agent compilation**: Compiles one source of truth into native rule files for Cursor, Claude Code, GitHub Copilot, Cline, Roo Code, Windsurf, and Aider.
- **Swarm bootstrapping**: Initializes `.crules/` with Manager, Coder, Git policy, and **Bootstrapper** workflow modes, a task pipeline, root `AGENTS.md` (`[TEMPLATE]` / `[CUSTOMIZED]`), and a scaffolded `project_spec.md` (no external shell script required).
- **Self-evaluating spec**: Skeleton `project_spec.md` drives repository discovery and customization after the Bootstrapper interview.
- **Universal preamble**: Injects a standardized preamble (including `AGENTS.md` gatekeeper rules) into every generated rule file so `project_spec.md` stays the source of truth.
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

*Creates: `.crules/tasks/`, `.crules/modes/` (including `BOOTSTRAPPER.md`), root `AGENTS.md`, and `project_spec.md`.*

### 3. Generate Language Context

Compile specific programming language rules for all enabled assistants.

```bash
# Add Python and Bash rules across all tools
crules python bash

# Target only specific assistants
crules -t cursor -t claude python

# Example: only Windsurf and Aider
crules -t windsurf -t aider python

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
enable_cline: true
enable_roo: true
enable_windsurf: true
enable_aider: true
global_rules_path: "~/.config/crules/cursorrules"
language_rules_dir: "~/.config/crules/lang_rules"

```

## License

MIT License - Copyright (c) 2023-2026 draeician.
