#!/usr/bin/env python3
"""Install the project-autopilot skillbox and custom agents into user-level Codex paths."""

from __future__ import annotations

import os
import shutil
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS_SRC = ROOT / "skills"
AGENTS_SRC = ROOT / "custom-agents"
EXTERNAL_SKILLS_SRC = ROOT / "external" / "skills"
GLOBAL_BLOCK_START = "<!-- BEGIN PROJECT-AUTOPILOT MANAGED BLOCK -->"
GLOBAL_BLOCK_END = "<!-- END PROJECT-AUTOPILOT MANAGED BLOCK -->"


GLOBAL_BLOCK = f"""{GLOBAL_BLOCK_START}
## Project Autopilot Skillbox Global Rules

- 非简单项目任务优先调用 `$project-autopilot` 技能宝箱入口。
- 默认自主推进，减少不必要提问和重复复述。
- 未通过验证不得宣布完成。
- 子智能体只用于真正可并行且边界清晰的任务。
- 未经用户明确允许，不下载、安装、启用或创建外部 Skill、应用、MCP，也不调用需要登录态的外部账号工具。
- 最终回复只报告完成结果、主要变更、验收证据和剩余风险。
{GLOBAL_BLOCK_END}
"""


def backup_file(path: Path, backup_root: Path) -> None:
    if not path.exists() or not path.is_file():
        return
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    safe_name = "__".join(path.parts[-6:])
    backup_path = backup_root / f"{safe_name}.{stamp}.bak"
    backup_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, backup_path)


def copy_file_with_backup(src: Path, dst: Path, backup_root: Path) -> None:
    if dst.exists() and src.read_bytes() != dst.read_bytes():
        backup_file(dst, backup_root)
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def skill_name(skill_dir: Path) -> str:
    text = (skill_dir / "SKILL.md").read_text(encoding="utf-8", errors="ignore")
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            for line in text[3:end].splitlines():
                if line.startswith("name:"):
                    return line.split(":", 1)[1].strip().strip('"')
    return skill_dir.name


def copy_tree(src: Path, dst: Path, backup_root: Path) -> None:
    dst.mkdir(parents=True, exist_ok=True)
    for item in src.iterdir():
        target = dst / item.name
        if item.is_dir():
            copy_tree(item, target, backup_root)
        else:
            copy_file_with_backup(item, target, backup_root)


def upsert_global_block(path: Path, backup_root: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    if GLOBAL_BLOCK_START in existing and GLOBAL_BLOCK_END in existing:
        before, rest = existing.split(GLOBAL_BLOCK_START, 1)
        _, after = rest.split(GLOBAL_BLOCK_END, 1)
        text = before.rstrip() + "\n\n" + GLOBAL_BLOCK + after.lstrip()
    else:
        text = existing.rstrip() + ("\n\n" if existing.strip() else "") + GLOBAL_BLOCK
    if text != existing:
        backup_file(path, backup_root)
        path.write_text(text, encoding="utf-8")


def main() -> int:
    home = Path.home()
    codex_home = Path(os.environ.get("CODEX_HOME", home / ".codex"))
    skills_dst = home / ".agents" / "skills"
    agents_dst = codex_home / "agents"
    backup_root = codex_home / "backups" / "project-autopilot"
    for skill_dir in sorted(SKILLS_SRC.iterdir()):
        if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
            copy_tree(skill_dir, skills_dst / skill_dir.name, backup_root)
    if EXTERNAL_SKILLS_SRC.exists():
        for skill_dir in sorted(EXTERNAL_SKILLS_SRC.iterdir()):
            if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
                copy_tree(skill_dir, skills_dst / skill_name(skill_dir), backup_root)
    agents_dst.mkdir(parents=True, exist_ok=True)
    for agent in AGENTS_SRC.glob("*.toml"):
        copy_file_with_backup(agent, agents_dst / agent.name, backup_root)
    upsert_global_block(codex_home / "AGENTS.md", backup_root)
    print(f"Installed Skills to {skills_dst}")
    print(f"Installed agents to {agents_dst}")
    print(f"Updated global rules in {codex_home / 'AGENTS.md'}")
    print(f"Backups, when needed, are in {backup_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
