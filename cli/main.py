from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from runtime.approvals import approve
from runtime.io import read_json
from runtime.projects import (
    REGISTRY_PATH,
    init_project,
    load_project,
    load_registry,
    register_project,
    use_project,
)
from runtime.tasks import commit_task, review_task, run_task
from runtime.workflows import WorkflowRunner


def print_result(data: Any) -> None:
    import json

    print(json.dumps(data, indent=2, sort_keys=True))


def cmd_init_project(args: argparse.Namespace) -> None:
    project = init_project(Path(args.path).expanduser(), args.name, args.type)
    print_result({"status": "initialized", "project": project.name, "path": str(project.path)})


def cmd_register_project(args: argparse.Namespace) -> None:
    project = register_project(args.name, Path(args.path).expanduser(), args.type)
    print_result({"status": "registered", "project": project.name, "path": str(project.path)})


def cmd_use_project(args: argparse.Namespace) -> None:
    project = use_project(args.name)
    print_result({"status": "active", "project": project.name, "path": str(project.path)})


def cmd_list_projects(args: argparse.Namespace) -> None:
    registry = load_registry()
    registry["registry_path"] = str(REGISTRY_PATH)
    print_result(registry)


def cmd_project_status(args: argparse.Namespace) -> None:
    project = load_project(args.name)
    state = read_json(project.state_path, {})
    print_result({"project": project.config, "state": state})


def cmd_intake(args: argparse.Namespace) -> None:
    project = load_project(args.project)
    payload = {"file": args.file, "content": Path(args.file).read_text(encoding="utf-8")}
    run = WorkflowRunner(project, dry_run=args.dry_run).run("01-intake-to-docs", payload)
    print_result(run)


def cmd_run_workflow(args: argparse.Namespace) -> None:
    project = load_project(args.project)
    run = WorkflowRunner(project, dry_run=args.dry_run).run(args.workflow, {"input": args.input or ""})
    print_result(run)


def cmd_approve(args: argparse.Namespace) -> None:
    project = load_project(args.project)
    print_result(approve(project, args.gate, args.note or ""))


def cmd_run_task(args: argparse.Namespace) -> None:
    project = load_project(args.project)
    print_result(run_task(project, args.task_id, dry_run=args.dry_run))


def cmd_review_task(args: argparse.Namespace) -> None:
    project = load_project(args.project)
    print_result(review_task(project, args.task_id, dry_run=args.dry_run))


def cmd_commit_task(args: argparse.Namespace) -> None:
    project = load_project(args.project)
    print_result(commit_task(project, args.task_id, dry_run=args.dry_run))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ai-system")
    parser.add_argument("--dry-run", action="store_true", help="Run without writing generated artifacts when supported.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init = subparsers.add_parser("init-project")
    init.add_argument("--name", required=True)
    init.add_argument("--path", default=".")
    init.add_argument("--type", default="generic")
    init.set_defaults(func=cmd_init_project)

    register = subparsers.add_parser("register-project")
    register.add_argument("--name", required=True)
    register.add_argument("--path", required=True)
    register.add_argument("--type", default="generic")
    register.set_defaults(func=cmd_register_project)

    use = subparsers.add_parser("use-project")
    use.add_argument("name")
    use.set_defaults(func=cmd_use_project)

    intake = subparsers.add_parser("intake")
    intake.add_argument("--file", required=True)
    intake.add_argument("--project")
    intake.set_defaults(func=cmd_intake)

    workflow = subparsers.add_parser("run-workflow")
    workflow.add_argument("workflow")
    workflow.add_argument("--input")
    workflow.add_argument("--project")
    workflow.set_defaults(func=cmd_run_workflow)

    approval = subparsers.add_parser("approve")
    approval.add_argument("--gate", required=True)
    approval.add_argument("--note")
    approval.add_argument("--project")
    approval.set_defaults(func=cmd_approve)

    run_task_parser = subparsers.add_parser("run-task")
    run_task_parser.add_argument("task_id")
    run_task_parser.add_argument("--project")
    run_task_parser.set_defaults(func=cmd_run_task)

    review = subparsers.add_parser("review-task")
    review.add_argument("task_id")
    review.add_argument("--project")
    review.set_defaults(func=cmd_review_task)

    commit = subparsers.add_parser("commit-task")
    commit.add_argument("task_id")
    commit.add_argument("--project")
    commit.set_defaults(func=cmd_commit_task)

    status = subparsers.add_parser("project-status")
    status.add_argument("--name")
    status.set_defaults(func=cmd_project_status)

    listing = subparsers.add_parser("list-projects")
    listing.set_defaults(func=cmd_list_projects)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)
    return 0
