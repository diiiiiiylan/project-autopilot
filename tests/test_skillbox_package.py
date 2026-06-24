from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


validate_package = load_module("validate_package", ROOT / "tools" / "validate_package.py")
skillbox_router = load_module("skillbox_router", ROOT / "tools" / "skillbox_router.py")
mcp_discovery = load_module("mcp_discovery", ROOT / "tools" / "mcp_discovery.py")


class SkillboxPackageTests(unittest.TestCase):
    def test_package_validation_passes(self):
        self.assertEqual(validate_package.validate_package(ROOT), [])

    def test_every_skill_has_frontmatter_and_openai_yaml(self):
        for skill_dir in sorted((ROOT / "skills").iterdir()):
            if not skill_dir.is_dir():
                continue
            meta = validate_package.parse_frontmatter((skill_dir / "SKILL.md").read_text(encoding="utf-8"))
            self.assertEqual(meta["name"], skill_dir.name)
            self.assertTrue(meta["description"])
            data = validate_package.parse_openai_yaml(skill_dir / "agents" / "openai.yaml")
            self.assertTrue(data["name"])
            self.assertTrue(data["description"])
            self.assertTrue(data["default_prompt"])

    def test_skills_are_isolated_not_one_monolith(self):
        sizes = {path.parent.name: path.stat().st_size for path in (ROOT / "skills").glob("*/SKILL.md")}
        self.assertGreaterEqual(len(sizes), 12)
        self.assertLess(max(sizes.values()), 8000)
        leader = (ROOT / "skills" / "project-autopilot" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("$project-intake", leader)
        self.assertIn("$project-acceptance", leader)
        self.assertLess(leader.count("# Project"), 2)

    def test_custom_agents_parse_and_have_required_fields(self):
        for name in validate_package.REQUIRED_AGENTS:
            data = validate_package.parse_toml(ROOT / "custom-agents" / name)
            self.assertTrue(data["name"])
            self.assertTrue(data["description"])
            self.assertTrue(data["developer_instructions"])

    def test_new_project_triggers_intake_staffing_and_domain_router(self):
        route = skillbox_router.route_prompt("start a SaaS project")
        self.assertIn("project-intake", route.skills)
        self.assertIn("project-staffing", route.skills)
        self.assertIn("project-domain-router", route.skills)
        self.assertIn("project-context-continuity", route.skills)
        self.assertIn("project-gpt-consultation", route.skills)

    def test_context_continuity_triggers_for_openspec_and_compaction(self):
        route = skillbox_router.route_prompt("Use OpenSpec and protect context before compaction and resume")
        self.assertIn("project-context-continuity", route.skills)
        self.assertIn("project-autopilot", route.skills)

    def test_plan_finalization_triggers_gpt_consultation(self):
        route = skillbox_router.route_prompt("before final proposal, use GPT consultation to discuss the plan thoroughly")
        self.assertIn("project-gpt-consultation", route.skills)
        self.assertIn("call_external_gpt", route.requires_permission)
        self.assertTrue(route.pause_for_permission)

    def test_bugfix_triggers_superpowers_debugging_route(self):
        route = skillbox_router.route_prompt("Fix a cross-module bug with failing tests")
        self.assertIn("project-superpowers-routing", route.skills)
        self.assertIn(route.complexity, {"medium", "large"})

    def test_prototype_polish_triggers_karpathy_methods(self):
        route = skillbox_router.route_prompt("prototype polish this vibe into an agentic implementation")
        self.assertIn("project-karpathy-methods", route.skills)

    def test_expert_missing_triggers_immediate_nuwa_permission_not_download(self):
        route = skillbox_router.route_prompt("missing domain expert, use Nuwa to distill an expert Skill")
        self.assertIn("project-expert-selection", route.skills)
        self.assertIn("project-nuwa-distillation", route.skills)
        self.assertIn("download_or_run_nuwa", route.requires_permission)
        self.assertTrue(route.pause_for_permission)
        self.assertEqual(route.permission_timing, "immediately_when_dependency_gap_is_found")

    def test_skill_evolution_triggers_immediate_darwin_permission_not_run(self):
        route = skillbox_router.route_prompt("optimize Skill and let Darwin evolve it")
        self.assertIn("project-darwin-evolution", route.skills)
        self.assertIn("download_or_run_darwin", route.requires_permission)
        self.assertTrue(route.pause_for_permission)
        self.assertEqual(route.permission_timing, "immediately_when_dependency_gap_is_found")

    def test_mcp_discovery_is_read_only_and_prioritizes_official_sources(self):
        result = mcp_discovery.discover("github mcp")
        self.assertFalse(result["install_permitted"])
        self.assertFalse(result["create_permitted"])
        self.assertTrue(result["permission_required_before_install_or_create"])
        self.assertTrue(result["must_pause_before_install_or_create"])
        self.assertEqual(result["ask_timing"], "immediately_when_mcp_or_app_gap_is_found")
        self.assertEqual(result["candidates"][0]["id"], "official-mcp-registry")

    def test_missing_mcp_generates_custom_plan_but_does_not_create(self):
        result = mcp_discovery.discover("no mcp for unknown tool")
        self.assertTrue(result["custom_mcp_plan_required"])
        self.assertFalse(result["create_permitted"])

    def test_permission_required_for_external_actions(self):
        for action in ("download_nuwa", "download_darwin", "install_app", "install_mcp", "create_mcp", "web_gpt"):
            self.assertTrue(skillbox_router.permission_required(action))

    def test_permission_request_is_immediate_and_not_completion_report(self):
        request = skillbox_router.build_permission_request(
            action="download",
            target="nuwa-skill",
            capability="distill a missing expert method into a candidate Skill",
            skipped_consequence="use a weaker local fallback without expert distillation",
        )
        self.assertEqual(request["ask_timing"], "immediately_when_dependency_gap_is_found")
        self.assertTrue(request["must_pause_before_action"])
        self.assertTrue(request["requires_explicit_user_approval"])
        self.assertTrue(request["must_not_report_as_completed_if_skipped"])

    def test_registries_are_parseable(self):
        for rel in validate_package.REGISTRY_FILES:
            payload = json.loads((ROOT / rel).read_text(encoding="utf-8"))
            self.assertTrue(payload["sources"])

    def test_external_nuwa_and_darwin_sources_are_present(self):
        self.assertTrue((ROOT / "external" / "skills" / "nuwa-skill" / "SKILL.md").exists())
        self.assertTrue((ROOT / "external" / "skills" / "darwin-skill" / "SKILL.md").exists())
        self.assertTrue((ROOT / "external" / "skills" / "SOURCES.md").exists())


if __name__ == "__main__":
    unittest.main()
