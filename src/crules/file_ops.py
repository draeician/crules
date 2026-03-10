"""File operations for crules."""
from pathlib import Path
from typing import List, Dict, Optional, Any
import logging
import shutil
import yaml
import click
from importlib import resources
from .ai_managers import CursorManager, ClaudeManager, CopilotManager

logger = logging.getLogger(__name__)

def copy_predefined_rules(lang_rules_dir: Path, verbose: bool = False, force: bool = False) -> None:
    """Copy predefined language rules to the lang_rules directory."""
    try:
        # Get predefined rules using importlib.resources
        with resources.as_file(resources.files('crules.rules')) as rules_path:
            if not rules_path.is_dir():
                logger.warning("No predefined rules found in package")
                return
                
            if verbose:
                logger.debug(f"Looking for rules in: {rules_path}")
                
            # Copy each rule file found
            for rule_file in rules_path.glob('cursor.*'):
                try:
                    if verbose:
                        logger.debug(f"Processing rule file: {rule_file}")
                    with rule_file.open('r') as src:
                        dest_file = lang_rules_dir / rule_file.name
                        if verbose:
                            logger.debug(f"Destination file: {dest_file} (exists: {dest_file.exists()}, force: {force})")
                        # Always copy if force is True or file doesn't exist
                        if force or not dest_file.exists():
                            content = src.read()
                            dest_file.write_text(content)
                            if verbose:
                                logger.info(f"{'Updated' if dest_file.exists() else 'Copied'} rules: {rule_file.name}")
                                logger.debug(f"Content length: {len(content)} bytes")
                        elif verbose:
                            logger.info(f"Skipped existing rules: {rule_file.name}")
                except Exception as e:
                    logger.error(f"Failed to copy {rule_file.name}: {e}")
                    raise  # Re-raise to see full traceback in verbose mode
                    
    except Exception as e:
        logger.error(f"Failed to copy predefined rules: {e}")
        raise  # Re-raise to see full traceback in verbose mode

def copy_workflow_files(workflows_dir: Path, verbose: bool = False, force: bool = False) -> None:
    """Copy workflow mode files (MANAGER.md, CODER.md) to the workflows directory."""
    try:
        with resources.as_file(resources.files('crules.rules.workflows')) as wf_path:
            if not wf_path.is_dir():
                logger.warning("No workflow files found in package")
                return

            for md_file in wf_path.glob('*.md'):
                try:
                    dest_file = workflows_dir / md_file.name
                    if force or not dest_file.exists():
                        dest_file.write_text(md_file.read_text())
                        if verbose:
                            logger.info(f"{'Updated' if dest_file.exists() else 'Copied'} workflow: {md_file.name}")
                    elif verbose:
                        logger.info(f"Skipped existing workflow: {md_file.name}")
                except Exception as e:
                    logger.error(f"Failed to copy {md_file.name}: {e}")
                    raise

    except Exception as e:
        logger.error(f"Failed to copy workflow files: {e}")
        raise


