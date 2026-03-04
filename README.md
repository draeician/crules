# Crules - Omni-Assistant Rules Generator

A Python utility that acts as a **Context Compiler**, turning a single set of universal rules into the native formats required by multiple AI coding assistants:

| Assistant | Output Directory | File Extension | Metadata Key |
|-----------|-----------------|----------------|--------------|
| Cursor | `.cursor/rules/` | `.mdc` | `globs` |
| Claude Code | `.claude/rules/` | `.md` | `paths` |
| GitHub Copilot | `.github/instructions/` | `.instructions.md` | `applyTo` |

## Features

- Compiles one source of truth into native rule files for Cursor, Claude Code, and GitHub Copilot
- Automatically translates glob patterns into each tool's metadata dialect
- Injects a Universal Preamble into every generated file for consistent AI behavior
- Per-tool toggles — enable or disable any assistant via config or CLI flags
- `--target` flag to generate rules for specific tools in a single invocation
- Legacy mode (`--legacy`) for backward-compatible `.cursorrules` output
- Supports multiple programming languages with per-language rule files
- Configurable via YAML

## Installation

1. Clone the repository:
```bash
git clone https://github.com/draeician/crules.git
cd crules
```

2. Install using pipx (recommended):
```bash
pipx install .
```

> **Note:** If you encounter an "externally-managed-environment" error, create a virtual environment:
> ```bash
> python3 -m venv .venv
> source .venv/bin/activate
> pip install .
> ```

## Configuration

The default configuration file is located at `~/.config/crules/config.yaml`:

```yaml
global_rules_path: "~/.config/crules/cursorrules"
language_rules_dir: "~/.config/crules/lang_rules"
enable_cursor: true
enable_claude: true
enable_copilot: true
delimiter: "\n# --- Delimiter ---\n"
```

Set any `enable_*` toggle to `false` to skip that assistant during generation.

### Source Directory Structure

```
~/.config/crules/
├── config.yaml
├── cursorrules              # global rules (applied to all files)
└── lang_rules/
    ├── cursor.python
    ├── cursor.javascript
    └── cursor.<language>
```

## Usage

### First-Time Setup

```bash
crules --setup
```

### Generate Rules for All Enabled Assistants

```bash
crules python javascript
```

### Target Specific Assistants

```bash
# Only Cursor and Claude Code
crules -t cursor -t claude python

# Only GitHub Copilot
crules --target copilot python rust
```

### List Available Languages

```bash
crules --list
```

### Legacy Mode

Generate a single `.cursorrules` file (pre-0.2 behavior):

```bash
crules --legacy python javascript
```

### Additional Options

```bash
crules -f python        # force overwrite existing rule files
crules -v python        # enable verbose logging
crules --help           # show all options
```

## Command-Line Options

| Option | Description |
|--------|-------------|
| `languages` | One or more language identifiers |
| `-t, --target` | AI tool to generate for (repeatable: `cursor`, `claude`, `copilot`) |
| `-f, --force` | Force overwrite of existing files |
| `-v, --verbose` | Enable verbose output |
| `-l, --list` | List available language rules |
| `-s, --setup` | Create necessary directories and files |
| `--legacy` | Generate a single `.cursorrules` file |
| `--version` | Show version |
| `--help` | Show help message |

## Generated Output

Running `crules python` with all assistants enabled produces:

```
project/
├── .cursor/rules/
│   ├── global.mdc
│   └── python.mdc
├── .claude/rules/
│   ├── global.md
│   └── python.md
└── .github/instructions/
    ├── global.instructions.md
    └── python.instructions.md
```

Each file contains YAML frontmatter with tool-native metadata and the Universal Preamble, followed by the rule content.

## Development

### Requirements

- Python 3.9+
- PyYAML
- Click

### Project Structure

```
crules/
├── src/
│   └── crules/
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli.py
│       ├── config.py
│       ├── ai_managers.py
│       ├── cursor_ops.py
│       └── file_ops.py
├── tests/
│   └── test_ai_managers.py
├── pyproject.toml
├── CHANGELOG.md
└── README.md
```

### Setting Up Development Environment

```bash
git clone https://github.com/draeician/crules.git
cd crules
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest tests/ -v
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

[![PyPI version](https://badge.fury.io/py/crules.svg)](https://badge.fury.io/py/crules)
[![Python versions](https://img.shields.io/pypi/pyversions/crules.svg)](https://pypi.org/project/crules/)
