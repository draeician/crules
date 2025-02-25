# Crules - Project Specification

## Overview
A Python utility for managing Cursor IDE rules, supporting both modern `.cursor/rules` directory structure and legacy `.cursorrules` file format.

## Core Features

1. **Rule Management**:
   - Support for `.cursor/rules` directory with individual `.mdc` rule files
   - Legacy support for single `.cursorrules` file
   - Global and language-specific rules
   - Metadata support in `.mdc` files

2. **Directory Structure**:
   ```
   Project Root/
   ├── .cursor/
   │   └── rules/
   │       ├── global.mdc
   │       ├── python.mdc
   │       └── <language>.mdc
   ```

3. **Rule File Format**:
   ```markdown
   ---
   description: Rule description
   globs: ["*.py"]  # File patterns this rule applies to
   ---
   # Rule Content
   <rule content here>
   ```

## Technical Details

### Programming Language
- Python 3.9+

### Dependencies
- PyYAML (>=6.0): YAML file handling
- Click (>=8.0.0): CLI interface
- setuptools (>=42.0.0): Package management

### Configuration
**Location**: `~/.config/Cursor/cursor-rules/config.yaml`

**Format**:
```yaml
global_rules_path: "~/.config/Cursor/cursor-rules/cursorrules"
language_rules_dir: "~/.config/Cursor/cursor-rules/lang_rules"
project_rules_dir: ".cursor/rules"
delimiter: "\n# --- Delimiter ---\n"
use_legacy: false
file_extension: ".mdc"
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

## Command-Line Interface

### Basic Usage
```bash
# Modern mode (default)
crules python javascript  # Creates .cursor/rules/{global,python,javascript}.mdc

