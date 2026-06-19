---
name: project-acceptance
description: Acceptance and finish Skill for discovering real build, lint, typecheck, test, privacy, security, artifact, and release checks. Use before claiming work is complete. Do not mark generated files as done without verification.
---

# Project Acceptance

Run the final evidence gate.

## Steps

1. Discover real commands from project instructions, package manifests, CI files, build scripts, test configs, README, and existing tooling.
2. Run applicable formatting, linting, type checking, unit, integration, end-to-end, build, smoke, privacy, and artifact checks.
3. If a check fails, perform up to three repair rounds: root cause, smallest fix, full re-run.
4. Record skipped checks with reason, impact, and substitute evidence.
5. Return final status, commands run, evidence, blocked checks, and remaining risk.

Never invent commands. Never call work complete just because files were generated.
