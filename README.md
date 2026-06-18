# project-autopilot

`project-autopilot` is a global user-level Codex Skill for low-interaction project control.

It helps Codex handle non-trivial project work by choosing the right execution mode, using OpenSpec or fallback templates as the source of truth, coordinating bounded department agents, preventing duplicate task execution, running verification gates, repairing failures, and producing acceptance evidence.

## What It Includes

- `skill/`: the Codex Skill folder.
- `custom-agents/`: four bounded department agent configs.
- `video/`: Remotion source for the 30-second intro video.
- `media/project-autopilot-intro.mp4`: rendered intro video.
- `tools/privacy_scan.py`: repeatable privacy and hardcoded-path scan.

## Install

```bash
python tools/install.py
```

This copies:

- `skill/` to `$HOME/.agents/skills/project-autopilot/`
- `custom-agents/*.toml` to `${CODEX_HOME:-$HOME/.codex}/agents/`

## Validate

```bash
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
