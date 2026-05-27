from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from providers.base import ProviderRequest
from providers.mock import MockProvider

from .approvals import is_approved
from .io import read_json, read_yaml, write_json
from .projects import Project


ROOT = Path(__file__).resolve().parents[1]

TEMPLATE_BY_OUTPUT = {
    "BRD": "brd.md",
    "SRD and FRD": "frd.md",
    "Solution Architecture": "solution-architecture.md",
    "Technical Design": "technical-design.md",
    "Test Plan": "test-plan.md",
    "Task Breakdown": "task-breakdown.md",
    "Review Report": "review-report.md",
}


class WorkflowRunner:
    def __init__(self, project: Project, provider: Any | None = None, dry_run: bool = False) -> None:
        self.project = project
        self.provider = provider or MockProvider()
        self.dry_run = dry_run

    def run(self, workflow_id: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        workflow = read_yaml(ROOT / "workflows" / f"{workflow_id}.yaml")
        run_id = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
        run = {
            "id": run_id,
            "workflow_id": workflow_id,
            "project": self.project.name,
            "status": "running",
            "dry_run": self.dry_run,
            "started_at": datetime.now(timezone.utc).isoformat(),
            "steps": [],
        }
        for step in workflow.get("steps", []):
            gate = step.get("approval_gate")
            if gate and not is_approved(self.project, gate):
                run["status"] = "blocked"
                run["blocked_gate"] = gate
                break
            request = ProviderRequest(
                prompt=step.get("input", ""),
                agent_id=step.get("agent", "delivery-orchestrator"),
                context={"title": step.get("output", step.get("id")), "payload": payload or {}},
            )
            response = self.provider.generate(request)
            content = self._render_output(step, response.content)
            output_path = self.project.system_dir / "runs" / run_id / f"{step.get('id')}.md"
            if not self.dry_run:
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_text(content, encoding="utf-8")
                self._write_document(step, content)
            run["steps"].append(
                {
                    "id": step.get("id"),
                    "agent": step.get("agent"),
                    "status": "completed",
                    "approval_gate": gate,
                    "output_path": str(output_path),
                    "metadata": response.metadata,
                }
            )
        else:
            run["status"] = "completed"
        run["finished_at"] = datetime.now(timezone.utc).isoformat()
        self._persist_run(run)
        return run

    def _persist_run(self, run: dict[str, Any]) -> None:
        state = read_json(self.project.state_path, {})
        state.setdefault("runs", []).append(run)
        state["active_workflow"] = run["workflow_id"]
        if not self.dry_run:
            write_json(self.project.state_path, state)
            write_json(self.project.system_dir / "runs" / run["id"] / "run.json", run)

    def _render_output(self, step: dict[str, Any], generated: str) -> str:
        template_name = TEMPLATE_BY_OUTPUT.get(str(step.get("output")))
        if not template_name:
            return generated
        template_path = ROOT / "documents" / "templates" / template_name
        template = template_path.read_text(encoding="utf-8")
        return f"{template.rstrip()}\n\n## Generated Draft\n\n{generated}"

    def _write_document(self, step: dict[str, Any], content: str) -> None:
        template_name = TEMPLATE_BY_OUTPUT.get(str(step.get("output")))
        if not template_name:
            return
        docs_dir = self.project.path / self.project.config.get("document_path", ".ai-system/docs")
        docs_dir.mkdir(parents=True, exist_ok=True)
        (docs_dir / template_name).write_text(content, encoding="utf-8")
