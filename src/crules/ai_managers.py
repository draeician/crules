"""AI Context Managers for different assistant platforms."""
import logging
import re
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any, List

import yaml

logger = logging.getLogger(__name__)

class BaseAIManager(ABC):
    """Abstract base class for all AI directory managers."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.target_dir = Path(".")
        self.file_extension = ".md"

    @abstractmethod
    def ensure_structure(self) -> None:
        """Create the necessary directory structure."""
        pass

    @abstractmethod
    def create_rule_file(self, name: str, content: str, globs: List[str]) -> bool:
        """Create a rule file with tool-specific metadata."""
        pass

    @abstractmethod
    def update_gitignore(self) -> None:
        """Update .gitignore with the tool-specific paths."""
        pass

    def _write_file_with_frontmatter(self, file_path: Path, content: str, metadata: Dict[str, Any]) -> bool:
        """Helper to consistently write YAML frontmatter and the Universal Preamble."""
        try:
            full_content = "---\n"
            full_content += yaml.dump(metadata, default_flow_style=None)
            full_content += "---\n\n"
            full_content += "# Universal AI Context\n"
            full_content += "You are operating in a multi-agent repository. Your native rules have been loaded.\n"
            full_content += "Always adhere to project_spec.md as the ultimate source of truth.\n"
            full_content += "If instructions conflict, prioritize: project_spec.md > Native Rules > Root Files.\n"
            full_content += (
                "CRITICAL: Before executing any task, you MUST read the root "
                "`AGENTS.md` file for common cross-IDE rules and repo status. "
                "If the status is `[TEMPLATE]`, you are strictly "
                "locked into the Bootstrapper persona (`.crules/modes/BOOTSTRAPPER.md`). "
                "Do not write code or manage tasks until the workspace is customized.\n\n"
            )
            full_content += content
            
            file_path.write_text(full_content)
            logger.info(f"Created rule file: {file_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to create rule file {file_path}: {e}")
            return False

    def _update_ignore_file(self, ignore_pattern: str) -> None:
        """Helper to consistently append patterns to .gitignore."""
        gitignore = Path(".gitignore")
        try:
            if gitignore.exists():
                content = gitignore.read_text()
                if ignore_pattern not in content:
                    if "# Crules specific" not in content:
                        content += "\n# Crules specific\n"
                    content += f"{ignore_pattern}\n"
                    gitignore.write_text(content)
                    logger.info(f"Updated .gitignore with {ignore_pattern}")
            else:
                gitignore.write_text(f"# Crules specific\n{ignore_pattern}\n")
                logger.info(f"Created .gitignore with {ignore_pattern}")
        except Exception as e:
            logger.warning(f"Failed to update .gitignore: {e}")


class CursorManager(BaseAIManager):
    """Manages the .cursor/rules directory structure."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.target_dir = Path(".cursor/rules")
        self.file_extension = ".mdc"

    def ensure_structure(self) -> None:
        self.target_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Ensured Cursor structure exists at {self.target_dir}")

    def create_rule_file(self, name: str, content: str, globs: List[str]) -> bool:
        file_path = self.target_dir / f"{name}{self.file_extension}"
        metadata = {
            "description": f"Rules for {name} development",
            "globs": globs
        }
        return self._write_file_with_frontmatter(file_path, content, metadata)

    def update_gitignore(self) -> None:
        self._update_ignore_file(f".cursor/rules/*{self.file_extension}")


class ClaudeManager(BaseAIManager):
    """Manages the .claude/rules directory structure."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.target_dir = Path(".claude/rules")
        self.file_extension = ".md"

    def ensure_structure(self) -> None:
        self.target_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Ensured Claude structure exists at {self.target_dir}")

    def _convert_to_globstar(self, globs: List[str]) -> List[str]:
        # Claude prefers deep matching (e.g., **/*.py instead of *.py)
        return [g if g.startswith("**") else f"**/{g}" for g in globs]

    def create_rule_file(self, name: str, content: str, globs: List[str]) -> bool:
        file_path = self.target_dir / f"{name}{self.file_extension}"
        metadata = {
            "description": f"Rules for {name} development",
            "paths": self._convert_to_globstar(globs)
        }
        return self._write_file_with_frontmatter(file_path, content, metadata)

    def update_gitignore(self) -> None:
        self._update_ignore_file(f".claude/rules/*{self.file_extension}")


class CopilotManager(BaseAIManager):
    """Manages the .github/instructions directory structure."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.target_dir = Path(".github/instructions")
        self.file_extension = ".instructions.md"

    def ensure_structure(self) -> None:
        self.target_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Ensured Copilot structure exists at {self.target_dir}")

    def _convert_to_globstar(self, globs: List[str]) -> List[str]:
        return [g if g.startswith("**") else f"**/{g}" for g in globs]

    def create_rule_file(self, name: str, content: str, globs: List[str]) -> bool:
        file_path = self.target_dir / f"{name}{self.file_extension}"
        metadata = {
            "description": f"Rules for {name} development",
            "applyTo": self._convert_to_globstar(globs)
        }
        return self._write_file_with_frontmatter(file_path, content, metadata)

    def update_gitignore(self) -> None:
        self._update_ignore_file(f".github/instructions/*{self.file_extension}")


