"""Operations for managing .cursor directory structure."""
from pathlib import Path
from typing import Dict, Any, List, Optional
import logging
import yaml

logger = logging.getLogger(__name__)

class CursorDirectoryManager:
    """Manages the .cursor directory structure and rule files."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the cursor directory manager.
        
        Args:
            config: Configuration dictionary containing paths and settings
        """
        self.config = config
        self.cursor_dir = Path(".cursor")
        self.rules_dir = self.cursor_dir / "rules"
        
    def ensure_cursor_structure(self) -> None:
        """Create the .cursor directory structure if it doesn't exist."""
        self.cursor_dir.mkdir(exist_ok=True)
        self.rules_dir.mkdir(exist_ok=True)
        logger.info(f"Ensured .cursor structure exists at {self.cursor_dir}")
            
    def create_rule_file(self, name: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> bool:
        """Create a rule file with optional metadata.
        
        Args:
            name: Name of the rule file (without extension)
            content: Rule content
            metadata: Optional metadata dictionary
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            file_path = self.rules_dir / f"{name}{self.config['file_extension']}"
            
            if metadata:
                full_content = "---\n"
                full_content += yaml.dump(metadata)
                full_content += "---\n"
                full_content += content
            else:
                full_content = content
                
            file_path.write_text(full_content)
            logger.info(f"Created rule file: {file_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to create rule file {name}: {e}")
            return False
            
    def list_rule_files(self) -> List[Path]:
        """List all rule files in the .cursor/rules directory.
        
        Returns:
            List[Path]: List of paths to rule files
        """
        if not self.rules_dir.exists():
            return []
        return list(self.rules_dir.glob(f"*{self.config['file_extension']}"))
        
    def update_gitignore(self) -> None:
        """Update .gitignore to include .cursor/rules/*.mdc."""
        gitignore = Path(".gitignore")
        cursor_ignore = f".cursor/rules/*{self.config['file_extension']}"
        
        try:
            if gitignore.exists():
                content = gitignore.read_text()
                if cursor_ignore not in content:
                    if "# Cursor specific" not in content:
                        content += "\n# Cursor specific\n"
                    content += f"{cursor_ignore}\n"
                    gitignore.write_text(content)
                    logger.info("Updated .gitignore with cursor rules pattern")
            else:
                gitignore.write_text(f"# Cursor specific\n{cursor_ignore}\n")
                logger.info("Created .gitignore with cursor rules pattern")
        except Exception as e:
            logger.warning(f"Failed to update .gitignore: {e}") 