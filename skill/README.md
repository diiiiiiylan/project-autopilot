# project-autopilot

Global user-level Codex Skill for low-interaction project control. It classifies task complexity, uses OpenSpec or fallback templates as the source of truth, coordinates bounded department agents, prevents duplicate task execution, runs verification, repairs failures, and produces acceptance evidence.

It also treats the first main project conversation as the project lead thread and uses a lightweight staffing model to add or remove departments only when project size, risk, and parallelism justify the token cost.

Install location: user Skill directory under `.agents/skills/project-autopilot`.

Validate with:

```bash
python scripts/validate_skill.py .
python -m unittest discover -s tests
```
