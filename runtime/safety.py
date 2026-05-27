from __future__ import annotations

import subprocess
from pathlib import Path

from .projects import Project


def ensure_git_branch(project: Project, dry_run: bool = False) -> str:
    if not (project.path / ".git").exists():
        return "not-a-git-repo"
    current = subprocess.run(
        ["git", "branch", "--show-current"],
        cwd=project.path,
        check=False,
        capture_output=True,
        text=True,
    ).stdout.strip()
    prefix = project.config.get("working_branch_prefix", "ai/")
    if current.startswith(prefix) or dry_run:
        return current or "unknown"
    branch = f"{prefix}delivery-task"
    subprocess.run(["git", "checkout", "-B", branch], cwd=project.path, check=True)
    return branch


def diff_summary(project: Project) -> str:
    if not (project.path / ".git").exists():
        return "Git diff unavailable: project is not a git repository."
    result = subprocess.run(
        ["git", "diff", "--stat"],
        cwd=project.path,
        check=False,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip() or "No file changes."


def run_command(project: Project, command: str) -> dict[str, str | int]:
    if not command:
        return {"command": "", "returncode": 0, "stdout": "No command configured.", "stderr": ""}
    result = subprocess.run(
        command,
        cwd=project.path,
        shell=True,
        check=False,
        capture_output=True,
        text=True,
    )
    return {
        "command": command,
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }

