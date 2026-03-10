# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2026-03-04

### Added
- Multi-agent architecture: compile a single set of universal rules into native formats for Cursor, Claude Code, and GitHub Copilot
- `CursorManager`, `ClaudeManager`, and `CopilotManager` classes in `ai_managers.py`, each producing tool-specific directory structures and metadata
- Claude Code support — generates `.claude/rules/*.md` with `paths` frontmatter
- GitHub Copilot support — generates `.github/instructions/*.instructions.md` with `applyTo` frontmatter
- `--target` / `-t` CLI argument (repeatable) to limit generation to specific tools (e.g. `crules -t cursor -t claude python`)
- `enable_cursor`, `enable_claude`, `enable_copilot` boolean toggles in `config.yaml`
- Universal Preamble injected into every generated rule file
- `write_rules_to_ai_dirs()` in `file_ops.py` replaces the old cursor-only writer
 - `--refresh-defaults` (`-R`) CLI flag to overwrite the global `cursorrules` file from the packaged `default_cursorrules`
 - `--status` CLI flag to print a diagnostic report of global and project setup, including remediation commands

### Changed
- `file_ops.py` now imports from `ai_managers` instead of `cursor_ops`
- CLI defaults to generating rules for all enabled assistants when no `--target` is specified
- Test suite renamed from `test_cursor_ops.py` to `test_ai_managers.py` and expanded to cover all three managers

### Removed
- `write_rules_to_cursor_dir()` function (replaced by `write_rules_to_ai_dirs()`)
- Direct dependency on `CursorDirectoryManager` from `cursor_ops.py` in the main workflow

## [0.2.1] - 2024-03-26

### Changed
- Improved organization and clarity of default cursor rules
- Enhanced documentation structure in default_cursorrules
- Added comprehensive sections for AI integration, maintenance, and CI/CD
- Removed redundancy in global rules

## [0.2.0] - 2024-03-26

### Added
- Support for `.cursor/rules/` directory with individual `.mdc` rule files
- Metadata support in `.mdc` files (description, globs)
- New `CursorDirectoryManager` class for managing `.cursor` directory operations
- Legacy mode support with `--legacy` flag for backward compatibility

### Changed
- Default output now uses `.cursor/rules/*.mdc` instead of single `.cursorrules` file
- Updated configuration to support new directory structure
- Improved error handling and logging
- Updated `.gitignore` handling for `.cursor/rules/*.mdc`

### Removed
- Backup functionality (`.cursor/rules.bak`)
- `backup_existing` configuration option

## [0.1.2] - 2024-03-26

### Added
- Initial release
- Support for generating `.cursorrules` file
- Global and language-specific rules
- Basic configuration management

## [0.1.1] - 2023-11-18
### Added
- Version flag (--version, -V) to CLI
- PyPI support with proper package metadata
- PyPI badges in README
- Comprehensive release documentation

### Changed
- Updated default_cursorrules with CHANGELOG.md management
- Enhanced project metadata in pyproject.toml

## [0.1.0] - 2023-11-18
### Added
- Initial release
- Global and language-specific cursor rules management
- Setup command for first-time configuration
- Multiple language support
- Backup functionality
- YAML configuration 