def setup_directory_structure(verbose: bool = False, force: bool = False) -> bool:
    """Create necessary directories and files for crules.
    
    Args:
        verbose: Whether to show verbose output
        force: Whether to overwrite existing files
    """
    try:
        base_dir = Path("~/.config/crules").expanduser()
        lang_rules_dir = base_dir / "lang_rules"
        workflows_dir = base_dir / "workflows"
        config_file = base_dir / "config.yaml"
        global_rules = base_dir / "cursorrules"

        # Create directories
        base_dir.mkdir(parents=True, exist_ok=True)
        if verbose:
            logger.info(f"Created directory: {base_dir}")
        
        lang_rules_dir.mkdir(exist_ok=True)
        if verbose:
            logger.info(f"Created directory: {lang_rules_dir}")

        workflows_dir.mkdir(exist_ok=True)
        if verbose:
            logger.info(f"Created directory: {workflows_dir}")

        # Copy predefined language rules
        copy_predefined_rules(lang_rules_dir, verbose, force)

        # Copy workflow mode files
        copy_workflow_files(workflows_dir, verbose, force)

        # Create or update global rules file
        if not global_rules.exists() or force:
            try:
                with resources.files('crules.rules').joinpath('default_cursorrules').open('r') as src:
                    global_rules.write_text(src.read())
                    if verbose:
                        logger.info(f"{'Updated' if global_rules.exists() else 'Created'} file with default rules: {global_rules}")
            except Exception as e:
                logger.error(f"Failed to copy default rules: {e}")
                logger.warning("Creating empty file instead")
                global_rules.touch()
                if verbose:
                    logger.info(f"Created empty file: {global_rules}")

        # Create or update default config
        if not config_file.exists() or force:
            default_config = {
                "global_rules_path": str(global_rules),
                "language_rules_dir": str(lang_rules_dir),
                "project_rules_dir": ".cursor/rules",
                "delimiter": "\n# --- Delimiter ---\n",
                "use_legacy": False,
                "file_extension": ".mdc"
            }
            with config_file.open('w') as f:
                yaml.dump(default_config, f, default_flow_style=False)
            if verbose:
                logger.info(f"{'Updated' if config_file.exists() else 'Created'} file: {config_file}")

        return True
    except Exception as e:
        logger.error(f"Setup failed: {e}")
        return False

def get_available_languages(language_rules_dir: Path) -> Dict[str, Path]:
    """Get all available language rule files."""
    lang_rules = {}
    if not language_rules_dir.exists():
        return lang_rules
        
    for file in language_rules_dir.glob("cursor.*"):
        if file.is_file():
            lang = file.name.replace("cursor.", "")
            lang_rules[lang] = file
            
    return lang_rules

def list_available_languages(language_rules_dir: Path) -> None:
    """Display all available language rule files."""
    lang_rules = get_available_languages(language_rules_dir)
    
    if not lang_rules:
        logger.info("No language rules found.")
        return
        
    print("\nAvailable language rules:")
    for lang, file in sorted(lang_rules.items()):
        print(f"- {lang} ({file.name})")
    print()

def check_files_exist(global_rules: Path, language_rules_dir: Path, languages: List[str]) -> bool:
    """Check if all required files exist."""
    if not global_rules.exists():
        logger.error(f"Global rules file not found at {global_rules}")
        return False
    
    for lang in languages:
        lang_file = language_rules_dir / f"cursor.{lang}"
        if not lang_file.exists():
            logger.error(f"Language rules file not found at {lang_file}")
            return False
    
    return True

def backup_existing_rules(force: bool = False) -> bool:
    """Backup existing .cursorrules file if it exists."""
    rules_file = Path(".cursorrules")
    if not rules_file.exists():
        return True
        
    if not force:
        response = input("Existing .cursorrules found. Overwrite? [y/N] ").lower()
        if response != 'y':
            logger.info("Operation cancelled by user")
            return False
    
    try:
        backup_file = Path(".cursorrules.bak")
        shutil.copy2(rules_file, backup_file)
        logger.info(f"Backed up existing rules to {backup_file}")
        return True
    except Exception as e:
        logger.error(f"Failed to create backup: {e}")
        return False

def combine_rules(global_rules: Path, language_rules_dir: Path, 
                 languages: List[str], delimiter: str) -> str:
    """Combine global and language-specific rules."""
    content_parts = []
    
    # Add global rules
    try:
        content_parts.append(global_rules.read_text().strip())
    except Exception as e:
        logger.error(f"Failed to read global rules: {e}")
        raise
        
    # Add language-specific rules
    for lang in languages:
        try:
            lang_file = language_rules_dir / f"cursor.{lang}"
            # Add just the language header and content
            content = lang_file.read_text().strip()
            # Remove any existing language headers or delimiters
            content = content.replace("# --- Delimiter ---", "")
            content = '\n'.join(line for line in content.splitlines() 
                              if not line.strip().startswith("# Rules for"))
            content_parts.append(f"# Rules for {lang}\n{content}")
        except Exception as e:
            logger.error(f"Failed to read rules for {lang}: {e}")
            raise
    
    # Update .gitignore if it exists
    update_gitignore()
            
    return delimiter.join(content_parts)

