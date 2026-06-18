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
]


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


def initialize_project(project: Path, title: str, force_fallback: bool = False) -> dict[str, object]:
    project = project.resolve()
    project.mkdir(parents=True, exist_ok=True)
    change_id = slugify(title)
    openspec = detect_openspec(project)
    native = bool(openspec.get("command") and openspec.get("initialized")) and not force_fallback
    if native:
        base = project / str(openspec["initialized_dirs"][0]) / "changes" / change_id
        mode = "native"
    else:
        base = project / ".project-autopilot" / "changes" / change_id
        mode = "fallback"
    base.mkdir(parents=True, exist_ok=True)
    values = {
        "mode": mode,
        "change_id": change_id,
        "target": title,
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
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = initialize_project(args.project, args.title, args.force_fallback)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
