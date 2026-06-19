# project-autopilot

`project-autopilot` is a global user-level Codex skillbox for low-interaction project control.

It helps Codex handle non-trivial project work by choosing the right execution mode, coordinating isolated Skills, using OpenSpec or fallback templates as the source of truth, coordinating bounded department agents, preventing duplicate task execution, running verification gates, repairing failures, and producing acceptance evidence.

The package now uses a skillbox model: `project-autopilot` is the project lead entrypoint, while intake, staffing, domain routing, expert selection, Superpowers routing, Karpathy methods, Nuwa/Darwin adapters, MCP orchestration, acceptance, and governance each live in their own Skill.

## What It Includes

- `skills/`: isolated Codex Skills that make up the skillbox.
- `skill/`: legacy compatibility Skill folder and validation scripts.
- `custom-agents/`: bounded department agent configs.
- `references/registries/`: tracked open-source Skill and MCP sources.
- `tools/validate_package.py`: package-level validation.
- `tools/dependency_audit.py`: read-only installed dependency audit.
- `tools/mcp_discovery.py`: read-only MCP source discovery.
- `video/`: Remotion source for the 30-second intro video.
- `media/project-autopilot-intro.mp4`: rendered intro video.
- `tools/privacy_scan.py`: repeatable privacy and hardcoded-path scan.

## Install

```bash
python tools/install.py
```

This copies:

- `skills/*` to `$HOME/.agents/skills/<skill-name>/`
- `custom-agents/*.toml` to `${CODEX_HOME:-$HOME/.codex}/agents/`
- a managed project-autopilot block into `${CODEX_HOME:-$HOME/.codex}/AGENTS.md`

Install does not download Nuwa, Darwin, Karpathy packages, apps, or MCPs. Those actions require explicit user permission.

## Validate

```bash
python tools/validate_package.py .
python -m unittest discover -s tests -v
python skill/scripts/validate_skill.py skill --agent-dir custom-agents
python -m unittest discover -s skill/tests -v
python tools/privacy_scan.py .
```

## Render The Video

```bash
cd video
npm install
npm run render
```

Rendered output is written to `media/project-autopilot-intro.mp4` from the repository root.

## Safety Notes

The repository is built from a sanitized release copy, not directly from a user home directory. Generated caches, local environment files, logs, and dependency folders are ignored.