def update_gitignore() -> None:
    """Add .cursorrules and .cursorrules.bak to .gitignore if it exists."""
    gitignore_path = Path('.gitignore')
    if not gitignore_path.exists():
        return

    # Read current content
    content = gitignore_path.read_text()
    lines = content.splitlines()

    # Check if either file is already in .gitignore
    cursor_entries = {'.cursorrules', '.cursorrules.bak'}
    existing_entries = cursor_entries.intersection(lines)
    
    if len(existing_entries) < len(cursor_entries):
        # Add section header and entries
        with gitignore_path.open('a') as f:
            # Ensure there's a newline before our new section if file isn't empty
            if content and not content.endswith('\n'):
                f.write('\n')
            f.write('\n# Cursor specific\n')
            
            # Add any missing entries
            for entry in cursor_entries - existing_entries:
                f.write(f'{entry}\n')
            
            logger.debug("Added Cursor entries to .gitignore")


def refresh_default_rules(verbose: bool = False) -> bool:
    """Refresh the global default rules file from the packaged defaults.

    Copies ``default_cursorrules`` from the installed ``crules.rules`` package
    into the user's ``~/.config/crules/cursorrules`` file, creating the
    configuration directory if needed.

    Args:
        verbose: Whether to emit verbose log messages.

    Returns:
        True if the refresh succeeded, False otherwise.
    """
    try:
        base_dir = Path("~/.config/crules").expanduser()
        base_dir.mkdir(parents=True, exist_ok=True)
        global_rules = base_dir / "cursorrules"

        with resources.files("crules.rules").joinpath("default_cursorrules").open("r") as src:
            content = src.read()
            global_rules.write_text(content)

        if verbose:
            logger.info(f"Refreshed default rules at {global_rules}")
        return True
    except Exception as e:
        logger.error(f"Failed to refresh default rules: {e}")
        return False

def bootstrap_swarm(config: dict) -> bool:
    """Initialize the generic Swarm infrastructure in the current repo.

    Creates the local `.crules/` directory tree, copies workflow mode files
    from the global config, scaffolds a `project_spec.md` when absent, and
    deploys the Universal Agent System instructions to all enabled IDE rule
    folders via `write_rules_to_ai_dirs`.

    Args:
        config: Configuration dict loaded from crules config.

    Returns:
        True if all steps succeeded, False otherwise.
    """
    try:
        crules_dir = Path(".crules")

        if crules_dir.exists():
            if not click.confirm(
                "\u26a0\ufe0f  This repository is already bootstrapped. "
                "Proceeding will refresh personas and rules. Continue?"
            ):
                logger.info("Bootstrap aborted by user")
                return True

        for sub in ("tasks/wip", "tasks/review", "tasks/done", "modes"):
            (crules_dir / sub).mkdir(parents=True, exist_ok=True)
        logger.info("Created .crules directory structure")

        workflows_src = Path("~/.config/crules/workflows").expanduser()
        modes_dest = crules_dir / "modes"
        for filename in ("MANAGER.md", "CODER.md", "GIT_POLICY.md"):
            dest = modes_dest / filename
            if dest.exists():
                logger.info(f"{filename} already exists in {modes_dest}, skipping")
                continue

            config_src = workflows_src / filename
            if config_src.exists():
                shutil.copy2(config_src, dest)
                logger.info(f"Copied {filename} from config to {modes_dest}")
                continue

            try:
                pkg_content = (
                    resources.files("crules.rules.workflows")
                    .joinpath(filename)
                    .read_text()
                )
                dest.write_text(pkg_content)
                logger.info(f"Copied {filename} from package resources to {modes_dest}")
            except Exception:
                logger.warning(f"Workflow template {filename} not found in config or package resources, skipping")

        project_spec = Path("project_spec.md")
        if not project_spec.exists():
            project_spec.write_text(
                "# Project Specification\n\n"
                "## Status\n"
                "- [ ] REPO EVALUATION REQUIRED: "
                "Act as Manager to initialize this document.\n"
            )
            logger.info("Created skeleton project_spec.md")
        else:
            logger.info("project_spec.md already exists, skipping")

        global_rules = Path(config["global_rules_path"]).expanduser()
        lang_rules_dir = Path(config["language_rules_dir"]).expanduser()

        if not global_rules.exists():
            logger.info("Global config not found, running initial setup...")
            if not setup_directory_structure():
                logger.error("Failed to initialize config directory")
                return False

        config.setdefault("enable_cursor", True)
        config.setdefault("enable_claude", True)
        config.setdefault("enable_copilot", True)

        if not write_rules_to_ai_dirs(config, global_rules, lang_rules_dir, []):
            logger.error("Failed to deploy global rules to AI directories")
            return False

        logger.info("Swarm bootstrap complete")
        return True

    except Exception as e:
        logger.error(f"Bootstrap failed: {e}")
        return False


