"""Tests for ai_managers module."""
import pytest
from pathlib import Path
from importlib import resources
import yaml
from crules.ai_managers import CursorManager, ClaudeManager, CopilotManager
from crules import file_ops


@pytest.fixture
def test_config():
    return {
        "file_extension": ".mdc",
        "enable_cursor": True,
        "enable_claude": True,
        "enable_copilot": True,
    }


@pytest.fixture
def chdir_tmp(tmp_path, monkeypatch):
    """Change working directory to tmp_path for the duration of the test."""
    monkeypatch.chdir(tmp_path)
    return tmp_path


@pytest.fixture
def bootstrap_env(tmp_path, monkeypatch):
    """Isolated environment for bootstrap tests.

    Sets HOME to a fake directory inside tmp_path so that
    ``~/.config/crules/workflows`` resolves predictably, then seeds
    the config dir with a global-rules file and workflow templates.
    """
    monkeypatch.chdir(tmp_path)

    fake_home = tmp_path / "fakehome"
    monkeypatch.setenv("HOME", str(fake_home))

    config_base = fake_home / ".config" / "crules"
    global_rules = config_base / "cursorrules"
    lang_rules_dir = config_base / "lang_rules"
    workflows_dir = config_base / "workflows"

    for d in (config_base, lang_rules_dir, workflows_dir):
        d.mkdir(parents=True)

    global_rules.write_text("# Global rules content\n")

    with resources.as_file(resources.files("crules.rules.workflows")) as wf_src:
        for md in wf_src.glob("*.md"):
            (workflows_dir / md.name).write_text(md.read_text())

    cfg = {
        "global_rules_path": str(global_rules),
        "language_rules_dir": str(lang_rules_dir),
        "file_extension": ".mdc",
        "enable_cursor": True,
        "enable_claude": True,
        "enable_copilot": True,
    }
    return tmp_path, cfg


# --------------- helpers ---------------

def _parse_frontmatter(text: str) -> dict:
    """Extract the YAML frontmatter from a rule file."""
    parts = text.split("---", 2)
    assert len(parts) >= 3, "Expected YAML frontmatter delimited by ---"
    return yaml.safe_load(parts[1])


# --------------- CursorManager ---------------

class TestCursorManager:
    def test_ensure_structure(self, test_config, chdir_tmp):
        manager = CursorManager(test_config)
        manager.ensure_structure()

        assert (chdir_tmp / ".cursor" / "rules").is_dir()

    def test_create_rule_file_extension(self, test_config, chdir_tmp):
        manager = CursorManager(test_config)
        manager.ensure_structure()

        assert manager.create_rule_file("global", "content", ["*"])
        rule_file = chdir_tmp / ".cursor" / "rules" / "global.mdc"
        assert rule_file.exists()

    def test_metadata_uses_globs_key(self, test_config, chdir_tmp):
        manager = CursorManager(test_config)
        manager.ensure_structure()
        manager.create_rule_file("python", "# py rules", ["*.py"])

        text = (chdir_tmp / ".cursor" / "rules" / "python.mdc").read_text()
        meta = _parse_frontmatter(text)
        assert "globs" in meta
        assert meta["globs"] == ["*.py"]
        assert "paths" not in meta
        assert "applyTo" not in meta

    def test_update_gitignore(self, test_config, chdir_tmp):
        manager = CursorManager(test_config)
        manager.update_gitignore()

        gitignore = chdir_tmp / ".gitignore"
        assert gitignore.exists()
        content = gitignore.read_text()
        assert ".cursor/rules/*.mdc" in content

    def test_update_gitignore_no_duplicate(self, test_config, chdir_tmp):
        manager = CursorManager(test_config)
        manager.update_gitignore()
        manager.update_gitignore()

        content = (chdir_tmp / ".gitignore").read_text()
        assert content.count(".cursor/rules/*.mdc") == 1


# --------------- ClaudeManager ---------------

class TestClaudeManager:
    def test_ensure_structure(self, test_config, chdir_tmp):
        manager = ClaudeManager(test_config)
        manager.ensure_structure()

        assert (chdir_tmp / ".claude" / "rules").is_dir()

    def test_create_rule_file_extension(self, test_config, chdir_tmp):
        manager = ClaudeManager(test_config)
        manager.ensure_structure()

        assert manager.create_rule_file("global", "content", ["*"])
        rule_file = chdir_tmp / ".claude" / "rules" / "global.md"
        assert rule_file.exists()

    def test_metadata_uses_paths_key(self, test_config, chdir_tmp):
        manager = ClaudeManager(test_config)
        manager.ensure_structure()
        manager.create_rule_file("python", "# py rules", ["*.py"])

        text = (chdir_tmp / ".claude" / "rules" / "python.md").read_text()
        meta = _parse_frontmatter(text)
        assert "paths" in meta
        assert meta["paths"] == ["**/*.py"]
        assert "globs" not in meta
        assert "applyTo" not in meta

    def test_globstar_conversion(self, test_config, chdir_tmp):
        manager = ClaudeManager(test_config)
        manager.ensure_structure()
        manager.create_rule_file("all", "content", ["*"])

        meta = _parse_frontmatter(
            (chdir_tmp / ".claude" / "rules" / "all.md").read_text()
        )
        assert meta["paths"] == ["**/*"]

    def test_update_gitignore(self, test_config, chdir_tmp):
        manager = ClaudeManager(test_config)
        manager.update_gitignore()

        content = (chdir_tmp / ".gitignore").read_text()
        assert ".claude/rules/*.md" in content


