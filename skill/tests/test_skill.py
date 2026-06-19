from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
REPO_AGENT_DIR = ROOT.parent / "custom-agents"
AGENT_DIR = REPO_AGENT_DIR if REPO_AGENT_DIR.exists() else Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")) / "agents"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


task_registry = load_module("task_registry", SCRIPTS / "task_registry.py")
initialize_project = load_module("initialize_project", SCRIPTS / "initialize_project.py")
acceptance_report = load_module("acceptance_report", SCRIPTS / "acceptance_report.py")
validate_skill = load_module("validate_skill", SCRIPTS / "validate_skill.py")


class ProjectAutopilotSkillTests(unittest.TestCase):
    def test_metadata_and_structure_are_valid(self):
        errors = validate_skill.validate_skill(ROOT, AGENT_DIR)
        self.assertEqual(errors, [])

    def test_agent_configs_parse_and_have_required_fields(self):
        for name in validate_skill.AGENT_FILES:
            data = validate_skill.parse_toml(AGENT_DIR / name)
            self.assertEqual(data["name"], name.removesuffix(".toml"))
            self.assertTrue(data["description"])
            self.assertTrue(data["developer_instructions"])
        people = validate_skill.parse_toml(AGENT_DIR / "people-operations-department.toml")
        self.assertIn("人事协调部门", people["description"])

    def test_small_task_does_not_trigger_complex_flow(self):
        self.assertEqual(validate_skill.classify_task("Fix a spelling typo in one file"), "small")
        self.assertEqual(validate_skill.classify_task("Explain this code only"), "small")
        with tempfile.TemporaryDirectory() as tmp:
            result = initialize_project.initialize_project(Path(tmp), "Fix README spelling", force_fallback=True, complexity="small")
            self.assertEqual(result["mode"], "direct")
            self.assertEqual(result["active_departments"], [])
            self.assertFalse((Path(tmp) / ".project-autopilot").exists())

    def test_cross_module_task_triggers(self):
        self.assertEqual(validate_skill.classify_task("Implement a cross-module integration"), "medium")
        self.assertEqual(validate_skill.classify_task("Add a data structure migration"), "large")
        self.assertTrue(validate_skill.needs_project_intake("我要开始做一个 SaaS 项目"))
        self.assertTrue(validate_skill.needs_project_intake("计划模式下优化一个跨模块功能"))

    def test_duplicate_task_cannot_be_claimed_twice(self):
        with tempfile.TemporaryDirectory() as tmp:
            registry = Path(tmp) / "task-registry.json"
            first = task_registry.claim_task(registry, "Add billing API", scope="api", owner="a")
            second = task_registry.claim_task(registry, "Add billing API", scope="api", owner="b")
            self.assertTrue(first["claimed"])
            self.assertFalse(second["claimed"])
            self.assertEqual(second["reason"], "already_active")

    def test_initialize_project_is_idempotent_and_fallback_without_openspec(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            old_path = os.environ.get("PATH", "")
            os.environ["PATH"] = ""
            try:
                first = initialize_project.initialize_project(project, "Demo Change", force_fallback=True)
                second = initialize_project.initialize_project(project, "Demo Change", force_fallback=True)
            finally:
                os.environ["PATH"] = old_path
            self.assertEqual(first["mode"], "fallback")
            self.assertEqual(second["mode"], "fallback")
            change_dir = project / ".project-autopilot" / "changes" / "demo-change"
            self.assertTrue((change_dir / "proposal.md").exists())
            self.assertTrue((change_dir / "task-registry.json").exists())
            self.assertTrue((change_dir / "project-brief.md").exists())
            self.assertTrue((change_dir / "staffing-plan.md").exists())
            state = json.loads((change_dir / "coordination-state.json").read_text(encoding="utf-8"))
            self.assertEqual(state["lead_thread_role"], "initial-main-thread")
            self.assertLessEqual(state["max_concurrency"], 4)
            self.assertEqual(len({item["scope_key"] for item in state["active_departments"]}), len(state["active_departments"]))
            self.assertNotIn("people-operations-department", {item["name"] for item in state["active_departments"]})

    def test_large_staffing_has_bounded_non_overlapping_departments(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = initialize_project.initialize_project(Path(tmp), "Large Platform Change", force_fallback=True, complexity="large")
            self.assertEqual(result["project_size"], "large")
            self.assertLessEqual(result["max_concurrency"], 4)
            scopes = [item["scope_key"] for item in result["active_departments"]]
            self.assertEqual(len(scopes), len(set(scopes)))
            self.assertIn("people-operations-department", {item["name"] for item in result["inactive_departments"]})

    def test_acceptance_failure_is_not_done(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = acceptance_report.generate_report(
                Path(tmp),
                "demo",
                "fallback",
                checks=["pass: unit tests", "fail: lint"],
                blocked=[],
                risks=[],
            )
            text = output.read_text(encoding="utf-8")
            self.assertIn("Status: failed", text)
            self.assertNotIn("Status: done", text)

    def test_templates_scripts_and_references_have_no_broken_paths(self):
        errors = validate_skill.validate_references(ROOT)
        self.assertEqual(errors, [])

    def test_no_real_secrets_or_hardcoded_project_paths(self):
        errors = validate_skill.validate_no_sensitive_data(ROOT)
        self.assertEqual(errors, [])

    def test_validation_script_cli_passes(self):
        completed = subprocess.run(
            [sys.executable, str(SCRIPTS / "validate_skill.py"), str(ROOT), "--agent-dir", str(AGENT_DIR)],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)


if __name__ == "__main__":
    unittest.main()