def sync_modes(config: dict) -> bool:
    """Copy workflow mode files from global config into the local .crules/modes/ directory,
    then refresh the IDE rule folders with the latest global rules.

    Args:
        config: Configuration dict loaded from crules config.

    Returns:
        True if sync succeeded, False otherwise.
    """
    try:
        workflows_src = Path("~/.config/crules/workflows").expanduser()
        modes_dest = Path(".crules/modes")
        modes_dest.mkdir(parents=True, exist_ok=True)

        if not workflows_src.exists():
            logger.warning(f"Global workflows directory not found: {workflows_src}")
            logger.info("Run 'crules --setup' first to create workflow templates.")
            return False

        copied = 0
        for md_file in workflows_src.glob("*.md"):
            dest = modes_dest / md_file.name
            shutil.copy2(md_file, dest)
            logger.info(f"Synced {md_file.name} -> {modes_dest}")
            copied += 1

        if copied == 0:
            logger.warning("No workflow files found to sync")

        global_rules = Path(config["global_rules_path"]).expanduser()
        lang_rules_dir = Path(config["language_rules_dir"]).expanduser()

        if not global_rules.exists():
            logger.warning("Global rules file not found, skipping IDE refresh")
            return True

        config.setdefault("enable_cursor", True)
        config.setdefault("enable_claude", True)
        config.setdefault("enable_copilot", True)

        if not write_rules_to_ai_dirs(config, global_rules, lang_rules_dir, []):
            logger.error("Failed to refresh IDE rule folders")
            return False

        logger.info("IDE rule folders refreshed")
        return True

    except Exception as e:
        logger.error(f"Sync failed: {e}")
        return False


