# OpenSpec Workflow

## Detection

Check for a native OpenSpec installation with `openspec --version` and `openspec --help`. Inspect project directories and instructions for existing OpenSpec layout, commands, templates, and rules.

## Native Mode

When OpenSpec exists, use its current command output and project rules. Do not overwrite native templates or assume a stale directory layout. The expected lifecycle is proposal/specification, implementation, verification, synchronization, and archive.

## Fallback Mode

When OpenSpec is missing and cannot be safely installed with user permissions, create:

```text
.project-autopilot/
  changes/<change-id>/
    proposal.md
    design.md
    tasks.md
    task-registry.json
    acceptance-report.md
```

Every fallback file must clearly state `Mode: fallback`. Fallback mode is a compatibility path, not proof that native OpenSpec commands ran.

## Required Record Fields

Record target, non-targets, constraints, assumptions, solution, tasks, dependencies, owner, acceptance criteria, risks, verification evidence, and final status for each change.
