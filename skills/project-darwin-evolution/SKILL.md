---
name: project-darwin-evolution
description: Darwin adapter Skill for improving existing Skills through approved experiments, scoring, and iteration. Use when a Skill needs optimization or evolution. Never download or run Darwin without explicit permission.
---

# Project Darwin Evolution

Use Darwin only as an approved external dependency for Skill evolution.

## Rules

- As soon as Darwin becomes necessary or materially beneficial, pause and ask before download, install, or invocation. Do not wait until final reporting.
- Define baseline behavior, candidate changes, scoring metrics, regression tests, and rollback before any evolution run.
- Keep experiments isolated from production Skills until validation passes.
- Do not evolve failed, one-off, sensitive, or poorly evidenced workflows.

If permission is denied, write a manual improvement plan and route validation to `$project-acceptance`.
