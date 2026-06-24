---
name: project-autopilot
description: Skillbox leader for non-trivial Codex projects. Use for new projects, plan mode, cross-module features, larger modifications, public API or data changes, migrations, new dependencies, MCP/app integration, multi-agent coordination, external skill selection, or complete acceptance evidence. Do not use for explanation-only questions, spelling fixes, simple single-file edits, or clearly low-risk commands.
---

# Project Autopilot

Act as the project lead for the skillbox. Keep this Skill as the entrypoint and route work to the smallest set of isolated Skills and department agents that can finish the task with evidence.

For non-simple project work, take the lead automatically. Do not ask the user to manually choose departments. The lead detects task size, creates the minimum roster, assigns bounded work, keeps durable state, and reports evidence.

## Lead Thread

- Treat the first main conversation for a project as the project lead.
- Own product interpretation, scope, staffing, task ordering, acceptance, and final reporting.
- Record `initial-main-thread` as the lead marker when a real thread ID is unavailable.
- Do not let a subagent become lead. Subagents report evidence and blockers; the lead decides.

## Routing

1. Classify the work as small, medium, large, or enterprise.
2. For starts, plan mode, vague changes, or product creation, route to `$project-intake`.
3. For employee count, department overlap, or token cost control, route to `$project-staffing`.
4. For domain-specific work, route to `$project-domain-router`, then `$project-expert-selection`.
5. For long work, multi-agent work, resumes, compaction risk, or OpenSpec state sync, route to `$project-context-continuity`.
6. Before finalizing a non-trivial proposal, architecture proposal, external Skill integration, or MCP/app strategy, route to `$project-gpt-consultation`.
7. For strict engineering flow, route to `$project-superpowers-routing`.
8. For understanding-first, minimal, or agentic engineering style, route to `$project-karpathy-methods`.
9. For MCP, app, external program, or connector needs, route to `$project-mcp-orchestrator`.
10. For final checks, privacy scans, build/test evidence, or release readiness, route to `$project-acceptance`.
11. For dependency conflicts, missing Skills, duplicate Skills, or package hygiene, route to `$project-skillbox-governance`.

## Size Policy

- Small: main thread only. Do not create OpenSpec changes, staffing plans, or department agents unless the user explicitly asks for a formal project flow.
- Medium: project lead plus at most two bounded workers. Use a light brief, task list, and focused verification.
- Large: use OpenSpec or fallback templates as the source of truth. Use requirements architecture, development, QA, independent review, and optional people operations only when useful.
- Enterprise: add temporary specialists only when their inputs, outputs, allowed files, and acceptance evidence are independent.

## Durable State And Context

- Use OpenSpec as the source of truth for non-simple project decisions whenever available.
- If OpenSpec is unavailable, use `.project-autopilot/changes/<change-id>/` fallback state.
- Before context compression, long pauses, resumes, or major phase changes, update the durable state with current goal, assumptions, decisions, tasks, owners, verification evidence, blockers, and next actions.
- After compression or resume, read durable state and current files before continuing. Do not trust compressed chat context alone.
- If remaining context is low or unknown and the task is not small, prioritize state sync before more implementation.

## Permission Gates

When routing discovers that an external Skill, app, MCP, browser automation using a logged-in account, paid service, public publish action, or production operation is needed or would materially improve the main path, stop immediately and ask before continuing into that branch. Do not defer this to the final report.

State capability gained, capability lost if skipped, install location, network/account/cost needs, and rollback boundary. Continue only after explicit user approval.

Do not download Nuwa, Darwin, Karpathy packages, apps, or MCPs automatically. Installed local Skills may be used after existence and version/path checks.

## Completion

Before final response, route through `$project-acceptance` for applicable verification. Do not report completion until checks pass or a real blocker is documented with impact and substitute evidence.
