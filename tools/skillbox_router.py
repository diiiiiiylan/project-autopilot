#!/usr/bin/env python3
"""Deterministic routing helpers for the project-autopilot skillbox."""

from __future__ import annotations

from dataclasses import dataclass


SKILLS = {
    "leader": "project-autopilot",
    "intake": "project-intake",
    "staffing": "project-staffing",
    "domain": "project-domain-router",
    "expert": "project-expert-selection",
    "context": "project-context-continuity",
    "gpt": "project-gpt-consultation",
    "nuwa": "project-nuwa-distillation",
    "darwin": "project-darwin-evolution",
    "superpowers": "project-superpowers-routing",
    "karpathy": "project-karpathy-methods",
    "mcp": "project-mcp-orchestrator",
    "acceptance": "project-acceptance",
    "governance": "project-skillbox-governance",
}


@dataclass(frozen=True)
class RouteResult:
    prompt: str
    complexity: str
    skills: list[str]
    requires_permission: list[str]
    permission_timing: str
    pause_for_permission: bool


def classify_complexity(prompt: str) -> str:
    text = prompt.lower()
    small = ("typo", "spelling", "readme spelling", "explain", "解释", "拼写")
    enterprise = ("长期", "enterprise", "multi-quarter", "organization-wide")
    large = (
        "architecture",
        "migration",
        "security",
        "release",
        "public api",
        "new dependency",
        "data structure",
        "large",
        "大型",
        "架构",
        "迁移",
        "发布",
        "安全",
    )
    medium = ("cross-module", "multiple files", "refactor", "integration", "计划模式", "跨模块", "优化", "修改")
    if any(marker in text for marker in enterprise):
        return "enterprise"
    if any(marker in text for marker in large):
        return "large"
    if any(marker in text for marker in medium):
        return "medium"
    if any(marker in text for marker in small):
        return "small"
    if any(marker in text for marker in ("start a", "开始做", "新项目", "saas", "project")):
        return "medium"
    return "small"


def permission_required(action: str) -> bool:
    text = action.lower()
    markers = (
        "download",
        "install",
        "enable_mcp",
        "install_mcp",
        "create_mcp",
        "web_gpt",
        "logged_in_account",
        "paid",
        "publish",
        "production",
        "nuwa",
        "darwin",
        "应用",
        "下载",
        "安装",
        "创建 mcp",
    )
    return any(marker in text for marker in markers)


def build_permission_request(action: str, target: str, capability: str, skipped_consequence: str) -> dict[str, object]:
    """Build the request that must be shown before an external action starts."""
    return {
        "action": action,
        "target": target,
        "capability_gained": capability,
        "capability_lost_if_skipped": skipped_consequence,
        "ask_timing": "immediately_when_dependency_gap_is_found",
        "must_pause_before_action": True,
        "requires_explicit_user_approval": True,
        "must_not_report_as_completed_if_skipped": True,
    }


def route_prompt(prompt: str) -> RouteResult:
    text = prompt.lower()
    complexity = classify_complexity(prompt)
    skills = [SKILLS["leader"]]
    requires_permission: list[str] = []

    if complexity != "small" or any(marker in text for marker in ("计划模式", "start", "开始", "project", "项目", "saas")):
        skills.extend([SKILLS["intake"], SKILLS["staffing"], SKILLS["domain"]])

    if complexity != "small" or any(
        marker in text for marker in ("openspec", "context", "compact", "resume", "handoff", "上下文", "压缩", "恢复")
    ):
        skills.append(SKILLS["context"])

    if complexity in {"medium", "large", "enterprise"} or any(
        marker in text for marker in ("plan", "proposal", "architecture", "方案", "聊透", "gpt", "chatgpt")
    ):
        skills.append(SKILLS["gpt"])

    if complexity in {"medium", "large", "enterprise"}:
        skills.append(SKILLS["superpowers"])

    if any(marker in text for marker in ("bug", "debug", "failure", "失败", "报错", "修复")):
        if SKILLS["superpowers"] not in skills:
            skills.append(SKILLS["superpowers"])

    if any(marker in text for marker in ("prototype", "polish", "vibe", "minimal", "understand", "供应链", "原型")):
        skills.append(SKILLS["karpathy"])

    if any(marker in text for marker in ("expert", "专家", "名人", "领域", "karpathy", "nuwa", "女娲")):
        skills.append(SKILLS["expert"])
        if any(marker in text for marker in ("missing", "缺少", "没有", "nuwa", "女娲")):
            skills.append(SKILLS["nuwa"])
            requires_permission.append("download_or_run_nuwa")

    if any(marker in text for marker in ("darwin", "evolve", "优化 skill", "进化", "达尔文")):
        skills.append(SKILLS["darwin"])
        requires_permission.append("download_or_run_darwin")

    if any(marker in text for marker in ("mcp", "connector", "app", "应用", "程序", "网页 gpt")):
        skills.append(SKILLS["mcp"])
        for action in ("install_mcp", "install_app", "create_mcp", "web_gpt"):
            if permission_required(action):
                requires_permission.append(action)

    if any(marker in text for marker in ("gpt", "web gpt", "chatgpt", "网页 gpt")):
        requires_permission.append("call_external_gpt")

    if complexity != "small" or any(marker in text for marker in ("finish", "acceptance", "验收", "发布", "push")):
        skills.append(SKILLS["acceptance"])

    if any(marker in text for marker in ("skillbox", "技能宝箱", "dependency", "依赖", "重复", "冲突")):
        skills.append(SKILLS["governance"])

    deduped = list(dict.fromkeys(skills))
    deduped_permissions = list(dict.fromkeys(requires_permission))
    return RouteResult(
        prompt=prompt,
        complexity=complexity,
        skills=deduped,
        requires_permission=deduped_permissions,
        permission_timing="immediately_when_dependency_gap_is_found" if deduped_permissions else "not_required",
        pause_for_permission=bool(deduped_permissions),
    )


def main() -> int:
    import argparse
    import json

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prompt")
    args = parser.parse_args()
    result = route_prompt(args.prompt)
    print(json.dumps(result.__dict__, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