def report_status() -> Dict[str, Any]:
    """Report the status of the global crules config and current project.

    Checks for the presence of the global configuration directory, config file,
    global rules, language rules, and workflow templates under
    ``~/.config/crules``. If the current directory contains a ``.crules``
    folder, it also inspects local modes and ``project_spec.md``.

    Returns:
        A dictionary with a boolean ``all_ok`` flag and a ``checks`` list of
        individual check results, each containing:
        - ``scope``: \"global\" or \"project\"
        - ``name``: Human-readable description of the check
        - ``path``: Filesystem path involved in the check
        - ``ok``: True if the check passed, False otherwise
        - ``remediation``: Suggested command string, or None
    """
    checks: list[Dict[str, Any]] = []

    base_dir = Path("~/.config/crules").expanduser()
    config_file = base_dir / "config.yaml"
    global_rules = base_dir / "cursorrules"
    lang_rules_dir = base_dir / "lang_rules"
    workflows_dir = base_dir / "workflows"

    def add_check(scope: str, name: str, path: Path, ok: bool, remediation: Optional[str]) -> None:
        checks.append(
            {
                "scope": scope,
                "name": name,
                "path": str(path),
                "ok": ok,
                "remediation": remediation,
            }
        )

    # Global config checks
    has_base = base_dir.exists()
    add_check("global", "Config directory", base_dir, has_base, "crules --setup" if not has_base else None)

    has_config_file = config_file.exists()
    add_check("global", "Config file", config_file, has_config_file, "crules --setup" if not has_config_file else None)

    has_global_rules = global_rules.exists()
    add_check(
        "global",
        "Global rules (cursorrules)",
        global_rules,
        has_global_rules,
        "crules --refresh-defaults" if not has_global_rules else None,
    )

    has_lang_dir = lang_rules_dir.exists()
    add_check(
        "global",
        "Language rules directory",
        lang_rules_dir,
        has_lang_dir,
        "crules --setup" if not has_lang_dir else None,
    )

    has_lang_files = has_lang_dir and any(lang_rules_dir.glob("cursor.*"))
    add_check(
        "global",
        "Language rule files (cursor.*)",
        lang_rules_dir,
        has_lang_files,
        "crules --setup" if not has_lang_files else None,
    )

    has_workflows_dir = workflows_dir.exists()
    add_check(
        "global",
        "Workflows directory",
        workflows_dir,
        has_workflows_dir,
        "crules --setup" if not has_workflows_dir else None,
    )

    core_names = ("MANAGER.md", "CODER.md", "GIT_POLICY.md")
    for name in core_names:
        wf_path = workflows_dir / name
        ok = wf_path.exists()
        add_check(
            "global",
            f"Workflow template {name}",
            wf_path,
            ok,
            "crules --setup" if not ok else None,
        )

    # Project-level checks (only if this looks like a crules-enabled repo)
    project_crules = Path(".crules")
    if project_crules.exists():
        modes_dir = project_crules / "modes"
        has_modes_dir = modes_dir.exists()
        add_check(
            "project",
            "Local modes directory (.crules/modes)",
            modes_dir,
            has_modes_dir,
            "crules --sync" if not has_modes_dir else None,
        )

        has_mode_files = has_modes_dir and any(modes_dir.glob("*.md"))
        add_check(
            "project",
            "Local mode files (.crules/modes/*.md)",
            modes_dir,
            has_mode_files,
            "crules --sync" if not has_mode_files else None,
        )

        project_spec = Path("project_spec.md")
        has_project_spec = project_spec.exists()
        add_check(
            "project",
            "project_spec.md",
            project_spec,
            has_project_spec,
            "crules --bootstrap" if not has_project_spec else None,
        )

    all_ok = all(entry["ok"] for entry in checks)
    return {"all_ok": all_ok, "checks": checks}


def write_rules_to_ai_dirs(
    config: dict,
    global_rules: Path,
    lang_rules_dir: Path,
    languages: list[str],
    force: bool = False
) -> bool:
    """Write rules to all enabled AI assistant directories.

    Instantiates managers for each enabled assistant (Cursor, Claude, Copilot)
    based on config flags, then writes global and per-language rule files
    through each manager.

    Args:
        config: Configuration dict with enable_cursor/enable_claude/enable_copilot flags
        global_rules: Path to global rules file
        lang_rules_dir: Path to language rules directory
        languages: List of language identifiers
        force: Whether to force overwrite existing files

    Returns:
        bool: True if all writes succeeded, False otherwise
    """
    try:
        manager_map = {
            "enable_cursor": CursorManager,
            "enable_claude": ClaudeManager,
            "enable_copilot": CopilotManager,
        }
        active_managers = [
            cls(config) for key, cls in manager_map.items() if config.get(key)
        ]

        if not active_managers:
            logger.warning("No AI assistants enabled in config")
            return False

        content = global_rules.read_text()

        for manager in active_managers:
            manager.ensure_structure()
            if not manager.create_rule_file("global", content, ["*"]):
                return False
            manager.update_gitignore()

        for lang in languages:
            lang_file = lang_rules_dir / f"cursor.{lang}"
            lang_content = lang_file.read_text()
            for manager in active_managers:
                if not manager.create_rule_file(lang, lang_content, [f"*.{lang}"]):
                    return False

        return True

    except Exception as e:
        logger.error(f"Failed to write rules to AI directories: {e}")
        return False