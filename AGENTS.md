# project-autopilot Repository Instructions

## Project Goal

Maintain a publishable Codex skillbox package that provides low-interaction project control, OpenSpec-aware workflow, dynamic department staffing, bounded subagent coordination, task de-duplication, MCP/app governance, external Skill dependency routing, and acceptance evidence.

## Team Roles

- Project lead: owns scope, staffing decisions, sequencing, acceptance, and final reporting. File edits allowed.
- Requirements architecture department: clarifies requirements, investigates impact, designs approach, and defines acceptance. Read-only by default.
- Development department: implements bounded changes and necessary tests. File edits allowed.
- Quality assurance department: designs and runs validation, reproduces failures, and records evidence. Read-only unless adding focused tests.
- Independent review department: checks correctness, safety, maintainability, missed requirements, and test gaps. Read-only by default.
- People operations department: recommends staffing changes, concurrency limits, ownership, and conflict fixes. No code edits.
- Methodology coordination department: routes stages to Superpowers, Karpathy, Nuwa, Darwin, or local fallback. No code edits.
- Domain expert department: identifies project domains and expert Skill gaps. File edits only when explicitly assigned a bounded implementation task.
- MCP connection department: discovers application/MCP candidates and prepares permission requests. No install/create actions without approval.
- Security supply chain department: checks external Skill, MCP, app, dependency, privacy, and publishing risk. Read-only by default.

## Validation Commands

Run these before claiming repository work is complete:

```bash
python tools/validate_package.py .
python -m unittest discover -s tests -v
python skill/scripts/validate_skill.py skill --agent-dir custom-agents
python -m unittest discover -s skill/tests -v
python tools/privacy_scan.py .
```

When changing Remotion video code, also run:

```bash
cd video
npm run render
```

## Safety Boundary

Do not commit `node_modules`, Python caches, local environment files, secrets, user-home paths, logs, or generated dependency caches. Run `tools/privacy_scan.py` before any GitHub push.

Do not download, install, enable, create, or call external Skills, applications, MCPs, or logged-in account tools without explicit user permission. The repository may track sources and prepare permission requests, but install actions must remain separate and auditable.
