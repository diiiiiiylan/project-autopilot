# project-autopilot

`project-autopilot` is a global user-level Codex skillbox for low-interaction project control.

It helps Codex handle non-trivial project work by choosing the right execution mode, coordinating isolated Skills, using OpenSpec or fallback templates as the source of truth, coordinating bounded department agents, preventing duplicate task execution, running verification gates, repairing failures, and producing acceptance evidence.

The package now uses a skillbox model: `project-autopilot` is the project lead entrypoint, while intake, staffing, context continuity, domain routing, expert selection, GPT consultation, Superpowers routing, Karpathy methods, Nuwa/Darwin adapters, MCP orchestration, acceptance, and governance each live in their own Skill.

## What It Includes

- `skills/`: isolated Codex Skills that make up the skillbox.
- `skill/`: legacy compatibility Skill folder and validation scripts.
- `custom-agents/`: bounded department agent configs.
- `references/registries/`: tracked open-source Skill and MCP sources.
- `external/skills/`: approved vendored source snapshots for Nuwa and Darwin.
- `tools/validate_package.py`: package-level validation.
- `tools/dependency_audit.py`: read-only installed dependency audit.
- `tools/mcp_discovery.py`: read-only MCP source discovery.
- `skills/project-context-continuity/`: OpenSpec/fallback state continuity for long threads, compression, resume, and anti-hallucination handoff.
- `video/`: Remotion source for the 30-second intro video.
- `media/project-autopilot-intro.mp4`: rendered intro video.
- `tools/privacy_scan.py`: repeatable privacy and hardcoded-path scan.

## Install

```bash
python tools/install.py
```

This copies:

- `skills/*` to `$HOME/.agents/skills/<skill-name>/`
- approved external Skill snapshots from `external/skills/*` to `$HOME/.agents/skills/<external-skill-name>/`
- `custom-agents/*.toml` to `${CODEX_HOME:-$HOME/.codex}/agents/`
- a managed project-autopilot block into `${CODEX_HOME:-$HOME/.codex}/AGENTS.md`

Nuwa and Darwin source snapshots are included under `external/skills/` after explicit user approval. Future downloads, app installs, MCP enablement, custom MCP creation, or account-backed GPT/web calls must pause immediately and request explicit user permission before that branch continues.

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

External downloads, installs, MCP enablement, custom MCP creation, and account-backed web/tool calls are not deferred to final reporting. They require an immediate permission request at discovery time.

For non-simple project work, the user should not have to manually choose departments. The project lead auto-detects task size, keeps OpenSpec/fallback state current, and syncs durable state before compression or resume.
