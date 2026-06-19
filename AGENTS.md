# project-autopilot Repository Instructions

## Project Goal

Maintain a publishable Codex Skill package that provides low-interaction project control, OpenSpec-aware workflow, dynamic department staffing, bounded subagent coordination, task de-duplication, and acceptance evidence.

## Team Roles

- Project lead: owns scope, staffing decisions, sequencing, acceptance, and final reporting. File edits allowed.
- Requirements architecture department: clarifies requirements, investigates impact, designs approach, and defines acceptance. Read-only by default.
- Development department: implements bounded changes and necessary tests. File edits allowed.
- Quality assurance department: designs and runs validation, reproduces failures, and records evidence. Read-only unless adding focused tests.
- Independent review department: checks correctness, safety, maintainability, missed requirements, and test gaps. Read-only by default.
- People operations department: recommends staffing changes, concurrency limits, ownership, and conflict fixes. No code edits.

## Validation Commands

Run these before claiming repository work is complete:

```bash
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
