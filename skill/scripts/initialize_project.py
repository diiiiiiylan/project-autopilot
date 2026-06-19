#!/usr/bin/env python3
"""Initialize a native or fallback project-autopilot change workspace."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path


TEMPLATE_NAMES = [
    "proposal.md",
    "design.md",
    "tasks.md",
    "department-brief.md",
    "handoff.md",
    "acceptance-report.md",
    "project-brief.md",
    "staffing-plan.md",
]

COORDINATION_TEMPLATE = "coordination-state.json"
COMPLEXITIES = {"small", "medium", "large", "enterprise"}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return slug[:64] or "change"


def skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def run_probe(command: list[str], cwd: Path) -> dict[str, object]:
    try:
        completed = subprocess.run(
            command,
            cwd=str(cwd),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=10,
            check=False,
        )
        return {
            "returncode": completed.returncode,
            "stdout": completed.stdout.strip()[:4000],
            "stderr": completed.stderr.strip()[:4000],
        }
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"error": str(exc)}


def detect_openspec(project: Path) -> dict[str, object]:
    exe = shutil.which("openspec")
    initialized_dirs = [
        item
        for item in (project / "openspec", project / "specs", project / ".openspec")
        if item.exists()
    ]
    result: dict[str, object] = {
        "command": exe,
        "initialized": bool(initialized_dirs),
        "initialized_dirs": [str(p.relative_to(project)) for p in initialized_dirs],
    }
    if exe:
        result["version"] = run_probe(["openspec", "--version"], project)
        result["help"] = run_probe(["openspec", "--help"], project)
    return result


def render_template(name: str, values: dict[str, str]) -> str:
    path = skill_root() / "assets" / "templates" / name
    content = path.read_text(encoding="utf-8")
    for key, value in values.items():
        content = content.replace("{{" + key + "}}", value)
    return content


def json_compact(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def active_departments_for(project_size: str) -> list[dict[str, object]]:
    if project_size == "medium":
        return [
            {
                "name": "requirements-architecture-department",
                "display_name": "需求架构部门",
                "scope_key": "requirements-and-architecture",
                "file_edit": False,
                "responsibility": "Clarify scope, inspect impact, design approach, and define acceptance.",
            },
            {
                "name": "development-department",
                "display_name": "开发部门",
                "scope_key": "bounded-implementation",
                "file_edit": True,
                "responsibility": "Implement bounded changes and necessary tests.",
            },
        ]
    if project_size in {"large", "enterprise"}:
        return [
            {
                "name": "requirements-architecture-department",
                "display_name": "需求架构部门",
                "scope_key": "requirements-and-architecture",
                "file_edit": False,
                "responsibility": "Clarify scope, inspect impact, design approach, and define acceptance.",
            },
            {
                "name": "development-department",
                "display_name": "开发部门",
                "scope_key": "bounded-implementation",
                "file_edit": True,
                "responsibility": "Implement bounded changes and necessary tests.",
            },
            {
                "name": "quality-assurance-department",
                "display_name": "质量保障部门",
                "scope_key": "verification-and-regression",
                "file_edit": False,
                "responsibility": "Design and run checks, reproduce failures, and collect evidence.",
            },
            {
                "name": "independent-review-department",
                "display_name": "独立审查部门",
                "scope_key": "independent-review",
                "file_edit": False,
                "responsibility": "Review correctness, safety, maintainability, requirements, and test gaps.",
            },
        ]
    return []


def inactive_departments_for(project_size: str) -> list[dict[str, object]]:
    departments = [
        {
            "name": "people-operations-department",
            "display_name": "人事协调部门",
            "scope_key": "staffing-and-conflict-check",
            "file_edit": False,
            "responsibility": "Recommend staffing changes, concurrency limits, task ownership, and conflict fixes.",
        }
    ]
    if project_size == "enterprise":
        departments.extend(
            [
                {
                    "name": "documentation-specialist",
                    "display_name": "文档临时员工",
                    "scope_key": "documentation",
                    "file_edit": True,
                    "responsibility": "Prepare docs only when documentation is an independent deliverable.",
                },
                {
                    "name": "security-specialist",
                    "display_name": "安全临时员工",
                    "scope_key": "security-review",
                    "file_edit": False,
                    "responsibility": "Review security-sensitive changes when risk justifies a separate pass.",
                },
            ]
        )
    return departments


def max_concurrency_for(project_size: str) -> int:
    if project_size == "medium":
        return 2
    if project_size in {"large", "enterprise"}:
        return 4
    return 1


def departments_markdown(departments: list[dict[str, object]]) -> str:
    if not departments:
        return "- None"
    lines: list[str] = []
    for department in departments:
        lines.extend(
            [
                f"- Role: {department['display_name']} (`{department['name']}`)",
                f"  - Scope: {department['scope_key']}",
                f"  - Responsibility: {department['responsibility']}",
                f"  - File edits: {'allowed' if department['file_edit'] else 'not allowed by default'}",
            ]
        )
    return "\n".join(lines)


def initialize_project(
    project: Path,
    title: str,
    force_fallback: bool = False,
    complexity: str = "medium",
) -> dict[str, object]:
    if complexity not in COMPLEXITIES:
        raise ValueError(f"Invalid complexity: {complexity}")
    project = project.resolve()
    project.mkdir(parents=True, exist_ok=True)
    change_id = slugify(title)
    if complexity == "small":
        return {
            "mode": "direct",
            "change_id": change_id,
            "created_or_updated_at": utc_now(),
            "change_dir": None,
            "created": [],
            "project_size": "small",
            "lead_thread_role": "initial-main-thread",
            "max_concurrency": 1,
            "active_departments": [],
            "inactive_departments": [],
        }
    openspec = detect_openspec(project)
    native = bool(openspec.get("command") and openspec.get("initialized")) and not force_fallback
    if native:
        base = project / str(openspec["initialized_dirs"][0]) / "changes" / change_id
        mode = "native"
    else:
        base = project / ".project-autopilot" / "changes" / change_id
        mode = "fallback"
    base.mkdir(parents=True, exist_ok=True)
    active_departments = active_departments_for(complexity)
    inactive_departments = inactive_departments_for(complexity)
    values = {
        "mode": mode,
        "change_id": change_id,
        "lead_thread_role": "initial-main-thread",
        "project_size": complexity,
        "max_concurrency": str(max_concurrency_for(complexity)),
        "active_departments": departments_markdown(active_departments),
        "inactive_departments": departments_markdown(inactive_departments),
        "active_departments_json": json_compact(active_departments),
        "inactive_departments_json": json_compact(inactive_departments),
        "updated_at": utc_now(),
        "target": title,
        "audience": "TBD",
        "in_scope": "TBD",
        "out_of_scope": "TBD",
        "acceptance_standard": "Applicable checks pass or blockers are recorded",
        "delivery_target": "TBD",
        "forbidden_actions": "TBD",
        "non_targets": "TBD",
        "constraints": "TBD",
        "assumptions": "TBD",
        "risks": "TBD",
        "context": "TBD",
        "solution": "TBD",
        "interfaces_and_data": "TBD",
        "alternatives": "TBD",
        "task_id": "task-001",
        "owner": "main",
        "task": "Define implementation tasks",
        "acceptance": "Applicable checks pass or blockers are recorded",
        "department": "main",
        "scope": "TBD",
        "inputs": "TBD",
        "output": "TBD",
        "completed": "TBD",
        "evidence": "TBD",
        "open_items": "TBD",
        "next_owner": "TBD",
        "status": "pending",
        "result": "TBD",
        "verification_evidence": "TBD",
        "blocked_checks": "TBD",
        "remaining_risks": "TBD",
    }
    created: list[str] = []
    for name in TEMPLATE_NAMES:
        target = base / name
        if not target.exists():
            target.write_text(render_template(name, values), encoding="utf-8", newline="\n")
            created.append(str(target.relative_to(project)))
    coordination_state = base / COORDINATION_TEMPLATE
    coordination_state_exists = coordination_state.exists()
    coordination_state.write_text(
        render_template(COORDINATION_TEMPLATE, values),
        encoding="utf-8",
        newline="\n",
    )
    if not coordination_state_exists:
        created.append(str(coordination_state.relative_to(project)))
    registry = base / "task-registry.json"
    if not registry.exists():
        registry.write_text('{\n  "version": 1,\n  "tasks": {}\n}\n', encoding="utf-8", newline="\n")
        created.append(str(registry.relative_to(project)))
    manifest = {
        "mode": mode,
        "change_id": change_id,
        "created_or_updated_at": utc_now(),
        "openspec": openspec,
        "change_dir": str(base),
        "created": created,
        "project_size": complexity,
        "lead_thread_role": "initial-main-thread",
        "max_concurrency": max_concurrency_for(complexity),
        "active_departments": active_departments,
        "inactive_departments": inactive_departments,
    }
    (base / "project-autopilot-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return manifest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, default=Path.cwd())
    parser.add_argument("--title", required=True)
    parser.add_argument("--force-fallback", action="store_true")
    parser.add_argument("--complexity", choices=sorted(COMPLEXITIES), default="medium")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = initialize_project(args.project, args.title, args.force_fallback, args.complexity)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
