---
name: project-autopilot
description: Low-interaction project controller for non-trivial Codex work. Use for cross-module features, larger modifications, new projects, public API or data-structure changes, new dependencies, migrations, complex defects, OpenSpec-driven work, multi-step planning/collaboration, automatic test repair, or tasks needing complete acceptance evidence. Do not use for explanation-only questions, clearly scoped single-file edits, spelling/copy fixes, simple commands, or explicitly low-risk operations that do not affect interfaces, data, dependencies, or multiple modules.
---

# Project Autopilot

Use this skill to run non-trivial project work with low interaction, bounded autonomy, optional department agents, OpenSpec as the source of truth, task de-duplication, automatic verification repair, and a final acceptance report.

## Load Only What Is Needed

- Read `references/project-governance.md` before starting any medium or large task.
- Read `references/openspec-workflow.md` when a task needs a specification, change lifecycle, or fallback templates.
- Read `references/department-contracts.md` before creating subagents or simulating department roles.
- Read `references/acceptance-gates.md` before declaring work complete.
- Read `references/skill-extraction.md` only when a repeated workflow might become a new Skill.

## Choose Execution Mode

Classify the task before acting:

- Small: scope is clear, low-risk, and does not change public interfaces, data structures, dependencies, migrations, security boundaries, or multiple modules. Complete directly in the main thread. Do not create OpenSpec changes or subagents.
- Medium: touches multiple files or one cross-module behavior, but has limited architecture and release risk. Create a lightweight spec and task list. Use at most two truly parallel department tasks.
- Large: affects multiple modules, architecture, public contracts, data migration, new dependencies, security, release, or long-running collaboration. Use the full OpenSpec lifecycle and department agents as needed.

Do not create departments for ceremony. Do not assign overlapping scopes. Do not parallelize tasks with ordering dependencies.

## Default Workflow

1. Inspect the project state, existing instructions, build/test commands, and whether OpenSpec is initialized.
2. State only critical assumptions. Ask only when missing information changes product direction, requires credentials, performs irreversible or production actions, spends money, publishes publicly, or deletes important data.
3. For medium or large tasks, establish the change source of truth:
   - Prefer native OpenSpec commands, templates, and directories when available.
   - If OpenSpec is unavailable and cannot be safely installed with current user permissions, use `assets/templates/` as fallback and mark every artifact as fallback.
4. Record goal, non-goals, constraints, assumptions, design, tasks, dependencies, owners, acceptance criteria, risks, verification evidence, and final status.
5. Create or update the task registry in the OpenSpec change directory. In fallback mode, use the project-local `.project-autopilot/` directory.
6. Claim tasks before execution using `scripts/task_registry.py`. Skip tasks already claimed, running, in review, done, cancelled, or fingerprint-duplicated.
7. Implement the smallest change that satisfies the spec and existing project style.
8. Run all applicable existing verification commands. Do not invent commands.
9. If verification fails, perform up to three rounds of root-cause analysis, minimal fix, and full re-verification.
10. Run independent review when the task is medium or large. Prefer read-only review. Fix evidence-backed issues, then re-run relevant checks.
11. Sync the source-of-truth spec/tasks/status, generate an acceptance report, and archive native OpenSpec changes when the lifecycle supports it.
12. Final response must report only completion result, main changes, acceptance evidence, and remaining real risk.

## OpenSpec Integration

Detect OpenSpec before writing spec files:

```bash
openspec --version
openspec --help
```

Also inspect project files for OpenSpec configuration and rules. If native OpenSpec exists, use its current commands and templates instead of hard-coded assumptions. If installation is safe and does not require sudo, install the official package with the project-appropriate package manager and verify the command. If installation is not possible, continue with fallback templates and clearly label the mode as fallback.

Never fabricate OpenSpec command output. Treat OpenSpec files as the decision and requirements source of truth. Agents must read them before work and sync them after work.

## Department Agents

Use real subagents only when the environment provides them. If real subagents are unavailable, perform the same department responsibilities sequentially in the main thread and say so in internal progress or final risk notes.

Use these global custom agents when available:

- `requirements-architecture-department.toml`
- `development-department.toml`
- `quality-assurance-department.toml`
- `independent-review-department.toml`

Title every delegated task as `XX部门：具体任务`. Maximum concurrency target is 4. Maximum depth is 1. Subagents must not create further subagents.

## Scripts

- `scripts/initialize_project.py`: initialize a native or fallback project-autopilot change workspace.
- `scripts/task_registry.py`: create stable IDs, fingerprints, and atomic claims.
- `scripts/detect_duplicate_tasks.py`: report repeated task fingerprints.
- `scripts/acceptance_report.py`: generate reports from the acceptance template without marking failed verification as done.
- `scripts/validate_skill.py`: validate this Skill installation.

Run scripts with the active Python interpreter and only standard-library dependencies.

## Verification Rules

Discover existing project commands from package files, lockfiles, CI files, build scripts, test configs, README, and project instructions. Use the commands that actually exist. If a check cannot run, record the reason, impact, and substitute evidence.

Do not mark work complete because code was generated. Completion requires applicable checks to pass or a clear, evidence-backed blocker.

## Skill Extraction

Create a candidate Skill only after a similar workflow succeeds at least twice and has stable inputs, steps, outputs, and acceptance criteria. Check existing Skills first. Remove project paths, accounts, secrets, and private data. Include positive triggers, negative triggers, and failure scenario tests.
