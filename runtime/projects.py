from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .io import read_json, read_yaml, write_json, write_yaml


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = Path(os.environ.get("AI_SYSTEM_REGISTRY", "~/.ai-system/projects.json")).expanduser()


DEFAULT_PROJECT_CONFIG: dict[str, Any] = {
    "project_name": "",
    "project_type": "generic",
    "repo_path": "",
    "default_branch": "main",
    "working_branch_prefix": "ai/",
    "tech_stack": [],
    "coding_rules": [],
    "test_command": "",
    "build_command": "",
    "deploy_command": "",
    "document_path": ".ai-system/docs",
    "review_required": True,
    "human_approval_required": True,
}


@dataclass(slots=True)
class Project:
    name: str
    path: Path
    config: dict[str, Any]

    @property
    def system_dir(self) -> Path:
        return self.path / ".ai-system"

    @property
    def state_path(self) -> Path:
        return self.system_dir / "state.json"


def load_registry() -> dict[str, Any]:
    return read_json(REGISTRY_PATH, {"current_project": None, "projects": {}})


def save_registry(registry: dict[str, Any]) -> None:
    write_json(REGISTRY_PATH, registry)


def init_project(path: Path, name: str, project_type: str = "generic") -> Project:
    system_dir = path / ".ai-system"
    for child in ("approvals", "runs", "memory", "tasks", "docs"):
        (system_dir / child).mkdir(parents=True, exist_ok=True)

    config_path = system_dir / "project.yaml"
    config = DEFAULT_PROJECT_CONFIG | {
        "project_name": name,
        "project_type": project_type,
        "repo_path": str(path.resolve()),
    }
    if config_path.exists():
        existing = read_yaml(config_path)
        config = DEFAULT_PROJECT_CONFIG | existing | {
            "project_name": existing.get("project_name") or name,
            "project_type": existing.get("project_type") or project_type,
            "repo_path": existing.get("repo_path") or str(path.resolve()),
        }
    write_yaml(config_path, config)

    state_path = system_dir / "state.json"
    if not state_path.exists():
        write_json(state_path, {"tasks": {}, "approvals": {}, "runs": [], "active_workflow": None})

    memory_defaults = {
        "decisions.md": "# Decisions\n\n",
        "assumptions.md": "# Assumptions\n\n",
        "glossary.md": "# Glossary\n\n",
        "architecture.md": "# Architecture Memory\n\n",
        "conventions.md": "# Conventions\n\n",
    }
    for filename, content in memory_defaults.items():
        target = system_dir / "memory" / filename
        if not target.exists():
            target.write_text(content, encoding="utf-8")
    task_history = system_dir / "memory" / "task-history.json"
    if not task_history.exists():
        write_json(task_history, [])

    return Project(name=name, path=path.resolve(), config=config)


def register_project(name: str, path: Path, project_type: str = "generic") -> Project:
    project = init_project(path.resolve(), name, project_type)
    registry = load_registry()
    registry.setdefault("projects", {})[name] = {
        "name": name,
        "path": str(project.path),
        "type": project_type,
    }
    registry["current_project"] = registry.get("current_project") or name
    save_registry(registry)
    return project


def use_project(name: str) -> Project:
    registry = load_registry()
    if name not in registry.get("projects", {}):
        raise ValueError(f"Project is not registered: {name}")
    registry["current_project"] = name
    save_registry(registry)
    return load_project(name)


def load_project(name: str | None = None) -> Project:
    registry = load_registry()
    selected = name or registry.get("current_project")
    if not selected:
        raise ValueError("No active project. Run `ai-system register-project` or `ai-system use-project`.")
    item = registry.get("projects", {}).get(selected)
    if not item:
        raise ValueError(f"Project is not registered: {selected}")
    path = Path(item["path"]).expanduser().resolve()
    config = read_yaml(path / ".ai-system" / "project.yaml")
    return Project(name=selected, path=path, config=config)

