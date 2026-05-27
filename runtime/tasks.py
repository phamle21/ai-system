from __future__ import annotations

from datetime import datetime, timezone

from .approvals import is_approved
from .io import read_json, write_json
from .projects import Project
from .safety import diff_summary, ensure_git_branch, run_command


def run_task(project: Project, task_id: str, dry_run: bool = False) -> dict[str, object]:
    if project.config.get("human_approval_required", True) and not is_approved(project, "task-plan"):
        return {"task_id": task_id, "status": "blocked", "blocked_gate": "task-plan"}
    branch = ensure_git_branch(project, dry_run=dry_run)
    log = {
        "task_id": task_id,
        "status": "planned" if dry_run else "executed",
        "branch": branch,
        "execution_plan": [
            "Load task context.",
            "Check approval gates.",
            "Ensure AI working branch.",
            "Run configured tests.",
            "Generate diff summary.",
        ],
        "test": run_command(project, project.config.get("test_command", "")) if not dry_run else {},
        "diff_summary": diff_summary(project) if not dry_run else "Dry run: no diff generated.",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    if not dry_run:
        write_json(project.system_dir / "tasks" / f"{task_id}.run.json", log)
        state = read_json(project.state_path, {})
        state.setdefault("tasks", {})[task_id] = {"status": log["status"], "updated_at": log["created_at"]}
        write_json(project.state_path, state)
    return log


def review_task(project: Project, task_id: str, dry_run: bool = False) -> dict[str, object]:
    report = {
        "task_id": task_id,
        "status": "reviewed",
        "review_required": project.config.get("review_required", True),
        "diff_summary": diff_summary(project) if not dry_run else "Dry run: review only.",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    if not dry_run:
        write_json(project.system_dir / "tasks" / f"{task_id}.review.json", report)
    return report


def commit_task(project: Project, task_id: str, dry_run: bool = False) -> dict[str, object]:
    if project.config.get("review_required", True):
        review_path = project.system_dir / "tasks" / f"{task_id}.review.json"
        if not review_path.exists():
            return {"task_id": task_id, "status": "blocked", "reason": "review-required"}
    return {
        "task_id": task_id,
        "status": "ready-to-commit" if dry_run else "commit-not-implemented",
        "message": "MVP records commit intent; wire Git commit policy in a future provider.",
    }