# Legacy mode
crules --legacy python javascript  # Creates single .cursorrules file
```

### Options
- `languages`: One or more language identifiers
- `-f, --force`: Force overwrite existing files
- `-v, --verbose`: Enable verbose output
- `-l, --list`: List available language rules
- `-s, --setup`: Create necessary directories and files
- `--legacy`: Use legacy .cursorrules file format
- `-h, --help`: Show help message

### Examples

1. **List Available Languages**:
   ```bash
   crules --list
   ```
   Output:
   ```
   Available language rules:
   - python (cursor.python)
   - javascript (cursor.javascript)
   ```

2. **Setup Directory Structure**:
   ```bash
   crules --setup
   ```
   Creates:
   - `~/.config/Cursor/cursor-rules/`
   - `~/.config/Cursor/cursor-rules/lang_rules/`
   - `~/.config/Cursor/cursor-rules/cursorrules`
   - `~/.config/Cursor/cursor-rules/config.yaml`

3. **Force Update**:
   ```bash
   crules -f python
   ```
   Overwrites existing rules without prompting.

4. **Legacy Mode**:
   ```bash
   crules --legacy python
   ```
   Creates single `.cursorrules` file with combined rules.

## Error Handling

1. **Missing Files**:
   - Clear error messages for missing configuration or rule files
   - Suggestion to run `--setup` when needed

2. **Permission Issues**:
   - Informative messages for file access problems
   - Proper error handling for configuration directory access

3. **Invalid Arguments**:
   - Validation of language identifiers
   - Clear usage messages for incorrect arguments

## Logging

1. **Standard Mode**:
   - Essential operation information
   - Success/failure messages
   - File creation notifications

2. **Verbose Mode** (`-v`):
   - Detailed operation logging
   - Configuration loading details
   - File operation tracing

## Development Guidelines

1. **Code Style**:
   - Follow PEP 8
   - Use type hints
   - Comprehensive docstrings
   - Line length: 88 characters (ruff configuration)

2. **Testing**:
   - Unit tests for core functionality
   - Integration tests for CLI
   - Test coverage tracking

3. **Documentation**:
   - Maintain CHANGELOG.md
   - Update README.md
   - Keep docstrings current

4. **Version Control**:
   - Semantic versioning
   - Tagged releases
   - Detailed commit messages

## Future Enhancements

1. **Rule Templates**:
   - Support for custom rule templates
   - Template variables and substitution

2. **Rule Validation**:
   - Syntax checking for rule files
   - Schema validation for metadata

3. **Integration**:
   - Direct integration with Cursor IDE
   - Rule synchronization across projects

4. **Rule Management**:
   - Rule enable/disable functionality
   - Rule priority management
1.  **Logging and Verbose Output**:
    
    *   **Why**: Adding logging capabilities can help track the script's operations, which is useful for debugging and monitoring. A verbose mode (`--verbose` or `-v`) can provide detailed output during execution, aiding in troubleshooting if something goes wrong.
    *   **Functionality**: The script could log actions like file reads/writes, errors encountered, and significant decision points (e.g., user prompts, file overwrites).
2.  **Custom Configuration Options**:
    
    *   **Why**: Allowing users to specify custom paths for configuration files or output files increases the script's flexibility and usability in various environments.
    *   **Functionality**: Command-line arguments or a separate configuration file to set custom paths, delimiters, or other preferences.
3.  **Error Handling and Exceptions**:
    
    *   **Why**: Robust error handling ensures that the script fails gracefully and provides meaningful feedback, improving user experience.
    *   **Functionality**: Catching exceptions, validating inputs, and providing clear error messages when files are missing or permissions are insufficient.
4.  **Backup Existing Files**:
    
    *   **Why**: Preventing data loss is important. Creating a backup of the existing `.cursorrules` file before overwriting can safeguard against accidental overwrites.
    *   **Functionality**: Automatically rename the existing file to `.cursorrules.bak` before creating a new one.
5.  **Unit Testing**:
    
    *   **Why**: Including tests ensures that the script works as intended and makes future maintenance easier.
    *   **Functionality**: Writing test cases for key functions, especially for file operations and argument parsing.
6.  **Cross-platform Compatibility**:
    
    *   **Why**: Ensuring the script works on different operating systems (Linux, macOS, Windows) broadens its usability.
    *   **Functionality**: Avoiding OS-specific features and testing on multiple platforms.

* * *

**Project Specification for Cursor Rules Generator Script**

**Overview**

Develop a Python script that generates a `.cursorrules` file in the current project directory. The script combines configuration rules from a global `cursorrules` file and one or more language-specific `cursor.<language>` files, using a delimiter to separate them. The language types are provided as command-line arguments, and the script supports multiple languages at once.

**Key Features**

1.  **Configuration Loading**
    
    *   **Config File**: Load configuration settings from `~/.config/Cursor/cursor-rules/config.yaml` (or `config.toml` if preferred).
        *   **Decision**: Use YAML (`config.yaml`) for its readability and familiarity in configuration files.
    *   **Settings**:
        *   Paths to global `cursorrules` file and language-specific `cursor.<language>` files.
        *   Custom delimiter string (if needed).
2.  **Command-Line Interface**
    
    *   **Usage**: `python script.py [options] <language1> [<language2> ...]`
    *   **Options**:
        *   `-f`, `--force`: Force overwrite of existing `.cursorrules` without prompt.
        *   `-v`, `--verbose`: Enable verbose output.
        *   `-h`, `--help`: Display help message.
        *   `-l`, `--list`: List available language rules.
        *   `-s`, `--setup`: Create necessary directories and files if they don't exist.
3.  **File Operations**
    
    *   **File Detection**:
        *   Check for the existence of the global `cursorrules` file.
        *   Check for the existence of each specified `cursor.<language>` file.
        *   Check for the existence of `.gitignore` file.
    *   **Error Handling**:
        *   If any file is missing, display an informative error message and exit.
    *   **Overwrite Prompt**:
        *   If `.cursorrules` already exists in the current directory and `--force` is not used, prompt the user (`[y/N]`) before overwriting.
    *   **Backup Existing File**:
        *   Optionally (based on configuration), create a backup of the existing `.cursorrules` file before overwriting.
    *   **Git Integration**:
        *   If `.gitignore` exists in the current directory, ensure `.cursorrules` is added to it.
        *   Add `.cursorrules` under a "# Cursor specific" section header.
        *   Add entry on a new line if not already present.
        *   Maintain proper newline formatting in `.gitignore`.
4.  **File Content Assembly**
    
    *   **Delimiter**:
        *   Use a specified delimiter (from config or default) to separate content sections.
        *   Example delimiter: `\n# --- Delimiter ---\n`
    *   **Content Order**:
        *   Global `cursorrules` content on top.
        *   For each language specified:
            *   Include the content of `cursor.<language>` files.
            *   If multiple languages are specified, each is appended with the delimiter in between.
    *   **Language Prefixing** (Optional):
        *   Optionally prefix each language section with a comment or header indicating the language.
        *   Example: `# Rules for <language>`
5.  **Output**
    
    *   **File Creation**:
        *   Write the assembled content to `.cursorrules` in the current directory.
    *   **Success Message**:
        *   Display a message indicating successful creation (if not in silent mode).
6.  **Logging and Verbose Output**
    
    *   **Verbose Mode**:
        *   If `--verbose` is specified, print detailed information about each step.
    *   **Logging**:
        *   Log important actions and errors to a log file or standard output (depending on configuration).
7.  **Error Handling**
    
    *   **Missing Files**:
        *   Provide clear messages indicating which file is missing.
    *   **Permission Issues**:
        *   Inform the user if the script lacks permissions to read source files or write the output file.
    *   **Invalid Arguments**:
        *   Handle unexpected command-line arguments gracefully.
8.  **Multiple Language Support**
    
    *   **Processing Multiple Languages**:
        *   Accept multiple language arguments and process each accordingly.
    *   **Delimiter Usage**:
        *   Use the same delimiter between multiple language sections.
    *   **Inclusion of Rules**:
        *   For each language `<language>`, include the corresponding `cursor.<language>` file content, followed by the global rules if specified in the configuration.

