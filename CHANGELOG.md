# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
