"""Configuration management for crules."""
from pathlib import Path
from typing import Dict, Any
import yaml
import logging

logger = logging.getLogger(__name__)

DEFAULT_CONFIG = {
    "global_rules_path": "~/.config/Cursor/cursor-rules/cursorrules",
    "language_rules_dir": "~/.config/Cursor/cursor-rules/lang_rules",
    "project_rules_dir": ".cursor/rules",
    "delimiter": "\n# --- Delimiter ---\n",
    "use_legacy": False,
    "file_extension": ".mdc",
}

def load_config() -> Dict[str, Any]:
    """Load configuration from YAML file or return defaults.
    
    Returns:
        Dict[str, Any]: Configuration dictionary with all settings
    """
    config_path = Path("~/.config/Cursor/cursor-rules/config.yaml").expanduser()
    
    try:
        if config_path.exists():
            with config_path.open() as f:
                config = yaml.safe_load(f)
                logger.debug(f"Loaded configuration from {config_path}")
                return {**DEFAULT_CONFIG, **(config or {})}
    except Exception as e:
        logger.warning(f"Error loading config file: {e}")
    
    logger.debug("Using default configuration")
    return DEFAULT_CONFIG 