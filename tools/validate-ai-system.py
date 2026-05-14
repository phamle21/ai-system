#!/usr/bin/env python3
"""Validate ai-system YAML files and internal skill/pipeline references."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
STRICT_DIRS = {"agents", "pipelines", "projects"}


def load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def collect_skill_refs(value: Any) -> set[str]:
    refs: set[str] = set()
    if isinstance(value, dict):
        for item in value.values():
            refs.update(collect_skill_refs(item))
    elif isinstance(value, list):
        for item in value:
            refs.update(collect_skill_refs(item))
    elif isinstance(value, str):
        if value.startswith("skills/") or value.startswith("projects/"):
            refs.add(value)
    return refs


def collect_pipeline_refs(value: Any) -> set[str]:
    refs: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            if key == "pipeline" and isinstance(item, str):
                refs.add(item)
            else:
                refs.update(collect_pipeline_refs(item))
    elif isinstance(value, list):
        for item in value:
            refs.update(collect_pipeline_refs(item))
    return refs


def ref_exists(ref: str) -> bool:
    direct = ROOT / ref
    if direct.exists():
        return True
    return direct.with_suffix(".yaml").exists() or direct.with_suffix(".md").exists()


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    yaml_files = sorted(
        path
        for path in ROOT.rglob("*")
        if path.suffix in {".yaml", ".yml"} and ".git" not in path.parts
    )

    parsed: dict[Path, Any] = {}
    for path in yaml_files:
        try:
            parsed[path] = load_yaml(path)
        except Exception as exc:
            rel = path.relative_to(ROOT)
            if path.parts[len(ROOT.parts)] in STRICT_DIRS:
                errors.append(f"YAML parse failed: {rel}: {exc}")
            else:
                warnings.append(f"Skipped legacy pseudo-YAML: {rel}")

    for path, data in parsed.items():
        if not isinstance(data, dict):
            errors.append(f"YAML root must be a mapping: {path.relative_to(ROOT)}")
            continue

        if path.parts[-2] in {"core", "wordpress", "laravel", "frontend", "testing"}:
            for field in ("name", "description", "version"):
                if field not in data:
                    errors.append(f"Missing {field}: {path.relative_to(ROOT)}")

        for ref in collect_skill_refs(data):
            if ref.endswith("/*"):
                continue
            if not ref_exists(ref):
                errors.append(f"Missing skill/project reference in {path.relative_to(ROOT)}: {ref}")

        for pipeline in collect_pipeline_refs(data):
            pipeline_path = ROOT / "pipelines" / f"{pipeline}.yaml"
            if not pipeline_path.exists():
                errors.append(f"Missing pipeline in {path.relative_to(ROOT)}: {pipeline}")

    if errors:
        print("ai-system validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    if warnings:
        print("ai-system validation warnings:")
        for warning in warnings:
            print(f"- {warning}")

    print(f"ai-system validation passed ({len(yaml_files)} YAML files)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