**Implementation Details**

*   **Programming Language**: Python 3.x
*   **Dependencies**:
    *   Standard Python libraries (`os`, `sys`, `argparse`, `yaml` or `toml`, depending on the config file format).
*   **Configuration File Format**:
    *   **YAML (`config.yaml`)**
        
        ```yaml
        global_rules_path: "/path/to/cursorrules"
        language_rules_dir: "/path/to/language/rules"
        delimiter: "\n# --- Delimiter ---\n"
        backup_existing: true
        ```
        
*   **Directory Structure**:
    *   **Global Config**: `~/.config/Cursor/cursor-rules/config.yaml`
    *   **Global Rules File**: As specified in the config (`global_rules_path`)
    *   **Language Rules Files**: Located in `~/.config/Cursor/cursor-rules/lang_rules/cursor.<language>`
*   **Setup Feature**:
    *   Creates necessary directories if they don't exist:
        ```
        ~/.config/Cursor/cursor-rules/
        ~/.config/Cursor/cursor-rules/lang_rules/
        ```
    *   Creates default files if they don't exist:
        *   `~/.config/Cursor/cursor-rules/cursorrules` (empty file)
        *   `~/.config/Cursor/cursor-rules/config.yaml` (with default configuration)
    *   Provides verbose output during setup if requested
    *   Returns success/failure status
    *   Can be run multiple times safely (idempotent)

**User Interaction Examples**

*   **Basic Usage**:
    
    ```bash
    python script.py python
    ```
    
    *   Generates `.cursorrules` with global rules and Python-specific rules.
*   **Multiple Languages**:
    
    ```bash
    python script.py python javascript
    ```
    
    *   Includes both Python and JavaScript rules.
*   **Force Overwrite**:
    
    ```bash
    python script.py --force python
    ```
    
    *   Overwrites existing `.cursorrules` without prompt.
*   **Verbose Output**:
    
    ```bash
    python script.py --verbose python
    ```
    
    *   Displays detailed processing information.
*   **List Available Languages**:
    ```bash
    python script.py --list
    ```
    *   Shows all available language rule files in the lang_rules directory
    *   Example output:
    ```
    Available language rules:
    - python (cursor.python)
    - javascript (cursor.javascript)
    - rust (cursor.rust)
    ```
*   **Setup Directory Structure**:
    ```bash
    python script.py --setup
    ```
    *   Creates necessary directories and files
    *   Example output:
    ```
    Setting up crules directory structure...
    Created directory: ~/.config/Cursor/cursor-rules
    Created directory: ~/.config/Cursor/cursor-rules/lang_rules
    Created file: ~/.config/Cursor/cursor-rules/cursorrules
    Created file: ~/.config/Cursor/cursor-rules/config.yaml
    Setup complete!
    ```

**Testing and Validation**

*   **Unit Tests**:
    *   Test loading of configuration files.
    *   Test file existence checks.
    *   Test the overwrite prompt logic.
    *   Test content assembly with various numbers of languages.
*   **Integration Tests**:
    *   Simulate running the script in different scenarios (no existing `.cursorrules`, with existing file, missing source files).

**Documentation**

*   **Usage Guide**:
    *   Provide a README with instructions on how to install and use the script.
*   **Configuration Guide**:
    *   Explain the structure and options available in `config.yaml`.

**Error Messages and Handling**

*   **File Not Found**:
    *   `"Error: Global rules file not found at /path/to/cursorrules. Use --setup to create required directories."`
    *   `"Error: Language rules directory not found at /path/to/language/rules. Use --setup to create required directories."`
*   **Setup Messages**:
    *   `"Created directory: ~/.config/Cursor/cursor-rules"`
    *   `"Created directory: ~/.config/Cursor/cursor-rules/lang_rules"`
    *   `"Created file: ~/.config/Cursor/cursor-rules/cursorrules"`
    *   `"Created file: ~/.config/Cursor/cursor-rules/config.yaml"`
*   **Permission Denied**:
    *   `"Error: Permission denied when attempting to read '/path/to/cursorrules'."`
*   **Invalid Language Argument**:
    *   `"Error: No language specified. Please provide at least one language."`

**Assumptions and Decisions**

*   **YAML over TOML**: Chose YAML for its widespread use and readability in configuration files.
*   **Default Delimiter**: Defined in the configuration file but can be overridden if necessary.
*   **No Special Cases**: Since no special cases were provided, the script focuses on the core functionality.

**Future Enhancements**

*   **Custom Delimiter per Language**: Allow specifying different delimiters for different languages if needed.
*   **Graphical User Interface**: Develop a GUI for users who prefer not to use the command line.
*   **Plugin System**: Enable support for additional languages or rules through plugins or extensions.

* * *
