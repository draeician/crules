# Crules - Cursor Rules Generator

A Python utility for generating `.cursorrules` files by combining global and language-specific cursor rules.

## Features

- Combines global cursor rules with language-specific rules
- Supports multiple programming languages
- Automatic backup of existing rules
- List available language configurations
- Configurable via YAML configuration
- Verbose logging support

## Installation

1. Clone the repository:
```bash
git clone https://github.com/draeician/crules.git
cd crules
```

2. Install using pipx: (much better than doing pip install .)
```bash
pipx install .
```
NOTE:  uninstall with pipx uninstall crules or 

> **Note:** If you encounter an "externally-managed-environment" error, you have two options:
> 1. **Recommended:** Create and use a virtual environment:
>    ```bash
>    python3 -m venv .venv
>    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
>    pip install .
>    ```us
> 2. **Alternative:** Use the `--break-system-packages` flag (not recommended):
>    ```bash
>    pip install . --break-system-packages
>    ```
>    This is not recommended as it may interfere with system Python packages.

## Configuration

The default configuration file is located at `~/.config/Cursor/cursor-rules/config.yaml`:

```yaml
global_rules_path: "~/.config/Cursor/cursor-rules/cursorrules"
language_rules_dir: "~/.config/Cursor/cursor-rules/lang_rules"
delimiter: "\n# --- Delimiter ---\n"
backup_existing: true
```

### Directory Structure

```
~/.config/Cursor/cursor-rules/
├── config.yaml
├── cursorrules
└── lang_rules/
    ├── cursor.python
    ├── cursor.javascript
    └── cursor.<language>
```

## Usage

### Basic Usage

Generate a `.cursorrules` file for one or more languages:

```bash
# Single language
python -m crules python

# Multiple languages
python -m crules python javascript rust
```

### List Available Languages

View all available language configurations:

```bash
python -m crules --list
```

Example output:
```
Available language rules:
- python (cursor.python)
- javascript (cursor.javascript)
- rust (cursor.rust)
```

### Additional Options

```bash
# Force overwrite existing .cursorrules file
python -m crules -f python

# Enable verbose output
python -m crules -v python

# Show help
python -m crules --help
```

## Command-line Options

- `languages`: One or more language identifiers
- `-f, --force`: Force overwrite of existing files
- `-v, --verbose`: Enable verbose output
- `-l, --list`: List available language rules
- `-s, --setup`: Create necessary directories and files
- `-h, --help`: Show help message

### First Time Setup

Before using crules, run the setup command to create necessary directories and files:

```bash
python -m crules --setup
```

This will create:
- Configuration directory: `~/.config/Cursor/cursor-rules/`
- Language rules directory: `~/.config/Cursor/cursor-rules/lang_rules/`
- Global rules file: `~/.config/Cursor/cursor-rules/cursorrules`
- Default config file: `~/.config/Cursor/cursor-rules/config.yaml`

## File Structure

The generated `.cursorrules` file combines:
1. Global rules from the `cursorrules` file
2. Language-specific rules from `cursor.<language>` files
3. Uses a configurable delimiter between sections

Example structure:
```
# Global Rules
<global rules content>

# --- Delimiter ---

# Rules for python
<python rules content>

# --- Delimiter ---

# Rules for javascript
<javascript rules content>
```

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
│       └── file_ops.py
├── pyproject.toml
└── README.md
```

### Setting Up Development Environment

1. Clone the repository
2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install development dependencies:
```bash
pip install -e ".[dev]"
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