class ClineManager(BaseAIManager):
    """Manages the .clinerules directory structure."""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.target_dir = Path(".clinerules")
        self.file_extension = ".md"

    def ensure_structure(self) -> None:
        self.target_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Ensured Cline structure exists at {self.target_dir}")

    def create_rule_file(self, name: str, content: str, globs: List[str]) -> bool:
        file_path = self.target_dir / f"{name}{self.file_extension}"
        metadata = {
            "description": f"Rules for {name} development",
            "globs": globs,
        }
        return self._write_file_with_frontmatter(file_path, content, metadata)

    def update_gitignore(self) -> None:
        self._update_ignore_file(f".clinerules/*{self.file_extension}")


class RooManager(BaseAIManager):
    """Manages the .roorules directory structure."""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.target_dir = Path(".roorules")
        self.file_extension = ".md"

    def ensure_structure(self) -> None:
        self.target_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Ensured Roo Code structure exists at {self.target_dir}")

    def create_rule_file(self, name: str, content: str, globs: List[str]) -> bool:
        file_path = self.target_dir / f"{name}{self.file_extension}"
        metadata = {
            "description": f"Rules for {name} development",
            "globs": globs,
        }
        return self._write_file_with_frontmatter(file_path, content, metadata)

    def update_gitignore(self) -> None:
        self._update_ignore_file(f".roorules/*{self.file_extension}")


class WindsurfManager(BaseAIManager):
    """Manages the .windsurf/rules directory structure."""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.target_dir = Path(".windsurf/rules")
        self.file_extension = ".md"

    def ensure_structure(self) -> None:
        self.target_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Ensured Windsurf structure exists at {self.target_dir}")

    def create_rule_file(self, name: str, content: str, globs: List[str]) -> bool:
        file_path = self.target_dir / f"{name}{self.file_extension}"
        metadata = {
            "description": f"Rules for {name} development",
            "globs": globs,
        }
        return self._write_file_with_frontmatter(file_path, content, metadata)

    def update_gitignore(self) -> None:
        self._update_ignore_file(f".windsurf/rules/*{self.file_extension}")


class AiderManager(BaseAIManager):
    """Manages the .aider/rules directory and ``read:`` entries in ``.aider.conf.yml``."""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.target_dir = Path(".aider/rules")
        self.file_extension = ".md"

    def ensure_structure(self) -> None:
        self.target_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Ensured Aider structure exists at {self.target_dir}")

    def _append_aider_conf_read(self, rule_path: Path) -> None:
        """Append ``- <path>`` under ``read:`` in ``.aider.conf.yml`` without YAML dump.

        Preserves comments and foreign keys by editing the raw file text only.
        """
        conf = Path(".aider.conf.yml")
        rel = rule_path.as_posix()
        list_marker = f"- {rel}"
        try:
            text = conf.read_text() if conf.exists() else ""
        except OSError as e:
            logger.warning("Could not read .aider.conf.yml: %s", e)
            return

        for raw_line in text.splitlines():
            if raw_line.strip() == list_marker:
                return

        lines = text.splitlines()
        read_idx = -1
        for i, line in enumerate(lines):
            head = line.split("#", 1)[0].rstrip()
            if re.match(r"^read:\s*$", head):
                read_idx = i
                break

        indent = "  "
        if read_idx < 0:
            block = f"read:\n{indent}{list_marker}"
            if not text.strip():
                new_text = block + "\n"
            else:
                new_text = text.rstrip("\n") + "\n" + block + "\n"
        else:
            j = read_idx + 1
            last_item_idx = read_idx
            while j < len(lines):
                line = lines[j]
                m_item = re.match(r"^(\s+)-\s", line)
                if m_item:
                    indent = m_item.group(1)
                    last_item_idx = j
                    j += 1
                    continue
                if not line.strip():
                    k = j + 1
                    while k < len(lines) and not lines[k].strip():
                        k += 1
                    if k < len(lines) and re.match(r"^\s+-\s", lines[k]):
                        j = k
                        continue
                    break
                break
            insert_at = last_item_idx + 1
            list_line = f"{indent}{list_marker}"
            new_lines = lines[:insert_at] + [list_line] + lines[insert_at:]
            new_text = "\n".join(new_lines) + "\n"

        try:
            conf.write_text(new_text)
        except OSError as e:
            logger.warning("Could not write .aider.conf.yml: %s", e)
            return
        logger.info("Registered %s under read: in %s (append-only text edit)", rel, conf)

    def create_rule_file(self, name: str, content: str, globs: List[str]) -> bool:
        file_path = self.target_dir / f"{name}{self.file_extension}"
        metadata = {
            "description": f"Rules for {name} development",
            "globs": globs,
        }
        ok = self._write_file_with_frontmatter(file_path, content, metadata)
        if ok:
            try:
                self._append_aider_conf_read(file_path)
            except Exception as e:
                logger.warning("Could not update .aider.conf.yml: %s", e)
        return ok

    def update_gitignore(self) -> None:
        self._update_ignore_file(f".aider/rules/*{self.file_extension}")
