"""File operations for crules."""
from pathlib import Path
from typing import List, Dict
import logging
import shutil
import yaml
from importlib import resources

logger = logging.getLogger(__name__)

def copy_predefined_rules(lang_rules_dir: Path, verbose: bool = False) -> None:
    """Copy predefined language rules to the lang_rules directory."""
    try:
        # Get predefined rules using importlib.resources
        with resources.files('crules.rules') as rules_path:
            if not rules_path.is_dir():
                logger.warning("No predefined rules found in package")
                return
                
            # Copy each rule file found
            for rule_file in rules_path.glob('cursor.*'):
                try:
                    with rule_file.open('r') as src:
                        dest_file = lang_rules_dir / rule_file.name
                        if not dest_file.exists():
                            dest_file.write_text(src.read())
                            if verbose:
                                logger.info(f"Copied predefined rules: {rule_file.name}")
                        elif verbose:
                            logger.info(f"Skipped existing rules: {rule_file.name}")
                except Exception as e:
                    logger.error(f"Failed to copy {rule_file.name}: {e}")
                    
    except Exception as e:
        logger.error(f"Failed to copy predefined rules: {e}")

def setup_directory_structure(verbose: bool = False) -> bool:
    """Create necessary directories and files for crules."""
    try:
        base_dir = Path("~/.config/Cursor/cursor-rules").expanduser()
        lang_rules_dir = base_dir / "lang_rules"
        config_file = base_dir / "config.yaml"
        global_rules = base_dir / "cursorrules"

        # Create directories
        base_dir.mkdir(parents=True, exist_ok=True)
        if verbose:
            logger.info(f"Created directory: {base_dir}")
        
        lang_rules_dir.mkdir(exist_ok=True)
        if verbose:
            logger.info(f"Created directory: {lang_rules_dir}")

        # Copy predefined language rules
        copy_predefined_rules(lang_rules_dir, verbose)

        # Create global rules file if it doesn't exist
        if not global_rules.exists():
            try:
                with resources.files('crules.rules').joinpath('default_cursorrules').open('r') as src:
                    global_rules.write_text(src.read())
                    if verbose:
                        logger.info(f"Created file with default rules: {global_rules}")
            except Exception as e:
                logger.error(f"Failed to copy default rules: {e}")
                logger.warning("Creating empty file instead")
                global_rules.touch()
                if verbose:
                    logger.info(f"Created empty file: {global_rules}")

        # Create default config if it doesn't exist
        if not config_file.exists():
            default_config = {
                "global_rules_path": str(global_rules),
                "language_rules_dir": str(lang_rules_dir),
                "delimiter": "\n# --- Delimiter ---\n",  # Ensure this is the correct delimiter
                "backup_existing": True,
            }
            with config_file.open('w') as f:
                yaml.dump(default_config, f, default_flow_style=False)
            if verbose:
                logger.info(f"Created file: {config_file}")

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
    """Add .cursorrules to .gitignore if it exists."""
    gitignore_path = Path('.gitignore')
    if not gitignore_path.exists():
        return

    # Read current content
    content = gitignore_path.read_text()
    lines = content.splitlines()

    # Check if .cursorrules is already in .gitignore
    if '.cursorrules' not in lines:
        # Add section header and .cursorrules
        with gitignore_path.open('a') as f:
            # Ensure there's a newline before our new section if file isn't empty
            if content and not content.endswith('\n'):
                f.write('\n')
            f.write('\n# Cursor specific\n.cursorrules\n')
            logger.debug("Added .cursorrules to .gitignore with section header")