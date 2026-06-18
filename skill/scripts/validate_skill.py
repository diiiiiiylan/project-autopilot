#!/usr/bin/env python3
"""Validate the project-autopilot Skill installation."""

from __future__ import annotations

import argparse
import ast
import os
import re
import sys
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    tomllib = None


REQUIRED_FILES = [
    "SKILL.md",
    "README.md",
    "CHANGELOG.md",
    "agents/openai.yaml",
    "references/project-governance.md",
    "references/openspec-workflow.md",
    "references/department-contracts.md",
    "references/acceptance-gates.md",
    "references/skill-extraction.md",
    "assets/templates/proposal.md",
    "assets/templates/design.md",
    "assets/templates/tasks.md",
    "assets/templates/department-brief.md",
    "assets/templates/handoff.md",
    "assets/templates/acceptance-report.md",
    "scripts/initialize_project.py",
    "scripts/task_registry.py",
    "scripts/detect_duplicate_tasks.py",
    "scripts/acceptance_report.py",
    "scripts/validate_skill.py",
    "tests/trigger_cases.json",
    "tests/test_skill.py",
]

AGENT_FILES = [
    "requirements-architecture-department.toml",
    "development-department.toml",
    "quality-assurance-department.toml",
    "independent-review-department.toml",
]

SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"ghp_[A-Za-z0-9_]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"(?i)(api_key|secret|token)\s*[:=]\s*['\"][^'\"]{12,}['\"]"),
]

HARDCODED_PATH_PATTERNS = [
    re.compile("[A-Za-z]" + chr(58) + r"\\"),
    re.compile("/" + "Users" + r"/[^/\s]+"),
    re.compile("/" + "home" + r"/[^/\s]+"),
]


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must start with YAML front matter")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError("SKILL.md front matter must close with ---")
    data: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            raise ValueError(f"Invalid front matter line: {line}")
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"')
    return data


def parse_toml(path: Path) -> dict[str, object]:
    if tomllib is None:
        text = path.read_text(encoding="utf-8")
        result: dict[str, object] = {}
        for line in text.splitlines():
            if "=" in line and not line.strip().startswith("#"):
                key, value = line.split("=", 1)
                result[key.strip()] = value.strip().strip('"')
        return result
    with path.open("rb") as handle:
        return tomllib.load(handle)


def classify_task(text: str) -> str:
    lowered = text.lower()
    small_markers = ["typo", "spelling", "explain", "single-file", "one file", "copy fix"]
    large_markers = [
        "migration",
        "public api",
        "data structure",
        "new dependency",
        "security",
        "release",
        "architecture",
        "multiple modules",
    ]
    medium_markers = ["cross-module", "multiple files", "integration", "refactor"]
    if any(marker in lowered for marker in large_markers):
        return "large"
    if any(marker in lowered for marker in medium_markers):
        return "medium"
    if any(marker in lowered for marker in small_markers):
        return "small"
    return "small"


def validate_references(root: Path) -> list[str]:
    errors: list[str] = []
    for rel in REQUIRED_FILES:
        if not (root / rel).exists():
            errors.append(f"Missing required file: {rel}")
    skill_text = (root / "SKILL.md").read_text(encoding="utf-8")
    for match in re.findall(r"`([^`]+?\.(?:md|py|yaml|json|toml))`", skill_text):
        candidate = root / match
        if match.startswith("requirements-") or match.startswith("development-") or match.startswith("quality-") or match.startswith("independent-"):
            continue
        if not candidate.exists():
            errors.append(f"Broken referenced path in SKILL.md: {match}")
    return errors


def validate_no_sensitive_data(root: Path) -> list[str]:
    errors: list[str] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if "__pycache__" in path.parts or path.suffix in {".pyc", ".pyo"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                errors.append(f"Potential secret pattern in {path.relative_to(root)}")
        for pattern in HARDCODED_PATH_PATTERNS:
            if pattern.search(text):
                errors.append(f"Hardcoded local path in {path.relative_to(root)}")
    return errors


def validate_python_scripts(root: Path) -> list[str]:
    errors: list[str] = []
    for path in (root / "scripts").glob("*.py"):
        try:
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except SyntaxError as exc:
            errors.append(f"Python syntax error in {path.name}: {exc}")
    return errors


def validate_agents(agent_dir: Path) -> list[str]:
    errors: list[str] = []
    for name in AGENT_FILES:
        path = agent_dir / name
        if not path.exists():
            errors.append(f"Missing global agent: {name}")
            continue
        try:
            data = parse_toml(path)
        except Exception as exc:  # noqa: BLE001
            errors.append(f"Invalid TOML {name}: {exc}")
            continue
        for field in ("name", "description", "developer_instructions"):
            if not str(data.get(field, "")).strip():
                errors.append(f"{name} missing {field}")
    return errors


def validate_skill(root: Path, agent_dir: Path | None = None) -> list[str]:
    root = root.resolve()
    agent_dir = agent_dir or Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")) / "agents"
    errors: list[str] = []
    errors.extend(validate_references(root))
    if (root / "SKILL.md").exists():
        frontmatter = parse_frontmatter((root / "SKILL.md").read_text(encoding="utf-8"))
        if frontmatter.get("name") != "project-autopilot":
            errors.append("SKILL.md name must be project-autopilot")
        description = frontmatter.get("description", "")
        for term in ("cross-module", "migrations", "Do not use"):
            if term not in description:
                errors.append(f"SKILL.md description missing trigger term: {term}")
    errors.extend(validate_python_scripts(root))
    errors.extend(validate_agents(agent_dir))
    errors.extend(validate_no_sensitive_data(root))
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--agent-dir", type=Path)
    args = parser.parse_args(argv)
    errors = validate_skill(args.root, args.agent_dir)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("project-autopilot validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
