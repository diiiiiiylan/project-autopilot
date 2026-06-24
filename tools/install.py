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

- 非简单项目任务自动调用 `$project-autopilot` 技能宝箱入口，由项目组长接管，不要求用户手动选择部门。
- 项目组长必须自动判断任务体量、风险、剩余上下文和并行价值，再动态编制/裁撤部门。
- OpenSpec 是非简单项目的需求、决策、任务和验收事实来源；没有 OpenSpec 时使用项目内 `.project-autopilot/changes/<change-id>/` fallback。
- 长线程、上下文不足、压缩、恢复、跨阶段或多 Agent 协作前后，必须先同步并读取 durable state，避免凭压缩摘要幻想继续。
- 默认自主推进，减少不必要提问和重复复述；只在凭据、付费、生产、不可逆、公开发布、重要删除或产品方向分歧时停下问。
- 未通过验证不得宣布完成。
- 子智能体只用于真正可并行且边界清晰的任务；最大深度 1，不能让用户手动当调度器。
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
