#!/usr/bin/env python3
"""Install project-autopilot Skill and custom agents into user-level Codex paths."""

from __future__ import annotations

import os
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_SRC = ROOT / "skill"
AGENTS_SRC = ROOT / "custom-agents"


def copy_tree(src: Path, dst: Path) -> None:
    dst.mkdir(parents=True, exist_ok=True)
    for item in src.iterdir():
        target = dst / item.name
        if item.is_dir():
            copy_tree(item, target)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, target)


def main() -> int:
    home = Path.home()
    codex_home = Path(os.environ.get("CODEX_HOME", home / ".codex"))
    skill_dst = home / ".agents" / "skills" / "project-autopilot"
    agents_dst = codex_home / "agents"
    copy_tree(SKILL_SRC, skill_dst)
    agents_dst.mkdir(parents=True, exist_ok=True)
    for agent in AGENTS_SRC.glob("*.toml"):
        shutil.copy2(agent, agents_dst / agent.name)
    print(f"Installed Skill to {skill_dst}")
    print(f"Installed agents to {agents_dst}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
