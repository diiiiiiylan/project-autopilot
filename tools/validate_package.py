#!/usr/bin/env python3
"""Validate the project-autopilot multi-Skill package."""

from __future__ import annotations

import argparse
import ast
import json
import os
import re
import sys
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    tomllib = None


REQUIRED_SKILLS = [
    "project-autopilot",
    "project-intake",
    "project-staffing",
    "project-domain-router",
    "project-expert-selection",
    "project-nuwa-distillation",
    "project-darwin-evolution",
    "project-superpowers-routing",
    "project-karpathy-methods",
    "project-mcp-orchestrator",
    "project-acceptance",
    "project-skillbox-governance",
]

REQUIRED_AGENTS = [
    "requirements-architecture-department.toml",
    "development-department.toml",
    "quality-assurance-department.toml",
    "independent-review-department.toml",
    "people-operations-department.toml",
    "methodology-coordination-department.toml",
    "domain-expert-department.toml",
    "mcp-connection-department.toml",
    "security-supply-chain-department.toml",
]

REGISTRY_FILES = [
    "references/registries/skill-sources.json",
    "references/registries/mcp-sources.json",
]

SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
]

ABSOLUTE_PATH_PATTERNS = [
    re.compile(r"[A-Za-z]:\\(?:Users|codex|projects)\\"),
    re.compile(r"/(?:Users|home)/[A-Za-z0-9._-]+"),
]


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        raise ValueError("missing YAML front matter")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError("unclosed YAML front matter")
    result: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            raise ValueError(f"bad front matter line: {line}")
        key, value = line.split(":", 1)
        result[key.strip()] = value.strip().strip('"')
    return result


def parse_openai_yaml(path: Path) -> dict[str, str]:
    data: dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip() or raw.lstrip().startswith("#") or raw.startswith("  ") or raw.strip().startswith("- "):
            continue
        if ":" in raw:
            key, value = raw.split(":", 1)
            data[key.strip()] = value.strip().strip('"')
    return data


def parse_toml(path: Path) -> dict[str, object]:
    if tomllib is not None:
        with path.open("rb") as handle:
            return tomllib.load(handle)
    data: dict[str, object] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        if "=" in raw and not raw.lstrip().startswith("#"):
            key, value = raw.split("=", 1)
            data[key.strip()] = value.strip().strip('"')
    return data


def validate_skills(root: Path) -> list[str]:
    errors: list[str] = []
    skills_dir = root / "skills"
    for name in REQUIRED_SKILLS:
        skill_dir = skills_dir / name
        skill_file = skill_dir / "SKILL.md"
        openai_file = skill_dir / "agents" / "openai.yaml"
        if not skill_file.exists():
            errors.append(f"missing Skill: {name}")
            continue
        try:
            meta = parse_frontmatter(skill_file.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{name}/SKILL.md invalid front matter: {exc}")
            continue
        if meta.get("name") != name:
            errors.append(f"{name}/SKILL.md name mismatch")
        if not meta.get("description"):
            errors.append(f"{name}/SKILL.md missing description")
        if skill_file.stat().st_size > 8000:
            errors.append(f"{name}/SKILL.md is too large for an isolated Skill")
        if not openai_file.exists():
            errors.append(f"{name}/agents/openai.yaml missing")
        else:
            data = parse_openai_yaml(openai_file)
            for field in ("name", "description", "default_prompt"):
                if not data.get(field):
                    errors.append(f"{name}/agents/openai.yaml missing {field}")
    return errors


def validate_agents(root: Path) -> list[str]:
    errors: list[str] = []
    agent_dir = root / "custom-agents"
    for name in REQUIRED_AGENTS:
        path = agent_dir / name
        if not path.exists():
            errors.append(f"missing custom agent: {name}")
            continue
        try:
            data = parse_toml(path)
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{name} invalid TOML: {exc}")
            continue
        for field in ("name", "description", "developer_instructions"):
            if not str(data.get(field, "")).strip():
                errors.append(f"{name} missing {field}")
    return errors


def validate_registries(root: Path) -> list[str]:
    errors: list[str] = []
    for rel in REGISTRY_FILES:
        path = root / rel
        if not path.exists():
            errors.append(f"missing registry: {rel}")
            continue
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{rel} invalid JSON: {exc}")
            continue
        if not isinstance(payload.get("sources"), list) or not payload["sources"]:
            errors.append(f"{rel} must contain non-empty sources list")
    return errors


def validate_tools(root: Path) -> list[str]:
    errors: list[str] = []
    for rel in (
        "tools/install.py",
        "tools/validate_package.py",
        "tools/dependency_audit.py",
        "tools/mcp_discovery.py",
        "tools/skillbox_router.py",
    ):
        path = root / rel
        if not path.exists():
            errors.append(f"missing tool: {rel}")
            continue
        try:
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except SyntaxError as exc:
            errors.append(f"{rel} syntax error: {exc}")
    if not (root / "tools" / "permission_request_template.md").exists():
        errors.append("missing permission request template")
    return errors


def validate_sensitive_data(root: Path) -> list[str]:
    errors: list[str] = []
    skip_parts = {".git", "node_modules", "__pycache__", ".cache", "dist", "out"}
    skip_suffixes = {".pyc", ".pyo", ".mp4", ".png", ".jpg", ".jpeg", ".gif"}
    for path in root.rglob("*"):
        if not path.is_file() or any(part in skip_parts for part in path.parts) or path.suffix.lower() in skip_suffixes:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                errors.append(f"potential secret in {path.relative_to(root)}")
        for pattern in ABSOLUTE_PATH_PATTERNS:
            if pattern.search(text):
                errors.append(f"hardcoded local path in {path.relative_to(root)}")
    return errors


def validate_package(root: Path) -> list[str]:
    root = root.resolve()
    errors: list[str] = []
    errors.extend(validate_skills(root))
    errors.extend(validate_agents(root))
    errors.extend(validate_registries(root))
    errors.extend(validate_tools(root))
    errors.extend(validate_sensitive_data(root))
    if not (root / "skill" / "SKILL.md").exists():
        errors.append("legacy compatibility skill/SKILL.md missing")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path.cwd())
    args = parser.parse_args(argv)
    errors = validate_package(args.root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("project-autopilot package validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
