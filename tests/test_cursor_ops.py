"""Tests for cursor_ops module."""
import pytest
from pathlib import Path
import yaml
from crules.cursor_ops import CursorDirectoryManager

@pytest.fixture
def test_config():
    """Fixture providing test configuration."""
    return {
        "project_rules_dir": ".cursor/rules",
        "file_extension": ".mdc",
        "backup_existing": True
    }

@pytest.fixture
def cursor_manager(test_config, tmp_path):
    """Fixture providing a CursorDirectoryManager instance in a temporary directory."""
    original_cwd = Path.cwd()
    try:
        Path(tmp_path).mkdir(exist_ok=True)
        Path.chdir(tmp_path)
        yield CursorDirectoryManager(test_config)
    finally:
        Path.chdir(original_cwd)

def test_ensure_cursor_structure(cursor_manager, tmp_path):
    """Test creation of .cursor directory structure."""
    cursor_manager.ensure_cursor_structure()
    
    assert (tmp_path / ".cursor").exists()
    assert (tmp_path / ".cursor" / "rules").exists()
    assert (tmp_path / ".cursor" / "rules").is_dir()

def test_create_rule_file(cursor_manager, tmp_path):
    """Test creation of rule file with and without metadata."""
    cursor_manager.ensure_cursor_structure()
    
    # Test without metadata
    content = "# Test rule\nThis is a test rule"
    assert cursor_manager.create_rule_file("test", content)
    
    rule_file = tmp_path / ".cursor" / "rules" / "test.mdc"
    assert rule_file.exists()
    assert rule_file.read_text() == content
    
    # Test with metadata
    metadata = {
        "description": "Test rule with metadata",
        "globs": ["*.py"]
    }
    assert cursor_manager.create_rule_file("test_meta", content, metadata)
    
    meta_file = tmp_path / ".cursor" / "rules" / "test_meta.mdc"
    assert meta_file.exists()
    
    file_content = meta_file.read_text()
    assert "---" in file_content
    assert "description:" in file_content
    assert content in file_content

def test_backup_rules(cursor_manager, tmp_path):
    """Test backup functionality for existing rules."""
    cursor_manager.ensure_cursor_structure()
    
    # Create a test rule
    test_content = "# Test rule"
    cursor_manager.create_rule_file("test", test_content)
    
    # Backup should succeed
    assert cursor_manager.backup_rules_if_needed()
    
    backup_dir = tmp_path / ".cursor" / "rules.bak"
    assert backup_dir.exists()
    assert (backup_dir / "test.mdc").exists()
    assert (backup_dir / "test.mdc").read_text() == test_content

def test_list_rule_files(cursor_manager, tmp_path):
    """Test listing of rule files."""
    cursor_manager.ensure_cursor_structure()
    
    # Create test rules
    cursor_manager.create_rule_file("test1", "content1")
    cursor_manager.create_rule_file("test2", "content2")
    
    rules = cursor_manager.list_rule_files()
    assert len(rules) == 2
    assert any(rule.name == "test1.mdc" for rule in rules)
    assert any(rule.name == "test2.mdc" for rule in rules)

def test_update_gitignore(cursor_manager, tmp_path):
    """Test .gitignore update functionality."""
    cursor_manager.update_gitignore()
    
    gitignore = tmp_path / ".gitignore"
    assert gitignore.exists()
    content = gitignore.read_text()
    
    assert "# Cursor specific" in content
    assert ".cursor/rules/*.mdc" in content
    
    # Test adding to existing .gitignore
    with open(gitignore, "w") as f:
        f.write("node_modules/\n")
    
    cursor_manager.update_gitignore()
    content = gitignore.read_text()
    
    assert "node_modules/" in content
    assert ".cursor/rules/*.mdc" in content
    assert content.count(".cursor/rules/*.mdc") == 1  # Should not duplicate 