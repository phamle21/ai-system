from __future__ import annotations

from datetime import datetime, timezone

from .io import read_json, write_json
from .projects import Project


def approval_key(gate: str) -> str:
    return gate.strip().lower().replace(" ", "-")


def approve(project: Project, gate: str, note: str = "") -> dict[str, str]:
    key = approval_key(gate)
    state = read_json(project.state_path, {"approvals": {}})
    approval = {
        "gate": key,
        "status": "approved",
        "note": note,
        "approved_at": datetime.now(timezone.utc).isoformat(),
    }
    state.setdefault("approvals", {})[key] = approval
    write_json(project.state_path, state)
    write_json(project.system_dir / "approvals" / f"{key}.json", approval)
    return approval


def is_approved(project: Project, gate: str | None) -> bool:
    if not gate:
        return True
    state = read_json(project.state_path, {"approvals": {}})
    approval = state.get("approvals", {}).get(approval_key(gate), {})
    return approval.get("status") == "approved"