# --------------- CopilotManager ---------------

class TestCopilotManager:
    def test_ensure_structure(self, test_config, chdir_tmp):
        manager = CopilotManager(test_config)
        manager.ensure_structure()

        assert (chdir_tmp / ".github" / "instructions").is_dir()

    def test_create_rule_file_extension(self, test_config, chdir_tmp):
        manager = CopilotManager(test_config)
        manager.ensure_structure()

        assert manager.create_rule_file("global", "content", ["*"])
        rule_file = chdir_tmp / ".github" / "instructions" / "global.instructions.md"
        assert rule_file.exists()

    def test_metadata_uses_applyto_key(self, test_config, chdir_tmp):
        manager = CopilotManager(test_config)
        manager.ensure_structure()
        manager.create_rule_file("python", "# py rules", ["*.py"])

        text = (chdir_tmp / ".github" / "instructions" / "python.instructions.md").read_text()
        meta = _parse_frontmatter(text)
        assert "applyTo" in meta
        assert meta["applyTo"] == ["**/*.py"]
        assert "globs" not in meta
        assert "paths" not in meta

    def test_globstar_conversion(self, test_config, chdir_tmp):
        manager = CopilotManager(test_config)
        manager.ensure_structure()
        manager.create_rule_file("all", "content", ["*"])

        meta = _parse_frontmatter(
            (chdir_tmp / ".github" / "instructions" / "all.instructions.md").read_text()
        )
        assert meta["applyTo"] == ["**/*"]

    def test_update_gitignore(self, test_config, chdir_tmp):
        manager = CopilotManager(test_config)
        manager.update_gitignore()

        content = (chdir_tmp / ".gitignore").read_text()
        assert ".github/instructions/*.instructions.md" in content


# --------------- Universal preamble ---------------

class TestUniversalPreamble:
    """Verify every manager injects the preamble."""

    @pytest.mark.parametrize("manager_cls,subdir,ext", [
        (CursorManager, ".cursor/rules", ".mdc"),
        (ClaudeManager, ".claude/rules", ".md"),
        (CopilotManager, ".github/instructions", ".instructions.md"),
    ])
    def test_preamble_present(self, test_config, chdir_tmp, manager_cls, subdir, ext):
        manager = manager_cls(test_config)
        manager.ensure_structure()
        manager.create_rule_file("global", "body", ["*"])

        text = (chdir_tmp / subdir / f"global{ext}").read_text()
        assert "# Universal AI Context" in text
        assert "project_spec.md" in text


# --------------- Swarm Bootstrap ---------------

class TestSwarmBootstrap:
    def test_bootstrap_structure(self, bootstrap_env):
        project_dir, cfg = bootstrap_env

        assert file_ops.bootstrap_swarm(cfg) is True

        for sub in ("tasks/wip", "tasks/review", "tasks/done", "modes"):
            assert (project_dir / ".crules" / sub).is_dir(), (
                f".crules/{sub} was not created"
            )

        spec = project_dir / "project_spec.md"
        assert spec.exists(), "project_spec.md was not created"
        spec_text = spec.read_text()
        assert "# Project Specification" in spec_text
        assert "EVALUATION REQUIRED" in spec_text

    def test_workflow_template_copy(self, bootstrap_env):
        project_dir, cfg = bootstrap_env

        assert file_ops.bootstrap_swarm(cfg) is True

        modes_dir = project_dir / ".crules" / "modes"
        for filename in ("MANAGER.md", "CODER.md"):
            mode_file = modes_dir / filename
            assert mode_file.exists(), f"{filename} not found in .crules/modes/"
            assert mode_file.stat().st_size > 0, f"{filename} is empty"

        global_rule = project_dir / ".cursor" / "rules" / "global.mdc"
        assert global_rule.exists(), "global.mdc not deployed during bootstrap"
        rule_text = global_rule.read_text()
        assert "# Universal AI Context" in rule_text
        assert "project_spec.md" in rule_text
