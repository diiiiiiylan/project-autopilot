#!/usr/bin/env python3
"""Read-only audit for project-autopilot skillbox dependencies."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path


DEPENDENCIES = [
    {"id": "project-autopilot", "type": "skill", "required": True},
    {"id": "project-intake", "type": "skill", "required": True},
    {"id": "project-staffing", "type": "skill", "required": True},
    {"id": "project-domain-router", "type": "skill", "required": True},
    {"id": "project-acceptance", "type": "skill", "required": True},
    {"id": "superpowers:verification-before-completion", "type": "plugin-skill", "required": False},
    {"id": "karpathy-understanding-first", "type": "skill", "required": False},
    {"id": "karpathy-minimalism", "type": "skill", "required": False},
    {"id": "karpathy-agentic-engineering", "type": "skill", "required": False},
    {"id": "karpathy-supply-chain-hygiene", "type": "skill", "required": False},
    {"id": "karpathy-vibe-to-agentic", "type": "skill", "required": False},
    {"id": "nuwa-skill", "type": "external-skill", "required": False, "permission_required": True},
    {"id": "darwin-skill", "type": "external-skill", "required": False, "permission_required": True},
]


def skill_roots() -> list[Path]:
    home = Path.home()
    codex_home = Path(os.environ.get("CODEX_HOME", home / ".codex"))
    roots = [
        home / ".agents" / "skills",
        codex_home / "skills",
        codex_home / "plugins" / "cache",
    ]
    return [root for root in roots if root.exists()]


def find_skill(dep_id: str, roots: list[Path]) -> list[str]:
    matches: list[str] = []
    simple_name = dep_id.split(":", 1)[-1]
    for root in roots:
        direct = root / simple_name / "SKILL.md"
        if direct.exists():
            matches.append(str(direct))
        for skill_file in root.rglob("SKILL.md"):
            if simple_name == skill_file.parent.name:
                matches.append(str(skill_file))
    return sorted(set(matches))


def audit() -> dict[str, object]:
    roots = skill_roots()
    results = []
    for dep in DEPENDENCIES:
        matches = find_skill(dep["id"], roots) if dep["type"] in {"skill", "plugin-skill"} else []
        installed = bool(matches)
        results.append(
            {
                "id": dep["id"],
                "type": dep["type"],
                "required": dep.get("required", False),
                "installed": installed,
                "locations": matches,
                "permission_required": dep.get("permission_required", False) or (not installed and dep["type"].startswith("external")),
                "ask_immediately_when_needed": bool(dep.get("permission_required", False) or (not installed and dep["type"].startswith("external"))),
            }
        )
    return {"skill_roots_checked": [str(root) for root in roots], "dependencies": results}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    args = parser.parse_args()
    payload = audit()
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        for item in payload["dependencies"]:
            status = "installed" if item["installed"] else "missing"
            permission = " permission-required" if item["permission_required"] else ""
            print(f"{item['id']}: {status}{permission}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
